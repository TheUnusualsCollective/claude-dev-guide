---
description: Create granular checkpoint commits on a work-in-progress branch
---

Create frequent, granular commits to track work progress without cluttering main branch history.

## Concept

Checkpoint commits capture work-in-progress state for:
- Recovery if something goes wrong
- Tracking exploration and experiments
- Documenting the journey, not just the destination

These commits stay on a `wip/` branch and can be squashed before merging to main.

## Steps

1. **Check current branch**:
   - If on `main` or `master`: offer to create/switch to a wip branch
   - If on `wip/*` branch: proceed with checkpoint

2. **Auto-generate commit message**:
   - Timestamp-based: `checkpoint: 2025-12-20 13:45`
   - Or context-based: `checkpoint: working on feature X`

3. **Stage and commit all changes**:
   ```
   git add -A
   git commit -m "checkpoint: <message>"
   ```

4. **Report**: Show what was committed.

## Arguments

- `<message>` (optional): Brief context for the checkpoint
- `--push`: Also push to remote for backup

## When to Use

- Before trying something risky
- After getting something working (even partially)
- Before taking a break
- Every 15-30 minutes during active development

## Cleanup

When ready to merge to main:
1. `git rebase -i main` to squash checkpoints
2. Write a proper commit message for the squashed work
3. Merge to main
