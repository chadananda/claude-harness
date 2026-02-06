# Basic VHS Tape Template
# Customize this for your TUI application

# Output files
Output ./tmp/screenshots/my-test.svg
Output ./tmp/screenshots/my-test.png

# Terminal configuration
Set FontSize 14
Set Width 1000
Set Height 600
Set Theme "Dracula"  # Or: Nord, Solarized Dark, etc.

# Launch your TUI application
Type "python my_tui_app.py"  # Replace with your command
Enter
Sleep 2s  # Wait for app to load

# ===== CUSTOMIZE YOUR NAVIGATION HERE =====

# Example: Navigate through menu
Down
Sleep 300ms
Down
Sleep 300ms

# Example: Select option
Enter
Sleep 1s

# Example: Type input
Type "hello world"
Sleep 300ms

# Example: Submit
Enter
Sleep 1s

# ==========================================

# Capture final state
Screenshot ./tmp/screenshots/my-test-final.png

# CRITICAL: Cleanup - always terminate process
Ctrl+C
Sleep 500ms
