# Level 2 Skill Template

## Directory Structure

```
your-skill/
├── SKILL.md
└── resources/
    └── template.txt
```

## SKILL.md Template

```yaml
---
name: your-skill
description: Generates or processes [target] using templates. Use when user needs to [specific action].
---

# Skill Title

Overview of this skill.

## Instructions

1. Read the template from `resources/template.txt`
2. Process or modify it
3. Output the result

## Example

User: "Create a new [file type]"

You should:
1. Read `resources/template.txt`
2. Fill in the blanks
3. Output the complete file
```

## resources/template.txt Template

```
Your template content here.
Use {{placeholder}} for variables.
```

## Use Cases

- License header insertion
- Code template generation
- Config file creation
- Standardized text blocks
