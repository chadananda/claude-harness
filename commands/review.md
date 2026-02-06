Multi-agent code review: Examine the code above with fresh eyes as if you're a senior developer doing a critical PR review. What would break? What edge cases are missed? What could be more efficient or secure? Look for bugs, race conditions, performance bottlenecks, security issues, and architectural improvements.

Then create a detailed plan for fixing any serious problems you find and implement the fixes with lint checks.

Execute these sub-agent tasks in parallel:

Sub-agent 1 - Documentation sync: Update all documentation to reflect current code changes and direction shifts. Focus on README.md and all .md files in /planning/ folder. Ensure docs accurately represent current functionality, API changes, and architectural decisions.

Sub-agent 2 - Test coverage audit: Review code for complete unit test coverage, verify existing tests match current expectations, add missing tests for each file, ensure all test scripts are properly configured in package.json, run npm test to validate everything passes. If tests fail, either fix the failing tests or report code flaws that the tests expose.

Sub-agent 3 - Security and performance review: Focus specifically on security vulnerabilities, performance bottlenecks, memory leaks, and optimization opportunities. Implement critical fixes immediately.

Coordinate results from all sub-agents, resolve any conflicts, and provide a comprehensive summary of all changes made.

