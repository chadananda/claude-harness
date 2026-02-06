#!/usr/bin/env python3
"""
Detect duplicate or overlapping documentation files
"""
import re
from pathlib import Path
from typing import List, Tuple, Set
from difflib import SequenceMatcher

def extract_headings(markdown_content: str) -> List[str]:
    """Extract all markdown headings from content"""
    headings = []
    for line in markdown_content.split('\n'):
        if line.strip().startswith('#'):
            # Remove # symbols and clean
            heading = line.lstrip('#').strip().lower()
            if heading:
                headings.append(heading)
    return headings

def calculate_heading_overlap(doc1_content: str, doc2_content: str) -> float:
    """Calculate percentage of overlapping headings (Jaccard similarity)"""
    headings1 = set(extract_headings(doc1_content))
    headings2 = set(extract_headings(doc2_content))
    if not headings1 or not headings2:
        return 0.0
    intersection = headings1 & headings2
    union = headings1 | headings2
    return len(intersection) / len(union) if union else 0.0

def calculate_content_similarity(doc1_content: str, doc2_content: str) -> float:
    """Calculate overall content similarity"""
    # Remove code blocks for fairer comparison
    doc1_clean = remove_code_blocks(doc1_content)
    doc2_clean = remove_code_blocks(doc2_content)
    matcher = SequenceMatcher(None, doc1_clean, doc2_clean)
    return matcher.ratio()

def remove_code_blocks(markdown: str) -> str:
    """Remove code blocks from markdown"""
    # Remove ```...``` blocks
    pattern = r'```[\s\S]*?```'
    return re.sub(pattern, '', markdown)

def categorize_overlap(similarity: float) -> Tuple[str, str]:
    """Categorize overlap level"""
    if similarity > 0.7:
        return 'DUPLICATE', 'Very high overlap, likely duplicates'
    elif similarity > 0.3:
        return 'OVERLAP', 'Moderate overlap, consider consolidation'
    else:
        return 'DISTINCT', 'Minimal overlap, keep separate'

def find_unique_headings(doc1_content: str, doc2_content: str) -> Tuple[Set[str], Set[str], Set[str]]:
    """Find unique and shared headings"""
    headings1 = set(extract_headings(doc1_content))
    headings2 = set(extract_headings(doc2_content))
    unique_to_1 = headings1 - headings2
    unique_to_2 = headings2 - headings1
    shared = headings1 & headings2
    return unique_to_1, unique_to_2, shared

def analyze_doc_pair(doc1: Path, doc2: Path) -> dict:
    """Analyze two documents for overlap"""
    try:
        with open(doc1, 'r', encoding='utf-8') as f1:
            content1 = f1.read()
        with open(doc2, 'r', encoding='utf-8') as f2:
            content2 = f2.read()
    except Exception as e:
        return {'error': str(e)}
    # Calculate similarities
    heading_sim = calculate_heading_overlap(content1, content2)
    content_sim = calculate_content_similarity(content1, content2)
    # Categorize
    category, description = categorize_overlap(heading_sim)
    # Find unique content
    unique1, unique2, shared = find_unique_headings(content1, content2)
    # Get file stats
    lines1 = len(content1.split('\n'))
    lines2 = len(content2.split('\n'))
    return {
        'doc1': str(doc1),
        'doc2': str(doc2),
        'heading_similarity': round(heading_sim, 2),
        'content_similarity': round(content_sim, 2),
        'category': category,
        'description': description,
        'lines': {
            'doc1': lines1,
            'doc2': lines2
        },
        'headings': {
            'unique_to_doc1': len(unique1),
            'unique_to_doc2': len(unique2),
            'shared': len(shared)
        },
        'unique_headings_doc1': sorted(list(unique1))[:5],  # First 5
        'unique_headings_doc2': sorted(list(unique2))[:5],  # First 5
        'shared_headings': sorted(list(shared))[:5]  # First 5
    }

def find_markdown_files(root: Path, exclude_dirs: Set[str] = None) -> List[Path]:
    """Find all markdown files in project"""
    if exclude_dirs is None:
        exclude_dirs = {'.git', 'node_modules', 'dist', 'build', 'target'}
    md_files = []
    for md_file in root.rglob('*.md'):
        # Skip if in excluded directory
        if any(excl in md_file.parts for excl in exclude_dirs):
            continue
        md_files.append(md_file)
    return sorted(md_files)

def detect_duplicates(root: Path, min_similarity: float = 0.3) -> List[dict]:
    """Detect duplicate or overlapping documentation"""
    md_files = find_markdown_files(root)
    results = []
    # Compare all pairs
    for i, doc1 in enumerate(md_files):
        for doc2 in md_files[i+1:]:
            analysis = analyze_doc_pair(doc1, doc2)
            if 'error' not in analysis and analysis['heading_similarity'] >= min_similarity:
                results.append(analysis)
    # Sort by similarity (highest first)
    results.sort(key=lambda x: x['heading_similarity'], reverse=True)
    return results

def main():
    """Main entry point"""
    import sys
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Detect duplicate documentation')
    parser.add_argument('path', nargs='?', default='.', help='Project root path')
    parser.add_argument('--min-similarity', type=float, default=0.3,
                       help='Minimum similarity threshold (0.0-1.0, default: 0.3)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()
    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    # Detect duplicates
    results = detect_duplicates(root, args.min_similarity)
    # Output
    if args.json:
        output = {
            'project_root': str(root),
            'min_similarity': args.min_similarity,
            'duplicates_found': len(results),
            'results': results
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        if not results:
            print(f"✅ No overlapping documentation found (minimum similarity: {args.min_similarity})")
            return
        print(f"Found {len(results)} potentially overlapping document pairs:\n")
        for i, result in enumerate(results, 1):
            print(f"[{i}] {result['category']}: {result['description']}")
            print(f"    Doc 1: {result['doc1']} ({result['lines']['doc1']} lines)")
            print(f"    Doc 2: {result['doc2']} ({result['lines']['doc2']} lines)")
            print(f"    Heading similarity: {result['heading_similarity']:.0%}")
            print(f"    Content similarity: {result['content_similarity']:.0%}")
            print(f"    Shared headings: {result['headings']['shared']}")
            if result['shared_headings']:
                print(f"    Examples: {', '.join(result['shared_headings'][:3])}")
            print(f"    Unique to Doc 1: {result['headings']['unique_to_doc1']}")
            print(f"    Unique to Doc 2: {result['headings']['unique_to_doc2']}")
            print()
        print("\nRecommendations:")
        for result in results:
            if result['category'] == 'DUPLICATE':
                print(f"  • Consider merging: {Path(result['doc1']).name} + {Path(result['doc2']).name}")
            elif result['category'] == 'OVERLAP':
                print(f"  • Review for consolidation: {Path(result['doc1']).name} + {Path(result['doc2']).name}")

if __name__ == '__main__':
    main()
