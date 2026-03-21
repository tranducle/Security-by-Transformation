---
description: Citation Hallucination Audit Workflow
---
# Citation Hallucination Audit Workflow

This workflow guides the process of verifying that all claims made in a manuscript are supported by genuine, relevant citations, ensuring the AI has not hallucinated references or misrepresented their findings.

1. Ensure the `CitationHallucinationAuditor` agent is active or you assume its role.
2. Ensure you have the manuscript file (e.g., `manuscript.md`) and the bibliography (e.g., `references.bib` or `synthesized_papers.bib`).
3. Run the hallucination audit tool to gather all citation keys, extract their abstracts (via Crossref or local scraping), and map them against the exact sentences in the manuscript where they are cited:
   // turbo
   `python src/tools/audit_hallucinations.py`
4. The script generates a report in `4_Formal_Evaluation/Citation_Hallucination_Audit_Report.md`. Each entry initially contains a **[PENDING AI ANALYSIS]** marker.
5. Manually review (using the AI reasoning capabilities) the mapping between the "Manuscript Context" and the "Abstract". Determine if the relation is supported or not.
6. Write or modify the `update_report.py` script to bulk-replace the **[PENDING AI ANALYSIS]** tags with either **[SUPPORTED] <reasoning>** or **[UNVERIFIED] <reasoning>**.
   // turbo
   `python update_report.py`
7. Present the updated `Citation_Hallucination_Audit_Report.md` to the user to review the final hallucination audit status.
