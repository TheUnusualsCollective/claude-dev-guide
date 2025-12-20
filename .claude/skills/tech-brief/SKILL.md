---
name: tech-brief
description: Generate structured technical briefs for features, tools, or systems. Use when asked to create a tech brief, technical summary, or system overview document.
---

# Technical Brief Skill

## Output Format
When creating a technical brief, structure it as:

1. **Purpose** - One sentence stating what this solves
2. **Context** - Why this matters now (2-3 sentences)
3. **Approach** - How it works at a high level
4. **Key Decisions** - Bullet list of important choices made and why
5. **Dependencies** - What this relies on
6. **Risks/Open Questions** - Known issues or unknowns

## Output Location

**Determining where to save:**
1. If the user specifies a path (e.g., "output to X", "save in X", "write to X"), use that path
2. If the project has a `docs/` directory, use `docs/tech-briefs/`
3. Otherwise, use `tech-briefs/` in the project root

Create the directory if it doesn't exist.

**Filename**: Use `{topic-slug}.md` (lowercase, hyphenated)

## Guidelines
- Keep each section concise (3-5 sentences max except bullets)
- Use concrete specifics, not vague generalities
- If information is missing, note it rather than inventing