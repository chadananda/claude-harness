# Documentation Consolidation Strategies

Guide to detecting duplicate/overlapping documentation and consolidating effectively.

## When to Consolidate

### Situations Requiring Consolidation

**1. Duplicate Documentation**
- Two docs with same title/topic
- Example: `architecture.md` AND `system-design.md` both describing system architecture
- **Overlap >70%**: Very likely duplicates

**2. Overlapping Content**
- Two docs with similar headings/topics
- Example: `api-guide.md` AND `api-reference.md` both documenting same endpoints
- **Overlap 30-70%**: Moderate overlap, user decision

**3. Scattered Information**
- Multiple small docs that should be one comprehensive guide
- Example: `setup-mac.md`, `setup-linux.md`, `setup-windows.md` → `installation-guide.md`
- **Best as single doc**: If <500 lines each

### Situations to KEEP Separate

**1. Different Audiences**
- `user-guide.md` (end users) vs `developer-guide.md` (contributors)
- Different perspective, vocabulary, detail level

**2. Different Lifecycles**
- `CHANGELOG.md` (updated frequently) vs `API.md` (stable)
- Separate files easier to maintain

**3. Different Formats**
- `api.md` (markdown reference) vs `openapi.yaml` (machine-readable spec)
- Serve different purposes

**4. Intentionally Separate**
- Architecture Decision Records (ADRs) intentionally atomic
- Each ADR is its own document by design

---

## Overlap Detection Algorithm

### Heading-Based Similarity

```python
import re
from typing import List, Set

def extract_headings(markdown_content: str) -> List[str]:
    """Extract all markdown headings from content"""
    headings = []
    for line in markdown_content.split('\n'):
        if line.startswith('#'):
            # Remove # symbols and clean
            heading = line.lstrip('#').strip().lower()
            headings.append(heading)
    return headings

def calculate_heading_overlap(doc1: str, doc2: str) -> float:
    """Calculate percentage of overlapping headings"""
    headings1 = set(extract_headings(doc1))
    headings2 = set(extract_headings(doc2))

    if not headings1 or not headings2:
        return 0.0

    # Jaccard similarity
    intersection = headings1 & headings2
    union = headings1 | headings2

    similarity = len(intersection) / len(union)
    return similarity

def detect_overlap_category(similarity: float) -> str:
    """Categorize overlap level"""
    if similarity > 0.7:
        return "DUPLICATE"  # Very high overlap
    elif similarity > 0.3:
        return "OVERLAP"    # Moderate overlap
    else:
        return "DISTINCT"   # Keep separate
```

### Content-Based Similarity

```python
from difflib import SequenceMatcher

def calculate_content_similarity(doc1: str, doc2: str) -> float:
    """Calculate overall content similarity"""
    # Remove code blocks (often similar across docs)
    doc1_clean = remove_code_blocks(doc1)
    doc2_clean = remove_code_blocks(doc2)

    # Calculate similarity
    matcher = SequenceMatcher(None, doc1_clean, doc2_clean)
    return matcher.ratio()

def remove_code_blocks(markdown: str) -> str:
    """Remove code blocks from markdown"""
    # Remove ```...``` blocks
    pattern = r'```[\s\S]*?```'
    return re.sub(pattern, '', markdown)
```

### Semantic Similarity (Advanced)

```python
def calculate_semantic_similarity(doc1: str, doc2: str) -> float:
    """Calculate semantic similarity using embeddings"""
    # Extract key phrases from each doc
    phrases1 = extract_key_phrases(doc1)
    phrases2 = extract_key_phrases(doc2)

    # Compare using word overlap or embeddings
    # (Implementation depends on available NLP libraries)
    pass
```

---

## Consolidation Strategies

### Strategy 1: Merge Into Single Document

**When to use:**
- High overlap (>70%)
- Same audience and purpose
- Combined length <2000 lines

**Process:**
1. Choose comprehensive title
2. Merge unique sections from both
3. Remove duplicate content
4. Update cross-references
5. Archive old files

**Example:**

**Before:**
```
docs/architecture.md (1,200 lines)
  - System Overview
  - Component Design
  - Database Schema
  - API Architecture

docs/design-doc.md (800 lines)
  - System Design
  - Components
  - Data Model
  - API Design
```

**After:**
```
docs/architecture.md (1,500 lines)
  - System Overview
  - Architecture Principles (from design-doc)
  - Component Design (merged)
  - Database Schema
  - API Architecture (merged)

docs/.archive/design-doc.md
  - ARCHIVED: Content moved to architecture.md
  - (Preserved for git history)
```

### Strategy 2: Create Hierarchy

**When to use:**
- Related but distinct topics
- One is high-level, one is detailed
- Combined would be too long (>3000 lines)

**Process:**
1. Identify high-level overview doc
2. Move detailed sections to subdocs
3. Link from overview to details
4. Create index in overview

**Example:**

**Before:**
```
docs/api-documentation.md (3,500 lines)
  - API Overview
  - Authentication
  - Users API (500 lines)
  - Products API (600 lines)
  - Orders API (700 lines)
  - Webhooks (400 lines)
```

**After:**
```
docs/api/README.md (200 lines)
  - API Overview
  - Authentication
  - Endpoints:
    - [Users API](users.md)
    - [Products API](products.md)
    - [Orders API](orders.md)
    - [Webhooks](webhooks.md)

docs/api/users.md (500 lines)
docs/api/products.md (600 lines)
docs/api/orders.md (700 lines)
docs/api/webhooks.md (400 lines)
```

### Strategy 3: Split by Audience

**When to use:**
- Same topic, different audiences
- Overlap but different detail levels
- Different terminology/perspective

**Process:**
1. Identify distinct audiences
2. Create audience-specific docs
3. Extract shared content to separate doc
4. Link from each to shared concepts

**Example:**

**Before:**
```
docs/deployment.md (mixed audience)
  - Deployment Overview
  - Prerequisites
  - Using the Web UI (for users)
  - Kubernetes Configuration (for ops)
  - CLI Reference (for developers)
  - Troubleshooting
```

**After:**
```
docs/deployment/README.md (Overview)
  - What is Deployment
  - Architecture
  - → [User Guide](user-guide.md)
  - → [Operations Guide](ops-guide.md)
  - → [Developer Reference](dev-reference.md)

docs/deployment/user-guide.md
  - Using the Web UI
  - Basic Troubleshooting

docs/deployment/ops-guide.md
  - Kubernetes Configuration
  - Monitoring
  - Advanced Troubleshooting

docs/deployment/dev-reference.md
  - CLI Reference
  - API Integration
```

### Strategy 4: Extract Common Sections

**When to use:**
- Multiple docs share introduction/concepts
- Common prerequisites or setup
- Shared terminology

**Process:**
1. Extract common sections
2. Create shared concepts doc
3. Link from each doc to shared concepts
4. Remove duplicate content

**Example:**

**Before:**
```
docs/user-guide.md
  - Introduction to the System
  - Core Concepts (Authentication, Permissions, ...)
  - User Tasks

docs/developer-guide.md
  - Introduction to the System (duplicate)
  - Core Concepts (duplicate)
  - Development Setup
```

**After:**
```
docs/README.md
  - Introduction to the System
  - Core Concepts
  - → [User Guide](user-guide.md)
  - → [Developer Guide](developer-guide.md)

docs/user-guide.md
  - (Links to core concepts)
  - User Tasks

docs/developer-guide.md
  - (Links to core concepts)
  - Development Setup
```

---

## User Interaction Patterns

### Interactive Mode

```
Found overlapping documentation:

[1] docs/architecture.md (1,245 lines, updated 2024-11-10)
    Headings: System Architecture, Component Design, Database Schema, API Design

[2] docs/design-doc.md (892 lines, updated 2024-11-01)
    Headings: System Design, Component Structure, Data Model, API Specification

Overlap Analysis:
  Heading similarity: 65%
  Content similarity: 48%
  Recommendation: OVERLAP (moderate, ask user)

Options:
[1] Merge into single docs/architecture.md
[2] Create hierarchy (docs/architecture/README.md + subdocs)
[3] Keep separate (different purposes)
[4] Preview diff (see what's different)
[5] Skip (decide later)

Choice [1-5]: _
```

### Preview Diff

```
Unique to architecture.md:
  - Performance Considerations (section)
  - Scalability Architecture (section)
  - Technology Stack Decisions (section)

Unique to design-doc.md:
  - Design Principles (section)
  - User Flow Diagrams (section)
  - Wireframes (images)

Shared Content:
  - Component Design (very similar, 85% match)
  - Database Schema (identical, 100% match)
  - API Design (similar headings, different detail)

Recommendation:
  Merge into architecture.md, incorporate unique sections from design-doc:
  - Add "Design Principles" as new section
  - Add "User Flow Diagrams" under new "User Experience" section
  - Merge component sections (take best from each)
  - Use architecture.md's database schema (more detailed)

Proceed with merge? [y/n/customize]: _
```

### Auto Mode (Safe Defaults)

```python
def should_auto_consolidate(similarity: float, file1: Path, file2: Path) -> bool:
    """Determine if safe to auto-consolidate without asking"""
    # Never auto-consolidate without extremely high confidence
    if similarity < 0.9:
        return False

    # Check if both docs are recent (avoid consolidating with old/stale docs)
    age1 = get_file_age_days(file1)
    age2 = get_file_age_days(file2)

    if max(age1, age2) > 90:  # Older than 3 months
        return False  # Ask user

    # Check if either is very large
    size1 = file1.stat().st_size
    size2 = file2.stat().st_size

    if max(size1, size2) > 50000:  # >50KB
        return False  # Ask user

    # Safe to auto-consolidate
    return True
```

---

## Merging Process

### Step 1: Analyze Both Documents

```python
def analyze_docs(doc1_path: Path, doc2_path: Path) -> dict:
    """Analyze two documents for merging"""
    with open(doc1_path) as f1, open(doc2_path) as f2:
        content1 = f1.read()
        content2 = f2.read()

    return {
        'headings1': extract_headings(content1),
        'headings2': extract_headings(content2),
        'unique_to_1': find_unique_sections(content1, content2),
        'unique_to_2': find_unique_sections(content2, content1),
        'shared': find_shared_sections(content1, content2),
        'word_count1': len(content1.split()),
        'word_count2': len(content2.split()),
    }
```

### Step 2: Create Merge Plan

```python
def create_merge_plan(analysis: dict) -> dict:
    """Create plan for merging docs"""
    plan = {
        'target_file': 'docs/architecture.md',  # Keep more recent/comprehensive
        'sections_to_add': [],
        'sections_to_merge': [],
        'sections_to_remove': [],
    }

    # Add unique sections from doc2
    for section in analysis['unique_to_2']:
        plan['sections_to_add'].append({
            'title': section['title'],
            'content': section['content'],
            'insert_after': find_best_position(section)
        })

    # Merge overlapping sections
    for shared in analysis['shared']:
        plan['sections_to_merge'].append({
            'title': shared['title'],
            'strategy': 'take_more_detailed',  # or 'take_newer', 'combine'
        })

    return plan
```

### Step 3: Execute Merge

```python
def execute_merge(plan: dict, doc1_path: Path, doc2_path: Path):
    """Execute the merge plan"""
    # Read target doc
    with open(doc1_path) as f:
        content = f.read()

    # Add unique sections
    for section in plan['sections_to_add']:
        content = insert_section(content, section)

    # Merge overlapping sections
    for merge_item in plan['sections_to_merge']:
        content = merge_section(content, merge_item)

    # Write merged content
    with open(doc1_path, 'w') as f:
        f.write(content)

    # Archive old doc
    archive_path = doc2_path.parent / '.archive' / doc2_path.name
    archive_path.parent.mkdir(exist_ok=True)

    # Add archive notice
    with open(doc2_path, 'r') as f:
        old_content = f.read()

    archive_notice = f"""# ARCHIVED

This content has been moved to [{doc1_path.name}](../{doc1_path.name}).

This file is preserved for git history reference only.

---

{old_content}
"""

    with open(archive_path, 'w') as f:
        f.write(archive_notice)

    # Use git mv
    subprocess.run(['git', 'mv', str(doc2_path), str(archive_path)])
```

### Step 4: Update Links

```python
def update_links(old_path: str, new_path: str, project_root: Path):
    """Update all links to moved/merged documentation"""
    # Find all markdown files
    md_files = list(project_root.rglob('*.md'))

    updated_files = []

    for md_file in md_files:
        if md_file.name.startswith('.'):
            continue  # Skip hidden

        with open(md_file, 'r') as f:
            content = f.read()

        # Replace links
        old_link = f"]({old_path})"
        new_link = f"]({new_path})"

        if old_link in content:
            content = content.replace(old_link, new_link)

            with open(md_file, 'w') as f:
                f.write(content)

            updated_files.append(str(md_file))

    return updated_files
```

### Step 5: Verify No Broken Links

```python
def verify_links(project_root: Path) -> List[str]:
    """Check for broken markdown links"""
    broken_links = []

    md_files = list(project_root.rglob('*.md'))

    for md_file in md_files:
        with open(md_file, 'r') as f:
            content = f.read()

        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, content)

        for link_text, link_url in links:
            # Skip external links
            if link_url.startswith(('http://', 'https://', '#')):
                continue

            # Resolve relative path
            target = (md_file.parent / link_url).resolve()

            if not target.exists():
                broken_links.append({
                    'file': str(md_file),
                    'link': link_url,
                    'target': str(target)
                })

    return broken_links
```

---

## Consolidation Report

```
Documentation Consolidation Report
=================================

Merged Files:
  docs/architecture.md + docs/design-doc.md
  → docs/architecture.md (1,847 lines)

Changes:
  [+] Added "Design Principles" section (from design-doc.md)
  [+] Added "User Flow Diagrams" section (from design-doc.md)
  [~] Merged "Component Design" sections (took best from each)
  [-] Removed duplicate "Database Schema" (kept architecture.md version)

Archived:
  docs/.archive/design-doc.md (preserved for git history)

Updated Links:
  Updated 7 files:
    - src/README.md: design-doc.md → architecture.md
    - docs/deployment.md: design-doc.md → architecture.md
    - docs/api.md: design-doc.md → architecture.md
    - CONTRIBUTING.md: design-doc.md → architecture.md
    - README.md: design-doc.md → architecture.md
    - docs/guide.md: design-doc.md → architecture.md
    - docs/testing.md: design-doc.md → architecture.md

Verified:
  ✅ No broken links
  ✅ Git history preserved
  ✅ All cross-references updated

Next Steps:
  1. Review merged docs/architecture.md
  2. Update table of contents if needed
  3. Commit changes: git commit -m "docs: consolidate architecture documentation"
```

---

## Best Practices

### DO:
- ✅ Always ask user before consolidating (unless >90% duplicate)
- ✅ Archive old docs (don't delete)
- ✅ Update all links across project
- ✅ Preserve git history (use `git mv`)
- ✅ Verify no broken links after consolidation
- ✅ Provide preview/diff before merging
- ✅ Keep comprehensive title when merging

### DON'T:
- ❌ Auto-consolidate without high confidence
- ❌ Delete old docs (archive instead)
- ❌ Lose unique content during merge
- ❌ Break existing links
- ❌ Consolidate if different audiences
- ❌ Merge very long docs (>3000 lines combined)
- ❌ Consolidate ADRs or changelog-style docs

---

## Special Cases

### Architecture Decision Records (ADRs)

**Never consolidate ADRs** - they are intentionally atomic:
```
docs/adr/
  ├─ 001-use-postgresql.md
  ├─ 002-choose-react.md
  ├─ 003-adopt-microservices.md
  └─ README.md (index)
```

**Each ADR is separate by design.**

### API Documentation

**Consolidate if:**
- Multiple outdated API docs describing same endpoints
- Partial/incomplete docs that should be one comprehensive reference

**Keep separate if:**
- OpenAPI spec (machine-readable) vs guide (human-readable)
- Different API versions (v1, v2)
- Public API vs internal API

### Changelogs

**Never consolidate** `CHANGELOG.md` with other docs - it has specific format and lifecycle.

---

## See Also

- Main documentation: `../SKILL.md`
- File classification: `file-classification.md`
- Language patterns: `language-patterns.md`
- Edge cases: `edge-cases.md`
