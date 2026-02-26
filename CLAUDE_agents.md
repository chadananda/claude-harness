# Agents

## Custom (`.claude/agents/`)
coder (TDD, sonnet) | reviewer (review+minimize, sonnet) | tester (unit/visual, sonnet) | doc (JSDoc+README, sonnet) | team-lead (orchestrates pipeline, opus) | stuck (human escalation, sonnet)

## Safety
TUI: NEVER run in main terminal — TUIs take over stdin/stdout, corrupt orchestrator state.
Web: Use Playwright MCP or webapp-testing skill — browser automation gives deterministic verification.
