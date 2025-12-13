# Coding Directive: Logging

**Purpose**: Proper logging practices for production-quality output and debugging.

**Last Updated**: 2025-12-03

---

## Core Rule

**ALWAYS use logging, NEVER use print().**

All Python scripts MUST use the `logging` module for output, not `print()` statements.

---

## Why Logging Over Print

### Benefits of Logging

1. **Timestamps**: Automatically included
2. **Log levels**: Control verbosity without code changes
3. **Redirection**: Can send to files without modifying code
4. **Professional format**: Consistent, structured output
5. **Better debugging**: Can enable/disable at module level
6. **Production ready**: Works in production environments

### Problems with Print

```python
# ❌ BAD: Using print
print("Processing file 1 of 100")
print(f"Warning: Low coherence detected")
print(f"ERROR: File not found: {path}")

# Problems:
# - No timestamps
# - Can't control verbosity
# - Hard to redirect to logs
# - No severity levels
# - Unprofessional in production
```

---

## Basic Setup

### At Module Level

```python
import logging

# Configure logging (usually at script entry point)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create logger for this module
logger = logging.getLogger(__name__)
```

### In Scripts

```python
#!/usr/bin/env python3
"""
Script to process animation data.
"""

import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting animation processing")
    # ... rest of script
```

---

## Log Levels

Use appropriate levels for different message types:

### DEBUG - Detailed diagnostic information

```python
logger.debug(f"Hand position: {hand_pos}")
logger.debug(f"Calculated pole vector: {pole}")
logger.debug(f"IDW weights: {weights}")
```

**When to use:**
- Detailed variable values
- Step-by-step algorithm progress
- Data structure contents
- Usually disabled in production

### INFO - General informational messages

```python
logger.info("Processing 100 animation files")
logger.info(f"Loaded configuration from {config_path}")
logger.info(f"Processing file {i}/{total}")
logger.info("[OK] Processing complete")
```

**When to use:**
- Progress updates
- Major milestones
- Configuration loading
- Successful operations
- Default level for most scripts

### WARNING - Something unexpected but not breaking

```python
logger.warning(f"Low coherence detected: {coherence}")
logger.warning(f"Missing optional data: pole vectors not found")
logger.warning(f"Using fallback value: {fallback}")
```

**When to use:**
- Unexpected but handled conditions
- Missing optional data
- Using fallback/default values
- Performance issues

### ERROR - Operation failed

```python
logger.error(f"Failed to process file: {path}")
logger.error(f"Invalid BVH structure: missing required joint")
logger.error(f"Configuration file not found: {config_path}")
```

**When to use:**
- Operations that failed
- Invalid input data
- Missing required files
- Exceptions caught and handled

### CRITICAL - System failure

```python
logger.critical("Unable to access data directory")
logger.critical("Configuration corrupted, cannot continue")
```

**When to use:**
- Fatal errors
- System-level failures
- Unrecoverable conditions

---

## IMPORTANT: Unicode Character Restrictions

**Windows console (cmd.exe) does NOT support Unicode symbols.**

### The Problem

```python
# ❌ FAILS ON WINDOWS
logger.info("✓ Processing complete")
# UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'
```

### The Solution: Use ASCII Alternatives

```python
# ✅ WORKS EVERYWHERE
logger.info("[OK] Processing complete")
logger.error("[FAIL] File not found")
logger.info("Model -> Prediction")
logger.warning("[WARN] Low coherence detected")
```

### Common Substitutions

| Unicode | ASCII Alternative | Usage |
|---------|------------------|-------|
| ✓ | `[OK]` or `PASS` | Success messages |
| ✗ | `[FAIL]` or `FAIL` | Failure messages |
| → | `->` | Arrows, flow |
| • | `-` or `*` | Bullet points |
| ⚠ | `[WARN]` or `WARNING` | Warnings |
| ⏳ | `[WAIT]` | Processing |
| ✨ | `[DONE]` | Completion |

### Error You'll See

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'
in position 4: character maps to <undefined>
```

This means you used a Unicode symbol that Windows console can't display.

---

## Usage Examples

### Processing Loop

```python
# ❌ BAD: Using print
total = len(files)
for i, file in enumerate(files):
    print(f"Processing {i+1}/{total}: {file.name}")
    result = process_file(file)
    print(f"  - Hand frames: {len(result['hand'])}")
    print(f"  - Pole frames: {len(result['pole'])}")

# ✅ GOOD: Using logging
total = len(files)
logger.info(f"Processing {total} files")
for i, file in enumerate(files):
    logger.info(f"[{i+1}/{total}] Processing: {file.name}")
    result = process_file(file)
    logger.debug(f"  Hand frames: {len(result['hand'])}")
    logger.debug(f"  Pole frames: {len(result['pole'])}")
logger.info("[OK] All files processed")
```

### Error Handling

```python
# ❌ BAD: Using print
try:
    data = load_file(path)
except FileNotFoundError:
    print(f"ERROR: File not found: {path}")
    sys.exit(1)

# ✅ GOOD: Using logging
try:
    data = load_file(path)
except FileNotFoundError:
    logger.error(f"File not found: {path}")
    sys.exit(1)
```

### Progress Updates

```python
# ❌ BAD: Using print
print("Loading animations...")
animations = load_animations()
print(f"Loaded {len(animations)} animations")
print("Processing...")
results = process_animations(animations)
print("Done!")

# ✅ GOOD: Using logging
logger.info("Loading animations...")
animations = load_animations()
logger.info(f"Loaded {len(animations)} animations")
logger.info("Processing animations...")
results = process_animations(animations)
logger.info("[OK] Processing complete")
```

### Detailed Debugging

```python
# ✅ GOOD: Debug level for detailed output
logger.debug(f"Hand position: {hand_pos}")
logger.debug(f"Shoulder position: {shoulder_pos}")
logger.debug(f"Calculated distance: {distance}")

# Can enable debug logging when needed:
logging.getLogger().setLevel(logging.DEBUG)

# Or keep at INFO level by default (debug messages hidden)
```

---

## Advanced Configuration

### Logging to File

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processing.log'),
        logging.StreamHandler()  # Also log to console
    ]
)
```

### Per-Module Log Levels

```python
# Set different levels for different modules
logging.getLogger('src.arm_processor').setLevel(logging.DEBUG)
logging.getLogger('src.geometry').setLevel(logging.WARNING)
```

### Custom Format

```python
# Shorter format for console
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

# Output: [INFO] Processing complete
```

---

## Migration from Print

When modifying existing code with `print()` statements:

### Step 1: Add Logging Setup

```python
import logging
logger = logging.getLogger(__name__)
```

### Step 2: Replace Print Statements

```python
# Before
print("Processing files")
print(f"Loaded {count} files")
print(f"ERROR: Failed to load {path}")

# After
logger.info("Processing files")
logger.info(f"Loaded {count} files")
logger.error(f"Failed to load {path}")
```

### Step 3: Check for Unicode

```python
# Before
print(f"✓ Processing complete")

# After
logger.info("[OK] Processing complete")
```

---

## Common Patterns

### Script Progress

```python
logger.info("="*60)
logger.info("Animation Processing Pipeline")
logger.info("="*60)
logger.info(f"Data directory: {data_dir}")
logger.info(f"Output directory: {output_dir}")
logger.info(f"Total files: {total}")
logger.info("-"*60)

# Processing...

logger.info("-"*60)
logger.info(f"[OK] Processed {success_count}/{total} files")
logger.info(f"[FAIL] Failed: {fail_count}")
logger.info("="*60)
```

### Conditional Verbosity

```python
def process_batch(files, verbose=False):
    """Process batch of files.

    Args:
        files: Files to process
        verbose: Enable debug logging
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    for file in files:
        logger.debug(f"Processing: {file}")
        # ...
```

---

## Checklist

Before committing:
- [ ] No `print()` statements (use `logger` instead)
- [ ] Appropriate log levels used
- [ ] No Unicode symbols (only ASCII)
- [ ] Logger configured at module level
- [ ] Progress updates use INFO level
- [ ] Errors use ERROR level
- [ ] Debug details use DEBUG level
- [ ] Messages are clear and informative

---

## Related Directives

- **directives-coding-function-design.md**: Functions should log, not print
- **directives-coding-organization.md**: Logging configuration placement

---
