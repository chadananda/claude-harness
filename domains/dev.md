# Domain: dev — Feature Development

## TDD
Strict Red-Green-Refactor. Agents load @TDD.md. Never implement without failing test — proves requirement exists.

## Agents
coder (TDD, sonnet) | reviewer (review+minimize, sonnet) | tester (unit/visual, sonnet) | doc (JSDoc+README, sonnet) | team-lead (orchestrates pipeline, opus) | stuck (human escalation, sonnet)

## Tasks
Native Tasks for multi-step work. Fan out parallel tasks with shared blockers — parallelism maximizes throughput. Auto-execute after /plan approval — human already approved, don't re-confirm.

## Teams
Teams for independent parallel features; subagents for sequential work or lower token budget. Each teammate owns different files — same-file editing → overwrites. 5-6 tasks per teammate.

## Style
No blank lines (comments to separate); single-line ifs; functional chaining; modern ES6+; ternaries when readable.

## YAGNI
No single-use helpers (inline <10 lines) — indirection without reuse obscures call site. No premature abstractions (Rule of Three). Single file until >500 lines.

## Safety
TUI: NEVER run in main terminal — corrupts orchestrator state. Use tmux/VHS.
Web: Use Playwright MCP or webapp-testing skill — deterministic verification.
