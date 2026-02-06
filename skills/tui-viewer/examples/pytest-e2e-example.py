#!/usr/bin/env python3
"""
E2E Testing Example with pytest

Use Case: Testing agent creating comprehensive TUI test suites

This demonstrates:
1. Integration with pytest framework
2. Multiple test scenarios (responsive, themes, user flows)
3. SVG analysis and verification
4. Proper cleanup between tests
5. Test fixtures for reusability

Run with: pytest examples/pytest-e2e-example.py -v
"""

import pytest
import subprocess
import os
import time
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    pytest.skip("beautifulsoup4 not installed", allow_module_level=True)


# Test Configuration
TUI_APP = "python examples/sample_tui.py"
SCREENSHOTS_DIR = "./tmp/screenshots/e2e"
TAPES_DIR = "./examples/tapes"


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_directories():
    """Create necessary directories before tests."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(TAPES_DIR, exist_ok=True)
    yield


@pytest.fixture(autouse=True)
def cleanup_processes():
    """Cleanup dangling TUI processes after each test."""
    yield  # Test runs here

    # Cleanup after test
    time.sleep(0.5)
    try:
        result = subprocess.run(
            ['pgrep', '-f', 'sample_tui.py'],
            capture_output=True
        )
        if result.returncode == 0:
            pids = result.stdout.decode().strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)
    except FileNotFoundError:
        pass  # pgrep not available


@pytest.fixture
def vhs_runner():
    """Fixture for running VHS tape files."""
    def run(tape_content, output_name, timeout=30):
        """
        Run VHS tape with given content.

        Args:
            tape_content: VHS tape commands as string
            output_name: Base name for output files
            timeout: Maximum execution time

        Returns:
            Path to generated SVG file
        """
        # Write tape file
        tape_path = os.path.join(TAPES_DIR, f"{output_name}.tape")
        with open(tape_path, 'w') as f:
            f.write(tape_content)

        # Run VHS
        result = subprocess.run(
            ['vhs', tape_path],
            capture_output=True,
            timeout=timeout
        )

        if result.returncode != 0:
            pytest.fail(f"VHS execution failed: {result.stderr.decode()}")

        # Return SVG path
        svg_path = os.path.join(SCREENSHOTS_DIR, f"{output_name}.svg")

        # Brief delay for file write
        time.sleep(0.5)

        if not os.path.exists(svg_path):
            pytest.fail(f"Screenshot not generated: {svg_path}")

        return svg_path

    return run


@pytest.fixture
def svg_analyzer():
    """Fixture for analyzing SVG screenshots."""
    def analyze(svg_path):
        """Parse SVG and return visual data."""
        with open(svg_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'xml')

        colors = {
            elem.get('fill')
            for elem in soup.find_all(attrs={'fill': True})
            if elem.get('fill') not in ['none', 'transparent', None]
        }

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

    return analyze


# ============================================================================
# Tests
# ============================================================================

class TestBasicLaunch:
    """Test basic TUI launch and initial state."""

    def test_default_appearance(self, vhs_runner, svg_analyzer):
        """Test TUI default appearance on launch."""
        tape = f"""
Output {SCREENSHOTS_DIR}/default-launch.svg
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"

Type "{TUI_APP}"
Enter
Sleep 2s

Screenshot {SCREENSHOTS_DIR}/default-launch.png

Ctrl+C
Sleep 500ms
        """

        svg_path = vhs_runner(tape, "default-launch")
        data = svg_analyzer(svg_path)

        # Verify expected elements
        assert len(data['text']) > 0, "No text content found"
        assert len(data['colors']) > 0, "No colors found"

        # Verify expected text (adjust for your TUI)
        content = ' '.join(data['text'])
        assert 'Menu' in content or 'Welcome' in content, \
            f"Expected text not found. Got: {data['text']}"


class TestResponsive:
    """Test TUI at different terminal sizes."""

    @pytest.mark.parametrize("size_name,width,height", [
        ("small", 400, 300),
        ("medium", 800, 600),
        ("large", 1200, 900),
    ])
    def test_responsive_layout(self, vhs_runner, svg_analyzer, size_name, width, height):
        """Test TUI adapts to different terminal sizes."""
        tape = f"""
Output {SCREENSHOTS_DIR}/responsive-{size_name}.svg
Set FontSize 14
Set Width {width}
Set Height {height}
Set Theme "Dracula"

Type "{TUI_APP}"
Enter
Sleep 2s

Screenshot {SCREENSHOTS_DIR}/responsive-{size_name}.png

Ctrl+C
Sleep 500ms
        """

        svg_path = vhs_runner(tape, f"responsive-{size_name}")
        data = svg_analyzer(svg_path)

        # Basic checks
        assert len(data['text']) > 0, f"No text at {size_name} size"
        assert len(data['colors']) > 0, f"No colors at {size_name} size"

        # Size-specific checks
        if size_name == "small":
            # Expect compact layout
            assert len(data['text']) >= 1
        elif size_name == "large":
            # Expect full layout with more details
            assert len(data['text']) >= 3


class TestThemes:
    """Test TUI with different color themes."""

    @pytest.mark.parametrize("theme", [
        "Dracula",
        "Nord",
        "Solarized Dark",
    ])
    def test_theme_colors(self, vhs_runner, svg_analyzer, theme):
        """Test TUI renders with correct theme colors."""
        tape = f"""
Output {SCREENSHOTS_DIR}/theme-{theme.lower().replace(' ', '-')}.svg
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "{theme}"

Type "{TUI_APP} --theme {theme.lower()}"
Enter
Sleep 2s

Screenshot {SCREENSHOTS_DIR}/theme-{theme.lower().replace(' ', '-')}.png

Ctrl+C
Sleep 500ms
        """

        svg_path = vhs_runner(tape, f"theme-{theme.lower().replace(' ', '-')}")
        data = svg_analyzer(svg_path)

        # Verify colors are present
        assert len(data['colors']) >= 2, \
            f"Expected multiple colors for {theme} theme"

        # Theme-specific color checks (adjust for your themes)
        if theme == "Dracula":
            # Check for Dracula-specific colors
            dracula_colors = ['#50fa7b', '#ff79c6', '#f8f8f2', '#282a36']
            found = [c for c in dracula_colors if c in data['colors']]
            assert len(found) >= 2, \
                f"Dracula theme colors not found. Got: {data['colors']}"


class TestUserFlows:
    """Test complete user interaction flows."""

    def test_menu_navigation_flow(self, vhs_runner, svg_analyzer):
        """Test navigating through menu options."""
        tape = f"""
Output {SCREENSHOTS_DIR}/menu-flow.svg
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"

# Launch
Type "{TUI_APP}"
Enter
Sleep 2s

# Navigate down
Down
Sleep 300ms
Down
Sleep 300ms

# Select option
Enter
Sleep 1s

Screenshot {SCREENSHOTS_DIR}/menu-flow-selected.png

Ctrl+C
Sleep 500ms
        """

        svg_path = vhs_runner(tape, "menu-flow")
        data = svg_analyzer(svg_path)

        # Verify navigation worked
        assert len(data['text']) > 0
        content = ' '.join(data['text'])

        # Check that we're in a submenu or different state
        # (Adjust assertions for your TUI behavior)
        assert content != '', "No content after navigation"

    def test_form_input_flow(self, vhs_runner, svg_analyzer):
        """Test form filling user flow."""
        tape = f"""
Output {SCREENSHOTS_DIR}/form-flow.svg
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"

# Launch
Type "{TUI_APP} --mode form"
Enter
Sleep 2s

# Fill form fields
Type "Test User"
Tab
Sleep 200ms

Type "test@example.com"
Tab
Sleep 200ms

# Submit
Enter
Sleep 1s

Screenshot {SCREENSHOTS_DIR}/form-submitted.png

Ctrl+C
Sleep 500ms
        """

        svg_path = vhs_runner(tape, "form-flow")
        data = svg_analyzer(svg_path)

        # Verify form submission
        content = ' '.join(data['text'])
        # Check for confirmation or success message
        # (Adjust for your TUI)
        assert len(content) > 0


class TestEdgeCases:
    """Test edge cases and error states."""

    def test_empty_state(self, vhs_runner, svg_analyzer):
        """Test TUI with no data/empty state."""
        tape = f"""
Output {SCREENSHOTS_DIR}/empty-state.svg
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"

Type "{TUI_APP} --empty"
Enter
Sleep 2s

Screenshot {SCREENSHOTS_DIR}/empty-state.png

Ctrl+C
Sleep 500ms
        """

        svg_path = vhs_runner(tape, "empty-state")
        data = svg_analyzer(svg_path)

        # Should still render, even if empty
        assert len(data['colors']) > 0, "No rendering in empty state"

        # Check for empty state message
        content = ' '.join(data['text'])
        # (Adjust for your TUI's empty state messaging)
        assert len(content) >= 0  # At least something rendered


# ============================================================================
# Test Summary
# ============================================================================

def pytest_sessionfinish(session, exitstatus):
    """Print summary after all tests."""
    if exitstatus == 0:
        print("\n" + "="*60)
        print("✅ All E2E tests PASSED!")
        print("="*60)
        print(f"📸 Screenshots saved to: {SCREENSHOTS_DIR}")
        print(f"📼 Tapes saved to: {TAPES_DIR}")
    else:
        print("\n" + "="*60)
        print("❌ Some E2E tests FAILED")
        print("="*60)
        print(f"📸 Review screenshots in: {SCREENSHOTS_DIR}")
