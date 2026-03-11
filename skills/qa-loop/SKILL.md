---
name: qa-loop
description: "Autonomous QA watchdog. Run via `/loop 1h /qa-loop` to continuously evaluate project state and take action — dev work when incomplete, QA when built, idle when nothing warrants action. Designed for overnight/idle runs."
argument-hint: "[optional: focus area or specific concern]"
---

# QA Loop — Autonomous Project Watchdog

One loop. Evaluates project state. Decides what to do. Acts or stays idle.

## Invocation
```
/loop 1h /qa-loop
/loop 1h /qa-loop focus on responsive layout
```

## Decision Tree

Run this on every tick:

```
1. IS THIS A SOFTWARE PROJECT?
   ├─ No → Log "not a software project, skipping" → IDLE
   └─ Yes ↓

2. READ PROJECT STATE
   Read: package.json (or equivalent), recent git log, tmp/qa-report.md (if exists),
         any task files, TODO/FIXME comments, open issues.
   Determine: What exists? What's expected? What's the gap?

3. IS THERE UNFINISHED DEV WORK?
   Check: failing tests, incomplete features, TODOs from plan, empty stub files,
          placeholder content, unimplemented routes.
   ├─ Yes → BRANCH: DEV (load domains/dev.md, pick highest-impact incomplete task, work it)
   └─ No ↓

4. HAS ANYTHING CHANGED SINCE LAST QA PASS?
   Compare: git diff since last qa-report timestamp, new commits, modified files.
   ├─ No changes + last QA was clean → Log "no changes, idle" → IDLE
   └─ Changes exist OR no prior QA ↓

5. BRANCH: QA
   Load domains/qa.md. Run the highest-priority applicable QA task:
   Visual regression → Functional → Responsive → Performance →
   Accessibility → Dead code → Links → Security.
   Do ONE category per tick — thorough beats broad.
```

## Rules

- **One action per tick.** Don't try to do everything in one pass. Pick the single highest-impact action and do it well. The loop runs again in an hour.
- **Always log.** Every tick appends to `tmp/qa-report.md` — even idle ticks get a one-line entry. This is your paper trail.
- **Never declare done.** There is no "all QA complete" state. There's always something to verify again, especially after any dev work.
- **Visual verification is mandatory.** If the project has a UI, every QA tick must include at least one screenshot. Code reading is not verification.
- **Fix safe things, flag risky things.** Auto-fix: missing alt text, obvious typos, unused imports. Flag for human: layout changes, feature decisions, architectural concerns.
- **Respect the dev domain.** When branching to dev work, follow TDD and the full agent pipeline. Don't take shortcuts because this is an automated loop.
- **Be skeptical by default.** "Looks fine" is not a finding. "Screenshot at tmp/qa-pass-3-home-mobile.png shows correct layout at 375px" is a finding.

## Focus Mode

If invoked with an argument (e.g., `/qa-loop focus on responsive layout`), weight that concern heavily in the decision tree. Still run the full evaluation, but prioritize the focus area when choosing which action to take.

## Report Format

```markdown
## [ISO timestamp] — Tick #N
Decision: DEV | QA | IDLE
Reason: [why this branch was chosen]
Action: [what was done]
Result: [outcome, with screenshot paths if applicable]
Next: [what the next tick should prioritize]
```

## Anti-Patterns (things this loop prevents)

- Claude finishing a task and sitting idle for 8 hours while obvious visual bugs exist.
- "All tests pass" declared as success when no visual verification happened.
- Responsive design claimed without testing at actual mobile widths.
- Performance regressions accumulating because nobody ran Lighthouse.
- Dead code and unused dependencies piling up between features.
