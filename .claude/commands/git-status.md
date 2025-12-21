---
description: Show git status with context about recent work
---

Provide a comprehensive git status overview with context.

## Steps

1. **Basic status**: Run `git status` and summarize:
   - Current branch
   - Ahead/behind remote
   - Staged changes count
   - Unstaged changes count
   - Untracked files count

2. **Recent commits**: Show last 5 commits with `git log --oneline -5`

3. **Changed files summary**: Group changes by directory/type.

4. **Large files check**: Warn about any files that might be too large for GitHub (>50MB warning, >100MB error).

5. **Actionable suggestions**:
   - If uncommitted changes: suggest commit or stash
   - If ahead of remote: suggest push
   - If behind remote: suggest pull
   - If untracked files: suggest staging or .gitignore
