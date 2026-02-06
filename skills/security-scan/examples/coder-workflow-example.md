# Coder Agent Security Scan Workflow Example

Complete example of how the coder agent integrates security scanning into its QA workflow.

## Scenario

Coder agent implements a new API configuration module and must run security scan before reporting completion.

---

## Step-by-Step Workflow

### Phase 1: Implementation

**Coder agent creates:**

```python
# src/config.py
import requests

# API configuration
OPENAI_API_KEY = "sk-proj-EXAMPLE_KEY_DO_NOT_USE_PLACEHOLDER_12345"
STRIPE_API_KEY = "sk_live_EXAMPLE_KEY_DO_NOT_USE_1234567890"

# Database connection
DATABASE_URL = "postgresql://admin:SecretPass123@prod.db.company.com:5432/app_db"

def get_openai_client():
    return requests.Session(headers={"Authorization": f"Bearer {OPENAI_API_KEY}"})

def get_stripe_client():
    import stripe
    stripe.api_key = STRIPE_API_KEY
    return stripe

def get_db_connection():
    import psycopg2
    return psycopg2.connect(DATABASE_URL)
```

**Coder agent dialogue:**
```
Coder: Implementation complete. Created src/config.py with API clients.
Coder: Now running mandatory security scan...
```

### Phase 2: Security Scan (Mandatory)

**Coder runs:**
```bash
gitleaks detect --no-git --source . --verbose --report-path ./tmp/security-scan.json
```

**Output:**
```
    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

Finding:     sk-proj-Hq8L7pB9...
Secret:      sk-proj-EXAMPLE_KEY_DO_NOT_USE_PLACEHOLDER_12345
RuleID:      openai-api-key
Entropy:     4.5
File:        src/config.py
Line:        5
Fingerprint: src/config.py:openai-api-key:5

Finding:     sk_live_51HrF2J...
Secret:      sk_live_EXAMPLE_KEY_DO_NOT_USE_1234567890
RuleID:      stripe-api-key
Entropy:     4.2
File:        src/config.py
Line:        6
Fingerprint: src/config.py:stripe-api-key:6

Finding:     postgresql://admin:SecretPass123@...
Secret:      [REDACTED]
RuleID:      connection-string
Entropy:     3.8
File:        src/config.py
Line:        9
Fingerprint: src/config.py:connection-string:9

8:45PM INF 1 commits scanned.
8:45PM INF scan completed in 89ms
8:45PM WRN leaks found: 3
```

**Coder agent response:**
```
Coder: ❌ Security scan FAILED

Detected 3 secrets in src/config.py:
1. Line 5: OpenAI API key (sk-proj-...)
2. Line 6: Stripe API key (sk_live_...)
3. Line 9: Database connection string with password

Cannot proceed. Invoking @stuck for guidance.
```

### Phase 3: Remediation (via @stuck)

**Coder invokes @stuck:**
```
@stuck

Security Scan FAILED - Multiple secrets detected

File: src/config.py

Findings:
1. Line 5: OpenAI API key
   OPENAI_API_KEY = "sk-proj-EXAMPLE_KEY_DO_NOT_USE_PLACEHOLDER_12345"

2. Line 6: Stripe API key
   STRIPE_API_KEY = "sk_live_EXAMPLE_KEY_DO_NOT_USE_1234567890"

3. Line 9: Database connection string
   DATABASE_URL = "postgresql://admin:SecretPass123@prod.db.company.com:5432/app_db"

Remediation plan:
1. Move all secrets to .env file
2. Update code to load from environment variables
3. Verify .env is in .gitignore
4. Re-run security scan

Need approval to proceed with remediation.
```

**User response:**
```
User: Yes, proceed with remediation. Move all secrets to .env.
```

### Phase 4: Fix Implementation

**Coder creates .env:**
```bash
# .env
OPENAI_API_KEY=sk-proj-EXAMPLE_KEY_DO_NOT_USE_PLACEHOLDER_12345
STRIPE_API_KEY=sk_live_EXAMPLE_KEY_DO_NOT_USE_1234567890
DATABASE_URL=postgresql://admin:SecretPass123@prod.db.company.com:5432/app_db
```

**Coder updates .gitignore:**
```bash
# Check if .env is in .gitignore
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
```

**Coder updates src/config.py:**
```python
# src/config.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration (loaded from environment)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
if not STRIPE_API_KEY:
    raise ValueError("STRIPE_API_KEY environment variable not set")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

def get_openai_client():
    return requests.Session(headers={"Authorization": f"Bearer {OPENAI_API_KEY}"})

def get_stripe_client():
    import stripe
    stripe.api_key = STRIPE_API_KEY
    return stripe

def get_db_connection():
    import psycopg2
    return psycopg2.connect(DATABASE_URL)
```

**Coder creates .env.example:**
```bash
# .env.example
OPENAI_API_KEY=sk-YOUR-KEY-HERE
STRIPE_API_KEY=sk_test_YOUR-KEY-HERE
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Phase 5: Re-scan

**Coder runs security scan again:**
```bash
gitleaks detect --no-git --source . --verbose
```

**Output:**
```
    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

8:47PM INF 1 commits scanned.
8:47PM INF scan completed in 72ms
8:47PM INF no leaks found
```

**Coder agent response:**
```
Coder: ✅ Security scan: PASSED

Files scanned: 48
Secrets detected: 0

Remediation summary:
- Moved 3 secrets to .env file
- Updated src/config.py to load from environment
- Verified .env is in .gitignore
- Created .env.example template
- Re-scanned: clean ✅

Ready to report completion.
```

### Phase 6: Install Pre-commit Hook

**Coder installs hook:**
```bash
# Copy pre-commit config from skill
cp ~/.claude/skills/security-scan/templates/pre-commit-config.yaml ./.pre-commit-config.yaml

# Install pre-commit (if not already)
pip install pre-commit

# Install hooks
pre-commit install

# Test
pre-commit run --all-files
```

**Output:**
```
Scan for secrets with Gitleaks...............................Passed
Detect private keys..........................................Passed
Check for merge conflicts....................................Passed
```

### Phase 7: Report Completion

**Coder agent final report:**
```
IMPLEMENTATION COMPLETE

Task: Create API configuration module

Files Created:
- src/config.py (32 lines)
- .env (3 lines, gitignored)
- .env.example (3 lines)

Files Modified:
- .gitignore (added .env)
- .pre-commit-config.yaml (added security hooks)

Implementation Summary:
- Created centralized API client configuration
- Environment variable loading with validation
- Secure secret management via .env
- Pre-commit hooks installed

Security QA:
- ✅ Security scan passed (0 secrets detected)
- ✅ All secrets moved to .env
- ✅ .env properly gitignored
- ✅ Pre-commit hook installed and tested
- ✅ .env.example template created

Basic Verification:
- ✅ Code runs without errors
- ✅ Environment variables load correctly
- ✅ All imports resolve
- ✅ Matches specification

Ready for testing phase.
```

---

## Key Takeaways

1. **Security scan is mandatory** - Never skip, even if "just testing"
2. **Stop immediately on failure** - Don't proceed with secrets present
3. **Invoke @stuck when blocked** - Get human guidance for remediation
4. **Re-scan after fixes** - Verify remediation was successful
5. **Install pre-commit hooks** - Prevent future secret commits
6. **Document security work** - Include in completion report

---

## Common Variations

### Variation 1: False Positive

```
Coder: Security scan flagged docs/api-examples.md:45
Coder: This is an example key marked with "YOUR-KEY-HERE"
Coder: Adding to .gitleaksignore...
```

```bash
echo "docs/api-examples.md:45  # Example key in documentation" >> .gitleaksignore
```

### Variation 2: MCP Server Config

```
Coder: Detected secret in mcp-server-config.json
Coder: This is an MCP server configuration file
Coder: Verifying it's in .gitignore...
```

```bash
grep -q "mcp-server-config.json" .gitignore || echo "mcp-server-config.json" >> .gitignore
```

### Variation 3: Already Using .env

```
Coder: Security scan passed ✅
Coder: Project already uses .env pattern correctly
Coder: Verifying pre-commit hook installed...
Coder: Hook installed. Proceeding to report completion.
```

---

## Anti-Patterns (What NOT to Do)

### ❌ BAD: Skip Security Scan

```
Coder: Implementation complete. Reporting to team-lead...
[NO SECURITY SCAN - WRONG!]
```

### ❌ BAD: Proceed with Secrets

```
Coder: Security scan found 2 secrets.
Coder: They're probably fine. Reporting completion...
[NEVER DO THIS]
```

### ❌ BAD: Manual Bypass Without @stuck

```
Coder: Security scan failed. Adding all files to .gitleaksignore...
[Don't blindly allowlist - verify first via @stuck]
```

### ✅ GOOD: Proper Workflow

```
Coder: Implementation complete. Running security scan...
Coder: [runs scan]
Coder: Security scan passed ✅
Coder: Installing pre-commit hook...
Coder: Ready to report completion.
```

---

## Integration with Team Workflow

```
Team-Lead: Invoking coder agent for Task #3

Coder: Received task specification. Starting implementation...
Coder: [implements code]
Coder: Implementation complete. Running security scan...
Coder: Security scan passed ✅
Coder: Reporting completion to team-lead.

Team-Lead: Coder complete. Invoking tester agent...
```

**Security scan happens automatically as part of coder's QA - no special invocation needed.**

---

## Summary

Security scanning is **mandatory, automatic, and non-negotiable** in the coder agent workflow. It's not a separate step - it's part of implementation completion. No code proceeds without passing security scan. Period. 🔒
