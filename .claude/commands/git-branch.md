---
description: Create or switch branches with naming conventions
---

Help manage git branches with consistent naming.

## Steps

1. **Show current state**:
   - Current branch
   - List of local branches
   - Any uncommitted changes (warn if present)

2. **Determine action**: Ask user:
   - Create new branch?
   - Switch to existing branch?
   - List all branches (including remote)?

3. **For new branch**:
   - Ask for branch purpose (feature, fix, experiment, etc.)
   - Ask for short description
   - Generate branch name following convention
   - Confirm with user before creating

4. **Create/switch**: Execute the branch operation.

## Branch Naming Convention

```
<type>/<short-description>
```

Types:
- `feature/` - New functionality
- `fix/` - Bug fixes
- `experiment/` - Exploratory work
- `refactor/` - Code restructuring
- `docs/` - Documentation updates
- `wip/` - Work in progress (temporary)

## Safety Checks

- Warn if uncommitted changes exist before switching
- Confirm before creating branch from non-main base
- Suggest stashing changes if needed
