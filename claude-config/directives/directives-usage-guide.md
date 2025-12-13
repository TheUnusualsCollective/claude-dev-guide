# Directives Usage Guide

**Purpose**: Framework for when and how to use project directives during development.

**Last Updated**: 2025-12-13

---

## What Are Directives?

Directives are project-specific guidelines that ensure consistency, quality, and maintainability. They capture:
- Coding standards and patterns
- Workflow requirements
- Anti-patterns to avoid
- Project-specific conventions

Think of directives as "how we do things in this project."

---

## When to Review Directives

### Simple Tasks (NO directive review needed)

Skip directive review for straightforward tasks:
- Single file read
- Running existing commands
- Answering questions without code changes
- Minor documentation updates
- Small configuration changes

### Complex Tasks (REQUIRES directive review)

**MUST review directives before starting:**
- Writing new functions or classes
- Modifying existing code logic
- Adding dependencies
- Refactoring code
- Creating new files
- Multi-file changes
- Implementing new features

---

## Directive Review Workflow

**If your task is complex, follow this workflow:**

### 1. STOP
- Do not begin coding immediately
- Take time to understand requirements and context

### 2. READ Relevant Directives
- **ALWAYS read**: `claude-config/directives/directives-quick-reference.md`
- **Read as needed** based on task domain:
  - **Coding tasks**: Review relevant `directives-coding-*.md` files
  - **Session workflow**: `directives-session-workflow.md`
  - **Python packages**: `directives-python-package-management.md`
  - **Project organization**: `directives-project-organization.md`
  - **Avoiding mistakes**: `directives-antipatterns.md`

### 3. SEARCH for Existing Implementations
- Look for similar functions: `grep -r "def similar_function" python/`
- Check if existing code can be generalized
- Avoid reinventing the wheel

### 4. REVIEW Recent Development Notes
- Read last 1-2 sessions: `project-notes/development-notes-archive/development-notes_XXX.md`
- Understand recent decisions and context
- Identify patterns and constraints

### 5. PLAN Your Approach
- Design solution following established patterns
- Consider separation of concerns
- Plan for reusability and testability
- Identify which existing utilities to leverage

### 6. IMPLEMENT
- Write code following directive guidelines
- Keep directives in mind during implementation
- Leave code better than you found it

---

## Cost vs Benefit

### Upfront Cost
- **10-20k tokens** to review directives and existing code
- **5-10 minutes** of reading and planning

### Benefit
- **Avoid 50-200k tokens** of refactoring later
- **Prevent technical debt** accumulation
- **Maintain consistency** across codebase
- **Faster future development** through reusable code

**The investment in reading directives pays dividends throughout the project lifecycle.**

---

## Which Directives to Read for Common Tasks

### Writing New Functions
- `directives-quick-reference.md` (always)
- `directives-coding-function-design.md`
- `directives-coding-separation-of-concerns.md`
- `directives-coding-code-reuse.md`

### Refactoring Code
- `directives-quick-reference.md` (always)
- `directives-coding-refactoring.md`
- `directives-coding-code-reuse.md`
- `directives-antipatterns.md`

### Adding Visualization Features
- `directives-quick-reference.md` (always)
- `directives-coding-separation-of-concerns.md`
- `directives-coding-parameterization.md`
- `directives-coding-organization.md`

### Processing/Analysis Scripts
- `directives-quick-reference.md` (always)
- `directives-coding-separation-of-concerns.md`
- `directives-coding-logging.md`
- `directives-python-package-management.md`

### Project Organization
- `directives-quick-reference.md` (always)
- `directives-project-organization.md`
- `directives-coding-organization.md`

---

## Directive Categories

### Core Guidelines
- **directives-quick-reference.md**: Essential rules, always read first
- **directives-usage-guide.md**: This file - how to use directives

### Workflow
- **directives-session-workflow.md**: Development notes and status tracking

### Coding Standards
- **directives-coding-separation-of-concerns.md**: Logic, I/O, presentation separation
- **directives-coding-function-design.md**: Writing clear, reusable functions
- **directives-coding-code-reuse.md**: DRY principle and shared utilities
- **directives-coding-refactoring.md**: Improving existing code
- **directives-coding-parameterization.md**: Avoiding hard-coded values
- **directives-coding-logging.md**: Proper logging practices
- **directives-coding-organization.md**: Code structure and imports

### Problem Solving
- **directives-problem-isolation.md**: Reduce/verify/expand debugging workflow
- **directives-coordinate-system-transforms.md**: Multi-format coordinate transformations

### Python Specific
- **directives-python-package-management.md**: Using `uv` for dependencies

### Project Specific
- **directives-project-organization.md**: Directory structure and file organization
- **directives-antipatterns.md**: Common mistakes to avoid

---

## Best Practices

### Do
- Review directives BEFORE starting complex work
- Load only relevant directives (saves tokens)
- Keep directives in mind during implementation
- Update directives when discovering new patterns
- Reference directive files in development notes

### Don't
- Skip directive review for complex tasks
- Load all directives at once (wastes tokens)
- Ignore directives because "my way is better"
- Create new patterns without documenting them
- Assume you remember all guidelines

---

## Authoring Directives

When creating or updating directives, follow these principles:

### Keep Directives Concise

Every token consumed by directives is context unavailable for actual work.

- **Target**: Under 200 lines per directive
- **Reduce verbiage** to minimum necessary to convey the principle
- **Prefer tables and lists** over prose
- **One code example** is usually enough - don't show 5 variations

### Single Focus Per Directive

Each directive should address ONE topic:

- **Good**: `directives-problem-isolation.md` - one methodology
- **Bad**: `directives-debugging-and-testing-and-deployment.md` - too broad

If a directive grows beyond its focus, split it.

### Reference, Don't Duplicate

When a directive needs content from another:

```markdown
## Related Directives
- **directives-problem-isolation.md**: Reduce/verify/expand workflow
```

Do NOT copy the content into both files.

### Hierarchical Loading

Directives are loaded on-demand, not all at once:

- **Quick reference**: Always loaded for complex tasks
- **Topic-specific**: Loaded only when relevant
- **Project-specific**: Loaded for domain work

Design directives so they stand alone but link to related guidance.

### Standard Structure

```markdown
# Directive: [Topic]

**Purpose**: One-line description

**Last Updated**: YYYY-MM-DD

---

## Core Principle
[The key insight in 1-2 sentences]

---

## [Main Sections]
[Concise guidance with minimal examples]

---

## Checklist
[Quick verification items]

---

## Related Directives
[Links to related guidance]
```

---

## Updating Directives

Directives evolve as the project grows. Update them when:
- Discovering new anti-patterns
- Establishing new conventions
- Finding better approaches
- Identifying missing guidance

**Location**: All directives live in `claude-config/directives/`

**Format**: Markdown files following the standard structure above

---

## Integration with Development Workflow

Directives work alongside other project documentation:

1. **CLAUDE.md**: Entry point, references directive framework
2. **Directives**: Standards and patterns (this folder)
3. **Development Notes**: Session-specific discoveries and decisions
4. **Development Status**: Current project state and active notes file

**Workflow**: Read directives → Follow patterns → Document discoveries → Update directives as needed

---
