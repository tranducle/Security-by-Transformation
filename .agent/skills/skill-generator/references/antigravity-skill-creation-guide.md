# Antigravity Skill Creation Guide

**Version:** 1.0.0
**Last Updated:** 2026-01-14
**Platform:** Google Antigravity (Agent-First IDE)
**Standard:** Agent Skills Open Standard (by Anthropic, Dec 18, 2025)

---

## Table of Contents

1. [Understanding Agent Skills](#part-1-understanding-agent-skills)
2. [Antigravity-Specific Implementation](#part-2-antigravity-specific-implementation)
3. [Creating Skills - 5 Levels of Complexity](#part-3-creating-skills---5-levels-of-complexity)
4. [Best Practices](#part-4-best-practices)
5. [Practical Examples](#part-5-practical-examples)
6. [Troubleshooting](#part-6-troubleshooting)
7. [Appendix](#appendix)

---

## Part 1: Understanding Agent Skills

### What Are Agent Skills?

**Agent Skills** is an **open standard** for extending AI agent capabilities with specialized knowledge and workflows. Published by Anthropic on December 18, 2025, it represents a shift from monolithic context loading to **progressive disclosure**.

#### Core Principles

1. **Progressive Disclosure**: Skills are discovered by semantic matching and loaded only when relevant
2. **Lightweight**: File-based, serverless architecture requiring no persistent infrastructure
3. **Portable**: Same skill works across multiple platforms (Claude, GitHub Copilot, VS Code, Cursor, OpenCode, Antigravity)
4. **Composable**: Skills can include scripts, templates, examples, and resources

#### The Problem Skills Solve

**Context Saturation & Tool Bloat:**
- Modern models (Gemini 2.5/3) have 1M+ token context windows
- Loading entire codebases, docs, and toolsets creates latency and cost overhead
- Example: GitHub MCP (50 tools) + Playwright MCP (24 tools) + Chrome DevTools MCP (26 tools) = 100+ tools consuming 40-50K tokens for a task that might use only one

**The Skills Solution:**
- Agent sees lightweight "menu" of skill metadata (name + description)
- Loads full instructions only when semantically relevant
- Dramatically reduces context window usage
- Improves agent accuracy and performance

### The Open Standard

Agent Skills was officially published as an open standard by Anthropic on December 18, 2025. It follows the same philosophy as MCP (Model Context Protocol) - creating a universal, cross-platform standard for AI agent capabilities.

#### Supported Platforms

| Platform | Status | Skill Path |
|----------|--------|------------|
| **Google Antigravity** | ✅ Supported (Jan 14, 2026) | `.agent/skills/` or `~/.gemini/antigravity/skills/` |
| Claude.ai / Claude Code | ✅ Native | `.claude/skills/` |
| GitHub Copilot | ✅ Supported | `.github/skills/` |
| VS Code | ✅ Supported | `.github/skills/` |
| Cursor | ✅ Supported | `.cursor/skills/` |
| OpenCode | ✅ Supported | `.opencode/skill/` |
| Gemini CLI | ✅ Supported | `~/.gemini/skills/` |

### Progressive Disclosure Pattern

The "progressive disclosure" pattern is the core innovation of Agent Skills:

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION START                                              │
│  ────────────                                              │
│  Agent loads:                                               │
│  • All skill names + descriptions (metadata only)          │
│  • NOT full SKILL.md files (too heavy)                     │
│                                                             │
│  Token usage: ~100-500 tokens                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  USER REQUEST: "Review my authentication code"             │
│  ────────────────────────────────────────────────────────  │
│  Agent performs semantic matching:                          │
│  • Compares request against all skill descriptions          │
│  • Identifies "code-review" and "auth-audit" as relevant    │
│                                                             │
│  Processing: Agent reasoning engine                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  SKILL ACTIVATION                                           │
│  ────────────────                                           │
│  Agent loads:                                               │
│  • Full SKILL.md for relevant skills only                   │
│  • Optional scripts, examples, references                   │
│                                                             │
│  Token usage: ~1-3K tokens (only what's needed)             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  EXECUTION                                                  │
│  ─────────                                                 │
│  Agent follows skill instructions precisely:                │
│  • Uses specified tools and scripts                         │
│  • Follows defined workflows                                │
│  • Produces formatted output                                │
└─────────────────────────────────────────────────────────────┘
```

### Skills vs MCP vs Rules vs Workflows

Understanding the distinction is critical for proper system design in Antigravity:

#### **Skills** (`.agent/skills/`)
- **Nature:** Agent-triggered, on-demand capabilities
- **Activation:** Semantic matching by agent
- **Scope:** Specific tools or capabilities not always needed
- **Use for:** Domain-specific knowledge, specialized workflows
- **Example:** Database query skill, API integration skill

#### **Model Context Protocol (MCP)**
- **Nature:** Client-server architecture for external system connections
- **Activation:** Persistent connection, always available tools
- **Scope:** Stateful connections to databases, APIs, services
- **Use for:** PostgreSQL, GitHub, Slack, file systems
- **Relationship:** Skills USE MCP tools as building blocks

```
MCP Tools = The Hands (deterministic functions: read_file, execute_query)
Skills = The Brains (methodology: how/when to use those tools)
```

#### **Rules** (`.agent/rules/`)
- **Nature:** Passive constraints, always "on"
- **Activation:** Automatically injected into system prompt
- **Scope:** Behaviors that must ALWAYS be followed
- **Use for:** "Always use TypeScript strict mode", "Never commit secrets"
- **Relationship:** Rules can mandate use of specific Skills

#### **Workflows** (`.agent/workflows/`)
- **Nature:** User-triggered, manual orchestration
- **Activation:** Explicit user invocation (`/test`, `/review`)
- **Scope:** Multi-step processes the user triggers
- **Use for:** Saved prompts, complex automation sequences
- **Relationship:** Workflows can invoke Skills as steps

### Composability Example

A common pattern combining all four:

```
┌────────────────────────────────────────────────────────────┐
│  RULE: "Always use safe-db-migration skill for DB changes"  │
│    ─────────────────────────────────────────────────────   │
│  ↓                                                          │
│  USER: "Migrate the user schema"                           │
│  ─────────────────────────────                              │
│  ↓                                                          │
│  AGENT: (Reasoning) → Activates safe-db-migration SKILL     │
│    ──────────────────────────────────────────────────      │
│  ↓                                                          │
│  SKILL: "Use postgres MCP tool to run migration script"     │
│    ─────────────────────────────────────────────────       │
│  ↓                                                          │
│  MCP: postgres.execute_migration(migration.sql)             │
│    ────────────────────────────────────────────────        │
└────────────────────────────────────────────────────────────┘
```

---

## Part 2: Antigravity-Specific Implementation

### Directory Structure

Antigravity supports two scopes for skills:

#### **Workspace Scope** (Project-Specific)
```
<workspace-root>/.agent/skills/<skill-folder>/
```

**Use cases:**
- Team-specific workflows (deployment, testing)
- Project-specific conventions (code style, patterns)
- Proprietary framework integrations
- Database schemas and migrations

**Example:**
```
my-app/.agent/skills/
├── deploy-to-staging/
│   └── SKILL.md
├── company-auth-style/
│   └── SKILL.md
└── custom-framework-generator/
    ├── SKILL.md
    └── scripts/
        └── scaffold.py
```

#### **Global Scope** (User-Specific)
```
~/.gemini/antigravity/skills/<skill-folder>/
```

**Use cases:**
- Personal productivity tools
- General utilities (JSON formatting, UUID generation)
- Personal coding preferences
- Cross-project standards

**Example:**
```
~/.gemini/antigravity/skills/
├── json-formatter/
├── conventional-commits/
├── my-code-style/
└── personal-templates/
```

### Skill Priority

When both workspace and global skills exist with the same name:
1. **Workspace skill takes priority**
2. **Description quality matters most** - precise descriptions win over vague ones
3. **Agent decides based on semantic relevance**, not just location

### SKILL.md Format

The `SKILL.md` file is the **only required file** in a skill. It consists of two parts:

#### **Part 1: YAML Frontmatter**

```yaml
---
name: skill-identifier          # Optional, defaults to directory name
description: Clear description  # REQUIRED - The most important field
version: 1.0.0                 # Optional
license: MIT                    # Optional
author: "Your Name"             # Optional
tags: ["category", "keywords"]  # Optional
---
```

**Critical Points:**
- `description` is **THE ONLY FIELD** indexed for semantic matching
- Vague descriptions like "Database tools" are insufficient
- Precise descriptions like "Executes read-only SQL queries against local PostgreSQL to debug data states" ensure correct activation

#### **Part 2: Markdown Body**

```markdown
# Skill Title

Brief overview of what this skill does.

## When to Use

- Use this when...
- Another scenario...

## Instructions

Step-by-step guidance for the agent.

### Sub-section

More detailed instructions.

## Examples

### Example 1: Basic Usage

Input → Expected output

### Example 2: Advanced Usage

Complex scenario walkthrough

## Constraints

- Do NOT do X
- Always validate Y
- Never output Z

## Troubleshooting

Common issues and solutions.
```

### File Organization Patterns

#### **Level 1: Minimal Skill**
```
skill-name/
└── SKILL.md
```

Use for: Simple instruction sets, conventions, guidelines

#### **Level 2: Asset Reference**
```
skill-name/
├── SKILL.md
└── resources/
    ├── template.txt
    └── config.json
```

Use for: Skills that reference static files (templates, configs)

#### **Level 3: Example-Guided**
```
skill-name/
├── SKILL.md
└── examples/
    ├── input.json
    └── output.py
```

Use for: Few-shot learning patterns

#### **Level 4: Script-Integrated**
```
skill-name/
├── SKILL.md
├── scripts/
│   ├── main.py
│   ├── utils.py
│   └── requirements.txt
└── .env.example
```

Use for: Skills that execute code

#### **Level 5: Full-Featured**
```
skill-name/
├── SKILL.md
├── scripts/
│   ├── generator.py
│   └── validator.py
├── resources/
│   └── template.hbs
├── examples/
│   └── reference-implementation.py
├── references/
│   ├── topic1.md
│   └── topic2.md
├── tests/
│   └── test_skill.py
└── .env.example
```

Use for: Complex, multi-step workflows

### Naming Conventions

#### **Directory Names:**
- Use **kebab-case**: `my-skill`, `database-migration`, `json-to-pydantic`
- Be descriptive: `git-commit-formatter` (not `gcf` or `commits`)
- Avoid numbers: `auth-audit` (not `auth2`)

#### **Skill Names in YAML:**
- Must match directory name (if provided)
- Lowercase, hyphens allowed
- Examples: `postgres-query`, `pr-reviewer`, `license-header-adder`

#### **Descriptions:**
- Start with action verbs: "Generates...", "Validates...", "Converts..."
- Include context: "...for Python code using pytest"
- Be specific: NOT "Database tools" BUT "Executes read-only PostgreSQL queries for debugging"

---

## Part 3: Creating Skills - 5 Levels of Complexity

Based on the official Google Cloud tutorial, here are the 5 levels of skill complexity:

### Level 1: Instructions-Only Skills

**The "Hello World" of Skills**

Simplest possible skill - contains only a `SKILL.md` with instructions. No scripts, no resources.

#### **When to Use:**
- Enforcing conventions (commit messages, code style)
- Providing checklists (code review, testing)
- Defining processes (deployment steps)

#### **Example: Git Commit Formatter**

**Directory:**
```
git-commit-formatter/
└── SKILL.md
```

**SKILL.md:**
```markdown
---
name: git-commit-formatter
description: Formats git commit messages according to Conventional Commits specification. Use when user asks to commit changes or write commit messages.
---

# Git Commit Formatter

When writing git commit messages, you MUST follow Conventional Commits specification.

## Format

```
<type>[optional scope]: <description>
```

## Allowed Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only
- **style**: Style changes (formatting, whitespace)
- **refactor**: Code change (neither bug nor feature)
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Build process or auxiliary tools

## Instructions

1. Analyze changes to determine primary `type`
2. Identify `scope` if applicable (component, file)
3. Write concise `description` in imperative mood
4. Add `BREAKING CHANGE:` footer if applicable

## Example

```
feat(auth): implement login with google

- Add OAuth2 flow
- Integrate with Google Identity Services
- Update user schema to store google_id
```
```

**How it works:**
1. User: "Commit these changes"
2. Agent sees `git-commit-formatter` description
3. Agent loads full SKILL.md
4. Agent follows Conventional Commits format
5. Result: `feat(api): add user authentication endpoint`

---

### Level 2: Asset Reference Skills

**The "Template" Pattern**

Skills that reference external files for static content (templates, configurations, legal text).

#### **When to Use:**
- License headers (legal text must be exact)
- Code templates (boilerplate)
- Configuration files
- Standardized text blocks

#### **Example: License Header Adder**

**Directory:**
```
license-header-adder/
├── SKILL.md
└── resources/
    └── HEADER_TEMPLATE.txt
```

**SKILL.md:**
```markdown
---
name: license-header-adder
description: Adds standard open-source license header to new source files. Use when creating new code files requiring copyright attribution.
---

# License Header Adder

This skill ensures all new source files have correct copyright header.

## Instructions

1. **Read the Template:**
   Read content from `resources/HEADER_TEMPLATE.txt`

2. **Prepend to File:**
   When creating new file (`.py`, `.java`, `.js`, `.ts`, `.go`), prepend target file content with template content

3. **Modify Comment Syntax:**
   - C-style languages (Java, JS, TS, C++): Keep `/* ... */`
   - Python, Shell, YAML: Convert to `#` comments
   - HTML/XML: Use `<!-- ... -->`

## Example Usage

User: "Create a python script for hello world"

You should generate:
```python
# Copyright (c) 2024 Google LLC
# SPDX-License-Identifier: Apache-2.0
# ... (rest of license text) ...

def main():
    print("Hello World")
```
```

**resources/HEADER_TEMPLATE.txt:**
```
Copyright (c) 2024 Google LLC
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

**Why this pattern:**
- Legal text must be VERBATIM (no LLM hallucinations)
- Keeps SKILL.md concise
- Easy to update template without touching instructions

---

### Level 3: Example-Guided Skills

**The "Few-Shot" Pattern**

LLMs are pattern-matching engines. Showing examples (Input → Output) is more effective than verbose instructions.

#### **When to Use:**
- Code generation with specific patterns
- Data transformation (JSON → Pydantic)
- Format conversions
- Style matching

#### **Example: JSON to Pydantic Converter**

**Directory:**
```
json-to-pydantic/
├── SKILL.md
└── examples/
    ├── input_data.json
    └── output_model.py
```

**SKILL.md:**
```markdown
---
name: json-to-pydantic
description: Converts JSON data snippets into Python Pydantic data models with proper type hints and Optional fields.
---

# JSON to Pydantic Converter

This skill converts raw JSON or API responses into structured Pydantic models.

## Instructions

1. **Analyze Input:**
   Examine JSON object provided by user

2. **Infer Types:**
   - `string` → `str`
   - `number` → `int` or `float`
   - `boolean` → `bool`
   - `array` → `List[Type]`
   - `null` → `Optional[Type]`
   - Nested objects → Separate sub-class

3. **Follow Example:**
   Review `examples/` to understand structure

   - Input: `examples/input_data.json`
   - Output: `examples/output_model.py`

## Style Guidelines

- Use `PascalCase` for class names
- Use type hints from `typing` module
- Default `Optional` fields to `None`
```

**examples/input_data.json:**
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

**examples/output_model.py:**
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

**Why this pattern:**
- LLMs learn by imitation
- Examples show exact expected output format
- Handles nested structures correctly
- Establishes coding style

---

### Level 4: Script-Integrated Skills

**The "Tool Use" Pattern**

Delegate complex or deterministic logic to scripts. Provides binary truth (True/False) that LLMs can't guarantee.

#### **When to Use:**
- Validation (complex rules, binary checks)
- Binary execution (compilers, formatters)
- Complex calculations
- Legacy system interactions

#### **Example: Database Schema Validator**

**Directory:**
```
database-schema-validator/
├── SKILL.md
└── scripts/
    └── validate_schema.py
```

**SKILL.md:**
```markdown
---
name: database-schema-validator
description: Validates SQL schema files for compliance with internal safety and naming policies. Use when checking database migrations or schema files.
---

# Database Schema Validator

This skill ensures SQL files comply with strict database standards.

## Policies Enforced

1. **Safety:** No `DROP TABLE` statements
2. **Naming:** All tables must use `snake_case`
3. **Structure:** Every table must have `id` column as PRIMARY KEY

## Instructions

1. **Do NOT read manually** - rules are complex and easily missed

2. **Run Validation Script:**
   Execute python script from `scripts/` folder:

   ```bash
   python scripts/validate_schema.py <path_to_user_file>
   ```

3. **Interpret Output:**
   - Exit code 0: Tell user schema looks good
   - Exit code 1: Report specific error messages from script
```

**scripts/validate_schema.py:**
```python
import sys
import re

def validate_schema(filename):
    """
    Validates SQL schema against internal policy:
    1. Table names must be snake_case
    2. Every table must have primary key named 'id'
    3. No 'DROP TABLE' statements
    """
    try:
        with open(filename, 'r') as f:
            content = f.read()

        lines = content.split('\n')
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
                errors.append(f"ERROR: Table '{table_name}' missing primary key 'id'.")

        if errors:
            for err in errors:
                print(err)
            sys.exit(1)
        else:
            print("Schema validation passed.")
            sys.exit(0)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_schema.py <schema_file>")
        sys.exit(1)

    validate_schema(sys.argv[1])
```

**Why this pattern:**
- Deterministic validation (script doesn't "guess")
- Complex rules enforced consistently
- Clear error messages
- Agent becomes "reporter" not "validator"

---

### Level 5: Full-Featured Skills

**The "Architect" Pattern**

Combines all previous patterns: Scripts, Templates, Examples, Multi-step workflows.

#### **When to Use:**
- Code scaffolding (generating full files)
- Complex multi-step processes
- Framework-specific generators
- Enterprise workflows

#### **Example: ADK Tool Scaffold Generator**

**Directory:**
```
adk-tool-scaffold/
├── SKILL.md
├── resources/
│   └── ToolTemplate.py.hbs
├── scripts/
│   └── scaffold_tool.py
└── examples/
    └── WeatherTool.py
```

**SKILL.md:**
```markdown
---
name: adk-tool-scaffold
description: Scaffolds new custom Tool classes for Agent Development Kit (ADK). Use when creating new ADK tools with proper structure.
---

# ADK Tool Scaffold

This skill automates creation of standard `BaseTool` implementations for ADK.

## Instructions

1. **Identify Tool Name:**
   Extract tool name from user request (e.g., "StockPrice", "EmailSender")

2. **Review Example:**
   Check `examples/WeatherTool.py` to understand ADK structure (imports, inheritance, schema)

3. **Run Scaffolder:**
   Execute python script to generate initial file:

   ```bash
   python scripts/scaffold_tool.py <ToolName>
   ```

4. **Refine:**
   After generation, edit file to:
   - Update `execute` method with real logic
   - Define JSON schema in `get_schema`

## Example Usage

User: "Create a tool to search Wikipedia"

Agent:
1. Runs `python scripts/scaffold_tool.py WikipediaSearch`
2. Reads generated file
3. Sees `# TODO: Implement logic`
4. Checks `examples/WeatherTool.py` for schema pattern
5. Edits file to add `requests` logic and `query` argument
```

**scripts/scaffold_tool.py:**
```python
import sys
import os

def scaffold_tool(tool_name):
    """Generate basic ADK tool structure"""

    class_name = f"{tool_name}Tool"
    filename = f"{class_name}.py"

    template = f'''from typing import Dict, Any
from adk import BaseTool

class {class_name}(BaseTool):
    """TODO: Add description"""

    def get_schema(self) -> Dict[str, Any]:
        """TODO: Define input schema"""
        return {{
            "type": "object",
            "properties": {{
                # TODO: Add properties
            }},
            "required": []
        }}

    def execute(self, inputs: Dict[str, Any]) -> str:
        """TODO: Implement tool logic"""
        # TODO: Implement
        return "Not implemented"
'''

    with open(filename, 'w') as f:
        f.write(template)

    print(f"Created {filename}")
    return filename

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scaffold_tool.py <ToolName>")
        sys.exit(1)

    scaffold_tool(sys.argv[1])
```

**resources/ToolTemplate.py.hbs:**
```python
# Advanced Jinja2 template for more complex scaffolding
from typing import Dict, Any
from adk import BaseTool

class {{ClassName}}(BaseTool):
    """{{Description}}"""

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                {{#each Properties}}
                "{{this}}": {"type": "string"}{{#unless @last}},{{/unless}}
                {{/each}}
            },
            "required": []
        }

    def execute(self, inputs: Dict[str, Any]) -> str:
        # TODO: Implement
        return "Result"
```

**examples/WeatherTool.py:**
```python
from typing import Dict, Any
from adk import BaseTool

class WeatherTool(BaseTool):
    """Fetches current weather for a location"""

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or zip code"
                }
            },
            "required": ["location"]
        }

    def execute(self, inputs: Dict[str, Any]) -> str:
        location = inputs.get("location")
        # Call weather API
        return f"Weather in {location}: 72°F, Sunny"
```

**Why this pattern:**
- Combines all best practices
- Script handles file creation
- Template provides boilerplate
- Example guides implementation
- Agent orchestrates the workflow

---

## Part 4: Best Practices

### Description Writing

**The description is THE MOST IMPORTANT part of your skill.** It's the only field used for semantic matching.

#### **DO:**
```yaml
description: Executes read-only SQL queries against local PostgreSQL database to retrieve user or transaction data. Use for debugging data states.
```

**Why it works:**
- Specific action: "Executes read-only SQL queries"
- Clear target: "local PostgreSQL database"
- Use case: "debugging data states"

#### **DON'T:**
```yaml
description: Database tools
```

**Why it fails:**
- Too vague - agent can't determine relevance
- No action verb
- No use case context

#### **Description Formula:**

```
<Action verb(s)> + <Target> + <Purpose/Use case>
```

**Examples:**
- "Generates unit tests for Python code using pytest conventions"
- "Validates SQL schemas for snake_case naming and primary key constraints"
- "Converts JSON snippets into Pydantic models with proper type hints"
- "Formats git commit messages according to Conventional Commits specification"

### Script Integration

#### **Best Practices:**

1. **Keep Scripts Atomic:**
   ```python
   # Good: One clear purpose
   def validate_schema(file_path):
       # Validates schema
       pass

   # Bad: Multiple responsibilities
   def do_everything(file_path):
       # Validates
       # Transforms
       # Uploads
       # Emails
       pass
   ```

2. **Use Exit Codes:**
   ```python
   # 0 = Success
   # 1 = Failure (with error message)
   sys.exit(0)  # or 1
   ```

3. **Provide Clear Output:**
   ```python
   if errors:
       for err in errors:
           print(err)  # Agent will read this
       sys.exit(1)
   ```

4. **Language Choice:**
   - Python: Most common, rich libraries
   - Bash: For simple shell operations
   - Node: For JavaScript/TypeScript projects
   - Go/Rust: For performance-critical tasks

5. **Requirements Management:**
   ```
   scripts/
   ├── main.py
   └── requirements.txt  # Always include this
   ```

### Error Handling

#### **In Scripts:**
```python
import sys
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Do work
        result = process()
        print(result)
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

#### **In SKILL.md:**
```markdown
## Error Handling

If script returns exit code 1:
1. Read error message from stdout
2. Report to user with suggested fix
3. Do NOT retry automatically

Common errors:
- "File not found" → Check file path
- "Permission denied" → Check file permissions
- "Invalid format" → Validate input format
```

### Testing Skills

#### **Manual Testing:**

1. **Create test file:**
   ```
   test-skill/
   └── SKILL.md
   ```

2. **Test in Antigravity:**
   - Open chat
   - Type request that should trigger skill
   - Verify skill activates (check agent response)
   - Verify output matches expectations

3. **Test edge cases:**
   - Empty input
   - Invalid input
   - Large files
   - Special characters

#### **Automated Testing:**

```python
# tests/test_skill.py
import subprocess
import os

def test_schema_validator():
    # Test valid schema
    result = subprocess.run(
        ['python', 'scripts/validate_schema.py', 'tests/fixtures/valid.sql'],
        capture_output=True
    )
    assert result.returncode == 0

    # Test invalid schema
    result = subprocess.run(
        ['python', 'scripts/validate_schema.py', 'tests/fixtures/invalid.sql'],
        capture_output=True
    )
    assert result.returncode == 1
    assert b'must be snake_case' in result.stdout
```

### Documentation Standards

#### **SKILL.md Structure:**

```markdown
---
name: skill-name
description: Clear, specific description
---

# Skill Title

One-line overview.

## When to Use

- Scenario 1
- Scenario 2

## Prerequisites

- Requirement 1
- Requirement 2

## Instructions

Step-by-step guide...

### Sub-section

More details...

## Examples

### Example 1: Basic

```
Input → Output
```

### Example 2: Advanced

```
Complex scenario
```

## Constraints

- Do NOT X
- Always Y
- Never Z

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| Error message | What happened | How to fix |
```

#### **Code Documentation:**

```python
def process_data(data: dict) -> str:
    """
    Process input data and return formatted result.

    Args:
        data: Input dictionary with 'name' and 'value' keys

    Returns:
        Formatted string result

    Raises:
        ValueError: If 'name' or 'value' missing

    Example:
        >>> process_data({"name": "test", "value": 123})
        "test: 123"
    """
    # Implementation
    pass
```

---

## Part 5: Practical Examples

### Real-World Use Cases

#### **1. Code Review Skill**

```
.code-review/
└── SKILL.md
```

```markdown
---
name: code-review
description: Reviews code changes for bugs, style issues, and best practices. Use when reviewing PRs, checking code quality, or auditing implementation.
---

# Code Review

Review code systematically using this checklist.

## Review Checklist

1. **Correctness:**
   - Does code implement requirements?
   - Are edge cases handled?

2. **Style:**
   - Follows project conventions?
   - Consistent formatting?

3. **Performance:**
   - Any obvious inefficiencies?
   - Proper data structures?

4. **Security:**
   - Input validation?
   - No hardcoded secrets?

5. **Testing:**
   - Tests cover functionality?
   - Edge cases tested?

## Feedback Format

```markdown
## Issues Found

### [Severity] Issue Title
- **File:** `path/to/file.py:42`
- **Problem:** Description
- **Suggestion:** Fix recommendation

## Positive Notes
- Well-structured X
- Good use of Y
```
```

#### **2. Database Migration Skill**

```
.database-migration/
├── SKILL.md
├── scripts/
│   ├── generate_migration.py
│   └── apply_migration.py
└── resources/
    └── migration_template.sql
```

```markdown
---
name: database-migration
description: Generates and applies safe database migrations for PostgreSQL. Use when making schema changes or adding new tables.
---

# Database Migration

Safe database migration workflow.

## Process

1. **Generate Migration:**
   ```bash
   python scripts/generate_migration.py <migration_name>
   ```

2. **Review Generated SQL:**
   Check `resources/migration_template.sql`

3. **Test on Staging:**
   ```bash
   python scripts/apply_migration.py --env=staging
   ```

4. **Apply to Production:**
   ```bash
   python scripts/apply_migration.py --env=production
   ```

## Safety Rules

- ALWAYS review generated SQL before applying
- Test on staging first
- Never skip backup step
- Rollback plan must exist
```

#### **3. API Integration Skill**

```
.api-integration/
├── SKILL.md
├── scripts/
│   ├── call_api.py
│   └── format_response.py
└── examples/
    ├── github_api.md
    └── slack_api.md
```

```markdown
---
name: api-integration
description: Integrates with external APIs (GitHub, Slack, etc.) by handling authentication and response formatting. Use when making API calls.
---

# API Integration

Structured API call workflow.

## Supported APIs

- GitHub REST API
- Slack Web API
- Custom REST APIs

## Instructions

1. **Identify API** from user request
2. **Check examples/** for similar integration
3. **Make API call:**
   ```bash
   python scripts/call_api.py --api=<github|slack|custom> --endpoint=<path>
   ```
4. **Format response:**
   ```bash
   python scripts/format_response.py --format=<json|markdown|table>
   ```

## Authentication

API keys loaded from environment:
- `GITHUB_TOKEN`
- `SLACK_TOKEN`
- `CUSTOM_API_KEY`

Never hardcode credentials in SKILL.md or scripts!
```

### Common Patterns

#### **Pattern 1: Sequential Operations**

```markdown
## Instructions

1. Step 1
2. Step 2
3. Step 3

Each step MUST complete successfully before proceeding.
```

#### **Pattern 2: Conditional Logic**

```markdown
## Decision Tree

IF input is JSON:
  → Use json-to-pydantic skill
ELSE IF input is XML:
  → Use xml-parser skill
ELSE:
  → Ask user to specify format
```

#### **Pattern 3: Validation → Processing**

```markdown
## Workflow

1. **Validate Input:**
   Run: `python scripts/validate.py <input>`

2. If validation passes:
   Run: `python scripts/process.py <input>`

3. If validation fails:
   Report errors and suggest fixes
```

---

## Part 6: Troubleshooting

### Common Issues

#### **Issue 1: Skill Not Activating**

**Symptoms:**
- Agent doesn't use your skill
- Uses generic approach instead

**Causes:**
1. Description too vague
2. Description doesn't match user language
3. Competing skill with better description

**Solutions:**
```yaml
# Bad
description: Database tools

# Good
description: Executes read-only PostgreSQL queries to debug data states

# Better
description: Executes read-only SQL queries against local PostgreSQL database. Use when user asks to query database, check table schemas, or inspect user data.
```

#### **Issue 2: Script Permission Denied**

**Symptoms:**
```
Error: Permission denied: 'scripts/myscript.py'
```

**Solutions:**
```bash
# Linux/Mac
chmod +x scripts/myscript.py

# Or call with python explicitly
python scripts/myscript.py
```

#### **Issue 3: Module Not Found**

**Symptoms:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solutions:**
```bash
# Install from requirements.txt
pip install -r scripts/requirements.txt

# Or in SKILL.md add:
## Prerequisites
Install dependencies: `pip install -r scripts/requirements.txt`
```

#### **Issue 4: Path Issues**

**Symptoms:**
```
FileNotFoundError: resources/template.txt
```

**Solutions:**
```python
# In scripts, use relative paths from script location
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(script_dir, '..', 'resources', 'template.txt')

with open(template_path, 'r') as f:
    content = f.read()
```

### Debugging Techniques

#### **1. Add Verbose Output:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug("Processing file: %s", file_path)
```

#### **2. Dry-Run Mode:**

```bash
python scripts/myscript.py --dry-run --input=test.json
```

```python
if args.dry_run:
    print("Would process:", input_data)
    sys.exit(0)
```

#### **3. Validation Mode:**

```markdown
## Instructions

To validate without executing:
```bash
python scripts/process.py --validate-only
```
```

### Performance Optimization

#### **1. Lazy Loading:**

```markdown
## Instructions

1. Do NOT load all reference files upfront
2. Load only the specific file needed for current task
3. Use `Read` tool to load on-demand
```

#### **2. Caching:**

```python
import json
from pathlib import Path

_cache = {}

def load_cached_config():
    if 'config' not in _cache:
        config_path = Path(__file__).parent / 'resources' / 'config.json'
        _cache['config'] = json.loads(config_path.read_text())
    return _cache['config']
```

#### **3. Streaming for Large Files:**

```python
import json

def process_large_json(file_path):
    with open(file_path, 'r') as f:
        # Process item by item
        for line in f:
            item = json.loads(line)
            yield process_item(item)
```

---

## Appendix

### Quick Reference

#### **Skill Structure:**
```
skill-name/
├── SKILL.md              # Required
├── scripts/              # Optional
├── resources/            # Optional
├── examples/             # Optional
└── tests/                # Optional
```

#### **SKILL.md Template:**
```markdown
---
name: skill-name
description: Action + Target + Purpose
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

#### **Antigravity Paths:**
- Workspace: `.agent/skills/`
- Global: `~/.gemini/antigravity/skills/`

### Template Checklist

When creating a new skill, check:

- [ ] Directory name is kebab-case
- [ ] SKILL.md exists with YAML frontmatter
- [ ] Description follows: Action + Target + Purpose
- [ ] Instructions are clear and step-by-step
- [ ] Examples provided (if applicable)
- [ ] Scripts have error handling
- [ ] requirements.txt included (if using Python)
- [ ] .env.example provided (if using env vars)
- [ ] Tests included (for complex skills)

### Migration Guide

#### **From Claude Code:**

**Claude Code paths:**
```
.claude/skills/
```

**Antigravity paths:**
```
.agent/skills/           # Workspace
~/.gemini/antigravity/skills/  # Global
```

**Changes needed:**
1. Move skills from `.claude/skills/` to `.agent/skills/`
2. SKILL.md format is compatible (no changes needed)
3. Scripts should work as-is
4. Test in Antigravity to verify

#### **From OpenCode:**

**OpenCode paths:**
```
.opencode/skill/
```

**Antigravity paths:**
```
.agent/skills/
```

**Changes needed:**
1. Move skills from `.opencode/skill/` to `.agent/skills/`
2. SKILL.md format is compatible
3. Scripts compatible
4. Test in Antigravity

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-14 | Initial release based on Antigravity documentation |

### Additional Resources

- [Google Antigravity Official Docs](https://antigravity.google/docs/skills)
- [Agent Skills Open Standard](https://www.anthropic.com/)
- [Google Cloud Skills Tutorial](https://medium.com/google-cloud/tutorial-getting-started-with-antigravity-skills-864041811e0d)
- [Community Examples](https://github.com/rominirani/antigravity-skills)

---

**End of Guide**

For questions or issues, refer to the [Antigravity Documentation](https://antigravity.google/docs/skills) or community forums.
