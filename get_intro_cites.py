import sys
import os
sys.path.append(os.getcwd())
try:
    from src.tools.literature_tools import search_openalex_sync, doi_to_bibtex
    # Search for Prompt Injection
    pi_results = search_openalex_sync("prompt injection LLM security", limit=3)
    # Search for STRIDE threat modeling
    stride_results = search_openalex_sync("STRIDE threat modeling frameworks", limit=3)
    
    with open("7_Manuscript_Draft/references.bib", "a") as f:
        for r in pi_results + stride_results:
            if 'doi' in r and r['doi']:
                bib = doi_to_bibtex(r['doi'])
                if bib:
                    f.write(bib + "\n\n")
                    print(f"Added: {r.get('title', 'Unknown')}")
    print("Citation search complete.")
except Exception as e:
    print(f"Error: {e}")
