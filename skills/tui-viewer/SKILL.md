---
name: tui-viewer
description: Universal guide for capturing, analyzing, and verifying TUI (Terminal User Interface) screenshots across any language or framework. Use when building, testing, or refactoring TUIs where visual verification of colors, layout, spacing, and interactive states is needed.
license: MIT
---

# TUI Viewer - Universal Terminal UI Visual Verification

## Overview

**Problem:** Agents can't "see" Terminal User Interfaces (TUIs), making it impossible to verify that colors, layout, spacing, and interactive states are correct.

**Solution:** This skill teaches agents how to capture high-fidelity screenshots of TUIs (preserving colors and layout) and programmatically analyze them to verify visual correctness.

**Works with:** Python, Node.js, Go, Rust, or ANY language/framework that produces terminal output.

---

## 🎯 Primary Use Cases

### Use Case 1: Iterative Development (Coder Agent)

**Scenario:** Agent is building a TUI and needs fast visual feedback to verify code changes work correctly.

**Workflow:**
```
1. Write/modify TUI code
2. Create VHS tape with navigation sequence to reach target screen
3. Run tape → Generate SVG screenshot
4. Analyze SVG programmatically:
   - Colors correct?
   - Layout good?
   - Text present?
5. If incorrect: Fix code, repeat (< 5 min cycle)
6. If correct: Continue to next feature
```

**Key Requirements:**
- Fast iteration (< 5 minutes per cycle)
- Navigate to specific screens (menus, dialogs, forms)
- Time delays for animations/async operations
- Proper process cleanup (no dangling processes)

### Use Case 2: E2E/Visual/Behavioral Testing (Testing Agent)

**Scenario:** Agent creates comprehensive test suites that verify TUI behavior and appearance using standard test frameworks.

**Workflow:**
```
1. Generate test files (pytest, jest, etc.)
2. Each test uses VHS to:
   - Launch TUI
   - Navigate through user flows
   - Capture screenshots at key states
3. Programmatically verify screenshots:
   - Expected colors present?
   - Layout matches baseline?
   - Interactive states correct?
4. Integrate with test assertions
5. Store screenshots as test artifacts
6. Generate test reports with visual evidence
```

**Key Requirements:**
- Integration with pytest, jest, go test, etc.
- Baseline comparison (visual regression)
- Responsive testing (multiple terminal sizes)
- Theme testing (dark/light modes)
- Proper cleanup (terminate processes after tests)

---

## 🚀 Quick Start

### Installation

**Minimum (VHS only - recommended):**
```bash
# macOS
brew install vhs

# Linux
go install github.com/charmbracelet/vhs@latest

# Docker (cross-platform)
docker pull ghcr.io/charmbracelet/vhs
```

**Complete (all options):**
```bash
# VHS
brew install vhs

# Python tools (for pexpect method)
pip install pexpect pyte beautifulsoup4 lxml

# Node.js tools (for svg conversion)
npm install -g svg-term-cli

# asciinema (alternative capture method)
pip install asciinema
```

### Basic Example: Iterative Development

**Create a tape file (iterative-test.tape):**
```tape
Output ./tmp/screenshots/current-state.svg

Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"

# Launch TUI
Type "python my_tui_app.py"
Enter
Sleep 2s

# Navigate to target screen
Type "down"    # Navigate down
Sleep 500ms
Type "down"    # Navigate down again
Sleep 500ms
Type "enter"   # Select option
Sleep 1s

# Capture final state
Screenshot ./tmp/screenshots/target-screen.png

# CRITICAL: Cleanup - terminate process
Ctrl+C
Sleep 500ms
```

**Run and verify:**
```bash
# 1. Execute tape
vhs iterative-test.tape

# 2. Verify colors/layout
python verify_screenshot.py ./tmp/screenshots/current-state.svg

# Output: ✅ Colors correct, ✅ Layout verified
```

### Basic Example: E2E Test Integration

**pytest test file:**
```python
# tests/test_tui_navigation.py

import subprocess
import os
from bs4 import BeautifulSoup

def test_menu_navigation():
    """Test navigating through main menu."""
    # Run VHS tape
    result = subprocess.run(
        ['vhs', 'tests/tapes/menu-navigation.tape'],
        capture_output=True,
        timeout=30  # Guard against hanging
    )
    assert result.returncode == 0, "VHS execution failed"

    # Verify screenshot
    svg_path = './tmp/screenshots/menu-screen.svg'
    assert os.path.exists(svg_path), "Screenshot not generated"

    # Parse SVG and verify
    with open(svg_path) as f:
        soup = BeautifulSoup(f.read(), 'xml')

    # Verify expected colors (Dracula theme)
    colors = {elem.get('fill') for elem in soup.find_all(fill=True)}
    assert '#50fa7b' in colors, "Green accent color missing"
    assert '#ff79c6' in colors, "Pink highlight missing"

    # Verify text content
    text_content = ' '.join(t.text for t in soup.find_all('text'))
    assert 'Main Menu' in text_content
    assert 'Option 1' in text_content

    # Cleanup: VHS should have sent Ctrl+C, but verify
    # No python processes should remain
    ps_result = subprocess.run(
        ['pgrep', '-f', 'my_tui_app.py'],
        capture_output=True
    )
    assert ps_result.returncode != 0, "TUI process still running!"
```

---

## 📚 Capture Methods

### Method 1: VHS (Recommended - Universal)

**Pros:**
- ✅ Works with ANY TUI (language-agnostic)
- ✅ Declarative `.tape` files (version controllable)
- ✅ Built-in process termination (Ctrl+C)
- ✅ Multiple output formats (PNG, GIF, SVG via fork)
- ✅ CI/CD friendly

**Use for:** All use cases, especially iterative development and E2E tests

**Reference:** [reference/vhs-guide.md](reference/vhs-guide.md)

### Method 2: asciinema + svg-term-cli

**Pros:**
- ✅ Record once, convert with different themes
- ✅ Standard `.cast` format (JSON)
- ✅ Mature ecosystem

**Use for:** Recording sessions for documentation, alternative to VHS

**Reference:** [reference/asciinema-guide.md](reference/asciinema-guide.md)

### Method 3: Language-Specific PTY Control

**Pros:**
- ✅ Direct programmatic control
- ✅ Precise timing and state verification
- ✅ Integrated into language-specific tests

**Use for:** Deep integration with language-specific test frameworks

**Reference:** [reference/pty-background.md](reference/pty-background.md)

---

## 🎬 VHS Tape File Reference

### Basic Structure

```tape
# Output files
Output ./tmp/screenshots/output.svg    # SVG (via fork)
Output ./tmp/screenshots/output.gif    # GIF
Output ./tmp/screenshots/output.png    # PNG

# Terminal configuration
Set FontSize 14
Set Width 1000              # Terminal width in pixels
Set Height 600              # Terminal height in pixels
Set Theme "Dracula"         # Color theme
Set TypingSpeed 100ms       # Typing delay (default: 50ms)

# Commands
Type "command"              # Type text
Enter                       # Press Enter
Sleep 2s                    # Wait (s=seconds, ms=milliseconds)
Ctrl+C                      # Send Ctrl+C
Backspace                   # Delete character
Tab                         # Tab key
Down                        # Arrow down (also: Up, Left, Right)
Screenshot file.png         # Capture frame

# Cleanup (CRITICAL)
Ctrl+C                      # Terminate process
Sleep 500ms                 # Wait for termination
```

### Navigation Patterns

**Menu navigation:**
```tape
# Navigate down 3 times, select
Type "down"
Sleep 300ms
Type "down"
Sleep 300ms
Type "down"
Sleep 300ms
Type "enter"
Sleep 1s
```

**Form filling:**
```tape
# Fill form fields
Type "John Doe"
Sleep 200ms
Tab
Sleep 200ms
Type "john@example.com"
Sleep 200ms
Tab
Sleep 200ms
Type "password123"
Sleep 200ms
Enter
Sleep 1s
```

**Multi-step workflow:**
```tape
# Step 1: Login
Type "python app.py"
Enter
Sleep 2s
Screenshot step1-login.png

# Step 2: Navigate to settings
Type "s"  # Keyboard shortcut
Sleep 500ms
Screenshot step2-settings.png

# Step 3: Change theme
Type "down"
Sleep 300ms
Type "enter"
Sleep 1s
Screenshot step3-theme-changed.png

# Cleanup
Ctrl+C
Sleep 500ms
```

---

## 🔍 SVG Analysis & Verification

### Why SVG?

**SVG = XML = Programmatically Analyzable**

SVG screenshots contain:
- All text content (`<text>` elements)
- All colors (`fill` and `stroke` attributes)
- Layout positions (`x`, `y` coordinates)
- Rectangles/borders (`<rect>` elements)
- Full visual structure

### Parsing SVG with Python

```python
from bs4 import BeautifulSoup

def analyze_svg(svg_path):
    """Parse SVG and extract visual information."""
    with open(svg_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'xml')

    # Extract colors
    colors = {
        elem.get('fill')
        for elem in soup.find_all(attrs={'fill': True})
        if elem.get('fill') not in ['none', 'transparent']
    }

    # Extract text content
    texts = [t.text.strip() for t in soup.find_all('text') if t.text.strip()]

    # Extract layout info
    rects = soup.find_all('rect')
    layout = [
        {
            'x': r.get('x'),
            'y': r.get('y'),
            'width': r.get('width'),
            'height': r.get('height'),
            'fill': r.get('fill'),
            'stroke': r.get('stroke')
        }
        for r in rects
    ]

    return {
        'colors': colors,
        'text': texts,
        'layout': layout
    }
```

### Verification Functions

**Color verification:**
```python
def verify_colors(svg_path, expected_colors):
    """Verify expected colors are present."""
    data = analyze_svg(svg_path)
    missing = set(expected_colors) - data['colors']
    if missing:
        raise AssertionError(f"Missing colors: {missing}")
    return True
```

**Text verification:**
```python
def verify_text(svg_path, expected_texts):
    """Verify expected text is present."""
    data = analyze_svg(svg_path)
    content = ' '.join(data['text'])
    for text in expected_texts:
        if text not in content:
            raise AssertionError(f"Missing text: {text}")
    return True
```

**Layout verification:**
```python
def verify_layout(svg_path):
    """Verify layout structure."""
    data = analyze_svg(svg_path)

    # Check border exists
    borders = [r for r in data['layout'] if r['stroke']]
    assert len(borders) > 0, "No borders found"

    # Check text is positioned correctly
    # (first text above second text)
    texts = soup.find_all('text')
    if len(texts) >= 2:
        y1 = float(texts[0].get('y', 0))
        y2 = float(texts[1].get('y', 0))
        assert y1 < y2, "Text order incorrect"

    return True
```

**Theme verification:**
```python
THEMES = {
    'dracula': {
        'bg': '#282a36',
        'fg': '#f8f8f2',
        'green': '#50fa7b',
        'pink': '#ff79c6',
        'purple': '#bd93f9',
    },
    'solarized-dark': {
        'bg': '#002b36',
        'fg': '#839496',
        'yellow': '#b58900',
        'orange': '#cb4b16',
    }
}

def verify_theme(svg_path, theme_name):
    """Verify TUI uses expected theme colors."""
    data = analyze_svg(svg_path)
    theme = THEMES[theme_name]

    # Check theme colors present
    found_colors = data['colors'] & set(theme.values())
    assert len(found_colors) >= 2, f"Theme colors not found: {theme_name}"

    return True
```

---

## 🧪 Testing Patterns

### Pattern 1: Iterative Development Verification

**Use Case:** Coder agent checking work during development

```python
# ./tmp/dev_tests/check_current_state.py

import subprocess
import sys
from verify_svg import verify_colors, verify_text

def quick_check():
    """Quick visual verification for iterative dev."""
    print("🔍 Running quick visual check...")

    # Run VHS tape
    result = subprocess.run(
        ['vhs', './tmp/dev_tests/current-state.tape'],
        capture_output=True,
        timeout=30
    )

    if result.returncode != 0:
        print(f"❌ VHS failed: {result.stderr.decode()}")
        sys.exit(1)

    # Verify screenshot
    svg_path = './tmp/screenshots/current-state.svg'

    try:
        # Check expected colors (theme-dependent)
        verify_colors(svg_path, ['#50fa7b', '#ff79c6'])  # Dracula
        print("✅ Colors correct")

        # Check expected text
        verify_text(svg_path, ['Welcome', 'Menu', 'Options'])
        print("✅ Text content correct")

        # Check layout (basic)
        data = analyze_svg(svg_path)
        assert len(data['layout']) > 0, "No layout elements"
        print("✅ Layout present")

        print("\n🎉 Visual verification PASSED!")
        print(f"📸 Screenshot: {svg_path}")
        return True

    except AssertionError as e:
        print(f"\n❌ Visual verification FAILED: {e}")
        print(f"📸 Review screenshot: {svg_path}")
        return False

if __name__ == '__main__':
    success = quick_check()
    sys.exit(0 if success else 1)
```

**Usage in iterative workflow:**
```bash
# Make code changes
vim my_tui.py

# Quick check
python ./tmp/dev_tests/check_current_state.py

# Output:
# ✅ Colors correct
# ✅ Text content correct
# ✅ Layout present
# 🎉 Visual verification PASSED!
```

### Pattern 2: Responsive Testing

**VHS tape for multiple sizes:**
```tape
# tests/tapes/responsive-test.tape

# Test at small size
Set Width 400
Set Height 300
Type "python app.py"
Enter
Sleep 2s
Screenshot ./tmp/screenshots/small-40x15.png
Ctrl+C
Sleep 1s

# Test at medium size
Set Width 800
Set Height 600
Type "python app.py"
Enter
Sleep 2s
Screenshot ./tmp/screenshots/medium-80x24.png
Ctrl+C
Sleep 1s

# Test at large size
Set Width 1200
Set Height 900
Type "python app.py"
Enter
Sleep 2s
Screenshot ./tmp/screenshots/large-120x40.png
Ctrl+C
Sleep 1s
```

**pytest test:**
```python
# tests/test_responsive.py

import subprocess
import pytest
from verify_svg import analyze_svg

SIZES = [
    ('small', 400, 300),
    ('medium', 800, 600),
    ('large', 1200, 900),
]

@pytest.mark.parametrize("name,width,height", SIZES)
def test_responsive_layout(name, width, height):
    """Test TUI at different terminal sizes."""
    # Run VHS for this size
    result = subprocess.run(
        ['vhs', f'tests/tapes/responsive-{name}.tape'],
        timeout=30
    )
    assert result.returncode == 0

    # Verify screenshot exists
    svg_path = f'./tmp/screenshots/{name}-{width}x{height}.svg'
    data = analyze_svg(svg_path)

    # Verify content adapts
    assert len(data['text']) > 0, "No text content"
    assert len(data['layout']) > 0, "No layout elements"

    # Size-specific checks
    if name == 'small':
        # Compact layout expected
        assert 'Menu' in ' '.join(data['text'])
    elif name == 'large':
        # Full layout with more details
        assert 'Detailed View' in ' '.join(data['text'])
```

### Pattern 3: Theme Testing

```python
# tests/test_themes.py

import subprocess
import pytest
from verify_svg import verify_theme

THEMES = ['dracula', 'solarized-dark', 'nord']

@pytest.mark.parametrize("theme", THEMES)
def test_theme_rendering(theme):
    """Test TUI with different color themes."""
    # Create tape with theme parameter
    tape_content = f"""
Output ./tmp/screenshots/theme-{theme}.svg
Set Theme "{theme.title()}"
Set Width 800
Set Height 600

Type "python app.py --theme {theme}"
Enter
Sleep 2s

Screenshot ./tmp/screenshots/theme-{theme}.png

Ctrl+C
Sleep 500ms
    """

    # Write temp tape file
    tape_path = f'./tmp/test-theme-{theme}.tape'
    with open(tape_path, 'w') as f:
        f.write(tape_content)

    # Run VHS
    result = subprocess.run(['vhs', tape_path], timeout=30)
    assert result.returncode == 0

    # Verify theme colors
    svg_path = f'./tmp/screenshots/theme-{theme}.svg'
    verify_theme(svg_path, theme)
```

### Pattern 4: E2E User Flow Testing

```python
# tests/test_user_flows.py

def test_login_flow():
    """Test complete login user flow."""
    # Run multi-step VHS tape
    result = subprocess.run(
        ['vhs', 'tests/tapes/login-flow.tape'],
        timeout=60
    )
    assert result.returncode == 0

    # Verify each step
    steps = [
        ('step1-launch', ['Login', 'Username']),
        ('step2-enter-username', ['Password']),
        ('step3-enter-password', ['Logging in']),
        ('step4-logged-in', ['Welcome back', 'Dashboard']),
    ]

    for step_name, expected_texts in steps:
        svg_path = f'./tmp/screenshots/{step_name}.svg'
        verify_text(svg_path, expected_texts)
```

---

## 🧹 Process Cleanup (CRITICAL)

### Why Cleanup Matters

**Problem:** TUI processes can become dangling background processes if not properly terminated, consuming resources and causing test failures.

**Solution:** Always ensure processes are terminated, even on errors.

### VHS Cleanup Pattern

**In tape files:**
```tape
# Your test commands here
Type "python app.py"
Enter
Sleep 2s

# Do your testing...

# CRITICAL: Always end with cleanup
Ctrl+C          # Send interrupt signal
Sleep 500ms     # Wait for graceful shutdown

# If process doesn't respond to Ctrl+C, VHS will timeout
# But guard against this in tests (see below)
```

### Python Cleanup Pattern

**Using subprocess with timeout:**
```python
import subprocess
import signal
import time

def run_vhs_with_cleanup(tape_path, timeout=30):
    """Run VHS with guaranteed cleanup."""
    proc = None
    try:
        proc = subprocess.Popen(
            ['vhs', tape_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait with timeout
        stdout, stderr = proc.communicate(timeout=timeout)

        if proc.returncode != 0:
            raise RuntimeError(f"VHS failed: {stderr.decode()}")

        return True

    except subprocess.TimeoutExpired:
        print(f"⚠️  VHS timeout after {timeout}s, killing process...")
        if proc:
            proc.kill()  # SIGKILL
            proc.wait(timeout=5)
        raise

    finally:
        # Verify cleanup: check for dangling TUI processes
        verify_no_dangling_processes()

def verify_no_dangling_processes():
    """Verify no TUI processes are still running."""
    result = subprocess.run(
        ['pgrep', '-f', 'my_tui_app.py'],  # Adjust pattern
        capture_output=True
    )

    if result.returncode == 0:
        pids = result.stdout.decode().strip().split('\n')
        print(f"⚠️  Warning: Found dangling processes: {pids}")

        # Force kill them
        for pid in pids:
            try:
                subprocess.run(['kill', '-9', pid])
            except:
                pass

        raise AssertionError("Dangling TUI processes found!")
```

**Context manager pattern:**
```python
import contextlib
import subprocess
import signal

@contextlib.contextmanager
def tui_process(command, timeout=30):
    """Context manager for TUI process with guaranteed cleanup."""
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=isinstance(command, str)
    )

    try:
        yield proc
    finally:
        # Cleanup
        try:
            proc.terminate()  # SIGTERM (graceful)
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()  # SIGKILL (force)
            proc.wait(timeout=1)

        # Verify terminated
        assert proc.poll() is not None, "Process still running!"

# Usage
def test_with_cleanup():
    with tui_process(['python', 'app.py']):
        # Run VHS or interact
        subprocess.run(['vhs', 'test.tape'], timeout=30)

    # Process guaranteed to be terminated here
```

### pytest Fixtures for Cleanup

```python
# conftest.py

import pytest
import subprocess
import time

@pytest.fixture
def cleanup_processes():
    """Fixture that ensures cleanup after each test."""
    yield  # Test runs here

    # After test: cleanup any dangling processes
    time.sleep(0.5)  # Brief delay

    # Find and kill any TUI processes
    patterns = ['my_tui_app.py', 'node.*tui', 'go.*tui']
    for pattern in patterns:
        result = subprocess.run(
            ['pgrep', '-f', pattern],
            capture_output=True
        )
        if result.returncode == 0:
            pids = result.stdout.decode().strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)

@pytest.fixture
def vhs_runner(cleanup_processes):
    """Fixture for running VHS with cleanup."""
    def run(tape_path, timeout=30):
        result = subprocess.run(
            ['vhs', tape_path],
            capture_output=True,
            timeout=timeout
        )
        if result.returncode != 0:
            raise RuntimeError(f"VHS failed: {result.stderr.decode()}")
        return result

    return run

# Usage in tests
def test_with_fixture(vhs_runner):
    """Test using VHS runner fixture."""
    vhs_runner('tests/tapes/my-test.tape')
    # Cleanup happens automatically
```

---

## 📖 Complete Examples

See [examples/](examples/) for complete working examples:

- `iterative-dev-example.py` - Coder agent iterative workflow
- `pytest-e2e-example.py` - Testing agent E2E tests
- `responsive-test-example.tape` - Multi-size testing
- `theme-test-example.py` - Theme verification
- `cleanup-example.py` - Process cleanup patterns

## 🎨 Templates

See [templates/](templates/) for starting points:

- `iterative-test-template.tape` - Quick dev check template
- `e2e-test-template.tape` - E2E test template
- `verify-template.py` - Verification script template

## 📚 Reference Documentation

- [VHS Complete Guide](reference/vhs-guide.md)
- [asciinema Workflow](reference/asciinema-guide.md)
- [SVG Analysis](reference/svg-analysis.md)
- [PTY Background Processes](reference/pty-background.md)
- [Troubleshooting](reference/troubleshooting.md)

---

## 🎯 Integration with Agents

### For @coder (Iterative Development)

```markdown
When building TUIs:

1. Write/modify code
2. Create `.tape` file with navigation to target screen
3. Run: `vhs my-test.tape`
4. Run verification: `python verify.py screenshot.svg`
5. Check output:
   ✅ Colors correct? → Continue
   ❌ Issues found? → Fix code, repeat

Fast cycle: < 5 minutes
```

### For @tester (E2E/Visual Testing)

```markdown
When creating test suites:

1. Generate pytest/jest test files
2. Each test runs VHS tape file
3. Programmatically verify screenshots:
   - Colors match theme
   - Layout elements present
   - Text content correct
   - Interactive states work
4. Store artifacts in ./tmp/screenshots/
5. Generate report with evidence
6. **CRITICAL:** Verify process cleanup in teardown

Comprehensive suite: 15-20 minutes
```

### For @refactor

```markdown
When refactoring TUIs:

1. Capture "before" screenshots (baseline)
2. Make refactoring changes
3. Capture "after" screenshots
4. Compare SVGs (visual regression)
5. Verify no unintended visual changes
6. Update baselines if intentional
```

---

## 🚨 Common Issues & Solutions

### Issue: Process won't terminate

**Symptom:** VHS hangs, Ctrl+C doesn't work

**Solution:**
```tape
# Add explicit cleanup
Ctrl+C
Sleep 500ms

# If still hanging, increase sleep
Ctrl+C
Sleep 2s
```

**In tests:**
```python
# Use timeout and force kill
subprocess.run(['vhs', 'test.tape'], timeout=30)
# Then verify no dangling processes
```

### Issue: Colors not preserved

**Symptom:** Screenshot shows wrong colors or no colors

**Solution:**
```bash
# Ensure 256-color terminal
export TERM=xterm-256color

# In tape file
Set Theme "Dracula"  # Or other theme with color support
```

### Issue: Navigation timing issues

**Symptom:** Screenshot captured before UI updates

**Solution:**
```tape
# Increase sleep after actions
Type "enter"
Sleep 2s  # Was 500ms, now 2s

# Or wait for specific text
# (not directly supported in VHS, use verification instead)
```

### Issue: Terminal size not applied

**Symptom:** TUI doesn't resize

**Solution:**
```tape
# Set dimensions in pixels, not columns×rows
Set Width 1200   # Pixels
Set Height 800   # Pixels

# Corresponds roughly to 120×40 at FontSize 14
```

For more troubleshooting: [reference/troubleshooting.md](reference/troubleshooting.md)

---

## 🌟 Community Sharing

This skill is designed to be:
- **Language-agnostic** (Python, Node, Go, Rust, any TUI)
- **Framework-agnostic** (Textual, Bubble Tea, Ink, blessed, etc.)
- **OS-agnostic** (macOS, Linux, Windows via Docker)
- **Well-documented** with complete examples
- **Ready for GitHub** sharing with community

Feel free to adapt and share!

---

## 📝 Summary

**Key Takeaways:**

1. **VHS is the recommended tool** - Universal, declarative, reliable
2. **Two primary workflows** - Iterative dev (fast) + E2E testing (comprehensive)
3. **SVG analysis is powerful** - Programmatically verify colors, layout, text
4. **Cleanup is critical** - Always terminate processes, verify no dangling procs
5. **Navigation + timing** - Key to reaching target screens in TUIs
6. **Integration-friendly** - Works with pytest, jest, any test framework

**Next Steps:**
- Install VHS: `brew install vhs`
- Try examples: `cd examples/ && vhs iterative-dev-example.tape`
- Read references for deep dives
- Adapt templates for your TUI

**Questions?** See [reference/troubleshooting.md](reference/troubleshooting.md)
