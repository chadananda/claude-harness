#!/usr/bin/env python3
"""
Generate file tree for README.md
"""
import subprocess
from pathlib import Path
from typing import Dict, Optional

# Directories to exclude from tree
EXCLUDE_DIRS = {
    'node_modules', 'dist', 'build', 'target', 'out',
    '__pycache__', '.pytest_cache', '.mypy_cache',
    '.git', '.venv', 'venv', 'env',
    '.tox', '.nox', 'htmlcov', 'coverage',
}

# File descriptions for common files
COMMON_DESCRIPTIONS = {
    'README.md': 'Project overview and quick start',
    '.gitignore': 'Git ignore patterns',
    'package.json': 'Node.js dependencies and scripts',
    'package-lock.json': 'npm dependency lock file',
    'yarn.lock': 'Yarn dependency lock file',
    'pyproject.toml': 'Python package configuration',
    'setup.py': 'Python package setup',
    'requirements.txt': 'Python dependencies',
    'Cargo.toml': 'Rust package manifest',
    'Cargo.lock': 'Rust dependency lock file',
    'go.mod': 'Go module definition',
    'go.sum': 'Go dependency checksums',
    'tsconfig.json': 'TypeScript configuration',
    '.eslintrc': 'ESLint configuration',
    '.prettierrc': 'Prettier configuration',
    'Dockerfile': 'Docker image definition',
    'docker-compose.yml': 'Docker Compose configuration',
    'LICENSE': 'Project license',
    'LICENSE.md': 'Project license',
    'CHANGELOG.md': 'Version history',
    'Makefile': 'Build automation',
}

# Directory descriptions
COMMON_DIR_DESCRIPTIONS = {
    'src': 'Source code',
    'lib': 'Library code',
    'tests': 'Test suite',
    'test': 'Test suite',
    '__tests__': 'Test suite',
    'docs': 'Documentation',
    'scripts': 'Build and deployment scripts',
    'examples': 'Usage examples',
    'tmp': 'Temporary files (gitignored)',
    'dist': 'Build output (gitignored)',
    'build': 'Build output (gitignored)',
    'public': 'Static assets',
    'assets': 'Static assets',
    'components': 'Components',
    'utils': 'Utility functions',
    'helpers': 'Helper functions',
    'models': 'Data models',
    'views': 'View templates',
    'controllers': 'Controllers',
    'routes': 'Application routes',
    'api': 'API definitions',
    'config': 'Configuration files',
}

def should_exclude(name: str) -> bool:
    """Check if directory should be excluded"""
    return name in EXCLUDE_DIRS or name.startswith('.')

def generate_tree_native(root: Path, max_depth: int = 3) -> str:
    """Generate tree using custom Python implementation"""
    def walk_tree(path: Path, prefix: str = "", depth: int = 0) -> list:
        if depth >= max_depth:
            return []
        lines = []
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            items = [item for item in items if not should_exclude(item.name)]
        except PermissionError:
            return []
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└─" if is_last else "├─"
            if item.is_dir():
                lines.append(f"{prefix}{connector} {item.name}/")
                extension = "   " if is_last else "│  "
                lines.extend(walk_tree(item, prefix + extension, depth + 1))
            else:
                lines.append(f"{prefix}{connector} {item.name}")
        return lines
    header = [f"{root.name}/"]
    body = walk_tree(root)
    return "\n".join(header + body)

def add_descriptions(tree: str, root: Path) -> str:
    """Add descriptions to tree lines"""
    lines = tree.split('\n')
    result = []
    for line in lines:
        # Extract filename/dirname from tree line
        # Format: "├─ filename" or "│  ├─ filename"
        match = line.split('─ ')
        if len(match) < 2:
            result.append(line)
            continue
        name = match[1].rstrip('/')
        is_dir = match[1].endswith('/')
        # Get description
        if is_dir:
            desc = COMMON_DIR_DESCRIPTIONS.get(name, '')
        else:
            desc = COMMON_DESCRIPTIONS.get(name, '')
        if desc:
            # Calculate padding for alignment
            padding_length = max(0, 30 - len(line))
            padding = " " * padding_length
            result.append(f"{line}{padding}# {desc}")
        else:
            result.append(line)
    return "\n".join(result)

def get_file_description_from_git(filepath: Path) -> Optional[str]:
    """Get file description from git history"""
    try:
        result = subprocess.run(
            ['git', 'log', '--format=%s', '--follow', '--', str(filepath)],
            capture_output=True,
            text=True,
            cwd=filepath.parent,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            commits = result.stdout.strip().split('\n')
            if commits:
                first_commit = commits[-1]  # Oldest commit
                # Extract description from commit message
                if 'add' in first_commit.lower():
                    return first_commit.replace('add ', '').replace('Add ', '').capitalize()
                return first_commit[:50]  # Limit length
    except:
        pass
    return None

def generate_tree_with_tree_command(root: Path, max_depth: int = 3) -> Optional[str]:
    """Generate tree using system tree command"""
    try:
        exclude_pattern = '|'.join(EXCLUDE_DIRS)
        result = subprocess.run(
            ['tree', '-L', str(max_depth), '--dirsfirst', '-I', exclude_pattern],
            capture_output=True,
            text=True,
            cwd=root,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None

def generate_file_tree(root: Path, max_depth: int = 3, with_descriptions: bool = True) -> str:
    """Generate file tree for README.md"""
    # Try system tree command first
    tree = generate_tree_with_tree_command(root, max_depth)
    # Fall back to native implementation
    if not tree:
        tree = generate_tree_native(root, max_depth)
    # Add descriptions if requested
    if with_descriptions:
        tree = add_descriptions(tree, root)
    return tree

def generate_readme_section(root: Path, max_depth: int = 3) -> str:
    """Generate complete README.md section"""
    tree = generate_file_tree(root, max_depth, with_descriptions=True)
    section = f"""## Project Structure

```
{tree}
```
"""
    return section

def main():
    """Main entry point"""
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Generate file tree for README.md')
    parser.add_argument('path', nargs='?', default='.', help='Project root path')
    parser.add_argument('--depth', type=int, default=3, help='Maximum depth (default: 3)')
    parser.add_argument('--no-descriptions', action='store_true', help='Omit descriptions')
    parser.add_argument('--section', action='store_true', help='Output complete README section')
    args = parser.parse_args()
    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory", file=sys.stderr)
        sys.exit(1)
    # Generate tree
    if args.section:
        output = generate_readme_section(root, args.depth)
    else:
        output = generate_file_tree(root, args.depth, not args.no_descriptions)
    print(output)

if __name__ == '__main__':
    main()
