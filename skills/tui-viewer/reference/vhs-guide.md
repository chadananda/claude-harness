# VHS Complete Reference Guide

## Overview

VHS (Video Home System) by Charm is a declarative tool for recording terminal sessions and generating screenshots. Perfect for TUI testing because:

- Language-agnostic (works with ANY TUI)
- Declarative `.tape` files (version-controllable)
- Automated execution (no human interaction)
- Multiple output formats
- Built-in process management

**GitHub:** https://github.com/charmbracelet/vhs

## Installation

```bash
# macOS
brew install vhs

# Linux/macOS with Go
go install github.com/charmbracelet/vhs@latest

# Docker (cross-platform)
docker pull ghcr.io/charmbracelet/vhs

# Verify installation
vhs --version
```

##

 Tape File Syntax

### Basic Structure

```tape
# Comments start with #

# Output configuration
Output output.gif
Output output.mp4
Output output.png

# Terminal configuration
Set FontSize 14
Set Width 1200
Set Height 600
Set Theme "Dracula"

# Commands
Type "your command"
Enter
Sleep 1s

# Cleanup
Ctrl+C
```

### Commands Reference

#### Type
```tape
Type "hello world"              # Types text
Type@500ms "slow typing"        # Custom typing speed
```

#### Keys
```tape
Enter                           # Press Enter/Return
Backspace                       # Delete character
Tab                             # Tab key
Space                           # Space bar
Escape                          # Escape key

# Arrow keys
Up
Down
Left
Right

# Modifiers
Ctrl+C                          # Ctrl+C (interrupt)
Ctrl+D                          # Ctrl+D (EOF)
Ctrl+L                          # Ctrl+L (clear)
Ctrl+Z                          # Ctrl+Z (suspend)

# Function keys
F1
F2
...
F12
```

#### Sleep
```tape
Sleep 1s                        # Sleep for 1 second
Sleep 500ms                     # Sleep for 500 milliseconds
Sleep 2.5s                      # Sleep for 2.5 seconds
```

#### Screenshot
```tape
Screenshot output.png           # Capture current frame as PNG
Screenshot@5s output.png        # Capture frame at 5s mark
```

#### Hide/Show
```tape
Hide                            # Hide subsequent typing
Type "password"
Show                            # Show typing again
```

### Set Commands

#### FontSize
```tape
Set FontSize 12                 # Small
Set FontSize 14                 # Default
Set FontSize 18                 # Large
```

#### Width/Height
```tape
# In pixels (not columns×rows)
Set Width 800                   # Terminal width
Set Height 600                  # Terminal height

# Common sizes:
# 400×300   ≈ 40×15  (small)
# 800×600   ≈ 80×24  (default)
# 1200×900  ≈ 120×40 (large)
# 1600×1200 ≈ 160×50 (xlarge)
```

#### Theme
```tape
Set Theme "Dracula"             # Popular themes
Set Theme "Monokai"
Set Theme "Nord"
Set Theme "Solarized Dark"
Set Theme "Solarized Light"
Set Theme "One Dark"
Set Theme "GitHub Dark"
Set Theme "GitHub Light"

# Custom theme (JSON file)
Set Theme "./custom-theme.json"
```

#### TypingSpeed
```tape
Set TypingSpeed 50ms            # Default
Set TypingSpeed 100ms           # Slower (more readable)
Set TypingSpeed 10ms            # Fast (demos)
```

#### Framerate
```tape
Set Framerate 60                # Smooth (default: 50)
Set Framerate 30                # Lower file size
```

#### PlaybackSpeed
```tape
Set PlaybackSpeed 1.0           # Normal (default)
Set PlaybackSpeed 0.5           # Slower
Set PlaybackSpeed 2.0           # Faster
```

#### Padding
```tape
Set Padding 20                  # Padding around terminal
```

#### WindowBar
```tape
Set WindowBar Colorful          # macOS-style window controls
Set WindowBar RingColors
Set WindowBar None              # No window decorations
```

## Advanced Patterns

### Multi-Step Workflows

```tape
Output multi-step.gif

Set FontSize 14
Set Width 1000
Set Height 600

# Step 1
Type "python app.py"
Enter
Sleep 2s
Screenshot step1.png

# Step 2
Type "menu"
Enter
Sleep 1s
Screenshot step2.png

# Step 3
Type "settings"
Enter
Sleep 1s
Screenshot step3.png

# Cleanup
Ctrl+C
Sleep 500ms
```

### Responsive Testing

```tape
# Test at multiple sizes
Output responsive.gif

# Small
Set Width 400
Set Height 300
Type "python app.py"
Enter
Sleep 2s
Screenshot small.png
Ctrl+C
Sleep 1s

# Medium
Set Width 800
Set Height 600
Type "python app.py"
Enter
Sleep 2s
Screenshot medium.png
Ctrl+C
Sleep 1s

# Large
Set Width 1200
Set Height 900
Type "python app.py"
Enter
Sleep 2s
Screenshot large.png
Ctrl+C
Sleep 1s
```

### Theme Comparison

```tape
Output theme-comparison.gif

Set Width 1000
Set Height 600

# Dark theme
Set Theme "Dracula"
Type "python app.py --theme dark"
Enter
Sleep 2s
Screenshot theme-dark.png
Ctrl+C
Sleep 1s

# Light theme
Set Theme "GitHub Light"
Type "python app.py --theme light"
Enter
Sleep 2s
Screenshot theme-light.png
Ctrl+C
Sleep 1s
```

### Form Filling

```tape
Output form-test.gif

Set Width 1000
Set Height 600

Type "python form-app.py"
Enter
Sleep 1s

# Field 1: Name
Type "John Doe"
Tab
Sleep 200ms

# Field 2: Email
Type "john@example.com"
Tab
Sleep 200ms

# Field 3: Password
Hide
Type "secretpassword"
Show
Tab
Sleep 200ms

# Submit
Enter
Sleep 2s

Screenshot form-submitted.png

Ctrl+C
```

### Menu Navigation

```tape
Output menu-nav.gif

Type "python menu-app.py"
Enter
Sleep 2s
Screenshot menu-start.png

# Navigate down 3 times
Down
Sleep 300ms
Down
Sleep 300ms
Down
Sleep 300ms

Screenshot menu-option-3.png

# Select
Enter
Sleep 1s

Screenshot menu-selected.png

Ctrl+C
```

## Output Formats

### GIF (Animated)
```tape
Output animation.gif

Set GIFLoop true               # Loop animation
Set GIFSize 1920               # Max width (maintains aspect)
```

### MP4 (Video)
```tape
Output video.mp4

Set Quality 100                # 0-100, default 100
```

### WebM (Video)
```tape
Output video.webm
```

### PNG (Static Image)
```tape
Screenshot frame.png           # Single frame at current time
Screenshot@5s frame.png        # Frame at 5 second mark
```

### SVG (Vector - via fork)
```tape
# Requires: https://github.com/agentstation/vhs (fork with SVG support)
Output output.svg
```

## Execution

### Command Line

```bash
# Basic execution
vhs demo.tape

# With docker
docker run --rm -v $PWD:/vhs ghcr.io/charmbracelet/vhs demo.tape

# Publish to vhs.charm.sh (shares GIF publicly)
vhs publish demo.tape
```

### Programmatic Execution

**Python:**
```python
import subprocess

def run_vhs(tape_path, timeout=30):
    """Execute VHS tape file."""
    result = subprocess.run(
        ['vhs', tape_path],
        capture_output=True,
        timeout=timeout
    )

    if result.returncode != 0:
        raise RuntimeError(f"VHS failed: {result.stderr.decode()}")

    return result.stdout.decode()

# Usage
try:
    run_vhs('tests/demo.tape')
    print("✅ VHS execution successful")
except RuntimeError as e:
    print(f"❌ VHS failed: {e}")
```

**Node.js:**
```javascript
const { execSync } = require('child_process');

function runVhs(tapePath, timeout = 30000) {
  try {
    execSync(`vhs ${tapePath}`, { timeout });
    console.log('✅ VHS execution successful');
  } catch (error) {
    throw new Error(`VHS failed: ${error.stderr}`);
  }
}

// Usage
runVhs('tests/demo.tape');
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/tui-test.yml

name: TUI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install VHS
        run: |
          go install github.com/charmbracelet/vhs@latest

      - name: Run TUI tests
        run: |
          vhs tests/demo.tape

      - name: Upload screenshots
        uses: actions/upload-artifact@v3
        with:
          name: screenshots
          path: ./tmp/screenshots/*.png
```

### Docker

```dockerfile
# Dockerfile for VHS testing

FROM golang:1.21-alpine

RUN apk add --no-cache \
    ttyd \
    chromium \
    font-noto-emoji \
    && go install github.com/charmbracelet/vhs@latest

WORKDIR /app
COPY . .

CMD ["vhs", "tests/demo.tape"]
```

## Best Practices

### 1. Always Add Cleanup

```tape
# ❌ Bad - no cleanup
Type "python app.py"
Enter
Sleep 2s

# ✅ Good - cleanup included
Type "python app.py"
Enter
Sleep 2s

Ctrl+C                # Terminate process
Sleep 500ms           # Wait for cleanup
```

### 2. Use Consistent Timing

```tape
# ✅ Good - predictable timing
Type "command"
Enter
Sleep 2s              # Consistent delay

Down
Sleep 300ms           # Same delay for all navigation

Enter
Sleep 1s
```

### 3. Capture at Key States

```tape
# ✅ Capture important states
Type "python app.py"
Enter
Sleep 2s
Screenshot initial-state.png    # State 1

Down
Sleep 300ms
Screenshot navigated.png        # State 2

Enter
Sleep 1s
Screenshot selected.png         # State 3
```

### 4. Name Files Descriptively

```tape
# ❌ Bad names
Output test.gif
Screenshot img1.png

# ✅ Good names
Output menu-navigation-dark-theme.gif
Screenshot login-form-80x24-dracula.png
```

### 5. Test Multiple Scenarios

```tape
# ✅ Comprehensive testing

# Scenario 1: Small terminal
Set Width 400
Set Height 300
Type "python app.py"
Enter
Sleep 2s
Screenshot small-terminal.png
Ctrl+C
Sleep 1s

# Scenario 2: Large terminal
Set Width 1200
Set Height 900
Type "python app.py"
Enter
Sleep 2s
Screenshot large-terminal.png
Ctrl+C
```

## Troubleshooting

### Issue: VHS hangs / doesn't terminate

**Solution:**
```tape
# Increase Ctrl+C delay
Ctrl+C
Sleep 2s              # Longer wait

# Or add multiple Ctrl+C
Ctrl+C
Sleep 500ms
Ctrl+C
Sleep 500ms
```

### Issue: Wrong colors

**Solution:**
```bash
# Ensure color terminal
export TERM=xterm-256color

# In tape file
Set Theme "Dracula"   # Use named theme
```

### Issue: Animation too fast/slow

**Solution:**
```tape
Set PlaybackSpeed 0.5  # Slower playback
Set TypingSpeed 100ms  # Slower typing
```

### Issue: Screenshots captured too early

**Solution:**
```tape
# Increase sleep before screenshot
Type "command"
Enter
Sleep 3s              # Was 1s, now 3s
Screenshot output.png
```

### Issue: Terminal size incorrect

**Solution:**
```tape
# Set size before launching app
Set Width 1200        # Set first
Set Height 800

Type "python app.py"  # Then launch
```

## Advanced: Dynamic Tape Generation

**Generate tapes programmatically:**

```python
def generate_responsive_tape(app_command, sizes):
    """Generate VHS tape for responsive testing."""
    tape_lines = ["Output responsive-test.gif\n"]

    for name, width, height in sizes:
        tape_lines.extend([
            f"Set Width {width}\n",
            f"Set Height {height}\n",
            f"Type \"{app_command}\"\n",
            "Enter\n",
            "Sleep 2s\n",
            f"Screenshot {name}-{width}x{height}.png\n",
            "Ctrl+C\n",
            "Sleep 1s\n\n",
        ])

    return ''.join(tape_lines)

# Usage
sizes = [
    ('small', 400, 300),
    ('medium', 800, 600),
    ('large', 1200, 900),
]

tape = generate_responsive_tape('python app.py', sizes)

with open('responsive-test.tape', 'w') as f:
    f.write(tape)

# Execute
subprocess.run(['vhs', 'responsive-test.tape'])
```

## Resources

- **Official Repo:** https://github.com/charmbracelet/vhs
- **Examples:** https://github.com/charmbracelet/vhs/tree/main/examples
- **Charm Community:** https://charm.sh/
- **SVG Fork:** https://github.com/agentstation/vhs

## Summary

VHS is the recommended tool for TUI testing because:

✅ Language-agnostic
✅ Declarative and version-controllable
✅ Automated execution
✅ Multiple output formats
✅ Built-in process management
✅ CI/CD friendly
✅ Active development

**Next:** See [svg-analysis.md](svg-analysis.md) for analyzing generated screenshots.
