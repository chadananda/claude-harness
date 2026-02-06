# Secret Remediation Guide

Step-by-step guide to fixing leaked secrets detected by Gitleaks.

## Immediate Response

**When secrets are detected:**

1. **STOP** - Do not proceed with commit/push
2. **Assess** - Identify what secrets were detected
3. **Rotate** - If secret was committed, rotate immediately
4. **Remediate** - Move secrets to proper location
5. **Verify** - Re-scan to confirm clean
6. **Document** - Record what happened and how it was fixed

---

## Step 1: Identify Leaked Secrets

### Run Detailed Scan

```bash
# Generate full report
gitleaks detect --no-git --source . --report-path ./tmp/security-report.json --verbose

# View report (prettified)
cat ./tmp/security-report.json | jq '.'
```

### Analyze Report

```json
{
  "Description": "OpenAI API Key",
  "File": "src/config.py",
  "StartLine": 23,
  "Match": "sk-proj-***",
  "Secret": "sk-proj-Hq8L7pB9...",
  "RuleID": "openai-api-key",
  "Tags": ["key", "openai"]
}
```

**Record:**
- File path: `src/config.py`
- Line number: `23`
- Secret type: OpenAI API Key
- Full secret: `sk-proj-Hq8L7pB9...` (for rotation)

---

## Step 2: Rotate the Secret (If Committed)

**If secret was EVER committed to Git:**

### OpenAI API Keys

```bash
# 1. Log into OpenAI Platform
# 2. Navigate to API Keys
# 3. Find the leaked key
# 4. Click "Delete" or "Revoke"
# 5. Create new key
# 6. Update .env with new key
```

### AWS Credentials

```bash
# Using AWS CLI
aws iam delete-access-key --access-key-id AKIA...

# Create new key
aws iam create-access-key --user-name your-user

# Update .env
echo "AWS_ACCESS_KEY_ID=AKIA..." > .env
echo "AWS_SECRET_ACCESS_KEY=..." >> .env
```

### GitHub Tokens

```bash
# 1. Go to https://github.com/settings/tokens
# 2. Find the leaked token
# 3. Click "Delete"
# 4. Generate new token
# 5. Update .env
```

### Stripe Keys

```bash
# 1. Log into Stripe Dashboard
# 2. Go to Developers > API Keys
# 3. Click "Roll" on the leaked key
# 4. Copy new key
# 5. Update .env
```

### Database Credentials

```sql
-- PostgreSQL
ALTER USER username WITH PASSWORD 'new-password';

-- MySQL
ALTER USER 'username'@'localhost' IDENTIFIED BY 'new-password';

-- Update connection string in .env
```

**⚠️  CRITICAL: Rotate BEFORE fixing code. Assume compromised until rotated.**

---

## Step 3: Move Secrets to Proper Location

### Option A: Environment Variables (.env)

**1. Create/update .env file:**

```bash
# .env
OPENAI_API_KEY=sk-proj-NEW-KEY-HERE
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
DATABASE_URL=postgresql://user:newpass@localhost/db
```

**2. Ensure .env is gitignored:**

```bash
# Check if .env is in .gitignore
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore

# Also ignore common variations
grep -q "^\.env\.local$" .gitignore || echo ".env.local" >> .gitignore
```

**3. Update code to load from environment:**

**Python:**
```python
# BEFORE (hardcoded - BAD)
API_KEY = "sk-proj-abc123..."

# AFTER (environment variable - GOOD)
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

**JavaScript/Node.js:**
```javascript
// BEFORE (hardcoded - BAD)
const apiKey = "sk-proj-abc123...";

// AFTER (environment variable - GOOD)
require('dotenv').config();

const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
    throw new Error("OPENAI_API_KEY environment variable not set");
}
```

**Go:**
```go
// BEFORE (hardcoded - BAD)
apiKey := "sk-proj-abc123..."

// AFTER (environment variable - GOOD)
import "os"

apiKey := os.Getenv("OPENAI_API_KEY")
if apiKey == "" {
    panic("OPENAI_API_KEY environment variable not set")
}
```

**Rust:**
```rust
// BEFORE (hardcoded - BAD)
let api_key = "sk-proj-abc123...";

// AFTER (environment variable - GOOD)
use std::env;

let api_key = env::var("OPENAI_API_KEY")
    .expect("OPENAI_API_KEY environment variable not set");
```

### Option B: MCP Server Config (Gitignored)

**For MCP server configurations:**

**1. Create config file (gitignored):**

```json
// mcp-server-config.json
{
  "mcpServers": {
    "my-service": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_TOKEN": "actual-secret-token",
        "DATABASE_URL": "postgresql://user:pass@host/db"
      }
    }
  }
}
```

**2. Gitignore the config:**

```bash
echo "mcp-server-config.json" >> .gitignore
echo "**/mcp-config.json" >> .gitignore
echo "mcp-server-*.json" >> .gitignore
```

**3. Create example template (safe to commit):**

```json
// mcp-server-config.example.json
{
  "mcpServers": {
    "my-service": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_TOKEN": "YOUR-TOKEN-HERE",
        "DATABASE_URL": "postgresql://user:pass@localhost/db"
      }
    }
  }
}
```

### Option C: Secret Management Service

**AWS Secrets Manager:**

```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
secrets = get_secret('prod/api/keys')
API_KEY = secrets['openai_key']
```

**HashiCorp Vault:**

```python
import hvac

client = hvac.Client(url='http://localhost:8200')
secret = client.secrets.kv.v2.read_secret_version(path='api/keys')
API_KEY = secret['data']['data']['openai_key']
```

---

## Step 4: Update Documentation

**If secret was in documentation:**

**BEFORE (BAD):**
```markdown
## Setup

Set your API key:
```bash
export OPENAI_API_KEY="sk-proj-Hq8L7pB9kN2mX..."
```
```

**AFTER (GOOD):**
```markdown
## Setup

1. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-YOUR-KEY-HERE
```

2. Replace `sk-YOUR-KEY-HERE` with your actual API key from [OpenAI Dashboard](https://platform.openai.com/api-keys)

3. Ensure `.env` is in `.gitignore` (it should be by default)
```

---

## Step 5: Clean Up Code

### Remove Hardcoded Secrets

**Find all occurrences:**

```bash
# Search for the leaked secret pattern
grep -r "sk-proj-" . --exclude-dir=node_modules --exclude-dir=.git

# Search for common secret patterns
grep -r "api_key\|API_KEY\|secret\|SECRET" . --include="*.py" --include="*.js"
```

**Replace with environment variable loading:**

```bash
# Example: Replace all instances in Python files
find . -name "*.py" -exec sed -i '' 's/API_KEY = "sk-proj-.*"/API_KEY = os.getenv("OPENAI_API_KEY")/g' {} +
```

### Add Error Handling

```python
# Good practice: Fail fast if environment variable missing
import os

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError(
        "OPENAI_API_KEY environment variable not set. "
        "Please add it to your .env file."
    )
```

---

## Step 6: Verify Fix

### Re-run Security Scan

```bash
# Full scan
gitleaks detect --no-git --source . --verbose

# Should output: No leaks detected ✅
```

### Test Application

```bash
# Verify environment variables load correctly
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"

# Run application
npm start  # or: python app.py, cargo run, etc.
```

### Verify .gitignore

```bash
# Check what would be committed
git status

# .env should NOT appear
# If it does:
git rm --cached .env
git commit -m "chore: remove .env from tracking"
```

---

## Step 7: Document the Incident

### Create Incident Log

```markdown
# Security Incident Log

## 2025-01-12: API Key Leak

**What happened:**
- OpenAI API key was hardcoded in `src/config.py:23`
- Detected by security scan before commit

**Actions taken:**
1. Rotated API key in OpenAI dashboard
2. Moved secret to `.env` file
3. Updated code to load from environment
4. Verified `.env` in `.gitignore`
5. Re-scanned and confirmed clean

**Prevention:**
- Pre-commit hook installed
- Team training on environment variables
- Documentation updated with secure practices

**Status:** Resolved
```

---

## Common Remediation Scenarios

### Scenario 1: Secret in Config File

**Problem:**
```python
# config.py
DATABASE_URL = "postgresql://admin:secretpass123@prod.db.com/app"
```

**Solution:**
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment")
```

```bash
# .env
DATABASE_URL=postgresql://admin:secretpass123@prod.db.com/app
```

### Scenario 2: Secret in Deployment Script

**Problem:**
```bash
# deploy.sh
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG..."
```

**Solution:**
```bash
# deploy.sh
# Load from environment (set in CI/CD secrets)
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo "Error: AWS_ACCESS_KEY_ID not set"
    exit 1
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "Error: AWS_SECRET_ACCESS_KEY not set"
    exit 1
fi

# Use AWS credentials from environment
aws s3 sync ./dist s3://my-bucket
```

### Scenario 3: Secret in Docker Compose

**Problem:**
```yaml
# docker-compose.yml
services:
  app:
    environment:
      - API_KEY=sk-proj-abc123def456...
```

**Solution:**
```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env
    environment:
      - API_KEY=${API_KEY}
```

```bash
# .env
API_KEY=sk-proj-abc123def456...
```

### Scenario 4: Secret in Documentation

**Problem:**
```markdown
# README.md
## Quick Start
```bash
export STRIPE_KEY="sk_live_51HrF2J..."
```
```

**Solution:**
```markdown
# README.md
## Quick Start

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add your Stripe key to `.env`:
```
STRIPE_KEY=your-stripe-key-here
```

3. Get your key from [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
```

---

## Prevention Checklist

After remediation, ensure:

- [ ] Secret rotated (if was committed)
- [ ] Secrets moved to `.env` or secret manager
- [ ] `.env` in `.gitignore`
- [ ] Code loads from environment variables
- [ ] Error handling for missing variables
- [ ] Documentation updated with secure examples
- [ ] Re-scanned with gitleaks (clean)
- [ ] Pre-commit hook installed
- [ ] `.env.example` created (safe template)
- [ ] Incident documented

---

## Emergency Procedures

### If Secret Was Already Pushed to GitHub

**Immediate actions:**

1. **Rotate secret immediately** (assume compromised)
2. **Remove from history** (optional, complex):
   ```bash
   # Use BFG Repo-Cleaner or git-filter-repo
   bfg --replace-text passwords.txt
   git push --force
   ```
   ⚠️  **Warning:** Force push rewrites history, affects collaborators

3. **Notify team** if in shared repository
4. **Check GitHub Advanced Security** for alerts
5. **Monitor for unauthorized usage**

### If Secret is in Public Repository

**Additional steps:**

1. **Rotate immediately** (critical - assume compromised)
2. **Check access logs** in service dashboard
3. **Revoke all related sessions/tokens**
4. **Enable 2FA** if not already enabled
5. **Consider security audit** of accounts/services

---

## Testing the Remediation

```bash
# 1. Clean scan
gitleaks detect --no-git --source . --verbose
# Output: No leaks detected ✅

# 2. Check .gitignore
git check-ignore .env
# Output: .env ✅

# 3. Verify environment loading
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(bool(os.getenv('API_KEY')))"
# Output: True ✅

# 4. Test application
npm test  # or: pytest, go test, cargo test
# Output: All tests pass ✅

# 5. Check git status
git status
# Output: .env should NOT appear ✅
```

---

## Long-Term Prevention

1. **Always use environment variables** for secrets
2. **Never hardcode credentials** in source code
3. **Pre-commit hooks mandatory** for all projects
4. **CI/CD scans** in all pipelines
5. **Regular security audits** (monthly full scans)
6. **Team training** on secure coding practices
7. **`.env.example` templates** for all projects
8. **Secret rotation policies** (quarterly or on-demand)
9. **Monitoring and alerting** for secret access
10. **Incident response plan** ready to execute

---

## Summary

**Remediation workflow:**
1. **Identify** - Run gitleaks, analyze report
2. **Rotate** - Immediately if committed
3. **Move** - To .env or secret manager
4. **Update** - Code to load from environment
5. **Document** - Update docs with secure examples
6. **Verify** - Re-scan, test, check gitignore
7. **Prevent** - Install pre-commit hooks, document incident

**Remember:** Security is not optional. Take time to do it right. 🔒
