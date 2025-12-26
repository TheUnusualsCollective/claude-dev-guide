---
name: docs-maintenance
description: Proactively identify and flag outdated documentation. When modifying code, check if related docs need updating or removal.
---

<!--
TEMPLATE: Rename directory from "docs-maintenance-TEMPLATE" to "docs-maintenance" to activate.
-->

# Documentation Maintenance Skill

Keeps documentation accurate by aggressively removing outdated content.

## Core Principle

**Outdated documentation is worse than no documentation.**

It misleads developers, wastes time on wrong approaches, and erodes trust.

**When in doubt, DELETE.** Git preserves history if recovery is needed.

## What You MUST Do

- **Verify against code** before updating any documentation
- **Delete outdated content** that no longer reflects reality
- **Flag changed docs** when code changes invalidate them
- **Inform user** with clear reasoning when outdated docs are found
- **Bias toward deletion** over preservation

## What You MUST NOT Do

- **NEVER** preserve documentation "just in case"
- **NEVER** document features that don't exist
- **NEVER** leave TODO items for completed work
- **NEVER** keep descriptions of removed features
- **NEVER** update docs without verifying against actual code

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

## Decision Framework

When deciding what to do:
1. Does the referenced code/feature exist? -> If no, DELETE
2. Is the information accurate? -> If no, UPDATE or DELETE
3. Is this duplicated elsewhere? -> If yes, CONSOLIDATE
4. Are you uncertain? -> FLAG for user, don't guess

## Red Flags (Likely Outdated)

- References to deleted files/functions
- "TODO" or "FIXME" for completed work
- "Will be implemented" for existing features
- Workarounds for fixed bugs
- Describes APIs or interfaces that have changed

## What to Preserve

- Architecture decisions (the "why" rarely becomes outdated)
- Design rationale and constraints
- Non-obvious constraints

## What to Delete

- Outdated how-to guides
- Wrong API documentation
- Obsolete setup instructions
- Descriptions of removed features

## Actions

When outdated docs are found:
1. **Inform user**: "This documentation appears outdated because..."
2. **Recommend action**: Delete, update, or flag for review
3. **Execute if approved**: Remove or update the content

## Manual Command

Users can explicitly invoke:
- `/docs-cleanup` - Full documentation audit
