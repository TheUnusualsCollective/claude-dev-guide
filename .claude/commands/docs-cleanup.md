---
description: Aggressively remove outdated or inaccurate documentation
---

Review and clean up documentation to keep it accurate and useful.

## Philosophy

**Outdated docs are worse than no docs.** They mislead, waste time, and erode trust.

When in doubt, DELETE. It's better to have no documentation than wrong documentation.

## Steps

1. **Identify documentation files**: Search for:
   - `*.md` files
   - `docs/` directory
   - Inline code comments mentioning "TODO", "FIXME", "deprecated"
   - README files

2. **For each document, evaluate**:
   - Is this still accurate?
   - Does the code it describes still exist?
   - Would someone be misled by this?
   - When was it last updated vs when was related code changed?

3. **Take action**:
   - **Delete**: If outdated, wrong, or describes removed features
   - **Update**: If mostly accurate but needs minor fixes
   - **Flag**: If uncertain, ask user for decision

4. **Report changes**: List what was deleted/updated and why.

## Red Flags (Likely Outdated)

- References to files/functions that no longer exist
- Describes APIs or interfaces that have changed
- Mentions "will be implemented" or "TODO" for things already done
- Describes workarounds for bugs that were fixed

## What to Keep

- Architecture decisions (even if implementation changed)
- "Why" explanations (reasoning rarely becomes outdated)
- Setup/installation instructions (verify they still work)

## Critical Rule

**Never preserve documentation "just in case."** Version control exists.
