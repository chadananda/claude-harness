---
name: project-cleanup
description: Organize AI-generated project files into proper directory structure with automated classification, documentation generation, and consolidation. Works with Python, Node.js, Rust, Go, and all major languages.
license: MIT
---
# Project Cleanup - Automated File Organization

## Overview

AI development tends to create disorganized project structures with documentation, scripts, and temporary files scattered in the project root. This skill automatically organizes projects into clean, professional structures that follow language-specific conventions and best practices.

**Problem this solves:**
- Documentation files littered in project root (architecture.md, api.md, design.md, etc.)
- Temporary scripts and files in root or OS /tmp instead of project ./tmp/
- Long-lived scripts undocumented and unorganized
- No folder-level README.md files explaining structure
- Missing file tree in main README.md
- Undocumented files with unclear purpose

**Solution:**
- Automatically classify and move files to proper locations
- Generate comprehensive documentation for all folders
- Create file tree in main README.md with descriptions
- Consolidate duplicate/overlapping documentation
- Maintain clean project root with ONLY config files
- Language-agnostic approach (Python, Node.js, Rust, Go, etc.)

## Quick Start

```bash
# Install dependencies
pip install -r ~/.claude/skills/project-cleanup/scripts/requirements.txt

# Interactive cleanup (recommended)
@project-cleanup --mode=interactive

# Auto cleanup (safe defaults)
@project-cleanup --mode=auto

# Preview changes only
@project-cleanup --mode=dry-run
```

## File Classification Rules

### Root Level (Allowed)

**Config files that MUST stay in root:**
- Package managers: `package.json`, `yarn.lock`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`
- Build tools: `Makefile`, `justfile`, `CMakeLists.txt`
- Docker: `Dockerfile`, `docker-compose.yml`
- Linters/formatters: `.prettierrc`, `.eslintrc`, `tsconfig.json`, `ruff.toml`
- Git: `.gitignore`, `.gitattributes`, `.gitleaksignore`
- Environment: `.env.example` (NOT `.env`)

**Documentation that MUST stay in root:**
- `README.md` - Project overview (always root)
- `CHANGELOG.md` - Version history (conventional location)
- `LICENSE`, `LICENSE.txt`, `LICENSE.md` - Legal (GitHub expects root)
- `CODE_OF_CONDUCT.md`, `SECURITY.md` - Community health files

### Move to docs/

**Permanent documentation files:**
- API documentation: `API.md`, `api-reference.md`
- Architecture: `architecture.md`, `ARCHITECTURE.md`, `design.md`
- Guides: `user-guide.md`, `developer-guide.md`, `deployment.md`
- Planning: `roadmap.md`, `spec.md`, `requirements.md`
- Any other `.md` files NOT in root-allowed list

**Consolidation logic:**
- Multiple small docs on same topic → Ask user to consolidate
- Duplicate content (>30% similar headings) → Ask user to merge
- Cross-referencing docs → Keep separate, update links

### Move to scripts/

**Long-lived scripts:**
- Deployment: `deploy.sh`, `deploy.py`
- Build: `build.sh`, `build.py`
- Setup: `setup.sh`, `setup.py` (executable scripts, not Python setup.py)
- CI/CD: `ci.sh`, `test-runner.sh`

**Detection:**
- Has shebang line (`#!/usr/bin/env python`, `#!/bin/bash`)
- Executable permission set
- Common script names (deploy, build, setup, etc.)

**scripts/README.md auto-generated with:**
- Script name
- Purpose (from git history + LLM analysis)
- Usage examples
- Prerequisites/dependencies

### Move to ./tmp/

**Temporary files (project-local, NOT OS /tmp):**
- Suffixes: `*.tmp`, `*.temp`, `*.bak`, `*.swp`, `*.log`
- Dated files: `report-2024-11-12.json`, `backup-20241112.tar.gz`
- Prefixes: `temp_*`, `tmp_*`, `test_*` (in root only)
- Generated reports: Coverage, test results, profiling

**Important:** All temporary files go in `./tmp/` INSIDE the project, never `~/tmp` or `/tmp`

### Move to tests/

**Test files:**
- Extensions: `*.test.js`, `*.spec.ts`, `*_test.go`, `*_test.py`
- Test fixtures in root → Move to `tests/fixtures/`
- Test data → Move to `tests/data/`

## Workflow

### Step 1: Scan Project

```bash
# Scan project root and subdirectories
python ~/.claude/skills/project-cleanup/scripts/classify.py
```

**Scans for:**
- All files in project root
- Existing directory structure (docs/, scripts/, tests/, tmp/)
- Language indicators (package.json, Cargo.toml, go.mod, etc.)
- Git history for file purposes

### Step 2: Classify Files

**Classification categories:**
- `config` - Config files (action: keep_root)
- `doc` - Documentation (action: move_docs or keep_root for README.md/LICENSE)
- `script` - Executable scripts (action: move_scripts or move_tmp)
- `test` - Test files (action: move_tests)
- `temp` - Temporary files (action: move_tmp)
- `source` - Source code (action: keep - already in src/)
- `unknown` - Needs manual review

**Detection methods:**
1. **Pattern matching** (90% of files, fast)
   - Filename in known config patterns
   - File extension + known patterns
   - Shebang line detection

2. **Git history analysis** (context-aware)
   - Extract commit message when file was added
   - "Add authentication module" → Purpose: "Authentication module"

3. **LLM summarization** (10% of files, accurate)
   - Pass first 50 lines + filename to LLM
   - Prompt: "In 1 sentence, what is the purpose of this file?"
   - Cache results to avoid re-processing

### Step 3: Detect Project Type

**Language detection:**
- Python: `pyproject.toml`, `setup.py`, `requirements.txt`
- Node.js: `package.json`
- Rust: `Cargo.toml`
- Go: `go.mod`
- Monorepo: `lerna.json`, `pnpm-workspace.yaml`

**Apply language-specific rules:**
- Python: Use `src/`, `tests/`, don't suggest `cmd/`
- Go: Use `cmd/`, `pkg/`, `internal/`, don't suggest `src/`
- Node.js: Use `src/`, `dist/` (gitignored), `tests/`
- Rust: Use `src/`, `target/` (gitignored), `tests/`

See: `reference/language-patterns.md` for full patterns

### Step 4: Generate Reorganization Plan

**Plan includes:**
- Files to move (with source → destination)
- Directories to create (if missing)
- Documentation to consolidate (if duplicates detected)
- Links to update (when moving docs)
- .gitignore entries to add

**Example plan:**
```
Reorganization Plan
==================

CREATE DIRECTORIES:
  docs/
  scripts/
  tmp/

MOVE FILES:
  architecture.md → docs/architecture.md
  api.md → docs/api.md
  deploy.sh → scripts/deploy.sh
  test-results.json → tmp/test-results.json
  temp_script.py → tmp/temp_script.py

CONSOLIDATE (requires approval):
  docs/architecture.md + docs/design.md → docs/architecture.md
  (Reason: 65% overlapping headings)

UPDATE LINKS:
  src/README.md: architecture.md → ../docs/architecture.md
  docs/guide.md: api.md → api.md (same folder, no change)

ADD TO .gitignore:
  tmp/
  *.log
  *.tmp

GENERATE DOCUMENTATION:
  docs/README.md (new)
  scripts/README.md (new)
  README.md file tree section (update)
```

### Step 5: User Approval (Interactive Mode)

**Present plan with actions:**

```
Found 12 files to reorganize:

[1] Move architecture.md → docs/
[2] Move api.md → docs/
[3] Move deploy.sh → scripts/
[4] Move test.log → tmp/

Consolidation opportunities:
[!] docs/architecture.md + docs/design.md have 65% overlap
    → Merge into single docs/architecture.md? [y/n/preview]

Approve all? [y/n/selective]
```

**Auto mode:** Applies safe defaults (moves only, no consolidation without approval)
**Dry-run mode:** Shows plan, exits without changes

### Step 6: Execute Reorganization

**For each file move:**
```bash
# Create destination directory if needed
mkdir -p docs/

# Use git mv to preserve history
git mv architecture.md docs/architecture.md

# Update .gitignore
echo "tmp/" >> .gitignore
```

**Important:** Always use `git mv` NOT regular `mv` to preserve git history

### Step 7: Update Documentation Links

**Scan all files for links to moved documents:**
```python
# Find all markdown files
for md_file in all_markdown_files:
    # Replace old links with new links
    content = content.replace("[Architecture](architecture.md)", "[Architecture](docs/architecture.md)")
```

**Report updated files:**
```
Updated links in 5 files:
  src/README.md
  docs/guide.md
  docs/api.md
  CONTRIBUTING.md
  README.md
```

### Step 8: Generate Folder README.md Files

**For docs/README.md:**
```markdown
# Documentation

## Purpose
Comprehensive project documentation including API references, architecture decisions, and user guides.

## Contents

### File: architecture.md
**Purpose:** System architecture and design decisions
**Last Updated:** 2024-11-12 (via git log)
**Topics:** Component structure, data flow, technology choices

### File: api.md
**Purpose:** REST API endpoint documentation
**Last Updated:** 2024-11-10
**Topics:** Authentication, endpoints, request/response formats

## Related Documentation
- Main project overview: [../README.md](../README.md)
- Contributing guidelines: [../CONTRIBUTING.md](../CONTRIBUTING.md)
```

**For scripts/README.md:**
```markdown
# Scripts

## Overview
Build, deployment, and utility scripts for this project.

## Scripts

### `build.sh`
**Purpose:** Compiles the project for production
**Usage:** `./scripts/build.sh`
**Dependencies:** Node.js 18+, npm

### `deploy.sh`
**Purpose:** Deploys to staging or production
**Usage:** `./scripts/deploy.sh [staging|production]`
**Prerequisites:** AWS credentials configured

## Running Scripts

All scripts should be run from the project root:
```bash
./scripts/build.sh
```

For more details on deployment, see [../docs/deployment.md](../docs/deployment.md)
```

See: `templates/folder-readme-template.md` for full template

### Step 9: Generate File Tree in Main README.md

**Add/update section at bottom of README.md:**

```markdown
## Project Structure

```
project-root/
├─ README.md              # Project overview and quick start
├─ .gitignore             # Git ignore patterns
├─ package.json           # Node.js dependencies and scripts
├─ src/                   # Source code
│   ├─ components/        # React components
│   ├─ lib/               # Utility libraries
│   └─ routes/            # Application routes
├─ tests/                 # Test suite
│   ├─ unit/              # Unit tests
│   └─ integration/       # Integration tests
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   ├─ api.md             # API reference
│   ├─ architecture.md    # System architecture
│   └─ guides/            # User and developer guides
├─ scripts/               # Build and deployment scripts
│   ├─ README.md          # Scripts documentation
│   ├─ build.sh           # Production build script
│   └─ deploy.sh          # Deployment script
└─ tmp/                   # Temporary files (gitignored)
```
```

**File descriptions generated from:**
1. Git history (commit messages)
2. File content analysis (imports, structure)
3. LLM summarization for ambiguous files

See: `scripts/generate-tree.py` for implementation

### Step 10: Commit Changes

```bash
# Stage all changes
git add -A

# Commit with descriptive message
git commit -m "chore: organize project structure

- Moved documentation to docs/
- Moved scripts to scripts/
- Moved temporary files to tmp/
- Generated folder README.md files
- Updated main README.md with file tree
- Updated all documentation links
- Added tmp/ to .gitignore"

# Optional: Push to remote
git push
```

## Consolidation Logic

### Duplicate Detection

**Algorithm:**
```python
def detect_overlap(doc1, doc2):
    """Detect if two markdown docs have overlapping content"""
    headings1 = extract_markdown_headings(doc1)
    headings2 = extract_markdown_headings(doc2)

    common = set(headings1) & set(headings2)
    similarity = len(common) / min(len(headings1), len(headings2))

    if similarity > 0.7:
        return "DUPLICATE"  # Very high overlap
    elif similarity > 0.3:
        return "OVERLAP"    # Moderate overlap, ask user
    else:
        return "DISTINCT"   # Keep separate
```

**Thresholds:**
- `>70%`: Likely duplicate, suggest auto-merge (with approval)
- `30-70%`: Possible overlap, ask user
- `<30%`: Distinct documents, keep separate

### Consolidation Workflow

**When overlap detected:**

1. **Present to user:**
   ```
   Found overlapping documentation:

   docs/architecture.md (1,245 lines)
     - System Architecture
     - Component Design
     - Database Schema
     - API Design

   docs/design.md (892 lines)
     - System Design
     - Component Structure
     - Database Design
     - API Specification

   Overlap: 65% (similar headings, likely duplicate content)

   Options:
   [1] Merge into docs/architecture.md (keep both sets of content)
   [2] Keep separate (different audiences/purposes)
   [3] Preview diff (see what's different)
   [4] Skip (decide later)

   Choice [1-4]:
   ```

2. **If user chooses merge:**
   - Combine unique content from both
   - Keep comprehensive title: "System Architecture and Design"
   - Preserve all cross-references
   - Move old file to `docs/.archive/design.md` (don't delete)
   - Add note in archived file: "ARCHIVED: Content moved to architecture.md"

3. **Update all links:**
   - Scan all files for references to `design.md`
   - Update to point to `architecture.md`
   - Report: "Updated links in 7 files"

4. **Git commit:**
   ```bash
   git add docs/
   git commit -m "docs: consolidate architecture documentation

   - Merged design.md into architecture.md
   - Archived old design.md
   - Updated 7 files with new links"
   ```

See: `reference/consolidation-strategies.md` for detailed strategies

## Edge Cases

### Root-Level Exceptions

**LICENSE variants:**
- `LICENSE`, `LICENSE.txt`, `LICENSE.md` → ALL allowed in root
- Never move (GitHub expects root location for licensing)

**CONTRIBUTING.md:**
- Can be root OR `.github/CONTRIBUTING.md`
- If both exist → Ask user which to keep
- GitHub supports both locations

**Example files:**
- `example.py`, `example-config.json` → Move to `examples/`
- Exception: `.env.example` stays in root (convention)

### Monorepo Handling

**Detection:**
- Multiple `package.json` in subdirectories
- `lerna.json`, `nx.json`, `pnpm-workspace.yaml` present

**Action:**
- Apply cleanup to each workspace independently
- Don't move files between workspaces
- Each workspace gets own docs/, scripts/, tmp/
- Ask user: "Apply to all workspaces or specific ones?"

### Generated Files

**Auto-generated markers:**
- Comments: `// AUTO-GENERATED`, `# Generated by...`
- Tools: Prisma, Protobuf, GraphQL codegen

**Action:**
- Check if belongs in `src/generated/` or similar
- If truly temporary → Move to `tmp/` and gitignore
- If source of truth → Leave in place

### Hidden Directories

**Always ignore:**
- `.git/` - Never touch
- `node_modules/`, `venv/`, `__pycache__/` - Dependencies
- `.cache/`, `.pytest_cache/` - Temp caches

**Check:**
- `.vscode/`, `.idea/` - IDE settings
  - If in git → Leave alone
  - If not → Add to .gitignore

### Git History Preservation

**Always use `git mv`:**
```bash
# ✅ Correct (preserves history)
git mv architecture.md docs/architecture.md

# ❌ Wrong (loses history)
mv architecture.md docs/architecture.md
git add docs/architecture.md
```

**Verify history preserved:**
```bash
# Check file history across renames
git log --follow -- docs/architecture.md
```

See: `reference/edge-cases.md` for comprehensive edge case handling

## Configuration

### Optional .cleanup-config.yaml

**Place in project root to override defaults:**

```yaml
# Files/patterns to keep in root (override defaults)
keep_in_root:
  - deploy.py          # Custom deployment script
  - ARCHITECTURE.md    # Team prefers in root

# Files/directories to never move
never_move:
  - legacy/            # Don't reorganize legacy code
  - examples/*.py      # Keep examples in place
  - vendor/            # Third-party code

# Custom directory mappings
directory_mappings:
  planning: docs/planning   # Move planning/ to docs/planning
  guides: docs/guides        # Custom docs subdirectory

# Consolidation preferences
consolidation:
  auto_merge_threshold: 0.5  # Auto-suggest merge at 50% overlap
  ask_user: true             # Always ask before merging
  archive_old: true          # Archive in docs/.archive/

# File tree settings
file_tree:
  max_depth: 3               # How deep to show in tree
  include_hidden: false      # Don't show hidden files
  exclude_patterns:
    - node_modules
    - __pycache__
    - .git
    - dist
    - build
    - target

# Language-specific overrides
language_overrides:
  go:
    use_cmd_pkg_structure: true  # Force Go conventions
  python:
    prefer_src_layout: true      # Use src/ not flat layout
```

See: `templates/cleanup-config-template.yaml` for full template

## Integration

### User Command (Primary)

```bash
# From command line or Claude Code
/cleanup                  # Interactive mode
/cleanup --auto           # Auto mode (safe defaults)
/cleanup --dry-run        # Preview only
/cleanup --consolidate    # Focus on doc consolidation
```

### Agent Integration

**Coder agent (optional final step):**
```markdown
## Optional Step 8: Project Organization Check

Before reporting completion:
1. Check if new files created in root that shouldn't be there
2. If >3 misplaced files, suggest: "Run @project-cleanup to organize?"
3. User decides whether to run cleanup
```

**Doc agent (after generating docs):**
```markdown
## Step 5: Organize Documentation

After generating documentation:
1. Ensure docs in proper locations (docs/, not root)
2. Generate folder README.md if missing
3. Update main README.md with file tree
4. Optionally run @project-cleanup to validate organization
```

**Orchestrator (after project completion):**
```markdown
## Step 8: Final Cleanup (Optional)

After all tasks complete:
1. Suggest: "Project complete. Run @project-cleanup to organize structure?"
2. User decides
3. If yes, run cleanup and commit final organized state
```

### Pre-commit Hook (Optional)

**Add to .pre-commit-config.yaml:**
```yaml
repos:
  - repo: local
    hooks:
      - id: project-organization-check
        name: Validate project organization
        entry: .claude/skills/project-cleanup/scripts/validate.sh
        language: script
        stages: [commit]
        always_run: true
        verbose: true
```

**Behavior:**
- Warns (doesn't block) if new files added to root incorrectly
- Suggests proper location: "Consider moving api.md to docs/"
- User can proceed with commit or fix first

## Language-Specific Patterns

### Python

**Standard structure:**
```
project/
├─ README.md
├─ pyproject.toml
├─ LICENSE
├─ .gitignore
├─ src/
│   └─ package/
├─ tests/
├─ docs/
└─ scripts/
```

**Respect:**
- `pyproject.toml` in root (modern Python packaging)
- `src/` layout (recommended) or flat layout (legacy)
- `tests/` for test files
- Don't suggest `cmd/` or `pkg/` (Go conventions)

### Node.js/TypeScript

**Standard structure:**
```
project/
├─ README.md
├─ package.json
├─ tsconfig.json
├─ .gitignore
├─ src/
├─ dist/ (gitignored)
├─ tests/
├─ docs/
└─ scripts/
```

**Respect:**
- `package.json`, `tsconfig.json` in root
- `dist/` gitignored (build output)
- `src/` for source, `tests/` for tests

### Rust

**Standard structure:**
```
project/
├─ README.md
├─ Cargo.toml
├─ LICENSE
├─ .gitignore
├─ src/
│   └─ main.rs or lib.rs
├─ target/ (gitignored)
├─ tests/
└─ docs/
```

**Respect:**
- `Cargo.toml` in root
- `src/` for source (required by Cargo)
- `target/` gitignored (build output)
- `tests/` for integration tests (unit tests in src/)

### Go

**Standard structure:**
```
project/
├─ README.md
├─ go.mod
├─ LICENSE
├─ .gitignore
├─ cmd/
│   └─ appname/
│       └─ main.go
├─ pkg/
│   └─ public-lib/
├─ internal/
│   └─ private-code/
└─ docs/
```

**Respect:**
- `go.mod` in root
- `cmd/` for binaries (Go convention)
- `pkg/` for public libraries
- `internal/` for private code
- Don't suggest `src/` (not Go convention)

See: `reference/language-patterns.md` for comprehensive patterns

## Success Criteria

**Cleanup is successful when:**

1. ✅ Project root contains ONLY:
   - Config files (package.json, Cargo.toml, .gitignore, etc.)
   - README.md (project overview)
   - LICENSE (if present)
   - Community health files (CHANGELOG.md, CODE_OF_CONDUCT.md, SECURITY.md)

2. ✅ All documentation in `docs/`:
   - docs/README.md present with folder overview
   - Each file described (purpose, last updated)
   - Architecture, API, guides organized

3. ✅ All scripts in `scripts/`:
   - scripts/README.md present
   - Each script documented (purpose, usage, prerequisites)
   - Temporary scripts moved to tmp/

4. ✅ All temporary files in `./tmp/`:
   - tmp/ in .gitignore
   - No temp files in root
   - No files in OS /tmp or ~/tmp

5. ✅ Main README.md has file tree:
   - Shows project structure (2-3 levels deep)
   - Each file/folder has brief description
   - Up-to-date and accurate

6. ✅ No broken links:
   - All documentation links updated
   - Cross-references work correctly
   - Report shows files updated

7. ✅ Git history preserved:
   - Used `git mv` for all moves
   - `git log --follow` shows full history
   - No files deleted (archived instead)

8. ✅ Language conventions followed:
   - Python: src/ or flat layout
   - Node: src/, dist/ gitignored
   - Rust: src/, target/ gitignored
   - Go: cmd/, pkg/, internal/

9. ✅ All folders documented:
   - Each folder has README.md (where appropriate)
   - .claude/agents/ and .claude/skills/ respect no-README rule
   - Purpose and contents clear

10. ✅ User approval received:
    - Consolidations approved (if any)
    - Plan reviewed in interactive mode
    - All changes committed with clear message

**Cleanup fails if:**

- ❌ Breaks build or tests
- ❌ Creates broken links
- ❌ Violates language conventions
- ❌ Moves files user explicitly wanted in root (via config)
- ❌ Loses git history
- ❌ Merges docs without permission
- ❌ Uses OS /tmp instead of ./tmp/
- ❌ Deletes files (should archive)

## Troubleshooting

### "Too many files to reorganize"

**Solution:**
```bash
# Start with docs only
@project-cleanup --focus=docs --dry-run

# Then scripts
@project-cleanup --focus=scripts --dry-run

# Then everything
@project-cleanup --auto
```

### "Consolidation suggestions seem wrong"

**Solution:**
- Use `.cleanup-config.yaml` to disable auto-consolidation:
  ```yaml
  consolidation:
    ask_user: true
    auto_merge_threshold: 0.9  # Very high bar
  ```
- Review overlap manually: `@project-cleanup --consolidate --dry-run`

### "Moved files broke imports/build"

**Solution:**
- Script files moved shouldn't break imports (they're executable)
- If build breaks, check:
  - Are source files in src/ moved? (shouldn't be)
  - Are config files moved? (shouldn't be)
  - Run `git log` to see what moved
  - Revert: `git revert <commit-hash>`

### "Want to keep file in root"

**Solution:**
Create `.cleanup-config.yaml`:
```yaml
keep_in_root:
  - deploy.py
  - ARCHITECTURE.md
```

### "Monorepo getting messy"

**Solution:**
```bash
# Run cleanup on each workspace
cd packages/workspace1 && @project-cleanup --auto
cd packages/workspace2 && @project-cleanup --auto

# Or from root
@project-cleanup --monorepo --workspace=all
```

## Reference Documentation

- **File Classification:** `reference/file-classification.md` - Detailed classification patterns
- **Consolidation Strategies:** `reference/consolidation-strategies.md` - Doc consolidation logic
- **Language Patterns:** `reference/language-patterns.md` - Language-specific structures
- **Edge Cases:** `reference/edge-cases.md` - Comprehensive edge case handling

## Templates

- **Folder README:** `templates/folder-readme-template.md` - Template for folder docs
- **Scripts README:** `templates/scripts-readme-template.md` - Template for scripts folder
- **File Tree:** `templates/file-tree-template.md` - Template for main README.md section
- **Config:** `templates/cleanup-config-template.yaml` - User configuration template

## Examples

- **Messy Project:** `examples/messy-project-before.md` - Before cleanup
- **Clean Project:** `examples/clean-project-after.md` - After cleanup
- **Consolidation:** `examples/consolidation-example.md` - Doc consolidation walkthrough
- **Integration:** `examples/integration-example.md` - How agents use this skill

## License

MIT License - See LICENSE.txt

---

**For AI agents:** This skill ensures clean, professional project structure. Run after significant development or when root directory becomes cluttered. Always ask user before consolidating docs. Use `git mv` to preserve history. 📁
