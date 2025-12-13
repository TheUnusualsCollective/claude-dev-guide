# Coding Directive: Coordinate System Transformations

**Purpose**: Prevent subtle bugs when transforming between coordinate systems, especially across different source formats.

**Last Updated**: 2025-12-13

---

## Core Principle

**"Local space" is ambiguous without knowing the axis conventions of the reference frame.**

Transforming to a local coordinate space requires TWO steps:
1. **Geometric transform**: Position/rotation relative to reference frame origin
2. **Axis normalization**: Ensuring consistent meaning of X, Y, Z across all sources

Skipping step 2 produces data that LOOKS correct but is silently inconsistent.

---

## The Hidden Problem

Different source formats (skeleton rigs, 3D packages, game engines) define "local axes" differently for the same logical bone or object:

| Format | Chest Bone X | Chest Bone Y | Chest Bone Z |
|--------|--------------|--------------|--------------|
| Mixamo | Right | Forward | Down-ish |
| HumanIK | Forward | Left | Down-ish |
| Unreal | Forward | Right-back | Down-ish |

If you transform world positions to "chest-local space" using just the chest's rotation matrix, the output X/Y/Z will have **different meanings** depending on which source format you started with.

**This bug is insidious because:**
- Code runs without errors
- Output looks plausible
- Values are in reasonable ranges
- Problem only appears when comparing outputs from different sources

---

## Solution Pattern

### 1. Define a Canonical Coordinate System

Document explicitly what your output coordinate system means:

```
Canonical Output:
- Handedness: Right-handed
- Up axis: +Y
- Forward axis: +Z (subject faces +Z)
- Right axis: +X
- Base unit: centimeters
```

### 2. Determine Axis Mappings Per Source Format

For each source format, determine how its axes map to canonical:

```python
# Determined by correlation analysis (see verification section)
AXIS_REMAP = {
    'mixamo': None,  # Reference format - no remapping needed
    'humanik': np.array([
        [0, -1, 0],   # Canonical X = -Source Y
        [1,  0, 0],   # Canonical Y = +Source X
        [0,  0, 1],   # Canonical Z = +Source Z
    ]),
    'unreal': np.array([
        [0,  0, -1],  # Canonical X = -Source Z
        [1,  0,  0],  # Canonical Y = +Source X
        [0, -1,  0],  # Canonical Z = -Source Y
    ]),
}
```

### 3. Apply Both Transforms

```python
def transform_to_local_canonical(world_pos, ref_pos, ref_axes, axis_remap):
    """
    Transform world position to canonical local space.

    Args:
        world_pos: Position in world space
        ref_pos: Reference frame origin in world space
        ref_axes: Reference frame rotation (columns = local axes in world)
        axis_remap: Matrix to convert local axes to canonical (or None)

    Returns:
        Position in canonical local space
    """
    # Step 1: Geometric transform to local space
    rotation_matrix = np.column_stack([ref_axes.x, ref_axes.y, ref_axes.z])
    relative_pos = world_pos - ref_pos
    local_pos = rotation_matrix.T @ relative_pos

    # Step 2: Axis normalization to canonical system
    if axis_remap is not None:
        local_pos = axis_remap @ local_pos

    return local_pos
```

---

## Verification Methods

### Correlation Analysis

Compare the same motion across different source formats to determine axis mappings:

```python
def find_axis_mapping(positions_format_a, positions_format_b):
    """
    Determine which axis in B corresponds to which axis in A.

    Correlation near +1.0: same axis, same sign
    Correlation near -1.0: same axis, flipped sign
    Correlation near 0.0: different axes
    """
    for i, axis_a in enumerate(['X', 'Y', 'Z']):
        for j, axis_b in enumerate(['X', 'Y', 'Z']):
            corr = np.corrcoef(
                positions_format_a[:, i],
                positions_format_b[:, j]
            )[0, 1]
            if abs(corr) > 0.95:
                sign = '+' if corr > 0 else '-'
                print(f"Format_A.{axis_a} = {sign}Format_B.{axis_b}")
```

### Visual Verification

Always visualize outputs from multiple source formats together:
- Overlay trajectories from different sources (same motion)
- If axes are wrong, trajectories will be rotated/flipped relative to each other
- Arm segments (shoulder->elbow->hand) should align across formats

### Numerical Verification

After applying transforms, positions from different sources should match within tolerance:

```python
# Same motion, different source formats
max_diff = np.max(np.abs(positions_mixamo - positions_humanik))
assert max_diff < 0.01, f"Format mismatch: {max_diff} units difference"
```

---

## Common Mistakes

### 1. Assuming "Local Space" Is Universal

```python
# BAD: Assumes all formats define chest axes the same way
def to_chest_local(world_pos, chest_pos, chest_rotation):
    return chest_rotation.T @ (world_pos - chest_pos)

# GOOD: Accounts for format-specific axis conventions
def to_chest_local_canonical(world_pos, chest_pos, chest_rotation, format_id):
    local = chest_rotation.T @ (world_pos - chest_pos)
    remap = AXIS_REMAP.get(format_id)
    return remap @ local if remap else local
```

### 2. Testing With Only One Format

```python
# BAD: Only tests Mixamo, misses format-specific bugs
def test_chest_transform():
    data = load_test_file("test_mixamo.fbx")
    result = transform(data)
    assert result.shape == (100, 3)  # Passes but hides axis bug!

# GOOD: Tests multiple formats, compares outputs
def test_chest_transform_consistency():
    mixamo = transform(load_test_file("test_mixamo.fbx"))
    humanik = transform(load_test_file("test_humanik.fbx"))
    unreal = transform(load_test_file("test_unreal.fbx"))

    # Same motion should produce same output regardless of source
    assert np.allclose(mixamo, humanik, atol=0.01)
    assert np.allclose(mixamo, unreal, atol=0.01)
```

### 3. Documenting Space But Not Axes

```python
# BAD: Says "local" but doesn't specify axis meanings
metadata = {
    'space': 'chest_local'  # Local to WHICH convention?
}

# GOOD: Fully specifies the coordinate system
metadata = {
    'space': 'chest_local',
    'handedness': 'right',
    'up_axis': '+Y',
    'forward_axis': '+Z',
    'right_axis': '+X'
}
```

---

## Checklist

Before implementing coordinate transforms:

- [ ] Defined canonical output coordinate system (handedness, up, forward, units)
- [ ] Identified all source formats that will be processed
- [ ] Determined axis mapping for each source format (via correlation analysis)
- [ ] Implemented axis remapping step after geometric transform
- [ ] Added verification comparing outputs across formats
- [ ] Documented coordinate system in output metadata

Before declaring transform "working":

- [ ] Tested with at least 2 different source formats
- [ ] Visually verified outputs overlay correctly
- [ ] Numerically verified outputs match within tolerance
- [ ] Output metadata fully describes the coordinate system

---

## Related Directives

- **directives-problem-isolation.md**: Reduce/verify/expand workflow for debugging transforms
- **directives-coding-parameterization.md**: Don't hard-code format-specific values
- **directives-coding-separation-of-concerns.md**: Keep transform logic separate from I/O

---
