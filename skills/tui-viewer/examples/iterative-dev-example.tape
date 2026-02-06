# Iterative Development Example
# Use Case: Coder agent checking visual state during TUI development
# This tape navigates to a specific screen and captures it for verification

Output ./tmp/screenshots/iterative-current-state.svg
Output ./tmp/screenshots/iterative-current-state.png

# Terminal configuration
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"
Set TypingSpeed 50ms

# Launch TUI application
Type "python examples/sample_tui.py"
Enter
Sleep 2s

# Navigate to target screen (adjust for your TUI)
# Example: Main menu → Settings → Theme settings

# Step 1: Navigate down to "Settings" option
Down
Sleep 300ms
Down
Sleep 300ms

# Step 2: Select Settings
Enter
Sleep 1s

# Step 3: Navigate to "Theme" option
Down
Sleep 300ms

# Step 4: Open theme submenu
Enter
Sleep 1s

# Capture final state
Screenshot ./tmp/screenshots/iterative-theme-screen.png

# CRITICAL: Cleanup - terminate process
Ctrl+C
Sleep 500ms
