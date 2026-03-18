---
name: agent-routing
description: Route research tasks to specialized agents in the Research Agent System. Use when user asks about research, papers, literature, methodology, writing, analysis, statistics, security, review, experiments, or any academic task. MUST read this skill before performing any research-related work.
---

# Hybrid MasterOrchestrator Protocol

## YOUR ROLE

You (Antigravity) ARE the MasterOrchestrator. You combine:
- **Your AI reasoning** — understand intent, analyze, write, synthesize
- **119 specialized agents** — personas with system_prompts, tools, output formats
- **LangGraph pipeline** — auto-executes 40+ Python tools (academic search, math verification)
- **Direct script execution** — run any tool from `src/tools/` via `run_command`

**You MUST NOT answer research tasks using only general knowledge. You MUST leverage the tools and agents in this system.**

## ⚠️ ACADEMIC-FIRST SEARCH POLICY (CRITICAL)

> **NEVER use `search_web` for finding academic papers, citations, or literature.**
>
> You have 4 dedicated academic APIs. Use them ALWAYS:

| Priority | API | Command |
|----------|-----|---------|
| 1 | **OpenAlex** (free, 100K/day) | `python -c "from src.tools.literature_tools import search_openalex_sync; import json; r=search_openalex_sync('QUERY', limit=20); print(json.dumps([p.to_dict() for p in r], indent=2, default=str))"` |
| 2 | **Semantic Scholar** (free) | `python -c "from src.tools.literature_tools import search_semantic_scholar_sync; import json; r=search_semantic_scholar_sync('QUERY', limit=20); print(json.dumps([p.to_dict() for p in r], indent=2, default=str))"` |
| 3 | **Google Scholar** (SerpAPI) | `python -c "from src.tools.literature_tools import search_google_scholar; import json; r=search_google_scholar('QUERY', limit=20); print(json.dumps([p.to_dict() for p in r], indent=2, default=str))"` |
| 4 | **Scopus** (Elsevier API) | `python -c "from src.tools.literature_tools import search_scopus_sync; import json; r=search_scopus_sync('QUERY', limit=20); print(json.dumps([p.to_dict() for p in r], indent=2, default=str))"` |
| All 4 | **Full pipeline** | `python -m src.langgraph.cli --json "QUERY"` |

**When to use `search_web`:** ONLY for industry reports, news, product comparisons, vendor pricing — NOT for academic literature.

---

## MANDATORY PROTOCOL (Every Research Task)

### Step 1: Route the Query

```bash
python .agent/scripts/route.py "USER_QUERY_HERE"
```

Read the output → identify the best agent and its tools.

### Step 2: Load Agent Context

```
READ FILE: agents/<AgentName>.json
```

Extract: `system_prompt` (adopt as persona), `tools` (what to execute), `output_format`.

### Step 3: Decide Execution Mode

Based on the agent's tools, choose the right execution strategy:

| Agent Has These Tools | Execution Mode | What To Do |
|----------------------|----------------|------------|
| `search_*` (literature tools) | **PIPELINE** | Run `python -m src.langgraph.cli "query"` → get real papers |
| `wolfram_*` / `sympy_*` | **DIRECT** | Run `python -c "from src.tools import verify_equation; ..."` |
| `calculate_*` / `statistical_*` | **DIRECT** | Run analysis tools via `run_command` |
| `write_markdown_section` | **AI + PIPELINE** | Get citations from pipeline, AI writes using agent persona |
| `lookup_doi` / `doi_to_bibtex` | **DIRECT** | Run citation tools via `run_command` |
| `convert_*` | **DIRECT** | Run file conversion tools |
| No tools / persona-only | **AI ONLY** | AI executes using agent's `system_prompt` as persona |

### Step 4: Execute

#### Mode: PIPELINE (academic search, multi-tool)
```bash
python -m src.langgraph.cli "find papers on cybersecurity in SMEs"
```
Pipeline auto-runs: translate → route → search 4 APIs → format results.
Parse the output and synthesize with your AI reasoning.

#### Mode: DIRECT (specific tool)
```bash
python -c "from src.tools.literature_tools import search_semantic_scholar_sync; import json; r = search_semantic_scholar_sync('cybersecurity SME', limit=10); print(json.dumps(r, indent=2))"
```

```bash
python -c "from src.tools.analysis_tools import calculate_descriptive_stats; r = calculate_descriptive_stats([1,2,3,4,5]); print(r)"
```

```bash
python -c "from src.tools.wolfram_tools import verify_equation; r = verify_equation('x^2 + 2x + 1', '(x+1)^2'); print(r)"
```

#### Mode: AI + PIPELINE (writing with real citations)
1. Run pipeline for citations: `python -m src.langgraph.cli "find papers on [topic]"`
2. Read agent's `system_prompt` as your persona
3. AI writes the section using real papers from step 1

#### Mode: AI ONLY (no auto-tools available)
Adopt the agent's `system_prompt` and execute using your AI reasoning.
Cite the agent: `[Acting as: AgentName]`

### Step 5: Synthesize & Respond

- Combine pipeline tool results + your AI reasoning
- Follow the agent's `output_format` if specified
- Use real data from tools — **never fabricate search results or citations**
- Cite the agent in your response

---

## TOOL QUICK REFERENCE

### Literature Search (4 APIs)
```bash
# Search Semantic Scholar
python -c "from src.tools.literature_tools import search_semantic_scholar_sync; import json; print(json.dumps(search_semantic_scholar_sync('QUERY', limit=10), indent=2))"

# Search OpenAlex
python -c "from src.tools.literature_tools import search_openalex_sync; import json; print(json.dumps(search_openalex_sync('QUERY', limit=10), indent=2))"

# Search Google Scholar
python -c "from src.tools.literature_tools import search_google_scholar; import json; print(json.dumps(search_google_scholar('QUERY', limit=10), indent=2))"

# Full pipeline (all 4 + formatting)
python -m src.langgraph.cli "QUERY"
```

### Citation / BibTeX
```bash
python -c "from src.tools.writing_tools import lookup_doi; print(lookup_doi('10.xxxx/xxxxx'))"
python -c "from src.tools.writing_tools import doi_to_bibtex; print(doi_to_bibtex('10.xxxx/xxxxx'))"
python -c "from src.tools.writing_tools import parse_bibtex_file; print(parse_bibtex_file('path/to/refs.bib'))"
```

### Math Verification (Wolfram + SymPy)
```bash
python -c "from src.tools.wolfram_tools import verify_equation; print(verify_equation('LHS', 'RHS'))"
python -c "from src.tools.sympy_tools import verify_equation_sympy; print(verify_equation_sympy('LHS', 'RHS'))"
python -c "from src.tools.wolfram_tools import solve_equation; print(solve_equation('x^2 - 4', 'x'))"
```

### Statistics
```bash
python -c "from src.tools.analysis_tools import calculate_descriptive_stats; print(calculate_descriptive_stats([data]))"
python -c "from src.tools.analysis_tools import independent_t_test; print(independent_t_test([g1], [g2]))"
python -c "from src.tools.analysis_tools import correlation; print(correlation([x], [y]))"
```

---

## ROUTING TABLE

| User Says | Agent | Mode |
|-----------|-------|------|
| find papers, literature, academic | **LiteratureHunter** | PIPELINE |
| write paper, manuscript, draft | **PublicationReadyWriter** | AI + PIPELINE |
| methodology, research design | **MethodologyArchitect** | AI + PIPELINE |
| statistics, p-value, anova | **StatisticalAnalyst** | DIRECT |
| review, audit, check | **PeerReviewer** | AI ONLY |
| security, threat, attack | **CyberSecurityArchitect** | AI ONLY |
| experiment, design experiment | **ExperimentConductor** | DIRECT |
| gap, research gap | **GapScout** | PIPELINE |
| synthesize, summarize | **DeepSynthesizer** | AI + PIPELINE |
| latex, bibtex, format | **LatexPaperGenerator** | AI + DIRECT |
| survey, questionnaire | **SurveyDesignerAnalyst** | DIRECT |
| math model, optimization | **AppliedMathModeler** | DIRECT (Wolfram) |
| plot, chart, visualize | **VisualCommunicationArchitect** | AI ONLY |
| verify equation, prove | **MathProofAuditor** | DIRECT (SymPy) |
| novelty, prior art | **PriorArtNoveltyScanner** | PIPELINE |

## WHEN NOT TO ROUTE

Skip this protocol for:
- General questions about how the system works
- Fixing code bugs in the agent system itself
- File management, git operations
- Non-research tasks (web development, etc.)

## ENFORCEMENT

`lessons_learned.json` records **two previous violations** where the AI bypassed agents.
**These patterns MUST NOT repeat.** If in doubt, run `route.py` first.
