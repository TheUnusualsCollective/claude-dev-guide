# Claude Code Configuration

**Template Version**: 1.1.0

## Project Structure
<!-- See claude-config/project-structure.md -->

## Project Commands
<!-- See claude-config/commands.md -->

### Build Plugin

### Development Mode


## Project-Specific Configuration
<!-- Customize these for your project -->
- Technology stack: See `claude-config/tech-stack.md` (create if needed)
- Implementation workflow: See `claude-config/workflow.md` (create if needed)
- Build commands: See `claude-config/commands.md` (create if needed)
- Project-specific directives: See `claude-config/directives/directives-project-specific-TEMPLATE.md`

---

## Specialized Agents

Use these for domain-specific tasks:

| Agent | Use For |
| ----- | ------- |
| `python-general` | General Python utilities, file I/O, data processing |
| `prototype-builder` | Rapid prototyping, proof-of-concept implementations |
| `docs-curator` | Documentation review, updates, and maintenance |
| `code-reviewer` | Code review, quality feedback, PR evaluation |

**Adding project-specific agents:** Create new `.md` files in `.claude/agents/` following the existing format.

---

## Session Workflow

Development notes provide continuity across sessions. Customize paths for your project.

**BEFORE any work, you MUST:**

1. **Read development status**: `project-notes/development-status.md` (identifies current notes file index)
2. **Read current notes**: Use the index from status file to find the current notes file
3. **Create new notes file if needed**: Increment index when starting new major work session

**Recommended structure:**
```
project-notes/
├── development-status.md          # Current state and notes index
└── development-notes-archive/
    ├── development-notes_001.md
    ├── development-notes_002.md
    └── ...
```

### Update Triggers

**Update notes file immediately when:**
- Making architecture/design decisions
- Discovering bugs or limitations
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

### What You MUST Do

- **Use `uv`** for all package management (`uv add`, `uv run`)
- **Use `logging` module** for all status output
- **Use ASCII only** in console output (`[OK]` `[FAIL]` `[WARN]`)
- **Search for existing code** before writing new functions
- **Put executable scripts** in `scripts/` directory only

### What You MUST NOT Do

- **NEVER** use `pip` - only `uv`
- **NEVER** add `if __name__ == "__main__"` in library files (`src/`, `lib/`, `utils/`)
- **NEVER** use `print()` for status messages - use `logging`
- **NEVER** use Unicode in console output (causes Windows encoding errors)
- **NEVER** hard-code values that should be parameters
- **NEVER** duplicate I/O logic - create/use utilities
- **NEVER** include Claude attribution in git commit messages

### Red Flags

Watch for these anti-patterns that indicate a problem:
- `print()` statements in library code
- `pip install` or `pip freeze` commands
- `if __name__ == "__main__":` in `src/`, `lib/`, or `utils/`
- Hard-coded paths or configuration values
- Duplicated file reading/writing logic across files
- Unicode symbols in logging output

### Before Writing New Code

1. Search: `grep -r "def similar_function" src/`
2. Check if existing code can be generalized
3. Only create new if fundamentally different

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

**Problem Solving:**
- `directives-problem-isolation.md` - Reduce/verify/expand debugging workflow
- `directives-coordinate-system-transforms.md` - Multi-format coordinate transformations

**Python Specific:**
- `directives-python-package-management.md` - Using `uv` for dependencies

**Project Organization:**
- `directives-project-organization.md` - Directory structure and patterns
- `directives-antipatterns.md` - Common mistakes to avoid
- `directives-project-specific-TEMPLATE.md` - Template for project-specific overrides

**All directives**: See `claude-config/directives/` directory

---

