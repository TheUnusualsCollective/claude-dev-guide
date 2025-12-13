# Python Package Management Directives

**ALWAYS use `uv` for package management. NEVER use `pip` directly.**

**Last Updated**: 2025-11-26

---

## Core Rules

1. **Package Manager**
   - ONLY use uv, NEVER pip
   - Installation: `uv add package`
   - Removal: `uv remove package`
   - Running: `uv run script.py`
   - FORBIDDEN: `pip install`, `pip freeze`, manual venv activation

2. **Project Setup**
   - Initialize: `uv init` (creates pyproject.toml)
   - Pin Python: `uv python pin 3.13`
   - Create env: `uv venv`
   - Install deps: `uv sync`

3. **Daily Workflow**
   - Add dependency: `uv add numpy`
   - Add dev dependency: `uv add --dev pytest`
   - Run code: `uv run script.py`
   - Update lock: `uv lock`

---

## uv vs py.exe

**Use uv for:**
- Project dependencies: `uv add package`
- Running project code: `uv run script.py`
- Virtual environments: `uv venv`
- Python version management: `uv python install 3.13`

**Use py.exe for:**
- Quick one-off scripts outside projects
- Version selection: `py -3.13 script.py`

**NEVER mix:** Don't use pip in uv projects

---

## Required Files

**Commit these:**
- `pyproject.toml` - Project metadata + dependencies
- `uv.lock` - Exact versions (auto-generated)
- `.python-version` - Pinned Python version

**Ignore these:**
- `.venv/` - Virtual environment (in .gitignore)

---

## Common Commands

| Task | Command |
|------|---------|
| Add package | `uv add package` |
| Add dev package | `uv add --dev package` |
| Remove package | `uv remove package` |
| Install all | `uv sync` |
| Run script | `uv run script.py` |
| Run tool | `uv run pytest` |
| Update lock | `uv lock` |
| Dependency tree | `uv tree` |

---

## Forbidden Patterns

```bash
# ❌ NEVER
pip install package          # Use: uv add package
pip freeze > requirements.txt  # Use: pyproject.toml + uv.lock
source .venv/bin/activate    # Use: uv run
python script.py             # Use: uv run script.py
pip install --user package   # Use: uv add package (project-local)

# ✅ ALWAYS
uv add package
uv run script.py
uv sync
git add pyproject.toml uv.lock
```

---

## Installation

- **Location**: `C:\Users\judah\.local\bin\uv.exe` (in PATH)
- **Version**: 0.9.13
- **Cache**: `C:\Users\judah\AppData\Local\uv\cache`

---

## Troubleshooting

1. **Command not found**
   - Open new terminal (PATH not updated in current shell)
   - Or use full path: `C:\Users\judah\.local\bin\uv.exe`

2. **Dependency conflicts**
   - Check tree: `uv tree`
   - Try upgrade: `uv lock --upgrade`

3. **Wrong Python**
   - Pin version: `uv python pin 3.13`
   - Recreate env: `rm -rf .venv && uv venv`

4. **Cache issues**
   - Clean cache: `uv cache clean`

---
