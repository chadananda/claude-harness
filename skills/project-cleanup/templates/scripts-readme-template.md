# Scripts

## Overview
{Brief description of what scripts in this folder do - build, deployment, utilities, etc.}

## Scripts

### `{script1.sh}`
**Purpose:** {What this script does}
**Usage:** `./scripts/{script1.sh} [arguments]`
**Arguments:**
- `{arg1}` - {Description of argument}
- `{arg2}` (optional) - {Description of optional argument}

**Prerequisites:**
- {Tool/dependency 1}
- {Tool/dependency 2}

**Example:**
```bash
./scripts/{script1.sh} production --verbose
```

### `{script2.py}`
**Purpose:** {What this script does}
**Usage:** `python scripts/{script2.py} [options]`
**Options:**
- `--flag` - {Description of flag}
- `--param VALUE` - {Description of parameter}

**Prerequisites:**
- Python 3.8+
- {Additional dependencies}

**Example:**
```bash
python scripts/{script2.py} --param value
```

## Running Scripts

All scripts should be run from the project root:
```bash
# ✅ Correct
./scripts/build.sh

# ❌ Wrong
cd scripts && ./build.sh
```

## Adding New Scripts

When adding a new script to this folder:

1. **Make it executable:**
   ```bash
   chmod +x scripts/new-script.sh
   ```

2. **Add shebang line:**
   ```bash
   #!/usr/bin/env bash
   # or
   #!/usr/bin/env python3
   ```

3. **Document it in this README** following the format above

4. **Add usage/help output:**
   ```bash
   ./scripts/new-script.sh --help
   ```

## Related Documentation
{Links to relevant documentation}

---

## Template Usage

Replace the {PLACEHOLDERS} with actual values:

- `{Brief description...}` - What scripts in this folder do overall
- `{script.sh}` - Actual script filename
- `{What this script does}` - Single sentence purpose
- `{arg}` - Argument name
- `{Description...}` - Description of what the argument does
- `{Tool/dependency}` - Required tools (Node.js 18+, AWS CLI, etc.)

## Example: scripts/README.md

```markdown
# Scripts

## Overview
Build, deployment, and utility scripts for this project. Scripts handle compiling, testing, deploying, and maintaining the application.

## Scripts

### `build.sh`
**Purpose:** Compiles the project for production
**Usage:** `./scripts/build.sh [environment]`
**Arguments:**
- `environment` (optional) - Target environment (staging, production). Defaults to production.

**Prerequisites:**
- Node.js 18+
- npm or yarn

**Example:**
```bash
./scripts/build.sh production
```

### `deploy.sh`
**Purpose:** Deploys application to specified environment
**Usage:** `./scripts/deploy.sh <environment> [options]`
**Arguments:**
- `environment` - Target environment (staging, production)
- `--skip-tests` (optional) - Skip test suite before deployment
- `--force` (optional) - Force deployment without confirmation

**Prerequisites:**
- AWS CLI configured with credentials
- kubectl access to cluster
- Docker installed

**Example:**
```bash
./scripts/deploy.sh staging
./scripts/deploy.sh production --skip-tests
```

### `setup-dev.sh`
**Purpose:** Sets up local development environment
**Usage:** `./scripts/setup-dev.sh`
**Arguments:** None

**Prerequisites:**
- None (script installs dependencies)

**Example:**
```bash
./scripts/setup-dev.sh
```

### `db-migrate.py`
**Purpose:** Runs database migrations
**Usage:** `python scripts/db-migrate.py [command]`
**Arguments:**
- `command` - Migration command (up, down, status)

**Prerequisites:**
- Python 3.8+
- Database connection configured in .env

**Example:**
```bash
python scripts/db-migrate.py up
python scripts/db-migrate.py status
```

### `cleanup.sh`
**Purpose:** Cleans temporary files and build artifacts
**Usage:** `./scripts/cleanup.sh [options]`
**Arguments:**
- `--all` (optional) - Also remove node_modules and caches

**Prerequisites:**
- None

**Example:**
```bash
./scripts/cleanup.sh
./scripts/cleanup.sh --all
```

## Running Scripts

All scripts should be run from the project root:
```bash
# ✅ Correct
./scripts/build.sh

# ❌ Wrong
cd scripts && ./build.sh
```

This ensures relative paths in scripts work correctly.

## Common Workflows

**Full Deployment:**
```bash
# 1. Build
./scripts/build.sh production

# 2. Run tests
npm test

# 3. Deploy
./scripts/deploy.sh production
```

**Local Development Setup:**
```bash
# 1. Setup environment
./scripts/setup-dev.sh

# 2. Start development server
npm run dev
```

**Database Management:**
```bash
# Check migration status
python scripts/db-migrate.py status

# Run pending migrations
python scripts/db-migrate.py up

# Rollback last migration
python scripts/db-migrate.py down
```

## Troubleshooting

### "Permission denied"
```bash
chmod +x scripts/script-name.sh
```

### "Command not found"
Ensure you're running from project root:
```bash
pwd  # Should show /path/to/project
./scripts/script-name.sh
```

### "Dependencies missing"
Check prerequisites section for each script. Install required tools:
```bash
# Node.js
brew install node

# AWS CLI
brew install awscli

# Python dependencies
pip install -r requirements.txt
```

## Adding New Scripts

When adding a new script to this folder:

1. **Make it executable:**
   ```bash
   chmod +x scripts/new-script.sh
   ```

2. **Add shebang line:**
   ```bash
   #!/usr/bin/env bash
   # or
   #!/usr/bin/env python3
   ```

3. **Document it in this README** following the format above

4. **Add usage/help output:**
   ```bash
   if [ "$1" = "--help" ]; then
       echo "Usage: $0 [options]"
       echo "Options:"
       echo "  --help    Show this help message"
       exit 0
   fi
   ```

5. **Test it works from project root:**
   ```bash
   ./scripts/new-script.sh --help
   ```

## Related Documentation
- Deployment guide: [../docs/deployment.md](../docs/deployment.md)
- Development setup: [../docs/development.md](../docs/development.md)
- Main project README: [../README.md](../README.md)
```

## Automation

This template can be auto-populated by analyzing script files:

```python
def generate_scripts_readme(scripts_dir: Path) -> str:
    \"\"\"Generate scripts/README.md content\"\"\"
    scripts = sorted([f for f in scripts_dir.iterdir() if f.is_file() and is_script(f)])

    content = [
        \"# Scripts\",
        \"\",
        \"## Overview\",
        detect_scripts_purpose(scripts_dir),
        \"\",
        \"## Scripts\",
        \"\"
    ]

    for script in scripts:
        # Extract script metadata
        purpose = extract_script_purpose(script)
        usage = extract_usage_from_script(script)
        prerequisites = detect_prerequisites(script)

        content.extend([
            f\"### `{script.name}`\",
            f\"**Purpose:** {purpose}\",
            f\"**Usage:** `{usage}`\",
            \"**Prerequisites:**\"
        ])

        for prereq in prerequisites:
            content.append(f\"- {prereq}\")

        content.append(\"\")

    # Add common sections
    content.extend([
        \"## Running Scripts\",
        \"\",
        \"All scripts should be run from the project root:\",
        \"```bash\",
        \"./scripts/script-name.sh\",
        \"```\",
        \"\"
    ])

    return \"\\n\".join(content)

def extract_usage_from_script(script_path: Path) -> str:
    \"\"\"Extract usage from script comments or --help output\"\"\"
    # Try running script with --help
    try:
        result = subprocess.run(
            [str(script_path), '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Parse first line of help output
            first_line = result.stdout.strip().split('\\n')[0]
            if 'usage:' in first_line.lower():
                return first_line.replace('Usage:', '').strip()
    except:
        pass

    # Fall back to file analysis
    with open(script_path, 'r') as f:
        for line in f:
            if 'usage:' in line.lower():
                return line.split(':', 1)[1].strip()

    # Default
    return f\"./scripts/{script_path.name}\"

def detect_prerequisites(script_path: Path) -> List[str]:
    \"\"\"Detect script prerequisites from content\"\"\"
    prerequisites = set()

    with open(script_path, 'r') as f:
        content = f.read()

    # Check shebangs and imports
    if '#!/usr/bin/env python' in content:
        prerequisites.add('Python 3.8+')
    if '#!/usr/bin/env node' in content:
        prerequisites.add('Node.js')
    if 'aws ' in content or 'import boto3' in content:
        prerequisites.add('AWS CLI configured')
    if 'kubectl ' in content:
        prerequisites.add('kubectl access')
    if 'docker ' in content:
        prerequisites.add('Docker')
    if 'npm ' in content or 'yarn ' in content:
        prerequisites.add('npm or yarn')

    return sorted(list(prerequisites))
```

## Customization by Project Type

**For deployment scripts:**
- Add more detailed prerequisites (AWS credentials, permissions)
- Include rollback procedures
- Note monitoring/verification steps

**For build scripts:**
- Specify build environments
- Note output locations
- Include clean build instructions

**For utility scripts:**
- Keep usage examples simple
- Note when script should be used
- Add troubleshooting section
