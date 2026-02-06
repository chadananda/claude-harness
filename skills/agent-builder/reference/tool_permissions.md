# Tool Permissions and Security

## Overview

Tool permissions define which tools your subagent can access. Following the **principle of least privilege** is critical for security and focus.

## Why Restrict Tools?

**Security:**
- Prevent unintended file modifications
- Limit command execution capabilities
- Reduce attack surface

**Performance:**
- Fewer tools = faster tool selection
- Reduced decision overhead
- More focused execution

**Clarity:**
- Explicit about capabilities
- Prevents tool misuse
- Clearer scope

## Available Tools

### File Operations

#### `Read`
**Purpose:** Read file contents

**Use for:**
- Code analysis
- Configuration review
- Documentation reading
- Data inspection

**Security:** Safe (read-only)

**Example:**
```yaml
tools: Read, Grep, Glob  # Safe read-only combo
```

#### `Write`
**Purpose:** Create new files

**Use for:**
- Code generation
- Test file creation
- Documentation generation
- Report output

**Security:** ⚠️ Medium risk (creates files)

**Example:**
```yaml
tools: Read, Write, Grep, Glob  # Controlled generation
```

#### `Edit`
**Purpose:** Modify existing files

**Use for:**
- Code refactoring
- Bug fixes
- Comment additions
- Configuration updates

**Security:** ⚠️ Medium-high risk (modifies existing code)

**Example:**
```yaml
tools: Read, Edit, Grep, Glob  # For refactoring agents
```

#### `Glob`
**Purpose:** Find files by pattern

**Use for:**
- Discovering source files
- Finding specific file types
- Project structure analysis

**Security:** Safe (read-only discovery)

**Example:**
```yaml
tools: Glob, Read  # Discover and read pattern
```

### Search Operations

#### `Grep`
**Purpose:** Search file contents with regex

**Use for:**
- Finding code patterns
- Vulnerability scanning
- Dependency searching
- Usage analysis

**Security:** Safe (read-only search)

**Example:**
```yaml
tools: Grep, Read  # Search and analyze
```

### Execution

#### `Bash`
**Purpose:** Execute shell commands

**Use for:**
- Running tests
- Building projects
- Running formatters
- Tool execution

**Security:** ⚠️⚠️⚠️ HIGH RISK (arbitrary command execution)

**Example:**
```yaml
tools: Read, Bash  # For test runners
```

**Dangers:**
- Can modify files: `rm -rf /`
- Can execute malicious code
- Can access environment variables
- Can make network requests

**Only grant when absolutely necessary**

#### `BashOutput`
**Purpose:** Read output from background bash processes

**Use for:**
- Monitoring long-running processes
- Reading build outputs
- Test result streaming

**Security:** Safe (read-only)

#### `KillShell`
**Purpose:** Terminate background shells

**Use for:**
- Cleaning up hung processes
- Managing background tasks

**Security:** ⚠️ Medium risk

### Web Access

#### `WebFetch`
**Purpose:** Fetch web content

**Use for:**
- Documentation lookup
- API documentation reading
- External resource access

**Security:** ⚠️ Medium risk (network access)

**Example:**
```yaml
tools: Read, WebFetch  # For research agents
```

#### `WebSearch`
**Purpose:** Search the web

**Use for:**
- Finding documentation
- Error message research
- Best practice lookup

**Security:** ⚠️ Medium risk (network access)

**Example:**
```yaml
tools: Read, WebSearch, WebFetch  # Research combo
```

### Delegation

#### `Task`
**Purpose:** Invoke other subagents

**Use for:**
- Multi-agent orchestration
- Delegating sub-tasks
- Complex workflows

**Security:** ⚠️ Risk depends on delegated agents

**Example:**
```yaml
tools: Task, Read, Grep  # For orchestrator agents
```

### Notebooks

#### `NotebookEdit`
**Purpose:** Edit Jupyter notebooks

**Use for:**
- Data science workflows
- Notebook generation
- Cell modifications

**Security:** ⚠️ Medium risk (modifies notebooks)

### User Interaction

#### `AskUserQuestion`
**Purpose:** Ask user for input

**Use for:**
- Clarification questions
- Decision points
- Option selection

**Security:** Safe (requires human input)

**Example:**
```yaml
tools: Read, AskUserQuestion  # For interactive agents
```

### MCP Resources

#### `ListMcpResourcesTool`
**Purpose:** List MCP server resources

**Use for:**
- MCP integration
- Resource discovery

**Security:** Safe (read-only)

#### `ReadMcpResourceTool`
**Purpose:** Read MCP resources

**Use for:**
- MCP data access
- External integrations

**Security:** Safe (read-only)

## Tool Sets by Agent Type

### Read-Only Analysis Agents

**Use case:** Code review, security audit, quality analysis

```yaml
tools: Read, Grep, Glob
```

**What they can do:**
- ✅ Read all files
- ✅ Search for patterns
- ✅ Find files by name
- ❌ Cannot modify anything
- ❌ Cannot execute commands

**Perfect for:**
- Security reviewers
- Code quality analyzers
- Documentation parsers
- Dependency auditors

### Code Generation Agents

**Use case:** Creating new code, tests, documentation

```yaml
tools: Read, Write, Grep, Glob
```

**What they can do:**
- ✅ Read existing code
- ✅ Create new files
- ✅ Search codebase
- ✅ Find files
- ❌ Cannot modify existing files
- ❌ Cannot execute commands

**Perfect for:**
- Test generators
- Documentation creators
- Boilerplate generators
- API client generators

### Code Refactoring Agents

**Use case:** Modifying existing code

```yaml
tools: Read, Edit, Grep, Glob
```

**What they can do:**
- ✅ Read existing code
- ✅ Modify existing files
- ✅ Search patterns
- ✅ Find files
- ❌ Cannot create new files (add Write if needed)
- ❌ Cannot execute commands

**Perfect for:**
- Refactoring specialists
- Code formatters (without shell)
- Comment generators
- Rename automation

### Test Execution Agents

**Use case:** Running tests and reporting results

```yaml
tools: Read, Write, Bash
```

**What they can do:**
- ✅ Read test files
- ✅ Create test reports
- ✅ Execute test commands
- ⚠️ Can run any shell command (risky)

**Perfect for:**
- Test runners
- CI/CD integrators
- Coverage reporters

**Security note:** High risk due to Bash

### Full-Stack Development Agents

**Use case:** Complete feature implementation

```yaml
tools: Read, Write, Edit, Grep, Glob, Bash
```

**What they can do:**
- ✅ Everything (read, write, modify, execute)
- ⚠️⚠️⚠️ Very powerful, very risky

**Perfect for:**
- Feature builders
- Full-stack developers
- Deploy automation

**Security note:** Maximum risk, only for trusted workflows

### Research Agents

**Use case:** Information gathering and analysis

```yaml
tools: Read, Grep, Glob, WebFetch, WebSearch
```

**What they can do:**
- ✅ Read local files
- ✅ Search locally
- ✅ Access web resources
- ❌ Cannot modify files
- ❌ Cannot execute commands

**Perfect for:**
- Documentation researchers
- Error message analyzers
- Best practice finders
- Technology explorers

### Orchestrator Agents

**Use case:** Coordinating multiple agents

```yaml
tools: Task, Read, Grep, Glob
```

**What they can do:**
- ✅ Invoke other subagents
- ✅ Read files for context
- ✅ Search and discover
- ❌ Cannot modify files directly
- ❌ Cannot execute commands directly

**Perfect for:**
- Workflow coordinators
- Multi-step automators
- Pipeline managers

## Security Best Practices

### 1. Start Minimal

```yaml
# Start here
tools: Read, Grep, Glob

# Add only what's needed
tools: Read, Grep, Glob, Write  # If generation needed
tools: Read, Grep, Glob, Edit   # If modification needed
```

### 2. Avoid Wildcards

```yaml
# ❌ NEVER DO THIS
tools: *

# ✅ Always specify explicitly
tools: Read, Write, Bash
```

### 3. Separate Concerns

```yaml
# Instead of one powerful agent:
# tools: Read, Write, Edit, Bash  # Too powerful

# Create specialized agents:

# Analyzer
tools: Read, Grep, Glob

# Generator
tools: Read, Write, Grep, Glob

# Runner
tools: Read, Bash
```

### 4. Document Why

```markdown
---
name: test-runner
description: Runs test suites and reports results
tools: Read, Bash  # Bash needed for pytest/jest execution
---
```

### 5. Review Periodically

- Can tools be reduced?
- Are all tools actually used?
- Is Bash necessary?
- Can Edit be replaced with Write?

## Dangerous Combinations

### ⚠️⚠️⚠️ EXTREME DANGER

```yaml
tools: Write, Edit, Bash
```

**Why dangerous:**
- Can modify any file
- Can execute any command
- Can delete files
- Full filesystem access

**Only use for:** Fully trusted, critical automation

### ⚠️⚠️ HIGH RISK

```yaml
tools: Edit, Bash
```

**Why dangerous:**
- Can modify code and execute it
- Can alter configuration and run
- High compromise potential

### ⚠️ MODERATE RISK

```yaml
tools: Write, Bash
```

**Why risky:**
- Can create and execute scripts
- Can generate malicious code

```yaml
tools: Edit
```

**Why risky:**
- Can break existing code
- Can introduce vulnerabilities

## Testing Tool Permissions

### Verification Checklist

After defining tools, verify:

- [ ] Agent can complete its task with these tools
- [ ] No unnecessary tools included
- [ ] Bash is only included if absolutely required
- [ ] Edit and Write aren't both included unless needed
- [ ] Read-only tasks don't have write permissions

### Testing Process

1. **Minimal test:**
   ```yaml
   tools: Read  # Start with least privilege
   ```
   - Does agent work? → Keep minimal
   - Does agent fail? → Add next minimal tool

2. **Incremental addition:**
   ```yaml
   tools: Read, Grep  # Add search
   ```
   - Test again
   - Continue until functional

3. **Review final set:**
   - Can any tool be removed?
   - Is each tool necessary?
   - Document why each is needed

## Tool Permission Patterns

### Pattern 1: Read-Analyze-Report

```yaml
tools: Read, Grep, Glob
```

**Flow:**
1. Discover files (Glob)
2. Search patterns (Grep)
3. Read details (Read)
4. Report findings (output text)

**Use for:** Analysis, auditing, reviewing

### Pattern 2: Read-Generate-Write

```yaml
tools: Read, Grep, Glob, Write
```

**Flow:**
1. Understand context (Read, Grep, Glob)
2. Generate new code/docs
3. Write new files (Write)

**Use for:** Generation, creation, templating

### Pattern 3: Read-Modify-Report

```yaml
tools: Read, Edit, Grep, Glob
```

**Flow:**
1. Find target files (Glob, Grep)
2. Read current state (Read)
3. Modify in place (Edit)
4. Report changes (output text)

**Use for:** Refactoring, formatting, updating

### Pattern 4: Read-Execute-Report

```yaml
tools: Read, Bash
```

**Flow:**
1. Read configuration (Read)
2. Execute command (Bash)
3. Report results (output text)

**Use for:** Test running, building, tool execution

### Pattern 5: Research-Synthesize

```yaml
tools: Read, Grep, Glob, WebFetch, WebSearch
```

**Flow:**
1. Search locally (Grep, Glob)
2. Read relevant files (Read)
3. Search web for additional info (WebSearch, WebFetch)
4. Synthesize findings (output text)

**Use for:** Research, documentation, investigation

## Common Mistakes

### 1. Over-Permissioning

❌ **Bad:**
```yaml
# For a code reviewer that only analyzes
tools: Read, Write, Edit, Bash, Grep, Glob
```

✅ **Good:**
```yaml
# Code reviewer only needs read access
tools: Read, Grep, Glob
```

### 2. Under-Permissioning

❌ **Bad:**
```yaml
# Test generator that needs to create files
tools: Read, Grep
```

✅ **Good:**
```yaml
tools: Read, Grep, Glob, Write  # Added Write for test creation
```

### 3. Inconsistent Permissions

❌ **Bad:**
```yaml
# Analyzer that can execute?
name: code-analyzer
description: Analyzes code quality
tools: Read, Bash  # Why Bash?
```

✅ **Good:**
```yaml
name: code-analyzer
description: Analyzes code quality
tools: Read, Grep, Glob  # Only analysis tools
```

## Next Steps

- [Model Selection](model_selection.md) - Choosing the right model
- [Best Practices](best_practices.md) - Production patterns
- [Examples](examples.md) - Complete subagent templates with tool justifications
