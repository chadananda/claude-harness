# Domain: review — Code Review
Use `/review` skill or `code-review:code-review` for standalone reviews outside the dev pipeline.

Project-specific checks (apply on top of built-in review):
- Reuse: Grep for existing utilities — flag reinvented wheels.
- YAGNI (HIGH): single-use → inline; abstractions <3 uses → remove; helper files 1-2 exports → merge; >3 files per feature → consolidate.
- Test after EVERY change — catches regressions before they stack.
- Priority: reuse existing > remove dead code > inline single-use > consolidate > simplify > naming.
- Never sacrifice readability for size — code read more than written.
- Stop minimizing when LOC plateaus — diminishing returns risk bugs.
- Use `pr-review-toolkit:code-simplifier` for minimization pass.
- Use `pr-review-toolkit:silent-failure-hunter` when reviewing error handling.
