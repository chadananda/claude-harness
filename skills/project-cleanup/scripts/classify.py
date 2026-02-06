#!/usr/bin/env python3
"""
File classification script for project-cleanup skill
Classifies files in project root into categories and suggests actions
"""
import os
import re
import json
import stat
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Literal

# Configuration patterns
CONFIG_PATTERNS = {
    'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    'pyproject.toml', 'setup.py', 'setup.cfg', 'requirements.txt',
    'Pipfile', 'Pipfile.lock', 'poetry.lock',
    'Cargo.toml', 'Cargo.lock',
    'go.mod', 'go.sum',
    'Gemfile', 'Gemfile.lock',
    'composer.json', 'composer.lock',
    'Makefile', 'justfile', 'CMakeLists.txt',
    'Dockerfile', 'docker-compose.yml', '.dockerignore',
    '.prettierrc', '.eslintrc', '.eslintrc.js', '.eslintrc.json',
    'tsconfig.json', 'jsconfig.json', '.editorconfig',
    'ruff.toml', '.rustfmt.toml',
    '.gitignore', '.gitattributes', '.gitleaksignore',
    '.env.example', '.env.template',
}
ROOT_ALLOWED_DOCS = {
    'README.md', 'CHANGELOG.md',
    'LICENSE', 'LICENSE.txt', 'LICENSE.md',
    'CODE_OF_CONDUCT.md', 'SECURITY.md', 'CONTRIBUTING.md'
}
TEMP_SUFFIXES = {'.tmp', '.temp', '.bak', '.backup', '.swp', '.swo', '.log', '.pid'}
TEST_PATTERNS = [
    r'\.test\.(js|ts|jsx|tsx)$',
    r'\.spec\.(js|ts|jsx|tsx)$',
    r'_test\.(py|go)$',
    r'test_.*\.py$',
    r'_spec\.rb$',
]

FileCategory = Literal['config', 'doc', 'script', 'test', 'temp', 'source', 'unknown']

class FileClassifier:
    def __init__(self, root: Path):
        self.root = root
    def is_config_file(self, name: str) -> bool:
        """Check if file is a configuration file"""
        return name in CONFIG_PATTERNS
    def is_root_allowed_doc(self, name: str) -> bool:
        """Check if doc should stay in root"""
        # Check exact matches
        if name in ROOT_ALLOWED_DOCS:
            return True
        # Check LICENSE variants
        if name.upper().startswith('LICENSE'):
            return True
        return False
    def is_temporary(self, filepath: Path) -> bool:
        """Check if file is temporary"""
        name = filepath.name
        # Temp suffixes
        if any(name.endswith(suffix) for suffix in TEMP_SUFFIXES):
            return True
        # Temp prefixes
        if name.startswith(('temp_', 'tmp_', 'test_', 'debug_')):
            return True
        # Dated filenames
        if re.search(r'\d{4}-\d{2}-\d{2}', name) or re.search(r'\d{8}', name):
            return True
        # Editor files
        if name.endswith('~'):
            return True
        return False
    def is_test_file(self, filepath: Path) -> bool:
        """Check if file is a test file"""
        name = filepath.name
        for pattern in TEST_PATTERNS:
            if re.search(pattern, name):
                return True
        return False
    def is_documentation(self, name: str) -> bool:
        """Check if file is documentation"""
        if not name.endswith('.md'):
            return False
        if self.is_root_allowed_doc(name):
            return False
        return True
    def is_script(self, filepath: Path) -> bool:
        """Check if file is an executable script"""
        # Check extension
        if filepath.suffix in {'.sh', '.bash', '.zsh'}:
            return True
        # Check executable permission
        try:
            st = filepath.stat()
            if st.st_mode & stat.S_IXUSR:
                return True
        except:
            pass
        # Check shebang
        try:
            with open(filepath, 'r', errors='ignore') as f:
                first_line = f.readline()
                if first_line.startswith('#!'):
                    return True
        except:
            pass
        return False
    def is_temporary_script(self, filepath: Path) -> bool:
        """Check if script is temporary"""
        name = filepath.name
        # Dated filenames
        if re.search(r'\d{4}-\d{2}-\d{2}', name) or re.search(r'\d{8}', name):
            return True
        # Temp prefixes
        if name.startswith(('temp_', 'tmp_', 'test_')):
            return True
        # Common temp script names
        if name.lower() in {'test.sh', 'temp.sh', 'quick.sh', 'debug.sh'}:
            return True
        return False
    def classify_file(self, filepath: Path) -> Dict:
        """Classify a single file"""
        name = filepath.name
        # Config files
        if self.is_config_file(name):
            return {
                'path': str(filepath.relative_to(self.root)),
                'category': 'config',
                'action': 'keep_root',
                'reason': 'Standard configuration file'
            }
        # Root-allowed docs
        if self.is_root_allowed_doc(name):
            return {
                'path': str(filepath.relative_to(self.root)),
                'category': 'doc',
                'action': 'keep_root',
                'reason': 'Root documentation file'
            }
        # Temporary files
        if self.is_temporary(filepath):
            return {
                'path': str(filepath.relative_to(self.root)),
                'category': 'temp',
                'action': 'move_tmp',
                'reason': 'Temporary file'
            }
        # Test files
        if self.is_test_file(filepath):
            return {
                'path': str(filepath.relative_to(self.root)),
                'category': 'test',
                'action': 'move_tests',
                'reason': 'Test file'
            }
        # Documentation
        if self.is_documentation(name):
            return {
                'path': str(filepath.relative_to(self.root)),
                'category': 'doc',
                'action': 'move_docs',
                'reason': 'Documentation file'
            }
        # Scripts
        if self.is_script(filepath):
            if self.is_temporary_script(filepath):
                return {
                    'path': str(filepath.relative_to(self.root)),
                    'category': 'script',
                    'action': 'move_tmp',
                    'reason': 'Temporary script'
                }
            else:
                return {
                    'path': str(filepath.relative_to(self.root)),
                    'category': 'script',
                    'action': 'move_scripts',
                    'reason': 'Executable script'
                }
        # Unknown
        return {
            'path': str(filepath.relative_to(self.root)),
            'category': 'unknown',
            'action': 'review',
            'reason': 'Needs manual review'
        }
    def scan_project_root(self) -> List[Dict]:
        """Scan project root and classify all files"""
        results = []
        for item in self.root.iterdir():
            # Skip hidden files and directories
            if item.name.startswith('.'):
                continue
            # Skip directories
            if item.is_dir():
                continue
            # Classify file
            classification = self.classify_file(item)
            results.append(classification)
        return results

def detect_project_language(root: Path) -> Optional[str]:
    """Detect primary project language"""
    if (root / 'pyproject.toml').exists() or (root / 'setup.py').exists():
        return 'python'
    if (root / 'package.json').exists():
        return 'node'
    if (root / 'Cargo.toml').exists():
        return 'rust'
    if (root / 'go.mod').exists():
        return 'go'
    if (root / 'Gemfile').exists():
        return 'ruby'
    return None

def main():
    """Main entry point"""
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Classify project files')
    parser.add_argument('path', nargs='?', default='.', help='Project root path')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--filter', choices=['config', 'doc', 'script', 'test', 'temp', 'unknown'],
                       help='Filter by category')
    args = parser.parse_args()
    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    # Detect language
    language = detect_project_language(root)
    # Classify files
    classifier = FileClassifier(root)
    results = classifier.scan_project_root()
    # Filter if requested
    if args.filter:
        results = [r for r in results if r['category'] == args.filter]
    # Output
    if args.json:
        output = {
            'project_root': str(root),
            'language': language,
            'files': results,
            'summary': {
                'total': len(results),
                'config': len([r for r in results if r['category'] == 'config']),
                'doc': len([r for r in results if r['category'] == 'doc']),
                'script': len([r for r in results if r['category'] == 'script']),
                'test': len([r for r in results if r['category'] == 'test']),
                'temp': len([r for r in results if r['category'] == 'temp']),
                'unknown': len([r for r in results if r['category'] == 'unknown']),
            }
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"Project: {root}")
        print(f"Language: {language or 'Unknown'}")
        print(f"\nClassified {len(results)} files:\n")
        for result in results:
            icon = {'config': '⚙️', 'doc': '📄', 'script': '📜', 'test': '🧪',
                   'temp': '🗑️', 'unknown': '❓'}.get(result['category'], '📁')
            action_text = {
                'keep_root': 'Keep in root',
                'move_docs': 'Move to docs/',
                'move_scripts': 'Move to scripts/',
                'move_tmp': 'Move to tmp/',
                'move_tests': 'Move to tests/',
                'review': 'Needs review'
            }.get(result['action'], result['action'])
            print(f"{icon} {result['path']}")
            print(f"   Action: {action_text}")
            print(f"   Reason: {result['reason']}\n")

if __name__ == '__main__':
    main()
