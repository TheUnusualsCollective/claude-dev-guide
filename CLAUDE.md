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

**BEFORE any work, you MUST:**

1. **Read development status**: `claude-config/development-status.md` (identifies current notes file index)
2. **Verify file structure**: List `project-notes/development-notes-archive/` to confirm current index
3. **Read current notes**: `project-notes/development-notes-archive/development-notes_XXX.md` (use index from step 1)
4. **Create new notes file if needed**:
   - Increment index when starting new major work session
   - **ALWAYS create in**: `project-notes/development-notes-archive/development-notes_<NEXT>.md`
   - **NEVER create in**: `claude-config/`

### Update Triggers

**Update notes file immediately when:**
- Making architecture/design decisions
- Discovering new API capabilities or bugs
- Implementing major features
- Identifying constraints or trade-offs
- Any material discovery relevant to future work

**DO NOT wait until end of session** - update as you go!

**Update status file when:**
- Goals achieved or todo items completed
- Development notes file updated
- Phase transitions or major milestones

### Critical Rules

- ✅ Update current development-notes throughout session
- ✅ Document decisions when made (not later)
- ✅ Create new file when approaching ~6k tokens
- ❌ NEVER modify archived development-notes files

**Detailed Guidelines**: See `claude-config/directives/directives-session-workflow.md`


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

**Logging:**
- ALWAYS use `logging` module (NEVER `print()`)
- NO Unicode characters (use ASCII: `[OK]` not `✓`)

**Git Commit Messages:**
- ❌ **DO NOT** include Claude attribution (`Generated with [Claude Code]` or `Co-Authored-By: Claude`)
- ✅ **DO** write clear, professional commit messages with context

### Directive Categories

**Core:**
- `directives-quick-reference.md` - Essential rules (always read first)
- `directives-usage-guide.md` - How to use directives effectively

**Workflow:**
- `directives-session-workflow.md` - Development notes and status tracking

**Coding Standards:**
- `directives-coding-separation-of-concerns.md` - Logic/I/O/presentation separation
- `directives-coding-function-design.md` - Writing clear, reusable functions
- `directives-coding-code-reuse.md` - DRY principle and shared utilities
- `directives-coding-refactoring.md` - Improving existing code
- `directives-coding-parameterization.md` - Avoiding hard-coded values
- `directives-coding-logging.md` - Proper logging practices
- `directives-coding-organization.md` - Code structure and imports

**Python Specific:**
- `directives-python-package-management.md` - Using `uv` for dependencies

**Project Specific:**
- `directives-project-organization.md` - Directory structure
- `directives-antipatterns.md` - Common mistakes to avoid

**All directives**: See `claude-config/directives/` directory

---

