# Session Workflow Directives

**Purpose**: Guidelines for session initialization, development notes, and documentation updates.

**Last Updated**: 2025-11-28

---

## Session Initialization

### At Start of Every Session

**BEFORE any work, you MUST:**

1. **Read development status**:
   - `claude-config/development-status.md` (identifies current notes file)

2. **Read current development notes**:
   - `project-notes/development-notes-archive/development-notes_XXX.md` (most recent)
   - Understand recent decisions, architecture, constraints

3. **Determine notes file index**:
   - Check `development-status.md` for current index number
   - If starting new session, increment: `development-notes_006.md` → `development-notes_007.md`
   - **IMPORTANT**: Always check existing files to avoid duplicates

### Why This Matters

- Maintains context across sessions
- Prevents re-introducing refactored patterns
- Understands architectural decisions already made
- Avoids duplicating work

---

## Development Notes System

### File Structure

**Location**: `project-notes/development-notes-archive/`

**Naming**: `development-notes_<INDEX>.md`
- `development-notes_000.md` (archived)
- `development-notes_001.md` (archived)
- ...
- `development-notes_006.md` (current - check development-status.md for latest)

### File Purpose

Each file contains:
- **Design decisions**: Why choices were made
- **Architecture notes**: System structure, patterns established
- **Implementation details**: Key technical decisions
- **Actions and results**: What was done, what happened
- **Files produced**: New files created or modified
- **Resources used**: Important references, APIs, docs
- **Timestamps**: When work was done
- **Time estimates**: Predicted vs actual time for major work

### Size Guidelines

- **Target**: ~6,000 tokens per file
- **Purpose**: Fast loading, digestible chunks
- **When to create new**: Current file approaches 6,000 tokens
- **Archive old**: Previous files remain for history (DO NOT MODIFY)

### Update Triggers

**Update notes file immediately when:**
- Making architecture/design decisions
- Discovering new API capabilities or bugs
- Implementing major features
- Identifying important constraints or trade-offs
- Any material discovery relevant to future work

**DO NOT wait until end of session** - update as you go!

---

## Development Status File

### File: `claude-config/development-status.md`

**Purpose**: Lightweight summary of current state

**Contains**:
- Current development notes file number
- Latest work summary (1-2 paragraphs)
- Current phase/status
- Recent achievements
- Next steps

**Does NOT contain**:
- Full history (that's in development-notes files)
- Detailed explanations (that's in development-notes files)

### Update Triggers

**Update status file when:**
- Goals achieved
- Todo items completed
- Development notes file updated
- Phase transitions
- Major milestones reached

---

## Workflow Pattern

### Standard Session Flow

```
1. Session Start
   ├─ Read development-status.md
   ├─ Identify current development-notes_XXX.md
   └─ Read current development notes

2. During Work
   ├─ Make decisions → Update notes immediately
   ├─ Complete milestones → Update status
   └─ Discover important info → Document in notes

3. Throughout Session (not end!)
   ├─ Keep notes updated as work progresses
   └─ Update status on significant changes

4. File Size Check
   └─ Approaching 6k tokens? → Create new indexed file
```

### Creating New Development Notes File

**When**: Starting new session or current file approaches 6,000 tokens

**How**:
1. **Check current index**: Read `development-status.md` for current notes file number
2. **Verify no conflicts**: List `project-notes/development-notes-archive/` to ensure next index doesn't exist
3. **Create new file**: `project-notes/development-notes-archive/development-notes_<NEXT>.md`
4. **Add header** with date and session info
5. **Update development-status.md** to reference new file
6. **DO NOT delete or modify old files** (archive for history)

**CRITICAL**: Always create files in `project-notes/development-notes-archive/`, NOT in `claude-config/`

**Example**:
```markdown
# Development Notes - Session 007
**Date**: 2025-11-26
**Previous**: development-notes_006.md

## Session Overview
...
```

---

## Documentation Structure

### Current Documentation Hierarchy

```
project-notes/
└── development-notes-archive/
    ├── development-notes_000.md (archived)
    ├── development-notes_001.md (archived)
    ├── development-notes_002.md (archived)
    ├── development-notes_003.md (archived)
    ├── development-notes_004.md (archived)
    ├── development-notes_005.md (archived)
    └── development-notes_006.md (current - check development-status.md)

claude-config/
├── development-status.md (current state summary - ALWAYS check this first)
└── directives/
    ├── directives-session-workflow.md (this file)
    └── ...other directives
```

**NOTE**: All development notes belong in `project-notes/development-notes-archive/`
**NEVER** create development-notes files in `claude-config/`

---

## Rules

### Archived Files (DO NOT)
- ❌ Open archived development-notes files
- ❌ Delete archived development-notes files
- ❌ Modify archived development-notes files

**Why**: Historical record must remain intact

### Current Files (DO)
- ✅ Update current development-notes throughout session
- ✅ Add timestamped entries as work progresses
- ✅ Document decisions when made (not later)
- ✅ Create new file when approaching size limit

---

## Content Guidelines

### What to Document

**Design Decisions:**
```markdown
**Decision**: Use voxel grid + IDW instead of RBF
**Rationale**: Better accuracy (8.59° vs 10°), O(1) lookup
**Date**: 2025-10-26
**Impact**: Changes model architecture, requires new training
```

**Implementation Details:**
```markdown
**Implementation**: Added shoulder/elbow to JSON output
**Files Modified**: src/arm_processor.py (lines 229-255)
**Reason**: Enable full skeleton visualization
**Trade-off**: File size +82% (62KB → 113KB)
```

**Time Tracking:**
```markdown
**Task**: Refactor visualization scripts
**Estimate**: 2-3 hours
**Actual**: 4 hours
**Reason for variance**: Found more duplicated code than expected
```

### What NOT to Document

- ❌ Verbose prose
- ❌ Code dumps (reference file:line instead)
- ❌ Obvious implementation details
- ❌ Temporary debugging notes

---

## Git Commit Messages

### Commit Message Guidelines

**DO NOT include Claude attribution in git commits:**
- ❌ `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- ❌ `Co-Authored-By: Claude <noreply@anthropic.com>`

**DO write clear, informative commit messages:**
- ✅ Focus on what changed and why
- ✅ List key files modified/created
- ✅ Include relevant context for reviewers
- ✅ Keep messages professional and concise

**Example Good Commit:**
```
Implement .unsanim format: domain-agnostic animation file format

Created new unified animation file format to replace split JSON format.

Key Features:
- Line-based text for fast scanning
- 50% file size reduction vs JSON
	- Channel-c2e4ntric storage

New Files:
- python/src/animation_io.py (Core I/O library)
- python/tests/test_animation_io.py (Unit tests)

Testing: All tests passing, data verified
```

---

## Quick Reference

### Session Checklist

```markdown
- [ ] Read claude-config/development-status.md (find current index)
- [ ] List project-notes/development-notes-archive/ (verify files)
- [ ] Read current development-notes_XXX.md from archive
- [ ] If new session: create next index in project-notes/development-notes-archive/
- [ ] Update notes as decisions are made
- [ ] Update status on milestones
- [ ] Check file size (~6k tokens?)
```

### File Locations

| File | Location | Purpose |
|------|----------|---------|
| Current notes | `project-notes/development-notes-archive/development-notes_XXX.md` | Detailed session log |
| Status | `claude-config/development-status.md` | Current state summary |
| Archived notes | `project-notes/development-notes-archive/development-notes_000-NNN.md` | Historical record |

---

## Related Files

- **Development status**: `claude-config/development-status.md`
- **Current notes**: Check `development-status.md` for file number
- **Other directives**: `claude-config/directives/`

---
