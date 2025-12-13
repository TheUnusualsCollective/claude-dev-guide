# Project Notes

This directory houses important project-related documentation, including session development notes and other reference material created by users or Claude.

## Directory Structure

```
project-notes/
├── README.md                      # This file
├── development-status.md          # Current project state and notes index
├── development-notes-archive/     # Sequential session notes (see below)
│   ├── development-notes_001.md
│   ├── development-notes_002.md
│   └── ...
└── [other-notes].md               # Additional project documentation
```

## Development Status

The `development-status.md` file tracks:
- Current project phase and state
- Active development notes file index
- Key capabilities and recent accomplishments
- Next steps and priorities

This file should be read at the start of every session and updated when milestones are reached.

## Development Notes Archive

The `development-notes-archive/` subdirectory contains session-by-session development notes that provide continuity across Claude Code sessions.

### Purpose

Development notes capture:
- Architecture and design decisions
- Discovered bugs, limitations, or constraints
- Implementation details for major features
- Trade-offs and their rationale
- Any material discovery relevant to future work

### Usage

1. **New sessions**: Create a new numbered file when starting major work
2. **During work**: Update notes immediately when making decisions (not at session end)
3. **File size**: Create a new file when approaching ~6k tokens
4. **Archive rule**: Never modify old notes files - they are historical record

## Other Project Notes

This directory can also contain other important project documentation:
- Research findings
- Reference material
- Design documents
- Meeting notes
- Any documentation that supports the project but doesn't belong in code

Both users and Claude can create notes here. Use descriptive filenames.

## Why This Matters

Claude Code sessions are stateless. Without development notes:
- Decisions get relitigated
- Context is lost between sessions
- Mistakes get repeated
- Architectural coherence degrades

With development notes:
- New sessions start with full context
- Decisions are documented with rationale
- Progress builds on previous work
- The project maintains consistency

## See Also

- `development-status.md` - Current project state and active notes index
- `../claude-config/directives/directives-session-workflow.md` - Detailed workflow guidelines
