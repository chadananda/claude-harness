# {FOLDER_NAME}

## Purpose
{Brief description of what this folder contains and why it exists}

## Contents

### File: {filename1.ext}
**Purpose:** {What this file does}
**Last Updated:** {YYYY-MM-DD} (from git log)
**Dependencies:** {Required libraries, tools, or files}
**Usage:** {How to use this file, if applicable}

### File: {filename2.ext}
**Purpose:** {What this file does}
**Last Updated:** {YYYY-MM-DD}
**Dependencies:** {Required libraries, tools, or files}
**Usage:** {How to use this file, if applicable}

### Subdirectory: {subdirname/}
**Purpose:** {What this subdirectory contains}
**Files:** {Number of files and types}

## Related Documentation
- Main project overview: [../README.md](../README.md)
- {Link to related docs}
- {Link to other relevant documentation}

## Maintenance Notes
{Any special considerations for maintaining files in this folder}
{Common issues or gotchas}
{When to add new files here vs elsewhere}

---

## Template Usage

This template should be used to generate README.md files for folders in the project. Replace the {PLACEHOLDERS} with actual values:

- `{FOLDER_NAME}` - Name of the folder (capitalize first letter)
- `{Brief description...}` - 1-2 sentence description of folder purpose
- `{filename.ext}` - Actual filename
- `{What this file does}` - Single sentence purpose
- `{YYYY-MM-DD}` - Date from git log
- `{Required libraries...}` - List of dependencies
- `{How to use...}` - Usage instructions if applicable
- `{subdirname/}` - Subdirectory name
- `{Number of files...}` - Stats about subdirectory

## Example: docs/README.md

```markdown
# Documentation

## Purpose
Comprehensive project documentation including API references, architecture decisions, user guides, and developer resources.

## Contents

### File: architecture.md
**Purpose:** System architecture and design decisions
**Last Updated:** 2024-11-12
**Dependencies:** None
**Usage:** Reference for understanding system structure

### File: api.md
**Purpose:** REST API endpoint documentation
**Last Updated:** 2024-11-10
**Dependencies:** None
**Usage:** Reference for API consumers and developers

### File: deployment.md
**Purpose:** Deployment procedures and configuration
**Last Updated:** 2024-11-08
**Dependencies:** Docker, Kubernetes knowledge
**Usage:** Follow for deploying to staging/production

### Subdirectory: guides/
**Purpose:** User and developer guides
**Files:** 5 markdown files

## Related Documentation
- Main project overview: [../README.md](../README.md)
- Contributing guidelines: [../CONTRIBUTING.md](../CONTRIBUTING.md)
- API examples: [api.md](api.md)

## Maintenance Notes
- Keep API documentation in sync with actual implementation
- Update deployment docs when infrastructure changes
- Add new guides to guides/ subdirectory
- Use clear, descriptive filenames (e.g., `user-authentication.md` not `auth.md`)
```

## Example: scripts/README.md (see scripts-readme-template.md)

For scripts folder, use the dedicated scripts template which includes usage examples and prerequisites.

## Automation

This template can be auto-populated using git history and file analysis:

```python
def generate_folder_readme(folder_path: Path) -> str:
    \"\"\"Generate README.md content for a folder\"\"\"
    folder_name = folder_path.name.capitalize()

    # Auto-detect purpose from folder name or ask LLM
    purpose = detect_folder_purpose(folder_path)

    # List all files
    files = sorted([f for f in folder_path.iterdir() if f.is_file() and f.name != 'README.md'])
    subdirs = sorted([d for d in folder_path.iterdir() if d.is_dir() and not d.name.startswith('.')])

    content = [
        f\"# {folder_name}\",
        \"\",
        \"## Purpose\",
        purpose,
        \"\",
        \"## Contents\",
        \"\"
    ]

    # Add file entries
    for file in files:
        file_purpose = get_file_purpose(file)
        last_updated = get_last_updated_date(file)

        content.extend([
            f\"### File: {file.name}\",
            f\"**Purpose:** {file_purpose}\",
            f\"**Last Updated:** {last_updated}\",
            \"\"
        ])

    # Add subdirectory entries
    for subdir in subdirs:
        subdir_files = list(subdir.rglob('*'))
        file_count = len([f for f in subdir_files if f.is_file()])

        content.extend([
            f\"### Subdirectory: {subdir.name}/\",
            f\"**Purpose:** {detect_folder_purpose(subdir)}\",
            f\"**Files:** {file_count} files\",
            \"\"
        ])

    # Add related docs
    content.extend([
        \"## Related Documentation\",
        \"- Main project overview: [../README.md](../README.md)\",
        \"\"
    ])

    return \"\\n\".join(content)
```

## Customization

Adjust this template based on folder type:

**For docs/:**
- Emphasize documentation structure
- Link to main README
- Note documentation standards

**For src/:**
- Emphasize code organization
- Link to architecture docs
- Note coding standards

**For tests/:**
- Emphasize test structure
- Link to testing guide
- Note how to run tests

**For scripts/:**
- Use dedicated scripts-readme-template.md
- Include usage examples
- Note prerequisites
