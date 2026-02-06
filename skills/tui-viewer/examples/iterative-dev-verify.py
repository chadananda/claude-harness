#!/usr/bin/env python3
"""
Iterative Development Verification Example

Use Case: Coder agent quickly verifying TUI changes during development

Workflow:
1. Run VHS tape to capture current TUI state
2. Analyze SVG screenshot programmatically
3. Verify colors, layout, and text
4. Report pass/fail with details
5. Cleanup processes

This runs in < 5 minutes for fast iteration cycles.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Missing dependency: pip install beautifulsoup4 lxml")
    sys.exit(1)


def run_vhs_capture(tape_path, timeout=30):
    """Execute VHS tape file with timeout."""
    print(f"🎬 Running VHS capture: {tape_path}")

    try:
        result = subprocess.run(
            ['vhs', tape_path],
            capture_output=True,
            timeout=timeout
        )

        if result.returncode != 0:
            stderr = result.stderr.decode()
            raise RuntimeError(f"VHS execution failed:\n{stderr}")

        print("✅ VHS capture completed")
        return True

    except subprocess.TimeoutExpired:
        print(f"⚠️  VHS timeout after {timeout}s")
        raise
    except FileNotFoundError:
        print("❌ VHS not found. Install with: brew install vhs")
        sys.exit(1)


def cleanup_processes(process_pattern="sample_tui.py"):
    """Kill any dangling TUI processes."""
    try:
        result = subprocess.run(
            ['pgrep', '-f', process_pattern],
            capture_output=True
        )

        if result.returncode == 0:
            pids = result.stdout.decode().strip().split('\n')
            print(f"🧹 Cleaning up {len(pids)} dangling process(es)")

            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)

            time.sleep(0.5)

    except FileNotFoundError:
        # pgrep not available (Windows), skip cleanup
        pass


def analyze_svg(svg_path):
    """Parse SVG and extract visual information."""
    if not os.path.exists(svg_path):
        raise FileNotFoundError(f"Screenshot not found: {svg_path}")

    with open(svg_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'xml')

    # Extract colors
    colors = {
        elem.get('fill')
        for elem in soup.find_all(attrs={'fill': True})
        if elem.get('fill') not in ['none', 'transparent', None]
    }

    # Extract text content
    texts = [
        t.text.strip()
        for t in soup.find_all('text')
        if t.text and t.text.strip()
    ]

    # Extract layout info (rectangles)
    rects = soup.find_all('rect')

    return {
        'colors': colors,
        'text': texts,
        'rect_count': len(rects),
        'svg': soup
    }


def verify_quick_check(svg_path, config):
    """Quick verification for iterative development."""
    print(f"\n🔍 Analyzing screenshot: {svg_path}")
    print("=" * 60)

    data = analyze_svg(svg_path)

    # Track results
    passed = []
    failed = []

    # 1. Verify colors (theme check)
    expected_colors = config.get('expected_colors', [])
    if expected_colors:
        missing = set(expected_colors) - data['colors']
        if missing:
            failed.append(f"Missing colors: {missing}")
        else:
            passed.append("Colors")

        # Show found colors
        print(f"\n🎨 Colors found ({len(data['colors'])}):")
        for color in sorted(data['colors'])[:10]:
            status = "✅" if color in expected_colors else "  "
            print(f"   {status} {color}")

    # 2. Verify text content
    expected_text = config.get('expected_text', [])
    if expected_text:
        content = ' '.join(data['text'])
        missing = [t for t in expected_text if t not in content]

        if missing:
            failed.append(f"Missing text: {missing}")
        else:
            passed.append("Text content")

        # Show found text
        print(f"\n📝 Text found ({len(data['text'])}):")
        for text in data['text'][:10]:
            status = "✅" if any(exp in text for exp in expected_text) else "  "
            print(f"   {status} {text}")

    # 3. Verify layout (basic check)
    min_rects = config.get('min_rects', 1)
    if data['rect_count'] >= min_rects:
        passed.append("Layout")
    else:
        failed.append(f"Insufficient layout elements: {data['rect_count']} < {min_rects}")

    print(f"\n📦 Layout: {data['rect_count']} rectangles")

    # Print results
    print(f"\n{'='*60}")
    print(f"📊 Verification Results")
    print(f"{'='*60}")

    if passed:
        print(f"\n✅ PASSED ({len(passed)}):")
        for item in passed:
            print(f"   - {item}")

    if failed:
        print(f"\n❌ FAILED ({len(failed)}):")
        for error in failed:
            print(f"   - {error}")

    # Overall result
    print(f"\n{'='*60}")
    if not failed:
        print("🎉 All checks PASSED! Visual verification successful.")
        print(f"📸 Screenshot: {svg_path}")
        return True
    else:
        print("⚠️  Some checks FAILED. Review screenshot and fix issues.")
        print(f"📸 Review: {svg_path}")
        return False


def main():
    """Main iterative development workflow."""
    print("\n" + "="*60)
    print("🚀 Iterative Development - Quick Visual Check")
    print("="*60)

    # Configuration
    tape_path = 'examples/iterative-dev-example.tape'
    svg_path = './tmp/screenshots/iterative-current-state.svg'

    # Expected visual characteristics (adjust for your TUI)
    config = {
        'expected_colors': [
            '#50fa7b',  # Dracula green
            '#ff79c6',  # Dracula pink
            '#f8f8f2',  # Dracula foreground
            '#282a36',  # Dracula background
        ],
        'expected_text': [
            'Settings',
            'Theme',
            'Menu',
        ],
        'min_rects': 3,  # Minimum layout elements
    }

    try:
        # Step 1: Ensure output directory exists
        os.makedirs('./tmp/screenshots', exist_ok=True)

        # Step 2: Run VHS capture
        run_vhs_capture(tape_path, timeout=30)

        # Step 3: Brief delay for file write
        time.sleep(0.5)

        # Step 4: Verify screenshot
        success = verify_quick_check(svg_path, config)

        # Step 5: Cleanup (critical!)
        cleanup_processes()

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"\n❌ Error: {e}")

        # Cleanup on error
        cleanup_processes()

        sys.exit(1)


if __name__ == '__main__':
    main()
