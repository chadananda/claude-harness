# Orchestrator

## Domains
Optional structured workflows. Load ONLY when the request clearly fits a domain — most work needs no domain at all. Read domains/{name}.md before starting when a domain applies — rules are not in default context; skipping them causes incorrect behavior (e.g., no TDD in dev work).

| Domain | When | File |
|--------|------|------|
| dev | implementation, features, coding, TDD, refactoring | domains/dev.md |
| plan | architecture, system design, project planning | domains/plan.md |
| doc | documentation, READMEs, JSDoc, technical writing | domains/doc.md |
| content | blog posts, articles, content writing, copywriting | domains/content.md |
| review | code review, audits, quality checks | domains/review.md |
| seo | SEO analysis, site audits, content optimization, GEO | domains/seo.md |
| plan-saas | SaaS project planning (idea → launch-ready) | domains/plan-saas.md |
| plan-api | API product planning (idea → developer GTM) | domains/plan-api.md |
| qa | autonomous QA, visual verification, regression testing | domains/qa.md |

Explicit *dev, *doc, *content, *plan, *review, *seo activate a domain. No command or no match = no domain loaded.
Ad-hoc tasks, questions, file ops, OS help, brainstorming — just work directly. No domain needed.

## Writing Voice
When producing human-facing text, load domains/writing-voice.md. Domains that generate prose already reference it.

## Conventions
- Root = config only — cluttered root signals disorganized project.
- src/|lib/ code; tests/ tests; docs/ docs; scripts/ utils; tmp/ temp (gitignored)
- Commit after each task group. Never commit tmp/ or .claude/context/. Use ./tmp/ not ~/tmp.

## Token Efficiency
- Use `--limit` when reading files — don't read entire files when you need a section.
- `grep`/`Grep` before reading — find the relevant section first.
- Don't re-read files already in context.
- Prefer `Glob` and `Grep` over `Bash(find)` and `Bash(grep)`.
- Run `/compact` after completing major task chunks to free context.

## Work in Lurches (Session Management)
For autonomous work, break into short sessions to avoid context bloat:
1. **Plan session:** analyze codebase → write plan to `tmp/work-plan.md` → exit
2. **Work session:** read plan → implement 2-3 items → commit → update plan → exit
3. **Repeat** until plan is complete
Each session starts fresh from the plan file. The plan is the continuity, not the conversation.

## Worker Status Reporting
On completing a task (especially autonomous/dispatched work), write `worker-status.json` to the project root:
```json
{"status":"complete","timestamp":"ISO","summary":"what was done","commits":["hash"],"tests_added":0,"files_removed":0,"lines_removed":0,"needs_attention":false}
```

## Autonomy
Work autonomously until blocked on human decision. Never ask "should I proceed?" — shifts cognitive load for non-decisions. Invoke stuck agent when genuinely stuck — real ambiguity needs human judgment.

### Never Go Idle With Work Remaining
If there is unfinished work, keep working. Do not stop and wait for a prompt. The user should never need to say "progress?" to un-stall you — if that one word gets you moving again, you were never actually blocked.

After completing any sub-task, immediately evaluate: is the overall goal done? If not, continue to the next step. The only valid reasons to stop are:
1. The entire task is complete.
2. You need a human decision (use stuck agent).
3. You've hit a hard external blocker (CI, deploy, waiting on a service).

"I finished this part" is not a stopping point — it's a transition to the next part.

### Loop State File Convention
Any skill run via `/loop` MUST maintain a state file at `tmp/{skill-name}-state.md` for continuity across ticks. Context compresses between ticks — without a state file, each tick starts blind.

**Start of tick:** Read the state file. If `status: IN_PROGRESS`, resume that work — do not re-evaluate from scratch.
**End of tick:** Write the state file with current status, what you're working on (specific enough to resume cold), and what comes next.

```markdown
# {Skill} State
last_tick: [ISO timestamp]
tick_number: [N]
status: IN_PROGRESS | BLOCKED | IDLE
current_task: [specific description of active work]
current_task_detail: [files, line numbers, exact progress — enough to resume blind]
blocked_reason: [if BLOCKED]
completed_this_session: [list]
next_priority: [what to do next if current_task finishes]
project_dir: [absolute path]
```
