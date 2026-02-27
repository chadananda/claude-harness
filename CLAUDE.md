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

Explicit *dev, *doc, *content, *plan, *review, *seo activate a domain. No command or no match = no domain loaded.
Ad-hoc tasks, questions, file ops, OS help, brainstorming — just work directly. No domain needed.

## Conventions
- Root = config only — cluttered root signals disorganized project.
- src/|lib/ code; tests/ tests; docs/ docs; scripts/ utils; tmp/ temp (gitignored)
- Commit after each task group. Never commit tmp/ or .claude/context/. Use ./tmp/ not ~/tmp.

## Autonomy
Work autonomously until blocked on human decision. Never ask "should I proceed?" — shifts cognitive load for non-decisions. Invoke stuck agent when genuinely stuck — real ambiguity needs human judgment.
