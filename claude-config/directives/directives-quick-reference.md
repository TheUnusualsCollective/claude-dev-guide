# Coding Directives - Quick Reference

**Purpose**: Fast lookup of critical coding rules. For detailed explanations, see full directive files.

**Last Updated**: 2025-11-25

---

## Pre-Coding Checklist

**BEFORE any coding task:**

1. **Review directives** (this file + relevant detailed files)
2. **Search for existing implementations** (`grep -r "def function_name"`)
3. **Check recent development notes** (last 1-2 sessions)

**Cost**: 10-20k tokens upfront
**Savings**: 50-200k tokens avoiding refactoring

---

## Core Rules

### 1. File Organization

- **Library code**: NO `if __name__ == "__main__"` blocks
- **Executable scripts**: ONLY in `scripts/` directory
- **Utilities**: Generic in `utils/`, domain-specific in root or domain folders
- **NEVER**: Mix library functions and executable code in same file

### 2. Function Design

- **Single responsibility**: One function, one job
- **Meaningful names**: `calculate_distance()` not `process()`
- **Maximum generality**: Accept `vector` not `hand_position`
- **NEVER**: Hard-code dictionary keys in generic functions
- **NEVER**: Embed domain assumptions in utilities

### 3. Code Reuse

- **Search before writing**: Use `grep -r "def similar_function"`
- **DRY**: Copy-paste twice = extract to function
- **Use existing utilities**: Check `utils/` and `src/` first
- **NEVER**: Duplicate I/O logic (use `file_utils.py`)
- **NEVER**: Rewrite without clear functional benefit

### 4. Parameterization

- **NO hard-coded values**: Paths, thresholds, keys = parameters
- **Provide defaults**: Sensible, documented defaults
- **Config files**: For project-wide constants
- **Command-line args**: For script parameters
- **NEVER**: Hard-code paths like `D:/dev/projects/data/`

### 5. I/O Operations

- **Co-locate read/write**: Same class/module for same format
- **Use generic utilities**: `file_utils.load_json_file()`
- **Format-specific I/O**: Add to class that owns format
- **NEVER**: Scatter JSON loading across multiple files
- **NEVER**: Duplicate `with open(file)` logic

### 6. Separation of Concerns

- **Logic**: Business logic in `src/` (pure functions)
- **I/O**: File operations separate from logic
- **Presentation**: Visualization separate from data processing
- **Configuration**: Separate from implementation
- **NEVER**: Mix parsing, processing, and visualization in one function

---

## Forbidden Patterns

### ❌ NEVER Do This

```python
# 1. if __name__ in library file
def useful_function():
    ...

if __name__ == "__main__":  # ❌ Wrong file!
    useful_function()

# 2. Hard-coded dictionary keys
def render_items(data):
    positions = [f['item_position'] for f in data['frames']]  # ❌ Not reusable!

# 3. Duplicated I/O
def load_data(path):
    with open(path) as f:  # ❌ file_utils already has this!
        return json.load(f)

# 4. Domain-specific utility
def normalize_user_score(score, max_score):  # ❌ Too specific!
    return score / max_score

# 5. Hard-coded paths
data_dir = Path("D:/dev/projects/data/2025-10-26")  # ❌ Not portable!
```

### ✅ Always Do This

```python
# 1. Separate executable scripts
# In scripts/visualization/run_viz.py:
if __name__ == "__main__":  # ✅ Correct location!
    visualize_data()

# 2. Parameterized keys
def render_trajectories(data, position_key='position'):
    positions = [f[position_key] for f in data['frames']]  # ✅ Reusable!

# 3. Use existing utilities
from utils.file_utils import load_json_file
data = load_json_file(path)  # ✅ No duplication!

# 4. Generic utility
def normalize_value(value, max_value):  # ✅ Works for anything!
    return value / max_value

# 5. Parameterized paths
data_dir = find_latest_directory(base_dir)  # ✅ Auto-detect!
# Or: data_dir = config['data_dir']  # ✅ From config!
```

---

## Quick Decisions

### When to create new code?

- [ ] Searched for existing implementation? (NO = search first)
- [ ] Can existing code be generalized? (YES = refactor, NO = create)
- [ ] Is this fundamentally new functionality? (YES = create, NO = reuse)

### Where does this code go?

```
Is it executable (has __main__ or CLI)?
├─ YES → scripts/
└─ NO → Continue

Is it domain-agnostic (no project-specific knowledge)?
├─ YES → utils/
│   Test: Could this be used in ANY project?
│   Examples: file pattern matching, text parsing, CSV helpers
│   Red flag: References to domain concepts in code
└─ NO → Continue

Is it core business logic?
├─ YES → src/
└─ NO → visualization_utils.py or similar
```

**CRITICAL: The domain-agnostic test**

Ask: "Could I use this exact code in a completely different project?"
- ✅ File glob/regex matching → YES → utils/
- ✅ Generic CSV reader → YES → utils/
- ❌ Domain-specific boundary detection → NO → src/
- ❌ Domain-specific data extraction → NO → src/

### Should I parameterize this?

```
Is this value hard-coded?
├─ NO → OK
└─ YES → Continue

Will this value ever change?
├─ NO → OK as constant (document why)
└─ YES → Continue

Is this a path, threshold, or key name?
├─ YES → MUST parameterize
└─ NO → Probably parameterize anyway
```

---

## Search Commands

**Before writing new function:**

```bash
# Find similar functions
grep -r "def load.*json" python/
grep -r "def render.*" python/
grep -r "def normalize.*" python/

# Find where concept is used
grep -r "target_value" python/
grep -r "item_position" python/

# Check existing utilities
ls python/utils/
ls python/src/
```

---

## Common Mistakes - Quick Fixes

| Mistake | Quick Fix |
|---------|-----------|
| `if __name__` in library file | Move to `scripts/` directory |
| Hard-coded dict keys | Add `key_name` parameter with default |
| Duplicated JSON loading | Use `file_utils.load_json_file()` |
| Hard-coded path | Add `path` parameter or use config |
| Domain-specific utility name | Rename to generic (`normalize_value` not `normalize_user_score`) |
| Mixed concerns (I/O + logic) | Split into separate functions |

---

## Review Checklist

### Before Committing Code

- [ ] NO `if __name__` in library files (src/, utils/)
- [ ] NO hard-coded dictionary keys in generic functions
- [ ] NO duplicated I/O logic
- [ ] NO hard-coded paths/values
- [ ] Used existing utilities where applicable
- [ ] Functions have single responsibility
- [ ] Names clearly describe purpose
- [ ] Parameters are as general as possible

### After Refactoring (Moving Code)

- [ ] Updated ALL import statements (search with grep)
- [ ] Updated sys.path in scripts if needed
- [ ] Verified no circular dependencies (utils/ never imports src/)
- [ ] Tested all entry points still work
- [ ] Checked for leftover old files
- [ ] No regression in functionality

---

## Token Economics

| Action | Cost | Value |
|--------|------|-------|
| Search existing code | 1-2k tokens | Find reusable code |
| Review directives | 5-10k tokens | Avoid anti-patterns |
| Review recent sessions | 5-10k tokens | Maintain consistency |
| **Total prevention** | **~15-25k tokens** | **Avoid 50-200k refactoring** |

**ROI: 4-12x efficiency**

---

## Related Directives

- **Anti-patterns**: `directives-antipatterns.md` (what NOT to do with analysis)
- **Function design**: `directives-coding-function-design.md`
- **Code reuse**: `directives-coding-code-reuse.md`
- **Project organization**: `directives-project-organization.md`

---
