#!/usr/bin/env python3
"""
YAML to Agent Schema Migration Script
Converts legacy YAML agent definitions to new production-ready format.
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.schemas.agent_schema import (
    AgentDefinition,
    ToolDefinition,
    ToolParameter,
    TriggerCondition,
    MemoryType,
)


# Domain mapping based on MasterOrchestrator.yaml
DOMAIN_MAPPING = {
    # Strategy & Operations
    "StrategicArchitect": "Strategy & Operations",
    "ProjectPlanner": "Strategy & Operations",
    "AgileProjectManager": "Strategy & Operations",
    "LogicStrategist": "Strategy & Operations",
    "ResourceConstraintAuditor": "Strategy & Operations",
    "ProjectStateKeeper": "Strategy & Operations",
    "ProgressTracker": "Strategy & Operations",
    "Scoper": "Strategy & Operations",
    "ResearchPlanGenerator": "Strategy & Operations",
    
    # Research & Discovery
    "LiteratureHunter": "Research & Discovery",
    "GoogleScholarSearch": "Research & Discovery",
    "SemanticSearch": "Research & Discovery", 
    "ScopusSearch": "Research & Discovery",
    "GeneralWebSearcher": "Research & Discovery",
    "ResearchLibrarian": "Research & Discovery",
    "SLRProtocolDroid": "Research & Discovery",
    "DeepSearchPlanner": "Research & Discovery",
    "GapScout": "Research & Discovery",
    "GapMapperResearchOpportunityExtractor": "Research & Discovery",
    "PriorArtNoveltyScanner": "Research & Discovery",
    "JournalIdeaScout": "Research & Discovery",
    "DatasetResearchSpecialist": "Research & Discovery",
    
    # Methodology & Analysis
    "MethodologyArchitect": "Methodology & Analysis",
    "MethodologyExperimentDesigner": "Methodology & Analysis",
    "StatisticalAnalyst": "Methodology & Analysis",
    "SurveyDesignerAnalyst": "Methodology & Analysis",
    "QualitativeCoder": "Methodology & Analysis",
    "AppliedMathModeler": "Methodology & Analysis",
    "MathProofAuditor": "Methodology & Analysis",
    "MathSymbolicSolver": "Methodology & Analysis",
    "EconometricsModeler": "Methodology & Analysis",
    "CausalAnalyst": "Methodology & Analysis",
    "CausalIdentificationStrategist": "Methodology & Analysis",
    "GameTheoryStrategist": "Methodology & Analysis",
    "NashEquilibriumStrategist": "Methodology & Analysis",
    "DataMetricsAnalyst": "Methodology & Analysis",
    "ExperimentConductor": "Methodology & Analysis",
    
    # Security & Risk
    "CyberSecurityArchitect": "Security & Risk",
    "AdversarialAttackSimulator": "Security & Risk",
    "ThreatModeler": "Security & Risk",
    "SaaSShadowITCartographer": "Security & Risk",
    "ProtocolNetworkSemanticsVerifier": "Security & Risk",
    "NetworkTrafficModeler": "Security & Risk",
    "CryptoProtocolVerifier": "Security & Risk",
    "MinViableSecurityArchitect": "Security & Risk",
    "IncidentReadinessPlaybookGenerator": "Security & Risk",
    "RedTeamEthicsDualUseGuard": "Security & Risk",
    "SecurityStandardsChecker": "Security & Risk",
    "CyberInsuranceAnalyst": "Security & Risk",
    "CyberInsuranceActuary": "Security & Risk",
    "SupplyChainRiskAnalyst": "Security & Risk",
    "RegulatoryComplianceAuditor": "Security & Risk",
    
    # Writing & Synthesis
    "PublicationReadyWriter": "Writing & Synthesis",
    "PaperOutlineArchitect": "Writing & Synthesis",
    "PaperWriter": "Writing & Synthesis",
    "ManuscriptReviser": "Writing & Synthesis",
    "WritingStylePolisher": "Writing & Synthesis",
    "EditorAgent": "Writing & Synthesis",
    "GrantProposalStrategist": "Writing & Synthesis",
    "AbstractTitleGenerator": "Writing & Synthesis",
    "LatexPaperGenerator": "Writing & Synthesis",
    "ReferenceManager": "Writing & Synthesis",
    "BibTeXOptimizer": "Writing & Synthesis",
    "DeepSynthesizer": "Writing & Synthesis",
    "DocumentSynthesizer": "Writing & Synthesis",
    "MultiSourceSynthesizer": "Writing & Synthesis",
    "DialecticalSynthesizer": "Writing & Synthesis",
    "SummarizerSynthesizer": "Writing & Synthesis",
    "DailySummarizer": "Writing & Synthesis",
    "CaseStudyArchivist": "Writing & Synthesis",
    
    # Coding & Engineering
    "CoderReproAgent": "Coding & Engineering",
    "PyTorchImplementer": "Coding & Engineering",
    "CodeDebugger": "Coding & Engineering",
    "CodeRefactorer": "Coding & Engineering",
    "ReproducibilityArtifactEngineer": "Coding & Engineering",
    "FrameworkArchitect": "Coding & Engineering",
    "FrameworkValidationArchitect": "Coding & Engineering",
    "FileIntegrator": "Coding & Engineering",
    "HardwareresourceEstimator": "Coding & Engineering",
    "ModelCapabilityRouter": "Coding & Engineering",
    "CrossDomainTransferHybridizationAgent": "Coding & Engineering",
    
    # Visualization & Presentation
    "VisualCommunicationArchitect": "Visualization & Presentation",
    "TikZPlotter": "Visualization & Presentation",
    "FigureGenerator": "Visualization & Presentation",
    "ResultVisualizer": "Visualization & Presentation",
    "HybridVisualizer": "Visualization & Presentation",
    "DiagramGenerator": "Visualization & Presentation",
    "ConceptVisualizer": "Visualization & Presentation",
    "PresentationArchitect": "Visualization & Presentation",
    "PresentationGenerator": "Visualization & Presentation",
    "ExplainabilityTranslator": "Visualization & Presentation",
    
    # Review & Quality
    "PeerReviewer": "Review & Quality",
    "ReviewerSimulator": "Review & Quality",
    "HarshReviewer": "Review & Quality",
    "ReviewerStrategist": "Review & Quality",
    "CriticAgent": "Review & Quality",
    "CitationVerifier": "Review & Quality",
    "CitationIntegrityAuditor": "Review & Quality",
    "FeasibilityRigorSoundnessChecker": "Review & Quality",
    "BaselineBenchmarkNoveltyDefender": "Review & Quality",
    "JournalSelector": "Review & Quality",
    "EthicalComplianceGuard": "Review & Quality",
    "DataPrivacyOfficer": "Review & Quality",
    "AgentSystemArchitect": "Review & Quality",
    "PromptOptimizer": "Review & Quality",
    
    # Business & Enterprise
    "CostBenefitAnalyst": "Business & Enterprise",
    "SMETypologyArchitect": "Business & Enterprise",
    "CompetitorAnalyst": "Business & Enterprise",
    "EntrepreneurialPsychProfiler": "Business & Enterprise",
    "HumanFactorCultureQuantifier": "Business & Enterprise",
    "FutureScenarioForecaster": "Business & Enterprise",
    
    # Innovation & Ideation
    "InnovationStrategist": "Innovation & Ideation",
    "BrainstormingFacilitator": "Innovation & Ideation",
    "IdeaMutationDesignSpaceExplorer": "Innovation & Ideation",
    "IdeaConcretizer": "Innovation & Ideation",
    "SystemDynamicsMapper": "Innovation & Ideation",
    "OmniThinker": "Innovation & Ideation",
    "MissingPartSuggester": "Innovation & Ideation",
    "ResearchScoper": "Innovation & Ideation",
    "ContextManager": "Innovation & Ideation",
    "HypothesisEngine": "Innovation & Ideation",
    "HypothesisGenerator": "Innovation & Ideation",
    "ArgumentDefender": "Innovation & Ideation",
    "CrossDisciplinaryConnector": "Innovation & Ideation",
    "AuthorStylist": "Innovation & Ideation",
    "AcademicPaperCritic": "Innovation & Ideation",
    "ArchiveManager": "Innovation & Ideation",
}

# Domain leads
DOMAIN_LEADS = {
    "Strategy & Operations": "StrategicArchitect",
    "Research & Discovery": "LiteratureHunter",
    "Methodology & Analysis": "MethodologyArchitect",
    "Security & Risk": "CyberSecurityArchitect",
    "Writing & Synthesis": "PublicationReadyWriter",
    "Coding & Engineering": "CoderReproAgent",
    "Visualization & Presentation": "VisualCommunicationArchitect",
    "Review & Quality": "PeerReviewer",
    "Business & Enterprise": "CostBenefitAnalyst",
    "Innovation & Ideation": "InnovationStrategist",
}

# Tool assignments based on agent capabilities
AGENT_TOOLS = {
    "LiteratureHunter": ["search_semantic_scholar", "search_google_scholar"],
    "SemanticSearch": ["search_semantic_scholar"],
    "GoogleScholarSearch": ["search_google_scholar"],
    "BibTeXOptimizer": ["parse_bibtex_file", "doi_to_bibtex", "lookup_doi"],
    "ReferenceManager": ["parse_bibtex_file", "write_markdown_section"],
    "CitationIntegrityAuditor": ["lookup_doi"],
    "PaperWriter": ["write_markdown_section"],
    "DeepSynthesizer": ["write_markdown_section"],
    "DocumentSynthesizer": ["write_markdown_section"],
    "StatisticalAnalyst": ["calculate_descriptive_stats", "independent_t_test", "correlation", "generate_stats_report"],
}

# Comprehensive trigger keywords from MasterOrchestrator.yaml Smart Routing
AGENT_TRIGGERS = {
    # Strategy & Planning
    "StrategicArchitect": ["plan", "roadmap", "strategy", "blueprint", "wbs", "strategic plan"],
    "ResearchPlanGenerator": ["research plan", "detailed plan", "comprehensive plan"],
    "ProjectStateKeeper": ["track", "status", "log", "progress", "project state"],
    "ProgressTracker": ["track progress", "milestone", "status update"],
    "AgileProjectManager": ["agile", "sprint", "kanban", "scrum"],
    "LogicStrategist": ["logic", "mece", "hypothesis", "problem solve"],
    "Scoper": ["scope", "boundary", "limit"],
    "ResearchScoper": ["research scope", "define scope", "scope definition"],
    "ResourceConstraintAuditor": ["resource", "budget", "tco", "feasibility", "resource constraint"],
    
    # Research & Discovery
    "LiteratureHunter": ["find papers", "search papers", "literature", "academic search", "tìm papers", "tìm bài báo", "research literature"],
    "GoogleScholarSearch": ["google scholar", "scholar search"],
    "SemanticSearch": ["semantic scholar", "citation graph", "related papers"],
    "ScopusSearch": ["scopus", "elsevier", "high impact"],
    "GeneralWebSearcher": ["web search", "general search", "internet", "tìm trên web"],
    "SLRProtocolDroid": ["systematic review", "slr", "prisma", "systematic literature review"],
    "GapScout": ["gap", "research gap", "opportunity", "lỗ hổng nghiên cứu"],
    "GapMapperResearchOpportunityExtractor": ["research opportunity", "gap analysis"],
    "PriorArtNoveltyScanner": ["prior art", "novelty check", "patent", "novelty"],
    "JournalIdeaScout": ["research idea", "find topic", "what should I research", "journal topic", "new project idea", "trending topics", "ý tưởng nghiên cứu"],
    "DatasetResearchSpecialist": ["dataset", "data source", "find data"],
    
    # Methodology & Analysis
    "MethodologyArchitect": ["methodology", "research design", "rigor", "phương pháp"],
    "MethodologyExperimentDesigner": ["experiment", "experiment design", "thiết kế thí nghiệm"],
    "ExperimentConductor": ["run experiment", "conduct experiment"],
    "StatisticalAnalyst": ["statistics", "p-value", "anova", "t-test", "regression", "thống kê", "phân tích thống kê"],
    "SurveyDesignerAnalyst": ["survey", "likert", "questionnaire", "efa", "cfa", "khảo sát"],
    "QualitativeCoder": ["qualitative", "thematic", "coding", "interview", "định tính"],
    "AppliedMathModeler": ["math model", "optimization", "linear program", "mô hình toán"],
    "MathProofAuditor": ["proof", "theorem", "verify math", "chứng minh"],
    "MathSymbolicSolver": ["solve equation", "symbolic", "sympy"],
    "EconometricsModeler": ["econometrics", "did", "iv", "rdd"],
    "CausalAnalyst": ["causal", "causality", "cause effect", "nhân quả"],
    "CausalIdentificationStrategist": ["causal identification", "identification strategy"],
    "GameTheoryStrategist": ["game theory", "nash", "attacker defender", "lý thuyết trò chơi"],
    "NashEquilibriumStrategist": ["nash equilibrium", "equilibrium analysis"],
    
    # Security & Risk
    "CyberSecurityArchitect": ["security architecture", "defense", "nist", "zero trust", "an ninh mạng"],
    "AdversarialAttackSimulator": ["attack", "red team", "kill chain", "mitre", "tấn công"],
    "ThreatModeler": ["threat model", "stride", "dread", "mô hình mối đe dọa"],
    "SaaSShadowITCartographer": ["shadow it", "saas", "cloud risk"],
    "ProtocolNetworkSemanticsVerifier": ["protocol", "rfc", "packet"],
    "NetworkTrafficModeler": ["network", "traffic model", "queueing"],
    "CryptoProtocolVerifier": ["crypto", "encryption", "tls", "certificate", "mã hóa"],
    "IncidentReadinessPlaybookGenerator": ["incident", "playbook", "ir", "incident response"],
    "MinViableSecurityArchitect": ["sme security", "lightweight security", "basic security"],
    "SupplyChainRiskAnalyst": ["supply chain", "vendor risk", "tprm", "third party"],
    "CyberInsuranceAnalyst": ["cyber insurance", "risk transfer", "bảo hiểm mạng"],
    "CyberInsuranceActuary": ["premium", "actuarial", "insurance cost"],
    "RegulatoryComplianceAuditor": ["compliance", "gdpr", "hipaa", "iso", "regulatory"],
    "SecurityStandardsChecker": ["security standards", "iso 27001", "nist compliance"],
    "RedTeamEthicsDualUseGuard": ["dual use", "ethics", "harm"],
    
    # Writing & Synthesis
    "PublicationReadyWriter": ["write paper", "manuscript", "draft", "viết bài"],
    "PaperOutlineArchitect": ["paper outline", "manuscript outline", "structure paper", "dàn ý"],
    "PaperWriter": ["write section", "draft section"],
    "ManuscriptReviser": ["revise manuscript", "address reviewer", "revision", "rewrite paragraph", "fix paper", "chỉnh sửa"],
    "WritingStylePolisher": ["polish", "refine", "style", "grammar"],
    "EditorAgent": ["edit", "proofread", "chỉnh sửa văn bản"],
    "GrantProposalStrategist": ["grant", "proposal", "funding", "nsf", "nih", "đề xuất dự án"],
    "AbstractTitleGenerator": ["abstract", "title", "summary", "tóm tắt", "tiêu đề"],
    "LatexPaperGenerator": ["latex", "format paper", "generate latex"],
    "ReferenceManager": ["references", "bibliography", "citation manager"],
    "BibTeXOptimizer": ["optimize bib", "fix bibtex", "find doi", "clean references", "doi2bib"],
    "DeepSynthesizer": ["synthesize", "summarize", "combine", "tổng hợp"],
    "MultiSourceSynthesizer": ["multi source", "combine sources", "synthesize multiple"],
    "DocumentSynthesizer": ["document synthesis", "combine documents"],
    "DailySummarizer": ["daily summary", "session summary"],
    "CaseStudyArchivist": ["case study", "use case", "real world example"],
    
    # Coding & Engineering
    "CoderReproAgent": ["code", "implement", "lập trình"],
    "PyTorchImplementer": ["pytorch", "neural network", "deep learning", "mạng neural"],
    "CodeDebugger": ["debug", "error", "fix code", "bug"],
    "CodeRefactorer": ["refactor", "clean code"],
    "ReproducibilityArtifactEngineer": ["reproducibility", "docker", "requirements.txt"],
    "FrameworkArchitect": ["framework", "architecture", "system design"],
    "FrameworkValidationArchitect": ["validate framework", "framework testing"],
    "HardwareresourceEstimator": ["gpu", "hardware", "memory estimate"],
    "ModelCapabilityRouter": ["which model", "model selection", "choose model"],
    "CrossDomainTransferHybridizationAgent": ["transfer learning", "cross domain", "domain adaptation"],
    
    # Visualization & Presentation
    "VisualCommunicationArchitect": ["plot", "chart", "visualize", "figure", "biểu đồ"],
    "TikZPlotter": ["tikz", "latex diagram"],
    "FigureGenerator": ["generate figure", "create chart"],
    "DiagramGenerator": ["mermaid", "flowchart", "sequence diagram", "sơ đồ"],
    "PresentationArchitect": ["presentation", "slides", "deck", "thuyết trình"],
    "PresentationGenerator": ["generate slides", "create presentation"],
    "HybridVisualizer": ["ascii diagram", "text diagram"],
    "ExplainabilityTranslator": ["explain", "lay summary", "simplify", "giải thích đơn giản"],
    "ResultVisualizer": ["visualize results", "result chart"],
    "ConceptVisualizer": ["visualize concept", "concept diagram"],
    
    # Review & Quality
    "PeerReviewer": ["review", "audit", "check", "verify", "đánh giá"],
    "ReviewerSimulator": ["simulate reviewer", "reviewer 2", "harsh review"],
    "HarshReviewer": ["harsh critique", "critical review"],
    "ReviewerStrategist": ["respond to reviewer", "rebuttal", "trả lời reviewer"],
    "CitationVerifier": ["citation check", "verify references", "check citations"],
    "CitationIntegrityAuditor": ["citation integrity", "reference audit"],
    "FeasibilityRigorSoundnessChecker": ["rigor", "soundness", "feasibility"],
    "BaselineBenchmarkNoveltyDefender": ["baseline", "benchmark", "defend novelty"],
    "JournalSelector": ["journal", "venue", "where to publish", "chọn tạp chí"],
    "EthicalComplianceGuard": ["ethics", "irb", "consent", "đạo đức nghiên cứu"],
    "DataPrivacyOfficer": ["privacy", "data protection", "bảo mật dữ liệu"],
    
    # Business & Enterprise
    "CostBenefitAnalyst": ["cost benefit", "roi", "tco", "budget", "chi phí lợi ích"],
    "SMETypologyArchitect": ["sme", "small business", "micro enterprise", "smb", "doanh nghiệp nhỏ"],
    "CompetitorAnalyst": ["competitor", "competitive analysis", "market", "đối thủ cạnh tranh"],
    "EntrepreneurialPsychProfiler": ["entrepreneur", "owner bias", "decision maker"],
    "HumanFactorCultureQuantifier": ["organizational culture", "culture audit", "human factor"],
    "FutureScenarioForecaster": ["business scenario", "future planning", "what if", "kịch bản tương lai"],
    
    # Innovation & Ideation
    "InnovationStrategist": ["innovate", "novel idea", "creative", "đổi mới"],
    "BrainstormingFacilitator": ["brainstorm", "ideation", "generate ideas", "động não"],
    "IdeaMutationDesignSpaceExplorer": ["design space", "explore options", "idea mutation"],
    "IdeaConcretizer": ["refine idea", "concretize", "cụ thể hóa ý tưởng"],
    "SystemDynamicsMapper": ["system dynamics", "feedback loop", "causal loop"],
    "MissingPartSuggester": ["missing", "suggest", "what's next", "thiếu gì"],
    "OmniThinker": ["complex reasoning", "deep think"],
    "HypothesisEngine": ["hypothesis", "giả thuyết"],
    "HypothesisGenerator": ["generate hypothesis", "tạo giả thuyết"],
    "ArgumentDefender": ["defend argument", "bảo vệ lập luận"],
    "CrossDisciplinaryConnector": ["cross discipline", "interdisciplinary", "liên ngành"],
}


def extract_role_goal_backstory(system_prompt: str, agent_name: str) -> Dict[str, str]:
    """Extract role, goal, and backstory from legacy system prompt."""
    
    # Default values
    result = {
        "role": f"{agent_name} Agent",
        "goal": "Assist with research tasks",
        "backstory": "An AI research assistant.",
    }
    
    if not system_prompt:
        return result
    
    # Try to find role (usually at the start)
    role_patterns = [
        r"#+\s*(?:SYSTEM\s+)?ROLE[:\s]*(.+?)(?:\n|$)",
        r"You are (?:a |an |the )?(.+?)(?:\.|,|\n)",
        r"Role[:\s]+(.+?)(?:\n|$)",
    ]
    for pattern in role_patterns:
        match = re.search(pattern, system_prompt, re.IGNORECASE)
        if match:
            result["role"] = match.group(1).strip()[:200]
            break
    
    # Try to find goal/objective
    goal_patterns = [
        r"#+\s*(?:OBJECTIVE|GOAL)[:\s]*(.+?)(?:\n\n|#{2,})",
        r"(?:Your |The )?(?:goal|objective|purpose) is to (.+?)(?:\.|$)",
        r"OBJECTIVE[:\s]+(.+?)(?:\n|$)",
    ]
    for pattern in goal_patterns:
        match = re.search(pattern, system_prompt, re.IGNORECASE | re.DOTALL)
        if match:
            result["goal"] = match.group(1).strip()[:500]
            break
    
    # Extract first paragraph as backstory if nothing specific found
    paragraphs = system_prompt.split("\n\n")
    if paragraphs:
        first_para = paragraphs[0].strip()
        if len(first_para) > 50:
            result["backstory"] = first_para[:1000]
    
    return result


def parse_yaml_agent(filepath: Path) -> Optional[Dict[str, Any]]:
    """Parse a YAML agent file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None


def convert_yaml_to_agent_definition(
    yaml_data: Dict[str, Any],
    agent_name: str,
) -> AgentDefinition:
    """Convert parsed YAML data to AgentDefinition."""
    
    system_prompt = yaml_data.get("system_prompt", "")
    extracted = extract_role_goal_backstory(system_prompt, agent_name)
    
    # Get domain
    domain = DOMAIN_MAPPING.get(agent_name, "Innovation & Ideation")
    is_lead = DOMAIN_LEADS.get(domain) == agent_name
    
    # Get tools
    tools = []
    tool_names = AGENT_TOOLS.get(agent_name, [])
    for tool_name in tool_names:
        tools.append(ToolDefinition(
            name=tool_name,
            description=f"Tool: {tool_name}",
            function_path=f"src.tools.{tool_name}",
        ))
    
    # Build triggers - use enriched keywords from MasterOrchestrator routing
    trigger_keywords = AGENT_TRIGGERS.get(agent_name, [agent_name.lower()])
    # Always include agent name as a keyword
    if agent_name.lower() not in [k.lower() for k in trigger_keywords]:
        trigger_keywords = [agent_name.lower()] + trigger_keywords
    
    triggers = TriggerCondition(
        keywords=trigger_keywords,
        priority=10 if is_lead else 5,
    )
    
    return AgentDefinition(
        name=agent_name,
        role=extracted["role"],
        goal=extracted["goal"],
        backstory=extracted["backstory"],
        domain=domain,
        is_domain_lead=is_lead,
        tools=tools,
        memory_type=MemoryType.BUFFER,
        triggers=triggers,
        system_prompt=system_prompt,  # Keep original for reference
    )


def migrate_all_agents(
    yaml_dir: str,
    output_dir: str,
    skip_master: bool = True,
) -> Dict[str, Any]:
    """
    Migrate all YAML agents to new format.
    
    Args:
        yaml_dir: Directory containing YAML agent files
        output_dir: Directory to write new agent definitions
        skip_master: Skip MasterOrchestrator (special handling)
    
    Returns:
        Summary of migration
    """
    yaml_path = Path(yaml_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = {
        "success": [],
        "failed": [],
        "skipped": [],
    }
    
    for yaml_file in yaml_path.glob("*.yaml"):
        agent_name = yaml_file.stem
        
        if skip_master and agent_name == "MasterOrchestrator":
            results["skipped"].append(agent_name)
            continue
        
        yaml_data = parse_yaml_agent(yaml_file)
        if not yaml_data:
            results["failed"].append(agent_name)
            continue
        
        try:
            agent_def = convert_yaml_to_agent_definition(yaml_data, agent_name)
            
            # Write as JSON
            output_file = output_path / f"{agent_name}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(agent_def.model_dump(), f, indent=2, ensure_ascii=False)
            
            results["success"].append(agent_name)
            
        except Exception as e:
            print(f"Error converting {agent_name}: {e}")
            results["failed"].append(agent_name)
    
    return results


def main():
    """Run migration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate YAML agents to new schema")
    parser.add_argument(
        "--yaml-dir",
        default="AI_Agents_YAML",
        help="Directory containing YAML agent files",
    )
    parser.add_argument(
        "--output-dir",
        default="agents",
        help="Output directory for new agent definitions",
    )
    parser.add_argument(
        "--agent",
        help="Migrate single agent by name",
    )
    
    args = parser.parse_args()
    
    print(f"Migrating agents from {args.yaml_dir} to {args.output_dir}")
    
    if args.agent:
        yaml_file = Path(args.yaml_dir) / f"{args.agent}.yaml"
        if not yaml_file.exists():
            print(f"Agent not found: {args.agent}")
            return
        
        yaml_data = parse_yaml_agent(yaml_file)
        agent_def = convert_yaml_to_agent_definition(yaml_data, args.agent)
        
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_file = output_path / f"{args.agent}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(agent_def.model_dump(), f, indent=2, ensure_ascii=False)
        
        print(f"Migrated {args.agent} -> {output_file}")
    else:
        results = migrate_all_agents(args.yaml_dir, args.output_dir)
        
        print(f"\n=== Migration Results ===")
        print(f"Success: {len(results['success'])}")
        print(f"Failed: {len(results['failed'])}")
        print(f"Skipped: {len(results['skipped'])}")
        
        if results["failed"]:
            print(f"\nFailed agents: {', '.join(results['failed'])}")


if __name__ == "__main__":
    main()
