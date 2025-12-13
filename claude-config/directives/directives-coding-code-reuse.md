# Coding Directive: Code Reuse

**Purpose**: Eliminate duplication through shared utilities and proper abstraction.

**Last Updated**: 2025-12-03

---

## Core Principle: DRY (Don't Repeat Yourself)

**Every piece of knowledge should have a single, unambiguous representation in the system.**

When you see duplicated code, you're seeing a missing abstraction.

---

## Before Writing New Code

Ask these questions in order:

1. **Does similar function exist?**
   - Search: `grep -r "def similar_function" python/`
   - Check existing utilities in `src/` and `utils/`

2. **Can existing code be generalized?**
   - Is it too specific for one use case?
   - Would making it generic benefit other code?

3. **Will I need this elsewhere?**
   - If yes, extract to shared location
   - If no, consider if it might be needed later

**Only create new code if:**
- No existing solution exists
- Generalizing would increase complexity
- Implementing fundamentally new capability

---

## The Copy-Paste Rule

**If you copy-paste code twice, extract it into a function.**

### Example

```python
# ❌ BAD: Duplicated logic (spotted after second copy-paste)
def process_hand_data(hand_pos, arm_length):
    return [hand_pos[0]/arm_length, hand_pos[1]/arm_length, hand_pos[2]/arm_length]

def process_pole_data(pole_pos, arm_length):
    return [pole_pos[0]/arm_length, pole_pos[1]/arm_length, pole_pos[2]/arm_length]

def process_shoulder_data(shoulder_pos, arm_length):
    return [shoulder_pos[0]/arm_length, shoulder_pos[1]/arm_length, shoulder_pos[2]/arm_length]

# ✅ GOOD: Single reusable function
def normalize_position(position: np.ndarray, magnitude: float) -> np.ndarray:
    """Normalize 3D position vector by magnitude."""
    return position / magnitude

# Usage everywhere
hand_normalized = normalize_position(hand_pos, arm_length)
pole_normalized = normalize_position(pole_pos, arm_length)
shoulder_normalized = normalize_position(shoulder_pos, arm_length)
```

---

## Where to Place Shared Code

### Decision Tree

```
Is it domain-agnostic (no hand/arm/animation knowledge)?
├─ Yes → utils/
│   Examples: math utilities, file I/O, generic rendering
│
└─ No → Is it core business logic?
    ├─ Yes → src/
    │   Examples: arm processing, pole vector calculation
    │
    └─ No → Domain-specific wrapper
        Examples: visualization_utils.py, animation_utils.py
```

### Examples

```python
# utils/geometry.py - Domain-agnostic
def normalize_vector(vector: np.ndarray, magnitude: float) -> np.ndarray:
    """Normalize any vector by magnitude."""
    return vector / magnitude

# src/arm_processor.py - Core business logic
def calculate_pole_vector(shoulder, elbow, hand, distance=2.0):
    """Calculate pole vector for arm IK."""
    # Uses domain knowledge about arms and IK
    ...

# visualization_utils.py - Domain-specific wrapper
def render_hand_trajectory(hand_positions, config):
    """Render hand trajectory using visualization config."""
    # Wraps generic utilities with domain-specific config
    return render_point_trajectory(hand_positions, config['color'], config['width'])
```

---

## Identifying Missing Abstractions

### Pattern 1: Similar Functions with Different Names

```python
# ❌ BAD: Similar logic, different names
def get_hand_distance(hand1, hand2):
    return np.linalg.norm(hand1 - hand2)

def get_shoulder_distance(shoulder1, shoulder2):
    return np.linalg.norm(shoulder1 - shoulder2)

def get_elbow_distance(elbow1, elbow2):
    return np.linalg.norm(elbow1 - elbow2)

# ✅ GOOD: Single generic function
def calculate_distance(point1: np.ndarray, point2: np.ndarray) -> float:
    """Calculate Euclidean distance between two 3D points."""
    return np.linalg.norm(point1 - point2)
```

### Pattern 2: Similar Code Blocks in Multiple Files

```python
# ❌ BAD: Same pattern in 5 different visualization scripts
# File A
trajectory_points = []
trajectory_lines = []
for i in range(len(positions) - 1):
    trajectory_points.append(positions[i])
    trajectory_points.append(positions[i + 1])
    trajectory_lines.append([2, i*2, i*2 + 1])

# File B
trajectory_points = []
trajectory_lines = []
for i in range(len(positions) - 1):
    trajectory_points.append(positions[i])
    trajectory_points.append(positions[i + 1])
    trajectory_lines.append([2, i*2, i*2 + 1])

# ✅ GOOD: Extract to shared utility
# utils/pyvista_utils.py
def create_trajectory_lines(positions: np.ndarray) -> Tuple[List, List]:
    """Convert positions to PyVista line format."""
    points = []
    lines = []
    for i in range(len(positions) - 1):
        points.append(positions[i])
        points.append(positions[i + 1])
        lines.append([2, i*2, i*2 + 1])
    return points, lines

# Usage in all files
points, lines = create_trajectory_lines(positions)
```

### Pattern 3: Configuration Duplication

```python
# ❌ BAD: Same config in multiple files
# visualize_script_1.py
color = [0.8, 0.624, 0.017]
line_width = 2
opacity = 0.6

# visualize_script_2.py
color = [0.8, 0.624, 0.017]
line_width = 2
opacity = 0.6

# ✅ GOOD: Centralized configuration
# visualization_config.json
{
  "trajectory": {
    "color": [0.8, 0.624, 0.017],
    "line_width": 2,
    "opacity": 0.6
  }
}

# All scripts
config = load_visualization_config()
render_trajectories(config['trajectory'])
```

---

## Refactoring for Reuse

When you find duplication, follow this process:

### 1. Identify the Pattern

```python
# Spot the duplication
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
```

### 2. Extract Common Logic

```python
def extract_arm_joints(parser, side: str):
    """Extract arm joints for specified side.

    Args:
        parser: BVH parser instance
        side: 'left' or 'right'
    """
    suffix = 'L' if side == 'left' else 'R'
    return {
        'shoulder': parser.get_joint(f"Shoulder_{suffix}"),
        'elbow': parser.get_joint(f"Elbow_{suffix}"),
        'hand': parser.get_joint(f"Hand_{suffix}")
    }
```

### 3. Update All Call Sites

```python
# Old code
left_arm = process_left_arm(parser)
right_arm = process_right_arm(parser)

# New code
left_arm = extract_arm_joints(parser, 'left')
right_arm = extract_arm_joints(parser, 'right')
```

### 4. Delete Duplicated Code

Remove the old `process_left_arm` and `process_right_arm` functions entirely.

---

## Examples Gallery

### Domain-Specific Duplication

```python
# ❌ BAD: Three nearly-identical functions
def normalize_hand_position(hand_pos, arm_length):
    return hand_pos / arm_length

def normalize_pole_position(pole_pos, arm_length):
    return pole_pos / arm_length

def normalize_shoulder_position(shoulder_pos, arm_length):
    return shoulder_pos / arm_length

# ✅ GOOD: One generic function
def normalize_position(position: np.ndarray, magnitude: float) -> np.ndarray:
    """Normalize 3D position vector by magnitude."""
    return position / magnitude
```

### I/O Duplication

```python
# ❌ BAD: File loading duplicated across scripts
# Script 1
with open(path, 'r') as f:
    data = json.load(f)

# Script 2
with open(path, 'r') as f:
    data = json.load(f)

# Script 3
with open(path, 'r') as f:
    data = json.load(f)

# ✅ GOOD: Shared utility (use utils/file_utils.py)
def load_json(path: Path) -> dict:
    """Load JSON file."""
    with open(path, 'r') as f:
        return json.load(f)

# All scripts
data = load_json(path)
```

---

## Checklist

Before writing new code:
- [ ] Searched for similar existing functions
- [ ] Checked if existing code can be generalized
- [ ] Considered where shared code should live
- [ ] Verified no duplication with existing utilities
- [ ] Ensured code is reusable in other contexts

When finding duplication:
- [ ] Extracted to shared function
- [ ] Updated all call sites
- [ ] Deleted duplicated code
- [ ] Placed in appropriate location (src/ or utils/)
- [ ] Made function as general as possible

---

## Related Directives

- **directives-coding-function-design.md**: Writing general, reusable functions
- **directives-coding-refactoring.md**: Improving existing code
- **directives-antipatterns.md**: Common duplication mistakes

---
