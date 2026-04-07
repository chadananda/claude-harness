---
name: ocr-extract
description: Extract high-quality Markdown from PDF documents using OCR and intelligent text correction. Handles scanned documents, poor-quality embedded text, academic papers with diacritical marks (especially Bahá'í transliteration), and structural formatting (headings, paragraphs, tables). Uses Tesseract OCR + fuzzy regex diacritical restoration + optional LLM structural analysis.
---

# OCR Extract Skill

## Purpose

Convert PDF documents to high-quality Markdown with:
- Accurate text extraction (OCR or embedded, auto-detected)
- Diacritical mark restoration (Bahá'í transliteration, Arabic/Persian terms)
- Structural formatting (headings, paragraph breaks, tables)
- YAML frontmatter metadata
- Cross-page paragraph joining and header/footer removal

## When to Use

- PDFs with poor or missing embedded text (scanned documents)
- Academic papers needing diacritical restoration
- Batch conversion of PDF collections to Markdown
- Any PDF-to-Markdown task requiring higher quality than basic text extraction

## Architecture

```
PDF → Phase A (rule-based, instant) → Phase B (LLM structural, optional) → Markdown

Phase A:
  1. Auto-detect: use embedded text if quality > 0.90, else Tesseract OCR
  2. Normalize quotes (curly → ASCII) — required before diacritical matching
  3. Join hyphenated line breaks (print artifacts)
  4. Fuzzy regex diacritical restoration (~100 patterns, catches 99%+ of Bahá'í terms)
  5. Macron → acute accent normalization
  6. Running header/footer removal
  7. Cross-page paragraph joining
  8. OCR artifact cleanup (®, ©, stray punctuation)

Phase B (optional, requires local LLM):
  1. Send numbered lines to LLM in ~120-line chunks
  2. LLM returns JSON formatting commands (heading, paragraph_break, join_previous, table)
  3. Commands applied programmatically — LLM never rewrites text content
  4. Result: properly formatted Markdown with ### headings, paragraph breaks, tables
```

## Dependencies

**Required:**
- Python 3.8+
- PyMuPDF (`pip install pymupdf`)
- Pillow (`pip install Pillow`)
- pytesseract (`pip install pytesseract`)
- Tesseract OCR (system install: `brew install tesseract`)

**Optional (for Phase B structural formatting):**
- Local LLM API (OpenAI-compatible endpoint)
- Recommended: Qwen3-32B or better for structural analysis

**For Persian/Arabic:**
- Tesseract language packs: `brew install tesseract-lang` or specific `tessdata` files

## Usage

### Single PDF
```bash
cd /path/to/project
python scripts/pipeline_v2.py document.pdf
# Output: tmp/v2_document.md

# Without LLM (regex-only, instant):
python scripts/pipeline_v2.py document.pdf --no-llm
```

### Programmatic
```python
from pipeline_v2 import process_pdf
from pathlib import Path

meta = {
    'title': 'Document Title',
    'author': 'Author Name',
    'series': 'Series Name',
    'volume': '1',
    'year': '2000',
}

md = process_pdf(Path('document.pdf'), meta, use_llm=True)
Path('output.md').write_text(md)
```

### Batch Processing
```python
from pipeline_v2 import process_pdf, extract_pdf_pages, PDF_DIR
from pathlib import Path
import json

# Load metadata (if available)
with open('metadata.json') as f:
    all_meta = json.load(f)

for pdf_path in sorted(PDF_DIR.glob('*.pdf')):
    meta = all_meta.get(pdf_path.name, {'title': pdf_path.stem})
    md = process_pdf(pdf_path, meta, use_llm=True)
    Path(f'md/{pdf_path.stem}.md').write_text(md)
```

## Configuration

Edit these constants in `pipeline_v2.py`:

| Constant | Default | Purpose |
|----------|---------|---------|
| `LLM_API` | `http://boss.taile945b3.ts.net:8000/v1/chat/completions` | LLM endpoint |
| `LLM_MODEL` | `"think"` | Model name for structural analysis |
| `LLM_DELAY` | `3` | Seconds between API calls |
| `LLM_TIMEOUT` | `300` | Max seconds per LLM request |
| `TESSERACT_DPI` | `300` | Resolution for page rendering |
| `LINES_PER_CHUNK` | `120` | Lines per LLM structural analysis chunk |

## Extending the Diacritical Dictionary

Edit `scripts/diacriticals.py` to add new patterns:

```python
# In _build_patterns():
add(r"\bYourTerm\b", "Corrected Term")

# Fuzzy patterns for OCR variants:
add(r"\bYour[Tt]erm\b", "Corrected Term")  # case variants
add(r"\bYo[uw]r\s*Term\b", "Corrected Term")  # OCR garbles
```

Run tests: `python diacriticals.py`

## Output Format

```markdown
---
title: "Document Title"
author: "Author Name"
series: "Series Name"
volume: 1
year: 2000
pages: "1-20"
source: "https://example.com/doc.pdf"
pdf: "document.pdf"
publisher: "'Irfán Colloquia"
---

# Document Title

*Author Name*

### First Section Heading

Body text with proper Bahá'í diacriticals...
```

## Quality Characteristics

- **Diacriticals**: 99.5%+ accuracy on Bahá'í terms via fuzzy regex (no LLM needed)
- **OCR quality**: Tesseract at 300 DPI, auto-detected language (eng/fas)
- **Structural**: LLM-assisted heading detection, paragraph splitting (when enabled)
- **Headers/footers**: Automatically removed (running headers, page numbers)
- **Cross-page**: Paragraphs joined across page boundaries
- **Hyphenation**: Print-artifact hyphens joined ("pil-\ngrimage" → "pilgrimage")

## Known Limitations

- Tables rendered as flat text (LLM can detect them but formatting is basic)
- Footnote superscripts lost in OCR (appear as punctuation artifacts)
- Some rare OCR garbles (~0.5%) not caught by regex patterns
- Drop caps on first page sometimes garbled
- LLM structural analysis inconsistent on timeout-prone chunks
