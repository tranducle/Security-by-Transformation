# Level 3 Skill Template

## Directory Structure

```
your-skill/
├── SKILL.md
└── examples/
    ├── input.json
    └── output.py
```

## SKILL.md Template

```yaml
---
name: your-skill
description: Converts [input format] to [output format] following specific patterns. Use when user provides [input type] and needs [output type].
---

# Skill Title

Overview of this conversion/transformation skill.

## Instructions

1. Analyze the input provided by the user
2. Review the examples in `examples/` to understand the pattern
3. Apply the same pattern to user's input
4. Generate output following the example format

## Examples

See `examples/` folder for reference:
- `input.json` - Example input
- `output.py` - Corresponding output

## Pattern Rules

- Rule 1 for conversion
- Rule 2 for conversion
- Rule 3 for conversion
```

## examples/input.json Template

```json
{
  "key1": "value1",
  "key2": "value2",
  "nested": {
    "key3": "value3"
  }
}
```

## examples/output.py Template

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class NestedClass:
    key3: str

@dataclass
class RootClass:
    key1: str
    key2: str
    nested: NestedClass
```

## Use Cases

- JSON to Pydantic models
- JSON to TypeScript interfaces
- SQL to ORM models
- API response to data classes
- Format conversion with specific patterns
