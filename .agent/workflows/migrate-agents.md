---
description: Run the agent migration from YAML to new JSON format
---

# Agent Migration Workflow

Use this one-time utility to import archived YAML agent definitions into the current JSON schema.

## Steps

### 1. Run Full Migration

// turbo

```bash
python migrate_yaml_to_agents.py --yaml-dir AI_Agents_YAML --output-dir agents
```

### 2. Migrate Single Agent (Optional)

```bash
python migrate_yaml_to_agents.py --agent LiteratureHunter --output-dir agents
```

### 3. Verify Migration

Check the output:

- `agents/` directory should contain JSON files
- Each JSON file should have: name, role, goal, backstory, domain, tools

### 4. Test an Agent

```python
from pathlib import Path
import json

agent_file = Path("agents/LiteratureHunter.json")
agent = json.loads(agent_file.read_text())
print(f"Agent: {agent['name']}")
print(f"Domain: {agent['domain']}")
print(f"Tools: {[t['name'] for t in agent['tools']]}")
```

## Expected Outcome

- JSON files generated for the selected YAML source set
- Each agent has proper domain assignment
- Key agents have tools assigned
