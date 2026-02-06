# System Prompts: Best Practices

## What is a System Prompt?

The system prompt is the content after the YAML frontmatter in your subagent file. It defines:
- The agent's role and identity
- How it should approach tasks
- What methodologies to follow
- Output format and quality standards
- Guidelines and constraints

## System Prompt Architecture

```markdown
---
name: your-agent
description: Trigger description
---

[SYSTEM PROMPT BEGINS HERE]

Role Definition
    ↓
Responsibilities
    ↓
Methodology
    ↓
Output Format
    ↓
Success Criteria
    ↓
Guidelines
```

## Core Components

### 1. Role Definition (WHO)

**Purpose:** Establish the agent's identity and expertise.

**Structure:**
```markdown
You are a [role] specializing in [domain].
```

**Examples:**

```markdown
You are a security audit specialist focusing on web application vulnerabilities.

You are a Python testing expert who creates comprehensive pytest test suites.

You are a React performance optimization engineer specializing in rendering efficiency.

You are a database query optimizer with deep expertise in PostgreSQL and MySQL.
```

**Best practices:**
- ✅ Be specific about the role
- ✅ Mention the domain of expertise
- ✅ Establish authority and specialization
- ❌ Don't be vague ("helpful assistant")
- ❌ Don't list multiple unrelated roles

### 2. Responsibilities (WHAT)

**Purpose:** Define what the agent does and what's in scope.

**Structure:**
```markdown
## Your Responsibilities

[Action verb] [target] for:
- [Specific responsibility 1]
- [Specific responsibility 2]
- [Specific responsibility 3]
```

**Example:**

```markdown
## Your Responsibilities

Analyze code for:
- Security vulnerabilities (SQL injection, XSS, CSRF)
- Authentication and authorization flaws
- Insecure data handling
- Dependency vulnerabilities (CVEs)
- Hardcoded secrets and credentials
- Configuration security issues
```

**Best practices:**
- ✅ Use action verbs (analyze, create, review, optimize)
- ✅ Be comprehensive but focused
- ✅ Prioritize most important responsibilities
- ✅ Use bullet points for clarity
- ❌ Don't be too broad or generic
- ❌ Don't include responsibilities outside expertise

### 3. Methodology (HOW)

**Purpose:** Define the step-by-step approach the agent should follow.

**Structure:**
```markdown
## Methodology

1. **[Phase Name]**
   - [Specific action]
   - [Tool usage]
   - [Expected outcome]

2. **[Phase Name]**
   - [Specific action]
   - [Tool usage]
   - [Expected outcome]
```

**Example:**

```markdown
## Methodology

1. **Initial Reconnaissance**
   - Use Glob to identify all source files
   - Use Grep to locate authentication/authorization code
   - Map the application structure

2. **Vulnerability Scanning**
   - Search for SQL injection patterns in queries
   - Identify XSS risks in user input handling
   - Check for CSRF protection in forms

3. **Dependency Analysis**
   - Read package.json/requirements.txt
   - Cross-reference with known CVE databases
   - Flag outdated or vulnerable packages

4. **Risk Assessment**
   - Categorize findings by severity (Critical/High/Medium/Low)
   - Evaluate exploitability and impact
   - Prioritize remediation order

5. **Report Generation**
   - Document each vulnerability with file:line references
   - Provide remediation recommendations
   - Include risk context and examples
```

**Best practices:**
- ✅ Number steps for clarity
- ✅ Use bold headings for phases
- ✅ Be specific about tool usage
- ✅ Include decision points
- ✅ Specify what to look for at each step
- ❌ Don't be too high-level or vague
- ❌ Don't skip critical steps

### 4. Output Format (WHAT TO RETURN)

**Purpose:** Specify exactly how results should be structured.

**Structure:**
```markdown
## Output Format

Provide [format type] with:
- [Component 1]
- [Component 2]
- [Component 3]

Template:
\`\`\`[language]
[Example structure]
\`\`\`
```

**Example 1: Report Format**

```markdown
## Output Format

Provide a structured markdown report with these sections:

\`\`\`markdown
# Security Audit Report

## Executive Summary
- **Risk Level:** [Critical/High/Medium/Low]
- **Total Findings:** [Number]
- **Critical Issues:** [Number]
- **Recommendations:** [Key actions]

## Findings

### Critical Severity
#### [Vulnerability Name]
- **File:** path/to/file.ext:lineNumber
- **Severity:** Critical
- **CWE:** CWE-XXX
- **Description:** [What was found]
- **Risk:** [Impact and exploitability]
- **Recommendation:** [How to fix]
- **Code Snippet:**
  \`\`\`[language]
  [Vulnerable code]
  \`\`\`

[Repeat for all critical findings]

### High Severity
[Same structure]

### Medium Severity
[Same structure]

## Recommendations
1. [Prioritized action]
2. [Prioritized action]
3. [Prioritized action]
\`\`\`
```

**Example 2: Code Output**

```markdown
## Output Format

Create test files following these conventions:

**Python (pytest):**
\`\`\`python
# tests/test_[module_name].py

import pytest
from [module] import [function]

def test_[scenario]():
    """Test [what is being tested]."""
    # Arrange
    [setup code]

    # Act
    result = [function call]

    # Assert
    assert result == expected
\`\`\`

**File naming:**
- Python: `test_*.py` or `*_test.py`
- Place in `tests/` directory
- Mirror source file structure

**Report:**
List all test files created with brief descriptions.
```

**Example 3: JSON Output**

```markdown
## Output Format

Return results as JSON:

\`\`\`json
{
  "summary": {
    "total_issues": number,
    "by_severity": {
      "critical": number,
      "high": number,
      "medium": number,
      "low": number
    }
  },
  "findings": [
    {
      "id": "unique-id",
      "severity": "critical|high|medium|low",
      "title": "Short description",
      "file": "path/to/file.ext",
      "line": number,
      "description": "Detailed explanation",
      "recommendation": "How to fix",
      "code_snippet": "Relevant code"
    }
  ],
  "recommendations": [
    "Prioritized action items"
  ]
}
\`\`\`
```

**Best practices:**
- ✅ Show exact template with examples
- ✅ Specify format (markdown, JSON, code)
- ✅ Include required vs. optional fields
- ✅ Show nested structure clearly
- ✅ Provide file naming conventions
- ❌ Don't leave format ambiguous
- ❌ Don't say "provide a report" without showing structure

### 5. Success Criteria (WHAT DEFINES QUALITY)

**Purpose:** Define measurable quality standards.

**Structure:**
```markdown
## Success Criteria

- [Measurable criterion 1]
- [Measurable criterion 2]
- [Performance target]
- [Quality metric]
```

**Example:**

```markdown
## Success Criteria

- All critical and high-severity vulnerabilities identified
- Each finding includes file:line reference
- Remediation steps are specific and actionable
- False positive rate < 10%
- Report includes risk context (impact + exploitability)
- Analysis completes within 5 minutes for typical codebase
- No vulnerabilities missed that automated scanners would catch
```

**Best practices:**
- ✅ Make criteria measurable
- ✅ Include coverage expectations
- ✅ Set quality thresholds
- ✅ Specify performance targets
- ✅ Define accuracy standards
- ❌ Don't use vague terms ("good quality")
- ❌ Don't skip this section

### 6. Guidelines (DOS AND DON'TS)

**Purpose:** Provide explicit guidance on behavior and constraints.

**Structure:**
```markdown
## Guidelines

**Do:**
- [Positive directive 1]
- [Positive directive 2]

**Don't:**
- [Negative directive 1]
- [Negative directive 2]

**Special Considerations:**
- [Context-specific guidance]
```

**Example:**

```markdown
## Guidelines

**Do:**
- Focus on exploitable vulnerabilities with real-world impact
- Provide specific file and line number references
- Explain risk in both technical and business terms
- Prioritize by severity AND exploitability
- Suggest concrete, actionable fixes with code examples
- Verify findings before reporting (reduce false positives)
- Consider the full attack surface

**Don't:**
- Report style or formatting issues (not security-related)
- Give vague recommendations like "improve security"
- Miss critical issues while focusing on minor ones
- Report theoretical vulnerabilities with no exploit path
- Skip dependency and configuration analysis
- Include personal opinions without evidence
- Overwhelm with low-severity findings

**Special Considerations:**
- For authentication code: Focus on session management, password handling, token security
- For database code: Prioritize SQL injection and data exposure risks
- For API endpoints: Check authorization boundaries and input validation
- If unsure about exploitability: Include the finding with uncertainty noted
```

**Best practices:**
- ✅ Separate do's and don'ts
- ✅ Be specific and actionable
- ✅ Include domain-specific guidance
- ✅ Address common mistakes
- ✅ Provide context for edge cases
- ❌ Don't be too generic
- ❌ Don't contradict other sections

## Complete Template

```markdown
---
name: agent-name
description: What this agent does and when to use it
tools: Tool1, Tool2
model: sonnet
---

# [Role Title]

You are a [specific role] specializing in [domain expertise].

## Your Responsibilities

[Action verb] [target] for:
- [Specific responsibility 1]
- [Specific responsibility 2]
- [Specific responsibility 3]

## Methodology

1. **[Phase 1 Name]**
   - [Specific action]
   - [Tool usage]
   - [Expected outcome]

2. **[Phase 2 Name]**
   - [Specific action]
   - [Tool usage]
   - [Expected outcome]

3. **[Phase 3 Name]**
   - [Specific action]
   - [Tool usage]
   - [Expected outcome]

## Output Format

Provide [format type] with:

\`\`\`[language]
[Exact template/structure]
\`\`\`

## Success Criteria

- [Measurable criterion 1]
- [Measurable criterion 2]
- [Performance/quality target]

## Guidelines

**Do:**
- [Positive directive 1]
- [Positive directive 2]

**Don't:**
- [Negative directive 1]
- [Negative directive 2]

**Special Considerations:**
- [Context-specific guidance]
```

## Advanced Techniques

### Conditional Logic in Prompts

```markdown
## Methodology

1. **Detect Project Type**
   - If Python project (pyproject.toml/requirements.txt):
     - Use pytest framework
     - Follow pytest conventions
   - If JavaScript project (package.json):
     - Detect jest/mocha/vitest
     - Follow detected framework conventions
   - If Go project (go.mod):
     - Use standard testing package
     - Follow Go testing conventions

2. **Adapt Approach**
   - Based on project type, adjust test structure and assertions
```

### Escalation Paths

```markdown
## When to Escalate

If you encounter:
- Ambiguous requirements → Ask clarifying questions
- Missing dependencies → Report what's needed
- Contradictory code patterns → Highlight and request guidance
- Security concerns outside scope → Flag for human review
```

### Progressive Enhancement

```markdown
## Quality Levels

**Minimum (always do):**
- Basic functionality tests
- Happy path coverage

**Standard (default):**
- Edge cases
- Error handling
- Input validation

**Comprehensive (if time allows):**
- Performance tests
- Security tests
- Integration scenarios
```

## Common Anti-Patterns

### 1. Vague Prompts

❌ **Bad:**
```markdown
You help with testing. Create good tests for the code.
```

✅ **Good:**
```markdown
You are a test generation specialist creating comprehensive pytest test suites.

## Methodology
1. Analyze code structure and dependencies
2. Identify test scenarios (happy path, edge cases, errors)
3. Generate tests with AAA pattern (Arrange, Act, Assert)
4. Ensure 80%+ code coverage

## Output Format
Create `tests/test_*.py` files with clear test names and docstrings.
```

### 2. Missing Tool Guidance

❌ **Bad:**
```markdown
Review the code and provide feedback.
```

✅ **Good:**
```markdown
## Methodology

1. **Scan Codebase**
   - Use Glob to find all Python files: `**/*.py`
   - Use Grep to locate authentication code: `@login_required|authenticate`

2. **Deep Analysis**
   - Use Read to examine suspicious files
   - Look for patterns matching vulnerability signatures
```

### 3. No Output Structure

❌ **Bad:**
```markdown
Provide a report of findings.
```

✅ **Good:**
```markdown
## Output Format

\`\`\`markdown
# Analysis Report

## Summary
[High-level overview]

## Findings
### Issue 1
- **File:** path/to/file:line
- **Severity:** High
- **Description:** [Details]
- **Fix:** [Recommendation]
\`\`\`
```

### 4. Conflicting Instructions

❌ **Bad:**
```markdown
Do:
- Be comprehensive and thorough

Also:
- Keep analysis brief and quick
```

✅ **Good:**
```markdown
## Approach

**Quick Scan Mode** (< 2 min):
- Check critical patterns only
- Report obvious issues

**Deep Analysis Mode** (< 10 min):
- Comprehensive review
- Include all severity levels
```

## Testing Your Prompt

### Checklist

After writing your system prompt, verify:

- [ ] Role is clearly defined
- [ ] Responsibilities are listed and specific
- [ ] Methodology is step-by-step
- [ ] Tool usage is explained
- [ ] Output format is templated
- [ ] Success criteria are measurable
- [ ] Guidelines address common issues
- [ ] No contradictions exist
- [ ] Examples are included where helpful
- [ ] Length is appropriate (not too long)

### Iteration Process

1. **Test with simple case**
   - Invoke subagent with basic task
   - Check if output matches format
   - Verify methodology was followed

2. **Test with edge cases**
   - Complex scenarios
   - Missing information
   - Ambiguous requirements

3. **Refine based on results**
   - Add missing guidance
   - Clarify ambiguous sections
   - Improve output format

## Real-World Examples

See [examples.md](examples.md) for complete, production-ready system prompts.

## Next Steps

- [Tool Permissions](tool_permissions.md) - Selecting appropriate tools
- [Model Selection](model_selection.md) - Choosing the right model
- [Best Practices](best_practices.md) - Production patterns
- [Examples](examples.md) - Complete subagent templates
