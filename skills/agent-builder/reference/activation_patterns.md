# Activation Patterns: Writing Effective Descriptions

## Overview

The `description` field in your subagent's YAML frontmatter is CRITICAL for automatic activation. Claude Code analyzes the description to determine when to invoke your subagent.

## How Activation Works

```
User Request
    ↓
Claude analyzes request
    ↓
Compares against all subagent descriptions
    ↓
Finds matching description keywords/context
    ↓
Invokes matched subagent via Task tool
```

## Description Formula

**Effective descriptions follow this pattern:**

```
[What it does] + [Domain/Tech] + [Trigger phrase]
```

**Examples:**
```yaml
# Formula applied:
# "Reviews code" + "security vulnerabilities" + "Use when analyzing security"
description: Reviews code for security vulnerabilities, OWASP Top 10 issues, and secure coding practices. Use when analyzing security risks in code.

# Formula applied:
# "Creates tests" + "Playwright/web apps" + "Use when testing frontend"
description: Creates comprehensive test suites using Playwright for web applications. Use when testing frontend functionality, visual regressions, or user interactions.

# Formula applied:
# "Optimizes performance" + "React" + "Use when optimizing"
description: Analyzes React components for performance issues, re-render problems, and optimization opportunities. Use when optimizing React application performance.
```

## Trigger Keywords by Category

### Code Quality & Review

**Strong trigger keywords:**
- review, analyze, check, audit, inspect, evaluate
- code quality, best practices, standards, conventions
- refactor, improve, optimize, enhance
- issues, problems, violations, anti-patterns

**Example descriptions:**
```yaml
description: Reviews code for quality issues, best practices violations, and potential bugs. Use when analyzing code quality.

description: Audits code for performance bottlenecks, memory leaks, and optimization opportunities. Use when improving application performance.

description: Checks code adherence to style guides, naming conventions, and project standards. Use when enforcing coding standards.
```

### Security

**Strong trigger keywords:**
- security, vulnerabilities, risks, threats, exploits
- OWASP, CVE, injection, XSS, CSRF, authentication
- audit, scan, penetration test, security review
- secrets, credentials, keys, tokens

**Example descriptions:**
```yaml
description: Scans code for security vulnerabilities including SQL injection, XSS, CSRF, and authentication issues. Use when conducting security audits.

description: Detects hardcoded secrets, API keys, passwords, and sensitive data in codebase. Use when checking for exposed credentials.

description: Analyzes authentication and authorization logic for security flaws and access control issues. Use when reviewing auth security.
```

### Testing

**Strong trigger keywords:**
- test, testing, coverage, assertions, test suite
- unit tests, integration tests, e2e tests, regression tests
- Playwright, pytest, jest, testing framework
- test generation, test creation, test automation

**Example descriptions:**
```yaml
description: Creates comprehensive unit test suites with high coverage for Python code using pytest. Use when generating Python unit tests.

description: Generates end-to-end tests using Playwright for web application user flows. Use when creating E2E test automation.

description: Builds integration tests for API endpoints and service interactions. Use when testing API integration points.
```

### Documentation

**Strong trigger keywords:**
- document, documentation, README, comments, docstrings
- API docs, guide, tutorial, reference, examples
- explain, describe, clarify, annotate

**Example descriptions:**
```yaml
description: Generates comprehensive API documentation with examples and usage patterns. Use when creating API reference documentation.

description: Creates clear README.md files with installation, usage, and contribution guidelines. Use when documenting projects or components.

description: Adds detailed inline comments and docstrings to code for better understanding. Use when improving code documentation.
```

### Deployment & DevOps

**Strong trigger keywords:**
- deploy, deployment, release, CI/CD, pipeline
- build, configure, setup, provision, infrastructure
- Docker, Kubernetes, AWS, cloud, containers
- automation, orchestration, configuration

**Example descriptions:**
```yaml
description: Automates deployment pipelines with CI/CD best practices for cloud environments. Use when setting up deployment automation.

description: Configures Docker containers and Kubernetes manifests for application deployment. Use when containerizing applications.

description: Provisions infrastructure as code using Terraform and cloud best practices. Use when setting up cloud infrastructure.
```

### Architecture & Design

**Strong trigger keywords:**
- architecture, design, pattern, structure, organization
- system design, architecture review, design patterns
- scalability, maintainability, modularity, coupling
- refactor, restructure, reorganize

**Example descriptions:**
```yaml
description: Analyzes codebase architecture for design patterns, coupling, and structural issues. Use when reviewing system architecture.

description: Recommends architectural improvements for scalability, maintainability, and performance. Use when optimizing architecture.

description: Designs modular system architectures following SOLID principles and best practices. Use when creating system designs.
```

### Data & Analytics

**Strong trigger keywords:**
- data, database, SQL, query, analytics, metrics
- optimization, indexing, performance, query analysis
- ETL, data pipeline, data processing, transformation
- visualization, reporting, dashboard

**Example descriptions:**
```yaml
description: Optimizes database queries, indexes, and schema design for performance. Use when improving database performance.

description: Analyzes SQL queries for efficiency, correctness, and optimization opportunities. Use when reviewing database queries.

description: Designs data pipelines and ETL processes for reliable data transformation. Use when building data workflows.
```

## Pattern Analysis: Good vs. Bad

### ❌ Bad Descriptions (Too Vague)

```yaml
description: Helps with testing
# Problem: What kind of testing? What tech? When to use?

description: Reviews code
# Problem: Review for what? Quality? Security? Style?

description: Python agent
# Problem: Does what with Python? Too generic.

description: Useful for web development
# Problem: What aspect? Frontend? Backend? What task?

description: General purpose assistant
# Problem: No specific trigger, will never activate.
```

### ✅ Good Descriptions (Specific & Actionable)

```yaml
description: Creates comprehensive pytest test suites with fixtures and parametrization for Python code. Use when generating Python unit tests.
# Why good: Specific tech (pytest), specific task (test generation), clear trigger

description: Reviews TypeScript code for type safety issues, strict mode violations, and typing best practices. Use when analyzing TypeScript type correctness.
# Why good: Language-specific, clear focus (type safety), actionable trigger

description: Generates React components following project conventions with TypeScript, proper hooks usage, and accessibility features. Use when creating React components.
# Why good: Tech stack specified, quality criteria listed, clear use case

description: Optimizes database queries by analyzing execution plans, suggesting indexes, and refactoring inefficient SQL. Use when improving database performance.
# Why good: Specific methodology, clear outcome, precise trigger
```

## Advanced Patterns

### Multi-Domain Triggers

For subagents that span multiple domains:

```yaml
description: Full-stack code reviewer that analyzes frontend (React/TypeScript), backend (Node.js/Python), and database (SQL) code for quality, security, and performance issues. Use when reviewing code across the entire stack.
```

**Pattern:** List all domains clearly, then provide broad trigger.

### Workflow-Based Triggers

For process-oriented subagents:

```yaml
description: Automates the complete PR review workflow: checks tests, reviews code quality, scans security, verifies CI/CD, and generates review report. Use when conducting comprehensive pull request reviews.
```

**Pattern:** Describe full workflow, emphasize "complete" or "end-to-end".

### Tech Stack Specific

For technology-specific agents:

```yaml
description: Rust development specialist that writes idiomatic Rust code following ownership rules, error handling best practices, and performance optimization patterns. Use when writing or reviewing Rust code.
```

**Pattern:** Lead with technology, list specific features/concepts, clear language trigger.

### Comparative Triggers

When you have multiple similar agents:

```yaml
# Agent 1: Quick review
description: Performs fast code quality checks for common issues and style violations. Use for quick code reviews.

# Agent 2: Deep review
description: Conducts comprehensive code analysis including architecture, security, performance, and maintainability. Use for thorough code audits.
```

**Pattern:** Differentiate with intensity keywords (quick/deep, fast/comprehensive, basic/advanced).

## Trigger Phrase Best Practices

### Effective "Use when..." Phrases

```yaml
# Task-oriented
"Use when creating..."
"Use when testing..."
"Use when deploying..."
"Use when analyzing..."

# Problem-oriented
"Use when fixing..."
"Use when debugging..."
"Use when optimizing..."
"Use when troubleshooting..."

# Context-oriented
"Use when working with..."
"Use when reviewing..."
"Use when building..."
"Use when integrating..."

# Goal-oriented
"Use for improving..."
"Use for ensuring..."
"Use for automating..."
"Use for generating..."
```

### Alternative Trigger Phrases

```yaml
"Invoke for..."
"Call when..."
"Activate during..."
"Apply to..."
"Useful for..."
```

## Testing Your Description

### Activation Test

After creating your subagent, test if the description triggers correctly:

**Test cases:**

1. **Direct match:**
   ```
   Description: "Reviews Python code for bugs"
   Test: "Review this Python code for bugs"
   Expected: ✅ Should activate
   ```

2. **Semantic match:**
   ```
   Description: "Analyzes React performance issues"
   Test: "Why is my React app slow?"
   Expected: ✅ Should activate
   ```

3. **Domain match:**
   ```
   Description: "Creates Playwright E2E tests for web apps"
   Test: "Write some browser tests for the login page"
   Expected: ✅ Should activate
   ```

4. **False positive test:**
   ```
   Description: "Python test generator using pytest"
   Test: "Review my JavaScript code"
   Expected: ❌ Should NOT activate
   ```

### Refinement Process

If activation doesn't work:

1. **Add more specific keywords**
   ```yaml
   # Before
   description: Helps with frontend testing

   # After
   description: Creates Playwright tests for React components including user interactions, visual regression, and accessibility checks. Use when testing React frontend.
   ```

2. **Include alternative terms**
   ```yaml
   # Before
   description: Reviews security vulnerabilities

   # After
   description: Reviews code for security vulnerabilities, exploits, CVEs, and attack vectors. Use when conducting security audits or penetration testing.
   ```

3. **Add explicit use cases**
   ```yaml
   # Before
   description: Database optimization agent

   # After
   description: Optimizes database queries, indexes, and schema for PostgreSQL and MySQL. Use when debugging slow queries, analyzing database performance, or reducing query time.
   ```

## Description Length Guidelines

### Optimal Length: 1-3 Sentences

**Too short (< 10 words):**
```yaml
description: Reviews code for issues
# Lacks context and specificity
```

**Good (20-50 words):**
```yaml
description: Reviews TypeScript code for type safety issues, strict mode violations, and typing best practices. Use when analyzing TypeScript type correctness.
# Clear, specific, actionable
```

**Too long (> 100 words):**
```yaml
description: This agent is designed to help you review your TypeScript codebase by analyzing the types, checking for any violations of strict mode, ensuring that best practices are being followed, looking for any potential bugs or issues related to type safety, and providing recommendations for improvements. It can handle large codebases and works with modern TypeScript features. Use this when you need to check your TypeScript code for any type-related problems or when you want to ensure your code follows TypeScript best practices.
# Too verbose, loses focus
```

## Real-World Examples

### Example 1: Code Reviewer

```yaml
name: code-reviewer
description: Reviews code for quality issues, bugs, performance problems, and best practices violations across multiple languages. Use when conducting code reviews or analyzing code quality.
```

**Why it works:**
- Clear action: "Reviews code"
- Specific areas: quality, bugs, performance, best practices
- Broad scope: multiple languages
- Clear trigger: "code reviews" or "analyzing code quality"

### Example 2: Security Auditor

```yaml
name: security-auditor
description: Performs comprehensive security audits checking for OWASP Top 10 vulnerabilities, dependency CVEs, hardcoded secrets, and insecure configurations. Use when conducting security assessments or penetration testing.
```

**Why it works:**
- Authority: "comprehensive security audits"
- Standards: OWASP Top 10
- Specific checks: CVEs, secrets, configs
- Clear triggers: "security assessments" or "penetration testing"

### Example 3: Test Generator

```yaml
name: playwright-test-generator
description: Generates comprehensive Playwright test suites for web applications including E2E flows, visual regression tests, and accessibility checks. Use when creating browser automation tests.
```

**Why it works:**
- Tech stack: Playwright, web applications
- Test types: E2E, visual regression, accessibility
- Clear action: "Generates test suites"
- Specific trigger: "browser automation tests"

### Example 4: Documentation Writer

```yaml
name: api-documenter
description: Creates detailed API documentation with OpenAPI/Swagger specs, code examples, request/response schemas, and usage guides. Use when documenting REST APIs or GraphQL services.
```

**Why it works:**
- Output specified: OpenAPI/Swagger
- Includes: examples, schemas, guides
- Tech coverage: REST APIs, GraphQL
- Clear use case: API documentation

## Common Pitfalls to Avoid

### 1. Ambiguous Action Verbs

❌ "Helps with", "Assists in", "Works on"
✅ "Reviews", "Creates", "Analyzes", "Generates", "Optimizes"

### 2. Missing Technology Context

❌ "Creates tests for web apps"
✅ "Creates Playwright tests for React web applications"

### 3. No Clear Trigger

❌ "Code quality agent"
✅ "Reviews code quality issues. Use when conducting code reviews."

### 4. Overlapping Descriptions

If you have:
```yaml
# Agent A
description: Reviews code for issues

# Agent B
description: Analyzes code for problems
```

Claude won't know which to invoke! Make them distinct:

```yaml
# Agent A
description: Reviews code for security vulnerabilities and OWASP issues. Use for security audits.

# Agent B
description: Analyzes code for performance bottlenecks and optimization opportunities. Use for performance reviews.
```

## Next Steps

- [System Prompts](system_prompts.md) - Writing effective system prompts
- [Subagent Structure](subagent_structure.md) - Complete file format reference
- [Examples](examples.md) - Real-world subagent templates
