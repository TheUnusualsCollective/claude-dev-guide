---
description: Initialize session with development status and current notes
---

Execute the session start workflow for this project.

## Steps

1. **Read development status**: Read `claude-config/development-status.md` to identify:
   - Current project phase
   - Latest session summary
   - Current notes file index (extract from the "Development Notes" line)

2. **List notes archive**: List files in `project-notes/development-notes-archive/` to verify the index.

3. **Read current notes**: Read the latest `development-notes_XXX.md` file.

4. **Present summary**: Provide a concise summary including:
   - Project phase
   - What was accomplished in the last session
   - Current next steps (prioritized list)
   - Any blockers or open questions

5. **Ask about new session**: Ask the user:
   - "Are you starting new major work that warrants a new notes file, or continuing the previous session's work?"

6. **If new notes file needed**:
   - Create `project-notes/development-notes-archive/development-notes_<NEXT_INDEX>.md` with template:
     ```
     # Development Notes XXX - [Title TBD]

     **Date**: [TODAY]
     **Focus**: [To be filled as work progresses]

     ## Session Summary

     [To be updated throughout session]

     ## Key Decisions Made

     [Document decisions as they happen]

     ## Files Created

     [List new files]

     ## Files Modified

     [List modified files]

     ## Technical Notes

     [Implementation details worth preserving]

     ## Future Considerations

     [Ideas for later]
     ```
   - Update `claude-config/development-status.md`:
     - Update "Last Updated" date
     - Update "Development Notes" range to include new file
     - Update "Latest Session" line with new index and placeholder description

7. **Confirm ready**: Confirm the session is set up and ask what the user wants to work on.
