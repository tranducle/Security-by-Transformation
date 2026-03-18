---
name: skill-generator
description: Comprehensive guide for creating Agent Skills for Antigravity, Claude Code, and compatible platforms. Use when creating, building, or developing new skills, or when updating existing skills with scripts, references, templates, or best practices.
license: See LICENSE.txt for terms
version: 2.0.0
---

# Skill Generator

Complete guide for creating Agent Skills that work with **Google Antigravity**, **Claude Code**, and other Agent Skills compatible platforms (GitHub Copilot, VS Code, Cursor, OpenCode).

## Quick Start

### What Are Agent Skills?

Agent Skills is an **open standard** (Anthropic, Dec 2025) for extending AI agent capabilities. Skills are discovered by **semantic matching** and loaded only when relevant.

**Key points:**

- **Progressive Disclosure**: Skills activate automatically based on your request
- **Portable**: Same skill works across Antigravity, Claude, Copilot, etc.
- **File-based**: No servers, no infrastructure - just files
- **Semantic Discovery**: The `description` field determines when skills activate

### Platform-Specific Paths

| Platform | Workspace Path | Global Path |
| :--- | :--- | :--- |
| **Antigravity** | `.agent/skills/` | `~/.gemini/antigravity/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| GitHub Copilot | `.github/skills/` | N/A |

### Minimal Skill Structure

```text
my-skill/
└── SKILL.md
```

That's it! Just a `SKILL.md` file is all you need.

## Skill Templates (5 Levels)

Choose the appropriate complexity level for your skill:

| Level | Structure | Use For |
| :--- | :--- | :--- |
| **1** | SKILL.md only | Conventions, guidelines |
| **2** | + resources/ | Templates, static files |
| **3** | + examples/ | Few-shot patterns |
| **4** | + scripts/ | Validation, logic |
| **5** | + all folders | Full workflows |

See `templates/` folder for ready-to-use templates for each level.

## Skill Creation Process

### Step 1: Initialize (Use Script)

#### Option A: Create for both platforms (Recommended)

```bash
python scripts/create_skill_both_platforms.py <skill-name>
```

Creates skill in **both** `.claude/skills/` AND `.agent/skills/` automatically.

#### Option B: Create for single platform

```bash
python scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates: directory structure, SKILL.md template, example files.

### Step 2: Edit SKILL.md

**CRITICAL**: The `description` field is used for semantic matching - be specific!

**Good:**

```yaml
description: Formats git commits according to Conventional Commits. Use when committing changes.
```

**Bad:**

```yaml
description: Git tools
```

**SKILL.md requirements:**

- **< 100 lines** - split to `references/` if longer
- Description formula: `<Action> + <Target> + <Purpose>`
- Use imperative form: "Create X by doing Y"

### Step 3: Add Resources

**scripts/** - Python/Node scripts for deterministic tasks
**references/** - Documentation for loading as needed
**examples/** - Input/output examples for few-shot learning
**templates/** - Boilerplate code/templates

### Step 4: Validate & Package

```bash
# Validate
python scripts/quick_validate.py <skill-folder>

# Package (includes validation)
python scripts/package_skill.py <skill-folder>
```

## Bundled Resources

### Scripts (`scripts/`)

**When to include**: Code rewritten repeatedly or needs deterministic reliability.

**Requirements:**

- Prefer Python/Node over bash (Windows compatibility)
- Include `requirements.txt` for Python
- Create `.env.example` for env vars
- Write tests for scripts

**Env file priority:** `process.env` > `.agent/skills/${SKILL}/.env` > `.agent/skills/.env`

### References (`references/`)

**When to include**: Documentation loaded as needed.

**Requirements:**

- Each file **< 100 lines** (progressive disclosure)
- Practical instructions, not just explanations
- Use grep patterns in SKILL.md for large files

### Examples (`examples/`)

**When to include**: Few-shot learning patterns.

**Structure:**

```text
examples/
├── input.json
└── output.py
```

## Progressive Disclosure

Skills use three-level loading:

1. **Metadata** (name + description) - Always in context
2. **SKILL.md body** - When skill triggers
3. **Bundled resources** - As needed

This keeps context usage minimal while enabling complex workflows.

## Best Practices

### Naming

- Use **kebab-case**: `my-skill`, `database-migration`
- Be descriptive: `git-commit-formatter` (not `gcf`)

### Description Formula

```text
<Action verb(s)> + <Target> + <Purpose/Use case>
```

Examples:

- "Formats git commits according to Conventional Commits"
- "Executes read-only PostgreSQL queries to debug data"
- "Converts JSON to Pydantic models with type hints"

### File Size Limits

- **SKILL.md**: < 100 lines
- **Reference files**: < 100 lines each
- **Scripts**: No limit (executed, not loaded)

## Further Reading

**Templates:** `templates/` folder

- `level-1-minimal.md` - Instructions-only
- `level-2-with-resources.md` - With templates
- `level-3-with-examples.md` - Few-shot patterns
- `level-4-with-scripts.md` - With scripts
- `level-5-full-featured.md` - Complete workflows

**References:** `references/` folder

- `quick-reference.md` - Quick lookup
- `antigravity-skill-creation-guide.md` - Comprehensive guide
- `antigravity-skill-templates.md` - Template collection

**External:**

- [Agent Skills (Claude)](https://docs.claude.com/en/docs/claude-code/skills.md)
- [Google Antigravity Docs](https://antigravity.google/docs/skills)
