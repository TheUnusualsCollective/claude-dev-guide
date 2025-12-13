# Anti-Pattern Directives

**Purpose**: Patterns to AVOID in this codebase.

**Last Updated**: 2025-11-26

---

## Critical: Review Before Coding

**BEFORE any coding task:**

1. **Review directives** (~5-10k tokens)
   - Read relevant `directives-*.md` files
   - Prevents re-introducing refactored patterns

2. **Search existing code** (~1-3k tokens)
   - `grep -r "def similar_function"`
   - Check `utils/`, `src/` for existing implementations

3. **Check recent sessions** (~5-10k tokens)
   - Review last 1-2 `project-notes/development-notes-archive/development-notes_XXX.md` files
   - Understand recent refactoring decisions

**Cost**: 10-20k tokens upfront
**Savings**: 50-200k tokens avoiding refactoring later
**ROI**: 4-12x efficiency

---

## Anti-Pattern 1: `if __name__ == "__main__"` in Library Files

### Problem

**DON'T** mix library code with executable scripts:

```python
# ❌ BAD: visualize_split_arms.py
def visualize_split_arms(right_path, left_path):
    """Reusable function."""
    ...

if __name__ == "__main__":  # Wrong! This is library code
    visualize_split_arms(sys.argv[1], sys.argv[2])
```

### Solution

**DO** separate library from executable:

```python
# ✅ GOOD: utils/visualization_utils.py (library)
def visualize_split_arms(right_path, left_path):
    """Reusable function."""
    ...

# ✅ GOOD: scripts/visualization/visualize_split_arms.py (executable)
if __name__ == "__main__":
    visualize_split_arms(sys.argv[1], sys.argv[2])
```

### Directory Rules

- **Library code** (reusable functions): `src/`, `utils/` - NO `__main__`
- **Executable scripts**: `scripts/` - YES `__main__`
- **Exception**: Only when user explicitly requests it

---

## Anti-Pattern 2: Hard-Coded Dictionary Keys

### Problem

**DON'T** hard-code data structure in generic functions:

```python
# ❌ BAD: Only works with exact structure
def visualize_arms(data):
    hands = np.array([f['hand_position'] for f in data['frames']])
    shoulders = np.array([f['shoulder'] for f in data['frames']])
    # Locked to 'hand_position', 'shoulder' keys - not reusable!
```

### Solution

**DO** parameterize keys:

```python
# ✅ GOOD: Works with any keys
def visualize_trajectories(data, frame_key='frames', position_key='hand_position'):
    positions = np.array([f[position_key] for f in data[frame_key]])
    # Now works for hands, feet, head, anything!

# Usage
visualize_trajectories(arm_data, position_key='hand_position')
visualize_trajectories(leg_data, position_key='foot_position')
```

### Benefits

- Same function handles arms, legs, head, any limbs
- Adapts to different JSON structures
- Changes to format only affect call sites

---

## Anti-Pattern 3: Scattered I/O for Same Format

### Problem

**DON'T** duplicate file I/O across files:

```python
# ❌ BAD: Duplicated in multiple files

# File 1: src/arm_processor.py
def export_to_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f)

# File 2: scripts/visualize.py
def load_arm_data(path):  # Duplicate!
    with open(path, 'r') as f:
        return json.load(f)

# File 3: scripts/analyze.py
def load_animation(path):  # Another duplicate!
    with open(path, 'r') as f:
        return json.load(f)
```

### Solution

**DO** co-locate read/write OR use generic utilities:

```python
# ✅ Option A: Use existing generic utility
from utils.file_utils import load_json_file
data = load_json_file(path)  # Already exists!

# ✅ Option B: Co-locate in format owner
class ArmProcessor:
    def export_to_json(self, path):
        """Write arm data."""
        ...

    @staticmethod
    def load_from_json(path):
        """Read arm data."""
        ...
```

### Decision

- **Generic JSON**: Use `file_utils.load_json_file()`
- **Format-specific**: Add read/write to same class

---

## Anti-Pattern 4: Ignoring Existing Utilities

### Problem

**DON'T** write new code when utilities exist:

```python
# ❌ BAD: Reinventing the wheel
def load_arm_data(path):
    with open(path, 'r') as f:
        return json.load(f)

# But utils/file_utils.py already has:
def load_json_file(path):
    with open(path, 'r') as f:
        return json.load(f)
```

### Solution

**DO** search before writing:

```bash
# Search for existing functions
grep -r "def load.*json" python/
grep -r "def render.*" python/
grep -r "json.load" python/utils/

# Found it! Use existing
from utils.file_utils import load_json_file
```

### Cost Analysis

| Action | Token Cost |
|--------|-----------|
| Search existing | 1-2k tokens |
| Write duplicate | 5-7k tokens (including later refactoring) |
| **Efficiency gain** | **3-4x** |

---

## Anti-Pattern 5: Post-Refactoring Regression

### Problem

**DON'T** reintroduce patterns that were already refactored:

**Example Timeline:**
- Session 003: Removed duplicated `load_animations()` functions
- Session 005: Added new `load_arm_data()` - **regression!**

### Solution

**DO** review recent sessions before coding:

1. Read last 1-2 `project-notes/development-notes-archive/development-notes_XXX.md`
2. Check what was refactored and WHY
3. Follow established patterns
4. Document new patterns as established

### Prevention

- Review directives before coding (10-20k tokens upfront)
- Prevents 50-200k tokens refactoring later
- Maintains architectural consistency

---

## Forbidden vs Required Patterns

### ❌ NEVER

```python
# 1. __main__ in library file
# In utils/visualization.py:
if __name__ == "__main__":  # ❌ Wrong location!

# 2. Hard-coded keys
hands = [f['hand_position'] for f in data['frames']]  # ❌ Not reusable

# 3. Duplicated I/O
def load_data(path):  # ❌ file_utils already has this
    with open(path) as f:
        return json.load(f)

# 4. Domain-specific utility
def normalize_hand_position(hand, arm_length):  # ❌ Too specific

# 5. Hard-coded paths
data_dir = Path("D:/dev/projects/data/2025-10-26")  # ❌ Not portable
```

### ✅ ALWAYS

```python
# 1. Separate executable scripts
# In scripts/visualization/run_viz.py:
if __name__ == "__main__":  # ✅ Correct location

# 2. Parameterized keys
positions = [f[position_key] for f in data[frame_key]]  # ✅ Reusable

# 3. Use existing utilities
from utils.file_utils import load_json_file  # ✅ No duplication
data = load_json_file(path)

# 4. Generic utility
def normalize_position(position, magnitude):  # ✅ Works for anything

# 5. Parameterized paths
data_dir = find_latest_directory(base_dir)  # ✅ Auto-detect
# Or: data_dir = config['data_dir']  # ✅ From config
```

---

## Search Commands

**Before writing new code:**

```bash
# Find similar functions
grep -r "def load.*json" python/
grep -r "def render.*" python/
grep -r "def normalize.*" python/

# Find concept usage
grep -r "hand_position" python/
grep -r "pole_vector" python/

# Check utilities
ls python/utils/
ls python/src/
```

---

## Pre-Coding Checklist

```markdown
- [ ] Read relevant directives (~5-10k tokens)
- [ ] Search for existing implementations (~1-3k tokens)
- [ ] Review recent development notes (~5-10k tokens)
- [ ] Design decision made (2-3 approaches considered)

Total: ~15-25k tokens upfront
Savings: 50-200k tokens (avoid refactoring)
ROI: 4-12x efficiency
```

---

## Common Mistakes - Quick Fixes

| Mistake | Fix |
|---------|-----|
| `if __main__` in library | Move to `scripts/` |
| Hard-coded dict keys | Add parameter with default |
| Duplicated JSON load | Use `file_utils.load_json_file()` |
| Hard-coded path | Add parameter or use config |
| Domain-specific name | Rename to generic |
| Mixed concerns | Split into separate functions |

---

## Token Economics

| Action | Cost | Savings |
|--------|------|---------|
| Review directives | 5-10k | Avoid anti-patterns |
| Search existing | 1-3k | Find reusable code |
| Review recent work | 5-10k | Maintain consistency |
| **Total prevention** | **15-25k** | **50-200k refactoring** |

**ROI: 4-12x token efficiency**

---
