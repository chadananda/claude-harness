# File Classification Reference

Comprehensive guide to classifying files in any project type (Python, Node.js, Rust, Go, etc.).

## Classification Categories

### 1. Config Files (keep_root)

**Definition:** Configuration files that control project behavior, dependencies, or tooling.

**Universal Patterns:**

**Package Managers:**
- `package.json`, `package-lock.json` - npm
- `yarn.lock`, `pnpm-lock.yaml` - Alternative Node package managers
- `pyproject.toml` - Modern Python packaging (PEP 518)
- `setup.py`, `setup.cfg` - Legacy Python packaging
- `requirements.txt`, `requirements-dev.txt` - Python dependencies
- `Pipfile`, `Pipfile.lock` - Pipenv
- `poetry.lock` - Poetry
- `Cargo.toml`, `Cargo.lock` - Rust
- `go.mod`, `go.sum` - Go modules
- `Gemfile`, `Gemfile.lock` - Ruby
- `composer.json`, `composer.lock` - PHP

**Build Tools:**
- `Makefile` - Make build system
- `justfile` - Just command runner
- `CMakeLists.txt` - CMake
- `build.gradle`, `settings.gradle` - Gradle
- `pom.xml` - Maven
- `meson.build` - Meson

**Docker:**
- `Dockerfile` - Docker image definition
- `docker-compose.yml`, `docker-compose.yaml` - Docker Compose
- `.dockerignore` - Docker ignore patterns

**Linters/Formatters:**
- `.prettierrc`, `.prettierrc.json`, `.prettierrc.js` - Prettier
- `.eslintrc`, `.eslintrc.json`, `.eslintrc.js` - ESLint
- `tsconfig.json`, `jsconfig.json` - TypeScript/JavaScript config
- `.editorconfig` - Editor configuration
- `ruff.toml`, `ruff.config.toml` - Ruff (Python)
- `pyproject.toml` [tool.black], [tool.ruff] - Python tools
- `.rustfmt.toml` - Rust formatter
- `.golangci.yml` - Go linters

**Git:**
- `.gitignore` - Git ignore patterns
- `.gitattributes` - Git attributes
- `.gitleaksignore` - Gitleaks false positives
- `.gitmodules` - Git submodules

**Environment:**
- `.env.example`, `.env.template` - Environment variable templates
- **NEVER `.env`** - Should be gitignored, not committed

**CI/CD:**
- `.github/workflows/*.yml` - GitHub Actions
- `.gitlab-ci.yml` - GitLab CI
- `.travis.yml` - Travis CI
- `Jenkinsfile` - Jenkins
- `.circleci/config.yml` - CircleCI

**IDE (if committed):**
- `.vscode/settings.json` - VS Code (if team shares)
- `.idea/` - IntelliJ (if team shares)
- Usually should be in .gitignore, but some teams commit

**Action:** Keep in root directory (these are expected there by tools)

---

### 2. Documentation (move_docs or keep_root)

**Root-Allowed Documentation (NEVER move):**

- `README.md` - Project overview, always root
- `CHANGELOG.md` - Version history, conventional location
- `LICENSE`, `LICENSE.txt`, `LICENSE.md` - Legal, GitHub expects root
- `CODE_OF_CONDUCT.md` - Community health file
- `SECURITY.md` - Security policy
- `CONTRIBUTING.md` - Can be root OR `.github/CONTRIBUTING.md`

**Move to docs/**

**API Documentation:**
- `API.md`, `api.md`, `api-reference.md`
- `endpoints.md`, `rest-api.md`, `graphql-schema.md`

**Architecture:**
- `architecture.md`, `ARCHITECTURE.md`
- `design.md`, `design-decisions.md`
- `adr/` (Architecture Decision Records) → `docs/adr/`

**Guides:**
- `user-guide.md`, `usage.md`, `tutorial.md`
- `developer-guide.md`, `development.md`
- `deployment.md`, `deployment-guide.md`
- `installation.md`, `setup.md`

**Planning:**
- `roadmap.md`, `ROADMAP.md`
- `spec.md`, `specification.md`
- `requirements.md`, `features.md`
- `TODO.md` (unless actively used, then keep root)

**Technical:**
- `database-schema.md`, `schema.md`
- `testing.md`, `testing-strategy.md`
- `performance.md`, `optimization.md`

**Detection Logic:**

```python
def is_documentation(filename: str) -> bool:
    """Check if file is documentation"""
    # Must be markdown
    if not filename.endswith('.md'):
        return False

    # Root-allowed docs stay
    ROOT_ALLOWED = {
        'README.md', 'CHANGELOG.md',
        'LICENSE.md', 'CODE_OF_CONDUCT.md',
        'SECURITY.md', 'CONTRIBUTING.md'
    }
    if filename in ROOT_ALLOWED:
        return False  # Don't move these

    # Everything else goes to docs/
    return True
```

---

### 3. Scripts (move_scripts or move_tmp)

**Long-Lived Scripts (move to scripts/):**

**Deployment:**
- `deploy.sh`, `deploy.py`, `deploy.js`
- `release.sh`, `publish.sh`

**Build:**
- `build.sh`, `build.py`
- `compile.sh`, `bundle.sh`

**Setup:**
- `setup.sh` (executable script, not Python setup.py)
- `install.sh`, `bootstrap.sh`

**CI/CD:**
- `ci.sh`, `test-runner.sh`
- `lint.sh`, `format.sh`

**Utilities:**
- `backup.sh`, `restore.sh`
- `migrate.sh`, `seed.sh`

**Detection:**

```python
import os
import stat

def is_script(filepath: Path) -> bool:
    """Check if file is an executable script"""
    # Check extension
    if filepath.suffix in {'.sh', '.bash', '.zsh'}:
        return True

    # Check executable permission
    if os.access(filepath, os.X_OK):
        return True

    # Check shebang
    try:
        with open(filepath, 'r') as f:
            first_line = f.readline()
            if first_line.startswith('#!'):
                return True
    except:
        pass

    return False

def is_temporary_script(filepath: Path) -> bool:
    """Check if script is temporary"""
    name = filepath.name

    # Dated filenames
    if any(char.isdigit() for char in name):
        if re.search(r'\d{4}-\d{2}-\d{2}', name):  # Has date
            return True
        if re.search(r'\d{8}', name):  # Has datestring
            return True

    # Temp prefixes
    if name.startswith(('temp_', 'tmp_', 'test_')):
        return True

    # Common temp script names
    if name in {'test.sh', 'temp.sh', 'quick.sh', 'debug.sh'}:
        return True

    return False
```

**Temporary Scripts (move to ./tmp/):**
- `temp_*.sh`, `tmp_*.py`
- `test.sh`, `debug.sh`, `quick.sh`
- Scripts with dates: `backup-2024-11-12.sh`
- One-off scripts with no long-term value

**Special Cases:**

- `setup.py` (Python) - Config file, keep root (NOT a script)
- `manage.py` (Django) - Source code, keep in place
- npm scripts in `package.json` - Keep inline (conventional)

---

### 4. Test Files (move_tests)

**Test Files:**

**Extensions:**
- `*.test.js`, `*.test.ts`, `*.test.jsx`, `*.test.tsx` - Jest/Vitest
- `*.spec.js`, `*.spec.ts` - Jasmine/Mocha
- `*_test.go` - Go tests
- `*_test.py`, `test_*.py` - pytest
- `*_spec.rb` - RSpec

**Detection:**

```python
def is_test_file(filepath: Path) -> bool:
    """Check if file is a test file"""
    name = filepath.name

    # Test extensions
    TEST_PATTERNS = [
        r'\.test\.(js|ts|jsx|tsx)$',
        r'\.spec\.(js|ts|jsx|tsx)$',
        r'_test\.(py|go)$',
        r'test_.*\.py$',
        r'_spec\.rb$',
    ]

    for pattern in TEST_PATTERNS:
        if re.search(pattern, name):
            return True

    return False
```

**Test Directories:**
- `tests/`, `test/`, `__tests__/` - Main test directories
- `spec/` - RSpec tests
- `tests/fixtures/` - Test fixtures
- `tests/data/` - Test data

**Test Fixtures (keep in tests/):**
- `tests/fixtures/*.json` - Test data
- `tests/snapshots/` - Snapshot tests
- `tests/__snapshots__/` - Jest snapshots

**Action:** If in root → Move to `tests/` or `test/` (use existing convention)

---

### 5. Temporary Files (move_tmp)

**Suffixes:**
- `*.tmp`, `*.temp` - Temporary files
- `*.bak`, `*.backup` - Backup files
- `*.swp`, `*.swo`, `*~` - Editor swap files
- `*.log` - Log files (unless in logs/)
- `*.pid` - Process ID files
- `*.lock` (transient locks, NOT package manager locks)

**Prefixes:**
- `temp_*`, `tmp_*` - Temporary files
- `test_*` (in root) - Test scripts/files
- `debug_*` - Debug files

**Dated Files:**
- `report-2024-11-12.json`
- `backup-20241112.tar.gz`
- `*-YYYYMMDD.*`

**Generated Reports:**
- `coverage/` - Coverage reports
- `test-results/`, `test-output/` - Test outputs
- `.nyc_output/` - NYC coverage
- `*.coverage` - Python coverage data

**Detection:**

```python
import re
from datetime import datetime

def is_temporary(filepath: Path) -> bool:
    """Check if file is temporary"""
    name = filepath.name

    # Temp suffixes
    TEMP_SUFFIXES = {
        '.tmp', '.temp', '.bak', '.backup',
        '.swp', '.swo', '.log', '.pid'
    }
    if any(name.endswith(suffix) for suffix in TEMP_SUFFIXES):
        return True

    # Temp prefixes
    if name.startswith(('temp_', 'tmp_', 'test_', 'debug_')):
        return True

    # Dated filenames (likely backups/reports)
    if re.search(r'\d{4}-\d{2}-\d{2}', name):
        return True
    if re.search(r'\d{8}', name):
        return True

    # Editor files
    if name.endswith('~') or name.startswith('.'):
        if filepath.suffix in {'.swp', '.swo', '.swn'}:
            return True

    return False
```

**Action:** Move to `./tmp/` (project-local, NOT OS /tmp) and add to .gitignore

---

### 6. Source Code (keep)

**Detection:** Should already be in `src/`, `lib/`, `pkg/`, `cmd/`, etc.

**Python:**
- `src/package/*.py`
- `lib/*.py`
- `package/*.py` (flat layout)

**Node.js:**
- `src/**/*.js`, `src/**/*.ts`
- `lib/**/*.js`
- `index.js`, `main.js` (entry points)

**Rust:**
- `src/**/*.rs`
- `src/main.rs`, `src/lib.rs`

**Go:**
- `cmd/**/*.go`
- `pkg/**/*.go`
- `internal/**/*.go`
- `*.go` (flat layout for small projects)

**Action:** Leave in place (already properly organized)

---

### 7. Unknown (review)

**Needs manual review:**
- Files that don't match any pattern
- Ambiguous names like `data.json`, `config.yaml`
- Custom project-specific files

**Detection:**

```python
def classify_file(filepath: Path) -> dict:
    """Classify a file into a category"""
    name = filepath.name

    # Try each category in order
    if is_config_file(name):
        return {'category': 'config', 'action': 'keep_root'}

    if is_root_allowed_doc(name):
        return {'category': 'doc', 'action': 'keep_root'}

    if is_temporary(filepath):
        return {'category': 'temp', 'action': 'move_tmp'}

    if is_test_file(filepath):
        return {'category': 'test', 'action': 'move_tests'}

    if is_documentation(name):
        return {'category': 'doc', 'action': 'move_docs'}

    if is_script(filepath):
        if is_temporary_script(filepath):
            return {'category': 'script', 'action': 'move_tmp'}
        else:
            return {'category': 'script', 'action': 'move_scripts'}

    # Unknown - needs review
    return {'category': 'unknown', 'action': 'review'}
```

**Review strategy:**
1. Check git history: `git log --follow -- <file>`
2. Analyze first 50 lines for patterns
3. Ask LLM: "In 1 sentence, what is the purpose of this file?"
4. Ask user in interactive mode

---

## Decision Tree

```
File in project root?
    ↓
Is it in CONFIG_PATTERNS?
    YES → keep_root
    NO ↓
Is it in ROOT_ALLOWED_DOCS?
    YES → keep_root
    NO ↓
Does it have temp suffix/prefix?
    YES → move_tmp
    NO ↓
Does it match test pattern?
    YES → move_tests
    NO ↓
Is it a .md file?
    YES → move_docs
    NO ↓
Is it executable/has shebang?
    YES →
        Is it temporary script?
            YES → move_tmp
            NO → move_scripts
    NO ↓
Check git history + LLM → review
```

##

 Priority Order

1. **Config files** (highest priority - never move these)
2. **Root-allowed docs** (LICENSE, README.md - never move)
3. **Temporary files** (move immediately to avoid clutter)
4. **Test files** (clear patterns, move to tests/)
5. **Documentation** (move to docs/)
6. **Scripts** (move to scripts/ or tmp/)
7. **Unknown** (requires manual review)

---

## False Positives

### Files that LOOK temporary but aren't:

**Example files:**
- `.env.example` - Stays in root (convention)
- `example.config.js` - May be documentation, check context

**Test fixtures:**
- `tests/fixtures/temp_data.json` - Part of test suite, don't move

**Build outputs:**
- `dist/bundle.js` - Should be gitignored, not moved

**Strategy:**
- Check parent directory context
- Check .gitignore (if already ignored, don't move)
- Check git history (if long history, not temporary)

---

## Multi-Language Projects

**Monorepo detection:**
```python
def is_monorepo(root: Path) -> bool:
    """Check if project is a monorepo"""
    MONOREPO_MARKERS = [
        'lerna.json',
        'nx.json',
        'pnpm-workspace.yaml',
        'rush.json',
    ]

    for marker in MONOREPO_MARKERS:
        if (root / marker).exists():
            return True

    # Multiple package.json in subdirectories
    package_jsons = list(root.rglob('package.json'))
    if len(package_jsons) > 1:
        return True

    return False
```

**Action:** Apply classification to each workspace independently

---

## Git History Analysis

**Extract file purpose from commit messages:**

```python
import subprocess

def get_file_purpose_from_git(filepath: Path) -> str:
    """Get file purpose from git history"""
    try:
        # Get first commit message for this file
        result = subprocess.run(
            ['git', 'log', '--format=%s', '--follow', '--', str(filepath)],
            capture_output=True,
            text=True,
            cwd=filepath.parent
        )

        if result.returncode == 0 and result.stdout:
            first_commit = result.stdout.strip().split('\n')[-1]

            # Parse common patterns
            if 'add' in first_commit.lower():
                # "Add user authentication module"
                purpose = first_commit.replace('add ', '').replace('Add ', '')
                return purpose.capitalize()

            return first_commit
    except:
        pass

    return "Unknown purpose"
```

---

## LLM Integration (Optional)

**For ambiguous files, use LLM to summarize:**

```python
def get_file_purpose_llm(filepath: Path) -> str:
    """Use LLM to determine file purpose"""
    try:
        with open(filepath, 'r') as f:
            # Read first 50 lines (or 2000 chars)
            content = ''.join(f.readlines()[:50])[:2000]

        prompt = f"""
        Filename: {filepath.name}
        Content preview:
        {content}

        In 1 sentence (max 15 words), what is the purpose of this file?
        """

        # Call LLM (implementation depends on available API)
        response = call_llm(prompt)
        return response.strip()
    except:
        return "Unknown purpose"
```

**Cache results to avoid re-processing:**
```python
# .cleanup-cache.json
{
    "file_purposes": {
        "mysterious_file.py": "Data processing utility for CSV imports",
        "config_old.yaml": "Legacy configuration (archived)"
    }
}
```

---

## See Also

- Main documentation: `../SKILL.md`
- Language patterns: `language-patterns.md`
- Edge cases: `edge-cases.md`
- Consolidation: `consolidation-strategies.md`
