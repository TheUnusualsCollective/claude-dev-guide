---
name: session-management
description: PROACTIVELY invoke at the START of every new conversation to load project context and development status. Also invoke when user indicates session end (e.g., "wrapping up", "that's all", "goodbye").
---

<!--
TEMPLATE: Rename this directory from "session-management-TEMPLATE" to "session-management" to activate.
Customize paths and workflows to match your project structure.
-->

# Session Management Skill

This skill ensures development continuity across sessions by managing development notes and status tracking.

## When to Use

**Session Start** - Automatically invoke when:
- Starting a new conversation in this project
- User asks about current project state or "what were we working on"
- User wants to continue previous work

**Session End** - Automatically invoke when:
- User indicates they're done for now ("let's wrap up", "that's all for today")
- User explicitly asks to document/save progress
- Significant milestone completed and user is pausing

## Session Start Workflow

1. **Read development status**: Read your status file to identify:
   - Current project phase
   - Latest session summary
   - Current notes file index
   <!-- Customize: Update path to your status file -->
   <!-- Example: `project-notes/development-status.md` -->

2. **List notes archive**: List files in your notes archive directory to verify the index.
   <!-- Customize: Update path to your notes archive -->
   <!-- Example: `project-notes/development-notes-archive/` -->

3. **Read current notes**: Read the latest development notes file.

4. **Present summary**: Provide a concise summary including:
   - Project phase
   - What was accomplished in the last session
   - Current next steps (prioritized list)
   - Any blockers or open questions

5. **Ask about new session**: Ask the user:
   - "Are you starting new major work that warrants a new notes file, or continuing the previous session's work?"

6. **If new notes file needed**:
   - Create new notes file with incremented index
   - Update status file with new index
   <!-- See session-start.md command for template structure -->

7. **Confirm ready**: Confirm the session is set up and ask what the user wants to work on.

## Session End Workflow

1. **Read current status**: Read status file to identify the current notes file.

2. **Read current notes**: Read the current development notes file.

3. **Generate session summary**: Based on the conversation, compile:
   - What was accomplished this session
   - Key decisions made
   - Files created or modified
   - Technical notes worth preserving
   - Any open questions or blockers for next session

4. **Present summary for review**: Show the user the proposed updates and ask for any corrections or additions.

5. **Update notes file**: Update the current development notes with session details.

6. **Update development status**: Update status file:
   - Update "Last Updated" date to today
   - Update "Latest Session" line with accurate summary
   - Update "Current State / Project Phase" if there was a significant milestone
   - Add/remove/reorder Next Steps based on what was completed or discovered

7. **Check notes file size**: If approaching ~6k tokens (~150+ lines), note this for next session.

8. **Confirm completion**: Confirm the session has been documented.

## Critical Rules

- Update current development-notes throughout session (not just at end)
- Document decisions when made (not later)
- Create new notes file when approaching ~6k tokens
- NEVER modify archived development-notes files

## Manual Invocation

Users can also manually invoke these workflows using slash commands:
- `/session-start` - Initialize session
- `/session-end` - Finalize session

## Customization Checklist

Before using this skill, update the following:

- [ ] Rename directory from `session-management-TEMPLATE` to `session-management`
- [ ] Update status file path in workflow steps
- [ ] Update notes archive path in workflow steps
- [ ] Adjust notes file naming convention if needed
- [ ] Review "When to Use" triggers for your workflow
