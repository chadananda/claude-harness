# TUI Viewer Skill

Universal skill for Terminal User Interface (TUI) visual verification across any programming language or framework.

## What This Skill Provides

This skill teaches Claude Code agents how to:

1. **Capture TUI screenshots** with colors and layout preserved
2. **Run TUIs in background** without corrupting the terminal
3. **Navigate through TUI applications** (menus, dialogs, forms)
4. **Analyze screenshots programmatically** (colors, text, layout)
5. **Test at different terminal sizes** (responsive testing)
6. **Verify visual correctness** during development and testing
7. **Properly cleanup processes** (no dangling background processes)

## Primary Use Cases

### Use Case 1: Iterative Development (Coder Agent)
Fast visual feedback loop for developers:
- Make code changes to TUI
- Capture screenshot with VHS
- Analyze colors, layout, text
- Iterate quickly (< 5 min cycles)

### Use Case 2: E2E/Visual Testing (Testing Agent)
Comprehensive test suite creation:
- Integration with pytest/jest/go test
- Visual regression testing
- Responsive testing (multiple sizes)
- Theme testing (dark/light modes)
- Behavioral testing with interactions

## File Structure

```
tui-viewer/
├── SKILL.md                    # Main skill guide
├── LICENSE.txt                 # MIT license
├── README.md                   # This file
├── reference/                  # Technical references
│   ├── vhs-guide.md           # VHS declarative capture
│   ├── asciinema-guide.md     # Alternative capture method
│   ├── svg-analysis.md        # Programmatic SVG analysis
│   ├── pty-background.md      # PTY process control
│   └── troubleshooting.md     # Common issues and solutions
├── examples/                   # Working examples
│   ├── iterative-dev-example.tape        # VHS tape for iterative dev
│   ├── iterative-dev-verify.py           # Verification script
│   └── pytest-e2e-example.py             # Complete pytest test suite
└── templates/                  # Customizable templates
    ├── basic-tape-template.tape          # VHS tape template
    └── verify-template.py                # Verification script template
```

## Quick Start

### 1. Install Dependencies

```bash
# Install VHS (primary capture tool)
brew install vhs

# Install Python dependencies (for verification)
pip install beautifulsoup4 lxml
```

### 2. Capture a TUI Screenshot

Create a `.tape` file:

```tape
Output ./tmp/screenshots/my-tui.svg

Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"

# Launch your TUI
Type "python my_tui_app.py"
Enter
Sleep 2s

# Navigate
Down
Sleep 300ms
Down
Sleep 300ms
Enter
Sleep 1s

# Cleanup
Ctrl+C
Sleep 500ms
```

Run it:
```bash
vhs my-capture.tape
```

### 3. Analyze the Screenshot

```python
from bs4 import BeautifulSoup

def analyze_svg(svg_path):
    with open(svg_path, 'r') as f:
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

    return {'colors': colors, 'text': texts}

data = analyze_svg('./tmp/screenshots/my-tui.svg')
print(f"Colors found: {data['colors']}")
print(f"Text found: {data['text']}")
```

## Key Features

### Language Agnostic
Works with:
- Python (Textual, Rich, urwid, curses)
- Node.js (blessed, ink, terminal-kit)
- Go (tview, termui, bubbletea)
- Rust (tui-rs, cursive, termion)
- Any TUI framework that runs in a terminal

### Preserves Visual Fidelity
- Full color support (24-bit RGB)
- Layout and spacing preserved
- SVG format (scalable, analyzable)
- Theme support (Dracula, Nord, Solarized, etc.)

### Proper Process Management
- PTY isolation (no terminal corruption)
- Timeout protection
- Guaranteed cleanup (no dangling processes)
- Signal escalation (SIGTERM → SIGKILL)

### Programmatic Analysis
- Extract colors (hex values)
- Extract text content
- Verify layout structure
- Compare against baselines
- Theme validation

## Testing Workflow

### Iterative Development

```bash
# 1. Capture current state
vhs iterative-dev.tape

# 2. Analyze
python verify.py ./tmp/screenshots/output.svg

# 3. Fix issues
# 4. Repeat
```

### E2E Testing

```python
# tests/test_tui_e2e.py
import pytest

@pytest.fixture
def vhs_runner():
    """Run VHS tapes with cleanup."""
    def run(tape_content, output_name):
        # ... VHS execution ...
        return svg_path
    return run

def test_responsive_layout(vhs_runner, svg_analyzer):
    """Test at multiple terminal sizes."""
    for size in [(40,15), (80,30), (120,40)]:
        svg = vhs_runner(create_tape(size), f"size-{size[0]}x{size[1]}")
        data = svg_analyzer(svg)
        assert len(data['colors']) > 0
        assert len(data['text']) > 0
```

## When to Use This Skill

**Use this skill when:**
- Building or refactoring a TUI application
- Need visual verification during development
- Creating comprehensive TUI test suites
- Testing responsive layouts (different terminal sizes)
- Verifying themes and color schemes
- Testing interactive behaviors (menus, forms, dialogs)
- Need to see what the TUI actually looks like

**Don't use this skill when:**
- Testing non-TUI CLI tools (just check stdout)
- No visual verification needed (unit tests sufficient)
- TUI framework has built-in visual testing

## Tool Comparison

| Tool | Best For | Pros | Cons |
|------|----------|------|------|
| **VHS** | Most use cases | Simple, declarative, built-in cleanup | Requires installation |
| **Asciinema + svg-term** | CI/CD, headless | Flexible, frame control | More complex setup |
| **PTY Direct** | Custom tools | Full control | Platform-specific, complex |

**Recommendation**: Start with VHS, use alternatives for special cases.

## Examples

All examples are in `examples/` directory:

1. **iterative-dev-example.tape** - Quick visual check during development
2. **iterative-dev-verify.py** - Automated verification with cleanup
3. **pytest-e2e-example.py** - Complete pytest test suite with fixtures

## Templates

Customizable templates in `templates/` directory:

1. **basic-tape-template.tape** - VHS tape starting point
2. **verify-template.py** - Verification script starting point

## Troubleshooting

See `reference/troubleshooting.md` for common issues:
- Dangling processes
- Color preservation
- Timing issues
- Terminal size problems
- VHS execution failures

## Contributing

This skill is community-shareable. Contributions welcome!

**License:** MIT (see LICENSE.txt)

## Resources

- VHS: https://github.com/charmbracelet/vhs
- Asciinema: https://asciinema.org
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/

## Support

For issues or questions:
1. Check `reference/troubleshooting.md`
2. Review examples in `examples/`
3. Consult reference docs in `reference/`

---

**Built for:** Claude Code agents
**Works with:** Any TUI framework in any language
**Focus:** Visual verification, fast iteration, comprehensive testing
