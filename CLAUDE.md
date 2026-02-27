# Orchestrator

## Modes
Optional structured workflows. Load ONLY when the request clearly fits a mode — most work needs no mode at all. Read modes/{mode}.md before starting when a mode applies — rules are not in default context; skipping them causes incorrect behavior (e.g., no TDD in dev work).

| Mode | When | File |
|------|------|------|
| dev | implementation, features, coding, TDD, refactoring | modes/dev.md |
| plan | architecture, system design, project planning | modes/plan.md |
| doc | documentation, READMEs, content writing | modes/doc.md |
| review | code review, audits, quality checks | modes/review.md |
| seo | SEO analysis, site audits, content optimization, GEO | modes/seo.md |
| plan-saas | SaaS project planning (idea → launch-ready) | modes/plan-saas.md |

Explicit *dev, *doc, *plan, *review, *seo activate a mode. No command or no match = no mode loaded.
Ad-hoc tasks, questions, file ops, OS help, brainstorming — just work directly. No mode needed.

## Conventions
- Root = config only — cluttered root signals disorganized project.
- src/|lib/ code; tests/ tests; docs/ docs; scripts/ utils; tmp/ temp (gitignored)
- Commit after each task group. Never commit tmp/ or .claude/context/. Use ./tmp/ not ~/tmp.

## Autonomy
Work autonomously until blocked on human decision. Never ask "should I proceed?" — shifts cognitive load for non-decisions. Invoke stuck agent when genuinely stuck — real ambiguity needs human judgment.
