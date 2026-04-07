You are performing a comprehensive QA pass on a project. Work autonomously. Commit after each logical chunk. When done, write worker-status.json.

## Project Context (Bedrock Math / Mental Math Academy)
- **Framework**: Astro 5 + TypeScript, static output for GitHub Pages
- **Styling**: Tailwind CSS with CSS variables (NEVER hardcode colors)
- **Tests**: Node.js built-in `node --test` (unit/integration) + Vitest (alternative)
- **Auth**: Better Auth, **Database**: Turso/LibSQL + Drizzle ORM
- **AI**: Anthropic, OpenAI, Perplexity, Mistral, Gemini

## Routes
- `/` — homepage (index.astro)
- `/login` — sign-in page (login.astro)
- `/api/auth/[...all]` — Better Auth handler (dynamic, not prerendered)
- Protected (middleware-guarded): `/app/*`, `/dashboard`, `/assessment`, `/practice/*`, `/settings`, `/admin/*`

## Utilities
- `src/lib/auth/auth.ts` — Better Auth config
- `src/lib/db/schema.ts` — Drizzle schema (users, userDatabases, invitations, globalContent)
- `src/lib/db/turso.ts` — DB connection, getUserDatabase, createUserDatabase, initializeUserSchema
- `src/middleware.ts` — session injection + route protection + RBAC

## QA Steps

### 1. Start Dev Server
```bash
cd /Users/chad/Dropbox/Public/JS/Projects/bedrockmath.com
npm run dev &
sleep 3
```
Check it responds: `curl -s -o /dev/null -w "%{http_code}" http://localhost:4321`

### 2. Run Existing Tests
```bash
npm run test:unit
npm run test:integration
```
Fix any failures before proceeding.

### 3. Visual Route Check (Chrome)
Use `mcp__claude-in-chrome__*` tools to visit each public route:
- http://localhost:4321 (homepage)
- http://localhost:4321/login
Check for: layout breaks, missing styles, console errors, accessibility issues.

### 4. Security Audit
```bash
npm audit --audit-level=moderate
```
Fix any moderate+ vulnerabilities (`npm audit fix`).

### 5. Identify Refactoring Candidates
- Single-function files: `Grep` for files with only one exported function
- Missing file headers: check each `src/lib/**` and `src/middleware.ts` for a top-line comment
- Dead code: `Grep` for unused imports, commented-out blocks >5 lines, TODO/FIXME markers

### 6. Fix & Improve

#### a) Fix broken tests
Run `npm run test:unit && npm run test:integration`. Fix failures. Commit.

#### b) Add file headers
Add a single-line `// <filename> — <one-sentence purpose>` header to every lib file and middleware that lacks one. Commit.

#### c) Remove dead code
Delete commented-out blocks, unused imports, unreachable code. Commit.

#### d) Add unit tests for utilities
For each function in `src/lib/`:
- `getUserDatabase` / `createUserDatabase` / `initializeUserSchema` in `turso.ts`
- Auth config validation in `auth.ts`
- Schema shape validation in `schema.ts`
Write tests in `tests/unit/db.test.js` and `tests/unit/auth-config.test.js` using `node:test` + `node:assert`. Use mocks — don't require live DB/API keys. Commit.

#### e) Add BDD feature files for every route
For each route, create a Gherkin feature file under `tests/features/`:
- `tests/features/homepage.feature`
- `tests/features/login.feature`
- `tests/features/auth-api.feature`
- `tests/features/protected-routes.feature`

Format:
```gherkin
Feature: <Route Name>

  Scenario: <happy path>
    Given I am on "<url>"
    When <action>
    Then <expected result>

  Scenario: <edge case>
    ...
```

Do NOT require a BDD runner to be installed — feature files are spec documentation. Commit.

### 7. Final Test Run
```bash
npm run test:unit && npm run test:integration
```
All tests must pass.

### 8. Write worker-status.json
```json
{
  "status": "complete",
  "timestamp": "<ISO>",
  "summary": "<what was done>",
  "commits": ["<hash1>", "<hash2>", "..."],
  "tests_added": <N>,
  "files_removed": <N>,
  "lines_removed": <N>,
  "needs_attention": false
}
```

## Commit Style
Each commit message should be terse and accurate:
- `fix: repair broken test assertions in auth.test.js`
- `chore: add file headers to lib modules`
- `refactor: remove dead code and unused imports`
- `test: add unit tests for turso db utilities`
- `docs: add BDD feature files for all routes`

## Constraints
- Never hardcode colors — use CSS variables
- Never break prerender/static output (output: 'static' in astro.config.mjs)
- Never commit .env files
- `node --test` glob syntax: use explicit paths, not `**` globs (they don't expand in all shells)
- Keep tests fast — mock all external services (Turso, AI APIs)
