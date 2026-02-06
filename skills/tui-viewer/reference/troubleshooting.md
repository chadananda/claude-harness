# Troubleshooting Guide

## Process Issues

### Problem: Process Won't Terminate

**Symptoms:**
- VHS hangs indefinitely
- Ctrl+C doesn't work
- Process continues running after test

**Solutions:**

1. **Increase Ctrl+C delay:**
```tape
Ctrl+C
Sleep 2s        # Instead of 500ms
```

2. **Send multiple Ctrl+C:**
```tape
Ctrl+C
Sleep 500ms
Ctrl+C
Sleep 500ms
```

3. **Force kill in code:**
```python
proc = subprocess.Popen(['vhs', 'test.tape'])
try:
    proc.wait(timeout=30)
except subprocess.TimeoutExpired:
    proc.kill()  # SIGKILL
    proc.wait()
```

4. **Verify cleanup:**
```bash
# Check for dangling processes
pgrep -f "my_tui_app"

# Kill if found
pkill -9 -f "my_tui_app"
```

### Problem: Dangling Background Processes

**Symptoms:**
- Multiple TUI processes running
- Tests fail due to port/resource conflicts
- System slowdown

**Solutions:**

1. **Always use cleanup in tests:**
```python
@pytest.fixture
def cleanup():
    yield
    subprocess.run(['pkill', '-9', '-f', 'my_tui_app'])
```

2. **Track PIDs:**
```python
proc = subprocess.Popen(['python', 'app.py'])
pid = proc.pid

try:
    # Your test
    pass
finally:
    os.kill(pid, signal.SIGTERM)
    time.sleep(1)
    try:
        os.kill(pid, signal.SIGKILL)  # Force if still running
    except ProcessLookupError:
        pass  # Already terminated
```

##

 Color Issues

### Problem: Colors Not Preserved

**Symptoms:**
- Screenshot shows wrong colors
- Only black and white visible
- Theme colors missing

**Solutions:**

1. **Set TERM environment variable:**
```bash
export TERM=xterm-256color
```

2. **In VHS tape:**
```tape
Set Theme "Dracula"  # Use named theme with color support
```

3. **Check TUI color support:**
```python
# Ensure TUI uses 256-color mode
import os
os.environ['TERM'] = 'xterm-256color'
os.environ['COLORTERM'] = 'truecolor'
```

4. **Verify terminal emulator:**
```bash
# Test color support
curl -s https://gist.githubusercontent.com/lifepillar/09a44b8cf0f9397465614e622979107f/raw/24-bit-color.sh | bash
```

### Problem: Theme Colors Don't Match

**Symptoms:**
- Expected theme colors not found in SVG
- Different colors than specified

**Solutions:**

1. **Pass theme to TUI app:**
```tape
Type "python app.py --theme dracula"  # Explicit theme
```

2. **Verify theme configuration:**
```python
# In your TUI app
if __name__ == '__main__':
    theme = os.getenv('TUI_THEME', 'dracula')
    app = MyApp(theme=theme)
```

3. **Check theme consistency:**
```python
# Verify theme in tests
verify_theme('screenshot.svg', 'dracula', min_colors=2)
```

## Timing Issues

### Problem: Screenshot Captured Too Early

**Symptoms:**
- Screenshot shows loading state
- UI not fully rendered
- Missing content

**Solutions:**

1. **Increase sleep delays:**
```tape
Type "python app.py"
Enter
Sleep 3s        # Was 1s, now 3s
Screenshot output.png
```

2. **Wait for specific state (manual timing):**
```tape
Type "python app.py"
Enter
Sleep 1s
# Navigate to ensure loaded
Down
Sleep 500ms
Up
Sleep 500ms
Screenshot output.png
```

3. **Add loading indicators in TUI:**
```python
# In TUI code
self.loading = False
# Set loading = False when ready
```

### Problem: Navigation Too Fast

**Symptoms:**
- Commands execute before UI updates
- State changes missed
- Incorrect final state

**Solutions:**

1. **Add delays between commands:**
```tape
Down
Sleep 500ms     # Consistent delay
Down
Sleep 500ms
Enter
Sleep 1s        # Longer for actions
```

2. **Use slower typing speed:**
```tape
Set TypingSpeed 100ms   # Slower (default: 50ms)
```

## Terminal Size Issues

### Problem: Wrong Terminal Dimensions

**Symptoms:**
- Layout doesn't match expected size
- Content cut off or wrapped

**Solutions:**

1. **Set size BEFORE launching:**
```tape
Set Width 1200      # Set first
Set Height 800
Type "python app.py"  # Then launch
```

2. **Match font size to dimensions:**
```tape
Set FontSize 14     # Default
Set Width 1000      # ~100 columns
Set Height 600      # ~30 rows
```

3. **Test at actual terminal size:**
```python
# Get terminal size in code
import shutil
cols, rows = shutil.get_terminal_size()
```

### Problem: Responsive Layout Not Working

**Symptoms:**
- Same layout at all sizes
- No size adaptation

**Solutions:**

1. **Ensure TUI reads terminal size:**
```python
# In TUI code
import os
cols = os.get_terminal_size().columns
rows = os.get_terminal_size().lines
```

2. **Test at distinct sizes:**
```tape
# Small (clearly different)
Set Width 400
Set Height 300

# Large (clearly different)
Set Width 1600
Set Height 1200
```

## VHS Execution Issues

### Problem: VHS Command Not Found

**Symptoms:**
- `vhs: command not found`
- Execution fails

**Solutions:**

1. **Install VHS:**
```bash
# macOS
brew install vhs

# Linux/Go
go install github.com/charmbracelet/vhs@latest

# Add to PATH
export PATH="$PATH:$(go env GOPATH)/bin"
```

2. **Use absolute path:**
```bash
/usr/local/bin/vhs test.tape
```

3. **Use Docker:**
```bash
docker run --rm -v $PWD:/vhs ghcr.io/charmbracelet/vhs test.tape
```

### Problem: VHS Timeout

**Symptoms:**
- VHS hangs for long time
- No output generated

**Solutions:**

1. **Check tape file syntax:**
```bash
# Validate tape file
cat test.tape  # Look for errors
```

2. **Use timeout in execution:**
```python
subprocess.run(['vhs', 'test.tape'], timeout=60)
```

3. **Simplify tape for debugging:**
```tape
# Minimal test
Type "echo hello"
Enter
Sleep 1s
Screenshot test.png
```

## SVG Analysis Issues

### Problem: BeautifulSoup Parse Error

**Symptoms:**
- `TypeError: __init__() got an unexpected keyword argument 'features'`
- Parse failure

**Solutions:**

1. **Install lxml:**
```bash
pip install lxml
```

2. **Use correct parser:**
```python
soup = BeautifulSoup(svg_content, 'xml')  # Not 'html'
```

3. **Check file encoding:**
```python
with open(svg_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'xml')
```

### Problem: Colors Not Found in SVG

**Symptoms:**
- `verify_colors()` fails
- Expected colors missing

**Solutions:**

1. **Print all colors found:**
```python
data = analyze_svg('screenshot.svg')
print(f"Colors found: {data['colors']}")
```

2. **Check color format:**
```python
# Colors might be RGB instead of hex
# Look for both formats
colors_hex = {e.get('fill') for e in soup.find_all(fill=True)}
colors_rgb = {e.get('fill') for e in soup.find_all(fill=lambda x: x and 'rgb' in x)}
```

3. **Lower expectations:**
```python
# Check for at least some theme colors
verify_theme('screenshot.svg', 'dracula', min_colors=1)  # Not 3
```

## Test Framework Integration

### Problem: pytest Can't Find Screenshots

**Symptoms:**
- `FileNotFoundError` for screenshots
- Tests pass locally but fail in CI

**Solutions:**

1. **Use absolute paths:**
```python
import os
screenshot_path = os.path.join(os.getcwd(), 'tmp/screenshots/test.svg')
```

2. **Create directories:**
```python
os.makedirs('./tmp/screenshots', exist_ok=True)
```

3. **Check working directory:**
```python
print(f"Current dir: {os.getcwd()}")
print(f"Files: {os.listdir('./tmp/screenshots')}")
```

### Problem: Tests Pass Individually, Fail Together

**Symptoms:**
- Individual tests pass
- Test suite fails
- Intermittent failures

**Solutions:**

1. **Add cleanup between tests:**
```python
@pytest.fixture(autouse=True)
def cleanup_between_tests():
    yield
    # Kill all TUI processes
    subprocess.run(['pkill', '-9', '-f', 'my_tui_app'])
    time.sleep(0.5)
```

2. **Use unique output files:**
```python
def test_feature_a():
    # Use test-specific filename
    subprocess.run(['vhs', 'test-a.tape'])

def test_feature_b():
    subprocess.run(['vhs', 'test-b.tape'])
```

3. **Add delays between tests:**
```python
@pytest.fixture
def delay():
    yield
    time.sleep(1)  # Brief delay for cleanup
```

## CI/CD Issues

### Problem: VHS Fails in CI

**Symptoms:**
- Works locally, fails in GitHub Actions
- Timeout in CI

**Solutions:**

1. **Install dependencies:**
```yaml
# .github/workflows/test.yml
- name: Install VHS
  run: go install github.com/charmbracelet/vhs@latest

- name: Add to PATH
  run: echo "$(go env GOPATH)/bin" >> $GITHUB_PATH
```

2. **Use Docker:**
```yaml
- name: Run tests with Docker
  run: |
    docker run --rm -v $PWD:/vhs ghcr.io/charmbracelet/vhs tests/demo.tape
```

3. **Increase timeouts:**
```python
# Longer timeouts in CI
timeout = 120 if os.getenv('CI') else 30
subprocess.run(['vhs', 'test.tape'], timeout=timeout)
```

## Performance Issues

### Problem: VHS is Slow

**Symptoms:**
- Tests take too long
- Each tape file takes minutes

**Solutions:**

1. **Reduce sleep times:**
```tape
Sleep 500ms     # Instead of 2s
```

2. **Skip animations:**
```tape
Set PlaybackSpeed 2.0   # 2x speed
```

3. **Use PNG instead of GIF:**
```tape
# PNG is faster to generate
Screenshot output.png
# Instead of Output output.gif
```

4. **Run tests in parallel:**
```bash
pytest -n auto  # Requires pytest-xdist
```

## Quick Debugging Checklist

When something fails:

- [ ] Check VHS is installed: `vhs --version`
- [ ] Verify tape file syntax (no typos)
- [ ] Test with minimal tape file
- [ ] Check for dangling processes: `pgrep -f my_tui`
- [ ] Verify TERM environment: `echo $TERM`
- [ ] Check file permissions
- [ ] Look at actual generated SVG/PNG
- [ ] Print all colors found in SVG
- [ ] Add delays between commands
- [ ] Use cleanup fixtures in tests
- [ ] Check working directory
- [ ] Verify dependencies installed (lxml, beautifulsoup4)

## Getting Help

If issues persist:

1. **Check VHS issues:** https://github.com/charmbracelet/vhs/issues
2. **Test with minimal example:**
```tape
Type "echo hello"
Enter
Sleep 1s
Screenshot test.png
Ctrl+C
```

3. **Enable verbose output:**
```bash
vhs --help  # Check available flags
```

4. **Share reproducible example** when asking for help

## Summary

Most issues fall into these categories:

1. **Process cleanup** - Always terminate properly
2. **Timing** - Increase sleeps for async operations
3. **Colors** - Set TERM=xterm-256color
4. **Paths** - Use absolute paths, create directories
5. **CI/CD** - Install dependencies, increase timeouts

**Remember:** When in doubt, add more Sleep delays!
