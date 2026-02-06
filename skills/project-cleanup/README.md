# Project Cleanup Skill

**Automatically organize AI-generated projects with clean directory structures and comprehensive documentation.**

## Problem

AI-assisted development often creates cluttered project roots with:
- Documentation files scattered everywhere (`.md` files in root)
- Temporary scripts mixed with production scripts
- Test outputs and debug logs committed to git
- Undocumented folders and files
- No clear project structure overview

## Solution

The `@project-cleanup` skill automatically:
- ✅ Moves documentation to `docs/` (consolidating overlaps)
- ✅ Moves scripts to `scripts/` with documentation
- ✅ Moves temporary files to project-local `tmp/` (gitignored)
- ✅ Organizes tests into `tests/` directory
- ✅ Generates `README.md` for every folder documenting contents
- ✅ Updates main `README.md` with complete file tree
- ✅ Preserves git history with `git mv`
- ✅ Works with any language (Python, Node, Rust, Go, etc.)

## Quick Start

### Option 1: AI Agent Invocation

```
User: "@project-cleanup --mode=interactive"
```

The skill will:
1. Scan your project directory
2. Classify all files (config, doc, script, test, temp)
3. Detect duplicate/overlapping documentation
4. Present organization plan
5. Ask for approval
6. Execute moves (with git history preservation)
7. Generate folder README.md files
8. Update main README.md with file tree
9. Git commit all changes

### Option 2: Auto Mode (Non-Interactive)

```
User: "@project-cleanup --mode=auto"
```

Automatically organizes without asking (useful for orchestrator integration).

### Option 3: Manual Script Execution

```bash
# Classify files
python ~/.claude/skills/project-cleanup/scripts/classify.py

# Detect duplicate docs
python ~/.claude/skills/project-cleanup/scripts/detect-duplicates.py

# Generate file tree
python ~/.claude/skills/project-cleanup/scripts/generate-tree.py
```

## What Gets Organized

### Root → docs/
- `*.md` files (except README.md, CONTRIBUTING.md, LICENSE.md)
- `architecture.md`, `api-docs.md`, `deployment.md`, etc.
- Consolidates overlapping documentation

### Root → scripts/
- Executable scripts (`.sh`, `.py`, `.js` with shebang)
- Build scripts, deployment scripts
- Generates `scripts/README.md` documenting each script

### Root → tmp/ (gitignored)
- Temporary output files (`test-results.json`, `coverage.html`)
- Debug logs (`debug.log`, `*.tmp`)
- Temporary scripts (`quick-test.sh`, `temp-*.sh`)

### Root → tests/
- Test files not already in test directory
- Test fixtures and data files

### Stays in Root
- Configuration files (`package.json`, `pyproject.toml`, `.gitignore`)
- Essential documentation (`README.md`, `LICENSE`, `CONTRIBUTING.md`)
- Build tools (`Makefile`, `Dockerfile`)

## Features

### 1. Intelligent File Classification

```python
# Detects file type and destination
architecture.md      → docs/architecture.md
build.sh             → scripts/build.sh
test-output.json     → tmp/test-output.json
example-test.js      → tests/example-test.js
package.json         → (stays in root)
```

### 2. Documentation Consolidation

Detects overlapping documentation using heading similarity:

```
[1] OVERLAP: Moderate overlap (42%)
    Doc 1: architecture.md (167 lines)
    Doc 2: api-guide.md (134 lines)
    Recommendation: Consider consolidating
```

Offers merge strategies:
- Merge into single comprehensive doc
- Create hierarchical structure
- Split by audience (internal vs external)
- Keep separate (if minimal overlap)

### 3. Folder Documentation Generation

Automatically creates `README.md` in each folder:

```markdown
# Documentation

## Purpose
Comprehensive project documentation including architecture and API guides.

## Contents

### File: architecture.md
**Purpose:** System architecture and design decisions
**Last Updated:** 2024-11-12
**Topics:** Component structure, API design, data models
```

### 4. File Tree Generation

Updates main `README.md` with complete project structure:

```
my-project/
├─ README.md              # Project overview and quick start
├─ package.json           # Node.js dependencies
├─ src/                   # Source code
│   ├─ components/        # React components
│   └─ lib/               # Utility libraries
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   └─ architecture.md    # System architecture
├─ scripts/               # Build and deployment scripts
│   ├─ README.md          # Scripts documentation
│   └─ build.sh           # Production build script
└─ tmp/                   # Temporary files (gitignored)
```

### 5. Git History Preservation

Always uses `git mv` to preserve file history:

```bash
git mv architecture.md docs/
git mv deploy.sh scripts/
git log --follow docs/architecture.md  # History preserved!
```

### 6. Language-Agnostic

Works with any language ecosystem:

- **Python**: `pyproject.toml`, `requirements.txt`, `src/` or flat layout
- **Node.js**: `package.json`, `src/`, `dist/` (gitignored)
- **Rust**: `Cargo.toml`, `src/`, `target/` (gitignored)
- **Go**: `go.mod`, `cmd/`, `pkg/`, `internal/`
- **Ruby**: `Gemfile`, `lib/`, `spec/`
- **Java**: `pom.xml`, `src/main/`, `target/` (gitignored)

### 7. Configuration Support

Optional `.cleanup-config.yaml` for project-specific rules:

```yaml
# Keep these in root (exceptions)
keep_in_root:
  - ARCHITECTURE.md  # This project documents architecture in root

# Never move these
never_move:
  - legacy/
  - vendor/

# Consolidation preferences
consolidation:
  auto_merge_threshold: 0.6
  ask_user: true

# Custom mappings
custom_destinations:
  "*-guide.md": "docs/guides/"
  "test-*.json": "tmp/test-results/"
```

### 8. Pre-Commit Hook

Optional validation to prevent adding files to root:

```bash
# Install pre-commit hook
cp ~/.claude/skills/project-cleanup/scripts/validate.sh .git/hooks/pre-commit

# Now warns when committing root files
$ git commit -m "Add feature"

⚠️  Project Organization Warning
The following files are being added to the project root:
  ✗ new-feature-docs.md → docs/

Recommendation: Move to appropriate directories
Run: @project-cleanup --mode=interactive
```

## Installation

### Dependencies

```bash
pip install -r ~/.claude/skills/project-cleanup/scripts/requirements.txt
```

Required packages:
- `pyyaml` - Configuration file parsing
- `markdown` - Markdown processing
- `beautifulsoup4` - HTML parsing
- `gitpython` - Git operations
- `tqdm` - Progress bars
- `click` - CLI interface

### Optional: Pre-commit Hook

```bash
# Copy validation script
cp ~/.claude/skills/project-cleanup/scripts/validate.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Or add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: project-organization-check
        name: Check project organization
        entry: ~/.claude/skills/project-cleanup/scripts/validate.sh
        language: script
        always_run: true
```

## Usage Examples

### Example 1: Basic Cleanup

```
User: "@project-cleanup"

@project-cleanup:
"Scanning project...

Found 11 files to organize:
- 4 docs → docs/
- 3 scripts → scripts/
- 4 temp files → tmp/

Would you like to proceed? (y/n)"

User: "y"

@project-cleanup:
"✅ Organized 11 files
✅ Generated docs/README.md
✅ Generated scripts/README.md
✅ Updated main README.md with file tree
✅ Updated .gitignore (added tmp/)
✅ Git committed: 'chore: organize project structure'

Done!"
```

### Example 2: With Consolidation

```
User: "@project-cleanup --consolidate"

@project-cleanup:
"Found overlapping documentation:
- architecture.md + api-guide.md (42% overlap)

Merge strategy:
1. Merge into architecture.md (single source of truth)
2. Archive old api-guide.md
3. Update cross-references

Proceed? (y/n)"

User: "y"

@project-cleanup:
"✅ Merged api-guide.md into architecture.md
✅ Archived api-guide.md to docs/.archive/
✅ Updated 3 files with new links
✅ Git committed: 'docs: consolidate architecture documentation'

Done!"
```

### Example 3: Orchestrator Integration

The orchestrator can automatically invoke after development:

```
Orchestrator:
"✅ Feature complete (3 agents, 18 minutes)

Scanning project structure...
⚠️  8 files in root need organization

Invoking @project-cleanup --mode=auto...

✅ Project organized. Git committed.
Moving to integration testing..."
```

## Project Structure

```
~/.claude/skills/project-cleanup/
├─ SKILL.md                           # Comprehensive skill guide
├─ README.md                          # This file
├─ LICENSE.txt                        # MIT License
├─ reference/                         # Reference documentation
│   ├─ file-classification.md         # File type detection rules
│   ├─ consolidation-strategies.md    # Doc consolidation logic
│   ├─ language-patterns.md           # Language-specific conventions
│   └─ edge-cases.md                  # Special cases and exceptions
├─ templates/                         # Generation templates
│   ├─ folder-readme-template.md      # Template for folder README.md
│   ├─ scripts-readme-template.md     # Template for scripts/README.md
│   ├─ file-tree-template.md          # Template for main README file tree
│   └─ cleanup-config-template.yaml   # Configuration file template
├─ scripts/                           # Executable scripts
│   ├─ requirements.txt               # Python dependencies
│   ├─ classify.py                    # File classification tool
│   ├─ generate-tree.py               # File tree generator
│   ├─ detect-duplicates.py           # Duplicate documentation detector
│   └─ validate.sh                    # Pre-commit validation hook
└─ examples/                          # Usage examples
    ├─ messy-project-before.md        # Before cleanup
    ├─ clean-project-after.md         # After cleanup
    ├─ consolidation-example.md       # Doc consolidation walkthrough
    └─ integration-example.md         # AI agent integration

Reference: SKILL.md (lines 1-650)
```

## Integration with Other Skills

### With @security-scan

```
Orchestrator: "Running post-development checks...
  1. @security-scan → ✅ No API keys
  2. @project-cleanup → ✅ Project organized"
```

### With @coder

```
@coder: "✅ Feature complete. Created:
  - src/Dashboard.jsx
  - docs/dashboard.md
  - scripts/deploy-dashboard.sh"

Orchestrator: "@project-cleanup --mode=auto
  ✅ Files already in correct locations"
```

## Benefits

### For Developers
- 🎯 Clean project structure
- 📚 Easy to find documentation
- 🔍 Scripts are documented
- 📋 File tree shows what's where

### For Teams
- 📖 Self-documenting projects
- 🤝 Consistent organization across projects
- 🚀 New contributors onboard faster
- 🧹 No clutter in root

### For CI/CD
- ✅ Scripts in predictable locations
- 🚫 Temporary files gitignored
- 📦 Clean repository structure

### For Git
- 🕰️ History preserved (git mv)
- 📝 Clear commit messages
- 🔍 Can trace file origins

## Before/After Comparison

| Aspect | Before | After |
|--------|--------|-------|
| Root files | 19 files | 4 files (config only) |
| Documentation | Scattered (5 in root) | Organized (docs/ + README) |
| Scripts | Mixed (5 in root) | Organized (scripts/ + README) |
| Temp files | 7 committed | All gitignored in tmp/ |
| Folder docs | None | Every folder has README.md |
| File tree | Not in README | Complete tree with descriptions |
| Git history | N/A | Preserved with git mv |

## Troubleshooting

### "Script can't find git command"
Ensure git is installed and in PATH: `which git`

### "File already exists at destination"
Use `--force` flag or manually resolve conflicts first

### "Permission denied"
Check file permissions: `chmod +x scripts/*.sh`

### "Configuration file not found"
Create `.cleanup-config.yaml` or use defaults

### "Pre-commit hook doesn't run"
Ensure executable: `chmod +x .git/hooks/pre-commit`

## Configuration Reference

See [cleanup-config-template.yaml](templates/cleanup-config-template.yaml) for all options.

## Documentation

- **SKILL.md** - Comprehensive guide with all details
- **reference/** - Deep dives on specific topics
- **examples/** - Real-world usage examples
- **templates/** - Generation templates

## Contributing

When adding new classification rules:
1. Update `scripts/classify.py`
2. Add patterns to `reference/file-classification.md`
3. Add test cases to `examples/`
4. Update `SKILL.md` with new rules

## License

MIT License - See [LICENSE.txt](LICENSE.txt)

## See Also

- [SKILL.md](SKILL.md) - Full skill documentation
- [examples/integration-example.md](examples/integration-example.md) - AI agent integration
- [reference/file-classification.md](reference/file-classification.md) - Classification rules
- [@security-scan](../security-scan/README.md) - Complementary security skill

---

**Created by:** Claude Code AI Assistant
**Version:** 1.0.0
**Last Updated:** 2024-11-12
