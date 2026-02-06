#!/usr/bin/env python3
"""PostToolUse hook: Auto-cleanup tmp/scripts/ after task completion."""
import json
import sys
import os
import glob

# Read hook input
data = json.load(sys.stdin)

# Only trigger on TaskUpdate
if data.get('tool_name') != 'TaskUpdate':
    sys.exit(0)

# Check if task was marked completed
tool_input = data.get('tool_input', {})
if tool_input.get('status') != 'completed':
    sys.exit(0)

# Clean tmp/scripts/ in current project
cwd = os.getcwd()
tmp_scripts = os.path.join(cwd, 'tmp', 'scripts')

if not os.path.exists(tmp_scripts):
    sys.exit(0)

# Remove all files except .gitkeep
files = [f for f in glob.glob(f'{tmp_scripts}/*') if os.path.isfile(f) and not f.endswith('.gitkeep')]

if files:
    for f in files:
        os.remove(f)
    print(f"🧹 Cleaned {len(files)} file(s) from ./tmp/scripts/", file=sys.stderr)

sys.exit(0)
