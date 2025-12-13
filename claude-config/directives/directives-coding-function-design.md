# Coding Directive: Function Design

**Purpose**: Guidelines for writing clear, maintainable, reusable functions.

**Last Updated**: 2025-12-03

---

## Core Principles

1. **Single Responsibility**: One function, one job
2. **Meaningful Names**: Names describe purpose, not implementation
3. **Maximum Generality**: Parameters as general as possible
4. **Clear Intent**: Code reads like prose

---

## Single Responsibility

### Rule
If you can't describe a function's purpose in one sentence, it's doing too much.

### Examples

```python
# ❌ BAD: Multiple responsibilities
def process_file(bvh_path):
    parser = BVHParser(bvh_path)           # Parse
    hand_pos = parser.get_joint_position() # Extract
    pole = calculate_pole_vector(...)     # Calculate
    hand_norm = hand_pos / 51.97           # Normalize
    with open('output.json', 'w') as f:    # Save
        json.dump({'hand': hand_norm}, f)
    return hand_norm

# ✅ GOOD: Each function one job
def parse_bvh(bvh_path):
    """Parse BVH file and return parser."""
    return BVHParser(bvh_path)

def extract_arm_data(parser, side='right'):
    """Extract arm joint positions from parser."""
    # Implementation
    return arm_data

def calculate_normalized_positions(arm_data):
    """Calculate and normalize all positions."""
    # Implementation
    return normalized_data

def save_to_json(data, output_path):
    """Save data to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(data, f)
```

---

## Meaningful Names

### Rules

- **Use verbs**: Functions perform actions
- **Be specific**: Describe what, not how
- **Avoid generic**: `process()`, `handle()`, `do_stuff()` are red flags

### Good Examples

```python
calculate_pole_vector()
transform_to_local_space()
validate_joints()
extract_hand_positions()
normalize_position()
```

### Bad Examples

```python
process()          # Process what? How?
handle_data()      # Handle how? What data?
do_stuff()         # What stuff?
compute()          # Compute what?
```

### Naming Pattern

```python
# Format: verb + noun/object + [context]
calculate_distance()           # verb + noun
transform_to_local_space()     # verb + destination
extract_joint_positions()      # verb + object
validate_bone_hierarchy()      # verb + object
```

---

## Maximum Generality

### Principle
Accept the most general type that makes sense. Don't embed domain assumptions in generic operations.

### Examples

```python
# ❌ BAD: Domain-specific, hard-coded keys
def render_hand_trajectory(data, frame_key='frames'):
    hand_positions = np.array([f['hand_position'] for f in data[frame_key]])
    # Only works for hands! Can't reuse for feet, head, etc.
    ...

# ✅ GOOD: Generic, parameterized
def render_point_trajectory(points: np.ndarray, color: str, line_width: int):
    """Render trajectory as connected line segments.

    Works for ANY trajectory: hands, feet, head, particles, anything.
    """
    trajectory_points = []
    trajectory_lines = []
    for i in range(len(points) - 1):
        trajectory_points.append(points[i])
        trajectory_points.append(points[i + 1])
        trajectory_lines.append([2, i*2, i*2 + 1])
    ...

# Usage: Works for anything!
render_point_trajectory(hand_positions, 'blue', 2)
render_point_trajectory(foot_positions, 'green', 2)
render_point_trajectory(head_positions, 'red', 2)
```

### Layered Generality

Create domain-specific wrappers around generic functions:

```python
# utils/pyvista_utils.py - Generic (no domain knowledge)
def render_point_trajectory(points: np.ndarray, color: str, line_width: int):
    """Render any trajectory as connected line segments."""
    # Generic implementation
    ...

# visualization_utils.py - Domain-specific wrapper
def render_hand_trajectory(hand_positions: np.ndarray, config: dict):
    """Render hand trajectory using visualization config."""
    return render_point_trajectory(
        hand_positions,
        config['hand_trajectory']['color'],
        config['hand_trajectory']['line_width']
    )
```

---

## Function Signatures

### Good Signatures

```python
# Clear types, clear purpose
def normalize_position(position: np.ndarray, magnitude: float) -> np.ndarray:
    """Normalize 3D position vector by magnitude."""
    return position / magnitude

# Sensible defaults
def load_animations(data_dir: Path = None, pole_multiplier: float = 2.0) -> List[Path]:
    """Load animations from directory (defaults to latest batch)."""
    if data_dir is None:
        data_dir = find_latest_batch_directory()
    return list(data_dir.glob("*.json"))
```

### Bad Signatures

```python
# Unclear types, unclear purpose
def process(data):
    """Process data."""  # What kind of data? How processed?
    ...

# Too many parameters (sign of doing too much)
def do_everything(a, b, c, d, e, f, g, h):
    ...
```

---

## Parameter Guidelines

### Accept General Types

```python
# ✅ GOOD: Accepts general numpy array
def normalize_vector(vector: np.ndarray, magnitude: float) -> np.ndarray:
    return vector / magnitude

# ❌ BAD: Assumes specific structure
def normalize_hand(hand_pos: dict, arm_data: dict) -> dict:
    # Why does normalization need dictionary structure?
    return {'normalized': hand_pos['position'] / arm_data['length']}
```

### Avoid Dictionary Keys in Generic Functions

```python
# ❌ BAD: Hard-coded keys in generic function
def extract_positions(data: dict) -> np.ndarray:
    return np.array([frame['hand_position'] for frame in data['frames']])

# ✅ GOOD: Accept data directly
def extract_positions(frames: List[dict], key: str) -> np.ndarray:
    return np.array([frame[key] for frame in frames])

# Or even better: Accept positions directly
def process_positions(positions: np.ndarray) -> np.ndarray:
    # Work with data, not structure
    ...
```

---

## Documentation

### Good Docstrings

```python
def calculate_pole_vector(shoulder: np.ndarray, elbow: np.ndarray,
                         hand: np.ndarray, distance: float = 2.0) -> np.ndarray:
    """Calculate pole vector position for IK solver.

    Args:
        shoulder: Shoulder position in world space
        elbow: Elbow position in world space
        hand: Hand position in world space
        distance: Distance multiplier from elbow (default: 2.0)

    Returns:
        3D position of pole vector in world space
    """
```

### When to Document

- **Complex algorithms**: Explain approach and reasoning
- **Non-obvious behavior**: Clarify edge cases
- **Public APIs**: Always document
- **Private helpers**: Document if behavior isn't obvious from name

### When NOT to Document

```python
# ❌ BAD: Obvious comment
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""  # Function name already says this
    return a + b

# ✅ GOOD: Self-documenting
def add_numbers(a: int, b: int) -> int:
    return a + b
```

---

## Checklist

Before committing a function, verify:
- [ ] Does one thing and does it well
- [ ] Name clearly describes purpose
- [ ] Parameters are as general as possible
- [ ] No hard-coded dictionary keys in generic functions
- [ ] Can be reused in different contexts
- [ ] Would make sense in a different project
- [ ] Type hints are accurate
- [ ] Docstring explains non-obvious behavior

---

## Related Directives

- **directives-coding-separation-of-concerns.md**: Single responsibility at module level
- **directives-coding-code-reuse.md**: Creating reusable functions
- **directives-coding-parameterization.md**: Avoiding hard-coded values

---
