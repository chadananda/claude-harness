# Subagent Best Practices

## Production-Ready Patterns

### 1. Start Simple, Iterate

**Don't:**
```yaml
# Creating a complex agent on first try
---
name: super-mega-agent
description: Does everything for all languages with all tools
tools: Read, Write, Edit, Bash, Grep, Glob, WebFetch, WebSearch, Task
model: opus
---

[10 pages of system prompt...]
```

**Do:**
```yaml
# Start with minimal viable agent
---
name: python-reviewer
description: Reviews Python code for common issues
tools: Read, Grep, Glob
---

Reviews Python code for:
- Common bugs
- Style issues
- Simple improvements

Returns markdown report with findings.
```

**Then iterate** based on real usage.

### 2. Single Responsibility Principle

**Don't:**
```yaml
---
name: do-everything
description: Reviews, tests, deploys, and documents code
---
```

**Do:**
```yaml
# Agent 1
---
name: code-reviewer
description: Reviews code quality
---

# Agent 2
---
name: test-creator
description: Generates tests
---

# Agent 3
---
name: deployer
description: Handles deployment
---
```

**Benefit:** Focused, reusable, maintainable

### 3. Clear, Testable Descriptions

**Don't:**
```yaml
description: Helps with stuff
```

**Do:**
```yaml
description: Reviews TypeScript code for type safety issues, strict mode violations, and typing best practices. Use when analyzing TypeScript type correctness.
```

**Test your description:**
- Does it clearly state what the agent does?
- Does it include trigger keywords?
- Would a human know when to invoke it?

### 4. Explicit Output Formats

**Don't:**
```markdown
Provide analysis results.
```

**Do:**
```markdown
## Output Format

\`\`\`markdown
# Analysis Report

## Summary
- Total issues: X
- Critical: Y
- High: Z

## Findings
### [Issue Title]
- **File:** path/to/file:line
- **Severity:** Critical
- **Description:** ...
- **Recommendation:** ...
\`\`\`
```

### 5. Measurable Success Criteria

**Don't:**
```markdown
Do a good job analyzing the code.
```

**Do:**
```markdown
## Success Criteria

- All critical issues identified (100% recall)
- Each finding includes file:line reference
- False positive rate < 10%
- Analysis completes in < 5 minutes
- Recommendations are specific and actionable
```

## Naming Conventions

### File Naming

**Pattern:** `{domain}-{task}.md`

**Examples:**
```
# Good
security-reviewer.md
python-test-generator.md
react-component-creator.md
database-optimizer.md

# Avoid
agent.md
helper.md
my-agent.md
thing1.md
```

### Agent Names in YAML

**Use kebab-case:**
```yaml
name: security-reviewer      # ✅ Good
name: SecurityReviewer       # ❌ Bad
name: security_reviewer      # ❌ Bad
name: security reviewer      # ❌ Bad
```

## Version Control

### Project Agents (.claude/agents/)

**Do commit:**
```bash
git add .claude/agents/
git commit -m "Add security-reviewer agent"
```

**Benefits:**
- Team shares agents
- Version tracked
- Reviewed in PRs

### User Agents (~/.claude/agents/)

**Don't commit:**
- These are personal
- Not in project repo
- User-specific

## Documentation

### Self-Documenting Prompts

**Include comments in system prompt:**

```markdown
---
name: test-generator
description: ...
tools: Read, Write, Bash  # Bash needed for pytest execution
model: sonnet  # Haiku insufficient for test design
---

# Test Generation Specialist

You create comprehensive test suites.

## Approach

1. **Analyze Code Structure**
   # This step identifies testable units
   - Find functions and classes
   - Map dependencies

2. **Identify Scenarios**
   # Critical: Don't just test happy path
   - Happy path (expected usage)
   - Edge cases (boundaries)
   - Error cases (failures)
```

### README for Agent Collections

If you have many agents, create documentation:

**`.claude/agents/README.md`:**
```markdown
# Project Subagents

## Available Agents

### security-reviewer
Reviews code for security vulnerabilities.

**Invoke:** "Review this code for security issues"
**Tools:** Read, Grep, Glob
**Model:** Sonnet

### test-creator
Generates comprehensive test suites.

**Invoke:** "Create tests for this module"
**Tools:** Read, Write, Bash
**Model:** Sonnet

## Usage

Agents activate automatically when Claude recognizes matching tasks.

You can also invoke explicitly:
- "Use the security-reviewer to analyze auth.py"
- "Invoke test-creator for the user module"
```

## Testing Strategies

### 1. Unit Testing Agents

Test with specific, isolated tasks:

```
Test: "Review this simple function for issues"

Expected: Agent activates, provides specific feedback

Verify:
- Correct agent invoked
- Output matches format
- Findings are accurate
- Performance acceptable
```

### 2. Integration Testing

Test in realistic workflows:

```
Workflow: Feature Development
1. Create code
2. Invoke test-creator
3. Invoke code-reviewer
4. Invoke security-reviewer

Verify:
- All agents work together
- No conflicts
- Complete coverage
```

### 3. Edge Case Testing

```
Test: Empty codebase
Test: Extremely large files
Test: Non-standard structure
Test: Missing dependencies

Verify: Graceful handling
```

## Performance Optimization

### 1. Choose Appropriate Model

```yaml
# Formatting (deterministic)
model: haiku  # Fast, cheap

# Code review (analysis)
model: sonnet  # Default, balanced

# Architecture (complex)
model: opus  # Deep reasoning
```

### 2. Limit Tool Access

```yaml
# Analysis agent doesn't need write access
tools: Read, Grep, Glob  # Not Write, Edit, Bash
```

**Benefits:**
- Faster tool selection
- Reduced decision overhead
- Better security

### 3. Scope Appropriately

**Don't:**
```yaml
description: General-purpose code helper for all languages and all tasks
```

**Do:**
```yaml
description: Reviews Python code for security vulnerabilities
```

**Focused agents activate faster and perform better.**

## Security Hardening

### 1. Least Privilege

```yaml
# ❌ Too broad
tools: *

# ✅ Minimal
tools: Read, Grep, Glob
```

### 2. Read-Only When Possible

```yaml
# For analysis/review agents
tools: Read, Grep, Glob  # No modification capability
```

### 3. Bash with Caution

```yaml
# Only when absolutely necessary
tools: Read, Bash  # Document why Bash is needed
```

**In system prompt:**
```markdown
## Bash Usage

Only use Bash for:
- Running pytest tests
- Checking installed dependencies

Never use Bash for:
- File manipulation (use Write/Edit instead)
- Destructive operations
```

### 4. Validate Inputs

**In system prompt:**
```markdown
## Input Validation

Before executing commands:
1. Verify paths are within project
2. Check file extensions match expected types
3. Sanitize any user-provided values
```

## Error Handling

### 1. Graceful Degradation

**In system prompt:**
```markdown
## Error Handling

If you encounter:
- **Missing files:** Report what's missing, suggest resolution
- **Tool errors:** Explain error, provide workaround if possible
- **Ambiguous requirements:** Ask clarifying questions
- **Insufficient permissions:** Explain what permission is needed
```

### 2. Clear Error Messages

**Don't:**
```markdown
Output: "Error occurred"
```

**Do:**
```markdown
Output:
"Error: Cannot read file `config.json`
Reason: File not found in project root
Solution: Create config.json or specify path with --config flag"
```

## Maintenance

### 1. Regular Review

**Monthly or quarterly:**
- Are agents still relevant?
- Can descriptions be improved?
- Are tools still minimal?
- Is performance acceptable?
- Are outputs still useful?

### 2. Version Tracking

**In system prompt comments:**
```markdown
---
name: security-reviewer
# Updated: 2025-01-15
# Changes: Added CVE checking, improved OWASP coverage
---
```

### 3. Deprecation Strategy

**For outdated agents:**

```markdown
---
name: old-agent
description: [DEPRECATED] Use new-agent instead. This agent will be removed in v2.0.
---

⚠️ This agent is deprecated. Use `new-agent` instead.

[Keep minimal functionality for transition period]
```

## Team Collaboration

### 1. Shared Conventions

**Team should agree on:**
- Naming patterns
- Tool permission policies
- Output format standards
- Documentation requirements

### 2. Code Review for Agents

**Review new agents like code:**
- Is description clear?
- Are tools minimal?
- Is model appropriate?
- Is output format specified?
- Are there tests?

### 3. Shared Agent Library

**Organize project agents:**
```
.claude/agents/
├── README.md           # Documentation
├── security/
│   ├── security-reviewer.md
│   └── dependency-auditor.md
├── testing/
│   ├── test-creator.md
│   └── test-runner.md
└── quality/
    ├── code-reviewer.md
    └── performance-analyzer.md
```

## Monitoring and Metrics

### Track Agent Usage

**Questions to answer:**
- Which agents are most used?
- Which are never used?
- What's the success rate?
- What's the average execution time?

### Collect Feedback

**From team:**
- Is output format helpful?
- Are findings accurate?
- Any false positives?
- Missing capabilities?

### Iterate Based on Data

**If agent is never used:**
- Description might be unclear
- Scope might be too narrow/broad
- Might not be needed

**If agent has low satisfaction:**
- Output might not be useful
- Too many false positives
- Missing key checks

## Common Pitfalls

### 1. Over-Engineering

❌ Creating 50 highly specialized agents
✅ Start with 5-10 core agents, add as needed

### 2. Under-Documenting

❌ No description of when to use
✅ Clear descriptions, examples, documentation

### 3. Tool Bloat

❌ Giving all agents all tools
✅ Minimal tools per agent

### 4. No Testing

❌ Deploy agents without testing
✅ Test with real scenarios before sharing

### 5. Abandoned Agents

❌ Create agent, never maintain
✅ Regular review and updates

## Success Patterns

### Pattern 1: Progressive Enhancement

**Start:**
```yaml
# v1: Basic
---
name: code-reviewer
description: Reviews code for issues
tools: Read, Grep, Glob
---

Basic code review checking common issues.
```

**Enhance:**
```yaml
# v2: Improved
---
name: code-reviewer
description: Reviews code for bugs, performance issues, and best practices violations
tools: Read, Grep, Glob
---

Comprehensive code review with categorized findings and specific recommendations.
```

### Pattern 2: Composition Over Complexity

**Instead of one mega-agent:**
```yaml
# ❌ One agent doing everything
---
name: full-pipeline
description: Does review, test, security, deploy
---
```

**Use multiple focused agents:**
```yaml
# ✅ Focused agents
# code-reviewer.md
# test-creator.md
# security-scanner.md
# deployer.md

# Orchestrator invokes them in sequence
```

### Pattern 3: Template + Specialization

**Base template:**
```yaml
---
name: base-reviewer
description: Generic code reviewer
---

Generic review methodology
```

**Specialized variants:**
```yaml
---
name: python-reviewer
description: Reviews Python code specifically
---

Python-specific checks (PEP 8, typing, etc.)
```

## Next Steps

- [Examples](examples.md) - Real-world subagent templates following these practices
- [Tool Permissions](tool_permissions.md) - Security and tool selection
- [Activation Patterns](activation_patterns.md) - Writing effective descriptions
