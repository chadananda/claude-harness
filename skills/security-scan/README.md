# Security Scan Skill

Detect and prevent API keys, tokens, and secrets from being committed to Git repositories.

## What This Skill Provides

Fast, automated secret detection using Gitleaks with pre-commit hook enforcement. **Mandatory QA step for coder agents** before implementation completion.

## Quick Start

```bash
# Install Gitleaks
brew install gitleaks

# Install pre-commit
pip install pre-commit

# Run scan
gitleaks detect --no-git --source . --verbose

# Install pre-commit hook
cp ~/.claude/skills/security-scan/templates/pre-commit-config.yaml ./.pre-commit-config.yaml
pre-commit install
```

## What Gets Detected

- **API Keys:** OpenAI, AWS, Stripe, GitHub, Slack, etc.
- **Database Credentials:** PostgreSQL, MongoDB, MySQL connection strings
- **Authentication Tokens:** JWT, OAuth, Bearer tokens
- **Private Keys:** RSA, EC, OpenSSH, PGP
- **800+ secret patterns** via Gitleaks built-in rules

## Use Cases

### 1. Coder Agent QA (Primary)

Coder agent automatically runs security scan before reporting completion:

```
1. Implement code
2. Test implementation
3. **Run security scan** ← Mandatory
4. If clean → Report completion
5. If secrets found → Invoke @stuck, remediate
```

### 2. Manual Security Audit

Developer or security team runs manual scan:

```bash
gitleaks detect --no-git --source . --report-path report.json --verbose
```

### 3. Pre-commit Hook (Automatic)

Blocks commits containing secrets:

```bash
git commit -m "add feature"
# Pre-commit hook runs automatically
# Blocks if secrets detected
```

## File Structure

```
security-scan/
├── SKILL.md                          # Main guide
├── README.md                         # This file
├── LICENSE.txt                       # MIT license
├── reference/
│   ├── gitleaks-guide.md            # CLI reference
│   ├── secret-patterns.md           # All detectable patterns
│   ├── false-positives.md           # Managing allowlists
│   └── remediation.md               # Fixing leaked secrets
├── templates/
│   ├── gitleaks.toml                # Custom configuration
│   ├── gitleaksignore.template      # False positive patterns
│   └── pre-commit-config.yaml       # Pre-commit hook
└── examples/
    ├── coder-workflow-example.md    # Complete coder workflow
    └── remediation-example.md       # Step-by-step fix guide
```

## Key Features

✅ **Fast** - < 1 second per scan
✅ **Comprehensive** - 800+ secret patterns
✅ **Language-agnostic** - Works with any programming language
✅ **Pre-commit hooks** - Automatic enforcement
✅ **Remediation guidance** - Step-by-step fixes
✅ **False positive management** - .gitleaksignore support
✅ **Custom patterns** - Add project-specific secrets

## Common Workflows

### Workflow 1: Clean Scan (No Secrets)

```bash
gitleaks detect --no-git --source . --verbose
# Output: No leaks detected ✅
# → Proceed with commit
```

### Workflow 2: Secrets Detected

```bash
gitleaks detect --no-git --source . --verbose
# Output: Found 2 secrets in src/config.py

# → Fix: Move to .env
# → Update code to load from environment
# → Re-scan: No leaks detected ✅
# → Proceed with commit
```

### Workflow 3: False Positive

```bash
gitleaks detect --no-git --source . --verbose
# Output: Found secret in docs/api-examples.md (example key)

# → Add to .gitleaksignore
echo "docs/api-examples.md:45  # Example key" >> .gitleaksignore

# → Re-scan: No leaks detected ✅
```

## Integration

### With Coder Agent

Automatically integrated as mandatory QA step:

```markdown
**Coder agent workflow:**
1. Implement code
2. Test basic functionality
3. **Run security scan** ← Automatic
4. If secrets found → Invoke @stuck
5. Report completion
```

See: `examples/coder-workflow-example.md`

### With Pre-commit

```bash
# Copy template
cp ~/.claude/skills/security-scan/templates/pre-commit-config.yaml ./.pre-commit-config.yaml

# Install
pre-commit install

# Test
pre-commit run --all-files
```

### With CI/CD

```yaml
# GitHub Actions
- name: Gitleaks
  uses: gitleaks/gitleaks-action@v2
```

## What Gets Scanned

### Included (All committable files)
- Source code (*.py, *.js, *.go, *.rs, etc.)
- Configuration files (.env, config.yaml, etc.)
- MCP server configs (if not .gitignored)
- Documentation (*.md, README, etc.)
- Scripts (*.sh, *.ps1, etc.)
- Infrastructure as Code (Terraform, K8s, etc.)

### Excluded (Respects .gitignore)
- Dependencies (node_modules/, vendor/, .venv/)
- Build outputs (dist/, build/, target/)
- Git internals (.git/)
- Temporary files (./tmp/, *.tmp)

## Performance

- **Small projects** (< 100 files): < 1 second
- **Medium projects** (100-1000 files): 1-3 seconds
- **Large projects** (1000+ files): 3-10 seconds
- **Pre-commit** (staged files only): < 1 second

## Best Practices

1. ✅ Always use environment variables for secrets
2. ✅ Keep .env in .gitignore
3. ✅ Create .env.example templates
4. ✅ Install pre-commit hooks on all projects
5. ✅ Run full scans before major releases
6. ✅ Rotate keys if committed (assume compromised)
7. ✅ Document false positives
8. ✅ Regular security audits (monthly)

## When to Use

**Use security-scan skill when:**
- Implementing new features (coder agent QA)
- Before committing code (pre-commit hook)
- During code review (manual audit)
- Onboarding new team members (project setup)
- Security audits (periodic scans)
- Suspected secret leaks (incident response)

## Common Secret Types

### API Keys
- OpenAI: `sk-proj-...`, `sk-...`
- AWS: `AKIA...`, `ASIA...`
- Stripe: `sk_live_...`, `sk_test_...`
- GitHub: `ghp_...`, `gho_...`, `github_pat_...`

### Database Credentials
- PostgreSQL: `postgresql://user:pass@host/db`
- MongoDB: `mongodb://user:pass@host/db`
- MySQL: `mysql://user:pass@host/db`

### Authentication
- JWT tokens: `ey...ey...`
- OAuth tokens: `Bearer ...`
- Private keys: `-----BEGIN PRIVATE KEY-----`

See: `reference/secret-patterns.md` for complete list

## Troubleshooting

### "gitleaks command not found"

```bash
brew install gitleaks
```

### "Too many false positives"

```bash
# Create .gitleaksignore
echo "docs/**/*.md" >> .gitleaksignore
echo "tests/**/*" >> .gitleaksignore
```

### "Need to bypass pre-commit"

```bash
# Emergency only
git commit --no-verify -m "Emergency fix"

# Then immediately fix and re-commit properly
```

## Resources

- **Main Guide:** `SKILL.md`
- **CLI Reference:** `reference/gitleaks-guide.md`
- **Secret Patterns:** `reference/secret-patterns.md`
- **Remediation Guide:** `reference/remediation.md`
- **Coder Workflow:** `examples/coder-workflow-example.md`

## Support

**For help:**
1. Read `SKILL.md` - Comprehensive guide
2. Check `reference/troubleshooting.md` - Common issues
3. Review examples in `examples/` - Walkthrough scenarios
4. Consult Gitleaks docs - https://github.com/gitleaks/gitleaks

## License

MIT License - See LICENSE.txt

---

**For coder agents:** This is mandatory QA. No exceptions. No shortcuts. Security is non-negotiable. 🔒
