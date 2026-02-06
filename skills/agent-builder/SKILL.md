---
name: agent-builder
description: Comprehensive guide for creating high-quality Claude Code subagents that extend capabilities through specialized workflows and domain expertise. Use when building custom subagents for task automation, domain-specific operations, or workflow optimization.
license: MIT
---

# Claude Code Subagent Development Guide

## Overview

To create high-quality Claude Code subagents that effectively automate tasks and provide specialized capabilities, use this skill. A subagent is a specialized AI assistant with its own context window, configured tools, and custom system prompt. The quality of a subagent is measured by how well it automates workflows and accomplishes real-world tasks independently.

---

# Process

## 🚀 High-Level Workflow

Creating a high-quality subagent involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Subagents vs Skills

Before diving into implementation, understand the difference:

**Subagents (`.claude/agents/`):**
- Specialized AI assistants with isolated context windows
- Invoked via the Task tool for complex, multi-step operations
- Can use any available tools (with permission restrictions)
- Best for: Autonomous workflows, research tasks, code generation

**Skills (`.claude/skills/`):**
- Knowledge injection into main conversation context
- Always loaded when description matches task
- Cannot execute tools independently
- Best for: Domain knowledge, guidelines, templates, references

**When to create a subagent:**
- Task requires multiple steps or deep research
- Need isolated context (main conversation should stay clean)
- Autonomous execution with tool usage
- Repeatable workflows (code review, testing, deployment)

**When to create a skill instead:**
- Providing reference documentation or guidelines
- Injecting domain-specific knowledge
- Templates or examples
- No tool execution needed

#### 1.2 Define the Subagent's Purpose

Answer these questions:
- **What task does this automate?** (Be specific)
- **What workflows does it handle?** (End-to-end scenarios)
- **What decisions will it make?** (Autonomous vs. requiring approval)
- **What tools does it need?** (Minimal set for security)
- **When should it activate?** (Description-based triggers)

#### 1.3 Research Existing Solutions

Before creating, check:
- Official Claude Code built-in subagents
- Community collections (VoltAgent, wshobson, 0xfurai repos)
- Similar subagents you can adapt
- Best practices from high-quality examples

**Reference**: [reference/subagent_fundamentals.md](reference/subagent_fundamentals.md)

---

### Phase 2: Design the Subagent Structure

#### 2.1 Choose File Location

**Project-level** (`.claude/agents/your-agent.md`):
- ✅ Shared with team via git
- ✅ Project-specific workflows
- ✅ Versioned with codebase

**User-level** (`~/.claude/agents/your-agent.md`):
- ✅ Personal workflows across all projects
- ✅ Private automation
- ✅ Not committed to version control

#### 2.2 Design the YAML Frontmatter

Required fields:
```yaml
---
name: your-agent-name        # kebab-case, lowercase
description: Clear trigger   # When Claude should invoke this
---
```

Optional fields:
```yaml
tools: Read, Write, Bash     # Restrict tool access (security)
model: sonnet                # sonnet (default), haiku (fast), opus (complex)
```

**Reference**: [reference/subagent_structure.md](reference/subagent_structure.md)

#### 2.3 Craft an Effective Description

The description is CRITICAL for auto-activation. Good descriptions:
- ✅ Specify clear triggers ("when reviewing code", "when analyzing performance")
- ✅ Include task keywords ("review", "test", "refactor", "debug")
- ✅ Mention domains ("security", "Python", "React", "database")
- ✅ Are concise but complete (1-2 sentences)

**Examples:**
- ❌ Bad: "Reviews code"
- ✅ Good: "Reviews code for security vulnerabilities, performance issues, and best practices violations. Use when analyzing code quality."

- ❌ Bad: "Helps with testing"
- ✅ Good: "Creates comprehensive test suites using Playwright for web applications. Use when testing frontend functionality, visual regressions, or user interactions."

**Reference**: [reference/activation_patterns.md](reference/activation_patterns.md)

---

### Phase 3: Write the System Prompt

#### 3.1 System Prompt Structure

A high-quality system prompt includes:

1. **Role definition** - Who is this agent?
2. **Primary responsibilities** - What does it do?
3. **Approach and methodology** - How does it work?
4. **Success criteria** - What defines good output?
5. **Constraints and guidelines** - What to avoid?
6. **Output format** - What to return?

#### 3.2 System Prompt Best Practices

**Do:**
- ✅ Be specific about the agent's expertise
- ✅ Define clear step-by-step workflows
- ✅ Specify output format (markdown, JSON, report structure)
- ✅ Include quality standards and criteria
- ✅ Mention when to escalate or ask questions
- ✅ Reference examples if needed

**Don't:**
- ❌ Make prompts too generic
- ❌ Give conflicting instructions
- ❌ Forget to specify output format
- ❌ Assume tools without listing them
- ❌ Skip error handling guidance

**Reference**: [reference/system_prompts.md](reference/system_prompts.md)

---

### Phase 4: Configure Tools and Model

#### 4.1 Tool Selection Strategy

**Principle**: Grant minimum required tools for security.

**Common tool sets:**

**Research agents:**
```yaml
tools: Read, Grep, Glob, WebFetch, WebSearch
```

**Code generation agents:**
```yaml
tools: Read, Write, Edit, Grep, Glob, Bash
```

**Testing agents:**
```yaml
tools: Read, Bash, Write  # For test execution and reports
```

**Review agents:**
```yaml
tools: Read, Grep, Glob  # Read-only for analysis
```

**Reference**: [reference/tool_permissions.md](reference/tool_permissions.md)

#### 4.2 Model Selection

Choose based on task complexity:

**Haiku** (`model: haiku`):
- Fast, cheap, deterministic tasks
- Simple transformations
- Template filling
- Quick analysis
- Cost-sensitive operations

**Sonnet** (default if not specified):
- Balanced performance
- Most workflows
- Code generation
- Complex analysis
- Recommended default

**Opus** (`model: opus`):
- Highest reasoning capability
- Complex decision-making
- Novel problem-solving
- Architecture design
- Use sparingly (expensive)

**Reference**: [reference/model_selection.md](reference/model_selection.md)

---

## 🎯 Workflow Summary

```
1. Research & Planning
   ├─ Define purpose and scope
   ├─ Check existing solutions
   └─ Decide: subagent vs skill?

2. Design Structure
   ├─ Choose file location (project vs user)
   ├─ Write descriptive name and description
   └─ Select tools and model

3. Write System Prompt
   ├─ Define role and responsibilities
   ├─ Specify methodology
   ├─ Include success criteria
   └─ Define output format

4. Test and Iterate
   ├─ Create the .md file
   ├─ Test activation (does description trigger it?)
   ├─ Test execution (does it work correctly?)
   └─ Refine based on results
```

---

## 📚 Reference Documentation

- [Subagent Fundamentals](reference/subagent_fundamentals.md) - Core concepts and architecture
- [Subagent Structure](reference/subagent_structure.md) - File format and YAML reference
- [Activation Patterns](reference/activation_patterns.md) - Writing effective descriptions
- [System Prompts](reference/system_prompts.md) - Best practices for prompts
- [Tool Permissions](reference/tool_permissions.md) - Security and tool selection
- [Model Selection](reference/model_selection.md) - Choosing the right model
- [Best Practices](reference/best_practices.md) - Production-ready patterns
- [Examples](reference/examples.md) - Real-world subagent templates

---

## 🎨 Quick Start Templates

See [templates/](templates/) for ready-to-use starting points:
- `basic-subagent-template.md` - Minimal working example
- `code-reviewer-template.md` - Code review specialist
- `test-creator-template.md` - Test generation specialist
- `research-agent-template.md` - Research and analysis specialist

---

## 🚀 Creating Your First Subagent

**Example: Creating a security-reviewer subagent**

1. **Create file**: `.claude/agents/security-reviewer.md`

2. **Add content**:
```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities, OWASP Top 10 issues, and secure coding practices. Use when analyzing security risks in code.
tools: Read, Grep, Glob
model: sonnet
---

You are a security review specialist focused on identifying vulnerabilities and security risks in code.

## Your Role

Analyze code for:
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Authentication/authorization flaws
- Insecure dependencies
- Secrets in code
- OWASP Top 10 vulnerabilities

## Methodology

1. Scan for common vulnerability patterns
2. Analyze authentication and authorization logic
3. Check input validation and sanitization
4. Review dependency versions for known CVEs
5. Search for hardcoded secrets or credentials

## Output Format

Provide a markdown report with:
- Executive summary (severity rating)
- Detailed findings (file:line references)
- Remediation recommendations
- Priority ranking (Critical/High/Medium/Low)

## Success Criteria

- All critical vulnerabilities identified
- Clear, actionable recommendations
- Code references for each finding
- False positive rate < 10%
```

3. **Test**: Ask Claude to "review the authentication code for security issues"

4. **Iterate**: Refine description and prompt based on activation and output quality

---

## 💡 Pro Tips

1. **Start simple** - Create basic subagent first, then enhance
2. **Test activation** - Verify description triggers the subagent correctly
3. **Limit tool access** - Only grant necessary tools for security
4. **Use Haiku for speed** - When task is deterministic and simple
5. **Version control project agents** - Commit to git for team sharing
6. **Document your subagents** - Add comments in system prompt
7. **Reuse patterns** - Adapt existing subagents for similar tasks
8. **Monitor performance** - Iterate based on real usage

---

## 🔗 Additional Resources

- Official Docs: https://code.claude.com/docs/en/sub-agents.md
- Community Collections:
  - https://github.com/VoltAgent/awesome-claude-code-subagents
  - https://github.com/wshobson/agents
  - https://github.com/0xfurai/claude-code-subagents

---

**Ready to build high-quality subagents!** 🚀
