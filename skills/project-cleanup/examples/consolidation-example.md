# Documentation Consolidation Example

Example of consolidating overlapping documentation files.

## Scenario

Two documentation files with significant overlap:
- `architecture.md` (245 lines)
- `design-decisions.md` (189 lines)

## Detection

```bash
$ python detect-duplicates.py .

Found 1 potentially overlapping document pair:

[1] OVERLAP: Moderate overlap, consider consolidation
    Doc 1: architecture.md (245 lines)
    Doc 2: design-decisions.md (189 lines)
    Heading similarity: 45%
    Content similarity: 38%
    Shared headings: 8
    Examples: system architecture, component design, database schema
```

## Analysis

**architecture.md headings:**
- System Overview
- Component Architecture
- Database Schema
- API Architecture
- Technology Stack
- Performance Considerations
- Scalability
- Security Model

**design-decisions.md headings:**
- Design Philosophy
- Component Design
- Data Model
- API Design
- Technology Choices
- Trade-offs
- Future Considerations

**Overlap:**
- Component architecture/design (85% similar)
- Database schema/data model (100% same)
- API architecture/design (75% similar)
- Technology stack/choices (90% similar)

**Unique to architecture.md:**
- System Overview
- Performance Considerations
- Scalability
- Security Model

**Unique to design-decisions.md:**
- Design Philosophy
- Trade-offs
- Future Considerations

## Consolidation Plan

**Target file:** `docs/architecture.md`
**Archived file:** `docs/.archive/design-decisions.md`

**Merge strategy:**
1. Keep architecture.md as base (more comprehensive)
2. Add unique sections from design-decisions.md:
   - Design Philosophy (new section 1)
   - Trade-offs subsection (add to Component Design)
   - Future Considerations (new final section)
3. Merge overlapping sections (take more detailed version)
4. Update cross-references
5. Archive old file

## Result

**New docs/architecture.md structure (312 lines):**
```markdown
# System Architecture and Design

## Design Philosophy
(Added from design-decisions.md)
- Simplicity over complexity
- Modular design
- Test-driven development

## System Overview
(From architecture.md)
...

## Component Design
(Merged from both)
...

### Trade-offs
(Added from design-decisions.md)
...

## Database Schema
(From architecture.md - was identical)
...

## API Architecture
(Merged from both)
...

## Technology Stack and Choices
(Merged from both)
...

## Performance Considerations
(From architecture.md)
...

## Scalability
(From architecture.md)
...

## Security Model
(From architecture.md)
...

## Future Considerations
(Added from design-decisions.md)
...
```

**Archived docs/.archive/design-decisions.md:**
```markdown
# ARCHIVED

This content has been merged into [architecture.md](../architecture.md).

This file is preserved for git history reference only.

Last updated: 2024-11-01

---

(Original content preserved below)
...
```

## Updated Links

Files referencing `design-decisions.md`:
- `docs/deployment.md`: design-decisions.md → architecture.md
- `docs/user-guide.md`: design-decisions.md → architecture.md
- `README.md`: design-decisions.md → architecture.md
- `CONTRIBUTING.md`: design-decisions.md → architecture.md

## Git Commits

```bash
# Merge docs
# (manual merge of content)

# Archive old file
mkdir -p docs/.archive
git mv docs/design-decisions.md docs/.archive/

# Update links in all files
# (automated with scripts/update-links.py)

# Commit
git add docs/
git commit -m "docs: consolidate architecture documentation

- Merged design-decisions.md into architecture.md
- Added design philosophy and trade-offs sections
- Archived old design-decisions.md for history
- Updated 4 files with new links
- Result: Single comprehensive architecture document (312 lines)

Co-authored-by: project-cleanup skill"
```

## Benefits

- **Single source of truth** for architecture
- **No duplication** - easier to maintain
- **More comprehensive** - combines best from both
- **Git history preserved** - can find original via archive
- **Links updated** - no broken references

## See Also

- [messy-project-before.md](messy-project-before.md)
- [clean-project-after.md](clean-project-after.md)
- [integration-example.md](integration-example.md)
