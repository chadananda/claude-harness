# Asciinema + svg-term-cli Guide

Alternative TUI capture method using asciinema recordings and svg-term-cli conversion.

## Overview

**Asciinema** records terminal sessions to `.cast` files (JSON format).
**svg-term-cli** converts `.cast` files to SVG images.

This method provides more control over recording vs rendering, useful for:
- Recording live terminal sessions
- Converting recordings to SVG after the fact
- Programmatic control over timing and frames
- CI/CD environments where VHS isn't available

## Installation

```bash
# Install asciinema
brew install asciinema

# Install svg-term-cli (requires Node.js)
npm install -g svg-term-cli
```

## Basic Workflow

### Step 1: Record Terminal Session

```bash
# Start recording
asciinema rec my-tui-session.cast

# Your TUI will launch in the recording session
# Interact normally
# Press Ctrl+D to stop recording
```

### Step 2: Convert to SVG

```bash
# Basic conversion
svg-term --cast my-tui-session.cast --out output.svg

# With options
svg-term \
  --cast my-tui-session.cast \
  --out output.svg \
  --width 80 \
  --height 30 \
  --term iterm2 \
  --profile Dracula
```

## Programmatic Recording

For agent workflows, use programmatic recording:

```python
#!/usr/bin/env python3
"""
Programmatic asciinema recording for TUI testing.
"""
import subprocess
import time
import os
import pty
import select

def record_tui_session(command, cast_file, interactions, timeout=30):
    """
    Record TUI session with programmatic interactions.

    Args:
        command: Command to launch TUI (e.g., "python my_tui.py")
        cast_file: Output .cast file path
        interactions: List of (action, delay) tuples
            action: string to type or special key
            delay: seconds to wait after action
        timeout: Maximum recording duration

    Example:
        interactions = [
            ("down", 0.3),     # Press down arrow
            ("down", 0.3),     # Press down arrow
            ("enter", 1.0),    # Press enter
            ("hello", 0.5),    # Type "hello"
            ("ctrl-c", 0.5),   # Send Ctrl+C
        ]
    """
    # Start asciinema recording
    env = os.environ.copy()
    env['TERM'] = 'xterm-256color'

    # Launch recording
    record_proc = subprocess.Popen(
        ['asciinema', 'rec', '--stdin', '--quiet', cast_file],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )

    time.sleep(1)  # Wait for asciinema to start

    # Launch TUI in PTY
    master, slave = pty.openpty()
    tui_proc = subprocess.Popen(
        command.split(),
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=env
    )

    os.close(slave)

    try:
        # Perform interactions
        for action, delay in interactions:
            if action == "enter":
                os.write(master, b'\n')
            elif action == "ctrl-c":
                os.write(master, b'\x03')
            elif action == "down":
                os.write(master, b'\x1b[B')
            elif action == "up":
                os.write(master, b'\x1b[A')
            elif action == "left":
                os.write(master, b'\x1b[D')
            elif action == "right":
                os.write(master, b'\x1b[C')
            elif action == "tab":
                os.write(master, b'\t')
            else:
                # Type text
                os.write(master, action.encode())

            time.sleep(delay)

        # Final cleanup
        os.write(master, b'\x03')  # Ctrl+C
        time.sleep(0.5)

    finally:
        # Cleanup
        os.close(master)
        tui_proc.terminate()
        tui_proc.wait(timeout=5)
        record_proc.terminate()
        record_proc.wait(timeout=5)

    print(f"✅ Recording saved to {cast_file}")
    return cast_file


def convert_to_svg(cast_file, svg_file, width=80, height=30, theme="Dracula"):
    """
    Convert .cast file to SVG.

    Args:
        cast_file: Input .cast file
        svg_file: Output SVG file
        width: Terminal width in columns
        height: Terminal height in rows
        theme: Color theme (Dracula, Nord, Solarized Dark, etc.)
    """
    result = subprocess.run(
        [
            'svg-term',
            '--cast', cast_file,
            '--out', svg_file,
            '--width', str(width),
            '--height', str(height),
            '--profile', theme,
            '--no-cursor',  # Hide cursor for clean screenshots
        ],
        capture_output=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"SVG conversion failed: {result.stderr.decode()}")

    print(f"✅ SVG saved to {svg_file}")
    return svg_file


def main():
    """Example workflow."""
    # Define interactions
    interactions = [
        (None, 2.0),        # Wait for app to load
        ("down", 0.3),      # Navigate down
        ("down", 0.3),      # Navigate down
        ("enter", 1.0),     # Select option
        ("ctrl-c", 0.5),    # Exit
    ]

    # Record session
    cast_file = "./tmp/recordings/my-session.cast"
    os.makedirs(os.path.dirname(cast_file), exist_ok=True)

    record_tui_session(
        command="python my_tui_app.py",
        cast_file=cast_file,
        interactions=interactions
    )

    # Convert to SVG
    svg_file = "./tmp/screenshots/my-session.svg"
    convert_to_svg(cast_file, svg_file, width=80, height=30, theme="Dracula")

    print(f"\n📸 Screenshot ready for analysis: {svg_file}")


if __name__ == '__main__':
    main()
```

## svg-term-cli Options

```bash
# Terminal size
--width <columns>          # Default: 80
--height <rows>            # Default: 24

# Theme/colors
--profile <theme>          # Dracula, Nord, Solarized Dark, etc.
--term <terminal>          # iterm2, gnome-terminal, etc.

# Appearance
--no-cursor               # Hide cursor (clean screenshots)
--padding <pixels>        # Padding around terminal
--padding-x <pixels>      # Horizontal padding
--padding-y <pixels>      # Vertical padding

# Frame selection
--from <timestamp>        # Start time (e.g., "2.5s")
--to <timestamp>          # End time (e.g., "5s")
--at <timestamp>          # Single frame at timestamp
```

## Frame Extraction

Extract specific frames from recording:

```bash
# Capture state at 3 seconds
svg-term \
  --cast session.cast \
  --at 3s \
  --out frame-3s.svg

# Capture range
svg-term \
  --cast session.cast \
  --from 2s \
  --to 5s \
  --out frames-2-5s.svg
```

## Asciinema vs VHS Comparison

| Feature | Asciinema + svg-term | VHS |
|---------|---------------------|-----|
| **Installation** | Two tools (asciinema + svg-term-cli) | One tool (VHS) |
| **Recording** | Live recording or programmatic | Declarative .tape files |
| **Navigation** | Programmatic PTY control | Built-in commands (Down, Up, etc.) |
| **SVG Output** | Yes (via svg-term-cli) | Yes (via fork) |
| **Cleanup** | Manual process management | Built-in Ctrl+C |
| **CI/CD** | Better for headless environments | Requires X11/display |
| **Flexibility** | More control over timing/frames | Simpler declarative syntax |
| **Learning Curve** | Steeper (PTY, subprocess) | Gentler (simple commands) |

## When to Use Asciinema

Choose asciinema + svg-term-cli when:
- Recording live development sessions
- Converting existing recordings to SVG
- Need frame-by-frame control
- Running in headless CI/CD without display
- Want to separate recording from rendering
- Need programmatic PTY control

Choose VHS when:
- Writing declarative test scenarios
- Simple navigation and screenshots
- Built-in cleanup and process management
- Easier for agents to generate .tape files
- All-in-one solution preferred

## Troubleshooting

### Issue: Colors not preserved

```bash
# Ensure TERM is set correctly
export TERM=xterm-256color
asciinema rec session.cast

# Or specify profile in svg-term
svg-term --cast session.cast --profile Dracula --out output.svg
```

### Issue: Process doesn't terminate

```python
# Always use timeout and force kill
try:
    tui_proc.wait(timeout=5)
except subprocess.TimeoutExpired:
    tui_proc.kill()  # Force kill
    tui_proc.wait()
```

### Issue: PTY control not working

```python
# Ensure proper timing
os.write(master, b'\x1b[B')  # Down arrow
time.sleep(0.3)  # Wait for UI to update
```

## Best Practices

1. **Always cleanup processes**: Use try/finally blocks
2. **Use timeout**: Prevent hanging recordings
3. **Set TERM correctly**: Ensures color support
4. **Add delays**: Wait for UI to update between actions
5. **Verify recordings**: Check .cast file before conversion
6. **Store recordings**: Keep .cast files for debugging

## Integration with Testing

```python
import pytest
from pathlib import Path

@pytest.fixture
def asciinema_recorder():
    """Fixture for recording TUI sessions."""
    def record(command, interactions, output_name):
        cast_file = f"./tmp/recordings/{output_name}.cast"
        svg_file = f"./tmp/screenshots/{output_name}.svg"

        # Record session
        record_tui_session(command, cast_file, interactions)

        # Convert to SVG
        convert_to_svg(cast_file, svg_file)

        return svg_file

    return record

def test_menu_navigation(asciinema_recorder, svg_analyzer):
    """Test menu navigation with asciinema."""
    svg_file = asciinema_recorder(
        command="python my_tui.py",
        interactions=[
            (None, 2.0),
            ("down", 0.3),
            ("down", 0.3),
            ("enter", 1.0),
            ("ctrl-c", 0.5),
        ],
        output_name="menu-nav"
    )

    # Analyze SVG
    data = svg_analyzer(svg_file)
    assert "Settings" in ' '.join(data['text'])
```

## Summary

Asciinema + svg-term-cli provides:
- ✅ Flexible recording options
- ✅ Frame-by-frame control
- ✅ Good for CI/CD
- ✅ SVG output for analysis
- ✅ Programmatic interactions

But requires:
- ⚠️ More setup (two tools)
- ⚠️ Manual PTY management
- ⚠️ More complex code
- ⚠️ Manual cleanup

**Recommendation**: Use VHS for most cases, asciinema for advanced scenarios requiring programmatic PTY control or when running in headless environments.
