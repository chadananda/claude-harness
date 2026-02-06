# PTY and Background Process Control

Guide to running TUI applications in background without terminal corruption.

## The Problem

When running TUI applications directly in the terminal during testing:
- Terminal gets corrupted with control sequences
- Output interferes with test runner output
- Hard to capture clean screenshots
- Process cleanup can fail, leaving dangling processes

**Solution**: Run TUI in a pseudo-terminal (PTY) in the background.

## What is a PTY?

A **PTY (Pseudo-Terminal)** is a virtual terminal that:
- Acts like a real terminal to the TUI application
- Runs in the background without affecting your current terminal
- Captures all output including colors and control sequences
- Allows programmatic control (sending keys, reading output)

## Basic PTY Usage

### Python (pty module)

```python
import pty
import os
import subprocess
import time

def run_tui_in_pty(command, timeout=10):
    """
    Run TUI command in PTY without corrupting main terminal.

    Args:
        command: Command to run (string or list)
        timeout: Maximum runtime in seconds

    Returns:
        Output captured from TUI
    """
    # Create PTY pair
    master, slave = pty.openpty()

    # Launch process in PTY
    process = subprocess.Popen(
        command if isinstance(command, list) else command.split(),
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=os.environ.copy()
    )

    # Close slave in parent (process has it)
    os.close(slave)

    try:
        # Wait for process
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        # Force kill if timeout
        process.kill()
        process.wait()
    finally:
        # Cleanup master
        os.close(master)

    return process.returncode


# Example usage
run_tui_in_pty("python my_tui_app.py", timeout=5)
```

### Sending Input to PTY

```python
import pty
import os
import subprocess
import time

def interact_with_tui(command, interactions, timeout=30):
    """
    Run TUI and send interactions.

    Args:
        command: Command to run
        interactions: List of (action, delay) tuples
            action: bytes or string to send
            delay: seconds to wait after sending

    Example:
        interactions = [
            (b'\x1b[B', 0.3),      # Down arrow
            (b'\x1b[B', 0.3),      # Down arrow
            (b'\n', 1.0),          # Enter
            (b'hello\n', 0.5),     # Type text + Enter
            (b'\x03', 0.5),        # Ctrl+C
        ]
    """
    master, slave = pty.openpty()

    process = subprocess.Popen(
        command.split(),
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=os.environ.copy()
    )

    os.close(slave)

    try:
        # Give TUI time to start
        time.sleep(1)

        # Send interactions
        for action, delay in interactions:
            if isinstance(action, str):
                action = action.encode()
            os.write(master, action)
            time.sleep(delay)

        # Wait for process to finish
        process.wait(timeout=timeout)

    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    except Exception as e:
        print(f"Error: {e}")
        process.kill()
        process.wait()
    finally:
        os.close(master)

    return process.returncode


# Example: Navigate TUI menu
interactions = [
    (b'\x1b[B', 0.3),  # Down
    (b'\x1b[B', 0.3),  # Down
    (b'\n', 1.0),      # Enter
    (b'\x03', 0.5),    # Ctrl+C to exit
]

interact_with_tui("python my_tui.py", interactions)
```

### Reading PTY Output

```python
import pty
import os
import subprocess
import select
import time

def capture_tui_output(command, duration=5):
    """
    Capture TUI output without blocking.

    Args:
        command: Command to run
        duration: How long to capture (seconds)

    Returns:
        Captured output as bytes
    """
    master, slave = pty.openpty()

    process = subprocess.Popen(
        command.split(),
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=os.environ.copy()
    )

    os.close(slave)

    output = b''
    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            # Check if data available (non-blocking)
            ready, _, _ = select.select([master], [], [], 0.1)

            if ready:
                try:
                    chunk = os.read(master, 4096)
                    if chunk:
                        output += chunk
                    else:
                        break  # EOF
                except OSError:
                    break  # Master closed

            # Check if process finished
            if process.poll() is not None:
                break

    finally:
        process.terminate()
        process.wait(timeout=2)
        os.close(master)

    return output


# Example usage
output = capture_tui_output("python my_tui.py", duration=3)
print(output.decode('utf-8', errors='ignore'))
```

## Control Sequences Reference

Common control sequences to send to PTY:

```python
# Navigation keys
DOWN_ARROW = b'\x1b[B'
UP_ARROW = b'\x1b[A'
LEFT_ARROW = b'\x1b[D'
RIGHT_ARROW = b'\x1b[C'

# Special keys
ENTER = b'\n'
TAB = b'\t'
BACKSPACE = b'\x7f'
ESCAPE = b'\x1b'
SPACE = b' '

# Control keys
CTRL_A = b'\x01'
CTRL_B = b'\x02'
CTRL_C = b'\x03'  # SIGINT
CTRL_D = b'\x04'  # EOF
CTRL_Z = b'\x1a'  # SIGTSTP

# Function keys
F1 = b'\x1bOP'
F2 = b'\x1bOQ'
F3 = b'\x1bOR'
F4 = b'\x1bOS'

# Page navigation
PAGE_UP = b'\x1b[5~'
PAGE_DOWN = b'\x1b[6~'
HOME = b'\x1b[H'
END = b'\x1b[F'

# Mouse events (if supported)
MOUSE_LEFT_CLICK = b'\x1b[M ...'  # Complex, varies by terminal
```

## Process Cleanup Patterns

### Pattern 1: Guaranteed Cleanup

```python
def run_with_cleanup(command, timeout=30):
    """Guarantee process cleanup even on errors."""
    master, slave = pty.openpty()
    process = None

    try:
        process = subprocess.Popen(
            command.split(),
            stdin=slave,
            stdout=slave,
            stderr=slave
        )
        os.close(slave)

        # Your interactions here...
        time.sleep(2)

        # Graceful shutdown
        os.write(master, b'\x03')  # Ctrl+C
        time.sleep(0.5)

        # Wait for graceful exit
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if not responding
            process.kill()
            process.wait()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always cleanup
        if process and process.poll() is None:
            process.kill()
            process.wait()
        try:
            os.close(master)
        except OSError:
            pass  # Already closed

    return process.returncode if process else -1
```

### Pattern 2: Context Manager

```python
import contextlib

@contextlib.contextmanager
def pty_process(command):
    """
    Context manager for PTY process.

    Usage:
        with pty_process("python my_tui.py") as (process, master):
            # Interact with process
            os.write(master, b'\x1b[B')
            time.sleep(0.3)
        # Automatic cleanup
    """
    master, slave = pty.openpty()
    process = None

    try:
        process = subprocess.Popen(
            command.split(),
            stdin=slave,
            stdout=slave,
            stderr=slave
        )
        os.close(slave)

        yield process, master

    finally:
        # Cleanup
        if process and process.poll() is None:
            try:
                os.write(master, b'\x03')  # Try graceful
                process.wait(timeout=2)
            except (subprocess.TimeoutExpired, OSError):
                process.kill()  # Force kill
                process.wait()

        try:
            os.close(master)
        except OSError:
            pass


# Usage
with pty_process("python my_tui.py") as (proc, master):
    time.sleep(1)
    os.write(master, b'\x1b[B')  # Down
    time.sleep(0.3)
    os.write(master, b'\n')      # Enter
    time.sleep(1)
# Automatic cleanup when context exits
```

### Pattern 3: Signal Escalation

```python
import signal

def kill_with_escalation(process, timeout=5):
    """
    Kill process with escalating signals.

    1. SIGTERM (graceful)
    2. Wait timeout
    3. SIGKILL (force)
    """
    if process.poll() is not None:
        return  # Already dead

    # Try graceful shutdown
    process.terminate()  # SIGTERM

    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        # Force kill
        process.kill()  # SIGKILL
        process.wait()


# Usage
try:
    # Run TUI
    process = subprocess.Popen(...)
    # ... interactions ...
finally:
    kill_with_escalation(process, timeout=5)
```

## Verification: No Dangling Processes

After running TUI tests, verify no processes remain:

```python
def verify_no_dangling_processes(process_pattern):
    """
    Check for dangling processes matching pattern.

    Args:
        process_pattern: String to search in process command
                        (e.g., "my_tui.py")

    Returns:
        List of dangling PIDs (empty if clean)
    """
    import subprocess

    try:
        result = subprocess.run(
            ['pgrep', '-f', process_pattern],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            return [int(pid) for pid in pids if pid]
        else:
            return []  # No processes found

    except FileNotFoundError:
        # pgrep not available (Windows)
        return []


def cleanup_dangling_processes(process_pattern):
    """Kill any dangling processes."""
    pids = verify_no_dangling_processes(process_pattern)

    if pids:
        print(f"🧹 Cleaning up {len(pids)} dangling process(es)")
        for pid in pids:
            try:
                subprocess.run(['kill', '-9', str(pid)], capture_output=True)
            except Exception as e:
                print(f"Failed to kill {pid}: {e}")

        time.sleep(0.5)

        # Verify cleanup
        remaining = verify_no_dangling_processes(process_pattern)
        if remaining:
            print(f"⚠️  Warning: {len(remaining)} process(es) still running")
        else:
            print("✅ All processes cleaned up")


# Usage in tests
cleanup_dangling_processes("my_tui.py")
```

## Integration with Testing

### pytest Fixture

```python
import pytest
import pty
import os
import subprocess
import time

@pytest.fixture
def tui_runner():
    """
    Fixture for running TUI in PTY with cleanup.
    """
    processes = []

    def run(command, interactions=None, timeout=30):
        """Run TUI with optional interactions."""
        master, slave = pty.openpty()

        process = subprocess.Popen(
            command.split(),
            stdin=slave,
            stdout=slave,
            stderr=slave
        )

        os.close(slave)
        processes.append((process, master))

        try:
            time.sleep(1)  # Wait for start

            if interactions:
                for action, delay in interactions:
                    os.write(master, action if isinstance(action, bytes) else action.encode())
                    time.sleep(delay)

            # Allow time for final state
            time.sleep(1)

        except Exception as e:
            pytest.fail(f"TUI interaction failed: {e}")

        return process, master

    yield run

    # Cleanup all processes
    for process, master in processes:
        if process.poll() is None:
            try:
                os.write(master, b'\x03')
                process.wait(timeout=2)
            except:
                process.kill()
                process.wait()

        try:
            os.close(master)
        except:
            pass


# Usage in test
def test_tui_navigation(tui_runner):
    """Test TUI navigation."""
    process, master = tui_runner(
        command="python my_tui.py",
        interactions=[
            (b'\x1b[B', 0.3),  # Down
            (b'\x1b[B', 0.3),  # Down
            (b'\n', 1.0),      # Enter
        ]
    )

    # Verify process is still running
    assert process.poll() is None

    # Cleanup happens automatically via fixture
```

## Platform Differences

### Unix/Linux/macOS

```python
import pty  # Available
import os
import subprocess

# Standard PTY approach works
master, slave = pty.openpty()
# ...
```

### Windows

Windows doesn't have PTY in the same way. Options:

1. **Use VHS** (cross-platform, recommended)
2. **Use conpty** (Windows 10+ pseudo-console):

```python
import subprocess

# Windows ConPTY (requires pywinpty)
try:
    import winpty
    pty_process = winpty.PTY(80, 30)
    pty_process.spawn("python my_tui.py")
    # Interact with pty_process
except ImportError:
    # Fall back to VHS
    pass
```

3. **Use WSL** (Windows Subsystem for Linux)

**Recommendation for Windows**: Use VHS instead of PTY manipulation.

## Best Practices

1. **Always cleanup**: Use try/finally or context managers
2. **Set timeouts**: Prevent hanging processes
3. **Verify cleanup**: Check no dangling processes after tests
4. **Use VHS for simplicity**: Unless you need direct PTY control
5. **Platform detection**: Use VHS on Windows, PTY on Unix
6. **Signal escalation**: SIGTERM first, SIGKILL if needed
7. **Add delays**: Wait for UI to update between actions
8. **Error handling**: Catch OSError, subprocess.TimeoutExpired

## Troubleshooting

### Issue: Process won't terminate

```python
# Try escalating signals
process.terminate()  # SIGTERM
time.sleep(2)
if process.poll() is None:
    process.kill()  # SIGKILL
    process.wait()
```

### Issue: Terminal size wrong

```python
import fcntl
import termios
import struct

def set_pty_size(fd, rows=30, cols=80):
    """Set PTY terminal size."""
    size = struct.pack('HHHH', rows, cols, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, size)

# Usage
master, slave = pty.openpty()
set_pty_size(master, rows=30, cols=80)
```

### Issue: Output garbled

```python
# Ensure proper encoding
output = os.read(master, 4096)
text = output.decode('utf-8', errors='ignore')
```

### Issue: "Bad file descriptor" error

```python
# Check fd is still open before writing
try:
    os.write(master, b'test')
except OSError as e:
    if e.errno == 9:  # EBADF
        print("Master already closed")
```

## Summary

PTY Background Control provides:
- ✅ Run TUIs without terminal corruption
- ✅ Programmatic control (send keys, read output)
- ✅ Proper isolation from test runner
- ✅ Capture colors and control sequences

But requires:
- ⚠️ Platform-specific code (Unix/Windows)
- ⚠️ Careful process cleanup
- ⚠️ Manual control sequence handling
- ⚠️ Error handling complexity

**Recommendation**: Use VHS for most TUI testing (simpler, cross-platform). Use PTY only when you need direct low-level control or are building custom capture tools.
