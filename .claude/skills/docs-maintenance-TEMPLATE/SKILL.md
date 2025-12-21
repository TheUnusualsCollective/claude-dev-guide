---
name: docs-maintenance
description: Proactively identify and flag outdated documentation. When modifying code, check if related docs need updating or removal.
---

<!--
TEMPLATE: Rename directory from "docs-maintenance-TEMPLATE" to "docs-maintenance" to activate.
-->

# Documentation Maintenance Skill

Keeps documentation accurate by aggressively removing outdated content.

## Scope

**This skill manages:**
- README files
- `docs/` directory
- Code comments and docstrings
- API documentation
- Any `.md` files NOT in development notes

**Does NOT touch:**
- Development notes (managed by session-management)
- Development status file (managed by session-management)

Development notes are session context, not permanent documentation.

## Core Philosophy

**Outdated documentation is worse than no documentation.**

- It misleads developers
- Wastes time on wrong approaches
- Erodes trust in all documentation

**When in doubt, DELETE.** Git preserves history if recovery is needed.

## When to Auto-Invoke

**During Code Changes** - When:
- Modifying a function that has docstrings
- Changing API signatures or interfaces
- Removing or renaming files
- Changing configuration formats

**During Session Review** - When:
- Session end is approaching
- Major feature is complete
- Refactoring is done

## Behaviors

### While Working
- Notice when code changes invalidate nearby documentation
- Flag inline comments that reference changed behavior
- Alert when README mentions modified features

### Red Flags to Watch For
- References to deleted files/functions
- "TODO" or "FIXME" for completed work
- "Will be implemented" for existing features
- Workarounds for fixed bugs

### What to Preserve
- Architecture decisions (the "why")
- Design rationale
- Non-obvious constraints

### What to Delete
- Outdated how-to guides
- Wrong API documentation
- Obsolete setup instructions
- Descriptions of removed features

## Actions

When outdated docs are found:
1. **Inform user**: "This documentation appears outdated because..."
2. **Recommend action**: Delete, update, or flag for review
3. **Execute if approved**: Remove or update the content
4. **No hesitation**: Bias toward deletion over preservation

## Manual Command

Users can explicitly invoke:
- `/docs-cleanup` - Full documentation audit
