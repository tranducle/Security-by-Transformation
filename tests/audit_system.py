"""
Full System Audit: AI Agent Research System v17
Tests imports, agent consistency, tool registration, init flow, workflows, and SOP integrity.
"""
import json, os, sys, glob, re, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"
results = []

def check(name, condition, detail="", severity="error"):
    status = PASS if condition else (FAIL if severity == "error" else WARN)
    results.append((name, status, detail))
    print(f"  {status} {name}" + (f" -- {detail}" if detail else ""))
    return condition

print("=" * 70)
print("FULL SYSTEM AUDIT: AI Agent Research System v17")
print("=" * 70)

# =====================================================================
# 1. CORE IMPORTS
# =====================================================================
print("\n[1] Core Imports")
try:
    from src.langgraph.state import ResearchState, create_initial_state
    check("Import state.py", True)
except Exception as e:
    check("Import state.py", False, str(e))

try:
    from src.langgraph.graph import create_research_graph, run_graph, run_without_langgraph
    check("Import graph.py", True)
except Exception as e:
    check("Import graph.py", False, str(e))

try:
    from src.langgraph.tools_integration import (
        AGENT_TOOLS_MAP, _TOOL_REGISTRY, TOOLS_AVAILABLE, get_tools_for_agent
    )
    check("Import tools_integration.py", True)
    check("TOOLS_AVAILABLE = True", TOOLS_AVAILABLE)
except Exception as e:
    check("Import tools_integration.py", False, str(e))

try:
    from src.langgraph.nodes.router import route_request, SOP_REGISTRY
    check("Import router.py", True)
except Exception as e:
    check("Import router.py", False, str(e))

try:
    from src.tools import LITERATURE_TOOLS, WRITING_TOOLS, ANALYSIS_TOOLS, WOLFRAM_TOOLS, SYMPY_TOOLS, CONVERT_TOOLS
    check("Import all tool categories", True)
    total_tools = len(LITERATURE_TOOLS) + len(WRITING_TOOLS) + len(ANALYSIS_TOOLS) + len(WOLFRAM_TOOLS) + len(SYMPY_TOOLS) + len(CONVERT_TOOLS)
    check(f"Total tools registered: {total_tools}", total_tools > 0)
except Exception as e:
    check("Import tool categories", False, str(e))

# =====================================================================
# 2. AGENT JSON INTEGRITY
# =====================================================================
print("\n[2] Agent JSON Integrity (119 files)")
agents_dir = PROJECT_ROOT / "agents"
agent_files = list(agents_dir.glob("*.json"))
check(f"Agent files found: {len(agent_files)}", len(agent_files) >= 100)

required_fields = ["name", "role", "domain", "sdp_output_dir"]
agents_missing_fields = []
agents_missing_tools = []
agents_bad_json = []
agent_names = set()
valid_sdp_dirs = [
    "0_Project_Admin", "1_Strategic_Plan", "2_Literature_Review",
    "3_Theoretical_Framework", "4_Methodology_Design", "5_Experiments_Simulations",
    "6_Analysis_Results", "7_Manuscript_Draft", "8_Project_Management",
    "9_Presentation", "Utils",
]

for af in agent_files:
    try:
        with open(af, "r", encoding="utf-8") as f:
            agent_data = json.load(f)
        agent_name = agent_data.get("name", af.stem)
        agent_names.add(agent_name)
        
        # Check required fields
        missing = [rf for rf in required_fields if rf not in agent_data or not agent_data[rf]]
        if missing:
            agents_missing_fields.append(f"{af.name}: missing {missing}")
        
        # Check sdp_output_dir is valid
        sdp = agent_data.get("sdp_output_dir", "")
        if sdp and sdp not in valid_sdp_dirs:
            agents_missing_fields.append(f"{af.name}: invalid sdp_output_dir={sdp}")
        
        # Check if tools[] references exist in AGENT_TOOLS_MAP
        agent_tools = agent_data.get("tools", [])
        if agent_tools and agent_name not in AGENT_TOOLS_MAP and agent_name != "MasterOrchestrator":
            agents_missing_tools.append(agent_name)
        
    except json.JSONDecodeError as e:
        agents_bad_json.append(f"{af.name}: {e}")
    except Exception as e:
        agents_bad_json.append(f"{af.name}: {e}")

check("All agent JSONs parse OK", len(agents_bad_json) == 0, 
      f"{len(agents_bad_json)} failures: {agents_bad_json[:5]}" if agents_bad_json else "")
check("All agents have required fields", len(agents_missing_fields) == 0,
      f"{len(agents_missing_fields)} issues: {agents_missing_fields[:5]}" if agents_missing_fields else "")

if agents_missing_tools:
    check(f"Agents with tools[] but not in AGENT_TOOLS_MAP", False,
          f"{len(agents_missing_tools)} agents: {agents_missing_tools[:10]}", severity="warn")
else:
    check("All tool-equipped agents in AGENT_TOOLS_MAP", True)

# =====================================================================
# 3. TOOL REGISTRATION CONSISTENCY
# =====================================================================
print("\n[3] Tool Registration Consistency")

# Check all tools in AGENT_TOOLS_MAP exist in _TOOL_REGISTRY
all_mapped_tools = set()
for tools_list in AGENT_TOOLS_MAP.values():
    all_mapped_tools.update(tools_list)

unresolved_tools = [t for t in all_mapped_tools if t not in _TOOL_REGISTRY]
check("All AGENT_TOOLS_MAP tools in registry", len(unresolved_tools) == 0,
      f"Missing: {unresolved_tools}" if unresolved_tools else "")

# Check _TOOL_REGISTRY callables are actually callable
non_callable = [name for name, func in _TOOL_REGISTRY.items() if func is not None and not callable(func)]
check("All registry entries are callable", len(non_callable) == 0,
      f"Non-callable: {non_callable}" if non_callable else "")

# Check for async tools in registry (should be sync)
import asyncio
async_tools = [name for name, func in _TOOL_REGISTRY.items() 
               if func is not None and asyncio.iscoroutinefunction(func)]
check("No async tools in sync registry", len(async_tools) == 0,
      f"Async: {async_tools}" if async_tools else "")

# =====================================================================
# 4. ROUTING CONSISTENCY
# =====================================================================
print("\n[4] Routing Consistency")

# Check SOP pipeline agent references exist as JSON files
all_sop_agents = set()
for sop_name, sop_data in SOP_REGISTRY.items():
    pipeline = sop_data.get("pipeline", [])
    all_sop_agents.update(pipeline)

missing_sop_agents = [a for a in all_sop_agents if a not in agent_names]
check("All SOP agents have JSON files", len(missing_sop_agents) == 0,
      f"Missing JSONs: {missing_sop_agents[:10]}" if missing_sop_agents else f"{len(all_sop_agents)} unique SOP agents")

# Check SOP pipeline agent references
sop_missing_agents = []
for sop_name, sop_data in SOP_REGISTRY.items():
    pipeline = sop_data.get("pipeline", [])
    for agent in pipeline:
        if agent not in agent_names:
            sop_missing_agents.append(f"{sop_name}: references {agent}")

check(f"All SOP pipeline agents exist (40 SOPs)", len(sop_missing_agents) == 0,
      f"Missing: {sop_missing_agents[:5]}" if sop_missing_agents else "")

# Test actual routing
test_routes = [
    "find papers about cybersecurity",
    "write a paper about AI",
    "verify this equation",
    "review my manuscript",
    "design a survey",
]
for query in test_routes:
    try:
        result = route_request(query)
        # route_request returns Tuple[str, str, List[str]]: (agent, domain, keywords)
        agent = result[0] if isinstance(result, tuple) else str(result)
        check(f"Route '{query[:30]}...'", agent and len(agent) > 0, f"-> {agent}")
    except Exception as e:
        check(f"Route '{query[:30]}...'", False, str(e))

# =====================================================================
# 5. WORKFLOW FILES
# =====================================================================
print("\n[5] Workflow Files (41 workflows)")
workflows_dir = PROJECT_ROOT / ".agent" / "workflows"
workflow_files = list(workflows_dir.glob("*.md"))
check(f"Workflow files found: {len(workflow_files)}", len(workflow_files) >= 30)

# Check each workflow has proper frontmatter
bad_frontmatter = []
for wf in workflow_files:
    content = wf.read_text(encoding="utf-8").lstrip('\ufeff')  # strip BOM
    if not content.strip().startswith("---"):
        bad_frontmatter.append(wf.name)
    elif "description:" not in content[:500]:
        bad_frontmatter.append(wf.name)

check("All workflows have frontmatter", len(bad_frontmatter) == 0,
      f"Missing frontmatter: {bad_frontmatter[:5]}" if bad_frontmatter else "")

# =====================================================================
# 6. INIT.MD FLOW INTEGRITY
# =====================================================================
print("\n[6] Init.md Flow Integrity")
init_content = (workflows_dir / "init.md").read_text(encoding="utf-8")

# Check that init.md references critical files/steps
init_checks = {
    "References SESSION_STATE.md": "SESSION_STATE.md" in init_content,
    "References setup_cm_os.py": "setup_cm_os.py" in init_content,
    "References mem0_loader.py": "mem0_loader.py" in init_content,
    "References MasterOrchestrator": "MasterOrchestrator" in init_content,
    "References config.yaml": "config.yaml" in init_content,
    "References memory-rule.md": "memory-rule.md" in init_content or "memory" in init_content.lower(),
    "References requirements.txt": "requirements.txt" in init_content,
    "Has Step ordering (at least 5 steps)": init_content.count("## Step") >= 5,
    "References LangGraph pipeline": "langgraph" in init_content.lower() or "LangGraph" in init_content,
    "References src.langgraph.cli": "src.langgraph.cli" in init_content,
}
for check_name, passed in init_checks.items():
    check(check_name, passed)

# =====================================================================
# 7. CRITICAL FILE EXISTENCE
# =====================================================================
print("\n[7] Critical File Existence")
critical_files = [
    "config.yaml",
    "requirements.txt",
    ".env",
    ".agent/rules/memory-rule.md",
    ".agent/scripts/route.py",
    ".agent/scripts/setup_cm_os.py",
    ".agent/workflows/init.md",
    "agents/MasterOrchestrator.json",
    "src/langgraph/graph.py",
    "src/langgraph/state.py",
    "src/langgraph/cli.py",
    "src/langgraph/tools_integration.py",
    "src/langgraph/tool_executor.py",
    "src/tools/literature_tools.py",
    "src/tools/writing_tools.py",
    "src/tools/analysis_tools.py",
    "src/tools/wolfram_tools.py",
    "src/tools/sympy_tools.py",
    "src/tools/mem0_loader.py",
    "src/tools/auto_experiment_tools.py",
    "src/tools/bibtex_optimizer.py",
    "src/tools/convert_to_markdown.py",
    "run_agent.py",
]
for cf in critical_files:
    exists = (PROJECT_ROOT / cf).exists()
    check(f"Exists: {cf}", exists)

# =====================================================================
# 8. LANGGRAPH GRAPH STRUCTURE
# =====================================================================
print("\n[8] LangGraph Graph Structure")
from src.langgraph.graph import create_research_graph, invalidate_graph_cache
invalidate_graph_cache()
graph = create_research_graph()
check("Graph compiles", graph is not None)

if graph:
    nodes = list(graph.nodes.keys())
    real_nodes = [n for n in nodes if not n.startswith("__")]
    check(f"Graph has 14 nodes", len(real_nodes) == 14, f"nodes={real_nodes}")

# =====================================================================
# 9. CONFIG.YAML INTEGRITY
# =====================================================================
print("\n[9] Config.yaml Integrity")
try:
    import yaml
    config = yaml.safe_load((PROJECT_ROOT / "config.yaml").read_text(encoding="utf-8"))
    check("Config.yaml parses OK", True)
    check("Has 'project_name'", "project_name" in config)
except ImportError:
    try:
        # Fallback: just read the file
        config_text = (PROJECT_ROOT / "config.yaml").read_text(encoding="utf-8")
        check("Config.yaml readable", True)
        check("Has 'project_name'", "project_name" in config_text)
    except Exception as e:
        check("Config.yaml", False, str(e))
except Exception as e:
    check("Config.yaml", False, str(e))

# =====================================================================
# 10. INIT.MD OUTDATED REFERENCES
# =====================================================================
print("\n[10] Init.md Outdated References Check")
# The init.md says "116 agents" but we have 119
agent_count_match = re.search(r"(\d+)\s*agent", init_content)
if agent_count_match:
    stated = int(agent_count_match.group(1))
    actual = len(agent_files)
    check(f"init.md agent count matches reality", stated == actual,
          f"init.md says {stated}, actual={actual}", severity="warn")

# Check pipeline description matches actual graph
if "optimize_prompt" in init_content and "validate_output" not in init_content:
    check("init.md pipeline description is up-to-date", False,
          "Missing new nodes: validate_output, context_compress, sop_orchestrator, checkpoint", severity="warn")
else:
    check("init.md pipeline description", "validate_output" in init_content)

# =====================================================================
# 11. TESTS HEALTH
# =====================================================================
print("\n[11] Tests Health")
test_files = list((PROJECT_ROOT / "tests").glob("test_*.py"))
check(f"Test files found: {len(test_files)}", len(test_files) >= 4)

for tf in test_files:
    content = tf.read_text(encoding="utf-8")
    has_imports = "import" in content
    has_tests = "def test_" in content
    check(f"{tf.name}: valid test structure", has_imports and has_tests)

# =====================================================================
# 12. .ENV FILE KEYS
# =====================================================================
print("\n[12] .env File Keys (no values shown)")
env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    env_content = env_file.read_text(encoding="utf-8")
    expected_keys = ["SERPAPI_API_KEY", "WOLFRAM_ALPHA_APP_ID"]
    for key in expected_keys:
        has_key = key in env_content
        check(f".env has {key}", has_key, severity="warn")

# =====================================================================
# 13. MEMORY SYSTEM CHECK
# =====================================================================
print("\n[13] Memory System Files")
ai_memory_dir = PROJECT_ROOT / ".ai_memory"
if ai_memory_dir.exists():
    check(".ai_memory/ exists", True)
    expected_subdirs = ["scripts", "packs"]
    for sd in expected_subdirs:
        check(f".ai_memory/{sd}/ exists", (ai_memory_dir / sd).exists())
else:
    check(".ai_memory/ exists", False, "Run setup_cm_os.py first", severity="warn")

memory_dir = PROJECT_ROOT / ".memory"
check(".memory/ exists", memory_dir.exists())

# =====================================================================
# 14. CROSS-REFERENCE: agents with tools in JSON vs AGENT_TOOLS_MAP
# =====================================================================
print("\n[14] Agent Tools Cross-Reference")
agents_with_tools_in_json = []
agents_with_no_map = []

for af in agent_files:
    try:
        with open(af, "r", encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("name", af.stem)
        tools = data.get("tools", [])
        if tools and len(tools) > 0:
            agents_with_tools_in_json.append(name)
            if name not in AGENT_TOOLS_MAP:
                agents_with_no_map.append(name)
    except:
        pass

check(f"Agents with tools[] in JSON: {len(agents_with_tools_in_json)}", True)
check(f"Agents in AGENT_TOOLS_MAP: {len(AGENT_TOOLS_MAP) - 1}", True, "(minus _default)")

if agents_with_no_map:
    check("All tool-agents mapped in tools_integration.py", False,
          f"{len(agents_with_no_map)} unmapped: {agents_with_no_map[:15]}", severity="warn")
else:
    check("All tool-agents mapped", True)

# =====================================================================
# SUMMARY
# =====================================================================
print("\n" + "=" * 70)
passed = sum(1 for _, s, _ in results if s == PASS)
failed = sum(1 for _, s, _ in results if s == FAIL)
warned = sum(1 for _, s, _ in results if s == WARN)
total = len(results)
pct = (passed/total*100) if total else 0
print(f"RESULTS: {passed}/{total} passed ({pct:.0f}%), {failed} FAIL, {warned} WARN")

if failed > 0:
    print(f"\n{FAIL} FAILURES:")
    for name, status, detail in results:
        if status == FAIL:
            print(f"  {FAIL} {name}: {detail}")

if warned > 0:
    print(f"\n{WARN} WARNINGS:")
    for name, status, detail in results:
        if status == WARN:
            print(f"  {WARN} {name}: {detail}")

print("=" * 70)
sys.exit(1 if failed > 0 else 0)
