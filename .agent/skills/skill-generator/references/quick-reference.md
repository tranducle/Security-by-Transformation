# Antigravity Skills Quick Reference

## File Structure

```
skill-name/
├── SKILL.md              # REQUIRED - Main skill definition
├── scripts/              # Optional - Python/bash/node scripts
├── resources/            # Optional - Templates, configs, static files
├── examples/             # Optional - Input/output examples
├── references/           # Optional - Additional docs
└── .env.example          # Optional - Env var template (NO real values!)
```

## SKILL.md Template

```yaml
---
name: skill-name
description: <Action> + <Target> + <Purpose>. Use when <scenario>.
---

# Title

Overview.

## When to Use
- Scenario 1
- Scenario 2

## Instructions
Steps...

## Examples
Examples...

## Constraints
- Do NOT X
- Always Y
```

## Description Formula

```
<Action verb(s)> + <Target> + <Purpose/Use case>
```

**Examples:**
- "Formats git commit messages according to Conventional Commits specification"
- "Executes read-only PostgreSQL queries to debug data states"
- "Converts JSON snippets into Pydantic models with proper type hints"

## Directory Paths

| Platform | Workspace | Global |
|----------|-----------|--------|
| **Antigravity** | `.agent/skills/` | `~/.gemini/antigravity/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| GitHub Copilot | `.github/skills/` | N/A |

## Naming Conventions

- **Folder names:** kebab-case (`my-skill`, `database-migration`)
- **Skill names:** Lowercase, hyphens allowed
- **Be descriptive:** `git-commit-formatter` (not `gcf`)

## 5 Skill Levels

| Level | Structure | Use Case |
|-------|-----------|----------|
| 1 | SKILL.md only | Conventions, guidelines |
| 2 | + resources/ | Templates, static files |
| 3 | + examples/ | Few-shot patterns |
| 4 | + scripts/ | Validation, complex logic |
| 5 | + all folders | Full-featured workflows |

## Semantic Matching

Skills activate automatically when your request matches the `description` field.

**Good:** "Formats git commit messages according to Conventional Commits specification. Use when user asks to commit changes."
**Bad:** "Git tools"

## Script Tips

```python
# Use relative paths from script location
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '..', 'resources', 'template.txt')
```

```bash
# Always use explicit python
python scripts/myscript.py
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Skill not activating | Improve description specificity |
| Module not found | Add requirements.txt |
| Permission denied | `chmod +x scripts/myscript.py` |
| File not found | Use absolute paths or resolve from script location |

## Checklist

- [ ] Folder name is kebab-case
- [ ] SKILL.md has YAML frontmatter
- [ ] Description follows Action + Target + Purpose formula
- [ ] Instructions are step-by-step
- [ ] Scripts have error handling
- [ ] requirements.txt included (if using Python)
- [ ] .env.example provided (if using env vars)
- [ ] Test in Antigravity to verify activation
