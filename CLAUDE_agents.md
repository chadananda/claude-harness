# Agents & Skills

## Agents

Agents in `.claude/agents/` are auto-loaded. Key agents:
- **coder** - Implementation (follows TDD.md)
- **reviewer** - Code review + refactoring (merged critic+refactor)
- **tester** - Unit test verification + visual testing (web/TUI)
- **doc** - Documentation (JSDoc + README)
- **team-lead** - Orchestrates mini-team per task (coder -> reviewer -> tester -> doc)
- **stuck** - Human escalation (only agent that pauses workflow)

## Skills Reference

Invoke with `/skill-name`:
- **/plan** - Requirements gathering and task decomposition
- **/frontend-design** - Distinctive, production-grade UI with bold aesthetics
- **/security-scan** - Detect secrets before commit (mandatory for coder agent)
- **/project-cleanup** - Organize messy project structure

## Project Type Detection

**TUI Projects** (textual, blessed, ink, bubbletea, etc.):
- NEVER run TUI in main terminal (corrupts state)
- Always use tmux/screen/background or VHS for testing
- See tui-viewer skill for visual verification

**Web Projects** (package.json, playwright.config):
- Use Playwright MCP or webapp-testing skill for browser testing
