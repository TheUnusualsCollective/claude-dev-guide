---
name: skill-name
description: Brief description that tells Claude WHEN to use this skill (critical for triggering)
---

# Instructions

Your instructions for Claude go here in markdown.
```

**Mechanics**: Claude scans available skill descriptions, loads relevant ones when triggered, and follows the instructions. You upload the folder as a ZIP to Settings > Capabilities > Skills.

**Simple Example Skill** - Let's make a "Technical Brief" skill that formats technical summaries consistently:
```
[SKILL-NAME-DIRECTORY]/
└── SKILL.md