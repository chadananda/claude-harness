# Domain: review — Code Review
Quality: duplication; functions >50 lines; unclear naming; missing boundary error handling; unhandled edge cases; inefficient patterns.
Reuse: Grep for existing utilities — flag reinvented wheels.
YAGNI (HIGH): single-use → inline; abstractions <3 uses → remove; helper files 1-2 exports → merge; >3 files per feature → consolidate.
Test after EVERY change — catches regressions before they stack.
Priority: reuse existing > remove dead code > inline single-use > consolidate > simplify > naming.
Never sacrifice readability for size — code read more than written.
Stop minimizing when LOC plateaus — diminishing returns risk bugs.
