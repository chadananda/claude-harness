# False Positive Management

Guide to handling false positives in secret scanning.

## Understanding False Positives

**False Positive:** When Gitleaks flags content as a secret, but it's actually safe.

**Common causes:**
- Example keys in documentation
- Test data with fake secrets
- High-entropy non-secrets (UUIDs, hashes, base64 images)
- Deactivated/rotated keys
- Public keys (not secrets)

##Using .gitleaksignore

### File Location

Create `.gitleaksignore` in project root (same level as `.git/`).

### Syntax

```gitignore
# Ignore entire files
path/to/safe-file.md
docs/api-examples.md

# Ignore directories
tests/fixtures/
examples/

# Glob patterns
**/test/**/*.py
**/*_test.go
docs/**/*.md

# Ignore specific findings (after rotation)
# Format: file:line or file:line:commit
src/old-config.py:45
scripts/deploy.sh:23:abc123def456

# Comments
# This file contains example keys only
```

### Example .gitleaksignore

```gitignore
# Documentation with example keys
README.md
docs/getting-started.md
docs/api-reference.md

# Test fixtures
tests/fixtures/api-keys.json
tests/data/sample-credentials.yaml

# Example code
examples/**/*

# Test files (all languages)
**/*_test.py
**/*_test.go
**/*_test.js
**/*.test.ts
**/*Spec.js

# Deactivated secrets (rotated on 2025-01-10)
src/legacy-config.py:45:abc123
old-deployment.sh:67:def456
```

## Inline Annotations

### Python

```python
# Suppress single line
api_key = "sk-proj-example-not-real"  # gitleaks:allow

# Suppress block
# gitleaks:allow
DATABASE_URL = "postgresql://user:pass@localhost/db"
API_TOKEN = "test-token-12345"
```

### JavaScript/TypeScript

```javascript
// Single line
const key = "AKIAIOSFODNN7EXAMPLE"; // gitleaks:allow

// Block
/* gitleaks:allow */
const config = {
  apiKey: "test-key-example",
  secret: "sample-secret-123"
};
```

### Go

```go
// Single line
apiKey := "test-key-not-real" // gitleaks:allow

// Block
// gitleaks:allow
var credentials = map[string]string{
    "key": "example-key-123",
    "secret": "sample-secret-456",
}
```

### YAML

```yaml
# gitleaks:allow
credentials:
  api_key: "test-key-example"
  secret: "sample-secret-123"
```

### Shell Scripts

```bash
# gitleaks:allow
export API_KEY="example-key-not-real"
export AWS_ACCESS_KEY="AKIA...EXAMPLE"
```

## Configuration-Based Allowlists

### In .gitleaks.toml

#### Path-Based Allowlist

```toml
[allowlist]
description = "Allowlist for false positives"

paths = [
    # Test files
    '''.*_test\.py''',
    '''.*_test\.go''',
    '''.*\.test\.js''',
    '''.*Spec\.js''',

    # Documentation
    '''docs/.*\.md''',
    '''README\.md''',
    '''examples/.*''',

    # Dependencies
    '''node_modules/.*''',
    '''vendor/.*''',
    '''\.git/.*''',

    # Build outputs
    '''dist/.*''',
    '''build/.*''',
    '''target/.*'''
]
```

#### Regex-Based Allowlist

```toml
[allowlist]
regexes = [
    # Example keys
    '''AKIA.*EXAMPLE''',
    '''sk-proj-.*EXAMPLE''',
    '''sk-.*YOUR-KEY-HERE''',

    # Test keys
    '''test-key-not-real''',
    '''fake-.*-key''',

    # Placeholders
    '''YOUR-.*-HERE''',
    '''REPLACE-WITH-.*''',
    '''INSERT-.*-HERE'''
]
```

#### Stopword-Based Allowlist

```toml
[allowlist]
stopwords = [
    'example',
    'sample',
    'test',
    'fake',
    'demo',
    'placeholder',
    'your-key-here',
    'replace-with'
]
```

#### Commit-Based Allowlist

```toml
[allowlist]
commits = [
    'abc123def456',  # Legacy migration commit
    'xyz789ghi012'   # One-time import with safe data
]
```

### Per-Rule Allowlists

```toml
[[rules]]
id = "aws-access-key"
description = "AWS Access Key ID"
regex = '''(AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}'''

[rules.allowlist]
description = "Allow AWS example keys"
paths = [
    '''docs/.*''',
    '''examples/.*'''
]
regexes = [
    '''AKIA.*EXAMPLE''',
    '''ASIA.*SAMPLE'''
]
stopwords = [
    'example',
    'sample'
]
```

## Managing Example Keys in Documentation

### Safe Patterns

```markdown
# ✅ GOOD - Clearly marked as example
To get started, replace `sk-YOUR-KEY-HERE` with your actual API key:

```bash
export OPENAI_API_KEY="sk-YOUR-KEY-HERE"
```

# ✅ GOOD - Obvious placeholder
Set your AWS credentials:
```bash
export AWS_ACCESS_KEY_ID="AKIA...EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalr...EXAMPLE"
```

# ✅ GOOD - Inline annotation
```python
# gitleaks:allow
api_key = "sk-proj-example-for-documentation-only"
```

# ❌ BAD - Looks like real key
```bash
export OPENAI_API_KEY="sk-proj-Hq8L7pB9kN2mX..."
```
```

### Placeholder Conventions

Use these placeholder patterns (automatically allowed):

```
# API Keys
sk-YOUR-KEY-HERE
sk-proj-YOUR-KEY-HERE
api-key-YOUR-KEY-HERE

# AWS
AKIA...EXAMPLE
ASIA...EXAMPLE
wJalr...EXAMPLE

# Tokens
ghp-YOUR-TOKEN-HERE
token-YOUR-TOKEN-HERE

# Generic
YOUR-SECRET-HERE
REPLACE-WITH-ACTUAL-KEY
INSERT-YOUR-KEY-HERE
```

## High-Entropy Non-Secrets

### UUIDs

```toml
[allowlist]
regexes = [
    # Standard UUID format
    '''[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'''
]
```

### Base64 Images

```toml
[allowlist]
regexes = [
    # Data URI images
    '''data:image/.*base64,.*'''
]
```

### Git Commit SHAs

```toml
[allowlist]
regexes = [
    # Git commit hashes (context-dependent)
    '''commit [0-9a-f]{40}'''
]
```

## Deactivated/Rotated Keys

### After Key Rotation

**If a secret was committed and rotated:**

1. **Rotate the key** (generate new one, deactivate old)
2. **Remove from code** (replace with environment variable)
3. **Add to .gitleaksignore** (prevent future false positives)

```gitignore
# Rotated keys (deactivated on 2025-01-10)
src/config.py:45:abc123def  # Old OpenAI key (rotated)
deploy.sh:67:def456ghi      # Old AWS key (rotated)
```

### Documenting Rotated Keys

```gitignore
# Rotated keys - SAFE TO IGNORE
# These keys were rotated and deactivated before being added to this file

# OpenAI API key - rotated 2025-01-10
src/legacy/config.py:45

# AWS credentials - rotated 2025-01-05
infrastructure/old-deploy.sh:23
```

## Test Data

### Test Fixtures

```gitignore
# Test fixtures with fake credentials
tests/fixtures/api-responses.json
tests/data/sample-keys.yaml
tests/mocks/credentials.js
```

### Test Files

```toml
[allowlist]
paths = [
    # Python tests
    '''.*_test\.py''',
    '''.*test_.*\.py''',
    '''tests/.*\.py''',

    # JavaScript/TypeScript tests
    '''.*\.test\.js''',
    '''.*\.test\.ts''',
    '''.*\.spec\.js''',
    '''.*\.spec\.ts''',
    '''__tests__/.*''',

    # Go tests
    '''.*_test\.go''',

    # Rust tests
    '''.*_test\.rs''',

    # Any test directory
    '''tests/.*''',
    '''test/.*''',
    '''__tests__/.*'''
]
```

## Public Keys (Not Secrets)

Public keys should NOT be flagged:

```gitignore
# Public SSH keys
*.pub
id_rsa.pub
authorized_keys

# Public certificates
*.crt
*.pem (public only)
```

But private keys SHOULD be flagged:
```
# Private keys (should be detected)
id_rsa
*.key
*-private.pem
```

## Best Practices

### ✅ DO:

1. **Add to .gitleaksignore** for genuine false positives
2. **Use placeholders** in documentation (`YOUR-KEY-HERE`)
3. **Rotate before ignoring** if key was real
4. **Comment allowlist entries** (why it's safe)
5. **Use stopwords** for common safe patterns
6. **Inline annotations** for isolated cases
7. **Test directory allowlists** for test files

### ❌ DON'T:

1. **Ignore without reviewing** - always verify it's truly safe
2. **Allowlist real secrets** - rotate first, then remove
3. **Overuse inline annotations** - prefer .gitleaksignore
4. **Ignore entire directories** unless necessary
5. **Use vague comments** - document why it's safe
6. **Skip testing** - verify allowlists work as expected
7. **Forget to update** - review periodically

## Verification Workflow

### After Adding to Allowlist

```bash
# 1. Add to .gitleaksignore or .gitleaks.toml
echo "docs/api-examples.md" >> .gitleaksignore

# 2. Test scan (should no longer flag)
gitleaks detect --verbose

# 3. Verify specific file
gitleaks detect --source docs/api-examples.md

# 4. Commit allowlist changes
git add .gitleaksignore
git commit -m "chore: allowlist API examples documentation"
```

## Example Complete Configuration

```toml
# .gitleaks.toml
title = "Project Security Scan"

[extend]
useDefault = true

[allowlist]
description = "Global allowlist for false positives"

paths = [
    # Tests
    '''.*_test\..*''',
    '''tests/.*''',
    '''__tests__/.*''',

    # Documentation
    '''docs/.*\.md''',
    '''examples/.*''',
    '''README\.md''',

    # Dependencies
    '''node_modules/.*''',
    '''vendor/.*''',

    # Build
    '''dist/.*''',
    '''build/.*'''
]

regexes = [
    # Placeholders
    '''YOUR-.*-HERE''',
    '''REPLACE-WITH-.*''',
    '''.*EXAMPLE.*''',

    # Test patterns
    '''test-key-not-real''',
    '''fake-.*''',

    # UUIDs
    '''[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'''
]

stopwords = [
    'example',
    'sample',
    'test',
    'fake',
    'demo',
    'not-real',
    'placeholder'
]

commits = []  # Add specific commits if needed
```

## Troubleshooting

### Still Getting False Positives?

1. **Check stopwords** - add common words
2. **Review regex patterns** - be specific
3. **Use path allowlists** - exclude entire directories
4. **Inline annotations** - for specific lines
5. **Adjust entropy threshold** - in custom rules

### Allowlist Not Working?

1. **Verify syntax** - check TOML format
2. **Test pattern** - use `gitleaks detect --verbose`
3. **Check file paths** - use relative paths from project root
4. **Regex escaping** - use triple quotes in TOML: `'''pattern'''`
5. **Reload config** - ensure `.gitleaks.toml` is in project root

## Summary

**Priority order for handling false positives:**

1. **Review first** - Is it genuinely safe?
2. **Stopwords** - For common safe patterns
3. **Regex allowlist** - For pattern-based exclusions
4. **Path allowlist** - For files/directories
5. **.gitleaksignore** - For specific file:line cases
6. **Inline annotations** - As last resort

**Always document why something is allowlisted.**
