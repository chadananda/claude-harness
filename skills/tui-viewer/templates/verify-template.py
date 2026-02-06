#!/usr/bin/env python3
"""
SVG Verification Template

Customize this script to verify your TUI screenshots.

Usage:
    python verify-template.py path/to/screenshot.svg
"""

import sys
import os
from bs4 import BeautifulSoup


def analyze_svg(svg_path):
    """Parse SVG and extract visual data."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'xml')

    # Extract colors
    colors = {
        elem.get('fill')
        for elem in soup.find_all(attrs={'fill': True})
        if elem.get('fill') not in ['none', 'transparent', None]
    }

    # Extract text
    texts = [
        t.text.strip()
        for t in soup.find_all('text')
        if t.text and t.text.strip()
    ]

    return {
        'colors': colors,
        'text': texts,
        'svg': soup
    }


def verify_screenshot(svg_path):
    """
    Verify screenshot meets expectations.

    Customize the checks below for your TUI.
    """
    print(f"\n🔍 Analyzing: {svg_path}")
    print("=" * 60)

    if not os.path.exists(svg_path):
        print(f"❌ File not found: {svg_path}")
        return False

    data = analyze_svg(svg_path)

    passed = []
    failed = []

    # ===== CUSTOMIZE YOUR CHECKS HERE =====

    # Check 1: Expected colors
    EXPECTED_COLORS = [
        '#50fa7b',  # Example: Dracula green
        '#ff79c6',  # Example: Dracula pink
        # Add your expected colors
    ]

    missing_colors = set(EXPECTED_COLORS) - data['colors']
    if missing_colors:
        failed.append(f"Missing colors: {missing_colors}")
    else:
        passed.append("Colors")

    # Check 2: Expected text content
    EXPECTED_TEXT = [
        'Welcome',
        'Menu',
        # Add your expected text
    ]

    content = ' '.join(data['text'])
    missing_text = [t for t in EXPECTED_TEXT if t not in content]
    if missing_text:
        failed.append(f"Missing text: {missing_text}")
    else:
        passed.append("Text content")

    # Check 3: Minimum elements
    MIN_TEXT_ELEMENTS = 3  # Customize this
    if len(data['text']) < MIN_TEXT_ELEMENTS:
        failed.append(
            f"Too few text elements: {len(data['text'])} < {MIN_TEXT_ELEMENTS}"
        )
    else:
        passed.append("Element count")

    # =========================================

    # Print what was found
    print(f"\n🎨 Colors found ({len(data['colors'])}):")
    for color in sorted(data['colors'])[:10]:
        print(f"   {color}")

    print(f"\n📝 Text found ({len(data['text'])}):")
    for text in data['text'][:10]:
        print(f"   {text}")

    # Print results
    print(f"\n{'='*60}")
    print("📊 Verification Results")
    print("=" * 60)

    if passed:
        print(f"\n✅ PASSED ({len(passed)}):")
        for item in passed:
            print(f"   - {item}")

    if failed:
        print(f"\n❌ FAILED ({len(failed)}):")
        for error in failed:
            print(f"   - {error}")

    # Overall result
    print("\n" + "=" * 60)
    if not failed:
        print("🎉 All checks PASSED!")
        return True
    else:
        print("⚠️  Some checks FAILED")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python verify-template.py <svg_path>")
        sys.exit(1)

    svg_path = sys.argv[1]
    success = verify_screenshot(svg_path)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
