---
description: Guide through staging, commit message, and optional push
---

Help create a well-structured git commit.

## Steps

1. **Check status**: Run `git status` to show:
   - Staged changes
   - Unstaged changes
   - Untracked files

2. **Review changes**: Run `git diff --staged` and `git diff` to understand what will be committed.

3. **Stage files** (if needed): Ask user which files to stage, or suggest based on related changes.

4. **Draft commit message**:
   - Summarize the nature of changes (feature, fix, refactor, docs, etc.)
   - Use imperative mood ("Add feature" not "Added feature")
   - Keep first line under 50 characters if possible
   - Add body with more detail if needed
   - Do NOT include Claude attribution

5. **Present for review**: Show the proposed commit message and ask for confirmation or edits.

6. **Create commit**: Execute the commit.

7. **Ask about push**: "Would you like to push to remote?"

## Commit Message Format

```
<type>: <short summary>

<optional body with more detail>
```

Types: feat, fix, refactor, docs, test, chore, style
