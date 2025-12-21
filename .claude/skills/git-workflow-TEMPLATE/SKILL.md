---
name: git-workflow
description: Proactively manage git operations. Auto-invoke for status checks before risky operations, suggest checkpoints during development, and prompt for commits when work is complete.
---

<!--
TEMPLATE: Rename directory from "git-workflow-TEMPLATE" to "git-workflow" to activate.
-->

# Git Workflow Skill

Ensures proper version control practices throughout development sessions.

## When to Auto-Invoke

**Status Check** - Before:
- Making significant code changes
- Refactoring or reorganizing files
- Starting work on a new feature

**Checkpoint Suggestion** - When:
- 15-30 minutes have passed since last commit
- A significant piece of work is complete (even partially)
- User is about to try something experimental/risky
- User mentions taking a break or stopping

**Commit Prompt** - When:
- Feature implementation is complete
- Bug is fixed and verified
- User indicates work is done ("that works", "looks good")
- Session is ending

**Branch Management** - When:
- Starting new feature work (suggest feature branch)
- Work is experimental (suggest wip branch)

## Behaviors

### Proactive Status Awareness
- Periodically note uncommitted changes
- Warn about files that may be too large for GitHub
- Alert if local is significantly behind remote

### Checkpoint Reminders
- After significant work blocks, gently suggest: "Consider a checkpoint commit?"
- Don't be annoying - once per significant work session is enough

### Commit Quality
- Help craft meaningful commit messages
- Ensure commits are atomic (one logical change)
- Never include Claude attribution in messages

### Branch Hygiene
- Encourage feature branches for new work
- Suggest wip branches for experiments

## Manual Commands

Users can explicitly invoke:
- `/git-status` - Detailed status with context
- `/git-commit` - Guided commit workflow
- `/git-branch` - Branch management
- `/git-checkpoint` - Quick checkpoint commit

## Safety Rules

- Never force push without explicit user request
- Never push to main/master without user confirmation
- Always warn about uncommitted changes before branch switches
