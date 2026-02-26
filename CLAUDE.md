# Orchestrator
Strict Red-Green-Refactor TDD. Agents load @TDD.md automatically.

## Conventions
- Root = config only (README, LICENSE, .gitignore, package.json, pyproject.toml, Cargo.toml, tsconfig.json, docker-compose.yml, Makefile, .env.example, dotfiles, locks) — cluttered root signals disorganized project.
- `src/`|`lib/` code; `tests/` tests; `docs/` docs; `scripts/` utils; `tmp/` temp (gitignored)
- Commit after each task group — creates rollback points, keeps diffs reviewable. Never commit `tmp/` or `.claude/context/`. Use `./tmp/` not `~/tmp` — project-scoped prevents cross-contamination.

@CLAUDE_workflow.md
@CLAUDE_agents.md
