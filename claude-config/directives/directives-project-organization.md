# Project Organization Directives

**Purpose**: Structural guidelines for organizing code, scripts, and execution patterns.

**Last Updated**: 2025-12-02

---

## Core Principle

**Organize by functionality, not by script. Separate "what to do" (execution) from "how to do it" (libraries).**

---

## 0. Path Initialization (CRITICAL)

### The Iron Rule

**NEVER manipulate `sys.path` inside project code.**

Path initialization happens EXTERNALLY, before any project code executes.

### Forbidden Patterns

```python
# ❌ FORBIDDEN - Never do this in project code
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

import setup_path  # This file has been deleted!
```

### Correct Approach

**Option 1: Use setup_env.bat (Windows)**

```batch
your_project/setup_env.bat
# Opens configured environment
python scripts/your_script.py <args>
```

**Option 2: External Python Script**

```python
# external_caller.py (OUTSIDE your_project/)
from init_paths import setup_python_path

setup_python_path(
    base_directory="/path/to/your_project",
    config_file="/path/to/your_project/config/project_paths.json",
    caller="my_script"
)

# Now import project code
from src.data_loader import DataLoader
```

**Option 3: Manual PYTHONPATH**

```bash
export PYTHONPATH="$PWD/python:$PWD/python/src:$PWD/python/utils"
python scripts/your_script.py
```

### Required Paths

Typical paths to add (can be configured in `config/project_paths.json`):
- `python/` - Enables `from src.X` and `from utils.Y`
- `python/src/` - Enables bare imports within src/
- `python/utils/` - Enables bare imports within utils/

---

## 1. Execution Files (Python Scripts)

### Purpose
Entry points that import, configure, and execute library code.

### What They Contain
- Input collection (args, config, environment)
- Minimal glue code connecting library functions
- Execution-specific configuration

### What They DON'T Contain
- Function definitions (move to libraries)
- Class definitions (move to modules)
- Data definitions (move to config/constants)
- Reusable logic (move to libraries)
- `if __name__ == "__main__":` blocks (file executes top-to-bottom)

### Pattern: Import → Configure → Execute → Report

```python
# ✅ GOOD: scripts/process_data.py
from src.data_loader import load_data
from src.processor import process_batch
from utils.file_utils import find_latest_directory

# Get configuration
data_dir = find_latest_directory(base_dir='data/processed')
config = {'multiplier': 2.0, 'reference': 'default'}

# Setup data
items = load_data(data_dir)

# Execute
results = process_batch(items, config)

# Report
print(f"Processed {len(results)} items")
```

```python
# ❌ BAD: Defining functions in execution file
def process_item(data):  # ❌ Should be in library
    ...

def calculate_result(a, b, c):  # ❌ Should be in library
    ...

# Get configuration
data = load_data()

# Execute (using local functions)
process_item(data)
```

### Keep Entry Points Simple
- 10-30 lines of glue code maximum
- If script is complex, logic belongs in library
- Script orchestrates, library implements

---

## 2. Batch/Shell Scripts

### Minimum Viable Scripts
- Absolute minimum - just kick off Python processes
- If batch file needs logic, move to Python
- Multiple simple scripts > one complex script

### Example

```bash
# ✅ GOOD: Simple process launcher
@echo off
uv run python scripts/data_processing/batch_process.py %*

# ❌ BAD: Logic in batch file
@echo off
set DATA_DIR=D:\data
if exist %DATA_DIR% (
    for %%f in (%DATA_DIR%\*.bvh) do (
        python process.py %%f
    )
)
# Logic should be in Python!
```

---

## 3. Function Libraries

### Purpose
Shared, reusable functionality organized by domain.

### Structure
- Group related functions in single files
- Name by domain: `file_utils.py`, `pyvista_utils.py`, `geometry.py`
- Keep functions pure when possible (no hidden state)

### When to Extract to Library

| Situation | Action |
|-----------|--------|
| Logic used by 2+ callers | Extract to library |
| Complex logic worth isolating | Extract for testability |
| Domain-specific operations | Extract to domain module |

### Directory Organization

```
python/
├── src/              # Domain-specific libraries
│   ├── geometry.py
│   ├── arm_processor.py
│   └── data_loader.py
│
├── utils/            # Generic utilities
│   ├── file_utils.py
│   ├── pyvista_utils.py
│   └── color_utils.py
│
└── scripts/          # Execution files (minimal)
    ├── process_batch.py
    └── visualize_results.py
```

---

## 4. Command-Line Parsing

### Strategy
- Parser definitions in function libraries (not execution files)
- Parsers map arguments to callable functions (strategy pattern)
- Execution files provide minimal glue
- Keep parser logic reusable and testable

### Example

```python
# ✅ GOOD: src/cli_parsers.py (library)
import argparse

def create_batch_parser():
    """Create argument parser for batch processing."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir', type=str)
    parser.add_argument('--workers', type=int, default=4)
    return parser

# ✅ GOOD: scripts/batch_process.py (execution)
from src.cli_parsers import create_batch_parser
from src.batch_processor import run_batch

parser = create_batch_parser()
args = parser.parse_args()
run_batch(args.data_dir, workers=args.workers)
```

```python
# ❌ BAD: Parser defined in execution file
# scripts/batch_process.py
import argparse

# Parser definition mixed with execution
parser = argparse.ArgumentParser()
parser.add_argument('--data-dir')  # ❌ Not reusable
args = parser.parse_args()

# Execution logic
...
```

---

## 5. Classes vs Functions

### When to Use Classes

**Use classes when:**
- Multiple operations on the same data
- State management required
- Clear initialization/cleanup needed
- Implementing interfaces/abstract patterns

**Example:**
```python
# ✅ GOOD: State management with class
class DataProcessor:
    def __init__(self, file_path, multiplier=2.0):
        self.file_path = file_path
        self.parser = Parser(file_path)
        self.multiplier = multiplier

    def process(self, mode='default'):
        # Uses self.parser, self.multiplier
        ...

    def export_to_json(self, output_path):
        # Uses processed data
        ...
```

### When to Use Functions

**Use functions when:**
- Pure computation (input → output)
- Stateless operations
- Simple transformations

**Example:**
```python
# ✅ GOOD: Stateless utility functions
def normalize_position(position, magnitude):
    return position / magnitude

def calculate_distance(point_a, point_b):
    return np.linalg.norm(point_b - point_a)
```

### Rule of Thumb
- **Classes**: Nouns with lifecycle (Processor, Manager, Handler)
- **Functions**: Verbs without state (calculate, transform, normalize)
- **Keep classes focused**: One responsibility per class

---

## 6. Data Configuration & Testing

### Production Data Setup

**Standardize data structures:**
```python
# ✅ GOOD: Use library functions
from src.data_loader import create_animation_container

# Production code
data = create_animation_container(config)

# Test code (same function!)
test_data = create_animation_container(test_config)
```

**Don't scatter setup logic:**
```python
# ❌ BAD: Data setup duplicated in tests
# test_processing.py
def setup_test_data():
    # Custom test setup duplicating production logic
    data = {'frames': [...], 'metadata': {...}}

# ✅ GOOD: Reuse production setup
from src.data_loader import create_animation_container
test_data = create_animation_container(test_config)
```

### Test Data Guidelines

- Treat test data as close to production as possible
- Reuse production configuration code
- Test-specific setup in dedicated testing modules
- Ensures consistency as codebase evolves

---

## 7. Extending Functionality

### Before Writing New Code

1. **Check existence**: Does similar functionality exist?
2. **Check parameterization**: Can existing code accept new parameters?
3. **Check extension**: Would branching/arguments extend cleanly?

### Adding to Existing Functions

```python
# ✅ GOOD: Optional parameters with defaults
def load_animations(data_dir=None, max_count=None, filter_pattern='*.json'):
    if data_dir is None:
        data_dir = find_latest_directory()
    files = data_dir.glob(filter_pattern)
    if max_count:
        files = files[:max_count]
    return load_files(files)
```

**Guidelines:**
- Use optional arguments with sensible defaults
- Branch behavior based on args (don't duplicate code)
- Document new parameters clearly

### When to Create New Functions

**Create new when:**
- Behavior is fundamentally different
- Adding would make existing function too complex
- Performance characteristics differ significantly

**Example:**
```python
# Existing: Sequential processing
def process_animations(animations):
    return [process_one(a) for a in animations]

# New: Parallel processing (fundamentally different)
def process_animations_parallel(animations, workers=4):
    with mp.Pool(workers) as pool:
        return pool.map(process_one, animations)
```

---

## 8. Command Logging (Optional Pattern)

### Purpose
Track script executions for debugging and auditing.

### Implementation
```python
# ✅ GOOD: Command logging at start of main()
import sys
from utils.command_logger import log_command

def main():
    # Log command execution
    log_command(__file__, sys.argv)

    # ... rest of script
```

### Log Location
- Directory: `logs/` or `command_log/`
- Format: `command_log_YYYY-MM-DD.txt`
- Each day gets its own dated log file

### Benefits
- Track script usage patterns
- Debug issues by reviewing execution history
- Reproduce complex workflows
- Audit data processing pipelines

---

## 9. File Organization Standards

### Test Files
- **Location**: `python/tests/`
- **Pattern**: `test_*.py`
- **Rule**: ALL test files MUST be in `tests/` directory
- **Never**: test_*.py files in project root

### Visualization Scripts
- **Location**: `python/scripts/visualization/`
- **Pattern**: `visualize_*.py`
- **Rule**: ALL visualization scripts in `scripts/visualization/`
- **Never**: visualize_*.py files in project root

### Import Pattern
Ensure Python path is configured before imports (see Section 0):
```python
# Path setup happens externally (setup_env.bat, PYTHONPATH, etc.)
from src.module import function
from utils.helper import utility
```

**Never use in library files:**
```python
# ❌ FORBIDDEN in src/ or utils/
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.append('src')
```

---

## Quick Reference

### File Types

| Type | Contains | Location | Max Lines |
|------|----------|----------|-----------|
| Execution | Glue code | `scripts/` | 10-30 |
| Library | Reusable functions | `src/`, `utils/` | 200-500 |
| Class module | Stateful operations | `src/` | 200-500 |
| Batch script | Process launcher | `scripts/` | 5-10 |
| Test | Unit/integration tests | `tests/` | 100-300 |
| Visualization | PyVista/plotting scripts | `scripts/visualization/` | 100-400 |

### Decision Trees

**Where does this code go?**
```
Is it an entry point that runs?
└─ scripts/ (10-30 lines of glue)

Is it reusable logic?
└─ Domain-specific? → src/
└─ Generic utility? → utils/

Does it need state management?
└─ Yes → Class in src/
└─ No → Functions in utils/
```

**Should I extend or create new?**
```
Similar function exists?
└─ Can it be parameterized? → Extend with optional args
└─ Fundamentally different? → Create new function
└─ Would make it complex? → Create new function
```

---

## Related Directives

- **Quick reference**: `directives-quick-reference.md`
- **Anti-patterns**: `directives-antipatterns.md`
- **Python packages**: `directives-python-package-management.md`

---
