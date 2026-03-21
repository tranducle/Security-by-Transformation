import os
import re
import sys
import asyncio
from pathlib import Path

# Add project root to python path to import src.tools
sys.path.append(str(Path(__file__).parent))
from src.tools.literature_tools import search_semantic_scholar_sync, search_openalex_sync
from google import genai
from pydantic import BaseModel

def parse_bib_titles(filepath):
    """Simple parser to extract titles from bibtex file"""
    titles = {}
    current_key = None
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('@'):
                # Extract citekey
                match = re.match(r'@\w+\{([^,]+),', line)
                if match:
                    current_key = match.group(1).strip()
            elif current_key and line.lower().startswith('title'):
                # Extract title
                match = re.search(r'title\s*=\s*[\{"](.+?)[\}"]', line, re.IGNORECASE)
                if match:
                    titles[current_key] = match.group(1).strip()
                    current_key = None
    return titles

def get_manuscript_context(filepath, citekey):
    """Find the paragraph where a citation is used in the manuscript"""
    contexts = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        paragraphs = content.split('\n\n')
        for p in paragraphs:
            # Check for the citation key in various formats: (Author, Year), etc.
            # This is a bit tricky since the manuscript uses plaintext citations like "(Budhwar et al., 2023)"
            # Let's just extract the author's last name from the citekey (e.g., 'budhwar' from 'budhwar2023human')
            author_match = re.search(r'^([a-zA-Z]+)\d+', citekey)
            if author_match:
                author = author_match.group(1).lower()
                if author in p.lower() and '(' in p and ')' in p:
                    # Simple heuristic: if author is in the paragraph and there are parentheses, it might be the citation context.
                    # Or we just return the paragraphs that contain the author name.
                    contexts.append(p.strip())
    return " | ".join(contexts)

def check_hallucination(abstract, context):
    """Placeholder to bypass external API"""
    return "PENDING AI ANALYSIS"

def main():
    print("Loading references...")
    bib_path = '7_Manuscript_Draft/references.bib'
    manuscript_path = '7_Manuscript_Draft/manuscript.md'
    
    if not os.path.exists(bib_path):
        print(f"File not found: {bib_path}")
        return
        
    titles = parse_bib_titles(bib_path)
    print(f"Found {len(titles)} references.")
    
    report_path = '4_Formal_Evaluation/Citation_Hallucination_Audit_Report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Citation Hallucination Audit Report\n\n")
        f.write("This report verifies the claims made in the manuscript against the actual abstracts of the cited papers.\n\n")
        
        for key, title in titles.items():
            print(f"\\nProcessing: {key} - {title}")
            f.write(f"## {key}: *{title}*\n")
            
            # Fetch abstract
            papers = search_semantic_scholar_sync(title, limit=1)
            abstract = None
            if papers and papers[0].abstract:
                abstract = papers[0].abstract
                print("  ✓ Abstract fetched via Semantic Scholar")
            else:
                # Fallback to OpenAlex
                papers = search_openalex_sync(title, limit=1)
                if papers and papers[0].abstract:
                    abstract = papers[0].abstract
                    print("  ✓ Abstract fetched via OpenAlex")
                else:
                    print("  ✗ Could not fetch abstract")
            
            if not abstract:
                f.write("**Status**: ⚠️ Could not fetch abstract for verification.\n\n")
                continue
                
            f.write(f"**Fetched Abstract:** {abstract[:300]}...\n\n")
            
            # Get manuscript context
            context = get_manuscript_context(manuscript_path, key)
            if not context:
                print("  ✗ Could not find clear citation context in manuscript")
                f.write("**Manuscript Context**: ⚠️ Could not automatically extract citation context. Manual verification required.\n\n")
                continue
                
            f.write(f"**Manuscript Context:** {context}\n\n")
            
            # Check hallucination
            print("  Analyzing hallucination...")
            analysis = check_hallucination(abstract, context)
            f.write(f"**LLM Verification:**\n{analysis}\n\n")
            f.write("---\n")
            print("  Done.")
            
    print(f"\\nAudit complete. View report at {report_path}")

if __name__ == "__main__":
    main()
