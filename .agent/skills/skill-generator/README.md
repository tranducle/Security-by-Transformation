# Antigravity Skill Creator

A reusable skill for creating Agent Skills compatible with Google Antigravity platform.

## What This Does

This skill provides complete guidance for creating Agent Skills. When you say:

- "Create a skill for [purpose]"
- "Build a new skill to [action]"
- "Make a skill that [description]"

The AI agent will automatically activate this skill and follow its instructions to help you create a proper skill.

## Installation Options

### Option 1: Copy to Another Project (Workspace Skill)

Copy the entire folder to your other project:

```bash
# On Linux/Mac
cp -r .agent/skills/antigravity-skill-creator /path/to/other-project/.agent/skills/

# On Windows (PowerShell)
Copy-Item -Recurse .agent\skills\antigravity-skill-creator E:\path\to\other-project\.agent\skills\

# On Windows (Command Prompt)
xcopy /E /I .agent\skills\antigravity-skill-creator E:\path\to\other-project\.agent\skills\antigravity-skill-creator\
```

**Use this when:** The skill is specific to a single project or team.

### Option 2: Install Globally (Available to All Projects)

Copy to your global Antigravity skills directory:

```bash
# On Linux/Mac
cp -r .agent/skills/antigravity-skill-creator ~/.gemini/antigravity/skills/

# On Windows (PowerShell)
Copy-Item -Recurse .agent\skills\antigravity-skill-creator $env:USERPROFILE\.gemini\antigravity\skills\

# On Windows (Command Prompt)
xcopy /E /I .agent\skills\antigravity-skill-creator %USERPROFILE%\.gemini\antigravity\skills\antigravity-skill-creator\
```

**Use this when:** You want the skill available across all your projects.

## How Skills Activate

Agent Skills uses **semantic matching** - there's no manual activation needed.

1. **Session Start:** Agent sees all skill descriptions (lightweight metadata)
2. **User Request:** You say "Create a skill for JSON formatting"
3. **Semantic Match:** Agent compares your request to all skill descriptions
4. **Automatic Load:** Skills matching above a threshold are loaded with full instructions
5. **Execution:** Agent follows the skill's instructions

This skill's description includes keywords like:
- "create, build, develop, or make a new skill"
- "skill structure, SKILL.md format"
- "directory organization, best practices"

So various phrasings will activate it:
- "Create a skill for X"
- "Build a new skill"
- "I need to make a skill"

## Folder Structure

```
antigravity-skill-creator/
├── SKILL.md                              # Main skill definition (READ THIS FIRST)
├── README.md                             # This file
├── references/                           # Supporting documentation
│   ├── quick-reference.md                # Quick lookup guide
│   ├── antigravity-skill-creation-guide.md  # Comprehensive guide
│   └── antigravity-skill-templates.md    # Template collection
└── templates/                            # Ready-to-use templates
    ├── level-1-minimal.md                # Instructions-only skill
    ├── level-2-with-resources.md         # With templates/assets
    ├── level-3-with-examples.md          # With few-shot examples
    ├── level-4-with-scripts.md           # With validation scripts
    └── level-5-full-featured.md          # Complete scaffolding skill
```

## Quick Start

1. **Copy this folder** to your project's `.agent/skills/` or global location
2. **Start Antigravity** and open a chat
3. **Say:** "Create a skill for [your purpose]"
4. **Follow the instructions** provided by the agent

## Platform Compatibility

This skill follows the **Agent Skills Open Standard** and works with:

| Platform | Status | Workspace Path |
|----------|--------|----------------|
| **Google Antigravity** | ✅ Primary | `.agent/skills/` |
| Claude Code | ✅ Compatible | `.claude/skills/` |
| GitHub Copilot | ✅ Compatible | `.github/skills/` |
| VS Code | ✅ Compatible | `.github/skills/` |
| Cursor | ✅ Compatible | `.cursor/skills/` |
| OpenCode | ✅ Compatible | `.opencode/skill/` |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-15 | Initial release |

## License

See LICENSE.txt for terms.

## Additional Resources

- [Google Antigravity Official Docs](https://antigravity.google/docs/skills)
- [Agent Skills Open Standard](https://www.anthropic.com/)
- [Google Cloud Skills Tutorial](https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d)

## Support

For issues or questions:
1. Check `references/quick-reference.md` for common solutions
2. Review `references/antigravity-skill-creation-guide.md` for detailed guidance
3. Consult Antigravity community forums
