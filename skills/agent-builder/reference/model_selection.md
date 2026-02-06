# Model Selection Guide

## Available Models

Claude Code supports three model tiers for subagents:

| Model | Speed | Cost | Reasoning | Use For |
|-------|-------|------|-----------|---------|
| **Haiku** | ⚡⚡⚡ Fastest | $ Cheap | Basic | Simple, deterministic tasks |
| **Sonnet** | ⚡⚡ Fast | $$ Moderate | Advanced | Most workflows (default) |
| **Opus** | ⚡ Slower | $$$$ Expensive | Expert | Complex reasoning, novel problems |

## Specifying Model

In YAML frontmatter:

```yaml
---
name: your-agent
description: What it does
model: sonnet  # or haiku, or opus
---
```

**Default:** If not specified, Sonnet is used.

## When to Use Each Model

### Haiku: Fast & Economical

**Best for:**
- ✅ Template filling and code generation from patterns
- ✅ Simple transformations and formatting
- ✅ Deterministic tasks with clear rules
- ✅ High-volume, repetitive operations
- ✅ Quick analysis without deep reasoning
- ✅ Cost-sensitive operations

**Examples:**
- Code formatting (applying prettier, black)
- Simple test generation from templates
- Documentation string generation
- File organization and renaming
- Configuration file generation
- Boilerplate code creation

**When NOT to use:**
- ❌ Novel problem-solving
- ❌ Complex architecture decisions
- ❌ Ambiguous requirements
- ❌ Deep code analysis
- ❌ Security vulnerability detection

**Example subagents:**

```yaml
---
name: code-formatter
description: Formats code using project style guidelines
tools: Read, Edit, Bash
model: haiku  # Simple, deterministic task
---
```

```yaml
---
name: docstring-generator
description: Generates docstrings for Python functions
tools: Read, Edit
model: haiku  # Template-based generation
---
```

### Sonnet: Balanced Default

**Best for:**
- ✅ Most workflows and use cases
- ✅ Code generation and refactoring
- ✅ Test suite creation
- ✅ Code review and analysis
- ✅ Documentation generation
- ✅ Bug fixing
- ✅ Moderate complexity tasks

**Examples:**
- Security vulnerability scanning
- Code quality review
- Comprehensive test generation
- API client generation
- Performance optimization
- Database query optimization
- Refactoring workflows

**This is the recommended default** for most subagents.

**Example subagents:**

```yaml
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob
model: sonnet  # or omit - sonnet is default
---
```

```yaml
---
name: test-creator
description: Creates comprehensive test suites
tools: Read, Write, Grep, Glob
# model not specified = sonnet used
---
```

### Opus: Maximum Reasoning

**Best for:**
- ✅ Novel problem-solving
- ✅ Architecture design
- ✅ Complex decision-making
- ✅ Ambiguous requirements
- ✅ Creative solutions
- ✅ System design
- ✅ Research and synthesis

**Examples:**
- Architecture analysis and design
- Complex refactoring strategies
- System optimization planning
- Novel algorithm design
- API design and interfaces
- Technology selection
- Performance bottleneck diagnosis

**Use sparingly** - significantly more expensive and slower.

**Example subagents:**

```yaml
---
name: architect
description: Designs system architecture and makes technology decisions
tools: Read, Grep, Glob, WebSearch
model: opus  # Complex reasoning needed
---
```

```yaml
---
name: performance-architect
description: Analyzes performance bottlenecks and designs optimization strategies
tools: Read, Grep, Glob, Bash
model: opus  # Deep analysis required
---
```

## Decision Matrix

Use this matrix to choose the right model:

```
Task Complexity
    │
    │   Opus Territory
    │   ┌─────────────┐
    │   │ Novel       │
    │   │ Architecture│
    │   │ Creative    │
    │   └─────────────┘
    │
    │   Sonnet Territory (Default)
    │   ┌─────────────────────────┐
    │   │ Code Review             │
    │   │ Test Generation         │
    │   │ Security Scanning       │
    │   │ Bug Fixing              │
    │   └─────────────────────────┘
    │
    │   Haiku Territory
    │   ┌───────────────┐
    │   │ Formatting    │
    │   │ Templates     │
    │   │ Simple Gen    │
    │   └───────────────┘
    │
    └────────────────────────────────
          Speed / Cost Efficiency
```

## Decision Flowchart

```
Is the task deterministic with clear rules?
    ├─ YES → Use Haiku
    │
    └─ NO ↓

Does it require novel problem-solving or architecture design?
    ├─ YES → Use Opus
    │
    └─ NO ↓

Use Sonnet (default)
```

## Cost Considerations

**Relative costs** (approximate):

```
Haiku:   1x   (base cost)
Sonnet:  15x  (15 times Haiku)
Opus:    75x  (75 times Haiku, 5x Sonnet)
```

### Cost Optimization Strategies

**1. Haiku for screening, Sonnet for analysis:**

```yaml
# Quick screener
---
name: quick-security-scan
model: haiku
---
Quickly scan for obvious security patterns.

# Deep analyzer
---
name: security-auditor
model: sonnet
---
Comprehensive security analysis with CVE checking.
```

**2. Chain models:**

```
Haiku (quick triage)
    ↓
Sonnet (analysis)
    ↓
Opus (if complex issue found)
```

**3. Use defaults wisely:**

```yaml
# Don't over-specify Opus
---
name: simple-formatter
model: opus  # ❌ Wasteful
---

# Use Haiku instead
---
name: simple-formatter
model: haiku  # ✅ Appropriate
---
```

## Performance Characteristics

### Response Time

**Haiku:**
- ⚡ Sub-second to few seconds
- Ideal for interactive workflows
- Great for high-frequency invocations

**Sonnet:**
- ⚡⚡ Few seconds to ~10-20 seconds
- Good balance for most tasks
- Acceptable for typical workflows

**Opus:**
- ⚡⚡⚡ 20 seconds to minutes
- Use when quality > speed
- Not for interactive use

### Throughput

**Haiku:**
- Process hundreds of files quickly
- Good for batch operations
- Minimal latency overhead

**Sonnet:**
- Process dozens of files efficiently
- Good for typical projects
- Moderate latency

**Opus:**
- Process few items thoroughly
- Use for critical items only
- Higher latency

## Quality vs Speed Tradeoff

```
Quality
   ↑
   │        Opus
   │         ●
   │
   │     Sonnet
   │       ●
   │
   │  Haiku
   │   ●
   │
   └──────────────→ Speed
```

## Real-World Examples

### Example 1: Code Formatting

```yaml
---
name: prettier-formatter
description: Formats JavaScript/TypeScript code using Prettier
tools: Read, Edit, Bash
model: haiku  # Simple, deterministic
---

1. Read files to format
2. Run prettier
3. Report formatted files
```

**Why Haiku:** Formatting is deterministic, no reasoning needed.

### Example 2: Test Generation

```yaml
---
name: test-generator
description: Generates comprehensive test suites with edge cases
tools: Read, Write, Grep, Glob
model: sonnet  # or default (sonnet)
---

1. Analyze code structure
2. Identify test scenarios
3. Generate tests with coverage
```

**Why Sonnet:** Requires understanding code, identifying scenarios, moderate complexity.

### Example 3: Architecture Review

```yaml
---
name: architecture-reviewer
description: Reviews system architecture and recommends improvements
tools: Read, Grep, Glob, WebSearch
model: opus  # Complex reasoning required
---

1. Analyze codebase structure
2. Identify architectural patterns
3. Evaluate scalability and maintainability
4. Recommend improvements
```

**Why Opus:** Novel analysis, complex trade-offs, architectural reasoning.

### Example 4: Security Scanner

```yaml
---
name: security-scanner
description: Scans for OWASP Top 10 vulnerabilities
tools: Read, Grep, Glob
model: sonnet  # Pattern matching with context
---

1. Search for vulnerability patterns
2. Analyze context and exploitability
3. Report findings with severity
```

**Why Sonnet:** Pattern matching + context understanding, not trivial but not novel.

### Example 5: Docstring Generator

```yaml
---
name: docstring-generator
description: Generates Python docstrings from function signatures
tools: Read, Edit
model: haiku  # Template-based generation
---

1. Read Python files
2. Identify functions without docstrings
3. Generate docstrings from signatures
```

**Why Haiku:** Template-based, clear rules, no complex reasoning.

## Hybrid Workflows

### Pattern 1: Triage then Deep-Dive

```yaml
# Agent 1: Quick scan (Haiku)
---
name: quick-scan
model: haiku
description: Quick security pattern scan
---

# Agent 2: Deep analysis (Sonnet)
---
name: security-auditor
model: sonnet
description: Comprehensive security analysis
---
```

**Workflow:**
1. Haiku quickly scans entire codebase (fast)
2. Identifies potential issues
3. Sonnet does deep analysis on flagged areas only

### Pattern 2: Generation then Optimization

```yaml
# Agent 1: Generate (Sonnet)
---
name: code-generator
model: sonnet
description: Generates working code
---

# Agent 2: Optimize (Opus)
---
name: code-optimizer
model: opus
description: Optimizes for performance and elegance
---
```

**Workflow:**
1. Sonnet generates functional code
2. Opus optimizes for peak performance

### Pattern 3: Screening Pipeline

```
Haiku (format check)
    ↓ pass
Haiku (lint check)
    ↓ pass
Sonnet (code review)
    ↓ issues found
Opus (architecture review for complex issues)
```

## Common Mistakes

### 1. Using Opus for Simple Tasks

❌ **Bad:**
```yaml
---
name: file-formatter
model: opus  # Wasteful!
---
```

✅ **Good:**
```yaml
---
name: file-formatter
model: haiku  # Appropriate
---
```

### 2. Using Haiku for Complex Reasoning

❌ **Bad:**
```yaml
---
name: architecture-designer
model: haiku  # Won't work well
---
```

✅ **Good:**
```yaml
---
name: architecture-designer
model: opus  # Needs high reasoning
---
```

### 3. Not Using Defaults

❌ **Bad:**
```yaml
---
name: code-reviewer
model: sonnet  # Redundant (sonnet is default)
---
```

✅ **Good:**
```yaml
---
name: code-reviewer
# model not specified = sonnet used automatically
---
```

### 4. Over-Engineering

❌ **Bad:**
```yaml
# Always using Opus "just to be safe"
model: opus
```

✅ **Good:**
```yaml
# Use appropriate model for task complexity
# Start with Sonnet (default), adjust if needed
```

## Testing and Iteration

### Start with Default (Sonnet)

1. Create subagent without specifying model
2. Test with typical tasks
3. Evaluate quality and speed

### Adjust Based on Results

**If output quality is poor:**
- Consider Opus for complex reasoning

**If task is simple and slow:**
- Consider Haiku for speed

**If cost is concern:**
- Evaluate if Haiku sufficient

### A/B Testing

Create two versions:

```yaml
# Version A
---
name: test-generator-fast
model: haiku
---

# Version B
---
name: test-generator-quality
model: sonnet
---
```

Test both, compare:
- Output quality
- Speed
- Cost
- User satisfaction

## Summary

**Default strategy:**
1. Start with Sonnet (or don't specify model)
2. Test with real tasks
3. Adjust to Haiku if task is simple and deterministic
4. Adjust to Opus if task requires complex reasoning

**Rule of thumb:**
- Haiku: "I know exactly what to do"
- Sonnet: "I need to understand and decide"
- Opus: "I need to reason about trade-offs and design"

## Next Steps

- [Best Practices](best_practices.md) - Production patterns
- [Examples](examples.md) - Real subagents with model choices explained
