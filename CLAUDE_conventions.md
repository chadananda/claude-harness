# Project Conventions

## Root = Config Only

README.md, LICENSE, .gitignore, package.json, pyproject.toml, Cargo.toml, tsconfig.json, docker-compose.yml, Makefile, .env.example, dotfiles, lock files.

## Directory Structure

- `src/` or `lib/` - production code
- `tests/` - all test files (TDD.md governs)
- `docs/` - documentation
- `scripts/` - reusable utilities
- `tmp/` - temporary files (gitignored)

## Git Discipline

- Commit after every completed task group
- Never commit `tmp/` or `.claude/context/`
- Use `./tmp/` never `~/tmp`
