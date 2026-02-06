# Edge Cases Reference

Comprehensive guide to handling unusual situations and edge cases in project cleanup.

## Root-Level Edge Cases

### LICENSE Variants

**Scenario:** Multiple LICENSE file variations

**Files:**
- `LICENSE` (plain text)
- `LICENSE.txt` (text extension)
- `LICENSE.md` (markdown format)
- `LICENSE-MIT` (specific license type)
- `LICENSE-APACHE` (dual licensing)

**Rule:** ALL stay in root (GitHub expects LICENSE in root for repository licensing)

**Never move:** Any file starting with `LICENSE`

**Exception:** `docs/licenses/third-party-licenses.md` (third-party attribution) can be in docs/

```python
def should_keep_license_in_root(filename: str) -> bool:
    """Check if LICENSE file should stay in root"""
    return filename.upper().startswith('LICENSE')
```

---

### CONTRIBUTING.md Location

**Scenario:** CONTRIBUTING.md can be in two places per GitHub convention

**Valid locations:**
1. Root: `CONTRIBUTING.md`
2. Hidden: `.github/CONTRIBUTING.md`

**Edge case:** Both exist

**Resolution:**
```python
def handle_contributing_files(root: Path) -> dict:
    """Handle CONTRIBUTING.md placement"""
    root_contrib = root / 'CONTRIBUTING.md'
    github_contrib = root / '.github' / 'CONTRIBUTING.md'

    if root_contrib.exists() and github_contrib.exists():
        # Both exist - ask user which to keep
        return {
            'action': 'ask_user',
            'message': 'Found CONTRIBUTING.md in both root and .github/. Which to keep?',
            'options': [
                {' label': 'Keep root (more visible)', 'action': 'delete_.github'},
                {'label': 'Keep .github (GitHub convention)', 'action': 'delete_root'},
                {'label': 'Keep both (if different content)', 'action': 'keep_both'}
            ]
        }

    # Only one exists - keep it where it is
    return {'action': 'keep', 'reason': 'Standard location'}
```

---

### .env vs .env.example

**Scenario:** Environment files

**Rules:**
- `.env` - NEVER commit (secrets), should be in .gitignore
- `.env.example`, `.env.template` - Stay in root (documentation)
- `.env.local`, `.env.production` - Usually gitignored

**Edge case:** `.env` is committed (user mistake)

**Resolution:**
```python
def handle_env_files(root: Path) -> dict:
    """Handle .env files"""
    env_file = root / '.env'

    if env_file.exists():
        # Check if in git
        result = subprocess.run(
            ['git', 'ls-files', '--error-unmatch', '.env'],
            capture_output=True,
            cwd=root
        )

        if result.returncode == 0:
            # .env is tracked in git (BAD!)
            return {
                'action': 'warning',
                'message': '.env is committed to git (contains secrets!)',
                'recommended_actions': [
                    'Move sensitive values out',
                    'Add .env to .gitignore',
                    'Create .env.example with placeholders',
                    'Remove from git history (git filter-branch)'
                ]
            }

    return {'action': 'keep', 'reason': 'Not tracked or is example file'}
```

---

### README variations

**Scenario:** Multiple README files

**Files:**
- `README.md` - Main project README (ALWAYS root)
- `README-DEV.md` - Developer-specific
- `README-API.md` - API documentation
- `README-DEPLOYMENT.md` - Deployment guide

**Resolution:**
```python
def handle_readme_files(root: Path) -> List[dict]:
    """Handle multiple README files"""
    actions = []

    # Find all README variants
    readme_files = list(root.glob('README-*.md'))

    for readme in readme_files:
        # Extract topic
        topic = readme.stem.replace('README-', '').lower()

        actions.append({
            'file': str(readme),
            'action': 'move_to_docs',
            'destination': f'docs/{topic}.md',
            'reason': 'Topic-specific documentation'
        })

    return actions

# README.md always stays in root
# README-DEV.md → docs/development.md
# README-API.md → docs/api.md
# README-DEPLOYMENT.md → docs/deployment.md
```

---

## Test Fixtures and Data

### Test Fixtures in Root

**Scenario:** Test data files in project root

**Files:**
- `test_data.json` - Test fixtures
- `sample_input.csv` - Test input
- `expected_output.xml` - Expected results

**Resolution:** Move to `tests/fixtures/`

```python
def is_test_fixture(filepath: Path, root: Path) -> bool:
    """Check if file is a test fixture"""
    name = filepath.name.lower()

    # Test prefixes/suffixes
    if any(x in name for x in ['test', 'fixture', 'mock', 'sample', 'expected']):
        # Check if in root (not already in tests/)
        if filepath.parent == root:
            return True

    return False

# Action: Move test_data.json → tests/fixtures/test_data.json
```

### Test Snapshots

**Scenario:** Test snapshot directories

**Files:**
- `__snapshots__/` (Jest)
- `.snapshots/` (pytest-textual-snapshot)
- `snapshots/` (various)

**Rule:** Keep in place if in tests/, move if in root

```python
def handle_snapshots(snapshot_dir: Path, root: Path) -> dict:
    """Handle snapshot directories"""
    # If in tests/ already, keep
    if 'test' in str(snapshot_dir.relative_to(root)).lower():
        return {'action': 'keep', 'reason': 'Part of test suite'}

    # If in root, move to tests/
    if snapshot_dir.parent == root:
        return {
            'action': 'move',
            'destination': root / 'tests' / snapshot_dir.name,
            'reason': 'Test-related directory'
        }

    return {'action': 'keep'}
```

---

## Build Outputs and Generated Files

### Identifying Generated Files

**Scenario:** Files that are auto-generated

**Markers:**
- `// AUTO-GENERATED` comment
- `# Generated by <tool>` comment
- Tool-specific patterns (Prisma, Protobuf, GraphQL)

```python
import re

def is_generated_file(filepath: Path) -> tuple[bool, str]:
    """Check if file is auto-generated"""
    try:
        with open(filepath, 'r') as f:
            first_lines = ''.join(f.readlines()[:10])

        # Check for generation markers
        markers = [
            r'AUTO[- ]GENERATED',
            r'DO NOT EDIT',
            r'Generated by',
            r'@generated',
            r'Code generated .* DO NOT EDIT',
        ]

        for marker in markers:
            if re.search(marker, first_lines, re.IGNORECASE):
                return True, f"Marker: {marker}"

        # Check file-specific patterns
        name = filepath.name

        # Prisma
        if '.prisma.ts' in name or 'prisma/client' in str(filepath):
            return True, "Prisma generated client"

        # Protobuf
        if name.endswith('.pb.go') or name.endswith('_pb2.py'):
            return True, "Protocol buffer generated"

        # GraphQL
        if 'generated' in name and '.graphql' in name:
            return True, "GraphQL codegen"

        return False, ""

    except:
        return False, ""
```

**Resolution:**
- If in root → Check if should be in `src/generated/` or similar
- If truly temporary → Move to `tmp/`
- If committed and part of source → Leave in place

---

### Build Outputs in Root

**Scenario:** Compiled files or artifacts in root

**Files:**
- `bundle.js`, `app.min.js` - Webpack/Rollup outputs
- `*.wasm` - WebAssembly binaries
- `*.so`, `*.dylib`, `*.dll` - Shared libraries
- `*.o`, `*.a` - Object files

**Resolution:**
```python
def handle_build_outputs(filepath: Path, root: Path) -> dict:
    """Handle build output files"""
    # Check if should be gitignored
    result = subprocess.run(
        ['git', 'check-ignore', str(filepath)],
        capture_output=True,
        cwd=root
    )

    if result.returncode == 0:
        # Already gitignored - OK to leave or clean
        return {
            'action': 'suggest_delete',
            'reason': 'Build output (should be regenerated)',
            'alternative': 'Add to .gitignore if not already'
        }

    # Not gitignored - should be moved
    return {
        'action': 'move_to_dist',
        'destination': root / 'dist' / filepath.name,
        'add_to_gitignore': True,
        'reason': 'Build output should be in dist/ and gitignored'
    }
```

---

## Hidden Directories

### IDE Directories

**Scenario:** IDE configuration directories

**Directories:**
- `.vscode/` - VS Code settings
- `.idea/` - IntelliJ/WebStorm
- `.vs/` - Visual Studio

**Resolution:**
```python
def handle_ide_directories(ide_dir: Path, root: Path) -> dict:
    """Handle IDE configuration directories"""
    # Check if tracked in git
    result = subprocess.run(
        ['git', 'ls-files', str(ide_dir)],
        capture_output=True,
        cwd=root
    )

    if result.stdout:
        # Some files are tracked (team shares IDE config)
        return {
            'action': 'keep',
            'reason': 'Team-shared IDE configuration'
        }
    else:
        # Not tracked - should be gitignored
        return {
            'action': 'add_to_gitignore',
            'reason': 'Personal IDE settings should not be committed',
            'note': 'Each developer has their own IDE preferences'
        }
```

### Cache Directories

**Scenario:** Hidden cache directories

**Directories:**
- `.cache/` - General cache
- `.pytest_cache/` - pytest
- `.mypy_cache/` - mypy
- `.eslintcache` - ESLint
- `.parcel-cache/` - Parcel

**Resolution:** Always add to .gitignore, optionally move to `tmp/`

```python
def handle_cache_directories(cache_dir: Path) -> dict:
    """Handle cache directories"""
    return {
        'action': 'add_to_gitignore',
        'optional_action': 'move_to_tmp',
        'reason': 'Cache directories should not be committed',
        'note': 'Will be regenerated on next run'
    }
```

---

## Monorepo Edge Cases

### Workspace Boundaries

**Scenario:** Files that could belong to workspace or root

**Example:**
```
monorepo/
├─ package.json           # Root package.json
├─ tsconfig.json          # Shared tsconfig
├─ docs/                  # Shared docs
├─ packages/
│   ├─ package-a/
│   │   ├─ package.json
│   │   ├─ tsconfig.json  # Extends root
│   │   └─ docs/          # Package-specific
│   └─ package-b/
│       └─ ...
```

**Resolution:**
```python
def determine_file_scope(filepath: Path, workspace_root: Path, project_root: Path) -> str:
    """Determine if file is workspace-scoped or root-scoped"""
    rel_to_workspace = filepath.relative_to(workspace_root)
    rel_to_root = filepath.relative_to(project_root)

    # If in workspace subdir, belongs to workspace
    if len(rel_to_workspace.parts) > len(rel_to_root.parts):
        return 'workspace'
    else:
        return 'root'

# Example:
# monorepo/docs/api.md → root (shared)
# monorepo/packages/pkg-a/docs/api.md → workspace (package-specific)
```

**Rule:** Never move files between workspaces - only within workspace boundaries

---

### Shared vs Package-Specific

**Scenario:** Deciding if file is shared or package-specific

**Decision tree:**
```
Is file in packages/<name>/?
    YES → Package-specific (don't move to root)
    NO → Check content:
        References multiple packages? → Shared (root docs/)
        References only one package? → Move to that package's docs/
```

---

## Special File Types

### Configuration with Secrets

**Scenario:** Config files that might contain secrets

**Files:**
- `config.json`, `config.yaml`
- `settings.local.json`
- `credentials.json`

**Resolution:**
```python
def check_for_secrets(config_file: Path) -> dict:
    """Check config file for potential secrets"""
    try:
        with open(config_file, 'r') as f:
            content = f.read()

        # Check for secret-like patterns
        secret_patterns = [
            r'api[_-]?key',
            r'password',
            r'secret',
            r'token',
            r'credential',
        ]

        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return {
                    'warning': True,
                    'message': f'Config file may contain secrets (found: {pattern})',
                    'recommended_action': 'Check if should be gitignored or use .env'
                }

        return {'warning': False}

    except:
        return {'warning': False}
```

---

### Example vs Real Config

**Scenario:** Distinguishing example configs from real ones

**Files:**
- `config.json` (real, may have secrets)
- `config.example.json` (template, safe)
- `config.sample.json` (template, safe)

**Resolution:**
```python
def is_example_file(filename: str) -> bool:
    """Check if file is an example/template"""
    example_markers = [
        '.example',
        '.sample',
        '.template',
        '-example',
        '-sample',
        '_example',
        '_sample',
    ]

    name_lower = filename.lower()

    for marker in example_markers:
        if marker in name_lower:
            return True

    return False

# config.example.json → Keep in root (template)
# config.json → Check for secrets, may need to gitignore
```

---

## Language-Specific Edge Cases

### Python: setup.py vs setup.py script

**Scenario:** `setup.py` can be packaging config OR executable script

**Detection:**
```python
def is_packaging_setup_py(filepath: Path) -> bool:
    """Check if setup.py is packaging config (not a script)"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        # Packaging setup.py has setuptools
        if 'from setuptools import' in content:
            return True
        if 'from distutils' in content:
            return True

        return False
    except:
        return False

# If packaging → Keep in root (config)
# If script → Move to scripts/ (executable)
```

### Node.js: index.js location

**Scenario:** `index.js` can be package entry point OR example

**Detection:**
```python
def is_package_entry_point(index_js: Path, root: Path) -> bool:
    """Check if index.js is package entry point"""
    package_json = root / 'package.json'

    if package_json.exists():
        import json
        with open(package_json) as f:
            pkg = json.load(f)

        # Check main field
        if pkg.get('main') == 'index.js':
            return True

        # Check exports
        exports = pkg.get('exports', {})
        if '.' in exports and exports['.'] == './index.js':
            return True

    return False

# If entry point → Keep in root (or src/)
# If not referenced → May be example, check content
```

### Rust: Cargo.lock presence

**Scenario:** Cargo.lock should be committed for binaries, not libraries

**Resolution:**
```python
def should_commit_cargo_lock(root: Path) -> bool:
    """Check if Cargo.lock should be committed"""
    cargo_toml = root / 'Cargo.toml'

    if cargo_toml.exists():
        with open(cargo_toml, 'r') as f:
            content = f.read()

        # Binary crate if has [[bin]]
        if '[[bin]]' in content:
            return True

        # Library crate if has [lib]
        if '[lib]' in content:
            return False  # Libraries don't commit Cargo.lock

    return True  # Default: commit

# Binary crate → Commit Cargo.lock
# Library crate → .gitignore Cargo.lock
```

---

## Filesystem Edge Cases

### Symbolic Links

**Scenario:** Symbolic links in project

**Resolution:**
```python
def handle_symlink(link: Path) -> dict:
    """Handle symbolic link"""
    try:
        target = link.readlink()

        # Check if target is within project
        if target.is_absolute():
            return {
                'action': 'warn',
                'message': 'Symbolic link points outside project',
                'note': 'May break when moved'
            }

        # Relative link within project - preserve
        return {
            'action': 'preserve',
            'note': 'Will update link target if moved'
        }

    except:
        return {'action': 'skip', 'reason': 'Cannot read symlink'}
```

### Case-Insensitive Filesystems

**Scenario:** `README.md` and `readme.md` on macOS (case-insensitive) vs Linux (case-sensitive)

**Resolution:**
```python
import platform

def detect_case_sensitivity() -> bool:
    """Detect if filesystem is case-sensitive"""
    return platform.system() != 'Darwin'  # macOS is case-insensitive

def find_case_conflicts(root: Path) -> List[dict]:
    """Find files that would conflict on case-insensitive FS"""
    files_by_lower = {}
    conflicts = []

    for file in root.rglob('*'):
        if file.is_file():
            lower_name = file.name.lower()

            if lower_name in files_by_lower:
                conflicts.append({
                    'file1': str(files_by_lower[lower_name]),
                    'file2': str(file),
                    'issue': 'Case-only difference would conflict on macOS/Windows'
                })
            else:
                files_by_lower[lower_name] = file

    return conflicts

# Example conflict:
# README.md and readme.md exist in same directory
# → On macOS, only one visible
# → On Linux, both visible
# → Suggest: rename one to IMPLEMENTATION.md or similar
```

---

## Git-Related Edge Cases

### Files Removed from Git but Still in Working Directory

**Scenario:** `git rm --cached` removed file from repo but not filesystem

**Detection:**
```python
def is_untracked_but_exists(filepath: Path, root: Path) -> bool:
    """Check if file exists but is untracked"""
    # Check git status
    result = subprocess.run(
        ['git', 'ls-files', '--', str(filepath.relative_to(root))],
        capture_output=True,
        cwd=root
    )

    is_tracked = bool(result.stdout)

    return filepath.exists() and not is_tracked
```

**Resolution:** Treat as new file (apply classification rules)

---

### Large Files (LFS)

**Scenario:** Files tracked with Git LFS

**Detection:**
```python
def is_lfs_file(filepath: Path, root: Path) -> bool:
    """Check if file is tracked with Git LFS"""
    result = subprocess.run(
        ['git', 'check-attr', 'filter', str(filepath.relative_to(root))],
        capture_output=True,
        text=True,
        cwd=root
    )

    return 'lfs' in result.stdout.lower()
```

**Resolution:** Leave LFS files in place (moving doesn't affect LFS, but preserve structure)

---

## Permission Edge Cases

### Executable Files Without Extension

**Scenario:** File is executable but no extension

**Example:** `deploy` (no .sh extension)

**Detection:**
```python
def detect_script_without_extension(filepath: Path) -> bool:
    """Detect executable script without extension"""
    # Check executable bit
    if not os.access(filepath, os.X_OK):
        return False

    # Check shebang
    try:
        with open(filepath, 'rb') as f:
            first_bytes = f.read(2)
            if first_bytes == b'#!':
                return True
    except:
        pass

    return False

# deploy (executable, has shebang) → scripts/deploy
```

---

## Summary: Edge Case Decision Matrix

| Scenario | Detection | Action |
|----------|-----------|--------|
| Multiple LICENSE files | Starts with LICENSE | Keep all in root |
| .env committed | git ls-files .env | Warn, suggest gitignore |
| README-*.md | README- prefix | Move to docs/ |
| Test fixtures in root | test/fixture/sample in name | Move to tests/fixtures/ |
| Generated files | AUTO-GENERATED marker | Check if should be in src/generated/ |
| Build outputs | *.min.js, *.bundle.js | Move to dist/, gitignore |
| IDE directories | .vscode/, .idea/ | Check if tracked, else gitignore |
| Monorepo files | In packages/? | Keep within workspace boundaries |
| Config with secrets | API key patterns | Warn, suggest .env |
| Example configs | .example, .sample | Keep in root (documentation) |
| Symlinks | Is link? | Preserve, update target |
| Executable without ext | Has shebang? | Move to scripts/ |
| LFS files | git check-attr | Leave in place |

---

## See Also

- Main documentation: `../SKILL.md`
- File classification: `file-classification.md`
- Language patterns: `language-patterns.md`
- Consolidation: `consolidation-strategies.md`
