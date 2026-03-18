"""
Tools Integration for LangGraph Research System.

Maps agents to available Python tools from src/tools/.
Returns ToolInfo dicts with resolved callables for auto-execution.
"""

import inspect
import sys
import logging
from typing import Dict, List, Callable, Any, Optional
from typing_extensions import TypedDict
from pathlib import Path

logger = logging.getLogger(__name__)

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# ============================================================================


class ToolInfo(TypedDict, total=False):
    name: str
    callable: Optional[Callable]
    description: str
    parameters: List[Dict[str, Any]]
    category: str
    auto_fillable: bool


# ============================================================================

# Import existing tools
try:
    from src.tools import (
        # Literature tools
        search_semantic_scholar_sync,
        search_google_scholar,
        search_openalex_sync,
        search_scopus_sync,
        format_papers_as_markdown,
        save_papers_to_json,
        LITERATURE_TOOLS,
        # Writing tools
        lookup_doi,
        doi_to_bibtex,
        parse_bibtex_file,
        find_missing_dois,
        generate_citation_key,
        write_markdown_section,
        WRITING_TOOLS,
        # Analysis tools
        calculate_descriptive_stats,
        independent_t_test,
        correlation,
        generate_stats_report,
        ANALYSIS_TOOLS,
        # Wolfram tools
        wolfram_query,
        verify_equation,
        simplify_expression,
        solve_equation,
        compute_derivative,
        verify_derivative,
        compute_integral,
        verify_integral,
        compute_limit,
        compute_series,
        matrix_operation,
        verify_matrix_equation,
        solve_linear_system,
        solve_ode,
        verify_ode_solution,
        distribution_property,
        compute_probability,
        compute_expectation,
        statistical_test,
        minimize,
        maximize,
        linear_optimization,
        find_critical_points,
        check_dimensions,
        check_boundary_conditions,
        sensitivity_analysis,
        audit_mathematical_model,
        WOLFRAM_TOOLS,
        # SymPy tools
        verify_equation_sympy,
        compute_derivative_sympy,
        compute_integral_sympy,
        simplify_expression_sympy,
        SYMPY_TOOLS,
        # Convert to Markdown tools
        convert_file_to_markdown,
        convert_url_to_markdown,
        convert_multiple_files,
        get_supported_extensions,
        CONVERT_TOOLS,
    )

    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False
    LITERATURE_TOOLS = []
    WRITING_TOOLS = []
    ANALYSIS_TOOLS = []
    WOLFRAM_TOOLS = []
    SYMPY_TOOLS = []
    CONVERT_TOOLS = []

# Auto Experiment tools (separate try block — optional dependency)
try:
    from src.tools.auto_experiment_tools import (
        launch_autonomous,
        read_results_history,
        load_config as load_experiment_config,
    )
    AUTO_EXPERIMENT_AVAILABLE = True
except ImportError:
    AUTO_EXPERIMENT_AVAILABLE = False

# Sprint 3-5 tool modules
try:
    from src.tools.epistemic_analysis_tools import (
        classify_epistemic_tier, detect_epistemic_jumps, map_certainty_levels,
        extract_causal_language, assess_causal_evidence,
        generate_epistemic_report, generate_causal_audit,
    )
    from src.tools.metric_operationalization_tools import (
        extract_metrics_used, audit_metric_semantics, detect_metric_masking,
        extract_concepts_and_metrics, assess_operationalization_validity,
        generate_gap_report,
    )
    from src.tools.structural_analysis_tools import (
        extract_claims_and_evidence, build_dependency_graph,
        detect_orphan_contributions, measure_concept_density,
        detect_notation_shifts, generate_cognitive_load_map,
        identify_rhetorical_motif, detect_narrative_fractures,
    )
    from src.tools.ablation_error_tools import (
        decompose_method_components, assess_ablation_coverage,
        detect_missing_ablations, build_error_taxonomy,
        map_error_to_component, generate_ablation_report,
    )
    from src.tools.deployment_assessment_tools import (
        score_deployment_friction, identify_adoption_barriers,
        inspect_temporal_validity, assess_dataset_provenance,
        generate_deployment_report, calculate_research_debt,
    )
    from src.tools.knowledge_depth_tools import (
        calculate_information_density, detect_redundant_passages,
        calculate_compression_ratio, distill_key_insights,
        generate_insight_report, extract_argument_chain,
        test_argument_robustness, extract_canonical_core,
        generate_one_page_summary,
    )
    SPRINT_TOOLS_AVAILABLE = True
except ImportError:
    SPRINT_TOOLS_AVAILABLE = False


# ============================================================================
# TOOL REGISTRY — single source of truth mapping name → callable
# ============================================================================


def _build_tool_registry() -> Dict[str, Optional[Callable]]:
    if not TOOLS_AVAILABLE:
        return {}
    registry = {
        # Literature
        "search_semantic_scholar_sync": search_semantic_scholar_sync,
        "search_google_scholar": search_google_scholar,
        "search_openalex_sync": search_openalex_sync,
        "search_scopus_sync": search_scopus_sync,
        "format_papers_as_markdown": format_papers_as_markdown,
        "save_papers_to_json": save_papers_to_json,
        # Writing
        "lookup_doi": lookup_doi,
        "doi_to_bibtex": doi_to_bibtex,
        "parse_bibtex_file": parse_bibtex_file,
        "find_missing_dois": find_missing_dois,
        "generate_citation_key": generate_citation_key,
        "write_markdown_section": write_markdown_section,
        # Analysis
        "calculate_descriptive_stats": calculate_descriptive_stats,
        "independent_t_test": independent_t_test,
        "correlation": correlation,
        "generate_stats_report": generate_stats_report,
        # Wolfram
        "wolfram_query": wolfram_query,
        "verify_equation": verify_equation,
        "simplify_expression": simplify_expression,
        "solve_equation": solve_equation,
        "compute_derivative": compute_derivative,
        "verify_derivative": verify_derivative,
        "compute_integral": compute_integral,
        "verify_integral": verify_integral,
        "compute_limit": compute_limit,
        "compute_series": compute_series,
        "matrix_operation": matrix_operation,
        "verify_matrix_equation": verify_matrix_equation,
        "solve_linear_system": solve_linear_system,
        "solve_ode": solve_ode,
        "verify_ode_solution": verify_ode_solution,
        "distribution_property": distribution_property,
        "compute_probability": compute_probability,
        "compute_expectation": compute_expectation,
        "statistical_test": statistical_test,
        "minimize": minimize,
        "maximize": maximize,
        "linear_optimization": linear_optimization,
        "find_critical_points": find_critical_points,
        "check_dimensions": check_dimensions,
        "check_boundary_conditions": check_boundary_conditions,
        "sensitivity_analysis": sensitivity_analysis,
        "audit_mathematical_model": audit_mathematical_model,
        # SymPy
        "verify_equation_sympy": verify_equation_sympy,
        "compute_derivative_sympy": compute_derivative_sympy,
        "compute_integral_sympy": compute_integral_sympy,
        "simplify_expression_sympy": simplify_expression_sympy,
        # Convert to Markdown
        "convert_file_to_markdown": convert_file_to_markdown,
        "convert_url_to_markdown": convert_url_to_markdown,
        "convert_multiple_files": convert_multiple_files,
        "get_supported_extensions": get_supported_extensions,
    }
    # Add auto experiment tools if available
    if AUTO_EXPERIMENT_AVAILABLE:
        registry["launch_autonomous"] = launch_autonomous
        registry["read_results_history"] = read_results_history
        registry["load_config"] = load_experiment_config
    # Add Sprint 3-5 tools if available
    if SPRINT_TOOLS_AVAILABLE:
        sprint_tools = {
            # Epistemic Analysis
            "classify_epistemic_tier": classify_epistemic_tier,
            "detect_epistemic_jumps": detect_epistemic_jumps,
            "map_certainty_levels": map_certainty_levels,
            "extract_causal_language": extract_causal_language,
            "assess_causal_evidence": assess_causal_evidence,
            "generate_epistemic_report": generate_epistemic_report,
            "generate_causal_audit": generate_causal_audit,
            # Metric Operationalization
            "extract_metrics_used": extract_metrics_used,
            "audit_metric_semantics": audit_metric_semantics,
            "detect_metric_masking": detect_metric_masking,
            "extract_concepts_and_metrics": extract_concepts_and_metrics,
            "assess_operationalization_validity": assess_operationalization_validity,
            "generate_gap_report": generate_gap_report,
            # Structural Analysis
            "extract_claims_and_evidence": extract_claims_and_evidence,
            "build_dependency_graph": build_dependency_graph,
            "detect_orphan_contributions": detect_orphan_contributions,
            "measure_concept_density": measure_concept_density,
            "detect_notation_shifts": detect_notation_shifts,
            "generate_cognitive_load_map": generate_cognitive_load_map,
            "identify_rhetorical_motif": identify_rhetorical_motif,
            "detect_narrative_fractures": detect_narrative_fractures,
            # Ablation & Error
            "decompose_method_components": decompose_method_components,
            "assess_ablation_coverage": assess_ablation_coverage,
            "detect_missing_ablations": detect_missing_ablations,
            "build_error_taxonomy": build_error_taxonomy,
            "map_error_to_component": map_error_to_component,
            "generate_ablation_report": generate_ablation_report,
            # Deployment Assessment
            "score_deployment_friction": score_deployment_friction,
            "identify_adoption_barriers": identify_adoption_barriers,
            "inspect_temporal_validity": inspect_temporal_validity,
            "assess_dataset_provenance": assess_dataset_provenance,
            "generate_deployment_report": generate_deployment_report,
            "calculate_research_debt": calculate_research_debt,
            # Knowledge Depth
            "calculate_information_density": calculate_information_density,
            "detect_redundant_passages": detect_redundant_passages,
            "calculate_compression_ratio": calculate_compression_ratio,
            "distill_key_insights": distill_key_insights,
            "generate_insight_report": generate_insight_report,
            "extract_argument_chain": extract_argument_chain,
            "test_argument_robustness": test_argument_robustness,
            "extract_canonical_core": extract_canonical_core,
            "generate_one_page_summary": generate_one_page_summary,
        }
        registry.update(sprint_tools)
    return registry

_TOOL_REGISTRY: Dict[str, Optional[Callable]] = _build_tool_registry()


# ============================================================================
# STARTUP VALIDATION — catch async mis-registration early
# ============================================================================

if TOOLS_AVAILABLE:
    import asyncio as _asyncio

    for _name, _func in _TOOL_REGISTRY.items():
        if _func is not None and inspect.iscoroutinefunction(_func):
            logger.warning(
                "ASYNC TOOL IN REGISTRY: '%s' is a coroutine function. "
                "The tool executor expects sync callables. Wrap it with a "
                "sync adapter (see writing_tools.py pattern).",
                _name,
            )


# ============================================================================
# PUBLIC HELPERS — used by tool_execution_node for grouping & replanning
# ============================================================================


def get_tool_category(tool_name: str) -> str:
    """Return the category string for a tool (e.g., 'literature', 'wolfram').

    Falls back to 'general' if tool not found in the category map.
    """
    return _TOOL_CATEGORY.get(tool_name, "general")


def get_tool_callable(tool_name: str) -> Optional[Callable]:
    """Return the callable for a tool from the registry.

    Returns None if tool not found or not available.
    """
    return _TOOL_REGISTRY.get(tool_name)


# ============================================================================
# TOOL CATEGORY MAPPING
# ============================================================================

_TOOL_CATEGORY: Dict[str, str] = {
    "search_semantic_scholar_sync": "literature",
    "search_google_scholar": "literature",
    "search_openalex_sync": "literature",
    "search_scopus_sync": "literature",
    "format_papers_as_markdown": "literature",
    "save_papers_to_json": "literature",
    "lookup_doi": "writing",
    "doi_to_bibtex": "writing",
    "parse_bibtex_file": "writing",
    "find_missing_dois": "writing",
    "generate_citation_key": "writing",
    "write_markdown_section": "writing",
    "calculate_descriptive_stats": "analysis",
    "independent_t_test": "analysis",
    "correlation": "analysis",
    "generate_stats_report": "analysis",
    "wolfram_query": "wolfram",
    "verify_equation": "wolfram",
    "simplify_expression": "wolfram",
    "solve_equation": "wolfram",
    "compute_derivative": "wolfram",
    "verify_derivative": "wolfram",
    "compute_integral": "wolfram",
    "verify_integral": "wolfram",
    "compute_limit": "wolfram",
    "compute_series": "wolfram",
    "matrix_operation": "wolfram",
    "verify_matrix_equation": "wolfram",
    "solve_linear_system": "wolfram",
    "solve_ode": "wolfram",
    "verify_ode_solution": "wolfram",
    "distribution_property": "wolfram",
    "compute_probability": "wolfram",
    "compute_expectation": "wolfram",
    "statistical_test": "wolfram",
    "minimize": "wolfram",
    "maximize": "wolfram",
    "linear_optimization": "wolfram",
    "find_critical_points": "wolfram",
    "check_dimensions": "wolfram",
    "check_boundary_conditions": "wolfram",
    "sensitivity_analysis": "wolfram",
    "audit_mathematical_model": "wolfram",
    "verify_equation_sympy": "sympy",
    "compute_derivative_sympy": "sympy",
    "compute_integral_sympy": "sympy",
    "simplify_expression_sympy": "sympy",
    "convert_file_to_markdown": "convert",
    "convert_url_to_markdown": "convert",
    "convert_multiple_files": "convert",
    "get_supported_extensions": "convert",
    "launch_autonomous": "auto_experiment",
    "read_results_history": "auto_experiment",
    "load_config": "auto_experiment",
    # Epistemic Analysis
    "classify_epistemic_tier": "epistemic",
    "detect_epistemic_jumps": "epistemic",
    "map_certainty_levels": "epistemic",
    "extract_causal_language": "epistemic",
    "assess_causal_evidence": "epistemic",
    "generate_epistemic_report": "epistemic",
    "generate_causal_audit": "epistemic",
    # Metric Operationalization
    "extract_metrics_used": "metric",
    "audit_metric_semantics": "metric",
    "detect_metric_masking": "metric",
    "extract_concepts_and_metrics": "metric",
    "assess_operationalization_validity": "metric",
    "generate_gap_report": "metric",
    # Structural Analysis
    "extract_claims_and_evidence": "structural",
    "build_dependency_graph": "structural",
    "detect_orphan_contributions": "structural",
    "measure_concept_density": "structural",
    "detect_notation_shifts": "structural",
    "generate_cognitive_load_map": "structural",
    "identify_rhetorical_motif": "structural",
    "detect_narrative_fractures": "structural",
    # Ablation & Error
    "decompose_method_components": "ablation",
    "assess_ablation_coverage": "ablation",
    "detect_missing_ablations": "ablation",
    "build_error_taxonomy": "ablation",
    "map_error_to_component": "ablation",
    "generate_ablation_report": "ablation",
    # Deployment Assessment
    "score_deployment_friction": "deployment",
    "identify_adoption_barriers": "deployment",
    "inspect_temporal_validity": "deployment",
    "assess_dataset_provenance": "deployment",
    "generate_deployment_report": "deployment",
    "calculate_research_debt": "deployment",
    # Knowledge Depth
    "calculate_information_density": "knowledge_depth",
    "detect_redundant_passages": "knowledge_depth",
    "calculate_compression_ratio": "knowledge_depth",
    "distill_key_insights": "knowledge_depth",
    "generate_insight_report": "knowledge_depth",
    "extract_argument_chain": "knowledge_depth",
    "test_argument_robustness": "knowledge_depth",
    "extract_canonical_core": "knowledge_depth",
    "generate_one_page_summary": "knowledge_depth",
}


# ============================================================================
# TOOL METADATA — collected from the *_TOOLS lists exported by src/tools/
# Build a name→metadata dict for fast lookup.
# ============================================================================


def _build_tool_metadata() -> Dict[str, Dict[str, Any]]:
    meta: Dict[str, Dict[str, Any]] = {}
    for tool_list in (
        LITERATURE_TOOLS,
        WRITING_TOOLS,
        ANALYSIS_TOOLS,
        WOLFRAM_TOOLS,
        SYMPY_TOOLS,
    ):
        for tool in tool_list:
            # Normalize name: the metadata lists may use short names like
            # "search_openalex" while the registry uses "search_openalex_sync".
            meta[tool["name"]] = tool
    return meta


_TOOL_METADATA: Dict[str, Dict[str, Any]] = (
    _build_tool_metadata() if TOOLS_AVAILABLE else {}
)


def _get_parameters_for_tool(tool_name: str) -> List[Dict[str, Any]]:
    meta = _TOOL_METADATA.get(tool_name)
    if meta and meta.get("parameters"):
        return meta["parameters"]

    # Short-name variants: metadata uses "search_openalex" not "search_openalex_sync"
    for short_name, m in _TOOL_METADATA.items():
        if tool_name.startswith(short_name) or short_name.startswith(tool_name):
            if m.get("parameters"):
                return m["parameters"]

    # Fall back to introspecting the callable
    func = _TOOL_REGISTRY.get(tool_name)
    if func is None:
        return []
    try:
        sig = inspect.signature(func)
        params = []
        for pname, p in sig.parameters.items():
            if pname in ("self", "cls"):
                continue
            param_info: Dict[str, Any] = {
                "name": pname,
                "type": "string",
                "description": pname.replace("_", " "),
                "required": p.default is inspect.Parameter.empty,
            }
            if p.default is not inspect.Parameter.empty:
                param_info["default"] = p.default
            params.append(param_info)
        return params
    except (ValueError, TypeError):
        return []


def _get_description_for_tool(tool_name: str) -> str:
    meta = _TOOL_METADATA.get(tool_name)
    if meta and meta.get("description"):
        return meta["description"]

    for short_name, m in _TOOL_METADATA.items():
        if tool_name.startswith(short_name) or short_name.startswith(tool_name):
            if m.get("description"):
                return m["description"]

    # Derive from docstring
    func = _TOOL_REGISTRY.get(tool_name)
    if func and func.__doc__:
        return func.__doc__.strip().split("\n")[0]
    return tool_name.replace("_", " ").title()


def _is_auto_fillable(params: List[Dict[str, Any]]) -> bool:
    return any(p.get("name") == "query" for p in params)


# ============================================================================
# AGENT TO TOOLS MAPPING
# ============================================================================


# Shared tool lists for DRY configuration
_ALL_4_SEARCH_TOOLS = [
    "search_openalex_sync",
    "search_google_scholar",
    "search_scopus_sync",
    "search_semantic_scholar_sync",
]
_CITATION_TOOLS = [
    "lookup_doi",
    "doi_to_bibtex",
]
_SEARCH_AND_CITE = _ALL_4_SEARCH_TOOLS + _CITATION_TOOLS

AGENT_TOOLS_MAP: Dict[str, List[str]] = {
    # ======================================================================
    # Research & Discovery agents
    # ======================================================================
    "LiteratureHunter": [
        *_ALL_4_SEARCH_TOOLS,
        "format_papers_as_markdown",
        "save_papers_to_json",
    ],
    "SemanticSearch": [*_ALL_4_SEARCH_TOOLS, "format_papers_as_markdown"],
    "GoogleScholarSearch": [*_ALL_4_SEARCH_TOOLS, "format_papers_as_markdown"],
    "OpenAlexSearch": [*_ALL_4_SEARCH_TOOLS, "format_papers_as_markdown"],
    "ScopusSearch": [*_ALL_4_SEARCH_TOOLS, "format_papers_as_markdown"],
    "DatasetResearchSpecialist": [*_ALL_4_SEARCH_TOOLS],
    "PriorArtNoveltyScanner": [
        *_ALL_4_SEARCH_TOOLS,
        "format_papers_as_markdown",
    ],
    # Research discovery agents — need search to find literature/gaps
    "SLRProtocolDroid": [*_ALL_4_SEARCH_TOOLS, "format_papers_as_markdown"],
    "GapScout": [*_ALL_4_SEARCH_TOOLS],
    "GapMapperResearchOpportunityExtractor": [*_ALL_4_SEARCH_TOOLS],
    "DeepSearchPlanner": [*_ALL_4_SEARCH_TOOLS],
    "JournalIdeaScout": [*_ALL_4_SEARCH_TOOLS],
    "ResearchLibrarian": [*_ALL_4_SEARCH_TOOLS, "format_papers_as_markdown"],
    # File conversion
    "FileToMarkdownConverter": [
        "convert_file_to_markdown",
        "convert_url_to_markdown",
        "convert_multiple_files",
        "get_supported_extensions",
    ],
    # ======================================================================
    # Writing agents — MUST search for citations when writing
    # ======================================================================
    "PaperWriter": [
        "write_markdown_section",
        *_SEARCH_AND_CITE,
    ],
    "PublicationReadyWriter": [
        "write_markdown_section",
        *_SEARCH_AND_CITE,
    ],
    "LatexPaperGenerator": [
        "write_markdown_section",
        *_SEARCH_AND_CITE,
    ],
    "ManuscriptReviser": [*_SEARCH_AND_CITE],
    "MethodologyArchitect": [*_SEARCH_AND_CITE],
    "GrantProposalStrategist": [*_SEARCH_AND_CITE],
    "AbstractTitleGenerator": [*_ALL_4_SEARCH_TOOLS],
    "PaperOutlineArchitect": [*_ALL_4_SEARCH_TOOLS],
    "WritingStylePolisher": [*_ALL_4_SEARCH_TOOLS],
    "CaseStudyArchivist": [*_SEARCH_AND_CITE],
    # Citation & Reference agents — need search for verification
    "ReferenceManager": [
        "parse_bibtex_file",
        "lookup_doi",
        "doi_to_bibtex",
        *_ALL_4_SEARCH_TOOLS,
    ],
    "BibTeXOptimizer": [
        "parse_bibtex_file",
        "find_missing_dois",
        "lookup_doi",
        "doi_to_bibtex",
        "generate_citation_key",
        *_ALL_4_SEARCH_TOOLS,
    ],
    "CitationIntegrityAuditor": [
        "parse_bibtex_file",
        "lookup_doi",
        *_ALL_4_SEARCH_TOOLS,
    ],
    "CitationVerifier": [
        "parse_bibtex_file",
        "lookup_doi",
        *_ALL_4_SEARCH_TOOLS,
    ],
    # ======================================================================
    # Synthesis agents — MUST search for citations when synthesizing
    # ======================================================================
    "DeepSynthesizer": [
        "write_markdown_section",
        *_SEARCH_AND_CITE,
    ],
    "DocumentSynthesizer": [
        "write_markdown_section",
        "convert_file_to_markdown",
        *_SEARCH_AND_CITE,
    ],
    "MultiSourceSynthesizer": [*_SEARCH_AND_CITE],
    "DialecticalSynthesizer": [*_SEARCH_AND_CITE],
    "SummarizerSynthesizer": [*_SEARCH_AND_CITE],
    "QualitativeCoder": [
        "write_markdown_section",
        *_SEARCH_AND_CITE,
    ],
    # ======================================================================
    # Analysis agents
    # ======================================================================
    "StatisticalAnalyst": [
        "calculate_descriptive_stats",
        "independent_t_test",
        "correlation",
        "generate_stats_report",
        "statistical_test",
    ],
    "DataMetricsAnalyst": [
        "calculate_descriptive_stats",
        "correlation",
        "generate_stats_report",
    ],
    # Math agents - Wolfram
    "WolframMathAuditor": [
        "wolfram_query",
        "verify_equation",
        "simplify_expression",
        "solve_equation",
        "compute_derivative",
        "verify_derivative",
        "compute_integral",
        "verify_integral",
        "compute_limit",
        "compute_series",
        "matrix_operation",
        "verify_matrix_equation",
        "solve_linear_system",
        "solve_ode",
        "verify_ode_solution",
        "check_dimensions",
        "check_boundary_conditions",
        "sensitivity_analysis",
        "audit_mathematical_model",
    ],
    "MathSymbolicSolver": [
        "wolfram_query",
        "verify_equation",
        "simplify_expression",
        "solve_equation",
        "compute_derivative",
        "compute_integral",
        "solve_ode",
        "verify_equation_sympy",
        "compute_derivative_sympy",
        "compute_integral_sympy",
        "simplify_expression_sympy",
    ],
    "MathProofAuditor": [
        "verify_equation",
        "simplify_expression",
        "compute_derivative",
        "verify_derivative",
        "compute_integral",
        "verify_integral",
        "verify_equation_sympy",
    ],
    "AppliedMathModeler": [
        "minimize",
        "maximize",
        "linear_optimization",
        "find_critical_points",
        "solve_equation",
        "wolfram_query",
    ],
    "MathArchitectureAnalyst": [
        "verify_equation",
        "check_dimensions",
        "simplify_expression",
    ],
    # Statistics agents - Wolfram
    "EconometricsModeler": [
        "statistical_test",
        "compute_probability",
        "compute_expectation",
    ],
    "CausalAnalyst": ["statistical_test"],
    "GameTheoryStrategist": ["wolfram_query", "solve_equation", "minimize", "maximize"],
    "NashEquilibriumStrategist": [
        "wolfram_query",
        "solve_equation",
        "solve_linear_system",
    ],
    # Coding & Engineering agents
    "DataPreprocessingEngineer": [
        "calculate_descriptive_stats",
        "generate_stats_report",
    ],
    # Methodology agents
    "ExperimentConductor": [
        "calculate_descriptive_stats",
        "independent_t_test",
        "correlation",
        "generate_stats_report",
    ],
    "SurveyDesignerAnalyst": ["calculate_descriptive_stats", "generate_stats_report"],
    # Auto Experiment agents
    "AutoExperimentRunner": [
        "launch_autonomous",
        "read_results_history",
        "load_config",
    ],
    # ==========================================================================
    # Sprint 3-5 agents — epistemic, metric, structural, ablation, deployment,
    # knowledge depth tools
    # ==========================================================================
    # Existing agents that use new Sprint 3-5 tools
    "EpistemicBoundaryMapper": [
        "classify_epistemic_tier",
        "detect_epistemic_jumps",
        "map_certainty_levels",
        "generate_epistemic_report",
    ],
    "CausalClaimGatekeeper": [
        "extract_causal_language",
        "assess_causal_evidence",
        "generate_causal_audit",
    ],
    "MetricSemanticsAuditor": [
        "extract_metrics_used",
        "audit_metric_semantics",
        "extract_concepts_and_metrics",
        "generate_gap_report",
    ],
    "OperationalizationGapDetector": [
        "extract_metrics_used",
        "assess_operationalization_validity",
        "extract_concepts_and_metrics",
    ],
    "ContributionDependencyGrapher": [
        "extract_claims_and_evidence",
        "build_dependency_graph",
        "detect_orphan_contributions",
    ],
    "ReaderCognitiveLoadSimulator": [
        "measure_concept_density",
        "detect_notation_shifts",
        "generate_cognitive_load_map",
    ],
    "RhetoricalSkeletonExtractor": [
        "identify_rhetorical_motif",
        "detect_narrative_fractures",
    ],
    "AblationCoverageOracle": [
        "decompose_method_components",
        "assess_ablation_coverage",
        "detect_missing_ablations",
        "generate_ablation_report",
    ],
    "ErrorTaxonomyMiner": [
        "build_error_taxonomy",
        "map_error_to_component",
        "generate_ablation_report",
    ],
    "DeploymentFrictionEstimator": [
        "score_deployment_friction",
        "identify_adoption_barriers",
        "calculate_research_debt",
        "generate_deployment_report",
    ],
    "TemporalValidityInspector": [
        "inspect_temporal_validity",
    ],
    "DatasetProvenanceExaminer": [
        "assess_dataset_provenance",
    ],
    # New Sprint 4-5 agents
    "SOTAInflationDetector": [
        "extract_metrics_used",
        "audit_metric_semantics",
        "detect_metric_masking",
    ],
    "KnowledgeCompressionAuditor": [
        "calculate_information_density",
        "detect_redundant_passages",
        "calculate_compression_ratio",
    ],
    "InsightDistiller": [
        "distill_key_insights",
        "generate_insight_report",
    ],
    "ArgumentLoadTester": [
        "extract_argument_chain",
        "test_argument_robustness",
    ],
    "CanonicalCoreExtractor": [
        "extract_canonical_core",
        "generate_one_page_summary",
    ],
    # Agents with no Python tools (prompt-only): ScholarlyRiskPortfolioManager,
    # IntellectualHonestyEnforcer, ScientificFalsifiabilityEngine,
    # ConceptualBridgeBuilder, ResearchProgramSeeder, CounterIntuitionDetector,
    # ScientificLegacyEstimator
    # --- Sprint 6: Paper Hardening Agents ---
    "PaperIdentityArchitect": [
        "identify_rhetorical_motif",
        "extract_claims_and_evidence",
        "calculate_information_density",
    ],
    "NoveltyDeltaCartographer": [
        "classify_epistemic_tier",
        "extract_claims_and_evidence",
        "build_dependency_graph",
    ],
    "HiddenAssumptionAssassin": [
        "classify_epistemic_tier",
        "detect_epistemic_jumps",
        "extract_causal_language",
        "assess_causal_evidence",
    ],
    "ReviewerWarGamer": [
        "extract_claims_and_evidence",
        "classify_epistemic_tier",
        "detect_epistemic_jumps",
        "assess_causal_evidence",
    ],
    "NegativeResultsAlchemist": [
        "build_error_taxonomy",
        "map_error_to_component",
        "decompose_method_components",
    ],
    "MinimalDecisiveExperimentDesigner": [
        "decompose_method_components",
        "assess_ablation_coverage",
        "detect_missing_ablations",
        "extract_claims_and_evidence",
    ],
    "ClaimEvidenceLedger": [
        "extract_claims_and_evidence",
        "classify_epistemic_tier",
        "assess_causal_evidence",
        "detect_epistemic_jumps",
    ],
    "GeneralizationBreaker": [
        "score_deployment_friction",
        "identify_adoption_barriers",
        "inspect_temporal_validity",
        "assess_dataset_provenance",
    ],
    "CrossDisciplinaryImportSmuggler": [
        "extract_concepts_and_metrics",
        "calculate_information_density",
    ],
    "ReproducibilityForensicsInvestigator": [
        "score_deployment_friction",
        "decompose_method_components",
        "calculate_information_density",
        "detect_redundant_passages",
    ],
    # --- Sprint 7: Batch 2 Agents ---
    "CitationVulnerabilityScanner": [
        "extract_claims_and_evidence",
        "classify_epistemic_tier",
        "calculate_information_density",
    ],
    "StatisticalSanityProsecutor": [
        "extract_claims_and_evidence",
        "classify_epistemic_tier",
        "detect_epistemic_jumps",
    ],
    "MethodologicalConfounderHunter": [
        "decompose_method_components",
        "assess_ablation_coverage",
        "detect_missing_ablations",
        "assess_dataset_provenance",
    ],
    "BaselineFairnessAuditor": [
        "extract_claims_and_evidence",
        "decompose_method_components",
        "detect_missing_ablations",
    ],
    "FigureArgumentArchitect": [
        "extract_claims_and_evidence",
        "decompose_method_components",
        "calculate_information_density",
    ],
    "TerminologyDriftDetector": [
        "calculate_information_density",
        "detect_redundant_passages",
        "extract_concepts_and_metrics",
    ],
    "ScopeCreepGuillotine": [
        "extract_claims_and_evidence",
        "build_dependency_graph",
        "calculate_information_density",
        "detect_redundant_passages",
    ],
    "CounterfactualReframer": [
        "decompose_method_components",
        "assess_ablation_coverage",
        "detect_missing_ablations",
        "extract_claims_and_evidence",
    ],
    "ScholarlyToneEqualizer": [
        "classify_epistemic_tier",
        "detect_epistemic_jumps",
        "extract_claims_and_evidence",
        "extract_causal_language",
    ],
    "SubmissionPersonaSimulator": [
        "extract_claims_and_evidence",
        "classify_epistemic_tier",
        "detect_epistemic_jumps",
        "calculate_information_density",
    ],
    "TableCompressionEngine": [
        "calculate_information_density",
        "detect_redundant_passages",
        "extract_claims_and_evidence",
    ],
    "EquationReadabilityInspector": [
        "calculate_information_density",
        "detect_redundant_passages",
        "decompose_method_components",
    ],
    "AppendixValueSorter": [
        "extract_claims_and_evidence",
        "calculate_information_density",
        "detect_redundant_passages",
        "build_dependency_graph",
    ],
    # ======================================================================
    # PPGA System (Paper-to-Program Grant Architect)
    # ======================================================================
    "PaperToProgramGrantArchitect": [*_ALL_4_SEARCH_TOOLS],
    "PaperToProgramDistiller": [*_ALL_4_SEARCH_TOOLS],
    "GrantabilityDiagnostician": ["search_openalex_sync"],
    "SponsorFitCartographer": ["search_openalex_sync", "search_google_scholar"],
    "ProgramExpansionArchitect": [*_ALL_4_SEARCH_TOOLS],
    "SpecificAimsComposer": ["search_openalex_sync"],
    "InnovationSignificanceReframer": ["search_openalex_sync"],
    "WorkplanMilestoneEngineer": [],
    "BroaderImpactTranslator": [],
    "ProposalStressTester": [],
    "PreliminaryEvidenceEstimator": [],
    "FundabilityGapAnalyzer": [],
    "SponsorLanguageMutator": [],
    "WhiteSpaceOpportunityMiner": [*_ALL_4_SEARCH_TOOLS],
    "ProgramOfficerBriefComposer": [],
    "AimsDependencyBreaker": [],
    "BroaderImpactsConstructor": [],
    "ReviewCriteriaReverseEngineer": [],
    "ProposalPaperContinuityKeeper": [],
    "GrantPortfolioPlanner": ["search_openalex_sync"],
    # Default - no special tools
    "_default": [],
    # ═══ Cyber Paper Hardening Agents ═══
    # Layer 1: Threat Realism
    "ThreatModelRealityAuditor": [],
    "AdaptiveAttackerSimulatorV2": [],
    "DefenseEvasionPressureTester": [],
    "KillChainCoverageMapper": [],
    # Layer 2: Data Integrity
    "SecurityDatasetProvenanceForensics": ["search_openalex_sync", "search_semantic_scholar_sync"],
    "TelemetryFidelityInspector": [],
    "LeakageHunterCyberPipelines": [],
    "GroundTruthIntegrityExaminer": [],
    # Layer 3: SOC Operations
    "SOCWorkflowCompatibilityAnalyzer": [],
    "FalsePositiveBurdenEstimator": [],
    "MeanTimeToDefendTranslator": [],
    "AlertExplainabilityAuditor": [],
    # Layer 4: SME Realism
    "SMEResourceRealityChecker": [],
    "CyberHygieneDependencyDetector": [],
    "SMEIncentiveAdoptionFrictionMapper": [],
    "ComplianceToControlBridgeBuilder": [],
    # Layer 5: AI-for-Cyber Rigor
    "SecurityAIClaimBoundaryEnforcer": [],
    "ModelDriftThreatDriftCoupler": [],
    "HumanAITrustCalibrationAnalyzer": [],
    "SecurityValueRealizationAuditor": [],
    # ═══════════════════════════════════════════════════════════════════
    # Base agents — backfilled to ensure full ROUTING_RULES coverage
    # ═══════════════════════════════════════════════════════════════════
    # Strategy & Operations
    "StrategicArchitect": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ResearchPlanGenerator": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ProjectStateKeeper": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ProgressTracker": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ProjectPlanner": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "LogicStrategist": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "Scoper": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ResearchScoper": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ResourceConstraintAuditor": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    # Research & Discovery
    "GeneralWebSearcher": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "search_scopus_sync", "format_papers_as_markdown"],
    # Methodology & Analysis
    "MethodologyExperimentDesigner": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "CausalIdentificationStrategist": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    # Security & Risk
    "CyberSecurityArchitect": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "AdversarialAttackSimulator": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ThreatModeler": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "SaaSShadowITCartographer": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ProtocolNetworkSemanticsVerifier": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "CryptoProtocolVerifier": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "IncidentReadinessPlaybookGenerator": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "MinViableSecurityArchitect": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "SupplyChainRiskAnalyst": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "CyberInsuranceAnalyst": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "CyberInsuranceActuary": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "RegulatoryComplianceAuditor": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "NetworkTrafficModeler": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "RedTeamEthicsDualUseGuard": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "SecurityStandardsChecker": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    # Writing & Synthesis
    "DailySummarizer": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    # Coding & Engineering
    "CoderReproAgent": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "PyTorchImplementer": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ReproducibilityArtifactEngineer": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "FrameworkArchitect": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "FrameworkValidationArchitect": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "HardwareresourceEstimator": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "ModelCapabilityRouter": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "FileIntegrator": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "CrossDomainTransferHybridizationAgent": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    # Visualization
    "VisualCommunicationArchitect": ["search_openalex_sync", "format_papers_as_markdown"],
    "TikZPlotter": ["search_openalex_sync", "format_papers_as_markdown"],
    "FigureGenerator": ["search_openalex_sync", "format_papers_as_markdown"],
    "ResultVisualizer": ["search_openalex_sync", "format_papers_as_markdown"],
    "HybridVisualizer": ["search_openalex_sync", "format_papers_as_markdown"],
    "PresentationArchitect": ["search_openalex_sync", "format_papers_as_markdown"],
    "PresentationGenerator": ["search_openalex_sync", "format_papers_as_markdown"],
    "ExplainabilityTranslator": ["search_openalex_sync", "format_papers_as_markdown"],
    # Review & Quality
    "PeerReviewer": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ReviewerSimulator": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "HarshReviewer": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ReviewerStrategist": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "FeasibilityRigorSoundnessChecker": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "JournalSelector": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "EthicalComplianceGuard": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "AgentSystemArchitect": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "BaselineBenchmarkNoveltyDefender": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "CounterIntuitionDetector": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "DataPrivacyOfficer": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "IntellectualHonestyEnforcer": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "PromptOptimizer": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ScholarlyRiskPortfolioManager": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ScientificFalsifiabilityEngine": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ScientificLegacyEstimator": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "SelfImprover": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "SystemQualityMonitor": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    # Business & Enterprise
    "SMETypologyArchitect": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "CostBenefitAnalyst": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "EntrepreneurialPsychProfiler": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "HumanFactorCultureQuantifier": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    "FutureScenarioForecaster": ["search_openalex_sync", "search_google_scholar", "format_papers_as_markdown"],
    # Innovation & Ideation
    "InnovationStrategist": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "BrainstormingFacilitator": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "IdeaMutationDesignSpaceExplorer": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "SystemDynamicsMapper": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "MissingPartSuggester": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "OmniThinker": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ConceptualBridgeBuilder": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
    "ResearchProgramSeeder": ["search_openalex_sync", "search_google_scholar", "search_semantic_scholar_sync", "format_papers_as_markdown"],
}


# ============================================================================
# PUBLIC API
# ============================================================================


def get_tools_for_agent(agent_name: str) -> List[ToolInfo]:
    """Returns resolved ToolInfo list (with callables) for the given agent."""
    tool_names = AGENT_TOOLS_MAP.get(agent_name, AGENT_TOOLS_MAP["_default"])
    if not tool_names or not TOOLS_AVAILABLE:
        return []

    tools: List[ToolInfo] = []
    for tname in tool_names:
        func = _TOOL_REGISTRY.get(tname)
        if func is None:
            logger.warning(
                "Tool '%s' for agent '%s' not found in registry — skipping",
                tname,
                agent_name,
            )
            continue

        params = _get_parameters_for_tool(tname)
        tools.append(
            ToolInfo(
                name=tname,
                callable=func,
                description=_get_description_for_tool(tname),
                parameters=params,
                category=_TOOL_CATEGORY.get(tname, "unknown"),
                auto_fillable=_is_auto_fillable(params),
            )
        )

    return tools


def get_tool_names_for_agent(agent_name: str) -> List[str]:
    return AGENT_TOOLS_MAP.get(agent_name, AGENT_TOOLS_MAP["_default"])


def get_tool_function(tool_name: str) -> Optional[Callable]:
    return _TOOL_REGISTRY.get(tool_name)


def get_tool_info(tool_name: str) -> Optional[ToolInfo]:
    func = _TOOL_REGISTRY.get(tool_name)
    if func is None:
        return None
    params = _get_parameters_for_tool(tool_name)
    return ToolInfo(
        name=tool_name,
        callable=func,
        description=_get_description_for_tool(tool_name),
        parameters=params,
        category=_TOOL_CATEGORY.get(tool_name, "unknown"),
        auto_fillable=_is_auto_fillable(params),
    )


def list_all_tools() -> List[Dict[str, Any]]:
    """List all available tools with their metadata."""
    all_tools = []

    if TOOLS_AVAILABLE:
        all_tools.extend(LITERATURE_TOOLS)
        all_tools.extend(WRITING_TOOLS)
        all_tools.extend(ANALYSIS_TOOLS)
        all_tools.extend(WOLFRAM_TOOLS)
        all_tools.extend(SYMPY_TOOLS)
        all_tools.extend(CONVERT_TOOLS)

    return all_tools


def get_tools_docs() -> str:
    """Get documentation for all available tools."""
    lines = ["# Available Python Tools\n"]

    if not TOOLS_AVAILABLE:
        lines.append("[WARN] Tools not available. Check imports in src/tools/\n")
        return "\n".join(lines)

    for category, tools in [
        ("Literature", LITERATURE_TOOLS),
        ("Writing", WRITING_TOOLS),
        ("Analysis", ANALYSIS_TOOLS),
        ("Wolfram Math", WOLFRAM_TOOLS),
        ("SymPy Math", SYMPY_TOOLS),
        ("Convert", CONVERT_TOOLS),
    ]:
        lines.append(f"\n## {category} Tools\n")
        for tool in tools:
            lines.append(f"### `{tool['name']}`")
            lines.append(f"- {tool['description']}")
            lines.append("- Parameters:")
            for param in tool.get("parameters", []):
                req = "required" if param.get("required") else "optional"
                lines.append(
                    f"  - `{param['name']}` ({param['type']}, {req}): {param['description']}"
                )
            lines.append("")

    return "\n".join(lines)


def print_tools_status():
    """Print status of tool availability."""
    logger.info("[TOOLS] STATUS")
    logger.info("Tools available: %s", "Yes" if TOOLS_AVAILABLE else "No")

    if TOOLS_AVAILABLE:
        logger.info(
            "Literature: %d, Writing: %d, Analysis: %d, Wolfram: %d, SymPy: %d",
            len(LITERATURE_TOOLS),
            len(WRITING_TOOLS),
            len(ANALYSIS_TOOLS),
            len(WOLFRAM_TOOLS),
            len(SYMPY_TOOLS),
        )
