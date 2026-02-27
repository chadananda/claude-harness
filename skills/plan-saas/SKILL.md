---
name: plan-saas
description: End-to-end SaaS project planner — idea validation, strategy, technical architecture, and 12-month marketing calendar. Four linear phases, each producing a deliverable document.
allowed-tools: Read, Write, Bash(*), WebSearch, WebFetch, AskUserQuestion
model: sonnet
argument-hint: "[idea] or [validate|strategy|technical|marketing|resume]"
---

# /plan-saas — End-to-End SaaS Project Planner

Takes a SaaS idea from napkin sketch to implementation-ready repo with a 12-month marketing calendar. Four linear phases: validate → strategy → technical → marketing. Each phase produces a deliverable document; each subsequent phase reads all prior documents to build context.

## Command Routing

Parse `$ARGUMENTS` to determine entry point:

| Input | Action |
|-------|--------|
| `validate [idea]` | Phase 1 only |
| `strategy` | Phase 2 (requires `viability-report.md`) |
| `technical` | Phase 3 (requires `strategy-brief.md`) |
| `marketing` | Phase 4 (requires `software-prd.md`) |
| `resume` | Detect last completed phase, continue from next |
| `[idea text]` (no subcommand) | Full 4-phase pipeline starting with idea |
| *(empty)* | Ask user for their SaaS idea, then full pipeline |

## Phase State Detection

Check which output files exist in the current working directory:

```
viability-report.md  → Phase 1 complete
strategy-brief.md    → Phase 2 complete
software-prd.md      → Phase 3 complete
marketing-prd.md     → Phase 4 complete
```

For `resume`: find the last existing file and start the next phase. If none exist, start Phase 1.

## Phase Gating

- **Phase 1 → 2**: Viability score must be ≥10 (Yellow zone). If Red zone, iterate on weakest factors before proceeding.
- **Phase 2 → 3**: `viability-report.md` must exist. Read it for context.
- **Phase 3 → 4**: `viability-report.md` + `strategy-brief.md` must exist. Read both.
- **Phase 4**: All three prior documents must exist. Read all for context.

## Phase Execution

For each phase, read the corresponding sub-skill file and follow its instructions exactly:

| Phase | Sub-skill | References (load on demand) | Output |
|-------|-----------|----------------------------|--------|
| 1: Validate | `skills/plan-validate.md` | `references/viability-scoring.md` | `viability-report.md` |
| 2: Strategy | `skills/plan-strategy.md` | `references/icp-framework.md`, `references/pricing-models.md` | `strategy-brief.md` |
| 3: Technical | `skills/plan-technical.md` | `references/saas-tech-stacks.md` | `software-prd.md` |
| 4: Marketing | `skills/plan-marketing.md` | `references/seo-strategy.md`, `references/content-marketing.md`, `references/guerrilla-playbook.md`, `references/distribution-channels.md`, `references/launch-sequence.md` | `marketing-prd.md` |

**Reference loading**: Read reference files at the START of each phase, not all at once. This keeps context focused.

## Output Templates

Each sub-skill writes its output document using the corresponding template from `templates/`. Read the template first, then fill in every section with specific, researched content. Never leave placeholder text.

## Conversation Style

- **Tough-love advisor**: Challenge assumptions with data. Don't be a yes-man.
- **One question at a time**: Never dump multiple questions. Ask, wait, research, challenge, score.
- **Specific numbers**: "The market is $2.3B growing at 14% CAGR" not "the market is large and growing."
- **WebSearch between questions**: Research competitors, market data, pricing pages, channels before asking the next question. Share findings to inform the conversation.
- **Show your work**: When scoring, explain exactly why with evidence from research.

## File Paths

All sub-skill, reference, and template paths are relative to this SKILL.md location:
`~/.claude/skills/plan-saas/`
