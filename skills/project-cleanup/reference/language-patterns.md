# Language-Specific Project Patterns

Comprehensive guide to project structures across different programming languages and ecosystems.

## Overview

Different programming languages have established conventions for project organization. The project-cleanup skill must respect these conventions and never violate ecosystem expectations.

**Key Principle:** Detect project language first, then apply language-specific rules.

---

## Language Detection

```python
from pathlib import Path
from typing import Optional

def detect_project_language(root: Path) -> Optional[str]:
    """Detect primary project language"""
    # Python
    if (root / 'pyproject.toml').exists():
        return 'python'
    if (root / 'setup.py').exists():
        return 'python'
    if (root / 'requirements.txt').exists():
        return 'python'

    # Node.js/JavaScript/TypeScript
    if (root / 'package.json').exists():
        return 'node'

    # Rust
    if (root / 'Cargo.toml').exists():
        return 'rust'

    # Go
    if (root / 'go.mod').exists():
        return 'go'

    # Ruby
    if (root / 'Gemfile').exists():
        return 'ruby'

    # Java
    if (root / 'pom.xml').exists():
        return 'java_maven'
    if (root / 'build.gradle').exists():
        return 'java_gradle'

    # PHP
    if (root / 'composer.json').exists():
        return 'php'

    # C/C++
    if (root / 'CMakeLists.txt').exists():
        return 'cpp_cmake'
    if (root / 'Makefile').exists():
        return 'c_make'

    return None
```

---

## Python Projects

### Modern Python (2024)

**Standard Structure:**
```
project/
├─ README.md
├─ pyproject.toml          # Modern packaging (PEP 518)
├─ LICENSE
├─ .gitignore
├─ src/
│   └─ package_name/
│       ├─ __init__.py
│       ├─ module.py
│       └─ py.typed        # Type hints marker
├─ tests/
│   ├─ __init__.py
│   ├─ test_module.py
│   └─ conftest.py         # pytest config
├─ docs/
│   ├─ conf.py            # Sphinx config
│   └─ index.rst
├─ scripts/
└─ tmp/
```

**Root-Level Files (Allowed):**
- `pyproject.toml` - Modern standard (PEP 518, 517, 621)
- `setup.py` - Legacy packaging (still common)
- `setup.cfg` - Legacy configuration
- `requirements.txt` - Dependencies
- `requirements-dev.txt` - Development dependencies
- `Pipfile`, `Pipfile.lock` - Pipenv
- `poetry.lock` - Poetry
- `MANIFEST.in` - Package manifest
- `tox.ini` - tox configuration
- `.python-version` - pyenv version
- `pytest.ini` - pytest configuration
- `.coveragerc` - Coverage configuration
- `mypy.ini` - Type checker configuration

**Build Outputs (Gitignore):**
- `dist/` - Built distributions
- `build/` - Build artifacts
- `*.egg-info/` - Egg metadata
- `__pycache__/` - Bytecode cache
- `.pytest_cache/` - pytest cache
- `.mypy_cache/` - mypy cache
- `.tox/` - tox environments
- `.venv/`, `venv/`, `env/` - Virtual environments

**Two Layouts:**

**1. src/ Layout (Recommended 2024):**
```
project/
└─ src/
    └─ mypackage/
        ├─ __init__.py
        └─ module.py
```
- Prevents accidentally importing from project root
- Forces proper installation

**2. Flat Layout (Legacy but common):**
```
project/
└─ mypackage/
    ├─ __init__.py
    └─ module.py
```
- Simpler for small projects
- Still widely used

**Never Suggest:** `cmd/`, `pkg/` (Go conventions)

---

## Node.js / JavaScript / TypeScript

### Modern Node.js (2024)

**Standard Structure:**
```
project/
├─ README.md
├─ package.json
├─ package-lock.json
├─ tsconfig.json           # TypeScript
├─ .gitignore
├─ src/
│   ├─ index.ts
│   ├─ lib/
│   ├─ components/         # React/Vue
│   └─ routes/             # Express/Fastify
├─ dist/                   # Build output (gitignored)
├─ tests/
│   ├─ unit/
│   └─ integration/
├─ docs/
└─ scripts/
```

**Root-Level Files (Allowed):**
- `package.json` - Dependencies and scripts
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` - Lock files
- `tsconfig.json`, `jsconfig.json` - TypeScript/JavaScript config
- `.eslintrc`, `.eslintrc.js`, `.eslintrc.json` - ESLint
- `.prettierrc`, `.prettierrc.js` - Prettier
- `.babelrc`, `babel.config.js` - Babel
- `webpack.config.js` - Webpack
- `vite.config.js`, `vite.config.ts` - Vite
- `jest.config.js`, `vitest.config.js` - Test frameworks
- `.nvmrc` - Node version
- `.npmrc` - npm configuration
- `playwright.config.js` - Playwright tests

**Build Outputs (Gitignore):**
- `node_modules/` - Dependencies
- `dist/`, `build/`, `out/` - Build outputs
- `.next/` - Next.js
- `.nuxt/` - Nuxt.js
- `.cache/` - Cache directories

**Framework-Specific:**

**React:**
```
src/
├─ components/
│   └─ Button/
│       ├─ Button.tsx
│       ├─ Button.test.tsx
│       ├─ Button.module.css
│       └─ README.md          # Component docs
├─ hooks/
├─ utils/
└─ App.tsx
```

**Next.js:**
```
app/                          # App Router (Next.js 13+)
├─ page.tsx
├─ layout.tsx
└─ api/
    └─ route.ts

pages/                        # Pages Router (legacy)
├─ index.tsx
└─ api/
    └─ hello.ts

public/                       # Static assets
└─ images/
```

**Vue:**
```
src/
├─ components/
├─ views/
├─ router/
├─ store/
└─ App.vue
```

**Never Suggest:** `src/` for Next.js pages (uses `pages/` or `app/`)

---

## Rust Projects

### Cargo Standard (2024)

**Standard Structure:**
```
project/
├─ README.md
├─ Cargo.toml
├─ Cargo.lock
├─ LICENSE
├─ .gitignore
├─ src/
│   ├─ main.rs             # Binary crate
│   ├─ lib.rs              # Library crate
│   └─ bin/                # Additional binaries
│       └─ another.rs
├─ tests/                  # Integration tests
│   └─ integration_test.rs
├─ benches/                # Benchmarks
│   └─ benchmark.rs
├─ examples/               # Example programs
│   └─ example.rs
├─ docs/                   # Additional docs
└─ scripts/
```

**Root-Level Files (Allowed):**
- `Cargo.toml` - Package manifest
- `Cargo.lock` - Dependency lock
- `.rustfmt.toml`, `rustfmt.toml` - Formatter config
- `clippy.toml` - Clippy config
- `rust-toolchain`, `rust-toolchain.toml` - Toolchain version

**Build Outputs (Gitignore):**
- `target/` - Build directory (ALWAYS gitignore)
- `Cargo.lock` (for libraries, optional)

**Cargo Conventions:**
- `src/main.rs` - Binary crate entry point
- `src/lib.rs` - Library crate entry point
- `src/bin/` - Additional binary targets
- `tests/` - Integration tests (unit tests in src/)
- `benches/` - Benchmarks
- `examples/` - Example code

**Never Suggest:**
- Moving `src/main.rs` or `src/lib.rs` (required by Cargo)
- `cmd/`, `pkg/` (Go conventions)
- `lib/` instead of `src/` (Cargo requires src/)

---

## Go Projects

### Go Standard (2024)

**Standard Structure (Standard Go Project Layout):**
```
project/
├─ README.md
├─ go.mod
├─ go.sum
├─ LICENSE
├─ .gitignore
├─ cmd/
│   └─ appname/
│       └─ main.go         # Application entrypoint
├─ pkg/
│   └─ publiclib/
│       └─ api.go          # Public libraries
├─ internal/
│   └─ privatelib/
│       └─ logic.go        # Private packages
├─ api/
│   ├─ openapi.yaml
│   └─ proto/
│       └─ service.proto
├─ web/
│   ├─ static/
│   └─ templates/
├─ scripts/
├─ deployments/
│   └─ docker/
├─ test/                   # Additional test files
└─ docs/
```

**Root-Level Files (Allowed):**
- `go.mod` - Module definition
- `go.sum` - Dependency checksums
- `.golangci.yml` - Linter configuration
- `Makefile` - Common for build automation

**Build Outputs (Gitignore):**
- `bin/` - Compiled binaries (if local)
- `vendor/` - Vendored dependencies (optional)

**Go Conventions:**

**cmd/** - Main applications
- Each subdirectory is a separate binary
- `cmd/server/main.go`, `cmd/cli/main.go`
- Keep code minimal (import from internal/, pkg/)

**pkg/** - Public libraries
- Code other projects can import
- Stable public APIs

**internal/** - Private code
- Cannot be imported by external projects
- Go compiler enforces this

**Never Suggest:**
- `src/` (not Go convention)
- `lib/` (use pkg/ or internal/)
- Flat layout with many .go files in root

**Small Project Exception:**
```
simple-project/
├─ main.go                 # OK for very small projects
├─ utils.go
└─ go.mod
```
For projects that grow, migrate to cmd/pkg/internal

---

## Ruby Projects

### Ruby/Rails Standard (2024)

**Gem Structure:**
```
gem_name/
├─ README.md
├─ Gemfile
├─ Gemfile.lock
├─ gem_name.gemspec
├─ LICENSE
├─ .gitignore
├─ lib/
│   ├─ gem_name.rb         # Main file
│   ├─ gem_name/
│   │   ├─ version.rb
│   │   └─ feature.rb
│   └─ tasks/
├─ spec/                   # RSpec tests
│   ├─ spec_helper.rb
│   └─ gem_name_spec.rb
├─ test/                   # Minitest (alternative)
│   └─ test_helper.rb
└─ docs/
```

**Rails Structure:**
```
rails_app/
├─ README.md
├─ Gemfile
├─ Gemfile.lock
├─ Rakefile
├─ config.ru
├─ app/
│   ├─ models/
│   ├─ views/
│   ├─ controllers/
│   └─ helpers/
├─ config/
│   └─ database.yml
├─ db/
│   ├─ migrate/
│   └─ schema.rb
├─ public/
│   └─ assets/
├─ spec/                   # RSpec (common)
└─ test/                   # Rails default
```

**Root-Level Files (Allowed):**
- `Gemfile`, `Gemfile.lock` - Dependencies
- `*.gemspec` - Gem specification
- `Rakefile` - Rake tasks
- `config.ru` - Rack configuration
- `.ruby-version` - Ruby version
- `.rspec` - RSpec configuration

**Never Suggest:**
- Moving Rails structure (app/, config/, db/)
- `src/` (use lib/ in Ruby)

---

## Java Projects

### Maven Structure

```
project/
├─ README.md
├─ pom.xml
├─ LICENSE
├─ .gitignore
├─ src/
│   ├─ main/
│   │   ├─ java/
│   │   │   └─ com/company/project/
│   │   │       └─ Main.java
│   │   └─ resources/
│   │       └─ application.properties
│   └─ test/
│       ├─ java/
│       │   └─ com/company/project/
│       │       └─ MainTest.java
│       └─ resources/
├─ target/                 # Build output (gitignore)
└─ docs/
```

### Gradle Structure

```
project/
├─ README.md
├─ build.gradle
├─ settings.gradle
├─ gradlew
├─ gradlew.bat
├─ LICENSE
├─ .gitignore
├─ src/
│   ├─ main/
│   │   └─ java/
│   │       └─ com/company/project/
│   └─ test/
│       └─ java/
│           └─ com/company/project/
├─ build/                  # Build output (gitignore)
└─ docs/
```

**Root-Level Files (Allowed):**
- `pom.xml` - Maven
- `build.gradle`, `settings.gradle` - Gradle
- `gradlew`, `gradlew.bat` - Gradle wrapper
- `.mvn/` - Maven wrapper

**Build Outputs (Gitignore):**
- `target/` - Maven
- `build/` - Gradle
- `out/` - IntelliJ
- `.gradle/` - Gradle cache

---

## PHP Projects

### Composer Structure

```
project/
├─ README.md
├─ composer.json
├─ composer.lock
├─ LICENSE
├─ .gitignore
├─ src/
│   └─ ClassName.php
├─ tests/
│   └─ ClassNameTest.php
├─ vendor/                 # Dependencies (gitignore)
├─ public/
│   └─ index.php
└─ docs/
```

**Laravel Structure:**
```
laravel_app/
├─ composer.json
├─ artisan
├─ app/
│   ├─ Http/
│   ├─ Models/
│   └─ Providers/
├─ config/
├─ database/
├─ public/
├─ resources/
│   ├─ views/
│   └─ js/
├─ routes/
├─ storage/
└─ tests/
```

**Root-Level Files (Allowed):**
- `composer.json`, `composer.lock`
- `.php-cs-fixer.php` - PHP CS Fixer
- `phpunit.xml` - PHPUnit
- `artisan` - Laravel CLI

**Build Outputs (Gitignore):**
- `vendor/` - Composer dependencies
- `storage/framework/` - Laravel caches

---

## Monorepos

### Detection

```python
def is_monorepo(root: Path) -> bool:
    """Detect if project is a monorepo"""
    # Lerna (Node.js)
    if (root / 'lerna.json').exists():
        return True

    # Nx (Node.js)
    if (root / 'nx.json').exists():
        return True

    # pnpm workspaces
    if (root / 'pnpm-workspace.yaml').exists():
        return True

    # npm/yarn workspaces
    package_json = root / 'package.json'
    if package_json.exists():
        import json
        with open(package_json) as f:
            data = json.load(f)
            if 'workspaces' in data:
                return True

    # Cargo workspaces
    cargo_toml = root / 'Cargo.toml'
    if cargo_toml.exists():
        with open(cargo_toml) as f:
            if '[workspace]' in f.read():
                return True

    # Go workspaces (Go 1.18+)
    if (root / 'go.work').exists():
        return True

    # Bazel
    if (root / 'WORKSPACE').exists() or (root / 'WORKSPACE.bazel').exists():
        return True

    # Multiple package.json files
    package_jsons = list(root.glob('*/package.json'))
    if len(package_jsons) > 1:
        return True

    return False
```

### Monorepo Structures

**Lerna/Nx (Node.js):**
```
monorepo/
├─ package.json
├─ lerna.json or nx.json
├─ packages/
│   ├─ package-a/
│   │   ├─ package.json
│   │   ├─ src/
│   │   ├─ tests/
│   │   └─ docs/
│   └─ package-b/
│       ├─ package.json
│       ├─ src/
│       ├─ tests/
│       └─ docs/
├─ docs/                   # Shared docs
└─ scripts/                # Shared scripts
```

**Cargo Workspace (Rust):**
```
workspace/
├─ Cargo.toml              # [workspace]
├─ crates/
│   ├─ crate-a/
│   │   ├─ Cargo.toml
│   │   └─ src/
│   └─ crate-b/
│       ├─ Cargo.toml
│       └─ src/
└─ docs/
```

**Monorepo Strategy:**
- Apply cleanup to each workspace independently
- Don't move files between workspaces
- Each workspace has own docs/, scripts/, tmp/
- Shared docs in root docs/

---

## Summary Table

| Language | Source Dir | Test Dir | Build Output | Root Config Files |
|----------|-----------|----------|--------------|-------------------|
| Python | `src/` or flat | `tests/` | `dist/`, `build/`, `__pycache__/` | pyproject.toml, setup.py |
| Node.js | `src/` | `tests/`, `__tests__/` | `dist/`, `build/`, `node_modules/` | package.json, tsconfig.json |
| Rust | `src/` | `tests/` | `target/` | Cargo.toml |
| Go | `cmd/`, `pkg/`, `internal/` | `*_test.go`, `test/` | `bin/`, `vendor/` | go.mod |
| Ruby | `lib/` | `spec/`, `test/` | - | Gemfile, *.gemspec |
| Java | `src/main/java/` | `src/test/java/` | `target/`, `build/` | pom.xml, build.gradle |
| PHP | `src/` | `tests/` | `vendor/` | composer.json |

---

## Language-Specific Rules Implementation

```python
def get_language_rules(language: str) -> dict:
    """Get language-specific organization rules"""
    rules = {
        'python': {
            'source_dirs': ['src/', 'lib/'],
            'test_dirs': ['tests/', 'test/'],
            'build_dirs': ['dist/', 'build/', '__pycache__/', '.pytest_cache/'],
            'doc_dirs': ['docs/'],
            'never_move': ['setup.py', 'pyproject.toml', 'requirements.txt'],
        },
        'node': {
            'source_dirs': ['src/', 'lib/'],
            'test_dirs': ['tests/', 'test/', '__tests__/'],
            'build_dirs': ['dist/', 'build/', 'node_modules/', '.next/', '.nuxt/'],
            'doc_dirs': ['docs/'],
            'never_move': ['package.json', 'tsconfig.json', '.eslintrc'],
        },
        'rust': {
            'source_dirs': ['src/'],
            'test_dirs': ['tests/'],
            'build_dirs': ['target/'],
            'doc_dirs': ['docs/'],
            'never_move': ['Cargo.toml', 'Cargo.lock'],
        },
        'go': {
            'source_dirs': ['cmd/', 'pkg/', 'internal/'],
            'test_dirs': ['test/'],
            'build_dirs': ['bin/', 'vendor/'],
            'doc_dirs': ['docs/'],
            'never_move': ['go.mod', 'go.sum'],
        },
    }

    return rules.get(language, {})
```

---

## See Also

- Main documentation: `../SKILL.md`
- File classification: `file-classification.md`
- Edge cases: `edge-cases.md`
- Consolidation: `consolidation-strategies.md`
