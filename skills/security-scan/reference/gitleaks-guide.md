# Gitleaks CLI Reference

Complete guide to using Gitleaks for secret detection.

## Installation

```bash
# macOS
brew install gitleaks

# Universal installer (Linux/macOS)
curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/scripts/install.sh | sh -s -- -b /usr/local/bin

# Windows
choco install gitleaks

# Docker
docker pull zricethezav/gitleaks:latest

# Go install
go install github.com/gitleaks/gitleaks/v8@latest
```

## Basic Usage

### Detect Mode (Scan current state)

```bash
# Scan current directory (respects .git)
gitleaks detect

# Scan without git history (faster, for non-git files)
gitleaks detect --no-git --source .

# Verbose output
gitleaks detect --verbose

# Generate JSON report
gitleaks detect --report-path report.json

# Generate SARIF report (for GitHub Advanced Security)
gitleaks detect --report-format sarif --report-path results.sarif
```

### Protect Mode (Scan staged files only)

```bash
# Scan only staged files (pre-commit use case)
gitleaks protect

# Verbose output
gitleaks protect --verbose

# With custom config
gitleaks protect --config .gitleaks.toml
```

## Command Options

### Common Flags

```bash
--source <path>           # Directory to scan (default: .)
--config <file>           # Config file (default: .gitleaks.toml)
--baseline-path <file>    # Path to baseline file
--report-path <file>      # Output report path
--report-format <format>  # json, csv, sarif (default: json)
--verbose, -v             # Verbose output
--no-git                  # Treat as non-git directory (faster)
--no-banner               # Hide Gitleaks banner
--exit-code <int>         # Custom exit code on leaks found
```

### Advanced Options

```bash
--redact                  # Redact secrets in output
--max-target-megabytes N  # Skip files larger than N MB (default: no limit)
--log-level <level>       # trace, debug, info, warn, error (default: info)
--log-opts <opts>         # Git log options (e.g., --all, --since="1 week ago")
```

## Configuration File (.gitleaks.toml)

### Minimal Config

```toml
title = "Gitleaks Configuration"

[extend]
useDefault = true  # Use all built-in rules
```

### Custom Rule

```toml
[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''api[_-]?key[_-]?[=:]\s*['"]?([A-Za-z0-9]{32,})['"]?'''
tags = ["api", "key"]
entropy = 3.5

[rules.allowlist]
description = "Ignore test files and examples"
paths = [
    '''.*_test\..*''',
    '''examples/.*''',
    '''docs/.*'''
]
regexes = [
    '''EXAMPLE''',
    '''YOUR-KEY-HERE'''
]
stopwords = [
    '''example''',
    '''sample''',
    '''test'''
]
```

### Complete Config Example

```toml
title = "Project Security Configuration"

[extend]
useDefault = true

[[rules]]
id = "internal-token"
description = "Internal Service Token"
regex = '''int_tok_[A-Za-z0-9]{32}'''
tags = ["internal"]
entropy = 3.5

[rules.allowlist]
description = "Allowlist"
paths = [
    '''node_modules/.*''',
    '''vendor/.*''',
    '''.*_test\.go''',
    '''.*\.md'''
]
regexes = [
    '''AKIA.*EXAMPLE''',
    '''sk-.*EXAMPLE''',
    '''test-key-not-real'''
]
stopwords = [
    '''example''',
    '''sample''',
    '''test''',
    '''fake''',
    '''demo''',
    '''placeholder'''
]

[allowlist]
description = "Global allowlist"
paths = [
    '''.git/.*''',
    '''dist/.*''',
    '''build/.*'''
]
commits = [
    '''abc123def456'''  # Specific commit to ignore
]
```

## Allowlist Configuration

### .gitleaksignore File

Create `.gitleaksignore` in project root:

```
# Ignore entire files
docs/api-examples.md
tests/fixtures/keys.json

# Ignore patterns
**/test/**
examples/**/*

# Ignore specific findings (after rotation)
# Format: file:line or file:line:commit
src/config.py:45
old-secrets.js:12:abc123def
```

### Inline Annotations

```python
secret = "sk-proj-example"  # gitleaks:allow
```

```javascript
const key = "AKIAIOSFODNN7EXAMPLE"; // gitleaks:allow
```

```go
apiKey := "test-key" // gitleaks:allow
```

## Exit Codes

```
0 - No leaks detected
1 - Leaks detected
126 - Error (permissions, file not found, etc.)
```

## Output Formats

### JSON (default)

```bash
gitleaks detect --report-format json --report-path report.json
```

```json
[
  {
    "Description": "OpenAI API Key",
    "StartLine": 23,
    "EndLine": 23,
    "StartColumn": 15,
    "EndColumn": 63,
    "Match": "sk-proj-abc***def",
    "Secret": "sk-proj-abc123def456...",
    "File": "src/config.py",
    "Commit": "abc123",
    "Entropy": 4.5,
    "Author": "developer@example.com",
    "Date": "2025-01-10",
    "Message": "Add configuration",
    "Tags": ["key", "openai"],
    "RuleID": "openai-api-key",
    "Fingerprint": "src/config.py:23:openai-api-key:abc123"
  }
]
```

### CSV

```bash
gitleaks detect --report-format csv --report-path report.csv
```

### SARIF (GitHub Advanced Security)

```bash
gitleaks detect --report-format sarif --report-path results.sarif
```

## Performance Tips

### Faster Scanning

```bash
# Skip git history (scan current files only)
gitleaks detect --no-git

# Scan specific directory
gitleaks detect --source ./src

# Skip large files
gitleaks detect --max-target-megabytes 10
```

### Baseline Approach

```bash
# Create baseline (first run)
gitleaks detect --report-path baseline.json

# Subsequent runs (detect new secrets only)
gitleaks detect --baseline-path baseline.json
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Secret Scanning
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### GitLab CI

```yaml
gitleaks:
  image: zricethezav/gitleaks:latest
  stage: test
  script:
    - gitleaks detect --verbose --report-format json --report-path gl-secret-scanning-report.json
  artifacts:
    reports:
      secret_detection: gl-secret-scanning-report.json
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.25.0
    hooks:
      - id: gitleaks
```

## Troubleshooting

### Too Many False Positives

1. Create `.gitleaksignore` for known safe files
2. Add stopwords to config: `example`, `sample`, `test`
3. Use path allowlists in `.gitleaks.toml`
4. Add inline `// gitleaks:allow` comments

### Scan Takes Too Long

1. Use `--no-git` for non-git scanning
2. Limit with `--source ./specific-dir`
3. Skip large files with `--max-target-megabytes`
4. Use baseline approach for incremental scans

### Missing Secrets

1. Check if file is in `.gitleaksignore`
2. Verify entropy threshold (default 3.0)
3. Add custom rules for project-specific patterns
4. Use `--verbose` to see scan progress

### Permission Errors

```bash
# Run with proper permissions
sudo gitleaks detect

# Or fix file permissions
chmod +r file-with-secret.txt
```

## Best Practices

1. **Scan early, scan often** - Run in pre-commit hooks
2. **Use `.gitleaksignore` wisely** - Only for genuine false positives
3. **Rotate before ignoring** - If secret was real, rotate first
4. **Keep config in repo** - Commit `.gitleaks.toml` for consistency
5. **Baseline approach** - Use baselines for large legacy codebases
6. **CI/CD enforcement** - Block PRs with secrets
7. **Regular full scans** - Weekly/monthly full repository scans
8. **Monitor output** - Don't ignore warnings and errors
9. **Custom rules** - Add project-specific secret patterns
10. **Document exceptions** - Comment why secrets are allowlisted

## Resources

- GitHub: https://github.com/gitleaks/gitleaks
- Documentation: https://github.com/gitleaks/gitleaks/wiki
- Configuration: https://github.com/gitleaks/gitleaks#configuration
- Rules: https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml
