# File Tree Template for README.md

This template should be added to the bottom of the main README.md file to document project structure.

## Basic Template

```markdown
## Project Structure

```
project-root/
├─ README.md              # Project overview and quick start
├─ .gitignore             # Git ignore patterns
├─ {config-file}          # {Config description}
├─ src/                   # Source code
│   ├─ {subdir}/          # {Subdirectory purpose}
│   └─ {file.ext}         # {File purpose}
├─ tests/                 # Test suite
│   ├─ unit/              # Unit tests
│   └─ integration/       # Integration tests
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   └─ {doc.md}           # {Document purpose}
├─ scripts/               # Build and deployment scripts
│   ├─ README.md          # Scripts documentation
│   └─ {script.sh}        # {Script purpose}
└─ tmp/                   # Temporary files (gitignored)
```
```

## Template Placeholders

- `{config-file}` - Configuration file (package.json, Cargo.toml, etc.)
- `{Config description}` - Brief description of config purpose
- `{subdir}/` - Subdirectory name
- `{Subdirectory purpose}` - What the subdirectory contains
- `{file.ext}` - File name
- `{File purpose}` - Single-line description of file purpose
- `{doc.md}` - Documentation file
- `{Document purpose}` - What the document covers
- `{script.sh}` - Script name
- `{Script purpose}` - What the script does

---

## Example: Node.js/React Project

```markdown
## Project Structure

```
my-react-app/
├─ README.md              # Project overview and quick start
├─ .gitignore             # Git ignore patterns
├─ package.json           # Node.js dependencies and scripts
├─ package-lock.json      # Dependency lock file
├─ tsconfig.json          # TypeScript configuration
├─ .eslintrc              # ESLint configuration
├─ .prettierrc            # Prettier configuration
├─ src/                   # Source code
│   ├─ components/        # React components
│   │   ├─ Button/        # Button component
│   │   └─ LoginForm/     # Login form component
│   ├─ hooks/             # Custom React hooks
│   ├─ lib/               # Utility libraries
│   ├─ routes/            # Application routes
│   ├─ styles/            # Global styles
│   ├─ App.tsx            # Main application component
│   └─ index.tsx          # Application entry point
├─ public/                # Static assets
│   ├─ index.html         # HTML template
│   └─ favicon.ico        # Favicon
├─ dist/                  # Build output (gitignored)
├─ tests/                 # Test suite
│   ├─ unit/              # Unit tests
│   ├─ integration/       # Integration tests
│   └─ setup.ts           # Test configuration
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   ├─ architecture.md    # System architecture
│   ├─ api.md             # API reference
│   └─ deployment.md      # Deployment guide
├─ scripts/               # Build and deployment scripts
│   ├─ README.md          # Scripts documentation
│   ├─ build.sh           # Production build script
│   └─ deploy.sh          # Deployment script
└─ tmp/                   # Temporary files (gitignored)
```
```

---

## Example: Python Project

```markdown
## Project Structure

```
my-python-package/
├─ README.md              # Project overview and quick start
├─ .gitignore             # Git ignore patterns
├─ pyproject.toml         # Python package configuration
├─ LICENSE               # MIT License
├─ src/                   # Source code
│   └─ mypackage/         # Main package
│       ├─ __init__.py    # Package initialization
│       ├─ core.py        # Core functionality
│       ├─ utils.py       # Utility functions
│       └─ py.typed       # Type hints marker
├─ tests/                 # Test suite
│   ├─ __init__.py        # Test package initialization
│   ├─ test_core.py       # Core functionality tests
│   ├─ test_utils.py      # Utility function tests
│   └─ conftest.py        # pytest configuration
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   ├─ api-reference.md   # API reference
│   ├─ user-guide.md      # User guide
│   └─ conf.py            # Sphinx configuration
├─ scripts/               # Utility scripts
│   ├─ README.md          # Scripts documentation
│   ├─ build.sh           # Build script
│   └─ publish.sh         # PyPI publish script
└─ tmp/                   # Temporary files (gitignored)
```
```

---

## Example: Rust Project

```markdown
## Project Structure

```
my-rust-app/
├─ README.md              # Project overview and quick start
├─ .gitignore             # Git ignore patterns
├─ Cargo.toml             # Rust package manifest
├─ Cargo.lock             # Dependency lock file
├─ LICENSE                # MIT License
├─ src/                   # Source code
│   ├─ main.rs            # Application entry point
│   ├─ lib.rs             # Library code
│   └─ modules/           # Application modules
│       ├─ auth.rs        # Authentication module
│       └─ db.rs          # Database module
├─ tests/                 # Integration tests
│   └─ integration_test.rs
├─ benches/               # Benchmarks
│   └─ benchmark.rs
├─ examples/              # Example programs
│   └─ example.rs
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   └─ architecture.md    # System architecture
├─ scripts/               # Build and deployment scripts
│   ├─ README.md          # Scripts documentation
│   └─ deploy.sh          # Deployment script
└─ tmp/                   # Temporary files (gitignored)
```
```

---

## Example: Go Project

```markdown
## Project Structure

```
my-go-app/
├─ README.md              # Project overview and quick start
├─ .gitignore             # Git ignore patterns
├─ go.mod                 # Go module definition
├─ go.sum                 # Go dependency checksums
├─ LICENSE                # MIT License
├─ cmd/                   # Main applications
│   └─ server/            # Server application
│       └─ main.go        # Server entry point
├─ pkg/                   # Public libraries
│   ├─ api/               # API client library
│   │   └─ client.go      # API client implementation
│   └─ models/            # Data models
│       └─ user.go        # User model
├─ internal/              # Private application code
│   ├─ handlers/          # HTTP handlers
│   │   └─ auth.go        # Authentication handler
│   └─ middleware/        # HTTP middleware
│       └─ logger.go      # Logging middleware
├─ api/                   # API definitions
│   └─ openapi.yaml       # OpenAPI specification
├─ web/                   # Web assets
│   ├─ static/            # Static files
│   └─ templates/         # HTML templates
├─ test/                  # Additional test files
├─ docs/                  # Documentation
│   ├─ README.md          # Documentation overview
│   └─ api.md             # API documentation
├─ scripts/               # Build and deployment scripts
│   ├─ README.md          # Scripts documentation
│   └─ deploy.sh          # Deployment script
└─ deployments/           # Deployment configurations
    └─ docker/            # Docker files
        └─ Dockerfile     # Docker image definition
```
```

---

## Automation

Generate file tree automatically using Python:

```python
import subprocess
from pathlib import Path

def generate_file_tree(root: Path, max_depth: int = 3, include_descriptions: bool = True) -> str:
    \"\"\"Generate file tree for README.md\"\"\"

    # Use tree command if available
    try:
        result = subprocess.run(
            ['tree', '-L', str(max_depth), '--dirsfirst', '-I',
             'node_modules|dist|build|target|__pycache__|.git'],
            capture_output=True,
            text=True,
            cwd=root
        )
        tree_output = result.stdout
    except FileNotFoundError:
        # Fall back to custom tree generation
        tree_output = generate_tree_custom(root, max_depth)

    if not include_descriptions:
        return tree_output

    # Add descriptions to tree output
    tree_with_descriptions = add_descriptions_to_tree(tree_output, root)

    return f\"\"\"## Project Structure

```
{tree_with_descriptions}
```
\"\"\"

def generate_tree_custom(root: Path, max_depth: int, prefix: str = \"\", depth: int = 0) -> str:
    \"\"\"Generate tree structure without tree command\"\"\"
    if depth >= max_depth:
        return \"\"

    lines = []
    items = sorted(root.iterdir(), key=lambda x: (not x.is_dir(), x.name))

    for i, item in enumerate(items):
        # Skip hidden and excluded
        if item.name.startswith('.') or item.name in {'node_modules', 'dist', 'build'}:
            continue

        is_last = i == len(items) - 1
        connector = \"└─\" if is_last else \"├─\"

        if item.is_dir():
            lines.append(f\"{prefix}{connector} {item.name}/\")
            extension = \"   \" if is_last else \"│  \"
            lines.append(generate_tree_custom(item, max_depth, prefix + extension, depth + 1))
        else:
            lines.append(f\"{prefix}{connector} {item.name}\")

    return \"\\n\".join(lines)

def add_descriptions_to_tree(tree: str, root: Path) -> str:
    \"\"\"Add descriptions to file tree lines\"\"\"
    lines = tree.split('\\n')
    result = []

    for line in lines:
        # Extract filename from tree line
        filename = extract_filename_from_tree_line(line)

        if filename:
            filepath = root / filename
            description = get_file_description(filepath)

            if description:
                # Add description as comment
                padding = \" \" * (40 - len(line))
                result.append(f\"{line}{padding}# {description}\")
                continue

        result.append(line)

    return \"\\n\".join(result)

def get_file_description(filepath: Path) -> str:
    \"\"\"Get description for file from git history or analysis\"\"\"
    # Try git history first
    try:
        result = subprocess.run(
            ['git', 'log', '--format=%s', '--follow', '--', str(filepath)],
            capture_output=True,
            text=True
        )
        if result.stdout:
            first_commit = result.stdout.strip().split('\\n')[-1]
            # Extract description from commit message
            if 'add' in first_commit.lower():
                return first_commit.replace('add ', '').replace('Add ', '').capitalize()
    except:
        pass

    # Fall back to filename patterns
    name = filepath.name.lower()

    DESCRIPTIONS = {
        'readme.md': 'Project overview and quick start',
        '.gitignore': 'Git ignore patterns',
        'package.json': 'Node.js dependencies and scripts',
        'pyproject.toml': 'Python package configuration',
        'cargo.toml': 'Rust package manifest',
        'go.mod': 'Go module definition',
        'tsconfig.json': 'TypeScript configuration',
        '.eslintrc': 'ESLint configuration',
        '.prettierrc': 'Prettier configuration',
        'dockerfile': 'Docker image definition',
        'license': 'MIT License',
        'changelog.md': 'Version history',
    }

    return DESCRIPTIONS.get(name, '')
```

## Customization Guidelines

### 1. Depth

**Recommended:** 2-3 levels deep
- Level 1: Top-level directories
- Level 2: Important subdirectories
- Level 3: Key files in subdirectories

**Too shallow (1 level):**
```
project/
├─ src/
├─ tests/
└─ docs/
```
Not enough information.

**Too deep (4+ levels):**
```
project/
├─ src/
│   ├─ components/
│   │   ├─ Button/
│   │   │   ├─ Button.tsx
│   │   │   ├─ Button.test.tsx
│   │   │   └─ Button.styles.css
```
Too much detail, overwhelming.

### 2. Descriptions

**Good descriptions:**
- "Project overview and quick start" (clear, specific)
- "React components" (concise, informative)
- "API endpoint handlers" (tells what's inside)

**Bad descriptions:**
- "Files" (too vague)
- "Code" (not helpful)
- "Stuff for the app" (unprofessional)

### 3. Exclusions

Always exclude from tree:
- `node_modules/`, `vendor/`, `.venv/`
- `dist/`, `build/`, `target/`, `out/`
- `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`
- `.git/`, `.gitignore` (unless documenting)
- IDE directories (`.vscode/`, `.idea/`)

### 4. Highlighting

Use comments to highlight important files:
```
├─ src/
│   ├─ App.tsx            # Main application component ⭐
│   └─ index.tsx          # Application entry point ⭐
```

### 5. Grouping

Group related directories:
```
# Source code
├─ src/                   # Application source code
├─ lib/                   # Shared libraries

# Testing
├─ tests/                 # Test suite
├─ fixtures/              # Test fixtures

# Documentation
├─ docs/                  # Documentation
└─ examples/              # Code examples
```

---

## Integration with cleanup skill

```python
def update_readme_file_tree(readme_path: Path, root: Path):
    \"\"\"Update file tree section in README.md\"\"\"
    with open(readme_path, 'r') as f:
        content = f.read()

    # Generate new tree
    new_tree = generate_file_tree(root, max_depth=3, include_descriptions=True)

    # Find existing tree section
    tree_start = content.find('## Project Structure')

    if tree_start == -1:
        # No tree section - add at end
        content += \"\\n\\n\" + new_tree
    else:
        # Find end of tree section (next ## heading or end of file)
        tree_end = content.find('##', tree_start + 1)
        if tree_end == -1:
            tree_end = len(content)

        # Replace tree section
        content = content[:tree_start] + new_tree + content[tree_end:]

    # Write updated content
    with open(readme_path, 'w') as f:
        f.write(content)
```

---

## See Also

- Main skill documentation: `../SKILL.md`
- Folder README template: `folder-readme-template.md`
- Scripts README template: `scripts-readme-template.md`
