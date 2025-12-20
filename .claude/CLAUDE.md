# Claude Code Configuration

**Template Version**: 1.1.0

## Project Structure
<!-- See claude-config/project-structure.md -->

## Project Commands
<!-- See claude-config/commands.md -->

### Build Plugin

### Development Mode


## Project-Specific Configuration
<!-- Reference your project-specific files here -->
- Technology stack: See claude-config/tech-stack.md
- Implementation workflow: See claude-config/workflow.md
- Build commands: See claude-config/commands.md
- API documentation: See claude-config/api-docs.md


## Session Workflow

**Use slash commands for session management:**
- `/session-start` - Initialize session (reads status, notes, sets up context)
- `/session-end` - Finalize session (updates notes and status)

### During Session

**Update notes file immediately when:**
- Making architecture/design decisions
- Discovering new API capabilities or bugs
- Implementing major features
- Any material discovery relevant to future work

**DO NOT wait until end of session** - update as you go!

### Critical Rules

- ✅ Update current development-notes throughout session
- ✅ Document decisions when made (not later)
- ✅ Create new file when approaching ~6k tokens
- ❌ NEVER modify archived development-notes files


## Directives

**Project directives ensure consistency, quality, and maintainability.**

**Framework**: See `claude-config/directives/directives-usage-guide.md` for when and how to use directives.

### Critical Rules (Always Apply)

**Python Package Management:**
- ONLY use `uv` (NEVER `pip`)
- Add package: `uv add package`
- Run code: `uv run script.py`

**Code Organization:**
- NO `if __name__ == "__main__"` in library files (`src/`, `utils/`)
- Executable scripts ONLY in `scripts/` directory
- NO hard-coded dictionary keys in generic functions
- NO duplicated I/O logic (use `utils/file_utils.py`)

**Before Writing New Code:**
1. Search: `grep -r "def similar_function" python/`
2. Check if existing code can be generalized
3. Only create new if fundamentally different

**Console Output:**
- ALWAYS use `logging` module (NEVER `print()` for status)
- NO Unicode in print()/logging output (causes Windows encoding errors)
- Use ASCII: `[OK]` `[FAIL]` `[WARN]` not `✓` `❌` `⚠`
- Unicode IS allowed in documents/markdown

**Git Commit Messages:**
- ❌ **DO NOT** include Claude attribution (`Generated with [Claude Code]` or `Co-Authored-By: Claude`)
- ✅ **DO** write clear, professional commit messages with context

### Directive Categories

**Core:**
- `directives-quick-reference.md` - Essential rules (always read first)
- `directives-usage-guide.md` - How to use directives effectively

**Coding Standards:**
- `directives-coding-separation-of-concerns.md` - Logic/I/O/presentation separation
- `directives-coding-function-design.md` - Writing clear, reusable functions
- `directives-coding-code-reuse.md` - DRY principle and shared utilities
- `directives-coding-refactoring.md` - Improving existing code
- `directives-coding-parameterization.md` - Avoiding hard-coded values
- `directives-coding-logging.md` - Proper logging practices
- `directives-coding-organization.md` - Code structure and imports
- `directives-coding-ascii-output.md` - ASCII-only console output (Windows compatibility)

**Python Specific:**
- `directives-python-package-management.md` - Using `uv` for dependencies

**Project Specific:**
- `directives-project-organization.md` - Directory structure
- `directives-antipatterns.md` - Common mistakes to avoid

**All directives**: See `claude-config/directives/` directory

---

