import requests
import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIG ---
# API keys loaded securely from environment
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")
SEMANTIC_SCHOLAR_KEY = os.getenv("SEMANTIC_SCHOLAR_KEY", "")

if not SERPAPI_KEY and not SEMANTIC_SCHOLAR_KEY:
    print("⚠️  Warning: No API keys found. Run 'python setup_api_keys.py' first.")

QUERIES = [
    "Ward Cunningham technical debt software engineering",
    "Zaydi 2024 SME cybersecurity dynamic risk management",
    "Marican 2022 SME cybersecurity challenges barriers complexity"
]
OUTPUT_DIR = "2_Literature_Review/Section4_Citations"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

BIB_FILE = os.path.join(OUTPUT_DIR, "section4_references.bib")
INSIGHTS_FILE = os.path.join(OUTPUT_DIR, "section4_search_results.md")

def get_bibtex_from_scholar(result):
    title = result.get('title', 'Unknown Title')
    pub_info = result.get('publication_info', {})
    summary = pub_info.get('summary', '')
    link = result.get('link', '')
    
    year = "2024"
    author_first = "Scholar"
    try:
        match = re.search(r'\b(19|20)\d{2}\b', summary)
        if match:
            year = match.group(0)
        
        if ' - ' in summary:
            author_part = summary.split(' - ')[0]
            author_first = author_part.split(',')[0].split()[-1]
    except:
        pass

    citation_key = "".join(x for x in f"{author_first}{year}{title.split()[0]}" if x.isalnum())
    
    bib = f"@article{{{citation_key},\n"
    bib += f"  title = {{{title}}},\n"
    bib += f"  author = {{{summary.split(' - ')[0].strip()}}},\n"
    bib += f"  journal = {{Google Scholar Index}},\n"
    bib += f"  year = {{{year}}},\n"
    bib += f"  url = {{{link}}}"
    bib += "}\n"
    return bib

def search_scholar(query):
    print(f"Searching Google Scholar for: {query}...")
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5,
        "as_ylo": 2018
    }
    try:
        resp = requests.get("https://serpapi.com/search", params=params)
        if resp.status_code == 200:
            return resp.json().get('organic_results', [])
        else:
            print(f"SerpAPI Error: {resp.status_code}")
            return []
    except Exception as e:
        print(f"SerpAPI Request failed: {e}")
        return []

def search_semantic_scholar(query):
    print(f"Searching Semantic Scholar for: {query}...")
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": 5,
        "year": "2018-2026",
        "fields": "title,url,abstract,authors,year,citationCount,venue"
    }
    headers = {"x-api-key": SEMANTIC_SCHOLAR_KEY} if SEMANTIC_SCHOLAR_KEY else {}
    try:
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code == 200:
            return resp.json().get('data', [])
        else:
            print(f"Semantic Scholar Error: {resp.status_code}")
            return []
    except Exception as e:
        print(f"Semantic Scholar Request failed: {e}")
        return []

def get_bibtex_from_semantic(paper):
    title = paper.get('title', 'Unknown Title')
    year = str(paper.get('year', '2024'))
    authors = paper.get('authors', [])
    author_name = authors[0].get('name', 'Unknown') if authors else "Unknown"
    author_last = author_name.split()[-1] if ' ' in author_name else author_name
    
    citation_key = "".join(x for x in f"{author_last}{year}{title.split()[0]}" if x.isalnum())
    
    author_str = " and ".join([a.get('name', '') for a in authors])
    
    bib = f"@article{{{citation_key},\n"
    bib += f"  title = {{{title}}},\n"
    bib += f"  author = {{{author_str}}},\n"
    bib += f"  journal = {{{paper.get('venue', 'Semantic Scholar')}}},\n"
    bib += f"  year = {{{year}}},\n"
    bib += f"  url = {{{paper.get('url', '')}}}"
    bib += "}\n"
    return bib

# --- EXECUTION ---
with open(INSIGHTS_FILE, 'w', encoding='utf-8') as f:
    f.write(f"# Related Works Search Insights\n")
    f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")

with open(BIB_FILE, 'w', encoding='utf-8') as bib_f, open(INSIGHTS_FILE, 'a', encoding='utf-8') as ins_f:
    for q in QUERIES:
        ins_f.write(f"## Query: {q}\n")
        
        # Google Scholar
        results = search_scholar(q)
        if results:
            ins_f.write("### Google Scholar Hits\n")
            for r in results:
                bib_f.write(get_bibtex_from_scholar(r) + "\n")
                ins_f.write(f"- **{r.get('title')}** ({r.get('publication_info', {}).get('summary')})\n")
                ins_f.write(f"  - {r.get('snippet')}\n")
        
        # Semantic Scholar
        results = search_semantic_scholar(q)
        if results:
            ins_f.write("### Semantic Scholar Hits\n")
            for p in results:
                bib_f.write(get_bibtex_from_semantic(p) + "\n")
                ins_f.write(f"- **{p.get('title')}** ({p.get('year')})\n")
                ins_f.write(f"  - {p.get('abstract')[:200]}...\n")
        
        ins_f.write("\n---\n\n")

print("Related Works search complete. Results saved.")