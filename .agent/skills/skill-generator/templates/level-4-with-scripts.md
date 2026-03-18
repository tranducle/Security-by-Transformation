# Level 4 Skill Template

## Directory Structure

```
your-skill/
├── SKILL.md
├── scripts/
│   ├── main.py
│   └── requirements.txt
└── .env.example
```

## SKILL.md Template

```yaml
---
name: your-skill
description: Validates or processes [target] using deterministic logic. Use when user needs to [specific action] with binary accuracy.
---

# Skill Title

Overview of this validation/processing skill.

## Instructions

1. **Do NOT process manually** - use the validation script for accuracy
2. Run the script:
   ```bash
   python scripts/main.py <input_file>
   ```
3. Interpret the output:
   - Exit code 0: Success
   - Exit code 1: Failure (check error messages)

## Prerequisites

Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

## Error Handling

If script fails:
1. Read the error message from stdout
2. Report to user with suggested fix
3. Do NOT retry automatically

## Environment Variables

If using `.env.example`:
- Copy to `.env` and fill in values
- Never commit actual `.env` file
```

## scripts/main.py Template

```python
#!/usr/bin/env python3
"""
Script description.
"""

import sys
import argparse

def validate(input_file: str) -> int:
    """
    Validate input file.

    Args:
        input_file: Path to input file

    Returns:
        0 for success, 1 for failure
    """
    try:
        with open(input_file, 'r') as f:
            content = f.read()

        # Validation logic here
        errors = []

        if errors:
            for err in errors:
                print(f"ERROR: {err}")
            return 1

        print("Validation passed!")
        return 0

    except FileNotFoundError:
        print(f"ERROR: File '{input_file}' not found")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Validate input")
    parser.add_argument("input", help="Input file to validate")
    args = parser.parse_args()

    return validate(args.input)

if __name__ == "__main__":
    sys.exit(main())
```

## scripts/requirements.txt Template

```
# Add your dependencies here
# Example:
# requests>=2.31.0
# pydantic>=2.0.0
```

## .env.example Template

```bash
# Example environment variables
# Copy this file to .env and fill in actual values
# NEVER commit .env to version control

API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

## Use Cases

- Schema validation
- Code linting/formatting
- Complex calculations
- File processing
- External API calls
