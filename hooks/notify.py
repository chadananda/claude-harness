#!/usr/bin/env python3
"""Minimal notification hook for Claude Code - plays sound when @stuck is invoked"""
import sys, json, subprocess, platform

def beep():
    """Cross-platform beep - uses built-in system sounds"""
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], check=False, timeout=2)
        elif system == "Windows":
            subprocess.run(["powershell", "-c", "[console]::beep(800,500)"], check=False, timeout=2)
        else:  # Linux
            print("\a", flush=True)  # Terminal bell - most reliable
    except: pass  # Silent fail - don't break Claude

try:
    data = json.load(sys.stdin)
    # Trigger on @stuck invocations or AskUserQuestion
    if ("stuck" in str(data.get("subagent", "")).lower() or
        data.get("tool_name") == "AskUserQuestion" or
        data.get("type") == "Notification"):
        beep()
        print("\n🔔 Claude needs your input!\n", flush=True)
except: pass

sys.exit(0)  # Always succeed