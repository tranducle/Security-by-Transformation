
import yaml
import json
import os

def convert_master_orchestrator():
    yaml_path = "AI_Agents_YAML/MasterOrchestrator.yaml"
    json_path = "agents/MasterOrchestrator.json"
    
    # Read YAML
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Convert to JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Converted {yaml_path} to {json_path}")
    
    # Verify content
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        
    print(f"Original keys: {list(data.keys())}")
    print(f"New keys: {list(json_data.keys())}")
    
    if data == json_data:
        print("✅ Content verification passed: IDENTICAL")
    else:
        print("❌ Content verification FAILED")

if __name__ == "__main__":
    convert_master_orchestrator()
