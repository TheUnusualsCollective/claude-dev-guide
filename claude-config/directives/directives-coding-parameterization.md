# Coding Directive: Parameterization

**Purpose**: Avoid hard-coded values through proper configuration and parameterization.

**Last Updated**: 2025-12-03

---

## Core Principle

**Hard-coded values are technical debt.**

Every hard-coded path, threshold, multiplier, or key is a maintenance burden and limits reusability.

---

## The Rule

**If it might change, parameterize it.**

Especially:
- File paths
- Directory locations
- Thresholds and tolerances
- Multipliers and scaling factors
- Color values
- Dictionary keys
- API endpoints
- Default behaviors

---

## Parameterization Hierarchy

From worst to best:

1. **Hard-coded in function** ❌ - Never acceptable
2. **Hard-coded as constant** ❌ - Still inflexible
3. **Environment variable** ⚠️ - Better, but limited
4. **Configuration file** ✅ - Good for application settings
5. **Function parameter with default** ✅ - Best for reusable functions

---

## Examples

### File Paths

```python
# ❌ WORST: Hard-coded in function
def load_animations():
    data_dir = Path("D:/dev/projects/data/processed/2025-10-26-07.50")
    return list(data_dir.glob("*.json"))

# ❌ BAD: Hard-coded as constant
DATA_DIR = Path("D:/dev/projects/data/processed/2025-10-26-07.50")

def load_animations():
    return list(DATA_DIR.glob("*.json"))

# ✅ GOOD: Parameterized with sensible default
def load_animations(data_dir: Path = None) -> List[Path]:
    """
    Load animation files from directory.

    Args:
        data_dir: Directory to load from (defaults to latest batch)
    """
    if data_dir is None:
        data_dir = find_latest_batch_directory()
    return list(data_dir.glob("*.json"))
```

### Thresholds and Multipliers

```python
# ❌ BAD: Hard-coded magic numbers
def calculate_pole_vector(shoulder, elbow, hand):
    direction = (elbow - shoulder) / np.linalg.norm(elbow - shoulder)
    pole_position = elbow + direction * 2.0  # What is 2.0?
    return pole_position

# ✅ GOOD: Parameterized with documented default
def calculate_pole_vector(shoulder: np.ndarray,
                         elbow: np.ndarray,
                         hand: np.ndarray,
                         distance_multiplier: float = 2.0) -> np.ndarray:
    """
    Calculate pole vector position for IK solver.

    Args:
        shoulder: Shoulder position in world space
        elbow: Elbow position in world space
        hand: Hand position in world space
        distance_multiplier: Distance from elbow to pole (default: 2.0,
                           validated through experimentation)

    Returns:
        3D position of pole vector in world space
    """
    direction = (elbow - shoulder) / np.linalg.norm(elbow - shoulder)
    pole_position = elbow + direction * distance_multiplier
    return pole_position
```

### Configuration Values

```python
# ❌ BAD: Scattered hard-coded values
# File: visualize_script_1.py
def render_trajectories():
    color = [0.8, 0.624, 0.017]  # Orange
    line_width = 2
    opacity = 0.6
    # ... rendering

# File: visualize_script_2.py
def render_other_stuff():
    color = [0.8, 0.624, 0.017]  # Same orange
    line_width = 2
    opacity = 0.6
    # ... rendering

# ✅ GOOD: Centralized configuration
# File: visualization_config.json
{
  "trajectory": {
    "color": [0.8, 0.624, 0.017],
    "line_width": 2,
    "opacity": 0.6,
    "description": "Orange trajectory - main motion path"
  },
  "pole_vector": {
    "color": [0.0, 1.0, 0.0],
    "point_size": 8,
    "opacity": 0.8,
    "description": "Green - IK pole targets"
  }
}

# All scripts
config = load_visualization_config()
render_trajectories(config['trajectory'])
```

### Dictionary Keys

```python
# ❌ BAD: Hard-coded keys in generic function
def extract_positions(data: dict) -> np.ndarray:
    """Extract hand positions from animation data."""
    # This function now ONLY works with this exact structure!
    return np.array([frame['hand_position'] for frame in data['frames']])

# ✅ GOOD: Parameterized or accept data directly
def extract_positions(frames: List[dict], key: str = 'position') -> np.ndarray:
    """Extract positions from frames using specified key."""
    return np.array([frame[key] for frame in frames])

# Or even better: Accept processed data
def process_positions(positions: np.ndarray) -> np.ndarray:
    """Process position array (independent of original structure)."""
    # Works with any position data, regardless of source
    return positions / np.linalg.norm(positions, axis=1, keepdims=True)
```

---

## Default Values

### Make Defaults Sensible

```python
# ✅ GOOD: Sensible defaults
def filter_animations(
    animations: List[Path],
    min_frames: int = 10,           # Most animations > 10 frames
    max_frames: int = 10000,        # Reasonable upper limit
    require_hand: bool = True,      # Almost always needed
    require_pole: bool = False      # Sometimes optional
) -> List[Path]:
    """
    Filter animations by criteria.

    Defaults allow most common use case without parameters:
        filtered = filter_animations(all_animations)

    But remain flexible for specific needs:
        filtered = filter_animations(all_animations, min_frames=30)
    """
```

### Document Why Defaults Were Chosen

```python
def calculate_idw_weights(
    distances: np.ndarray,
    power: float = 2.0  # Shepard's original paper used 2.0
                        # Validated: produces smooth interpolation for our data
) -> np.ndarray:
    """
    Calculate Inverse Distance Weighting.

    Args:
        distances: Distance from query point to data points
        power: IDW power parameter (default: 2.0)
               Lower = smoother, higher = more local influence
    """
    return 1.0 / (distances ** power)
```

---

## Configuration Files vs Parameters

### Use Configuration Files For:

- Application-wide settings
- Values that change between environments (dev/prod)
- Visual styling (colors, sizes, opacity)
- Data paths and directories
- Feature flags

```json
// visualization_config.json
{
  "camera": {
    "position": [100, 100, 100],
    "focal_point": [0, 0, 0],
    "view_up": [0, 1, 0]
  },
  "rendering": {
    "background_color": [0.1, 0.1, 0.1],
    "show_grid": true,
    "anti_aliasing": true
  }
}
```

### Use Function Parameters For:

- Algorithm parameters
- Runtime behavior
- Data-dependent values
- Options that vary per call

```python
def process_animation(
    bvh_path: Path,
    side: str = 'right',           # Runtime choice
    normalize: bool = True,        # Algorithm behavior
    pole_distance: float = 2.0     # Data-dependent
) -> dict:
    """Process animation with configurable behavior."""
```

---

## Migration Strategy

### When Encountering Hard-coded Values

1. **Identify the value**
   ```python
   # Found: Hard-coded 51.97
   normalized = hand_pos / 51.97
   ```

2. **Understand what it represents**
   ```python
   # It's the average arm length from shoulder to hand
   ```

3. **Decide parameterization approach**
   ```python
   # This is an algorithm parameter, not config
   # Should be function parameter with default
   ```

4. **Add parameter with default**
   ```python
   def normalize_hand_position(
       hand_pos: np.ndarray,
       arm_length: float = 51.97  # Average from dataset analysis
   ) -> np.ndarray:
       return hand_pos / arm_length
   ```

5. **Update call sites**
   ```python
   # Most calls use default
   normalized = normalize_hand_position(hand_pos)

   # Special cases can override
   normalized = normalize_hand_position(hand_pos, arm_length=custom_length)
   ```

---

## Common Violations

### 1. Absolute Paths

```python
# ❌ BAD
bvh_dir = Path("D:/dev/projects/pole-solver/data/bvh")

# ✅ GOOD
bvh_dir = project_config.get_data_dir() / "bvh"
```

### 2. Magic Numbers

```python
# ❌ BAD
if coherence < 0.15:  # What is 0.15?
    mark_as_low_coherence()

# ✅ GOOD
COHERENCE_THRESHOLD = 0.15  # Below this: poor IK convergence

if coherence < COHERENCE_THRESHOLD:
    mark_as_low_coherence()

# ✅ EVEN BETTER
def check_coherence(coherence: float, threshold: float = 0.15) -> bool:
    """
    Check if coherence is acceptable.

    Args:
        coherence: Coherence value (0-1)
        threshold: Minimum acceptable coherence (default: 0.15,
                  determined from IK convergence testing)
    """
    return coherence >= threshold
```

### 3. Hard-coded Dictionary Keys in Generic Code

```python
# ❌ BAD: Generic function with hard-coded keys
def render_trajectory(animation_data):
    # Why does rendering need to know about data structure?
    positions = [f['hand_position'] for f in animation_data['frames']]
    render_points(positions)

# ✅ GOOD: Accept processed data
def render_trajectory(positions: np.ndarray, color: str, width: int):
    """Render trajectory from position array."""
    render_points(positions, color, width)

# Data extraction happens separately
positions = extract_hand_positions(animation_data)
render_trajectory(positions, 'blue', 2)
```

---

## Checklist

Before committing code with values:
- [ ] No absolute file paths
- [ ] No hard-coded thresholds without explanation
- [ ] No magic numbers in calculations
- [ ] No hard-coded dictionary keys in generic functions
- [ ] Configuration values in config files
- [ ] Algorithm parameters as function parameters
- [ ] Default values are sensible and documented
- [ ] Why defaults were chosen is explained

---

## Related Directives

- **directives-coding-function-design.md**: Designing parameter-friendly functions
- **directives-coding-refactoring.md**: Extracting hard-coded values
- **directives-antipatterns.md**: Hard-coding anti-patterns

---
