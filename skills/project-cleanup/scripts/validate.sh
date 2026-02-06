#!/usr/bin/env bash
#
# Pre-commit hook for project organization validation
# Warns if files are added to root that shouldn't be there
#
# Usage:
#   .claude/skills/project-cleanup/scripts/validate.sh
#
# Or via pre-commit:
#   Add to .pre-commit-config.yaml:
#   repos:
#     - repo: local
#       hooks:
#         - id: project-organization-check
#           name: Check project organization
#           entry: .claude/skills/project-cleanup/scripts/validate.sh
#           language: script
#           always_run: true

set -eo pipefail

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Configuration
STRICT_MODE=${STRICT_MODE:-false}  # Set to true to block commits
WARN_ONLY=${WARN_ONLY:-true}       # Warn but allow commit

# Allowed files in root (config files)
ALLOWED_ROOT_PATTERNS=(
    "package.json"
    "package-lock.json"
    "yarn.lock"
    "pnpm-lock.yaml"
    "pyproject.toml"
    "setup.py"
    "setup.cfg"
    "requirements.txt"
    "Pipfile"
    "poetry.lock"
    "Cargo.toml"
    "Cargo.lock"
    "go.mod"
    "go.sum"
    "Gemfile"
    "Makefile"
    "justfile"
    "Dockerfile"
    "docker-compose.yml"
    ".dockerignore"
    "tsconfig.json"
    "jsconfig.json"
    ".eslintrc*"
    ".prettierrc*"
    ".editorconfig"
    ".gitignore"
    ".gitattributes"
    ".gitleaksignore"
    ".env.example"
    ".env.template"
    "README.md"
    "CHANGELOG.md"
    "LICENSE*"
    "CODE_OF_CONDUCT.md"
    "SECURITY.md"
    "CONTRIBUTING.md"
)

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -v '/' || true)

if [ -z "$STAGED_FILES" ]; then
    # No files in root being staged
    exit 0
fi

# Check each staged file
MISPLACED_FILES=()

for file in $STAGED_FILES; do
    # Skip if file doesn't exist (deleted)
    if [ ! -f "$file" ]; then
        continue
    fi

    # Check if file matches allowed patterns
    ALLOWED=false
    for pattern in "${ALLOWED_ROOT_PATTERNS[@]}"; do
        if [[ "$file" == $pattern ]]; then
            ALLOWED=true
            break
        fi
    done

    if [ "$ALLOWED" = false ]; then
        # File doesn't match allowed patterns
        # Determine where it should go
        SUGGESTION=""

        if [[ "$file" == *.md ]]; then
            SUGGESTION="docs/"
        elif [[ "$file" == *.sh ]] || [[ -x "$file" ]]; then
            SUGGESTION="scripts/"
        elif [[ "$file" == *test* ]] || [[ "$file" == *spec* ]]; then
            SUGGESTION="tests/"
        elif [[ "$file" == *.tmp ]] || [[ "$file" == *.bak ]] || [[ "$file" == temp_* ]]; then
            SUGGESTION="tmp/"
        else
            SUGGESTION="appropriate directory"
        fi

        MISPLACED_FILES+=("$file → $SUGGESTION")
    fi
done

# Report findings
if [ ${#MISPLACED_FILES[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Project Organization Warning${NC}"
    echo ""
    echo "The following files are being added to the project root:"
    echo ""

    for item in "${MISPLACED_FILES[@]}"; do
        echo -e "  ${RED}✗${NC} $item"
    done

    echo ""
    echo "Recommendation: Move files to appropriate directories before committing"
    echo ""
    echo "To organize your project automatically, run:"
    echo -e "  ${GREEN}@project-cleanup --mode=interactive${NC}"
    echo ""

    if [ "$STRICT_MODE" = true ]; then
        echo -e "${RED}Commit blocked by strict mode.${NC}"
        echo "Set STRICT_MODE=false to allow commits with warnings."
        echo ""
        exit 1
    else
        if [ "$WARN_ONLY" = true ]; then
            echo -e "${YELLOW}Proceeding with commit (warning only).${NC}"
            echo "To block commits, set STRICT_MODE=true"
            echo ""
            exit 0
        fi
    fi
fi

# All good
echo -e "${GREEN}✓ Project organization looks good${NC}"
exit 0
