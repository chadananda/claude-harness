---
description: Manually cleanup tmp/scripts/ directory
---

Clean temporary scripts from the current project:

```bash
rm -rf ./tmp/scripts/* && echo "✅ tmp/scripts/ cleaned"
```

This removes all files in ./tmp/scripts/ (normally auto-cleaned after task completion via PostToolUse hook).
