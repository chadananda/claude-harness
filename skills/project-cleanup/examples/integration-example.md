# Integration Example: Using @project-cleanup with AI Agents

This example shows how the project-cleanup skill integrates with AI development workflows.

## Scenario

After an AI agent builds a React app, the project root is cluttered with documentation, scripts, and temporary files that need organization.

## Initial State

```bash
$ ls -1
README.md
package.json
architecture.md          # ❌ Should be in docs/
api-guide.md            # ❌ Should be in docs/
deployment.md           # ❌ Should be in docs/
testing-guide.md        # ❌ Should be in docs/
build.sh                # ❌ Should be in scripts/
deploy.sh               # ❌ Should be in scripts/
setup-dev.sh            # ❌ Should be in scripts/
test-output.json        # ❌ Should be in tmp/
coverage.html           # ❌ Should be in tmp/
debug.log               # ❌ Should be in tmp/
quick-test.sh           # ❌ Should be in tmp/
example-test.js         # ❌ Should be in tests/
.gitignore
src/
node_modules/
```

## Agent Invocation

### Option 1: User Invokes Directly

```
User: "@project-cleanup --mode=interactive"

@project-cleanup:
"Scanning project directory...

Found 11 files that need organization:
- 4 documentation files → docs/
- 3 scripts → scripts/
- 4 temporary files → tmp/
- 1 test file → tests/

Running duplicate detection on documentation...

[1] OVERLAP: Moderate overlap (42%)
    Doc 1: architecture.md (167 lines)
    Doc 2: api-guide.md (134 lines)
    Recommendation: Consider consolidating

Would you like to:
1. Auto-organize with consolidation suggestions
2. Auto-organize without consolidation
3. See detailed plan first

Your choice?"

User: "1"

@project-cleanup:
"Creating organization plan...

Plan:
1. Move docs to docs/
   - architecture.md → docs/architecture.md
   - api-guide.md → docs/api-guide.md (consider merging with architecture.md)
   - deployment.md → docs/deployment.md
   - testing-guide.md → docs/testing-guide.md

2. Move scripts to scripts/
   - build.sh → scripts/build.sh
   - deploy.sh → scripts/deploy.sh
   - setup-dev.sh → scripts/setup-dev.sh

3. Move temporary files to tmp/
   - test-output.json → tmp/test-output.json
   - coverage.html → tmp/coverage.html
   - debug.log → tmp/debug.log
   - quick-test.sh → tmp/quick-test.sh

4. Move tests to tests/
   - example-test.js → tests/example-test.js

5. Generate folder README.md files:
   - docs/README.md
   - scripts/README.md

6. Update main README.md with file tree

7. Update .gitignore (add tmp/)

8. Git commit all changes

Proceeding..."
```

### Option 2: Orchestrator Auto-Invokes

**After @coder completes feature implementation:**

```
Orchestrator:
"✅ Feature implementation complete (3 agents, 18 minutes)

Deliverables:
- src/components/Dashboard.jsx
- src/lib/api.js
- tests/dashboard.test.js
- docs/dashboard-api.md
- docs/architecture-updates.md

Scanning project structure...

⚠️  Detected 8 files in root that should be organized:
- 5 documentation files
- 2 scripts
- 3 temporary test outputs

Invoking @project-cleanup --mode=auto..."

@project-cleanup:
"Auto-organizing project (non-interactive mode)...

✅ Moved 5 documentation files to docs/
✅ Moved 2 scripts to scripts/
✅ Moved 3 temporary files to tmp/
✅ Generated docs/README.md
✅ Generated scripts/README.md
✅ Updated main README.md with file tree
✅ Updated .gitignore (added tmp/)
✅ Git committed: 'chore: organize project structure'

Project organization complete."

Orchestrator:
"✅ Project cleanup complete. Git committed.

Final project structure:
- Root: 4 files (config only)
- docs/ (5 files + README.md)
- scripts/ (2 files + README.md)
- tmp/ (gitignored, 3 files)
- tests/ (organized)

Moving to integration testing..."
```

## Detailed Workflow

### Step 1: Detection and Classification

```bash
$ python scripts/classify.py --json

{
  "classified_files": [
    {
      "path": "architecture.md",
      "category": "doc",
      "action": "move_to_docs",
      "reason": "Documentation file",
      "destination": "docs/architecture.md"
    },
    {
      "path": "build.sh",
      "category": "script",
      "action": "move_to_scripts",
      "reason": "Executable script",
      "destination": "scripts/build.sh"
    },
    {
      "path": "test-output.json",
      "category": "temp",
      "action": "move_to_tmp",
      "reason": "Temporary output file",
      "destination": "tmp/test-output.json"
    }
  ]
}
```

### Step 2: Duplicate Detection

```bash
$ python scripts/detect-duplicates.py --min-similarity 0.3

Found 1 potentially overlapping document pair:

[1] OVERLAP: Moderate overlap (42%)
    Doc 1: architecture.md (167 lines)
    Doc 2: api-guide.md (134 lines)
    Heading similarity: 42%
    Content similarity: 35%
    Shared headings: 6
    Examples: api endpoints, authentication, data models

Recommendation:
  • Review for consolidation: architecture.md + api-guide.md
```

### Step 3: Interactive Consolidation

```
@project-cleanup:
"I found overlapping documentation. Would you like to consolidate?

Option 1: Merge api-guide.md into architecture.md
  - Creates comprehensive architecture + API doc
  - Eliminates duplication
  - Single source of truth

Option 2: Keep separate
  - architecture.md focuses on design
  - api-guide.md focuses on usage
  - Some duplication remains

Option 3: Create hierarchy
  - docs/architecture/
    - overview.md
    - api-design.md
  - Splits by topic

Your choice? (1/2/3)"

User: "1"

@project-cleanup:
"Merging api-guide.md into architecture.md...

Merge plan:
1. Keep architecture.md as base (more comprehensive)
2. Add unique API sections from api-guide.md
3. Consolidate overlapping sections
4. Archive old api-guide.md

Proceeding..."
```

### Step 4: Folder Documentation Generation

```
@project-cleanup:
"Generating folder documentation...

Created: docs/README.md
"""
# Documentation

## Purpose
Comprehensive project documentation including architecture, API guides, deployment procedures, and testing strategies.

## Contents

### File: architecture.md
**Purpose:** System architecture and API design
**Last Updated:** 2024-11-12
**Topics:** Component structure, API endpoints, data models, authentication

### File: deployment.md
**Purpose:** Deployment procedures
**Last Updated:** 2024-11-10
**Topics:** Staging deployment, production deployment, rollback procedures

### File: testing-guide.md
**Purpose:** Testing strategies and guidelines
**Last Updated:** 2024-11-08
**Topics:** Unit tests, integration tests, E2E tests, coverage requirements
"""

Created: scripts/README.md
"""
# Scripts

## Overview
Build, deployment, and development setup scripts.

## Scripts

### `build.sh`
**Purpose:** Compiles project for production
**Usage:** `./scripts/build.sh`
**Prerequisites:** Node.js 18+, npm

### `deploy.sh`
**Purpose:** Deploys to staging or production
**Usage:** `./scripts/deploy.sh [staging|production]`
**Prerequisites:** AWS CLI, kubectl configured

### `setup-dev.sh`
**Purpose:** Sets up local development environment
**Usage:** `./scripts/setup-dev.sh`
**Prerequisites:** None (installs dependencies)
"""
```

### Step 5: File Tree Generation

```bash
$ python scripts/generate-tree.py --with-descriptions

my-project/
├─ README.md              # Project overview and quick start
├─ package.json           # Node.js dependencies and scripts
├─ .gitignore             # Git ignore patterns (includes tmp/)
├─ src/                   # Source code
│   ├─ components/        # React components
│   ├─ lib/               # Utility libraries
│   └─ routes/            # Application routes
├─ tests/                 # Test suite
│   ├─ unit/              # Unit tests
│   ├─ integration/       # Integration tests
│   └─ fixtures/          # Test fixtures
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   ├─ architecture.md    # System architecture and API design
│   ├─ deployment.md      # Deployment procedures
│   └─ testing-guide.md   # Testing strategies
├─ scripts/               # Build and deployment scripts
│   ├─ README.md          # Scripts documentation
│   ├─ build.sh           # Production build script
│   ├─ deploy.sh          # Deployment script
│   └─ setup-dev.sh       # Development setup
└─ tmp/                   # Temporary files (gitignored)
    ├─ test-output.json   # Test results
    ├─ coverage.html      # Coverage report
    └─ debug.log          # Debug logs
```

### Step 6: Git Operations

```bash
# Create directories
mkdir -p docs scripts tmp tests

# Move files (preserving history)
git mv architecture.md docs/
git mv api-guide.md docs/  # Will be consolidated
git mv deployment.md docs/
git mv testing-guide.md docs/

git mv build.sh scripts/
git mv deploy.sh scripts/
git mv setup-dev.sh scripts/

git mv test-output.json tmp/
git mv coverage.html tmp/
git mv debug.log tmp/
git mv quick-test.sh tmp/

git mv example-test.js tests/

# Update .gitignore
echo "tmp/" >> .gitignore

# Create folder README files
# (generated by project-cleanup)

# Update main README.md
# (file tree added by generate-tree.py)

# Commit
git add -A
git commit -m "chore: organize project structure

- Moved documentation to docs/ (consolidated architecture + API)
- Moved scripts to scripts/
- Moved temporary files to tmp/ (gitignored)
- Moved tests to tests/
- Generated folder README.md files
- Updated main README.md with file tree
- Updated .gitignore

Co-authored-by: project-cleanup skill"
```

## Integration with Other Skills

### With @security-scan

```
Orchestrator:
"Running post-development checks...

1. Running @security-scan...
   ✅ No API keys in tracked files

2. Running @project-cleanup...
   ✅ Project structure organized
   ✅ No temporary files in root
   ✅ All folders documented

All checks passed."
```

### With @coder

```
@coder:
"✅ Feature implementation complete.

Created files:
- src/components/Dashboard.jsx
- docs/dashboard-architecture.md
- tests/dashboard.test.js
- scripts/deploy-dashboard.sh

Signaling completion to orchestrator..."

Orchestrator:
"Received completion from @coder.

Running @project-cleanup --mode=auto...

✅ Organized new files:
- docs/dashboard-architecture.md → docs/features/dashboard.md
- scripts/deploy-dashboard.sh → scripts/deploy-dashboard.sh (kept in scripts/)

Project remains organized."
```

### With @doc

```
@doc:
"Creating documentation for authentication system...

Generated:
- docs/authentication-overview.md
- docs/api/auth-endpoints.md
- src/lib/auth/README.md (JSDoc inline)

Files placed in appropriate directories automatically."

[No cleanup needed - @doc already followed organization rules]
```

## Configuration File Usage

**Project-specific config: `.cleanup-config.yaml`**

```yaml
# Keep these in root (exceptions to rules)
keep_in_root:
  - ARCHITECTURE.md  # This project documents architecture in root
  - deploy.py        # Primary deployment script

# Never move these (legacy or special)
never_move:
  - legacy/
  - vendor/

# Consolidation preferences
consolidation:
  auto_merge_threshold: 0.6  # Auto-merge at 60% similarity
  ask_user: true             # Ask before consolidating
  archive_old: true          # Keep old files in .archive/

# Custom destination mappings
custom_destinations:
  "*-guide.md": "docs/guides/"
  "test-*.json": "tmp/test-results/"
  "*.log": "tmp/logs/"

# Language-specific overrides
language_overrides:
  go:
    use_cmd_pkg_structure: true
  python:
    use_src_layout: true
```

## Pre-commit Hook Integration

**In `.git/hooks/pre-commit` or `.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: local
    hooks:
      - id: project-organization-check
        name: Check project organization
        entry: .claude/skills/project-cleanup/scripts/validate.sh
        language: script
        always_run: true
```

**Effect:**

```bash
$ git commit -m "Add new feature"

⚠️  Project Organization Warning

The following files are being added to the project root:

  ✗ new-feature-docs.md → docs/
  ✗ deploy-new-feature.sh → scripts/

Recommendation: Move files to appropriate directories before committing

To organize your project automatically, run:
  @project-cleanup --mode=interactive

Proceeding with commit (warning only).
```

## API Usage (Programmatic)

**From Python scripts:**

```python
from project_cleanup import ProjectCleaner

# Initialize
cleaner = ProjectCleaner(root_path=".", config=".cleanup-config.yaml")

# Classify files
classifications = cleaner.classify_all()

# Detect duplicates
duplicates = cleaner.detect_duplicates(min_similarity=0.3)

# Generate plan
plan = cleaner.generate_plan(
    auto_consolidate=False,
    ask_user=True
)

# Execute plan
cleaner.execute_plan(
    plan,
    git_commit=True,
    commit_message="chore: organize project structure"
)
```

## Expected Results

### Before

```
Project root: 19 files
Documentation: Scattered (5 files in root)
Scripts: Mixed (3 permanent, 2 temporary in root)
Temp files: 4 files committed to git
Tests: 2 files in root
Folder docs: None
Main README: No file tree
```

### After

```
Project root: 4 files (config only)
Documentation: Organized (docs/ with README.md)
Scripts: Organized (scripts/ with README.md)
Temp files: All in tmp/ (gitignored)
Tests: Organized (tests/ directory)
Folder docs: docs/README.md, scripts/README.md
Main README: Complete file tree with descriptions
Git history: Preserved via git mv
```

## Benefits

1. **Automatic Integration**: Orchestrator can auto-invoke after development phases
2. **Non-disruptive**: Works with git history preservation
3. **Configurable**: Project-specific overrides via .cleanup-config.yaml
4. **Preventive**: Pre-commit hooks warn before committing misplaced files
5. **Self-documenting**: Generates folder README.md files automatically
6. **Language-agnostic**: Works with Python, Node, Rust, Go, etc.

## See Also

- [messy-project-before.md](messy-project-before.md) - Example of messy project
- [clean-project-after.md](clean-project-after.md) - Example of clean project
- [consolidation-example.md](consolidation-example.md) - Doc consolidation details
