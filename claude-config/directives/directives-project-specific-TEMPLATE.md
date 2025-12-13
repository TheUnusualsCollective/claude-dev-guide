# Project-Specific Directives - TEMPLATE

**Purpose**: Template for creating project-specific overrides and extensions to general directives.

**Last Updated**: 2025-12-13

---

## How to Use This Template

1. Copy this file to your project's `claude-config/directives/` directory
2. Rename to `directives-project-specific-<project-name>.md`
3. Fill in the sections below with project-specific guidance
4. Reference from your project's CLAUDE.md

---

## Path Management Overrides

If your project has special path handling requirements, document them here.

### Example: UV Projects Without External Setup

```python
# ✅ ALLOWED in scripts/ (for projects using uv without external setup)
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))

from your_module import YourClass
```

**Critical Rules:**
- ✅ Scripts can add to `sys.path` at the very top (before library imports)
- ❌ Library files (src/, utils/) NEVER touch `sys.path`
- ✅ Use relative paths from `__file__` for portability
- ❌ Never use absolute paths

---

## Domain Boundaries

Define what belongs in `src/` vs `utils/` for your project.

### Decision Tree: utils/ vs src/

```
Does this code know about [YOUR DOMAIN CONCEPTS]?
├─ YES → src/ (domain-specific)
│   Examples:
│   - [domain]_processor.py
│   - data_extractor.py
│   - [domain]_writer.py
│
└─ NO → utils/ (domain-agnostic)
    Examples:
    - file_resolver.py (pure file pattern matching)
    - text_parser_utils.py (generic parsing)
```

### Red Flags for Misplaced Code

**If you see these in utils/, move to src/:**
- References to domain-specific concepts
- Knowledge of your data structures
- Domain-specific processing logic

**If you see these in src/, consider extracting to utils/:**
- Generic file operations
- Generic text parsing
- Generic data transformations

---

## Project-Specific Conventions

Document any project-specific patterns here.

### Naming Conventions

| Entity | Pattern | Example |
|--------|---------|---------|
| Processors | `{domain}_processor.py` | `data_processor.py` |
| Output files | `{type}_{date}.{ext}` | `report_2025-01-15.csv` |

### Directory Structure

```
your_project/
├── src/           # Domain-specific code
├── utils/         # Generic utilities
├── scripts/       # Executable entry points
├── config/        # Configuration files
├── data/          # Input data
└── output/        # Generated output
```

---

## Post-Refactoring Checklist

After moving code between directories:

1. **Update all imports**
   ```bash
   grep -rn "from old_location" scripts/ src/ utils/
   ```

2. **Test execution**
   ```bash
   uv run python scripts/main_script.py --test
   ```

3. **Check for circular dependencies**
   ```bash
   # utils/ should NEVER import from src/
   grep -rn "from src" utils/
   ```

4. **Verify no __main__ blocks in libraries**
   ```bash
   grep -rn "if __name__" src/ utils/
   ```

---

## Related Directives

- **Core organization**: `directives-project-organization.md`
- **Code reuse**: `directives-coding-code-reuse.md`
- **Separation of concerns**: `directives-coding-separation-of-concerns.md`
- **Quick reference**: `directives-quick-reference.md`

---
