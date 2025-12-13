# Coding Directive: Separation of Concerns

**Purpose**: Keep business logic, I/O, and presentation separate for maintainability and testability.

**Last Updated**: 2025-12-03

---

## Core Principle

**Each module, class, and function should have a single, well-defined responsibility.**

What this means:
- Business logic separated from presentation logic
- Data processing separated from I/O operations
- Configuration separated from implementation
- Domain-specific code separated from generic utilities

---

## Directory Structure

The project structure reflects separation of concerns:

```
python/
├── src/              # Core logic (no I/O, no presentation)
├── utils/            # Generic utilities (no domain knowledge)
├── scripts/          # Executable workflows (orchestration)
│   ├── visualization/
│   ├── data_processing/
│   └── analysis/
└── tests/            # Test code
```

---

## Examples

### Bad: Mixed Concerns

```python
def process_and_visualize(bvh_path):
    parser = BVHParser(bvh_path)      # I/O
    hand_pos = extract_hand(parser)   # Logic
    plotter = pv.Plotter()            # Presentation
    plotter.add_mesh(hand_cloud)      # Presentation
    plotter.show()                     # Presentation
```

**Problems:**
- Can't test logic without running visualization
- Can't reuse processing for different outputs
- Can't change visualization without touching logic
- Hard to understand what the function actually does

### Good: Separated Concerns

```python
# src/arm_processor.py (logic only)
def process_arm(bvh_path):
    """Extract and process arm data from BVH file."""
    parser = BVHParser(bvh_path)
    return extract_arm_data(parser)

# scripts/visualization/visualize.py (presentation)
def visualize_animation(arm_data):
    """Visualize arm animation data."""
    plotter = create_plotter()
    add_trajectories(plotter, arm_data)
    plotter.show()
```

**Benefits:**
- Easy to test (mock I/O separately)
- Easy to reuse (same processing, different outputs)
- Easy to modify (change visualization without touching logic)
- Clear purpose for each function

---

## Where Does Code Go?

Use this decision tree:

```
Executable (has __main__)?
└─ scripts/

Domain-agnostic (no hand/arm knowledge)?
└─ utils/

Core business logic?
└─ src/

Otherwise
└─ Domain-specific wrapper (visualization_utils.py, etc.)
```

---

## Common Violations to Avoid

### 1. Mixing I/O and Logic

```python
# ❌ BAD
def process_file(path):
    with open(path) as f:           # I/O
        data = json.load(f)         # I/O
    result = calculate(data)        # Logic
    return result

# ✅ GOOD
def calculate_from_data(data):      # Logic only
    return calculate(data)

# I/O happens in calling code
with open(path) as f:
    data = json.load(f)
result = calculate_from_data(data)
```

### 2. Mixing Presentation and Logic

```python
# ❌ BAD
def analyze_trajectory(positions):
    velocity = calculate_velocity(positions)  # Logic
    print(f"Max velocity: {max(velocity)}")   # Presentation
    return velocity

# ✅ GOOD
def calculate_trajectory_velocity(positions):  # Logic only
    return calculate_velocity(positions)

# Presentation happens in calling code
velocity = calculate_trajectory_velocity(positions)
logger.info(f"Max velocity: {max(velocity)}")
```

### 3. Mixing Configuration and Implementation

```python
# ❌ BAD
def render_trajectories():
    color = [0.8, 0.624, 0.017]  # Hard-coded config
    line_width = 2
    # ... rendering logic

# ✅ GOOD
def render_trajectories(config):
    color = config['trajectory']['color']  # Config passed in
    line_width = config['trajectory']['line_width']
    # ... rendering logic
```

---

## Testing Benefits

Separated concerns make testing straightforward:

```python
# Test logic without I/O
def test_calculate_pole_vector():
    shoulder = np.array([0, 0, 0])
    elbow = np.array([1, 0, 0])
    hand = np.array([2, 0, 0])

    pole = calculate_pole_vector(shoulder, elbow, hand)

    assert np.allclose(pole, expected_pole)
    # No files needed, no visualization windows opened
```

---

## Checklist

Before committing, verify:
- [ ] Business logic is separate from I/O
- [ ] Processing is separate from presentation
- [ ] Configuration is separate from implementation
- [ ] Each function has one clear responsibility
- [ ] Code is in the appropriate directory
- [ ] Functions can be tested independently

---

## Related Directives

- **directives-coding-function-design.md**: Writing single-responsibility functions
- **directives-coding-organization.md**: Code structure and file organization
- **directives-project-organization.md**: Project directory structure

---
