# SVG Analysis and Verification

## Why SVG?

**SVG = Scalable Vector Graphics = XML = Programmatically Analyzable**

SVG screenshots of TUIs contain:
- All text content (`<text>` elements)
- All colors (`fill`, `stroke` attributes)
- Layout positions (`x`, `y`, `width`, `height`)
- Visual structure (rectangles, paths, groups)

This makes them perfect for automated verification!

## SVG Structure Example

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">
  <!-- Background -->
  <rect x="0" y="0" width="800" height="600" fill="#282a36"/>

  <!-- Text elements with colors and positions -->
  <text x="10" y="20" fill="#f8f8f2" font-family="monospace">Welcome to My TUI</text>
  <text x="10" y="40" fill="#50fa7b" font-family="monospace">› Option 1</text>
  <text x="10" y="60" fill="#f8f8f2" font-family="monospace">  Option 2</text>

  <!-- Border/frame -->
  <rect x="5" y="5" width="790" height="590" fill="none" stroke="#ff79c6"/>
</svg>
```

## Parsing SVG

### Python with BeautifulSoup

**Installation:**
```bash
pip install beautifulsoup4 lxml
```

**Basic parsing:**
```python
from bs4 import BeautifulSoup

def parse_svg(svg_path):
    """Parse SVG file and return BeautifulSoup object."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'xml')

# Usage
soup = parse_svg('screenshot.svg')
```

### Extract All Information

```python
def analyze_svg(svg_path):
    """Extract all visual information from SVG."""
    soup = parse_svg(svg_path)

    # Extract colors (fill attributes)
    fill_colors = {
        elem.get('fill')
        for elem in soup.find_all(attrs={'fill': True})
        if elem.get('fill') not in ['none', 'transparent', None]
    }

    # Extract colors (stroke attributes)
    stroke_colors = {
        elem.get('stroke')
        for elem in soup.find_all(attrs={'stroke': True})
        if elem.get('stroke') not in ['none', 'transparent', None]
    }

    all_colors = fill_colors | stroke_colors

    # Extract text content
    texts = [
        t.text.strip()
        for t in soup.find_all('text')
        if t.text and t.text.strip()
    ]

    # Extract rectangles (layout)
    rects = [
        {
            'x': r.get('x'),
            'y': r.get('y'),
            'width': r.get('width'),
            'height': r.get('height'),
            'fill': r.get('fill'),
            'stroke': r.get('stroke'),
        }
        for r in soup.find_all('rect')
    ]

    # Extract text elements (with positions and colors)
    text_elements = [
        {
            'text': t.text.strip() if t.text else '',
            'x': t.get('x'),
            'y': t.get('y'),
            'fill': t.get('fill'),
            'font-family': t.get('font-family'),
        }
        for t in soup.find_all('text')
    ]

    return {
        'colors': all_colors,
        'text': texts,
        'rects': rects,
        'text_elements': text_elements,
        'svg': soup,
    }
```

## Verification Functions

### Color Verification

```python
def verify_colors(svg_path, expected_colors):
    """Verify expected colors are present in SVG."""
    data = analyze_svg(svg_path)
    missing = set(expected_colors) - data['colors']

    if missing:
        found = ', '.join(sorted(data['colors']))
        raise AssertionError(
            f"Missing colors: {missing}\n"
            f"Found colors: {found}"
        )

    return True

# Usage
verify_colors(
    'screenshot.svg',
    ['#50fa7b', '#ff79c6', '#282a36']  # Dracula theme colors
)
```

### Text Content Verification

```python
def verify_text(svg_path, expected_texts, exact=False):
    """Verify expected text content is present."""
    data = analyze_svg(svg_path)

    if exact:
        # Exact match required
        if set(expected_texts) != set(data['text']):
            raise AssertionError(
                f"Text mismatch:\n"
                f"Expected: {expected_texts}\n"
                f"Found: {data['text']}"
            )
    else:
        # Partial match - all expected texts must be present
        content = ' '.join(data['text'])
        missing = [t for t in expected_texts if t not in content]

        if missing:
            raise AssertionError(
                f"Missing text: {missing}\n"
                f"Found: {data['text']}"
            )

    return True

# Usage
verify_text('screenshot.svg', ['Welcome', 'Menu', 'Options'])
```

### Layout Verification

```python
def verify_layout(svg_path, checks=None):
    """Verify layout structure."""
    data = analyze_svg(svg_path)

    # Default checks
    if checks is None:
        checks = {
            'has_border': True,
            'has_background': True,
            'min_text_elements': 1,
        }

    # Check for border (rect with stroke)
    if checks.get('has_border'):
        borders = [r for r in data['rects'] if r['stroke']]
        assert len(borders) > 0, "No border found"

    # Check for background (rect with fill)
    if checks.get('has_background'):
        backgrounds = [r for r in data['rects'] if r['fill']]
        assert len(backgrounds) > 0, "No background found"

    # Check minimum text elements
    if 'min_text_elements' in checks:
        min_count = checks['min_text_elements']
        assert len(data['text']) >= min_count, \
            f"Expected at least {min_count} text elements, found {len(data['text'])}"

    return True

# Usage
verify_layout('screenshot.svg', {
    'has_border': True,
    'has_background': True,
    'min_text_elements': 5,
})
```

### Position Verification

```python
def verify_text_positions(svg_path):
    """Verify text elements are positioned correctly."""
    data = analyze_svg(svg_path)
    text_elements = data['text_elements']

    if len(text_elements) < 2:
        return True  # Not enough elements to verify order

    # Check that text elements are ordered top-to-bottom
    for i in range(len(text_elements) - 1):
        current = text_elements[i]
        next_elem = text_elements[i + 1]

        current_y = float(current['y']) if current['y'] else 0
        next_y = float(next_elem['y']) if next_elem['y'] else 0

        # Next element should be below current (higher y value)
        if next_y < current_y:
            raise AssertionError(
                f"Text order incorrect: '{current['text']}' (y={current_y}) "
                f"is above '{next_elem['text']}' (y={next_y})"
            )

    return True
```

### Theme Verification

```python
# Common TUI themes
THEMES = {
    'dracula': {
        'bg': '#282a36',
        'fg': '#f8f8f2',
        'comment': '#6272a4',
        'cyan': '#8be9fd',
        'green': '#50fa7b',
        'orange': '#ffb86c',
        'pink': '#ff79c6',
        'purple': '#bd93f9',
        'red': '#ff5555',
        'yellow': '#f1fa8c',
    },
    'nord': {
        'bg': '#2e3440',
        'fg': '#d8dee9',
        'blue': '#88c0d0',
        'cyan': '#8fbcbb',
        'green': '#a3be8c',
        'orange': '#d08770',
        'purple': '#b48ead',
        'red': '#bf616a',
        'yellow': '#ebcb8b',
    },
    'solarized-dark': {
        'bg': '#002b36',
        'fg': '#839496',
        'blue': '#268bd2',
        'cyan': '#2aa198',
        'green': '#859900',
        'magenta': '#d33682',
        'orange': '#cb4b16',
        'red': '#dc322f',
        'violet': '#6c71c4',
        'yellow': '#b58900',
    },
}

def verify_theme(svg_path, theme_name, min_colors=2):
    """Verify TUI uses expected theme colors."""
    if theme_name not in THEMES:
        raise ValueError(f"Unknown theme: {theme_name}")

    data = analyze_svg(svg_path)
    theme_colors = set(THEMES[theme_name].values())
    found_theme_colors = data['colors'] & theme_colors

    if len(found_theme_colors) < min_colors:
        raise AssertionError(
            f"Theme '{theme_name}' not found. "
            f"Expected at least {min_colors} theme colors, "
            f"found {len(found_theme_colors)}: {found_theme_colors}"
        )

    return True

# Usage
verify_theme('screenshot.svg', 'dracula', min_colors=3)
```

## Complete Verification Example

```python
def comprehensive_verification(svg_path, config):
    """Run comprehensive verification on SVG screenshot."""
    results = {
        'passed': [],
        'failed': [],
    }

    # Color verification
    if 'expected_colors' in config:
        try:
            verify_colors(svg_path, config['expected_colors'])
            results['passed'].append('Colors')
        except AssertionError as e:
            results['failed'].append(('Colors', str(e)))

    # Text verification
    if 'expected_text' in config:
        try:
            verify_text(svg_path, config['expected_text'])
            results['passed'].append('Text content')
        except AssertionError as e:
            results['failed'].append(('Text content', str(e)))

    # Layout verification
    if 'layout_checks' in config:
        try:
            verify_layout(svg_path, config['layout_checks'])
            results['passed'].append('Layout')
        except AssertionError as e:
            results['failed'].append(('Layout', str(e)))

    # Theme verification
    if 'theme' in config:
        try:
            verify_theme(svg_path, config['theme'])
            results['passed'].append(f"Theme ({config['theme']})")
        except AssertionError as e:
            results['failed'].append((f"Theme ({config['theme']})", str(e)))

    # Print results
    print(f"\n📊 Verification Results for {svg_path}")
    print(f"{'='*60}")

    if results['passed']:
        print(f"\n✅ PASSED ({len(results['passed'])}):")
        for item in results['passed']:
            print(f"   - {item}")

    if results['failed']:
        print(f"\n❌ FAILED ({len(results['failed'])}):")
        for item, error in results['failed']:
            print(f"   - {item}: {error}")

    # Return overall result
    return len(results['failed']) == 0

# Usage
config = {
    'expected_colors': ['#50fa7b', '#ff79c6', '#282a36'],
    'expected_text': ['Welcome', 'Menu', 'Settings'],
    'layout_checks': {
        'has_border': True,
        'min_text_elements': 3,
    },
    'theme': 'dracula',
}

success = comprehensive_verification('screenshot.svg', config)
sys.exit(0 if success else 1)
```

## Baseline Comparison (Visual Regression)

```python
def compare_with_baseline(current_svg, baseline_svg, tolerance=0):
    """Compare current screenshot with baseline."""
    current_data = analyze_svg(current_svg)
    baseline_data = analyze_svg(baseline_svg)

    differences = []

    # Compare colors
    color_diff = (current_data['colors'] - baseline_data['colors'],
                  baseline_data['colors'] - current_data['colors'])

    if color_diff[0]:  # New colors
        differences.append(f"New colors: {color_diff[0]}")
    if color_diff[1]:  # Removed colors
        differences.append(f"Removed colors: {color_diff[1]}")

    # Compare text
    text_diff = (set(current_data['text']) - set(baseline_data['text']),
                 set(baseline_data['text']) - set(current_data['text']))

    if text_diff[0]:  # New text
        differences.append(f"New text: {text_diff[0]}")
    if text_diff[1]:  # Removed text
        differences.append(f"Removed text: {text_diff[1]}")

    # Compare layout count
    if len(current_data['rects']) != len(baseline_data['rects']):
        differences.append(
            f"Rectangle count changed: "
            f"{len(baseline_data['rects'])} → {len(current_data['rects'])}"
        )

    # Return result
    if differences and tolerance == 0:
        raise AssertionError(
            f"Visual regression detected:\n" +
            "\n".join(f"  - {d}" for d in differences)
        )

    return differences

# Usage
try:
    diffs = compare_with_baseline('current.svg', 'baseline.svg')
    if diffs:
        print("⚠️  Visual differences found (within tolerance):")
        for diff in diffs:
            print(f"  - {diff}")
    else:
        print("✅ No visual differences")
except AssertionError as e:
    print(f"❌ Visual regression: {e}")
```

## Debugging: Visual Diff Output

```python
def generate_diff_report(current_svg, baseline_svg, output_html='diff-report.html'):
    """Generate HTML report comparing two SVGs."""
    current_data = analyze_svg(current_svg)
    baseline_data = analyze_svg(baseline_svg)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Visual Diff Report</title>
        <style>
            body {{ font-family: monospace; padding: 20px; }}
            .side-by-side {{ display: flex; gap: 20px; }}
            .panel {{ flex: 1; border: 1px solid #ccc; padding: 10px; }}
            .diff {{ background: #ffeb3b; }}
            .added {{ background: #c8e6c9; }}
            .removed {{ background: #ffcdd2; }}
        </style>
    </head>
    <body>
        <h1>Visual Diff Report</h1>

        <div class="side-by-side">
            <div class="panel">
                <h2>Baseline</h2>
                <embed src="{baseline_svg}" width="800" height="600">
            </div>
            <div class="panel">
                <h2>Current</h2>
                <embed src="{current_svg}" width="800" height="600">
            </div>
        </div>

        <h2>Differences</h2>

        <h3>Colors</h3>
        <p class="added">Added: {current_data['colors'] - baseline_data['colors']}</p>
        <p class="removed">Removed: {baseline_data['colors'] - current_data['colors']}</p>

        <h3>Text</h3>
        <p class="added">Added: {set(current_data['text']) - set(baseline_data['text'])}</p>
        <p class="removed">Removed: {set(baseline_data['text']) - set(current_data['text'])}</p>

        <h3>Layout</h3>
        <p>Rectangles: {len(baseline_data['rects'])} → {len(current_data['rects'])}</p>
    </body>
    </html>
    """

    with open(output_html, 'w') as f:
        f.write(html)

    print(f"📊 Diff report generated: {output_html}")

# Usage
generate_diff_report('current.svg', 'baseline.svg')
```

## Quick Verification Script

```python
#!/usr/bin/env python3
"""
Quick SVG verification script.

Usage:
    python verify_svg.py screenshot.svg
    python verify_svg.py screenshot.svg --colors '#50fa7b,#ff79c6'
    python verify_svg.py screenshot.svg --text 'Welcome,Menu,Settings'
"""

import sys
import argparse
from bs4 import BeautifulSoup

def quick_verify(svg_path, expected_colors=None, expected_text=None):
    """Quick verification with command-line args."""
    # Parse SVG
    with open(svg_path) as f:
        soup = BeautifulSoup(f.read(), 'xml')

    # Extract data
    colors = {e.get('fill') for e in soup.find_all(attrs={'fill': True})}
    texts = [t.text.strip() for t in soup.find_all('text') if t.text.strip()]

    print(f"\n🔍 Analyzing {svg_path}")
    print(f"{'='*60}")

    # Display colors
    print(f"\n🎨 Colors found ({len(colors)}):")
    for color in sorted(colors):
        if color not in ['none', 'transparent']:
            print(f"   - {color}")

    # Display text
    print(f"\n📝 Text content ({len(texts)}):")
    for text in texts[:10]:  # First 10
        print(f"   - {text}")
    if len(texts) > 10:
        print(f"   ... and {len(texts) - 10} more")

    # Verify if specified
    success = True

    if expected_colors:
        missing = set(expected_colors) - colors
        if missing:
            print(f"\n❌ Missing colors: {missing}")
            success = False
        else:
            print(f"\n✅ All expected colors found")

    if expected_text:
        content = ' '.join(texts)
        missing = [t for t in expected_text if t not in content]
        if missing:
            print(f"\n❌ Missing text: {missing}")
            success = False
        else:
            print(f"\n✅ All expected text found")

    return success

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verify SVG screenshot')
    parser.add_argument('svg_path', help='Path to SVG file')
    parser.add_argument('--colors', help='Expected colors (comma-separated)')
    parser.add_argument('--text', help='Expected text (comma-separated)')

    args = parser.parse_args()

    expected_colors = args.colors.split(',') if args.colors else None
    expected_text = args.text.split(',') if args.text else None

    success = quick_verify(args.svg_path, expected_colors, expected_text)
    sys.exit(0 if success else 1)
```

## Summary

SVG analysis enables:

✅ **Automated color verification** - Check themes and palettes
✅ **Text content validation** - Verify expected UI text
✅ **Layout structure checks** - Ensure proper positioning
✅ **Visual regression detection** - Compare with baselines
✅ **Theme verification** - Validate color schemes

**Key insight:** SVG is XML, making it fully program programmatically analyzable!

**Next:** See [pty-background.md](pty-background.md) for running TUIs in background processes.
