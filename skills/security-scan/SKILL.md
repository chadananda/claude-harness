---
name: security-scan
description: Detect and prevent API keys, tokens, and secrets from being committed to Git repositories. Mandatory QA step for coder agents before implementation completion. Uses Gitleaks for fast scanning with pre-commit hook enforcement.
license: MIT
---

# Security Scan - API Key & Secret Detection

## Overview

**Problem:** AI agents sometimes accidentally hardcode API keys, tokens, and secrets into source code, configs, or documentation, creating security vulnerabilities when committed to Git.

**Solution:** This skill provides fast, automated secret detection using Gitleaks, scans ALL files eligible for commit (respecting .gitignore), and blocks commits containing secrets via pre-commit hooks.

**Used by:** Coder agent as mandatory QA step before signaling completion.

---

## 🎯 Primary Use Case

### Coder Agent QA Workflow (Mandatory)

**After implementing code, before reporting completion:**

1. **Run security scan**
   ```bash
   gitleaks detect --no-git --source . --verbose --report-path ./tmp/security-scan.json
   ```

2. **If NO secrets found** ✅
   - Proceed to report completion
   - Ensure pre-commit hook is installed
   - Pass to tester agent

3. **If secrets FOUND** ❌
   - **DO NOT proceed**
   - Invoke @stuck with details
   - Use remediation guidance (see below)
   - Re-scan after fixes
   - Only proceed when clean

**This is non-negotiable.** No code proceeds to testing with secrets present.

---

## 🚀 Quick Start

### Installation (One-Time Setup)

```bash
# Install Gitleaks
brew install gitleaks  # macOS

# Alternative: Universal installer (Linux/macOS)
curl -sSfL https://raw.githubusercontent.com/gitleaks/gitleaks/master/scripts/install.sh | sh -s -- -b /usr/local/bin

# Windows
choco install gitleaks

# Install pre-commit framework (Python)
pip install pre-commit
```

### First Scan

```bash
# Scan all files (excluding .gitignore entries)
gitleaks detect --no-git --source . --verbose

# Generate detailed report
gitleaks detect --no-git --source . --report-path ./tmp/gitleaks-report.json --verbose
```

### Install Pre-commit Hook

```bash
# Copy template (from this skill)
cp ~/.claude/skills/security-scan/templates/pre-commit-config.yaml ./.pre-commit-config.yaml

# Install hooks
pre-commit install

# Test (scans all files)
pre-commit run --all-files
```

**Pre-commit hook blocks commits containing secrets.**

---

## 🔍 What Gets Scanned

### Included (ALL committable files)
- Source code: `*.py`, `*.js`, `*.go`, `*.rs`, etc.
- Configuration: `.env`, `.env.example`, `config.yaml`, etc.
- MCP server configs: `mcp-config.json`, `server-config.json`
- Documentation: `*.md`, `README`, API docs
- Scripts: `*.sh`, `*.ps1`, build scripts
- Infrastructure as Code: Terraform, CloudFormation, K8s manifests
- Generated files: build configs, lock files (if not in .gitignore)

### Excluded (respects .gitignore)
- Dependencies: `node_modules/`, `vendor/`, `venv/`
- Build outputs: `dist/`, `build/`, `target/`
- Git internals: `.git/`
- Temp files: `./tmp/`, `*.tmp`
- Other .gitignore entries

**Key Point:** Scan respects `.gitignore` - if it won't be committed, it won't be scanned.

---

## 🔑 Detected Secret Types

Gitleaks detects 800+ secret patterns including:

### Common Patterns

**AWS Credentials**
- Access Key ID: `AKIA...`, `ASIA...`, `ABIA...`, `ACCA...`
- Secret Access Key: 40-character base64 strings
- Session tokens

**OpenAI API Keys**
- Legacy: `sk-...` (48 chars)
- Project keys: `sk-proj-...` (contains `T3BlbkFJ`)
- Service account: `sk-svcacct-...`
- Admin keys: `sk-admin-...`

**GitHub Tokens**
- Personal Access Token: `ghp_...`
- OAuth Token: `gho_...`
- App Token: `ghu_...`
- Fine-Grained PAT: `github_pat_...`
- Refresh Token: `ghr_...`

**Stripe Keys**
- Secret: `sk_test_...`, `sk_live_...`
- Restricted: `rk_live_...`

**Database Connection Strings**
- PostgreSQL: `postgresql://user:pass@host/db`
- MongoDB: `mongodb://user:pass@host/db`
- MySQL: `mysql://user:pass@host/db`

**JWT Tokens**
- Format: `ey...ey...`

**Private Keys**
- RSA, EC, DSA, OpenSSH, PGP private keys

**Generic High-Entropy Strings**
- API keys with `api_key`, `apikey` in context
- Tokens with `token`, `secret` in context
- Base64-encoded credentials

**See:** [reference/secret-patterns.md](reference/secret-patterns.md) for complete list with regex patterns.

---

## 🛠️ Coder Agent Workflow

### Step-by-Step Security Scan

**1. After Implementation (before reporting completion)**

```bash
# Run scan on all committable files
gitleaks detect --no-git --source . --verbose --report-path ./tmp/security-scan.json
```

**2a. If CLEAN (no secrets found)**

```markdown
✅ Security scan: PASSED

Files scanned: 45
Secrets detected: 0

Pre-commit hook: ✅ Installed

Ready to report completion.
```

**2b. If SECRETS FOUND**

```markdown
❌ Security scan: FAILED

Secrets detected:
- src/config.py:23 - OpenAI API key (sk-proj-...)
- scripts/deploy.sh:45 - AWS access key (AKIA...)
- docs/api-guide.md:78 - GitHub token (ghp_...)

⚠️  Cannot proceed until resolved.

Remediation options:
1. Move to .env file (load via environment variables)
2. Move to MCP server config (ensure .gitignored)
3. If false positive, add to .gitleaksignore
4. If example key, replace with placeholder (YOUR-KEY-HERE)

See: ~/.claude/skills/security-scan/reference/remediation.md
```

**3. Invoke @stuck (DO NOT proceed)**

```
@stuck

Security Scan FAILED - Secrets detected in committable files

Found:
- src/config.py:23 - OpenAI API key (sk-proj-abc123...)
  Line 23: API_KEY = "sk-proj-abc123def456..."

- scripts/deploy.sh:45 - AWS access key (AKIAIOSFODNN7EXAMPLE)
  Line 45: export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"

These secrets would be committed to Git.

Remediation needed:
1. Move secrets to .env file
2. Update code to load from environment
3. Verify .env is in .gitignore
4. Re-run security scan

Cannot proceed until scan is clean.
```

**4. Remediation (with user guidance)**

```python
# BEFORE (hardcoded secret)
API_KEY = "sk-proj-abc123def456..."

# AFTER (load from environment)
import os
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment")
```

```bash
# Add to .env (this file is in .gitignore)
OPENAI_API_KEY=sk-proj-abc123def456...

# Verify .gitignore contains .env
echo ".env" >> .gitignore
```

**5. Re-scan**

```bash
gitleaks detect --no-git --source . --verbose
# Output: No secrets detected ✅
```

**6. Report completion**

Only after scan is clean.

---

## 🎨 False Positive Management

### Common False Positives

**Example Keys in Documentation:**
```markdown
# ✅ SAFE (marked as example)
To get started, replace `sk-YOUR-KEY-HERE` with your actual key.

export OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE"
```

**Test Data:**
```python
# ✅ SAFE (test file, obvious fake)
def test_api_client():
    fake_key = "sk-proj-test-EXAMPLE-not-real-key"
    client = APIClient(api_key=fake_key)
```

### Using .gitleaksignore

Create `.gitleaksignore` in project root:

```gitignore
# Ignore specific files
docs/examples.md
tests/fixtures/api-keys.json

# Ignore patterns
**/test/**/*.py
examples/**/*
**/*_test.go

# Ignore specific secrets (after rotation/deactivation)
# Format: path:line:commit
src/old-config.py:45:abc123def
```

**Template:** `~/.claude/skills/security-scan/templates/gitleaksignore.template`

### Inline Annotations

```python
# Python
api_key = "sk-proj-example-key"  # gitleaks:allow

# JavaScript
const key = "AKIAIOSFODNN7EXAMPLE";  // gitleaks:allow

# Go
apiKey := "sk-proj-test-key" // gitleaks:allow
```

**Use sparingly:** Only for known safe content like examples and test data.

---

## ⚙️ Configuration

### Custom Patterns

Create `.gitleaks.toml` in project root:

```toml
title = "Project Security Scan Configuration"

# Use all built-in patterns
[extend]
useDefault = true

# Add custom pattern
[[rules]]
id = "custom-internal-token"
description = "Internal Service Token"
regex = '''int_tok_[A-Za-z0-9]{32}'''
tags = ["key", "internal"]
entropy = 3.5

[rules.allowlist]
description = "Ignore safe patterns"
paths = [
    '''.*_test\..*''',
    '''examples/.*''',
    '''docs/.*\.md'''
]
regexes = [
    '''EXAMPLE''',
    '''YOUR-KEY-HERE''',
    '''test-key-not-real'''
]
stopwords = [
    '''example''',
    '''sample''',
    '''test''',
    '''fake''',
    '''placeholder'''
]
```

**Template:** `~/.claude/skills/security-scan/templates/gitleaks.toml`

### Pre-commit Hook Configuration

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.25.0
    hooks:
      - id: gitleaks
        args: ['--no-banner', '--verbose']
```

**Features:**
- Runs automatically on `git commit`
- Scans only staged files (fast)
- Blocks commit if secrets detected
- Bypass: `git commit --no-verify` (discouraged)

---

## 🚑 Remediation Guide

### Step 1: Identify Leaked Secrets

```bash
# Get detailed report
gitleaks detect --no-git --source . --report-path report.json --verbose

# View report
cat report.json | jq '.[]'
```

Output shows:
- File path
- Line number
- Secret type
- Match text (partially redacted)

### Step 2: Move Secrets to Proper Location

**Option A: Environment Variables (.env)**

```bash
# Create/update .env file
echo "OPENAI_API_KEY=sk-proj-actual-key" >> .env
echo "AWS_ACCESS_KEY_ID=AKIA..." >> .env
echo "AWS_SECRET_ACCESS_KEY=..." >> .env

# Ensure .env is gitignored
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
```

Update code:
```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

**Option B: MCP Server Config (gitignored)**

```json
// mcp-server-config.json (in .gitignore)
{
  "mcpServers": {
    "my-service": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_TOKEN": "actual-secret-token"
      }
    }
  }
}
```

Ensure gitignored:
```bash
echo "mcp-server-config.json" >> .gitignore
echo "**/mcp-config.json" >> .gitignore
```

**Option C: Secret Management Service**

- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- Google Secret Manager

### Step 3: Update Documentation

If secret was in docs:

```markdown
<!-- BEFORE -->
Set your API key: `sk-proj-abc123def456...`

<!-- AFTER -->
Set your API key in .env:
```bash
export OPENAI_API_KEY="sk-YOUR-KEY-HERE"
```
Replace `sk-YOUR-KEY-HERE` with your actual key from OpenAI dashboard.
```

### Step 4: Verify Fix

```bash
# Re-scan
gitleaks detect --no-git --source . --verbose

# Should output: No secrets detected ✅
```

### Step 5: Consider Key Rotation

**If secret was committed to Git:**
1. Rotate the key immediately (generate new key)
2. Update .env with new key
3. Deactivate old key in service dashboard
4. Consider the old key compromised

**See:** [reference/remediation.md](reference/remediation.md) for detailed steps.

---

## 🔧 Pre-commit Hook Behavior

### What Happens on Commit

```bash
git add src/config.py
git commit -m "Add configuration"

# Pre-commit hook runs automatically:
Gitleaks...............................................Failed
- hook id: gitleaks
- exit code: 1

    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

Finding:     sk-proj-abc123def456...
Secret:      sk-proj-abc123def456...
RuleID:      openai-api-key
Entropy:     4.5
File:        src/config.py
Line:        23
Fingerprint: 23:abc123...

8:21PM INF 1 commits scanned.
8:21PM INF scan completed in 142ms
8:21PM WRN leaks found: 1
```

**Commit is blocked.** Fix required.

### Bypassing Hook (Emergency Only)

```bash
# Bypass pre-commit hooks (use with extreme caution)
git commit --no-verify -m "Emergency hotfix"
```

**⚠️  WARNING:**
- Bypasses ALL pre-commit hooks, including secret detection
- Should only be used in genuine emergencies
- Secrets will still be caught by CI/CD pipeline
- Requires manual cleanup later

**Better approach:**
```bash
# Add to .gitleaksignore if genuinely safe
echo "path/to/file.py:23" >> .gitleaksignore
git add .gitleaksignore
git commit -m "Allow safe pattern"
```

---

## 📊 Performance

**Scan Speed:**
- Small projects (< 100 files): < 1 second
- Medium projects (100-1000 files): 1-3 seconds
- Large projects (1000+ files): 3-10 seconds

**Pre-commit Hook:**
- Scans only staged files (not entire repo)
- Typically < 1 second
- No noticeable impact on commit workflow

**Memory Usage:**
- Minimal (< 50MB for most projects)
- Golang implementation is very efficient

---

## 🎯 Integration with Coder Agent

### Mandatory QA Step

**Coder agent workflow:**
```
1. Write implementation code
2. Test implementation (basic QA)
3. **Run security scan** ← MANDATORY
   - If clean: proceed
   - If secrets found: invoke @stuck
4. Install pre-commit hook
5. Report completion to team-lead
```

**Agent instructions:**
- **Never skip security scan**
- **Never proceed with secrets present**
- **Always invoke @stuck if secrets found**
- **Assist with remediation using this skill**

### Example Agent Dialogue

```
Coder: Implementation complete. Running security scan...
Coder: [runs gitleaks detect]
Coder: ❌ Security scan failed. API key detected in src/config.py:23

Coder: @stuck

Security scan detected OpenAI API key in src/config.py:23
Line: API_KEY = "sk-proj-abc123..."

Need to:
1. Move to .env file
2. Load via os.getenv()
3. Re-scan

How should I proceed?
```

---

## 📚 Reference Documentation

- **[reference/gitleaks-guide.md](reference/gitleaks-guide.md)** - Complete Gitleaks CLI reference
- **[reference/secret-patterns.md](reference/secret-patterns.md)** - All detectable secret types with regex patterns
- **[reference/false-positives.md](reference/false-positives.md)** - Managing .gitleaksignore and allowlists
- **[reference/remediation.md](reference/remediation.md)** - Step-by-step guide to fixing leaked secrets

## 🎨 Templates

- **[templates/gitleaks.toml](templates/gitleaks.toml)** - Custom configuration template
- **[templates/gitleaksignore.template](templates/gitleaksignore.template)** - Common false positive patterns
- **[templates/pre-commit-config.yaml](templates/pre-commit-config.yaml)** - Pre-commit hook configuration

## 💡 Examples

- **[examples/coder-workflow-example.md](examples/coder-workflow-example.md)** - Complete coder agent workflow example
- **[examples/remediation-example.md](examples/remediation-example.md)** - Step-by-step secret remediation

---

## ✅ Success Criteria

Security scan is successful when:
- ✅ No secrets detected in committable files
- ✅ Pre-commit hook installed and working
- ✅ .gitignore properly configured (.env, MCP configs)
- ✅ False positives managed in .gitleaksignore
- ✅ Custom patterns added (if needed)
- ✅ Agent can proceed to report completion

Security scan FAILS when:
- ❌ Any secret detected in files to be committed
- ❌ API keys, tokens, credentials present
- ❌ Database connection strings with passwords
- ❌ Private keys or certificates

**When scan fails: STOP. Remediate. Re-scan. Only proceed when clean.**

---

## 🔐 Security Best Practices

1. **Never commit secrets** - Use .env files or secret management services
2. **Always .gitignore .env** - Environment files should never be committed
3. **Use environment variables** - Load secrets at runtime via os.getenv()
4. **Rotate leaked keys** - If a secret was committed, rotate immediately
5. **Document placeholders** - Use `YOUR-KEY-HERE` in examples
6. **Pre-commit hooks required** - Enforce automatic scanning
7. **MCP configs gitignored** - Server configs often contain auth tokens
8. **No fake keys in code** - GitHub rejects repos with fake keys matching patterns
9. **Test data separate** - Keep test fixtures in separate files, clearly marked
10. **Regular audits** - Periodic full scans with `gitleaks detect --no-git`

---

## 🆘 Troubleshooting

### "gitleaks command not found"

```bash
# Install Gitleaks
brew install gitleaks  # macOS
# or use universal installer (see Quick Start)
```

### "pre-commit command not found"

```bash
pip install pre-commit
```

### "Too many false positives"

Create `.gitleaksignore`:
```
docs/**/*.md
tests/**/*
examples/**/*
```

### "Scan takes too long"

```bash
# Scan only git-tracked files
gitleaks detect --source . --verbose

# Or use pre-commit hook (staged files only)
pre-commit run gitleaks
```

### "Need to bypass for emergency"

```bash
# Use with caution
git commit --no-verify -m "Emergency fix"

# Then immediately:
# 1. Fix the secret issue
# 2. Run full scan
# 3. Commit remediation
```

---

**For coder agents:** This skill is mandatory QA. No shortcuts. No proceeding with secrets present. Security is non-negotiable. 🔒
