Complete trunk development cycle: We're using trunk-style development with short-lived feature branches. The goal is to prepare our current work for merging into main.

1) Senior dev review - critically analyze code for bugs, edge cases, security issues, performance problems
2) Fix planning - create detailed plan for any serious issues found
3) Implementation - fix issues, lint thoroughly, add/run tests
4) AI code cleanup - this is critical: merge related functions into single files, remove excessive logging/debug code, delete temporary script files, refactor complex functions into simple pure functions with exported helpers, add vitest unit tests for each helper function
5) Git workflow - we need to fetch latest main branch from origin first, then merge our changes into updated main, increment package.json version appropriately, push to main with tags, then create a new randomly-named short-lived branch to continue development

The cleanup step is essential because AI tends to over-engineer and create too many separate files, excessive logging, and overly complex functions. Clean, simple, testable code is the goal before merging to main.

Make sure to remove any temporary test data added by testing or test-runs. Remove folders as well as files to avoid accidentally deleting actual code files later during cleanup.

6) FINAL STEP: After completing all steps, run the compact command to minimize output. Then report the commit message and new version number and the new branch name.
