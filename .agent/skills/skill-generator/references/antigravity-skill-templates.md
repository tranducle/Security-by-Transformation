# Antigravity Skill Templates

**Version:** 1.0.0
**Last Updated:** 2026-01-14
**Companion to:** [Antigravity Skill Creation Guide](./antigravity-skill-creation-guide.md)

---

## Overview

This document provides ready-to-use templates for each of the 5 skill complexity levels. Copy and customize these templates to create your own skills for Google Antigravity.

---

## Table of Contents

1. [Level 1: Instructions-Only Template](#level-1-instructions-only-template)
2. [Level 2: Asset Reference Template](#level-2-asset-reference-template)
3. [Level 3: Example-Guided Template](#level-3-example-guided-template)
4. [Level 4: Script-Integrated Template](#level-4-script-integrated-template)
5. [Level 5: Full-Featured Template](#level-5-full-featured-template)

---

## Level 1: Instructions-Only Template

**Use for:** Simple conventions, checklists, process definitions

### Directory Structure

```
skill-name/
└── SKILL.md
```

### SKILL.md Template

```markdown
---
name: skill-name
description: [Action verb] + [Target] + [Purpose]. Use when [specific scenario].
---

# Skill Title

One-line overview of what this skill does.

## When to Use

- Use this when [scenario 1]
- Use this when [scenario 2]
- Use this when [scenario 3]

## Overview

[Brief explanation of the problem this skill solves]

## Rules/Guidelines

1. **Rule 1:**
   - Detail 1
   - Detail 2

2. **Rule 2:**
   - Detail 1
   - Detail 2

3. **Rule 3:**
   - Detail 1
   - Detail 2

## Process/Steps

1. **Step 1:**
   - Action 1
   - Action 2

2. **Step 2:**
   - Action 1
   - Action 2

3. **Step 3:**
   - Action 1
   - Action 2

## Examples

### Example 1: [Basic Use Case]

```
[Input] → [Expected Output]
```

### Example 2: [Advanced Use Case]

```
[Input] → [Expected Output]
```

## Constraints

- Do NOT [constraint 1]
- Always [constraint 2]
- Never [constraint 3]

## Common Mistakes to Avoid

- Mistake 1: Description
- Mistake 2: Description
- Mistake 3: Description

## Checklist

Before completing task, verify:
- [ ] Check 1
- [ ] Check 2
- [ ] Check 3
```

### Real-World Example: Conventional Commits

```markdown
---
name: conventional-commits
description: Formats git commit messages according to Conventional Commits specification. Use when user asks to commit changes or write commit messages.
---

# Conventional Commits

Enforces Conventional Commits format for all git commit messages.

## When to Use

- User asks to commit changes
- User asks for commit message suggestions
- User is preparing a PR

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Allowed Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, whitespace)
- **refactor:** Code refactoring
- **perf:** Performance improvements
- **test:** Adding or updating tests
- **chore:** Build process, auxiliary tools
- **ci:** CI/CD changes
- **build:** Build system changes

## Instructions

1. **Analyze the change:**
   - What type of change is it?
   - What component/module is affected?
   - What is the core purpose?

2. **Write the subject line:**
   - Use imperative mood ("add" not "added")
   - Use lowercase for type
   - Keep under 72 characters
   - Don't end with period

3. **Add body (if needed):**
   - Explain WHAT and WHY
   - Not HOW
   - Wrap at 72 characters

4. **Add footer (if needed):**
   - Breaking changes: `BREAKING CHANGE: description`
   - Closes issues: `Closes #123`

## Examples

### Simple feat
```
feat(auth): add login with google
```

### Complex feat with body
```
feat(api): implement user search

- Add fuzzy search by name and email
- Support pagination
- Add rate limiting (100 req/min)

Closes #456
```

### Breaking change
```
feat(db): migrate to PostgreSQL

BREAKING CHANGE: SQLite is no longer supported.
All users must migrate to PostgreSQL.

Migration guide: docs/migration.md
```

### Bug fix
```
fix(api): handle null values in user profile

Fixes crash when profile_image_url is null.
```

## Constraints

- **NEVER** use vague descriptions like "update files" or "fix stuff"
- **ALWAYS** use imperative mood
- **NEVER** include issue numbers in subject line
- **ALWAYS** keep subject line under 72 characters

## Common Mistakes

❌ `fix: fixed bug`
✅ `fix(auth): resolve login timeout issue`

❌ `feat: added feature`
✅ `feat(ui): add dark mode toggle`

❌ `update Readme`
✅ `docs: update installation guide`
```

---

## Level 2: Asset Reference Template

**Use for:** Skills that reference external files (templates, configs, legal text)

### Directory Structure

```
skill-name/
├── SKILL.md
└── resources/
    ├── template.txt
    ├── config.json
    └── style-guide.md
```

### SKILL.md Template

```markdown
---
name: skill-name
description: [Action verb] + [Target] + [Purpose]. Use when [specific scenario].
---

# Skill Title

Overview of skill that uses external resource files.

## When to Use

- Use this when [scenario 1]
- Use this when [scenario 2]

## Resources

This skill uses the following resource files:

- `resources/template.txt` - [Description]
- `resources/config.json` - [Description]
- `resources/style-guide.md` - [Description]

## Instructions

1. **Read Resource:**
   Read the content from `resources/[filename]`

2. **Apply Resource:**
   [How to use the resource]

3. **Adapt if Necessary:**
   [When to modify based on context]

## Resource Files

### template.txt

[Purpose of this template]

**Usage:**
```
[How to use template]
```

### config.json

[Purpose of this config]

**Schema:**
```json
{
  "field1": "description",
  "field2": "description"
}
```

### style-guide.md

[Style guidelines reference]

## Examples

### Example 1: Basic Usage

Input: [User input]

Process:
1. Read `resources/template.txt`
2. Apply to input
3. Generate output

Output: [Expected result]

### Example 2: With Modifications

Input: [User input]

Process:
1. Read `resources/template.txt`
2. Modify based on context: [what to change]
3. Generate output

Output: [Expected result]

## Customization

You can customize resource files by editing:
- `resources/template.txt` - Change [what]
- `resources/config.json` - Change [what]
- `resources/style-guide.md` - Change [what]
```

### Resource File Templates

#### **template.txt**
```
[Static template content that should be used verbatim]

{{placeholder}} for dynamic content

[More static content]
```

#### **config.json**
```json
{
  "version": "1.0.0",
  "settings": {
    "option1": "value1",
    "option2": "value2"
  }
}
```

#### **style-guide.md**
```markdown
# Style Guide

## Rule 1
[Description]

## Rule 2
[Description]
```

### Real-World Example: License Header Adder

```
license-header-adder/
├── SKILL.md
└── resources/
    └── MIT_LICENSE.txt
```

**SKILL.md:**
```markdown
---
name: license-header-adder
description: Adds MIT license header to new source files. Use when creating new code files that require copyright attribution.
---

# License Header Adder

Automatically adds MIT license header to new source files.

## When to Use

- Creating new source files
- Adding files to open-source project
- User asks to "add license header"

## Resources

- `resources/MIT_LICENSE.txt` - MIT license template

## Instructions

1. **Read License Template:**
   Read content from `resources/MIT_LICENSE.txt`

2. **Prepend to File:**
   Add license header at the top of the new file

3. **Adapt Comment Syntax:**
   - Python/Shell/YAML: Use `#` for each line
   - Java/JS/TS/C++: Keep `/* ... */` block
   - HTML/XML: Use `<!-- ... -->`

## License Template

The MIT license template includes:
- Copyright notice
- Permission notice
- Warranty disclaimer

## Examples

### Python File

Input: Create `utils.py`

Output:
```python
# Copyright (c) 2024 Your Name
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction...

def utility_function():
    pass
```

### JavaScript File

Input: Create `app.js`

Output:
```javascript
/*
 * Copyright (c) 2024 Your Name
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction...
 */

function app() {
  // code
}
```

## Year

Use current year: 2024 (or 2026 when reading this)
```

**resources/MIT_LICENSE.txt:**
```
Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Level 3: Example-Guided Template

**Use for:** Few-shot learning patterns, style matching, format conversions

### Directory Structure

```
skill-name/
├── SKILL.md
└── examples/
    ├── example1-input.txt
    ├── example1-output.txt
    ├── example2-input.json
    └── example2-output.py
```

### SKILL.md Template

```markdown
---
name: skill-name
description: [Action verb] + [Target] + [Purpose]. Use when [specific scenario].
---

# Skill Title

Converts/transforms [input format] to [output format] following established patterns.

## When to Use

- Use this when [scenario 1]
- Use this when [scenario 2]

## Instructions

1. **Analyze Input:**
   Examine the [input format] provided by user

2. **Identify Pattern:**
   Match input structure to one of the examples in `examples/`

3. **Apply Transformation:**
   Follow the pattern from matching example:
   - [Transformation rule 1]
   - [Transformation rule 2]
   - [Transformation rule 3]

4. **Generate Output:**
   Produce [output format] following example style

## Examples

Review examples in `examples/` directory:

### Example 1: [Example name]

**Input:** `examples/example1-input.txt`
```
[Input content]
```

**Output:** `examples/example1-output.txt`
```
[Output content]
```

**Key transformations:**
- [Pattern 1 observed]
- [Pattern 2 observed]

### Example 2: [Example name]

**Input:** `examples/example2-input.json`
```json
[Input content]
```

**Output:** `examples/example2-output.py`
```python
[Output content]
```

**Key transformations:**
- [Pattern 1 observed]
- [Pattern 2 observed]

## Type Mappings

| Input Type | Output Type | Notes |
|------------|-------------|-------|
| type1 | Type1 | Notes |
| type2 | Type2 | Notes |
| type3 | Optional[Type3] | For nullable fields |

## Style Guidelines

- **Naming:** Use [PascalCase/camelCase/snake_case] for [entities]
- **Indentation:** Use [2/4] spaces/[tabs]
- **Line length:** Keep under [N] characters
- **Imports:** [Import organization rule]

## Common Patterns

### Pattern 1: [Pattern name]

When [condition], apply [transformation]

### Pattern 2: [Pattern name]

When [condition], apply [transformation]

### Pattern 3: [Pattern name]

When [condition], apply [transformation]
```

### Real-World Example: JSON to Pydantic

```
json-to-pydantic/
├── SKILL.md
└── examples/
    ├── user-input.json
    ├── user-output.py
    ├── product-input.json
    └── product-output.py
```

**SKILL.md:**
```markdown
---
name: json-to-pydantic
description: Converts JSON data snippets into Python Pydantic data models with proper type hints and Optional fields. Use when user provides JSON and wants Pydantic classes.
---

# JSON to Pydantic Converter

Converts raw JSON or API responses into structured Pydantic models.

## When to Use

- User provides JSON snippet
- User wants to create Pydantic models
- User asks to "convert this JSON to Pydantic"

## Instructions

1. **Analyze Input:**
   Examine JSON object structure

2. **Infer Types:**
   - `string` → `str`
   - `number` → `int` or `float`
   - `boolean` → `bool`
   - `array` → `List[Type]`
   - `null` → `Optional[Type]` with default `None`
   - Nested objects → Separate sub-classes

3. **Follow Example Pattern:**
   Review `examples/` to understand output structure

4. **Generate Pydantic Model:**
   Create Python class with proper type hints

## Examples

### Example 1: User Object

**Input:** `examples/user-input.json`
```json
{
    "user_id": 12345,
    "username": "jdoe_88",
    "is_active": true,
    "preferences": {
        "theme": "dark",
        "notifications": ["email", "push"]
    },
    "last_login": "2024-03-15T10:30:00Z",
    "meta_tags": null
}
```

**Output:** `examples/user-output.py`
```python
from pydantic import BaseModel
from typing import List, Optional

class Preferences(BaseModel):
    theme: str
    notifications: List[str]

class User(BaseModel):
    user_id: int
    username: str
    is_active: bool
    preferences: Preferences
    last_login: Optional[str] = None
    meta_tags: Optional[List[str]] = None
```

**Key patterns:**
- Nested object `preferences` → separate `Preferences` class
- Array `notifications` → `List[str]`
- Null field `meta_tags` → `Optional` with default `None`
- Required fields have no default

### Example 2: Product Object

**Input:** `examples/product-input.json`
```json
{
    "product": "Widget",
    "cost": 10.99,
    "stock": null,
    "tags": ["home", "garden"]
}
```

**Output:** `examples/product-output.py`
```python
from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    product: str
    cost: float
    stock: Optional[int] = None
    tags: List[str]
```

**Key patterns:**
- Decimal number → `float`
- Integer could be null → `Optional[int]`
- String array → `List[str]`

## Type Mapping Reference

| JSON Type | Python Type | Notes |
|-----------|-------------|-------|
| `string` | `str` | - |
| `number` (no decimal) | `int` | Use int for whole numbers |
| `number` (with decimal) | `float` | Use float for decimals |
| `boolean` | `bool` | - |
| `array` | `List[Type]` | Infer type from items |
| `null` | `Optional[Type]` | Add default `None` |
| `object` | Separate class | Create nested model |

## Style Guidelines

- **Class names:** PascalCase (`User`, `Preferences`)
- **Field names:** snake_case (`user_id`, `is_active`)
- **Imports:** Group in order: pydantic, typing
- **Optional fields:** Always provide default `None`
- **Required fields:** No default value

## Common Patterns

### Nested Objects

```python
# Input: {"address": {"street": "123 Main", "city": "NYC"}}

# Output:
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    address: Address  # Separate class for nested object
```

### Arrays

```python
# Input: {"tags": ["red", "blue", "green"]}

# Output:
class Item(BaseModel):
    tags: List[str]  # Array of primitive type
```

### Nullable Fields

```python
# Input: {"name": "John", "nickname": null}

# Output:
from typing import Optional

class User(BaseModel):
    name: str
    nickname: Optional[str] = None  # Always default None
```
```

---

## Level 4: Script-Integrated Template

**Use for:** Validation, complex logic, binary execution, deterministic checks

### Directory Structure

```
skill-name/
├── SKILL.md
├── scripts/
│   ├── main.py
│   ├── utils.py
│   └── requirements.txt
└── .env.example
```

### SKILL.md Template

```markdown
---
name: skill-name
description: [Action verb] + [Target] + [Purpose]. Use when [specific scenario].
---

# Skill Title

Performs [task] using automated scripts for deterministic results.

## When to Use

- Use this when [scenario 1]
- Use this when [scenario 2]

## Prerequisites

Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

## Instructions

**DO NOT attempt to [task] manually.** The rules are complex and require automated validation.

### Step 1: Run Validation/Processing

Execute the main script:

```bash
python scripts/main.py [input_file]
```

### Step 2: Interpret Output

**Exit code 0 (Success):**
- Script output: [success message]
- Tell user: [what to say on success]

**Exit code 1 (Failure):**
- Script output: [error message]
- Report errors to user
- Suggest fixes based on error message

### Step 3: Take Action

Based on script output:
- If success → [next action]
- If failure → [recovery action]

## Script Capabilities

The `main.py` script:

- **Validates:** [what it validates]
- **Checks:** [what it checks]
- **Enforces:** [what it enforces]
- **Returns:** [what it returns]

## Environment Variables

Optional environment variables (see `.env.example`):

- `VAR_NAME` - Description
- `VAR_NAME` - Description

## Examples

### Example 1: Valid Input

Input: `[valid input example]`

Command:
```bash
python scripts/main.py input.txt
```

Output:
```
[success message from script]
```

Response to user:
```
[tell user about success]
```

### Example 2: Invalid Input

Input: `[invalid input example]`

Command:
```bash
python scripts/main.py input.txt
```

Output:
```
[error message from script]
```

Response to user:
```
[tell user about error]
[suggested fix]
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| [Error 1] | [Cause] | [Solution] |
| [Error 2] | [Cause] | [Solution] |
| [Error 3] | [Cause] | [Solution] |

## Troubleshooting

**Script not found:**
- Ensure you're in skill directory
- Check scripts/ folder exists

**Module not found:**
- Run: `pip install -r scripts/requirements.txt`

**Permission denied:**
- Linux/Mac: `chmod +x scripts/main.py`
- Or use: `python scripts/main.py`
```

### Script Templates

#### **main.py**
```python
#!/usr/bin/env python3
"""
Main script for [skill-name].
Performs [task] with deterministic results.
"""

import sys
import logging
from pathlib import Path

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from utils import helper_function

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        logger.error("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Perform validation/processing
        result = process(input_file)

        if result.success:
            logger.info("Success: %s", result.message)
            sys.exit(0)
        else:
            logger.error("Error: %s", result.message)
            for error in result.errors:
                logger.error("  - %s", error)
            sys.exit(1)

    except FileNotFoundError:
        logger.error("File not found: %s", input_file)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        sys.exit(1)

def process(input_file):
    """Process input file and return result."""
    # Implementation here
    pass

if __name__ == "__main__":
    main()
```

#### **utils.py**
```python
"""Utility functions for [skill-name]."""

import re
from typing import List, Tuple

def helper_function(data: str) -> List[str]:
    """Helper function for processing."""
    # Implementation
    pass

def validate_format(data: str) -> Tuple[bool, List[str]]:
    """Validate format and return (is_valid, errors)."""
    errors = []

    # Validation logic here

    return len(errors) == 0, errors
```

#### **requirements.txt**
```
# Add your dependencies here
# Example:
# requests>=2.31.0
# pydantic>=2.0.0
```

#### **.env.example**
```
# Copy this file to .env and fill in values
# EXAMPLE_VAR=your_value_here
```

### Real-World Example: Schema Validator

```
sql-schema-validator/
├── SKILL.md
└── scripts/
    └── validate_schema.py
```

**SKILL.md:**
```markdown
---
name: sql-schema-validator
description: Validates SQL schema files for snake_case naming and primary key constraints. Use when checking database migrations or schema files.
---

# SQL Schema Validator

Validates SQL schemas against internal database standards.

## When to Use

- User creates schema file
- User asks to "validate this schema"
- User creates database migration

## Instructions

**DO NOT validate manually.** Run the automated validator script.

### Run Validation

```bash
python scripts/validate_schema.py <schema_file.sql>
```

### Interpret Results

**Exit code 0:**
- Output: "Schema validation passed."
- Tell user: Schema is compliant with standards

**Exit code 1:**
- Output: Error messages
- Report each error to user
- Suggest specific fix for each error

## Validation Rules

The script enforces:

1. **No DROP TABLE statements** (safety rule)
2. **Table names must be snake_case** (naming convention)
3. **Every table must have `id` column as PRIMARY KEY** (structure rule)

## Examples

### Valid Schema

Input file: `valid.sql`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);
```

Command:
```bash
python scripts/validate_schema.py valid.sql
```

Output:
```
Schema validation passed.
```

### Invalid Schema

Input file: `invalid.sql`
```sql
CREATE TABLE Users (
    Name TEXT
);
```

Command:
```bash
python scripts/validate_schema.py invalid.sql
```

Output:
```
ERROR: Table 'Users' must be snake_case.
ERROR: Table 'Users' is missing a primary key named 'id'.
```

Response to user:
```
Your schema has 2 errors:

1. Table 'Users' must be snake_case
   → Fix: Rename to 'users'

2. Table 'Users' missing primary key 'id'
   → Fix: Add 'id SERIAL PRIMARY KEY' as first column
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| Table name not snake_case | Uses uppercase or hyphens | Rename to lowercase with underscores |
| Missing primary key | No `id` column | Add `id SERIAL PRIMARY KEY` |
| DROP TABLE forbidden | Contains DROP statement | Remove DROP statement |
```

**scripts/validate_schema.py:**
```python
#!/usr/bin/env python3
"""SQL Schema Validator"""

import sys
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def validate_schema(filename):
    """
    Validates SQL schema file against internal policy:
    1. Table names must be snake_case
    2. Every table must have primary key named 'id'
    3. No 'DROP TABLE' statements
    """
    try:
        with open(filename, 'r') as f:
            content = f.read()

        errors = []

        # Check 1: No DROP TABLE
        if re.search(r'DROP TABLE', content, re.IGNORECASE):
            errors.append("ERROR: 'DROP TABLE' statements are forbidden.")

        # Check 2 & 3: CREATE TABLE checks
        table_defs = re.finditer(
            r'CREATE TABLE\s+(?P<name>\w+)\s*\((?P<body>.*?)\);',
            content,
            re.DOTALL | re.IGNORECASE
        )

        for match in table_defs:
            table_name = match.group('name')
            body = match.group('body')

            # Snake case check
            if not re.match(r'^[a-z][a-z0-9_]*$', table_name):
                errors.append(f"ERROR: Table '{table_name}' must be snake_case.")

            # Primary key check
            if not re.search(r'\bid\b.*PRIMARY KEY', body, re.IGNORECASE):
                errors.append(f"ERROR: Table '{table_name}' is missing a primary key named 'id'.")

        if errors:
            for err in errors:
                logger.error(err)
            return False

        logger.info("Schema validation passed.")
        return True

    except FileNotFoundError:
        logger.error("Error: File '%s' not found.", filename)
        return False

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python validate_schema.py <schema_file>")
        sys.exit(1)

    if validate_schema(sys.argv[1]):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Level 5: Full-Featured Template

**Use for:** Complex workflows, code scaffolding, enterprise automation

### Directory Structure

```
skill-name/
├── SKILL.md
├── scripts/
│   ├── scaffold.py
│   ├── generator.py
│   └── requirements.txt
├── resources/
│   ├── template.txt
│   └── config.json
├── examples/
│   └── reference-implementation.py
└── .env.example
```

### SKILL.md Template

```markdown
---
name: skill-name
description: [Action verb] + [Target] + [Purpose]. Use when [specific scenario].
---

# Skill Title

Comprehensive skill that combines scripts, templates, and examples for [complex task].

## When to Use

- Use this when [scenario 1]
- Use this when [scenario 2]

## Prerequisites

Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

Optional environment variables (see `.env.example`):
```bash
export VAR_NAME=value
```

## Workflow

### Step 1: Analyze Request

Extract from user request:
- [Parameter 1]
- [Parameter 2]
- [Parameter 3]

### Step 2: Review Example

Check `examples/reference-implementation.py` to understand:
- Expected structure
- Import patterns
- Code style
- Best practices

### Step 3: Generate Scaffold

Run scaffolding script:
```bash
python scripts/scaffold.py [parameter1] [parameter2]
```

This creates:
- `[output_file1]`
- `[output_file2]`

### Step 4: Customize

Edit generated files to:
1. [Customization 1]
2. [Customization 2]
3. [Customization 3]

### Step 5: Validate

Run validation:
```bash
python scripts/validate.py [output_file]
```

## Resources

### template.txt

[Description of template]

### config.json

Configuration schema:
```json
{
  "field1": "description",
  "field2": "description"
}
```

## Examples

### Example 1: Basic Usage

User request: "[example request]"

Process:
1. Extract: [param1=value1, param2=value2]
2. Run: `python scripts/scaffold.py value1 value2`
3. Edit generated file
4. Validate

Output: `[description of result]`

### Example 2: Advanced Usage

User request: "[complex request]"

Process:
1. Extract: [params]
2. Review example
3. Run scaffold with flags
4. Customize based on config
5. Validate

Output: `[description of result]`

## Script Reference

### scaffold.py

Generates initial code structure.

**Usage:**
```bash
python scripts/scaffold.py [options] <name>
```

**Options:**
- `--type=<type>` - Specify type
- `--config=<file>` - Use custom config

### generator.py

Generates code from templates.

**Usage:**
```bash
python scripts/generator.py <template> <output>
```

### validate.py

Validates generated code.

**Usage:**
```bash
python scripts/validate.py <file>
```

## Troubleshooting

**Scaffold fails:**
- Check parameters are valid
- Review example for correct format

**Generation fails:**
- Check template exists in resources/
- Validate template syntax

**Validation fails:**
- Review error messages
- Compare with example

## Customization

You can customize:

1. **Templates:** Edit `resources/template.txt`
2. **Config:** Edit `resources/config.json`
3. **Examples:** Add new examples to `examples/`
4. **Scripts:** Modify `scripts/` as needed
```

### Real-World Example: API Client Scaffold

```
api-client-scaffold/
├── SKILL.md
├── scripts/
│   ├── scaffold.py
│   └── requirements.txt
├── resources/
│   └── client_template.py
└── examples/
    └── github_client.py
```

---

**End of Templates**

For detailed explanations, see [Antigravity Skill Creation Guide](./antigravity-skill-creation-guide.md).
