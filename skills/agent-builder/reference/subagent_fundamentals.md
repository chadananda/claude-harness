# Subagent Fundamentals

## What Are Claude Code Subagents?

Subagents are specialized AI assistants that operate independently with their own context windows. They are invoked by the main Claude Code instance via the Task tool to handle specific tasks autonomously.

### Key Characteristics

**Isolated Context:**
- Each subagent runs in its own context window
- Main conversation stays clean and focused
- Subagent results are returned when complete

**Tool Access:**
- Can use any tools granted via permissions
- Tool restrictions provide security boundaries
- Can read files, write code, run commands, etc.

**Custom System Prompts:**
- Specialized instructions for specific domains
- Defined workflows and methodologies
- Quality criteria and success metrics

**Autonomous Operation:**
- Runs independently until task completion
- Makes decisions without main conversation input
- Returns complete results back to orchestrator

## Subagents vs Skills: When to Use Each

### Use Subagents For:

✅ **Multi-step autonomous workflows**
- Code review processes
- Test suite creation
- Research and analysis
- Deployment automation

✅ **Complex tasks requiring tool usage**
- File reading and writing
- Command execution
- Search and analysis
- Report generation

✅ **Context isolation needs**
- Deep research that would clutter main conversation
- Parallel task execution
- Specialized analysis requiring focus

✅ **Repeatable processes**
- Standardized workflows
- Quality assurance pipelines
- Consistent methodologies

### Use Skills For:

✅ **Domain knowledge and guidelines**
- API documentation references
- Best practices guides
- Code style guidelines
- Architecture patterns

✅ **Templates and examples**
- Code templates
- Configuration examples
- Workflow checklists

✅ **Context enrichment**
- Background information
- Domain-specific terminology
- Reference materials

✅ **No tool execution needed**
- Pure knowledge injection
- Guidelines and principles
- Examples and patterns

## Subagent Architecture

```
Main Claude Code Instance
    ↓
    Invokes via Task tool
    ↓
┌─────────────────────────┐
│   Subagent Instance     │
│                         │
│  - Own context window   │
│  - Custom system prompt │
│  - Tool permissions     │
│  - Model selection      │
│                         │
│  Executes autonomously  │
│  ↓                      │
│  Returns results        │
└─────────────────────────┘
    ↓
    Results integrated back
    ↓
Main Claude Code Instance
```

## Subagent Lifecycle

1. **Activation:**
   - Main instance recognizes task matching subagent description
   - OR explicit invocation by user or instruction

2. **Invocation:**
   - Task tool called with subagent_type parameter
   - Subagent receives task description and context

3. **Execution:**
   - Subagent runs with its system prompt
   - Uses granted tools to complete task
   - Operates in isolated context window

4. **Completion:**
   - Subagent returns complete results
   - Results integrate into main conversation
   - Main instance continues with enriched information

## File Storage Locations

### Project-Level Subagents
**Location:** `.claude/agents/your-agent.md`

**When to use:**
- Team-shared workflows
- Project-specific automation
- Versioned with codebase
- Consistent across team members

**Benefits:**
- ✅ Version controlled (git)
- ✅ Team collaboration
- ✅ Project-specific context
- ✅ Consistency across developers

### User-Level Subagents
**Location:** `~/.claude/agents/your-agent.md`

**When to use:**
- Personal workflows
- Cross-project automation
- Private tools
- Individual preferences

**Benefits:**
- ✅ Available in all projects
- ✅ Private (not committed)
- ✅ Personal customization
- ✅ Portable across projects

## Built-in Subagents

Claude Code ships with several built-in subagents:

### Plan Subagent
- **Purpose:** Research and planning during plan mode
- **Tools:** Read, Glob, Grep, Bash (read-only operations)
- **Model:** Sonnet
- **Activation:** Automatically when entering plan mode

### Additional Built-ins
The specific set varies by Claude Code version. Check `/agents` command to see current built-ins.

## Activation Methods

### Automatic Activation
Claude recognizes when task matches subagent description:

```markdown
User: "Review this code for security issues"

Claude recognizes → Invokes security-reviewer subagent
```

**Key:** Description must clearly specify trigger keywords and context.

### Explicit Invocation
User or instructions directly request subagent:

```markdown
User: "Use the code-reviewer subagent to analyze my changes"

Claude directly invokes → code-reviewer subagent
```

### Programmatic Invocation
System prompts or workflows can invoke subagents:

```markdown
"After implementation, invoke the test-creator subagent
to generate comprehensive tests."
```

## Best Use Cases

### Code Quality & Review
- Security vulnerability scanning
- Performance analysis
- Best practices enforcement
- Code style compliance

### Testing & QA
- Test suite generation
- Visual regression testing
- Integration test creation
- Test coverage analysis

### Research & Analysis
- Codebase exploration
- Dependency analysis
- Architecture documentation
- Technical research

### Automation & Deployment
- Build pipeline execution
- Deployment automation
- Environment setup
- Configuration management

### Documentation
- API documentation generation
- README creation
- Code comment enhancement
- Architecture diagram generation

## Performance Considerations

### Context Window
Each subagent has its own context window:
- Pro: Main conversation stays focused
- Con: Subagent doesn't see entire main conversation
- Solution: Pass necessary context in invocation

### Model Selection
Choose model based on task:
- **Haiku:** Fast, cheap, simple tasks
- **Sonnet:** Balanced, most use cases (default)
- **Opus:** Complex reasoning, expensive

### Tool Permissions
Restrict tools for:
- **Security:** Limit potentially dangerous operations
- **Performance:** Reduce decision overhead
- **Focus:** Prevent tool misuse

## Security Considerations

### Principle of Least Privilege
Only grant tools absolutely necessary:

```yaml
# Too broad
tools: *  # Grants ALL tools (dangerous)

# Better
tools: Read, Grep, Glob  # Only read operations

# Best
tools: Read  # Minimal for task
```

### Dangerous Tool Combinations
Be cautious with:
- `Write + Bash` - Can modify and execute
- `Edit + Bash` - Can alter and run code
- `Bash` alone - Command execution

### Safe Tool Sets
Read-only analysis:
```yaml
tools: Read, Grep, Glob, WebFetch
```

Code generation (controlled):
```yaml
tools: Read, Write, Grep, Glob
```

## Common Patterns

### Specialist Pattern
Create domain-specific experts:
- `python-expert` - Python best practices
- `react-specialist` - React component patterns
- `sql-optimizer` - Database query optimization

### Workflow Pattern
Automate end-to-end processes:
- `code-review-workflow` - Review → Report → Suggestions
- `test-pipeline` - Generate → Execute → Report
- `deploy-automation` - Build → Test → Deploy

### Research Pattern
Deep analysis and investigation:
- `architecture-analyzer` - Codebase structure analysis
- `dependency-auditor` - Security and version checking
- `performance-profiler` - Bottleneck identification

## Next Steps

- [Subagent Structure](subagent_structure.md) - File format and YAML reference
- [Activation Patterns](activation_patterns.md) - Writing effective descriptions
- [System Prompts](system_prompts.md) - Crafting quality prompts
- [Tool Permissions](tool_permissions.md) - Security and tool selection
- [Model Selection](model_selection.md) - Choosing the right model
