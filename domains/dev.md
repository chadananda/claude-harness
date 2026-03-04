# Domain: dev — Feature Development

## TDD
Strict Red-Green-Refactor. Agents load @TDD.md. Never implement without failing test — proves requirement exists.

## Agents
coder (TDD, sonnet) | reviewer (review+YAGNI, sonnet) | tester (unit/visual, sonnet) | doc (JSDoc+README, sonnet) | team-lead (orchestrates pipeline, opus) | stuck (systematic-debugging → human escalation, sonnet)

Prefer built-in over custom: `code-simplifier` for minimization, `code-reviewer` for generic review, `systematic-debugging` before human escalation, `feature-dev:code-architect` for architecture, `feature-dev:code-explorer` for codebase analysis, `silent-failure-hunter` for error handling review.

Pipeline: coder → code-simplifier → reviewer → tester → doc.

## Tasks
Native Tasks for multi-step work. Fan out parallel tasks with shared blockers — parallelism maximizes throughput. Auto-execute after /plan approval — human already approved, don't re-confirm.

## Teams
Teams for independent parallel features; subagents for sequential work or lower token budget. Each teammate owns different files — same-file editing → overwrites. 5-6 tasks per teammate.

## File Context Blocks
Every non-trivial source file gets a `:ctx` block at top (after imports). LLM-targeted, not human docs. Terse, high-signal, no prose filler.

Format — labeled fields, compressed values:
```
# :arch: what this module is, core pattern
# :why: key design decisions, constraints that drove them
# :deps: what it reads/calls → what it gets | consumers of this module
# :rules: invariants, constraints, things that must never change
# :edge: non-obvious gotchas, failure modes, perf cliffs
```

Rules:
- Skip fields that don't apply — no empty labels.
- Update on every meaningful change — stale context is worse than none.
- Max 6 lines. If you need more, the module is doing too much.
- Language-appropriate comment syntax (# // /* etc).
- No field is mandatory — use only what adds signal for the specific file.

## Style
No blank lines (comments to separate); single-line ifs; functional chaining; modern ES6+; ternaries when readable.

## YAGNI
No single-use helpers (inline <10 lines) — indirection without reuse obscures call site. No premature abstractions (Rule of Three). Single file until >500 lines.

## Safety
TUI: NEVER run in main terminal — corrupts orchestrator state. Use tmux/VHS.
Web: Use Playwright MCP or webapp-testing skill — deterministic verification.
