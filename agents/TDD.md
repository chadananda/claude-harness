# TDD — Red-Green-Refactor

## Rules
1. Never implement without failing test first — proves requirement exists and implementation satisfies it.
2. One test at a time — isolates failures to single behavior.
3. Run tests every phase — execution is proof, assumptions aren't.
4. Minimum code to pass — over-engineering makes refactoring harder and tests less meaningful.
5. Test fails → fix code, not test — changing tests hides bugs. Only change if expectation wrong; state why.
6. Refactor = structure only — behavioral changes without test updates create silent regressions. Test breaks → undo.
7. Report each phase — audit trail catches skipped steps: 🔴 RED (test+failure) → 🟢 GREEN (change+pass) → 🔵 REFACTOR (improvement+pass)

## Anti-Patterns
- Test + implementation same step — can't verify test detects failure if never seen failing.
- Hardcoding returns for multiple tests — false confidence without solving problem.
- Tests after implementation — post-hoc tests rationalize, don't specify.
- Batch tests then implement — loses red-green feedback loop.
- Skip test execution — unexecuted tests are just comments.

## BDD
`describe` = context; `it` = "should [behavior]". Name by behavior not implementation — impl-coupled names break on refactor. Body: given → when → then. One assertion; independent; deterministic — multiple assertions obscure which behavior failed.

### Web: Gherkin + Playwright
Feature files in business language. ARIA-first locators (`getByRole`, `getByLabel`, `getByText`). No XPath/CSS-class selectors. axe-core a11y per scenario. See bdd-playwright skill.

## Workflow
1. Restate requirement → smallest testable increments
2. Outer: failing acceptance test (stays red across unit cycles)
3. Inner: 🔴→🟢→🔵 until acceptance green
4. Refactor whole; full suite; stay green

## Spikes
Spike = throwaway. Learn, delete, TDD fresh — promoting spike code bypasses test-driven design, bakes in accidental complexity.
