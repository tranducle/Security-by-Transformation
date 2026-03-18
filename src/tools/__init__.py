# Tools package
from .auto_experiment_tools import (
    launch_autonomous,
    read_results_history,
    load_config,
)
from .literature_tools import (
    Paper,
    search_openalex,
    search_openalex_sync,
    search_semantic_scholar,
    search_semantic_scholar_sync,
    search_google_scholar,
    search_scopus,
    search_scopus_sync,
    format_papers_as_markdown,
    save_papers_to_json,
    LITERATURE_TOOLS,
)
from .writing_tools import (
    BibEntry,
    lookup_doi,
    doi_to_bibtex,
    parse_bibtex_file,
    find_missing_dois,
    generate_citation_key,
    write_markdown_section,
    WRITING_TOOLS,
)
from .analysis_tools import (
    StatResult,
    calculate_descriptive_stats,
    independent_t_test,
    correlation,
    generate_stats_report,
    ANALYSIS_TOOLS,
)
from .wolfram_tools import (
    WolframResult,
    AuditResult,
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
    clear_wolfram_cache,
    get_cache_stats,
)
from .sympy_tools import (
    verify_equation_sympy,
    compute_derivative_sympy,
    compute_integral_sympy,
    simplify_expression_sympy,
    SYMPY_TOOLS,
)
from .convert_to_markdown import (
    convert_file_to_markdown,
    convert_url_to_markdown,
    convert_multiple_files,
    get_supported_extensions,
    CONVERT_TOOLS,
)

# Sprint 3-5 tool modules
from . import epistemic_analysis_tools
from . import metric_operationalization_tools
from . import structural_analysis_tools
from . import ablation_error_tools
from . import deployment_assessment_tools
from . import knowledge_depth_tools

__all__ = [
    # Literature (Priority Order: OpenAlex -> GoogleScholar -> Scopus -> Semantic)
    "Paper",
    "search_openalex",
    "search_openalex_sync",
    "search_google_scholar",
    "search_scopus",
    "search_scopus_sync",
    "search_semantic_scholar",
    "search_semantic_scholar_sync", 
    "format_papers_as_markdown",
    "save_papers_to_json",
    "LITERATURE_TOOLS",
    # Writing
    "BibEntry",
    "lookup_doi",
    "doi_to_bibtex",
    "parse_bibtex_file",
    "find_missing_dois",
    "generate_citation_key",
    "write_markdown_section",
    "WRITING_TOOLS",
    # Analysis
    "StatResult",
    "calculate_descriptive_stats",
    "independent_t_test",
    "correlation",
    "generate_stats_report",
    "ANALYSIS_TOOLS",
    # Wolfram (Math Auditing)
    "WolframResult",
    "AuditResult",
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
    "distribution_property",
    "compute_probability",
    "compute_expectation",
    "statistical_test",
    "minimize",
    "maximize",
    "linear_optimization",
    "find_critical_points",
    "check_dimensions",
    "check_boundary_conditions",
    "sensitivity_analysis",
    "audit_mathematical_model",
    "WOLFRAM_TOOLS",
    # Cache utilities
    "clear_wolfram_cache",
    "get_cache_stats",
    # SymPy (Local Math Verification)
    "verify_equation_sympy",
    "compute_derivative_sympy",
    "compute_integral_sympy",
    "simplify_expression_sympy",
    "SYMPY_TOOLS",
    # Convert to Markdown (File Conversion)
    "convert_file_to_markdown",
    "convert_url_to_markdown",
    "convert_multiple_files",
    "get_supported_extensions",
    "CONVERT_TOOLS",
    # Auto Experiment (Autonomous Runner)
    "launch_autonomous",
    "read_results_history",
    "load_config",
    # Sprint 3-5 Tool Modules
    "epistemic_analysis_tools",
    "metric_operationalization_tools",
    "structural_analysis_tools",
    "ablation_error_tools",
    "deployment_assessment_tools",
    "knowledge_depth_tools",
]

