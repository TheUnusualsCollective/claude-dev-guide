---
name: code-linting
description: Proactively check code for directive violations. Auto-invokes after writing Python code to library directories and before commits.
---

# Code Linting Skill

Automated directive compliance checking for Python code.

## Activation

To activate this skill:
1. Rename this directory from `code-linting-TEMPLATE` to `code-linting`
2. Configure the paths below for your project structure

## Configuration

### Monitored Directories
```
# CUSTOMIZE: Set your library directories
LIBRARY_DIRS = ["src/", "lib/", "utils/"]

# CUSTOMIZE: Set your scripts directory (where __main__ IS allowed)
SCRIPTS_DIR = "scripts/"
```

## What You MUST Do

- **Report violations clearly** with file and line references
- **Offer to fix** violations when possible
- **Check before commits** affecting library code
- **Respect configured paths** for your project

## What You MUST NOT Do

- **NEVER** silently ignore violations
- **NEVER** auto-fix without user approval
- **NEVER** check directories outside the configured scope

## Default Checks

These checks are enabled by default. Disable by removing from the list.

### 1. Print Statements in Libraries
```
CHECK: print() calls in library files
WHY: Should use logging module for proper output control
FIX: Replace with logging.info(), logging.debug(), etc.
```

### 2. Main Block in Libraries
```
CHECK: if __name__ == "__main__": in library files
WHY: Executable code belongs in scripts/ directory
FIX: Move executable code to scripts/, keep only library functions
```

### 3. Unicode in Console Output
```
CHECK: Unicode characters in print()/logging output
WHY: Causes Windows encoding errors (cp1252 codec)
FIX: Use ASCII alternatives: [OK], [FAIL], [WARN] instead of symbols
```

### 4. Hard-coded Paths
```
CHECK: Absolute paths in code
WHY: Breaks portability across machines
FIX: Use relative paths, Path objects, or configuration
```

## Adding Custom Checks

To add project-specific checks, add them below:

```
### Custom Check: [Name]
CHECK: [What to look for]
WHY: [Why it's a problem]
FIX: [How to fix it]
```

## When to Auto-Invoke

**After Writing Code** - When:
- Creating or editing files in library directories
- Adding new functions to existing modules

**Before Commits** - When:
- Staged changes include library files
- Running `/git-commit` command

## Behaviors

### On Violation Found
1. Report the violation with file:line reference
2. Explain why it's a problem
3. Offer to fix (if auto-fixable)
4. Wait for user approval before changes

### Severity Levels

| Severity | Blocks Commit | Examples |
|----------|---------------|----------|
| ERROR | Yes | `if __name__` in library, security issues |
| WARNING | No | Print statements, hard-coded values |
| INFO | No | Style suggestions, minor improvements |

## Integration with Git Workflow

This skill works with the git-workflow skill:
- Linting runs before commits
- ERRORs block the commit
- WARNINGs are reported but don't block
- User can override with explicit approval

## Manual Invocation

Users can run checks manually:
- `/lint` - Check all library files
- `/lint path/to/file.py` - Check specific file

## Example Output

```
Code Linting Report

ERRORS (blocking):
  src/utils.py:45 - if __name__ == "__main__": found in library file
    FIX: Move to scripts/run_utils.py

WARNINGS:
  src/processor.py:23 - print() statement in library
    FIX: Replace with logger.info()
  src/config.py:12 - Hard-coded path "/home/user/data"
    FIX: Use Path or configuration

Checked 15 files in src/, lib/, utils/
```
