#!/usr/bin/env python3
"""Claude Code PreToolUse hook: blocks git commits that flip dev/tasks.json
tasks to 'pass' without a verify_cmd and progress.md update in staged files."""
import json, sys, subprocess, os

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

# Only care about git commit commands
if "git commit" not in cmd:
    sys.exit(0)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(args):
    try:
        return subprocess.run(args, cwd=root, capture_output=True, text=True).stdout.strip()
    except Exception:
        return ""

def git_show(ref):
    try:
        return subprocess.run(["git", "show", ref], cwd=root, capture_output=True, text=True).stdout
    except Exception:
        return None

staged_files = run(["git", "diff", "--cached", "--name-only"]).split("\n")
staged_files = [f for f in staged_files if f]

tasks_path = "dev/tasks.json"
progress_path = "dev/progress.md"

if tasks_path not in staged_files:
    sys.exit(0)

# Get previous and current tasks.json
prev_raw = git_show(f"HEAD:{tasks_path}")
curr_raw = git_show(f":{tasks_path}")

if not curr_raw:
    print("ERROR: dev/tasks.json staged but unreadable", file=sys.stderr)
    sys.exit(2)

try:
    curr_tasks = json.loads(curr_raw).get("tasks", [])
except json.JSONDecodeError:
    print("ERROR: dev/tasks.json has invalid JSON", file=sys.stderr)
    sys.exit(2)

prev_status = {}
if prev_raw:
    try:
        prev_status = {t["id"]: t["status"] for t in json.loads(prev_raw).get("tasks", [])}
    except Exception:
        pass

# Find tasks flipped from fail to pass
flipped = [t for t in curr_tasks
           if t["status"] == "pass" and prev_status.get(t["id"], "fail") == "fail"]

if not flipped:
    sys.exit(0)

# Check 1: verify_cmd exists
missing_verify = [t for t in flipped if not t.get("verify_cmd", "").strip()]
if missing_verify:
    ids = ", ".join(t["id"] for t in missing_verify)
    print(f"BLOCKED: Tasks flipped to pass without verify_cmd: {ids}", file=sys.stderr)
    sys.exit(2)

# Check 2: progress.md must be staged
if progress_path not in staged_files:
    ids = ", ".join(t["id"] for t in flipped)
    print(f"BLOCKED: dev/tasks.json has pass-flips ({ids}) but dev/progress.md is not staged", file=sys.stderr)
    sys.exit(2)

# Check 3: progress.md must mention each flipped task ID
progress_content = git_show(f":{progress_path}") or ""
missing_entries = [t for t in flipped if t["id"] not in progress_content]
if missing_entries:
    ids = ", ".join(t["id"] for t in missing_entries)
    print(f"BLOCKED: dev/progress.md missing log entries for: {ids}", file=sys.stderr)
    sys.exit(2)

ids = ", ".join(t["id"] for t in flipped)
print(f"Harness OK: {len(flipped)} task(s) verified ({ids})", file=sys.stderr)
sys.exit(0)
