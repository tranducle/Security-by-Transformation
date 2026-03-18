"""
Evaluation Harness for Autoresearch-Style Self-Improvement Loop.

This is the equivalent of autoresearch's prepare.py — a READ-ONLY evaluation
script that produces a composite quality score. DO NOT MODIFY this file
during experiments.

Usage:
    python src/tools/evaluate_system.py
    python src/tools/evaluate_system.py --json

Output:
    ---
    quality_score:     0.847
    routing_accuracy:  0.920
    test_pass_rate:    1.000
    health_errors:     0
    health_warnings:   2
    tests_total:       22
    tests_passed:      22
    routing_total:     10
    routing_correct:   9
"""

import sys
import json
import time
import subprocess
import unittest
import io
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# 1. Routing Accuracy Test
# ---------------------------------------------------------------------------

# Expected routing results — ground truth for scoring
ROUTING_TESTS = [
    # ---- Original 20 tests ----
    ("create tikz diagram", "TikZPlotter"),
    ("find literature on cybersecurity", "LiteratureHunter"),
    ("write methodology section", "MethodologyArchitect"),
    ("threat model for zero trust", "ThreatModeler"),
    ("cost benefit analysis", "CostBenefitAnalyst"),
    ("game theory analysis", "GameTheoryStrategist"),
    ("optimize bibtex entries", "BibTeXOptimizer"),
    ("fix my bibtex references", "BibTeXOptimizer"),
    ("create latex document", "LatexPaperGenerator"),
    ("create mermaid flowchart", "HybridVisualizer"),
    ("read pdf document for me", "FileToMarkdownConverter"),
    ("find papers on machine learning", "LiteratureHunter"),
    ("write paper abstract", "AbstractTitleGenerator"),
    ("design an experiment", "SOP_QUANT_EXPERIMENT"),
    ("brainstorm research ideas", "BrainstormingFacilitator"),
    ("analyze data with t-test", "StatisticalAnalyst"),
    ("causal inference analysis", "CausalAnalyst"),
    ("survey design questionnaire", "SurveyDesignerAnalyst"),
    ("security architecture design", "SOP_DEFENSE_ARCH"),
    ("deployment friction estimation", "DeploymentFrictionEstimator"),
    # ---- Exp#6: 10 harder edge cases ----
    ("run p-value significance test", "StatisticalAnalyst"),
    ("convert my docx file to text", "FileToMarkdownConverter"),
    ("write a grant proposal for NSF", "SOP_GRANT_APPLICATION"),  # SOP correct for full grants
    ("preprocess my data for training", "DataPreprocessingEngineer"),
    ("create a pytorch neural network", "SOP_CODE_IMPLEMENTATION"),  # SOP correct for code impl
    ("check my paper for hidden assumptions", "SOP_PAPER_HARDENING"),  # SOP correct for paper audit
    ("simulate harsh reviewer feedback", "HarshReviewer"),
    ("find research gap in IoT security", "GapScout"),
    ("visualize my experiment results", "ResultVisualizer"),
    ("check novelty of my contribution", "SOP_NOVELTY_DEFENSE"),  # SOP correct for novelty check
    # ---- Exp#9: 10 cross-domain & ambiguous edge cases ----
    ("systematic literature review prisma", "SLRProtocolDroid"),
    ("create beamer slides", "SOP_PRESENTATION_GEN"),  # SOP correct for full presentation
    ("calculate nash equilibrium", "NashEquilibriumStrategist"),
    ("incident response playbook", "IncidentReadinessPlaybookGenerator"),
    ("polish my writing style", "WritingStylePolisher"),
    ("debug pytorch training loop", "CoderReproAgent"),
    ("cyber insurance cost analysis", "CyberInsuranceAnalyst"),  # correct - Analyst handles cost analysis
    ("daily research summary", "DailySummarizer"),
    ("mathematical proof verification", "MathProofAuditor"),
    ("generate tikz plot for results", "TikZPlotter"),
    # ---- Exp#13: 10 rare agent & tricky edge cases ----
    ("run regression analysis with instrumental variables", "EconometricsModeler"),
    ("write specific aims for NIH grant", "SOP_GRANT_APPLICATION"),  # SOP correct for full grant
    ("check GDPR compliance of my dataset", "DataPrivacyOfficer"),
    ("create a case study document", "SOP_CASE_STUDY"),  # SOP correct for full case study
    ("model attacker-defender game dynamics", "GameTheoryStrategist"),
    ("find semantic scholar citations", "SemanticSearch"),
    ("refactor and clean my python code", "CoderReproAgent"),
    ("text to summarize from a single document", "DocumentSynthesizer"),
    ("scope my research project boundaries", "ResearchScoper"),
    ("create ascii diagram of system architecture", "HybridVisualizer"),
    # ---- Exp#16: 10 compound multi-keyword queries ----
    ("run difference-in-differences causal analysis", "EconometricsModeler"),
    ("write a briefing doc on cybersecurity", "SOP_DEFENSE_ARCH"),  # SOP correct for security-focused writing
    ("create docker reproducibility artifact", "ReproducibilityArtifactEngineer"),
    ("extract tables from this pdf", "FileToMarkdownConverter"),
    ("check my paper for overclaiming bias", "SOP_PAPER_HARDENING"),  # SOP correct for paper audit
    ("design a likert scale survey instrument", "SurveyDesignerAnalyst"),
    ("estimate hardware GPU memory for training", "HardwareresourceEstimator"),
    ("find openalex open access papers", "OpenAlexSearch"),
    ("generate matplotlib figure for paper", "SOP_FIGURE_GENERATION"),  # SOP correct for full figure
    ("build a research framework architecture", "SOP_FRAMEWORK_DEV"),  # SOP correct for framework
]


def run_routing_accuracy():
    """Test routing accuracy against expected results."""
    try:
        from src.langgraph.nodes.router import route_request
    except Exception as e:
        return {"correct": 0, "total": len(ROUTING_TESTS), "accuracy": 0.0, "error": str(e)}

    correct = 0
    total = len(ROUTING_TESTS)
    details = []

    for query, expected_agent in ROUTING_TESTS:
        try:
            domain, agent, keywords = route_request(query)
            # For SOP triggers, the agent might be SOP:SOP_NAME
            # Accept if the expected agent name is contained
            is_correct = (agent == expected_agent) or (expected_agent in agent)
            if is_correct:
                correct += 1
            details.append({
                "query": query,
                "expected": expected_agent,
                "got": agent,
                "correct": is_correct,
            })
        except Exception as e:
            details.append({
                "query": query,
                "expected": expected_agent,
                "got": f"ERROR: {e}",
                "correct": False,
            })

    return {
        "correct": correct,
        "total": total,
        "accuracy": correct / total if total > 0 else 0.0,
        "details": details,
    }


# ---------------------------------------------------------------------------
# 2. Unit Test Pass Rate
# ---------------------------------------------------------------------------

def run_unit_tests():
    """Run pytest and return pass/fail counts."""
    tests_dir = PROJECT_ROOT / "tests"
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests_dir), "-q", "--tb=no", "--no-header"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout + result.stderr

        # Parse pytest output: "22 passed, 1 failed" or "22 passed"
        passed = 0
        failed = 0
        for line in output.split("\n"):
            line = line.strip()
            if "passed" in line or "failed" in line:
                import re
                m_passed = re.search(r"(\d+)\s+passed", line)
                m_failed = re.search(r"(\d+)\s+failed", line)
                if m_passed:
                    passed = int(m_passed.group(1))
                if m_failed:
                    failed = int(m_failed.group(1))

        total = passed + failed
        return {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": passed / total if total > 0 else 0.0,
            "output": output[-500:] if len(output) > 500 else output,
        }
    except subprocess.TimeoutExpired:
        return {"passed": 0, "failed": 0, "total": 0, "pass_rate": 0.0, "error": "timeout"}
    except Exception as e:
        return {"passed": 0, "failed": 0, "total": 0, "pass_rate": 0.0, "error": str(e)}


# ---------------------------------------------------------------------------
# 3. Health Check
# ---------------------------------------------------------------------------

def run_health_check():
    """Run system health check and count errors/warnings."""
    try:
        from src.langgraph.nodes.router import ROUTING_RULES, SOP_REGISTRY
        from src.langgraph.nodes.agent_loader import load_agent
    except Exception as e:
        return {"errors": 99, "warnings": 0, "error": str(e)}

    agents_dir = PROJECT_ROOT / "agents"
    all_json = sorted([f.stem for f in agents_dir.glob("*.json")])
    errors = 0
    warnings = 0

    # Check 1: All agents load
    for name in all_json:
        config = load_agent(name)
        if config is None:
            errors += 1

    # Check 2: Ghost agents (in routing but no JSON)
    routing_agents = set()
    for domain, agents in ROUTING_RULES.items():
        for agent in agents:
            routing_agents.add(agent)
    ghosts = routing_agents - set(all_json)
    errors += len(ghosts)

    # Check 3: Orphan agents
    orphans = set(all_json) - routing_agents - {"MasterOrchestrator"}
    warnings += len(orphans)

    # Check 4: Domain consistency
    domain_map = {}
    for domain, agents in ROUTING_RULES.items():
        for agent_name in agents:
            domain_map[agent_name] = domain
    for agent_name, expected in domain_map.items():
        config = load_agent(agent_name)
        if config and config.get("domain", "") != expected:
            errors += 1

    # Check 5: Keyword conflicts
    keyword_agents = defaultdict(set)
    for domain, agents_dict in ROUTING_RULES.items():
        for agent_name, keywords in agents_dict.items():
            for kw in keywords:
                keyword_agents[kw].add(agent_name)
    conflicts = {kw: a for kw, a in keyword_agents.items() if len(a) > 1}
    if len(conflicts) >= 15:
        warnings += 1

    return {
        "errors": errors,
        "warnings": warnings,
        "agents_total": len(all_json),
        "routing_agents": len(routing_agents),
        "sops_total": len(SOP_REGISTRY),
        "conflicts": len(conflicts),
    }


# ---------------------------------------------------------------------------
# 4. Composite Score Calculation
# ---------------------------------------------------------------------------

def compute_composite_score(routing, tests, health):
    """
    Composite quality score (0.0 - 1.0).

    Weights:
      - routing_accuracy: 40%  (most critical — wrong routing = wrong agent)
      - test_pass_rate:   30%  (code correctness)
      - health_score:     20%  (system integrity — 0 errors = 1.0)
      - conflict_score:   10%  (low keyword conflicts = better)
    """
    routing_acc = routing.get("accuracy", 0.0)
    test_rate = tests.get("pass_rate", 0.0)

    # Health: 1.0 if 0 errors, degrades with errors
    health_errors = health.get("errors", 0)
    health_score = max(0.0, 1.0 - (health_errors * 0.1))

    # Conflicts: 1.0 if < 5 conflicts, degrades after
    conflicts = health.get("conflicts", 0)
    conflict_score = max(0.0, 1.0 - max(0, conflicts - 5) * 0.05)

    composite = (
        0.40 * routing_acc
        + 0.30 * test_rate
        + 0.20 * health_score
        + 0.10 * conflict_score
    )

    return round(composite, 6)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def evaluate():
    """Run full evaluation and return results dict."""
    start = time.time()

    routing = run_routing_accuracy()
    tests = run_unit_tests()
    health = run_health_check()
    quality_score = compute_composite_score(routing, tests, health)

    elapsed = round(time.time() - start, 1)

    return {
        "quality_score": quality_score,
        "routing_accuracy": routing.get("accuracy", 0.0),
        "routing_correct": routing.get("correct", 0),
        "routing_total": routing.get("total", 0),
        "test_pass_rate": tests.get("pass_rate", 0.0),
        "tests_passed": tests.get("passed", 0),
        "tests_total": tests.get("total", 0),
        "health_errors": health.get("errors", 0),
        "health_warnings": health.get("warnings", 0),
        "health_agents": health.get("agents_total", 0),
        "health_sops": health.get("sops_total", 0),
        "conflicts": health.get("conflicts", 0),
        "eval_seconds": elapsed,
        "routing_details": routing.get("details", []),
        "test_output": tests.get("output", ""),
    }


def main():
    """CLI entry point."""
    results = evaluate()

    if "--json" in sys.argv:
        print(json.dumps(results, indent=2, default=str))
    else:
        # Autoresearch-style output
        print("---")
        print(f"quality_score:     {results['quality_score']:.6f}")
        print(f"routing_accuracy:  {results['routing_accuracy']:.3f}")
        print(f"test_pass_rate:    {results['test_pass_rate']:.3f}")
        print(f"health_errors:     {results['health_errors']}")
        print(f"health_warnings:   {results['health_warnings']}")
        print(f"tests_total:       {results['tests_total']}")
        print(f"tests_passed:      {results['tests_passed']}")
        print(f"routing_total:     {results['routing_total']}")
        print(f"routing_correct:   {results['routing_correct']}")
        print(f"conflicts:         {results['conflicts']}")
        print(f"eval_seconds:      {results['eval_seconds']}")

        # Show routing failures
        failures = [d for d in results.get("routing_details", []) if not d.get("correct")]
        if failures:
            print("\n--- routing failures ---")
            for f in failures:
                print(f"  FAIL: '{f['query']}' → expected {f['expected']}, got {f['got']}")


if __name__ == "__main__":
    main()
