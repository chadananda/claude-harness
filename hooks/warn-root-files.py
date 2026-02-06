#!/usr/bin/env python3
"""PreToolUse hook: Warn when creating non-config files in project root."""
import json
import sys
import os

# Read hook input
data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '') or data.get('tool_input', {}).get('path', '')

# Skip if no file path or if operating in .claude directory
if not file_path or '/.claude/' in file_path:
    sys.exit(0)

# Config files allowed in root
ROOT_ALLOWED = {
    'README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md',
    'package.json', 'package-lock.json', 'yarn.lock', 'bun.lockb',
    'pyproject.toml', 'setup.py', 'requirements.txt', 'Pipfile', 'poetry.lock',
    'Cargo.toml', 'Cargo.lock', 'go.mod', 'go.sum',
    'Makefile', 'Dockerfile', 'docker-compose.yml',
    '.gitignore', '.dockerignore', '.npmignore', '.gitattributes',
    '.env.example', '.env.template',
    'tsconfig.json', 'jsconfig.json', 'vite.config.js', 'vite.config.ts',
    'rollup.config.js', 'webpack.config.js',
    '.prettierrc', '.prettierrc.json', '.eslintrc', '.eslintrc.json', '.eslintrc.js',
    '.editorconfig', '.nvmrc', '.node-version', '.python-version'
}

# Get filename and check if it's in root
filename = os.path.basename(file_path)
parent_dir = os.path.dirname(file_path)

# Only check files being created directly in project root
if parent_dir and parent_dir not in ['.', './']:
    sys.exit(0)  # File is in a subdirectory, allow it

# Check if filename is allowed in root
if filename in ROOT_ALLOWED or filename.startswith('.git'):
    sys.exit(0)  # Allowed config file

# Determine suggested location by extension
ext = os.path.splitext(filename)[1]
suggestions = {
    '.js': 'src/', '.ts': 'src/', '.jsx': 'src/', '.tsx': 'src/',
    '.py': 'src/', '.rs': 'src/', '.go': 'src/',
    '.test.js': 'tests/', '.test.ts': 'tests/', '.spec.js': 'tests/', '.spec.ts': 'tests/',
    '.test.py': 'tests/', '_test.py': 'tests/', '_test.go': 'tests/',
    '.md': 'docs/', '.txt': 'docs/', '.rst': 'docs/',
    '.sh': 'scripts/', '.bash': 'scripts/', '.zsh': 'scripts/',
}

suggested_dir = suggestions.get(ext, 'src/')

# Warn with suggestion
print(f"⚠️  File '{filename}' should go in {suggested_dir} not project root.")
print(f"💡 Suggested: {suggested_dir}{filename}")
print(f"📖 Reason: Only config files belong in root. Code, docs, tests, and scripts should be organized in subdirectories.")

sys.exit(0)  # Exit code 0 = warn only (allow action to proceed)
