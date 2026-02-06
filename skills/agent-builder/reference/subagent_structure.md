# Subagent Structure Reference

## File Format

Subagents are Markdown files with YAML frontmatter stored in:
- **Project:** `.claude/agents/your-agent.md`
- **User:** `~/.claude/agents/your-agent.md`

## Complete Structure

```markdown
---
name: your-agent-name
description: Clear description of when and why to use this agent
tools: Tool1, Tool2, Tool3
model: sonnet
---

System prompt content explaining the agent's role, approach, and expectations.

## Optional Sections

You can structure the system prompt with markdown sections for clarity.
```

## YAML Frontmatter Reference

### Required Fields

#### `name` (required)
**Format:** kebab-case, lowercase letters, numbers, and hyphens only

**Purpose:** Unique identifier for the subagent

**Rules:**
- ✅ Use descriptive, clear names
- ✅ kebab-case: `security-reviewer`, `test-creator`
- ❌ No spaces: `security reviewer`
- ❌ No uppercase: `SecurityReviewer`
- ❌ No underscores: `security_reviewer` (use hyphens)

**Examples:**
```yaml
name: code-reviewer          # Good
name: security-auditor       # Good
name: react-specialist       # Good
name: CodeReviewer          # Bad - uppercase
name: code_reviewer         # Bad - underscore
name: code reviewer         # Bad - space
```

#### `description` (required)
**Format:** Clear, concise text (1-3 sentences)

**Purpose:** Triggers automatic activation when task matches

**Rules:**
- ✅ Start with what the agent does
- ✅ Include trigger keywords
- ✅ Mention domain/tech stack if relevant
- ✅ Specify "Use when..." for clarity
- ❌ Don't be vague or generic
- ❌ Don't use just a single word

**Examples:**
```yaml
# Good - specific, clear triggers
description: Reviews code for security vulnerabilities, OWASP Top 10 issues, and secure coding practices. Use when analyzing security risks in code.

# Good - includes tech stack and use case
description: Creates comprehensive test suites using Playwright for web applications. Use when testing frontend functionality, visual regressions, or user interactions.

# Good - specifies domain and methodology
description: Analyzes React components for performance issues, re-render problems, and optimization opportunities. Use when optimizing React application performance.

# Bad - too vague
description: Helps with testing

# Bad - too generic
description: Reviews code

# Bad - missing context
description: Use for Python
```

### Optional Fields

#### `tools` (optional)
**Format:** Comma-separated list of tool names

**Purpose:** Restricts which tools the subagent can use

**Default:** If not specified, subagent has access to all tools

**Security Note:** Always specify tools for least-privilege security

**Available Tools:**
- **File Operations:** `Read`, `Write`, `Edit`, `Glob`
- **Search:** `Grep`
- **Execution:** `Bash`, `BashOutput`, `KillShell`
- **Web:** `WebFetch`, `WebSearch`
- **Delegation:** `Task`
- **Notebooks:** `NotebookEdit`
- **Documentation:** `ListMcpResourcesTool`, `ReadMcpResourceTool`
- **Interaction:** `AskUserQuestion`

**Common Tool Sets:**

```yaml
# Read-only research agent
tools: Read, Grep, Glob, WebFetch

# Code generation agent
tools: Read, Write, Edit, Grep, Glob

# Test execution agent
tools: Read, Write, Bash

# Review agent (analysis only)
tools: Read, Grep, Glob

# Full-stack development agent
tools: Read, Write, Edit, Grep, Glob, Bash

# Research with web access
tools: Read, Grep, Glob, WebFetch, WebSearch

# Multi-agent orchestrator
tools: Task, Read, Grep, Glob
```

**Security Guidelines:**

```yaml
# ⚠️ DANGEROUS - Unrestricted access
# tools: *  # DON'T DO THIS

# ⚠️ HIGH RISK - Can modify and execute
tools: Write, Edit, Bash

# ✅ SAFE - Read-only operations
tools: Read, Grep, Glob

# ✅ CONTROLLED - Generation without execution
tools: Read, Write, Grep, Glob

# ✅ MINIMAL - Single purpose
tools: Read  # Only needs to read files
```

#### `model` (optional)
**Format:** `haiku`, `sonnet`, or `opus`

**Purpose:** Selects which Claude model powers the subagent

**Default:** `sonnet` (if not specified)

**When to Use Each:**

```yaml
# Haiku - Fast & Cheap
model: haiku
# Use for:
# - Simple transformations
# - Template filling
# - Deterministic tasks
# - High-volume operations
# - Quick analysis

# Sonnet - Balanced (DEFAULT)
model: sonnet
# Use for:
# - Most workflows
# - Code generation
# - Complex analysis
# - Recommended default
# - Best balance of speed/quality

# Opus - Highest Reasoning
model: opus
# Use for:
# - Novel problem-solving
# - Architecture design
# - Complex decision-making
# - Highest quality needs
# - Use sparingly (expensive)
```

**Cost Considerations:**

```
Haiku   < Sonnet   < Opus
 $        $$        $$$$
Fast     Medium    Slower
```

## System Prompt Structure

The content after the frontmatter is the system prompt. This defines the agent's behavior.

### Recommended System Prompt Structure

```markdown
---
name: your-agent
description: What the agent does and when to use it
tools: Tool1, Tool2
model: sonnet
---

# Primary Role
[One sentence defining who this agent is]

## Responsibilities
[Bullet list of what this agent does]

## Methodology
[Step-by-step approach the agent should follow]

## Output Format
[Specify exactly what format to return]

## Success Criteria
[What defines a successful execution]

## Guidelines
[Dos and don'ts, constraints, considerations]

## Examples (optional)
[Example scenarios and expected outputs]
```

### Minimal System Prompt

```markdown
---
name: simple-agent
description: Does a specific task clearly defined here
---

You are [role description].

When invoked, you [specific task methodology].

Return results as [output format specification].
```

### Complex System Prompt Example

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities, OWASP Top 10 issues, and secure coding practices. Use when analyzing security risks in code.
tools: Read, Grep, Glob
model: sonnet
---

# Security Review Specialist

You are a security review expert specializing in identifying vulnerabilities and security risks in code.

## Your Responsibilities

Analyze code for:
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- CSRF (Cross-Site Request Forgery) issues
- Authentication and authorization flaws
- Insecure deserialization
- Security misconfigurations
- Sensitive data exposure
- Insufficient logging
- Vulnerable dependencies
- Hardcoded secrets or credentials

## Review Methodology

1. **Initial Scan**
   - Use Grep to search for common vulnerability patterns
   - Identify authentication and authorization code
   - Locate database queries and API calls

2. **Deep Analysis**
   - Review input validation and sanitization
   - Analyze authentication flows
   - Check authorization boundaries
   - Examine cryptographic implementations

3. **Dependency Check**
   - Review package.json, requirements.txt, go.mod, etc.
   - Flag outdated or vulnerable dependencies

4. **Secret Detection**
   - Search for API keys, passwords, tokens in code
   - Check environment variable handling

5. **Risk Assessment**
   - Categorize findings by severity
   - Provide exploitability context

## Output Format

Provide a structured markdown report:

\`\`\`markdown
# Security Review Report

## Executive Summary
[Overall risk level: Critical/High/Medium/Low]
[Key findings summary]

## Critical Findings
### [Vulnerability Name]
- **File:** path/to/file.ext:lineNumber
- **Severity:** Critical
- **Description:** [What the vulnerability is]
- **Risk:** [What could happen]
- **Recommendation:** [How to fix]

## High Findings
[Same structure as Critical]

## Medium Findings
[Same structure as Critical]

## Low Findings
[Same structure as Critical]

## Positive Observations
[Security measures already in place]

## Recommendations
1. [Prioritized action items]
\`\`\`

## Success Criteria

- All critical and high-severity vulnerabilities identified
- Clear, actionable remediation steps provided
- File and line number references for each finding
- Risk context explains exploitability
- False positive rate < 10%
- Report completed within 5 minutes

## Guidelines

**Do:**
- Focus on exploitable vulnerabilities
- Provide specific file:line references
- Explain risk in business terms
- Prioritize by severity and exploitability
- Suggest concrete fixes

**Don't:**
- Report style issues (that's code-reviewer's job)
- Give vague recommendations
- Miss critical issues for minor ones
- Create false positives
- Skip dependency analysis
```

## File Naming Conventions

### Recommended Patterns

```
# Domain-specific
python-expert.md
react-specialist.md
database-optimizer.md

# Task-specific
code-reviewer.md
test-creator.md
security-auditor.md

# Workflow-specific
deploy-automation.md
ci-pipeline.md
release-manager.md

# Tech stack specific
typescript-linter.md
rust-analyzer.md
go-formatter.md
```

### Avoid

```
# Too generic
agent.md
helper.md
utils.md

# Too vague
thing.md
myagent.md
agent1.md

# Unclear purpose
test.md
review.md
check.md
```

## Complete Example Files

### Minimal Example

**.claude/agents/formatter.md:**
```markdown
---
name: formatter
description: Formats code according to project style guidelines. Use when code needs formatting or style corrections.
tools: Read, Edit, Bash
model: haiku
---

You format code according to the project's style guidelines.

1. Read the files to format
2. Detect the language and style config
3. Run appropriate formatter (prettier, black, gofmt, etc.)
4. Report files formatted

Return a list of formatted files.
```

### Medium Complexity Example

**.claude/agents/test-creator.md:**
```markdown
---
name: test-creator
description: Creates comprehensive test suites for code using appropriate testing frameworks. Use when generating unit tests, integration tests, or test coverage.
tools: Read, Write, Grep, Glob, Bash
model: sonnet
---

You are a test creation specialist that generates high-quality, comprehensive test suites.

## Approach

1. Analyze code to understand functionality
2. Identify testing framework (pytest, jest, go test, etc.)
3. Generate tests covering:
   - Happy path scenarios
   - Edge cases
   - Error handling
   - Boundary conditions
4. Ensure tests follow project conventions
5. Run tests to verify they pass

## Output

Create test files following project naming conventions:
- Python: test_*.py or *_test.py
- JavaScript: *.test.js or *.spec.js
- Go: *_test.go

Include:
- Setup and teardown when needed
- Clear test names describing what's tested
- Assertions for expected behavior
- Comments explaining complex test logic

Report:
- Files created
- Test coverage achieved
- Any tests that need manual verification
```

### Complex Example

See the security-reviewer example in the "Complex System Prompt Example" section above.

## Validation Checklist

Before finalizing your subagent, verify:

**YAML Frontmatter:**
- [ ] Name is kebab-case, lowercase, descriptive
- [ ] Description clearly states when to use
- [ ] Description includes trigger keywords
- [ ] Tools are minimal set required
- [ ] Model is appropriate for complexity

**System Prompt:**
- [ ] Role is clearly defined
- [ ] Responsibilities are listed
- [ ] Methodology is step-by-step
- [ ] Output format is specified
- [ ] Success criteria are measurable
- [ ] Guidelines include dos and don'ts

**File:**
- [ ] Saved in correct location (.claude/agents/ or ~/.claude/agents/)
- [ ] Filename matches name in frontmatter
- [ ] Markdown is properly formatted
- [ ] No syntax errors in YAML

**Testing:**
- [ ] Description triggers agent automatically
- [ ] Agent has access to required tools
- [ ] Output format matches specification
- [ ] Performance is acceptable
- [ ] Results are accurate

## Next Steps

- [Activation Patterns](activation_patterns.md) - Writing effective descriptions
- [System Prompts](system_prompts.md) - Crafting quality prompts
- [Tool Permissions](tool_permissions.md) - Security and tool selection
- [Examples](examples.md) - Real-world templates
