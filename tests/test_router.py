"""Unit tests for LangGraph routing system."""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestLangGraphRouter(unittest.TestCase):
    def setUp(self):
        from src.langgraph.nodes.router import (
            route_request,
            ROUTING_RULES,
            KEYWORD_TO_AGENT,
            SOP_REGISTRY,
        )

        self.route_request = route_request
        self.ROUTING_RULES = ROUTING_RULES
        self.KEYWORD_TO_AGENT = KEYWORD_TO_AGENT
        self.SOP_REGISTRY = SOP_REGISTRY

    def test_routing_rules_not_empty(self):
        self.assertEqual(len(self.ROUTING_RULES), 10)

    def test_keyword_to_agent_populated(self):
        self.assertGreater(len(self.KEYWORD_TO_AGENT), 50)

    def test_sop_registry_has_entries(self):
        self.assertGreater(len(self.SOP_REGISTRY), 30)

    def test_route_tikz(self):
        domain, agent, keywords = self.route_request("create tikz diagram")
        self.assertEqual(agent, "TikZPlotter")
        self.assertIn("Visualization", domain)

    def test_route_literature(self):
        domain, agent, keywords = self.route_request("find literature on cybersecurity")
        self.assertEqual(agent, "LiteratureHunter")

    def test_route_methodology(self):
        domain, agent, keywords = self.route_request("write methodology section")
        self.assertEqual(agent, "MethodologyArchitect")

    def test_route_statistics(self):
        domain, agent, keywords = self.route_request("run anova test on data")
        self.assertEqual(agent, "SOP:SOP_QUANT_EXPERIMENT")

    def test_route_threat_model(self):
        domain, agent, keywords = self.route_request("threat model for zero trust")
        self.assertEqual(agent, "ThreatModeler")

    def test_route_cost_benefit(self):
        domain, agent, keywords = self.route_request("cost benefit analysis")
        self.assertEqual(agent, "CostBenefitAnalyst")

    def test_route_review(self):
        domain, agent, keywords = self.route_request("review my paper")
        self.assertIn(agent, ["PeerReviewer", "ReviewerSimulator", "HarshReviewer"])

    def test_route_game_theory(self):
        domain, agent, keywords = self.route_request("game theory analysis")
        self.assertEqual(agent, "GameTheoryStrategist")

    def test_route_bibtex(self):
        domain, agent, keywords = self.route_request("optimize bibtex entries")
        self.assertEqual(agent, "BibTeXOptimizer")

    def test_route_fallback(self):
        domain, agent, keywords = self.route_request("xyzzy random noise 42")
        self.assertEqual(agent, "MasterOrchestrator")

    def test_sop_systematic_review(self):
        sop = self.SOP_REGISTRY.get("SOP_SYSTEMATIC_REVIEW")
        self.assertIsNotNone(sop)
        agents = sop.get("agents", sop) if isinstance(sop, dict) else sop
        if isinstance(agents, list):
            self.assertGreater(len(agents), 0)

    def test_all_agents_in_routing_have_json(self):
        agents_dir = PROJECT_ROOT / "agents"
        for domain, agents_dict in self.ROUTING_RULES.items():
            for agent_name in agents_dict:
                json_file = agents_dir / f"{agent_name}.json"
                self.assertTrue(
                    json_file.exists(),
                    f"Agent '{agent_name}' in domain '{domain}' has no JSON file",
                )


class TestRouterConflicts(unittest.TestCase):
    def test_conflicts_are_documented(self):
        from src.langgraph.nodes.router import ROUTING_RULES
        from collections import defaultdict

        keyword_agents = defaultdict(set)
        for domain, agents_dict in ROUTING_RULES.items():
            for agent_name, keywords in agents_dict.items():
                for kw in keywords:
                    keyword_agents[kw].add(agent_name)

        conflicts = {
            kw: agents for kw, agents in keyword_agents.items() if len(agents) > 1
        }
        self.assertLess(
            len(conflicts),
            15,
            f"Too many routing conflicts ({len(conflicts)}): {list(conflicts.keys())}",
        )


class TestDomainRoutingConsistency(unittest.TestCase):
    def test_json_domain_matches_routing_domain(self):
        import json
        from src.langgraph.nodes.router import ROUTING_RULES

        agents_dir = PROJECT_ROOT / "agents"

        domain_map = {}
        for domain, agents in ROUTING_RULES.items():
            for agent_name in agents:
                domain_map[agent_name] = domain

        mismatches = []
        for agent_name, expected_domain in domain_map.items():
            json_path = agents_dir / f"{agent_name}.json"
            if json_path.exists():
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                json_domain = data.get("domain", "MISSING")
                if json_domain != expected_domain:
                    mismatches.append(
                        f"{agent_name}: JSON='{json_domain}' vs ROUTING='{expected_domain}'"
                    )

        self.assertEqual(
            len(mismatches),
            0,
            f"Domain mismatches found:\n  " + "\n  ".join(mismatches),
        )


class TestPriorityKeywordCorrectness(unittest.TestCase):
    def setUp(self):
        from src.langgraph.nodes.router import route_request

        self.route_request = route_request

    def test_bibtex_routes_to_optimizer(self):
        domain, agent, kw = self.route_request("fix my bibtex references")
        self.assertEqual(agent, "BibTeXOptimizer")

    def test_latex_routes_to_generator(self):
        domain, agent, kw = self.route_request("create latex document")
        self.assertEqual(agent, "LatexPaperGenerator")

    def test_file_to_markdown_routing(self):
        domain, agent, kw = self.route_request("read pdf document for me")
        self.assertEqual(agent, "FileToMarkdownConverter")

    def test_mermaid_routes_to_hybrid(self):
        domain, agent, kw = self.route_request("create mermaid flowchart")
        self.assertEqual(agent, "HybridVisualizer")


class TestSemanticSOPMatching(unittest.TestCase):
    def route_request(self, message):
        from src.langgraph.nodes.router import route_request

        return route_request(message)

    def test_check_novelty_triggers_sop(self):
        domain, agent, kw = self.route_request("Check novelty of the proposal")
        self.assertIn("SOP_NOVELTY_DEFENSE", agent)

    def test_assess_gaps_triggers_correct_agent(self):
        domain, agent, kw = self.route_request("Assess research gaps in the field")
        self.assertTrue(
            agent == "GapScout" or "SOP_GAP_ANALYSIS" in agent,
            f"Expected GapScout or SOP_GAP_ANALYSIS, got: {agent}",
        )

    def test_evaluate_citations_triggers_sop(self):
        domain, agent, kw = self.route_request("Evaluate citation quality and DOIs")
        self.assertIn("SOP_CITATION_AUDIT", agent)

    def test_build_presentation_triggers_sop(self):
        domain, agent, kw = self.route_request("Build a presentation deck for my talk")
        self.assertIn("SOP_PRESENTATION_GEN", agent)

    def test_simple_query_stays_direct_agent(self):
        domain, agent, kw = self.route_request("find literature on cybersecurity")
        self.assertNotIn("SOP:", agent)

    def test_priority_keywords_bypass_semantic(self):
        domain, agent, kw = self.route_request("create tikz diagram")
        self.assertEqual(agent, "TikZPlotter")


if __name__ == "__main__":
    unittest.main()
