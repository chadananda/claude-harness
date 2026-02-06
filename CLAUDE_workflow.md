# Workflow & Task Management

## Autonomy

Work autonomously until complete or blocked on a decision requiring human input.
- Never ask "should I proceed?" or "anything else?" - keep working
- Progress style: `Completed X. Committing... Moving to Y...`
- Pause only when genuinely stuck on a decision (invoke stuck agent)

## Task Management

Use native Tasks for all multi-step work:

```
TaskCreate with:
  - subject: brief title
  - description: detailed requirements
  - activeForm: "Doing X" (spinner text)

TaskUpdate with:
  - addBlockedBy: [task-ids] for dependencies
  - status: pending -> in_progress -> completed
```

Fan out parallel work as independent tasks with shared blockers.
After /plan completes, execute task groups via subagents automatically.

## Workflow Steps

1. **Setup**: Create .gitignore (tmp/, .claude/context/, node_modules/, dist/, .env), create directories, initial commit
2. **Route**: Simple request -> handle directly; Complex project -> /plan skill
3. **Plan**: /plan skill outputs native Tasks with DAG dependencies
4. **Execute**: Subagents handle each task following pipeline (coder -> reviewer -> tester -> doc)
5. **Commit**: After each task group
6. **Complete**: Integration test, version bump if applicable, final commit, report done
