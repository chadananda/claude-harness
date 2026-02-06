# Example: Messy Project (Before Cleanup)

This example shows a typical messy project root after AI-assisted development.

## Project Structure (Before)

```
my-project/
├─ README.md                      # ✅ Correct location
├─ package.json                   # ✅ Correct location
├─ .gitignore                     # ✅ Correct location
├─ architecture.md                # ❌ Should be in docs/
├─ api-documentation.md           # ❌ Should be in docs/
├─ deployment-guide.md            # ❌ Should be in docs/
├─ design-decisions.md            # ❌ Should be in docs/
├─ user-guide.md                  # ❌ Should be in docs/
├─ deploy.sh                      # ❌ Should be in scripts/
├─ build.sh                       # ❌ Should be in scripts/
├─ setup-dev.sh                   # ❌ Should be in scripts/
├─ temp-test.sh                   # ❌ Should be in tmp/
├─ quick-fix.sh                   # ❌ Should be in tmp/
├─ test-results.json              # ❌ Should be in tmp/
├─ coverage-report.html           # ❌ Should be in tmp/
├─ backup-2024-11-12.tar.gz       # ❌ Should be in tmp/
├─ debug-output.log               # ❌ Should be in tmp/
├─ test.tmp                       # ❌ Should be in tmp/
├─ example-test.js                # ❌ Should be in tests/ or examples/
├─ fixture-data.json              # ❌ Should be in tests/fixtures/
├─ LICENSE                        # ✅ Correct location
├─ src/
│   ├─ index.js
│   ├─ lib/
│   └─ components/
├─ node_modules/                  # ✅ Dependency directory
└─ dist/                          # ✅ Build output (should be gitignored)
```

## Problems

### 1. Documentation Scattered in Root
- `architecture.md` - Architecture documentation
- `api-documentation.md` - API reference
- `deployment-guide.md` - Deployment procedures
- `design-decisions.md` - Design rationale
- `user-guide.md` - User documentation

**Problem:** Hard to find, not organized, no overview

### 2. Scripts Unorganized
- `deploy.sh` - Deployment script
- `build.sh` - Build script
- `setup-dev.sh` - Development setup
- `temp-test.sh` - Temporary test script
- `quick-fix.sh` - One-off script

**Problem:** Mix of permanent and temporary scripts, no documentation

### 3. Temporary Files in Root
- `test-results.json` - Test output
- `coverage-report.html` - Coverage report
- `backup-2024-11-12.tar.gz` - Dated backup
- `debug-output.log` - Log file
- `test.tmp` - Temporary file

**Problem:** Clutters root, should be gitignored

### 4. Test Files Misplaced
- `example-test.js` - Test file in root
- `fixture-data.json` - Test fixture in root

**Problem:** Should be organized with other tests

### 5. No Folder Documentation
- No `docs/README.md` explaining documentation structure
- No `scripts/README.md` explaining what scripts do
- No file tree in main `README.md`

## Classification Results

Running `classify.py` on this project:

```bash
$ python classify.py .

Project: /path/to/my-project
Language: node

Classified 15 files:

⚙️ package.json
   Action: Keep in root
   Reason: Standard configuration file

⚙️ .gitignore
   Action: Keep in root
   Reason: Standard configuration file

📄 README.md
   Action: Keep in root
   Reason: Root documentation file

📄 LICENSE
   Action: Keep in root
   Reason: Root documentation file

📄 architecture.md
   Action: Move to docs/
   Reason: Documentation file

📄 api-documentation.md
   Action: Move to docs/
   Reason: Documentation file

📄 deployment-guide.md
   Action: Move to docs/
   Reason: Documentation file

📄 design-decisions.md
   Action: Move to docs/
   Reason: Documentation file

📄 user-guide.md
   Action: Move to docs/
   Reason: Documentation file

📜 deploy.sh
   Action: Move to scripts/
   Reason: Executable script

📜 build.sh
   Action: Move to scripts/
   Reason: Executable script

📜 setup-dev.sh
   Action: Move to scripts/
   Reason: Executable script

📜 temp-test.sh
   Action: Move to tmp/
   Reason: Temporary script

📜 quick-fix.sh
   Action: Move to tmp/
   Reason: Temporary script

🗑️ test-results.json
   Action: Move to tmp/
   Reason: Temporary file

🗑️ coverage-report.html
   Action: Move to tmp/
   Reason: Temporary file

🗑️ backup-2024-11-12.tar.gz
   Action: Move to tmp/
   Reason: Temporary file

🗑️ debug-output.log
   Action: Move to tmp/
   Reason: Temporary file

🗑️ test.tmp
   Action: Move to tmp/
   Reason: Temporary file

🧪 example-test.js
   Action: Move to tests/
   Reason: Test file

🧪 fixture-data.json
   Action: Move to tests/
   Reason: Test file
```

## Duplicate Detection

Running `detect-duplicates.py`:

```bash
$ python detect-duplicates.py .

Found 2 potentially overlapping document pairs:

[1] OVERLAP: Moderate overlap, consider consolidation
    Doc 1: architecture.md (245 lines)
    Doc 2: design-decisions.md (189 lines)
    Heading similarity: 45%
    Content similarity: 38%
    Shared headings: 8
    Examples: system architecture, component design, database schema
    Unique to Doc 1: 10
    Unique to Doc 2: 6

[2] OVERLAP: Moderate overlap, consider consolidation
    Doc 1: api-documentation.md (512 lines)
    Doc 2: user-guide.md (287 lines)
    Heading similarity: 32%
    Content similarity: 28%
    Shared headings: 5
    Examples: authentication, endpoints, error handling
    Unique to Doc 1: 18
    Unique to Doc 2: 11

Recommendations:
  • Review for consolidation: architecture.md + design-decisions.md
  • Review for consolidation: api-documentation.md + user-guide.md
```

## User Impact

**Developer trying to find information:**
- "Where's the deployment guide?" → Searches root directory
- "How do I run tests?" → No scripts/README.md to check
- "What's in this project?" → No file tree in README.md

**New contributor onboarding:**
- Overwhelmed by cluttered root directory
- Doesn't know which files are important
- Unclear where to find documentation

**CI/CD pipeline:**
- Temp files committed to git (shouldn't be)
- Build artifacts in root (should be in dist/ and gitignored)
- Scripts scattered (hard to reference in CI config)

## Next Steps

See [clean-project-after.md](clean-project-after.md) for the organized version of this project.
