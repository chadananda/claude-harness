# Secret Remediation Example

Step-by-step walkthrough of fixing a leaked secret.

## Scenario: Hardcoded OpenAI API Key

Developer accidentally hardcoded an API key. Security scan detected it before commit.

---

## Step 1: Detection

**Command:**
```bash
gitleaks detect --no-git --source . --verbose --report-path report.json
```

**Output:**
```
Finding:     sk-proj-abc123...
Secret:      sk-proj-abc123def456ghi789jkl012mno345pqr678
RuleID:      openai-api-key
File:        src/api_client.py
Line:        12
```

**Code:**
```python
# src/api_client.py (BEFORE)
import openai

# Hardcoded API key (BAD!)
openai.api_key = "sk-proj-abc123def456ghi789jkl012mno345pqr678"

def generate_completion(prompt):
    response = openai.Completion.create(model="gpt-4", prompt=prompt)
    return response.choices[0].text
```

---

## Step 2: Assess Impact

**Questions:**
- Was this committed to Git? **No** (caught by pre-commit scan)
- Was it pushed to remote? **No**
- Is it in a public repo? **No**

**Conclusion:** Low risk, but still needs immediate fixing.

---

## Step 3: Create .env File

```bash
# Create .env in project root
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678
EOF
```

---

## Step 4: Update .gitignore

```bash
# Check if .env is ignored
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore

# Also ignore common variations
grep -q "^\.env\.local$" .gitignore || echo ".env.local" >> .gitignore
grep -q "^\.env\.*.local$" .gitignore || echo ".env.*.local" >> .gitignore
```

---

## Step 5: Update Code

```python
# src/api_client.py (AFTER)
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable not set. "
        "Please create a .env file with your API key."
    )

def generate_completion(prompt):
    response = openai.Completion.create(model="gpt-4", prompt=prompt)
    return response.choices[0].text
```

---

## Step 6: Create .env.example

```bash
# Create template for other developers
cat > .env.example << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=sk-YOUR-KEY-HERE

# Get your API key from: https://platform.openai.com/api-keys
EOF
```

---

## Step 7: Verify Fix

### Test Environment Loading

```bash
# Test that .env loads correctly
python3 << 'EOF'
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key and api_key.startswith("sk-proj-"):
    print("✅ API key loaded successfully")
else:
    print("❌ API key not loaded")
EOF
```

**Output:**
```
✅ API key loaded successfully
```

### Re-run Security Scan

```bash
gitleaks detect --no-git --source . --verbose
```

**Output:**
```
8:52PM INF no leaks found
```

### Check Git Status

```bash
git status
```

**Output:**
```
On branch main
Changes not staged for commit:
  modified:   src/api_client.py
  modified:   .gitignore

Untracked files:
  .env.example

(.env is NOT shown - correctly ignored!)
```

---

## Step 8: Commit the Fix

```bash
# Stage changes
git add src/api_client.py .gitignore .env.example

# Pre-commit hook runs automatically
git commit -m "fix: move API key to environment variable"
```

**Output:**
```
Scan for secrets with Gitleaks...............................Passed
Detect private keys..........................................Passed
[main abc123d] fix: move API key to environment variable
 3 files changed, 15 insertions(+), 2 deletions(-)
 create mode 100644 .env.example
```

---

## Step 9: Document in README

Update project documentation:

```markdown
# Project Setup

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file: `cp .env.example .env`
4. Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
5. Get your API key from [OpenAI Dashboard](https://platform.openai.com/api-keys)

## Security

- **Never commit `.env` files** - they contain secrets
- Use `.env.example` as a template
- Pre-commit hooks scan for leaked secrets
```

---

## Complete Before/After

### BEFORE (Insecure)

**src/api_client.py:**
```python
import openai
openai.api_key = "sk-proj-abc123def456ghi789jkl012mno345pqr678"
```

**Security scan:**
```
❌ FAILED - 1 secret detected
```

### AFTER (Secure)

**.env (gitignored):**
```
OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678
```

**.gitignore:**
```
.env
.env.local
```

**src/api_client.py:**
```python
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
```

**.env.example (committed):**
```
OPENAI_API_KEY=sk-YOUR-KEY-HERE
```

**Security scan:**
```
✅ PASSED - 0 secrets detected
```

---

## Time Required

- **Detection:** < 1 second (automated scan)
- **Remediation:** 2-3 minutes
  - Create .env: 30 seconds
  - Update .gitignore: 15 seconds
  - Modify code: 1 minute
  - Create .env.example: 30 seconds
  - Verify: 30 seconds
- **Documentation:** 5 minutes (README update)

**Total:** ~10 minutes for complete remediation

---

## Key Lessons

1. **Pre-commit hooks catch secrets early** - Before they reach remote
2. **Remediation is simple** - Move to .env, load from environment
3. **.env must be gitignored** - Verify it's never committed
4. **.env.example helps teammates** - Template for required variables
5. **Test after fixing** - Re-scan and verify environment loading
6. **Document for team** - Update README with setup instructions

---

## What If Secret Was Already Committed?

### Additional Steps Required:

1. **Rotate key immediately** (assume compromised)
   ```
   - Go to OpenAI Dashboard
   - Delete leaked key
   - Create new key
   - Update .env with new key
   ```

2. **Remove from Git history** (optional, complex)
   ```bash
   # Use BFG Repo-Cleaner
   bfg --replace-text passwords.txt
   git push --force
   ```

3. **Notify team** if in shared repository

4. **Monitor for unauthorized usage** in service dashboard

**Prevention is easier than cleanup!** Use pre-commit hooks to catch secrets before they're committed.
