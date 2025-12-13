# Coding Directive: Code Organization

**Purpose**: Standards for structuring code, imports, and modules.

**Last Updated**: 2025-12-03

---

## Core Principles

1. **Logical Structure**: Related code grouped together
2. **Clear Dependencies**: No circular imports, unidirectional flow
3. **Appropriate Sizing**: Files split when too large
4. **Clean Imports**: Import only what's needed

---

## File Structure

### Standard Python File Layout

```python
#!/usr/bin/env python3
"""
Module docstring explaining purpose.

Detailed description if needed.
"""

# Standard library imports
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports
import numpy as np
import pyvista as pv

# Local imports
from src.geometry import normalize_position
from src.config import load_config
from utils.file_utils import load_json

# Module-level constants
DEFAULT_ARM_LENGTH = 51.97
COHERENCE_THRESHOLD = 0.15

# Module-level logger
import logging
logger = logging.getLogger(__name__)


# Classes and functions
class ArmProcessor:
    """Process arm animation data."""
    ...

def process_animation(path: Path) -> dict:
    """Process single animation file."""
    ...


# Main execution (scripts only)
if __name__ == "__main__":
    main()
```

---

## Import Organization

### Import Order

**Three groups, separated by blank lines:**

1. **Standard library**: Built-in Python modules
2. **Third-party**: Installed packages
3. **Local**: Your project modules

```python
# Standard library
import sys
import json
from pathlib import Path
from typing import List, Dict

# Third-party
import numpy as np
import pyvista as pv
from bvh_parser import BVHParser

# Local modules
from src.geometry import normalize_position
from src.arm_processor import process_arm
from utils.file_utils import load_json
```

### Import Rules

**Do:**
```python
# Import specific items
from pathlib import Path
from typing import List, Dict

# Import module for frequent use
import numpy as np

# Relative imports within package
from .geometry import normalize_position
from ..utils import file_utils
```

**Don't:**
```python
# ❌ Wildcard imports
from module import *

# ❌ Unused imports
import sys  # Not used anywhere

# ❌ Wrong order (third-party before stdlib)
import numpy as np
import sys
```

---

## Module Organization

### When to Split a File

Split when:
- File exceeds 500 lines
- Multiple unrelated concerns in one file
- Difficult to find specific functions
- Circular dependency issues

### How to Split

```python
# Before: visualization_utils.py (800 lines)
# - Trajectory rendering
# - Arm rendering
# - Pole vector rendering
# - Camera setup
# - Color utilities

# After: Split by concern
visualization/
├── trajectory_renderer.py    # Trajectory-specific
├── arm_renderer.py           # Arm-specific
├── pole_renderer.py          # Pole vector-specific
├── camera_setup.py           # Camera utilities
└── color_utils.py            # Color utilities
```

---

## Directory Organization

### Execution vs Library Code

**Rule: `if __name__ == "__main__"` ONLY in `scripts/`**

```
python/
├── src/              # Library code (no __main__)
│   ├── geometry.py
│   ├── arm_processor.py
│   └── config.py
├── utils/            # Generic utilities (no __main__)
│   ├── file_utils.py
│   └── pyvista_utils.py
└── scripts/          # Executable code (has __main__)
    ├── process_batch.py
    └── visualize.py
```

### Bad Organization

```python
# ❌ BAD: Executable code in src/
# src/arm_processor.py
def process_arm(data):
    ...

if __name__ == "__main__":  # Don't do this in src/!
    # This makes it hard to import as library
    data = load_data()
    process_arm(data)
```

### Good Organization

```python
# ✅ GOOD: Library in src/
# src/arm_processor.py
def process_arm(data):
    """Process arm data (pure function, no I/O)."""
    ...

# ✅ GOOD: Executable in scripts/
# scripts/process_animations.py
from src.arm_processor import process_arm

def main():
    data = load_data()
    result = process_arm(data)
    save_result(result)

if __name__ == "__main__":
    main()
```

---

## Dependency Management

### Unidirectional Dependencies

```
scripts/  →  src/  →  utils/
  ↓           ↓
  └─────────→┘

Flow: scripts use src, src uses utils
      scripts can use utils directly
      NEVER: utils uses src, src uses scripts
```

### Avoiding Circular Imports

```python
# ❌ BAD: Circular dependency
# module_a.py
from module_b import function_b

def function_a():
    return function_b()

# module_b.py
from module_a import function_a  # Circular!

def function_b():
    return function_a()

# ✅ GOOD: Extract common dependency
# shared.py
def shared_function():
    return "shared logic"

# module_a.py
from shared import shared_function

# module_b.py
from shared import shared_function
```

---

## Code Grouping

### Within a Module

Group related functions together:

```python
# geometry.py

# ============================================================================
# Vector Operations
# ============================================================================

def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """Normalize vector to unit length."""
    ...

def calculate_magnitude(vector: np.ndarray) -> float:
    """Calculate vector magnitude."""
    ...


# ============================================================================
# Distance Calculations
# ============================================================================

def euclidean_distance(point1: np.ndarray, point2: np.ndarray) -> float:
    """Calculate Euclidean distance between points."""
    ...

def manhattan_distance(point1: np.ndarray, point2: np.ndarray) -> float:
    """Calculate Manhattan distance between points."""
    ...


# ============================================================================
# Coordinate Transformations
# ============================================================================

def world_to_local(position: np.ndarray, origin: np.ndarray) -> np.ndarray:
    """Transform world coordinates to local space."""
    ...
```

---

## Constants and Configuration

### Module-Level Constants

```python
# At top of file, after imports

# Physical constants
DEFAULT_ARM_LENGTH = 51.97  # Average from dataset analysis
SHOULDER_TO_ELBOW_RATIO = 0.55  # Anatomical proportion

# Algorithm parameters
IDW_POWER = 2.0  # Shepard's original paper
COHERENCE_THRESHOLD = 0.15  # Below this: poor IK convergence

# File patterns
BVH_PATTERN = "*.bvh"
JSON_PATTERN = "*.json"
```

### When to Use Config Files

Use external config when:
- Values change between environments
- Non-programmers need to modify
- Many related settings

```python
# visualization_config.json
{
  "trajectory": {
    "color": [0.8, 0.624, 0.017],
    "line_width": 2,
    "opacity": 0.6
  }
}

# Load in code
config = load_visualization_config()
```

---

## Documentation

### Module Docstrings

```python
"""
Module for processing arm animation data.

This module provides functions for extracting and normalizing
arm joint positions from BVH files.

Typical usage:
    from src.arm_processor import process_arm

    data = process_arm(bvh_path, side='right')
"""
```

### Function Docstrings

Use Google style:

```python
def process_arm(bvh_path: Path, side: str = 'right') -> dict:
    """
    Extract and process arm data from BVH file.

    Args:
        bvh_path: Path to BVH file
        side: Which arm to process ('left' or 'right')

    Returns:
        Dictionary containing:
            - shoulder: Shoulder positions (N, 3)
            - elbow: Elbow positions (N, 3)
            - hand: Hand positions (N, 3)
            - pole: Pole vector positions (N, 3)

    Raises:
        FileNotFoundError: If BVH file doesn't exist
        ValueError: If side is not 'left' or 'right'
    """
```

---

## Example: Well-Organized Module

```python
#!/usr/bin/env python3
"""
Arm processor for motion capture data.

Extracts and normalizes arm joint positions from BVH files,
calculating IK pole vectors for animation retargeting.
"""

# Standard library
from pathlib import Path
from typing import Dict

# Third-party
import numpy as np

# Local
from src.geometry import normalize_position, calculate_distance
from utils.file_utils import validate_file_exists

# Constants
DEFAULT_ARM_LENGTH = 51.97
POLE_DISTANCE_MULTIPLIER = 2.0

# Logging
import logging
logger = logging.getLogger(__name__)


# ============================================================================
# Public API
# ============================================================================

def process_arm(bvh_path: Path, side: str = 'right') -> Dict[str, np.ndarray]:
    """
    Extract and process arm data from BVH file.

    Args:
        bvh_path: Path to BVH file
        side: Which arm ('left' or 'right')

    Returns:
        Processed arm data with normalized positions
    """
    validate_file_exists(bvh_path)
    logger.info(f"Processing {side} arm from {bvh_path.name}")

    raw_data = _extract_raw_joints(bvh_path, side)
    normalized = _normalize_positions(raw_data)

    return normalized


# ============================================================================
# Internal Helpers
# ============================================================================

def _extract_raw_joints(bvh_path: Path, side: str) -> dict:
    """Extract raw joint positions (internal helper)."""
    # Implementation...
    pass


def _normalize_positions(raw_data: dict) -> dict:
    """Normalize positions by arm length (internal helper)."""
    # Implementation...
    pass
```

---

## Checklist

Before committing:
- [ ] Imports organized in three groups
- [ ] No wildcard imports (`from x import *`)
- [ ] No circular dependencies
- [ ] File size reasonable (< 500 lines)
- [ ] Related functions grouped together
- [ ] Module docstring present
- [ ] Public functions documented
- [ ] Constants defined at module level
- [ ] No `if __name__ == "__main__"` in library code

---

## Related Directives

- **directives-coding-separation-of-concerns.md**: Where code belongs
- **directives-project-organization.md**: Directory structure
- **directives-coding-function-design.md**: Function documentation

---
