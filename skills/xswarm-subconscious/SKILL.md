---
name: xswarm-subconscious
description: Subconscious memory — store important decisions, constraints, and patterns
user-invocable: false
---

# Subconscious Memory

You have a persistent subconscious memory that automatically surfaces relevant context. When you make important decisions, discover constraints, encounter gotchas, establish patterns, or define processes, store them for future recall.

## When to Store

Store memories when you encounter:
- **Decisions** — technology choices, architectural decisions, tradeoffs made
- **Constraints** — hard requirements, limitations, compatibility issues
- **Gotchas** — surprising behaviors, non-obvious pitfalls, debugging insights
- **Patterns** — established conventions, naming patterns, code organization rules
- **Processes** — workflows, deployment steps, review procedures

Do NOT store: verbose output, raw code blocks, secrets/credentials, trivial facts.

## How to Store

Run this command via Bash:

```bash
xswarm-subconscious store \
  --text "Original conversational context with full detail for later reference" \
  --summary "Concise standardized notation optimized for search matching" \
  --tags "comma,separated,labels" \
  --category decision \
  --importance 2 \
  --topic "domain:specific-key" \
  --keywords "predictive,search,terms,future,queries,might,use"
```

### Parameters

- `--text` (required): The original context — preserve conversational detail, reasoning, and nuance. This is what a human reads later.
- `--summary` (required): Simplified, standardized notation using canonical technical terms. This is what FTS5 searches against. Use consistent terminology.
- `--tags`: Comma-separated labels for faceted lookup (e.g., "decision:db,libsql,storage,backend")
- `--category`: One of: decision, constraint, process, pattern, gotcha, progress, context
- `--importance`: 0 (background) to 3 (critical). Default 1. Use 2+ for decisions that would be costly to re-derive.
- `--topic`: Decision topic key for versioning (e.g., "stack:db", "auth:method"). When a new decision supersedes an old one on the same topic, the old one is automatically marked superseded.
- `--keywords`: Predictive search terms — words that a FUTURE prompt might contain when this memory would be relevant. Think: "what question would someone ask that this answers?"

### Quality Guidelines

**Summary** should be standardized: "Using libsql with FTS5 for embedded search" not "we decided to go with that sql lite thing"

**Keywords** should be predictive: for a database decision, include "database", "storage", "persistence", "query", "sql", "embed" — terms future prompts might contain.

**Topics** enable versioning: if you store `--topic "stack:db"` and later store another decision with the same topic, the first is automatically superseded. Always use topics for decisions.

## Examples

### Decision
```bash
xswarm-subconscious store \
  --text "After evaluating SQLite, PostgreSQL, and libsql, chose libsql for embedded use with FTS5 support. Key factors: zero-config, built-in full-text search, no external process needed." \
  --summary "Using libsql with FTS5 for embedded database — zero config, built-in full-text search" \
  --tags "decision:db,libsql,fts5,storage" \
  --category decision \
  --importance 2 \
  --topic "stack:db" \
  --keywords "database,storage,persistence,sql,sqlite,embed,search,query"
```

### Gotcha
```bash
xswarm-subconscious store \
  --text "libsql client execute() only accepts single SQL statements. Attempting to pass multiple semicolon-separated statements causes a silent failure. Must call execute() separately for each statement." \
  --summary "libsql execute() accepts only single SQL statements — call separately for each" \
  --tags "gotcha,libsql,sql,execute" \
  --category gotcha \
  --importance 2 \
  --keywords "libsql,execute,multiple,statements,sql,batch,error,silent"
```

### Constraint
```bash
xswarm-subconscious store \
  --text "Node.js 18+ required because we use built-in test runner and top-level await" \
  --summary "Requires Node.js 18+ for built-in test runner and top-level await" \
  --tags "constraint,nodejs,version,runtime" \
  --category constraint \
  --importance 1 \
  --keywords "node,version,require,minimum,runtime,compatibility"
```
