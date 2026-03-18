# Level 5 Skill Template

## Directory Structure

```
your-skill/
├── SKILL.md
├── scripts/
│   ├── generator.py
│   ├── validator.py
│   └── requirements.txt
├── resources/
│   └── template.txt
├── examples/
│   └── reference-implementation.py
├── references/
│   └── additional-docs.md
└── tests/
    └── test_skill.py
```

## SKILL.md Template

```yaml
---
name: your-skill
description: Full-featured [purpose] combining code generation, validation, and templates. Use when user needs to create, validate, or scaffold [target] with proper structure and error handling.
---

# Skill Title

Comprehensive skill for complex multi-step workflows.

## Workflow

1. **Review Example:** Check `examples/reference-implementation.py` for pattern
2. **Generate:** Run `scripts/generator.py` to create initial scaffold
3. **Refine:** Edit generated file based on requirements
4. **Validate:** Run `scripts/validator.py` to verify correctness

## Prerequisites

Install dependencies:
```bash
pip install -r scripts/requirements.txt
```

## Quick Start

```bash
# Generate scaffold
python scripts/generator.py <Name>

# Validate output
python scripts/validator.py <output_file>
```

## Example

User: "Create a new [component type] for [purpose]"

Agent:
1. Reviews `examples/` for similar pattern
2. Runs generator script: `python scripts/generator.py MyComponent`
3. Reads generated file
4. Makes adjustments based on template
5. Validates: `python scripts/validator.py MyComponent.py`

## Constraints

- Always validate generated output
- Never skip the review step
- Follow the pattern in examples/

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Generation fails | Check templates/ for syntax errors |
| Validation fails | Review error messages, fix issues |
| Wrong pattern | Re-check examples/ folder |
```

## scripts/generator.py Template

```python
#!/usr/bin/env python3
"""
Code generator for scaffolding.
"""

import sys
import os
from pathlib import Path

def generate(name: str, output_dir: str = ".") -> str:
    """
    Generate scaffold code.

    Args:
        name: Component/class name
        output_dir: Output directory

    Returns:
        Path to generated file
    """
    template_dir = Path(__file__).parent.parent / "resources"
    template_file = template_dir / "template.txt"

    # Read template
    with open(template_file, 'r') as f:
        template = f.read()

    # Fill template
    content = template.replace("{{NAME}}", name)

    # Write output
    output_path = Path(output_dir) / f"{name}.py"
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"Generated: {output_path}")
    return str(output_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generator.py <Name> [output_dir]")
        sys.exit(1)

    name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    generate(name, output_dir)
```

## scripts/validator.py Template

```python
#!/usr/bin/env python3
"""
Validator for generated code.
"""

import sys
import ast
from pathlib import Path

def validate(file_path: str) -> int:
    """
    Validate generated file.

    Args:
        file_path: Path to file to validate

    Returns:
        0 for success, 1 for failure
    """
    path = Path(file_path)

    if not path.exists():
        print(f"ERROR: File '{file_path}' not found")
        return 1

    # Parse Python file
    try:
        with open(path, 'r') as f:
            code = f.read()
        ast.parse(code)
    except SyntaxError as e:
        print(f"ERROR: Syntax error at line {e.lineno}: {e.msg}")
        return 1

    # Custom validation
    errors = []

    # Add your validation rules here
    if "TODO" in code:
        errors.append("File contains TODO markers")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print(f"Validation passed: {file_path}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validator.py <file_path>")
        sys.exit(1)

    sys.exit(validate(sys.argv[1]))
```

## resources/template.txt Template

```python
"""
{{NAME}} - Description
"""

class {{NAME}}:
    """{{NAME}} class."""

    def __init__(self):
        """Initialize {{NAME}}."""
        # TODO: Implement initialization
        pass

    def execute(self):
        """Execute {{NAME}} logic."""
        # TODO: Implement execute method
        pass
```

## tests/test_skill.py Template

```python
#!/usr/bin/env python3
"""
Tests for skill functionality.
"""

import subprocess
import tempfile
from pathlib import Path

def test_generator():
    """Test code generation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = subprocess.run(
            ["python", "scripts/generator.py", "TestComponent", tmpdir],
            capture_output=True
        )
        assert result.returncode == 0
        assert Path(tmpdir, "TestComponent.py").exists()

def test_validator():
    """Test validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate test file
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("print('hello')")

        # Validate
        result = subprocess.run(
            ["python", "scripts/validator.py", str(test_file)],
            capture_output=True
        )
        assert result.returncode == 0

if __name__ == "__main__":
    test_generator()
    test_validator()
    print("All tests passed!")
```

## Use Cases

- Code scaffolding/frameworks
- Multi-step workflows
- Complex generators
- Enterprise integrations
- Full-featured tooling
