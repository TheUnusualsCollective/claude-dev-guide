---
description: Aggressively remove outdated or inaccurate documentation
---

Review and clean up documentation to keep it accurate and useful.

## Core Principle

**Outdated docs are worse than no docs.** They mislead, waste time, and erode trust.

When in doubt, DELETE. Git preserves history if recovery is needed.

## What You MUST Do

- **Verify against code** before updating any documentation
- **Delete outdated content** that no longer reflects reality
- **Consolidate redundant info** into single sources of truth
- **Check recent commits** to understand what changed
- **Report all changes** with clear reasoning

## What You MUST NOT Do

- **NEVER** preserve documentation "just in case"
- **NEVER** document features that don't exist
- **NEVER** leave TODO items for completed work
- **NEVER** keep descriptions of removed features
- **NEVER** update docs without verifying against actual code

## Methodology

### 1. Audit Phase
Identify documentation files:
- `*.md` files (except development notes archives)
- `docs/` directory
- README files
- Inline comments with "TODO", "FIXME", "deprecated"

### 2. Verification Phase
For each document, evaluate:
- Does the code it describes still exist?
- Is this still accurate?
- Would someone be misled by this?
- When was it last updated vs related code?

### 3. Action Phase
| Finding | Action |
|---------|--------|
| Outdated, wrong, or describes removed features | **Delete** |
| Mostly accurate but needs minor fixes | **Update** |
| Uncertain about accuracy | **Flag for user review** |

## Decision Framework

When deciding what to do:
1. Does the referenced code/feature exist? -> If no, DELETE
2. Is the information accurate? -> If no, UPDATE or DELETE
3. Is this duplicated elsewhere? -> If yes, CONSOLIDATE
4. Are you uncertain? -> FLAG for user, don't guess

## Red Flags (Likely Outdated)

- References to files/functions that no longer exist
- Describes APIs or interfaces that have changed
- Mentions "will be implemented" for things already done
- Describes workarounds for bugs that were fixed
- Documents deprecated approaches

## What to Keep

- Architecture decisions (the "why" rarely becomes outdated)
- Design rationale and constraints
- Setup/installation instructions (if verified working)
- API documentation (if actively maintained)

## Output Format

```
Documentation Cleanup Report

DELETED:
- docs/old-api.md (API no longer exists)
- README section on deprecated feature

UPDATED:
- docs/setup.md (fixed outdated commands)

FLAGGED FOR REVIEW:
- docs/architecture.md (may be outdated, please verify)
```
