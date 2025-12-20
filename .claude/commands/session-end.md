---
description: Finalize session by updating notes and development status
---

Execute the session end workflow for this project.

## Steps

1. **Read current status**: Read `claude-config/development-status.md` to identify the current notes file.

2. **Read current notes**: Read the current `development-notes_XXX.md` file.

3. **Generate session summary**: Based on the conversation, compile:
   - What was accomplished this session
   - Key decisions made
   - Files created or modified
   - Technical notes worth preserving
   - Any open questions or blockers for next session

4. **Present summary for review**: Show the user the proposed updates and ask for any corrections or additions.

5. **Update notes file**: Update `project-notes/development-notes-archive/development-notes_XXX.md` with:
   - Session Summary section
   - Key Decisions Made section
   - Files Created section
   - Files Modified section
   - Technical Notes section (if applicable)
   - Future Considerations section (if applicable)

6. **Update development status**: Update `claude-config/development-status.md`:
   - Update "Last Updated" date to today
   - Update "Latest Session" line with accurate summary of what was accomplished
   - Update "Current State / Project Phase" if there was a significant milestone
   - Add/remove/reorder Next Steps based on what was completed or discovered
   - Update Key Files table if new important files were created

7. **Check notes file size**: If the current notes file is approaching ~6k tokens (roughly 150+ lines of content), note this so the next session knows to create a new file.

8. **Confirm completion**: Confirm the session has been documented and remind about any pending items for next session.
