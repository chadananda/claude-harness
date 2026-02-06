---
name: plan
description: Interactive requirements gathering and task decomposition. Phase 0 gathers requirements with user input. Phase 1+ outputs native Tasks with DAG dependencies for parallel execution.
---

# /plan - Project Planning Skill

## Overview

Transform vague requirements into executable task DAGs using native Claude Code Tasks. This is the SINGLE canonical planning system.

## When to Use

- Starting a new feature or project
- Requirements are unclear or complex
- Work can be parallelized
- TDD workflow applies (most development tasks)

## Workflow

### Phase 0: Requirements Gathering (INTERACTIVE)

**5W1H Analysis:**
- **What**: Describe the feature/project in concrete terms
- **Why**: What problem does this solve?
- **Who**: Who are the users? (human, API, other systems)
- **Where**: Where will this run? (local, cloud, CI)
- **When**: Any deadlines or phasing constraints?
- **How**: How will users interact with it?
- **Which**: Any tech preferences or constraints?

**MoSCoW Prioritization:**
- **Must Have**: MVP blockers - won't ship without these
- **Should Have**: Important but not blocking
- **Could Have**: Nice to have if time permits
- **Won't Have**: Explicitly out of scope (prevents scope creep)

**Scenarios (Given-When-Then):**
```
Given [context/precondition]
When [action/trigger]
Then [expected outcome]
```

**Ambiguity Resolution:**
- Vague terms ("fast", "scalable") -> Ask for specifics
- Missing quantities ("handle users") -> Ask "how many?"
- Undefined terms -> Ask for examples
- Technology choices -> Present 2-3 options with tradeoffs

**WAIT for user approval before proceeding to Phase 1.**

### Phase 1: Research (AUTONOMOUS)

Before decomposing tasks:

1. **Codebase Research**
   - Use Grep/Glob to find existing utilities, components, patterns
   - Read key files to understand coding style and conventions
   - Document what exists and what can be reused

2. **Technology Verification**
   - Check package.json or equivalent for current versions
   - Verify compatibility of existing dependencies
   - Research latest versions of needed libraries

3. **Anti-Hallucination Checklist**
   Before specifying ANY dependency or utility:
   - Verify module exists in package.json (or registry)
   - Confirm version compatibility
   - Verify import paths exist
   - Catalog existing utilities to reuse
   - If you can't verify something, ask the user

### Phase 2: Task Decomposition

**Task Sizing Tiers:**

| Size | Time | Scope | Example |
|------|------|-------|---------|
| XS | 5-15 min | Single file <50 LOC, no deps | Config file, simple utility |
| S | 15-30 min | Single file <150 LOC, 1-2 deps | API endpoint, form component |
| M | 30-60 min | 1-2 files <300 LOC, multiple deps | Multi-step wizard, complex validation |
| L | 60+ min | **MUST break down further** | Never allowed in final plan |

**No task should exceed 60 minutes. Break L tasks into S/M subtasks.**

**Automatic Breakdown Rules:**
- Task >60 min -> split into subtasks
- Multiple files to create (>3) -> one task per file/component
- Multiple concerns -> separate data/logic/UI
- Long sequential steps (>5) -> create pipeline of smaller tasks

**Testability Categorization (schedule in this order):**

| Tier | Type | Schedule | Test Strategy |
|------|------|----------|---------------|
| 1 | Pure functions | FIRST | Unit tests, 100% coverage |
| 2 | Business logic | SECOND | Unit tests with mocks, >80% |
| 3 | Integration points | THIRD | E2E tests, slower feedback |
| 4 | Configuration/glue | LAST | Smoke tests only |

Front-load Tier 1 tasks to get fast test feedback early.

### Phase 3: Output Native Tasks

Use TaskCreate for each task with proper dependencies:

```
TaskCreate:
  subject: "Implement password hashing utility"
  description: |
    Size: XS (10 min) | Testability: Tier 1 (pure function)
    File: src/lib/auth/hash.ts
    Exports: hashPassword(plain) -> hash, verifyPassword(plain, hash) -> boolean
    Tests: tests/lib/auth/hash.test.ts
    Reuse: [list existing utilities to import]
    TDD: Red-green-refactor per TDD.md
  activeForm: "Implementing password hashing"
```

**Dependency Mapping via DAG:**
- Tasks with no blockedBy run in parallel (Group 1)
- Tasks blocked by Group 1 run together after (Group 2)
- Continue until all tasks assigned
- Validate: no circular dependencies, every task assigned to a group

```
TaskUpdate:
  taskId: [login-task-id]
  addBlockedBy: [hash-task-id, jwt-task-id]
```

### Phase 4: Execute

After tasks created:
1. Fan out parallel tasks to subagents (team-lead per task)
2. Each task follows TDD.md via coder -> reviewer -> tester -> doc pipeline
3. Commit after each group completes
4. Update task status as work progresses

## Task Specification Quality

**Good spec (coder can execute mechanically):**
```
Size: S (25 min) | Testability: Tier 2
File: src/routes/api/auth/login.ts
Imports: { hashPassword } from src/lib/auth/hash, { generateToken } from src/lib/auth/jwt
Pattern: Follow src/routes/api/admin/auth/+server.ts lines 23-45
Adapts: Change endpoint path, use getUserByEmail instead of getAdminByUsername
Tests: tests/routes/api/auth/login.test.ts
Success: POST /api/auth/login returns 200+JWT on valid creds, 401 on invalid
```

**Bad spec (forces coder to research):**
```
Implement JWT authentication
```

Every spec must include: file paths, imports, patterns to follow, success criteria.

## Key Principles

1. **Native Tasks Only** - Use TaskCreate/TaskUpdate, NOT JSON files or TodoWrite
2. **DAG Dependencies** - Use addBlockedBy for proper ordering
3. **Test-First** - Pure functions before integration
4. **60 Min Max** - Break down larger tasks
5. **Phase 0 Blocks** - Never proceed without user approval on requirements
6. **Anti-Hallucination** - Verify every dependency and import path exists
7. **Minimal Code** - Specify reuse of existing utilities, no unnecessary abstractions

## Success Criteria

- User has approved Phase 0 requirements
- All tasks created with TaskCreate
- Dependencies mapped via addBlockedBy
- No task exceeds 60 minutes
- Test-first ordering applied
- Every task spec includes file paths, imports, patterns, success criteria
- Ready for parallel execution
