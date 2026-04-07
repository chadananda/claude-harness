#!/usr/bin/env python3
"""
PDF → Markdown OCR extraction pipeline.

Architecture:
  Phase A: Rule-based cleanup (zero tokens)
    - Tesseract OCR or embedded text extraction (auto-detected)
    - Hyphen joining (print artifacts)
    - Running header/footer removal (configurable patterns)
    - Diacritical dictionary (Bahá'í transliteration + fuzzy OCR correction)
    - Macron → acute accent normalization
    - Quote/footnote artifact cleanup
    - Cross-page paragraph joining
  Phase B: LLM structural formatting (minimal tokens, optional)
    - Send numbered lines to LLM
    - Get back JSON formatting commands (heading, paragraph_break, join, table)
    - Apply commands programmatically — LLM never rewrites text
  Phase C: Assembly
    - YAML frontmatter + formatted markdown

Usage:
    python pipeline_v2.py <pdf_file> [--no-llm] [--pdf-dir DIR] [--out-dir DIR]
"""

import fitz
from PIL import Image
import pytesseract
import requests
import json
import os
import re
import time
import unicodedata
import sys
from pathlib import Path
from diacriticals import restore_diacriticals, fix_ocr_punctuation, normalize_quotes, normalize_macrons

# ============================================================
# Configuration
# ============================================================

LLM_API = os.environ.get("LOCAL_LLM", "http://boss.taile945b3.ts.net:8000") + "/v1/chat/completions"
LLM_MODEL = os.environ.get("LLM_THINK_MODEL", "think")
LLM_DELAY = int(os.environ.get("LLM_DELAY", "3"))
LLM_TIMEOUT = int(os.environ.get("LLM_TIMEOUT", "300"))
TESSERACT_DPI = 300
LINES_PER_CHUNK = 120  # lines sent to LLM per structural analysis call

# Defaults — overridden by CLI args or caller
PDF_DIR = Path(os.environ.get("OCR_PDF_DIR", "."))
MD_DIR = Path(os.environ.get("OCR_MD_DIR", "."))
TMP_DIR = Path(os.environ.get("OCR_TMP_DIR", "./tmp"))

# ============================================================
# Phase A: Rule-based cleanup
# ============================================================

def assess_embedded_quality(text):
    """Score embedded text quality."""
    words = text.split()
    if len(words) < 10:
        return 0.0, False
    arabic_forms = len(re.findall(r'[\uFB50-\uFDFF\uFE70-\uFEFF]', text))
    is_persian = arabic_forms > 50
    single_chars = sum(1 for w in words if len(w) == 1 and w.isalpha() and w not in ('I', 'a', 'A'))
    score = 1.0 - (single_chars / len(words))
    if is_persian and arabic_forms > 100:
        score = min(score, 0.5)
    return score, is_persian


def extract_pdf_pages(pdf_path, force_ocr=False):
    """Extract text from all pages of a PDF. Returns list of (page_num, text, method)."""
    doc = fitz.open(str(pdf_path))
    is_persian = 'safini' in pdf_path.name.lower()
    pages = []
    for i, page in enumerate(doc):
        embedded = page.get_text("text")
        score, detected_persian = assess_embedded_quality(embedded)
        if is_persian:
            detected_persian = True
        if force_ocr or score < 0.90 or detected_persian:
            lang = 'fas' if detected_persian else 'eng'
            pix = page.get_pixmap(dpi=TESSERACT_DPI)
            img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang=lang)
            method = f"tesseract-{lang}"
        else:
            text = embedded
            method = "embedded"
        pages.append((i + 1, text, method))
    doc.close()
    return pages


def join_hyphens(text):
    """Join words hyphenated across line breaks (print artifact)."""
    # Pattern: word-fragment + hyphen + newline + continuation
    # But preserve real hyphens (e.g., "Kitáb-i-Aqdas", "well-known")
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Check if line ends with a hyphenated word fragment
        if (i + 1 < len(lines)
            and line.rstrip().endswith('-')
            and lines[i + 1].strip()
            and lines[i + 1].strip()[0].islower()):
            # Join: remove hyphen, concatenate with next line
            joined = line.rstrip()[:-1] + lines[i + 1].lstrip()
            result.append(joined)
            i += 2
        else:
            result.append(line)
            i += 1
    return '\n'.join(result)


def remove_headers_footers(text, is_persian=False):
    """Remove running headers, footers, and page numbers from a single page."""
    lines = text.split('\n')
    filtered = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\d{1,3}$', stripped):
            continue
        if re.match(r"^Lights of\s+[''\"]*Irf[áaā]n", stripped, re.IGNORECASE):
            continue
        if re.match(r'^\d{1,3}\s+Lights of', stripped):
            continue
        if re.match(r'^سفین[هة]\s*عرفان', stripped):
            continue
        if re.match(r'^سفينة\s*عرفان', stripped):
            continue
        if re.match(r"^'?Irf[áa]n\s+Occasional\s+Papers", stripped, re.IGNORECASE):
            continue
        filtered.append(line.rstrip())
    return '\n'.join(filtered)


def remove_inline_headers(text):
    """Remove running headers concatenated into text during page joining."""
    text = re.sub(r"\s*Lights of\s+[''\"]*Irf[áaā]n\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*Lights of\s+[''\"]*Irf[áaā]n\s+vol\.\s*\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*Lights of\s+[''\"]*Irf[áaā]n\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d{1,3}\s+Lights of\s+[''\"]*Irf[áaā]n.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*سفین[هة]\s*عرفان.*$", "", text, flags=re.MULTILINE)
    return text


def fix_quotes_and_footnotes(text):
    """Fix OCR quote artifacts and footnote markers."""
    # Double apostrophes
    text = re.sub(r"''+(?=[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜḤṬṢḌẒṆṚa-z])", "'", text)
    text = text.replace("''Irfán", "'Irfán").replace("''Irfan", "'Irfán")
    # Mangled footnote refs
    text = re.sub(r'\.["\']{2,}', '.', text)
    text = re.sub(r',"["\']{2,}', ',', text)
    # Missing apostrophe in Bahá'ís
    text = re.sub(r'\bBaháís\b', "Bahá'ís", text)
    # Normalize macrons to acute accents (non-Bahá'í transliteration)
    macron_to_acute = str.maketrans('āēīōūĀĒĪŌŪ', 'áéíóúÁÉÍÓÚ')
    text = text.translate(macron_to_acute)
    return text


def join_pages(pages_text):
    """Join page texts, handling cross-page paragraph continuations."""
    if not pages_text:
        return ""
    result = pages_text[0].rstrip()
    for i in range(1, len(pages_text)):
        curr = pages_text[i].strip()
        if not curr:
            continue
        prev_lines = [l for l in result.split('\n') if l.strip()]
        if not prev_lines:
            result += '\n\n' + curr
            continue
        last_line = prev_lines[-1].rstrip()
        curr_lines = [l for l in curr.split('\n') if l.strip()]
        if not curr_lines:
            continue
        first_line = curr_lines[0].strip()
        last_char = last_line[-1] if last_line else ''
        first_char = first_line[0] if first_line else ''

        if last_char == '-' and first_char.islower():
            result = result.rstrip()[:-1] + curr
        elif first_char.islower() or last_char == ',':
            result = result.rstrip() + ' ' + curr
        elif last_char not in '.!?:;"\')\u201d' and first_char.isupper():
            result = result.rstrip() + ' ' + curr
        else:
            result += '\n\n' + curr
    return result


def remove_first_page_header(text, title=""):
    """Remove OCR-captured title duplicate from the start of the document."""
    if not title:
        return text
    lines = text.split('\n')
    cleaned = []
    skip_count = 0
    title_lower = title.lower().strip()
    for line in lines:
        stripped = line.strip()
        if skip_count < 6 and stripped:
            skip_count += 1
            stripped_lower = stripped.lower()
            if (title_lower and (
                stripped_lower == title_lower
                or stripped_lower.startswith(title_lower[:30])
                or title_lower.startswith(stripped_lower[:30])
            )):
                continue
            if stripped_lower.startswith('by '):
                continue
            if ('irfán' in stripped_lower or 'irfan' in stripped_lower) and len(stripped) < 40:
                continue
        cleaned.append(line)
    return '\n'.join(cleaned)


LLM_DIACRITICAL_PROMPT = """You correct OCR errors in academic Bahá'í text. Fix garbled words using context. Restore proper Bahá'í transliteration diacriticals. Do NOT change meaning or structure. Do NOT add formatting. Return ONLY the corrected text."""


def llm_diacritical_correct(text):
    """Light LLM pass to fix OCR garbles that the dictionary can't catch."""
    if len(text.strip()) < 20:
        return text
    try:
        time.sleep(LLM_DELAY)
        r = requests.post(LLM_API, json={
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": LLM_DIACRITICAL_PROMPT},
                {"role": "user", "content": f"/no_think\n{text}"}
            ],
            "max_tokens": len(text) * 2,
            "temperature": 0.0,
        }, timeout=LLM_TIMEOUT)
        if r.status_code == 200:
            content = r.json()['choices'][0]['message']['content']
            content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
            return content
        return text
    except Exception as e:
        print(f"      LLM diacritical error: {e}")
        return text


def phase_a(pages, is_persian=False, title="", use_llm_diacritical=False):
    """Run all rule-based cleanup. Returns cleaned full text.

    If use_llm_diacritical=True, also runs LLM correction on Tesseract'd pages
    (needed for volumes 1-3 and Persian where OCR garbles are unpredictable).
    """
    # Per-page cleanup
    cleaned_pages = []
    for pnum, text, method in pages:
        text = remove_headers_footers(text, is_persian)
        text = join_hyphens(text)
        text = normalize_quotes(text)  # Must run before diacritical dictionary
        if not is_persian:
            text = restore_diacriticals(text)
            text = normalize_macrons(text)
            text = fix_ocr_punctuation(text)

        # LLM diacritical correction for OCR'd pages only
        if use_llm_diacritical and 'tesseract' in method:
            print(f"    LLM diacritical correction for page {pnum}...")
            sys.stdout.flush()
            text = llm_diacritical_correct(text)
            # Re-run dictionary after LLM (safety net)
            if not is_persian:
                text = normalize_quotes(text)
                text = restore_diacriticals(text)

        cleaned_pages.append(text)

    # Join pages
    full_text = join_pages(cleaned_pages)

    # Post-join cleanup
    full_text = remove_inline_headers(full_text)
    full_text = fix_quotes_and_footnotes(full_text)
    full_text = remove_first_page_header(full_text, title)

    # Collapse excessive blank lines
    full_text = re.sub(r'\n{4,}', '\n\n\n', full_text)
    full_text = '\n'.join(l.rstrip() for l in full_text.split('\n'))
    return full_text.strip()


# ============================================================
# Phase B: LLM structural formatting
# ============================================================

STRUCTURAL_PROMPT = """You are a markdown formatting specialist for OCR'd academic papers. You receive numbered lines of text from a scanned document. The text content is already correct — your job is ONLY to identify structural formatting issues.

Analyze the text and output a JSON array of formatting commands. Each command is an object with "line" (line number) and "action" (one of the types below).

Command types:
- {"line": N, "action": "heading3"} — This line is a SECTION HEADING, not regular text. See strict criteria below.
- {"line": N, "action": "paragraph_break"} — Insert a blank line BEFORE this line. Use when two paragraphs are run together without separation.
- {"line": N, "action": "join_previous"} — This line is an orphaned fragment that should be part of the previous paragraph. Remove the blank line before it.
- {"line": N, "action": "table_start", "end": M} — Lines N through M form a table.

STRICT rules for heading detection:
- A heading is a SECTION TITLE like "Introduction", "Places of Pilgrimage", "Conclusion", "Bibliography"
- Headings are STANDALONE short lines (under 50 chars), NOT followed by continuation on the same logical thought
- Headings are in Title Case or ALL CAPS
- A heading does NOT start with articles like "The", "A", "In", "It", "If" — those are paragraph starts
- A heading does NOT end with a comma, period, or other sentence punctuation
- A heading does NOT contain a complete sentence
- If in doubt, it is NOT a heading — be very conservative
- Quote attributions like "The Guardian adds," are NOT headings

Other rules:
- Only output the JSON array, nothing else
- Do NOT suggest changes to text content
- Be conservative — only flag things you're confident about
- If there are no issues in this chunk, output an empty array: []

Output ONLY valid JSON. No markdown code fences, no commentary."""


def llm_structural_analysis(numbered_text):
    """Send numbered lines to LLM, get back formatting commands."""
    try:
        time.sleep(LLM_DELAY)
        r = requests.post(LLM_API, json={
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": STRUCTURAL_PROMPT},
                {"role": "user", "content": f"/no_think\n{numbered_text}"}
            ],
            "max_tokens": 2000,
            "temperature": 0.0,
        }, timeout=LLM_TIMEOUT)

        if r.status_code != 200:
            print(f"    LLM API error {r.status_code}")
            return []

        content = r.json()['choices'][0]['message']['content']
        # Strip thinking tags if present
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
        # Extract JSON from response (might have markdown fences)
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return []
    except json.JSONDecodeError as e:
        print(f"    LLM JSON parse error: {e}")
        return []
    except Exception as e:
        print(f"    LLM error: {e}")
        return []


def phase_b(text, use_llm=True):
    """LLM structural analysis and formatting."""
    lines = text.split('\n')

    if not use_llm:
        return text

    # Collect all formatting commands
    all_commands = []

    for chunk_start in range(0, len(lines), LINES_PER_CHUNK):
        chunk_end = min(chunk_start + LINES_PER_CHUNK, len(lines))
        chunk_lines = lines[chunk_start:chunk_end]

        # Build numbered text
        numbered = '\n'.join(f"{chunk_start + i + 1}: {line}" for i, line in enumerate(chunk_lines))

        print(f"    Analyzing lines {chunk_start + 1}-{chunk_end}...")
        sys.stdout.flush()
        commands = llm_structural_analysis(numbered)
        all_commands.extend(commands)
        print(f"    Got {len(commands)} commands")
        sys.stdout.flush()

    # Apply commands
    return apply_formatting_commands(lines, all_commands)


def apply_formatting_commands(lines, commands):
    """Apply structural formatting commands to lines."""
    # Index commands by line number
    headings = set()
    para_breaks = set()
    joins = set()
    tables = []  # list of (start, end)

    for cmd in commands:
        line_num = cmd.get('line', 0)
        action = cmd.get('action', '')

        if action == 'heading3':
            headings.add(line_num)
        elif action == 'paragraph_break':
            para_breaks.add(line_num)
        elif action == 'join_previous':
            joins.add(line_num)
        elif action == 'table_start':
            tables.append((line_num, cmd.get('end', line_num + 5)))

    # Build table ranges for quick lookup
    table_lines = set()
    for start, end in tables:
        for i in range(start, end + 1):
            table_lines.add(i)

    # Apply
    result = []
    i = 0
    while i < len(lines):
        line_num = i + 1  # 1-indexed
        line = lines[i]

        # Check if this line should be joined to previous (remove blank before it)
        if line_num in joins and result and not result[-1].strip():
            result.pop()  # Remove the blank line

        # Check if paragraph break needed before this line
        if line_num in para_breaks:
            if result and result[-1].strip():
                result.append('')

        # Format as heading
        if line_num in headings:
            if result and result[-1].strip():
                result.append('')
            stripped = line.strip()
            if not stripped.startswith('###'):
                result.append(f'### {stripped}')
            else:
                result.append(line)
            # Ensure blank line after heading
            if i + 1 < len(lines) and lines[i + 1].strip():
                result.append('')
            i += 1
            continue

        # Table formatting
        if line_num in table_lines:
            # Collect all table lines
            table_start = line_num
            while table_start - 1 in table_lines:
                table_start -= 1
            table_end = line_num
            while table_end + 1 in table_lines:
                table_end += 1

            if line_num == table_start:
                # Format the whole table
                table_rows = []
                for j in range(table_start - 1, min(table_end, len(lines))):
                    table_rows.append(lines[j].strip())
                formatted = format_table(table_rows)
                if result and result[-1].strip():
                    result.append('')
                result.append(formatted)
                result.append('')
                i = table_end
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def format_table(rows):
    """Best-effort table formatting from flat text rows."""
    if not rows:
        return ''
    # For now, just preserve as-is with a note
    # Real table parsing would need column detection
    return '\n'.join(rows)


# ============================================================
# Phase C: Assembly
# ============================================================

def build_yaml_frontmatter(meta):
    def esc(s):
        if not s: return '""'
        s = str(s).strip().replace('"', '\\"')
        return f'"{s}"'
    lines = ['---']
    for key in ['title', 'author', 'series']:
        if meta.get(key):
            lines.append(f'{key}: {esc(meta[key])}')
    for key in ['volume', 'year', 'session']:
        if meta.get(key):
            lines.append(f'{key}: {meta[key]}')
    for key in ['pages', 'source', 'pdf']:
        if meta.get(key):
            lines.append(f'{key}: {esc(meta[key])}')
    lines.append("publisher: \"'Irfán Colloquia\"")
    lines.append('---')
    return '\n'.join(lines)


def assemble(frontmatter, title, author, body):
    parts = [frontmatter, '']
    parts.append(f'# {title}' if title else '# Untitled')
    if author:
        parts.append(f'\n*{author}*')
    parts.append('')
    parts.append(body)
    return '\n'.join(parts)


# ============================================================
# Main
# ============================================================

def process_pdf(pdf_path, meta, use_llm=True):
    """Full pipeline for a single PDF."""
    filename = pdf_path.name
    is_persian = 'safini' in filename.lower()
    title = meta.get('title', '')

    print(f"\n{'='*60}")
    print(f"Processing: {filename}")
    print(f"{'='*60}")

    # Phase A
    print("  Phase A: Extracting and rule-based cleanup...")
    sys.stdout.flush()
    pages = extract_pdf_pages(pdf_path)

    # Auto-detect if LLM diacritical correction is needed (OCR'd pages)
    ocr_pages = sum(1 for _, _, m in pages if 'tesseract' in m)
    needs_llm_diacritical = use_llm and ocr_pages > 0
    if needs_llm_diacritical:
        print(f"    {ocr_pages}/{len(pages)} pages OCR'd — will use LLM diacritical correction")
    text = phase_a(pages, is_persian, title, use_llm_diacritical=needs_llm_diacritical)
    print(f"    {len(pages)} pages → {len(text)} chars")
    sys.stdout.flush()

    # Phase B
    if use_llm:
        print("  Phase B: LLM structural analysis...")
        sys.stdout.flush()
        text = phase_b(text)

    # Phase C
    print("  Phase C: Assembly...")
    sys.stdout.flush()
    frontmatter = build_yaml_frontmatter(meta)
    md = assemble(frontmatter, title, meta.get('author', ''), text)

    # Final cleanup
    md = re.sub(r'\n{4,}', '\n\n\n', md)
    md = '\n'.join(l.rstrip() for l in md.split('\n'))

    print(f"  Done: {len(md)} chars")
    return md


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PDF → Markdown OCR extraction pipeline")
    parser.add_argument('pdf', help='PDF file path or filename (looked up in --pdf-dir)')
    parser.add_argument('--no-llm', action='store_true', help='Skip LLM structural formatting')
    parser.add_argument('--pdf-dir', type=str, default=None, help='Directory containing PDFs')
    parser.add_argument('--out-dir', type=str, default=None, help='Output directory for markdown')
    parser.add_argument('--tmp-dir', type=str, default=None, help='Temp directory for intermediate files')
    parser.add_argument('--title', type=str, default=None, help='Document title for frontmatter')
    parser.add_argument('--author', type=str, default=None, help='Author for frontmatter')
    parser.add_argument('--series', type=str, default=None, help='Series name for frontmatter')
    parser.add_argument('--volume', type=str, default=None, help='Volume number for frontmatter')
    parser.add_argument('--year', type=str, default=None, help='Year for frontmatter')
    args = parser.parse_args()

    # Override dirs if specified
    if args.pdf_dir:
        PDF_DIR = Path(args.pdf_dir)
    if args.out_dir:
        MD_DIR = Path(args.out_dir)
        MD_DIR.mkdir(parents=True, exist_ok=True)
    if args.tmp_dir:
        TMP_DIR = Path(args.tmp_dir)
        TMP_DIR.mkdir(parents=True, exist_ok=True)

    pdf_path = Path(args.pdf) if Path(args.pdf).exists() else PDF_DIR / args.pdf
    if not pdf_path.exists():
        print(f"Error: {pdf_path} not found")
        sys.exit(1)

    meta = {'title': args.title or pdf_path.stem, 'pdf': pdf_path.name}
    if args.author: meta['author'] = args.author
    if args.series: meta['series'] = args.series
    if args.volume: meta['volume'] = args.volume
    if args.year: meta['year'] = args.year

    md = process_pdf(pdf_path, meta, use_llm=not args.no_llm)

    out_dir = MD_DIR if args.out_dir else TMP_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{pdf_path.stem}.md"
    out.write_text(md, encoding='utf-8')
    print(f"\nOutput: {out}")
