# Coding Directive: Refactoring

**Purpose**: Guidelines for improving existing code without changing its behavior.

**Last Updated**: 2025-12-03

---

## Core Principle

**Leave the codebase better than you found it.**

When you encounter existing code:
- Understand it before changing it
- Prefer extending/generalizing over duplicating
- Consolidate duplication immediately
- Refactor incrementally, not all at once

---

## When to Refactor

### Always Refactor When:
- You find duplicated code
- You need to modify existing functionality
- You discover overly-specific code that could be generalized
- You see hard-coded values that should be configurable
- You encounter unclear or misleading names

### Consider Refactoring When:
- Function has multiple responsibilities
- Code is difficult to understand
- Adding new feature requires copy-pasting existing code
- Tests are hard to write due to coupling

### Don't Refactor When:
- Code works and doesn't need modification
- You're just making stylistic changes
- "I prefer my version" is the only reason
- Refactoring would increase complexity without benefit

---

## Refactoring Workflow

### 1. Understand the Code

**Before changing anything:**
- Read the entire function/module
- Understand what it does and why
- Identify dependencies
- Check for tests
- Look for existing call sites

```python
# Don't just jump to refactoring - understand context first
grep -r "function_name" python/  # Find all uses
```

### 2. Identify the Problem

Common issues:
- **Duplication**: Same logic in multiple places
- **Over-specificity**: Hard-coded domain assumptions
- **Mixed concerns**: I/O + logic + presentation in one function
- **Poor naming**: Function name doesn't match behavior
- **Hard-coding**: Paths, thresholds, keys embedded in code

### 3. Plan the Refactoring

**Ask:**
- What's the minimal change that solves the problem?
- Can I generalize without increasing complexity?
- Will this benefit other code?
- What needs to be updated?

**Document:**
- Write down the refactoring plan
- Identify all call sites that need updating
- Note any potential breaking changes

### 4. Refactor Incrementally

**Don't:**
- Rewrite entire module at once
- Change behavior while refactoring
- Mix multiple refactorings together

**Do:**
- Make one improvement at a time
- Keep code working after each change
- Test after each step
- Commit logical units

### 5. Verify Correctness

After refactoring:
- Run existing tests
- Test manually if no automated tests
- Check all call sites still work
- Verify behavior is unchanged

---

## Common Refactoring Patterns

### Extract Function

**When**: Code block is duplicated or doing too much

```python
# Before: Duplicated logic
def process_left_arm(parser):
    shoulder = parser.get_joint("Shoulder_L")
    elbow = parser.get_joint("Elbow_L")
    hand = parser.get_joint("Hand_L")
    return {'shoulder': shoulder, 'elbow': elbow, 'hand': hand}

def process_right_arm(parser):
    shoulder = parser.get_joint("Shoulder_R")
    elbow = parser.get_joint("Elbow_R")
    hand = parser.get_joint("Hand_R")
    return {'shoulder': shoulder, 'elbow': elbow, 'hand': hand}

# After: Extracted common logic
def extract_arm_joints(parser, side: str):
    """Extract arm joints for specified side ('left' or 'right')."""
    suffix = 'L' if side == 'left' else 'R'
    return {
        'shoulder': parser.get_joint(f"Shoulder_{suffix}"),
        'elbow': parser.get_joint(f"Elbow_{suffix}"),
        'hand': parser.get_joint(f"Hand_{suffix}")
    }

# Updated usage
left_arm = extract_arm_joints(parser, 'left')
right_arm = extract_arm_joints(parser, 'right')
```

### Generalize Function

**When**: Function is too specific, could work for more cases

```python
# Before: Too specific
def normalize_hand_position(hand_pos: np.ndarray, arm_length: float) -> np.ndarray:
    """Normalize hand position by arm length."""
    return hand_pos / arm_length

# After: Generalized
def normalize_position(position: np.ndarray, magnitude: float) -> np.ndarray:
    """Normalize 3D position vector by magnitude."""
    return position / magnitude

# Works for anything
hand_norm = normalize_position(hand_pos, arm_length)
pole_norm = normalize_position(pole_pos, arm_length)
shoulder_norm = normalize_position(shoulder_pos, arm_length)
```

### Extract Configuration

**When**: Hard-coded values scattered across code

```python
# Before: Hard-coded values
def render_trajectories():
    color = [0.8, 0.624, 0.017]
    line_width = 2
    opacity = 0.6
    # ... rendering code

# After: Configuration extracted
# visualization_config.json
{
  "trajectory": {
    "color": [0.8, 0.624, 0.017],
    "line_width": 2,
    "opacity": 0.6
  }
}

# Code
def render_trajectories(config: dict):
    color = config['color']
    line_width = config['line_width']
    opacity = config['opacity']
    # ... rendering code
```

### Separate Concerns

**When**: Function mixes I/O, logic, and presentation

```python
# Before: Mixed concerns
def process_and_save_file(bvh_path, output_path):
    parser = BVHParser(bvh_path)              # I/O
    hand_pos = extract_hand(parser)            # Logic
    normalized = hand_pos / 51.97              # Logic
    with open(output_path, 'w') as f:          # I/O
        json.dump({'hand': normalized}, f)     # I/O
    print(f"Processed {bvh_path.name}")        # Presentation

# After: Separated concerns
def extract_hand_data(parser):
    """Extract and normalize hand data."""
    hand_pos = extract_hand(parser)
    return hand_pos / 51.97

def save_hand_data(data, output_path):
    """Save hand data to JSON."""
    with open(output_path, 'w') as f:
        json.dump({'hand': data}, f)

# Usage - each step is clear
parser = BVHParser(bvh_path)
hand_data = extract_hand_data(parser)
save_hand_data(hand_data, output_path)
logger.info(f"Processed {bvh_path.name}")
```

### Rename for Clarity

**When**: Name doesn't match behavior

```python
# Before: Misleading name
def process(data):  # What kind of processing?
    return data / np.linalg.norm(data)

# After: Clear name
def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize vector to unit length."""
    return vector / np.linalg.norm(vector)
```

---

## Avoid "Not Invented Here" Syndrome

### The Problem

Don't rewrite existing code just because you think you can do it better.

```python
# ❌ BAD: Creating duplicate functionality
# Existing in src/geometry.py
def normalize_position(position, magnitude):
    return position / magnitude

# New code - Don't do this!
def my_normalize_function(pos, mag):
    """I prefer this version."""
    return pos / mag

# ✅ GOOD: Use existing function
from src.geometry import normalize_position
result = normalize_position(position, magnitude)
```

### When to Rewrite

Only rewrite when:
- Existing code has clear functional deficiency
- Performance is measurably inadequate
- Existing approach is fundamentally wrong
- Code is blocking other work

**Not valid reasons:**
- "I would have done it differently"
- "My style is better"
- "I don't like their variable names"

---

## Refactoring Anti-patterns

### 1. Big Bang Refactoring

```python
# ❌ BAD: Rewrite entire module at once
# - High risk of breaking things
# - Hard to review
# - Hard to debug if something breaks

# ✅ GOOD: Incremental refactoring
# - Extract one function
# - Test it works
# - Extract another function
# - Test it works
# - Continue...
```

### 2. Refactoring + Behavior Change

```python
# ❌ BAD: Mix refactoring with new features
def process_arm(parser, side):
    # Refactored to accept side parameter
    # AND added new pole vector calculation
    # AND changed normalization approach
    # Hard to debug if something breaks!

# ✅ GOOD: Separate refactoring from feature work
# 1. Refactor to accept side parameter (commit)
# 2. Add pole vector calculation (commit)
# 3. Change normalization (commit)
```

### 3. Over-engineering

```python
# ❌ BAD: Making it too generic
def process(data, mode, params, flags, options):
    """Process data in various ways depending on configuration."""
    # Now handles 10 different cases
    # Most of which are theoretical

# ✅ GOOD: Generalize only as needed
def normalize_position(position: np.ndarray, magnitude: float):
    """Normalize 3D position vector by magnitude."""
    return position / magnitude
    # Simple, focused, actually used
```

---

## Consolidating Duplication Immediately

### Rule

**When you find duplicated code, consolidate it before adding more.**

### Example Workflow

```python
# Step 1: Notice duplication
# File A has function X
# File B has similar function Y

# Step 2: STOP - Don't create function Z in file C

# Step 3: Extract common logic to shared location
# Create shared_utils.py with function X generalized

# Step 4: Update files A and B to use shared function

# Step 5: NOW create function Z if still needed
```

---

## Checklist

Before refactoring:
- [ ] Understand what code currently does
- [ ] Found all call sites
- [ ] Identified what needs to change
- [ ] Have plan for incremental changes
- [ ] Know how to verify correctness

During refactoring:
- [ ] Making one change at a time
- [ ] Testing after each change
- [ ] Not mixing refactoring with new features
- [ ] Keeping code working throughout

After refactoring:
- [ ] All tests still pass
- [ ] All call sites updated
- [ ] Behavior is unchanged
- [ ] Code is simpler/clearer than before
- [ ] No duplication remains

---

## Related Directives

- **directives-coding-code-reuse.md**: Eliminating duplication
- **directives-coding-function-design.md**: Writing better functions
- **directives-antipatterns.md**: Common mistakes to avoid

---
