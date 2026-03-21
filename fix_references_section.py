import re

# Read manuscript
with open('7_Manuscript_Draft/manuscript.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Split text
if '# References' in text:
    main_text, _ = text.split('# References', 1)
else:
    main_text = text

# Find citations
paren_cites = re.findall(r'\(([^)]*\d{4}[a-z]?[^)]*)\)', main_text)
narrative_cites = re.findall(r'([A-Z][a-z]+(?: et al\.)?)\s+\((\d{4}[a-z]?)\)', main_text)

citations = []
for cite in paren_cites:
    parts = cite.split(';')
    for part in parts:
        part = part.strip()
        if re.search(r'\d{4}', part):
            citations.append(part)

for author, year in narrative_cites:
    citations.append(f"{author}, {year}")

authors_cited = set()
for c in citations:
    c = re.sub(r', p\. \d+', '', c)
    c = c.strip()
    authors_cited.add(c)

print("Citations extracted from text:")
for a in sorted(authors_cited):
    print(f" - {a}")

import json
try:
    with open('7_Manuscript_Draft/references.bib', 'r', encoding='utf-8') as f:
        bib = f.read()
except FileNotFoundError:
    bib = ""

import re

# Parse bib entries manually
entries = []
# split by @
raw_entries = ['@' + e for e in bib.split('@')[1:]]
for raw in raw_entries:
    # get key
    match = re.search(r'@(\w+)\s*\{\s*([^,]+),', raw)
    if not match: continue
    entry_type = match.group(1).lower()
    entry_key = match.group(2).strip()
    
    # extract fields using regex
    fields = {}
    # match field = {value} or field = "value"
    field_matches = re.finditer(r'^\s*([a-zA-Z]+)\s*=\s*(\{([^}]+)\}|"([^"]+)"|(.*?)),?\s*$', raw, re.MULTILINE | re.DOTALL)
    for fm in field_matches:
        field_name = fm.group(1).lower()
        if fm.group(3):
            val = fm.group(3)
        elif fm.group(4):
            val = fm.group(4)
        else:
            val = fm.group(5)
        # clean up val (newlines)
        val = re.sub(r'\s+', ' ', val).strip()
        fields[field_name] = val
    entries.append({'key': entry_key, 'type': entry_type, 'fields': fields})

def format_authors(author_str):
    authors = author_str.split(' and ')
    formatted = []
    for a in authors:
        parts = a.split(',')
        if len(parts) == 2:
            formatted.append(f"{parts[0].strip()}, {parts[1].strip()[0]}.")
        else:
            # First Last -> Last, F.
            names = a.strip().split()
            if len(names) > 1:
                formatted.append(f"{names[-1]}, {' '.join([n[0]+'.' for n in names[:-1]])}")
            else:
                formatted.append(names[0])
    if len(formatted) > 1:
        if len(formatted) > 20: # APA 7th ed cap
            return ", ".join(formatted[:19]) + ", ... " + formatted[-1]
        elif len(formatted) == 2:
            return f"{formatted[0]} & {formatted[1]}"
        else:
            return ", ".join(formatted[:-1]) + ", & " + formatted[-1]
    elif formatted:
        return formatted[0]
    return ""

def generate_apa(entry):
    f = entry['fields']
    # Author
    author = format_authors(f.get('author', 'Unknown'))
    year = f.get('year', 'n.d.')
    title = f.get('title', '')
    title = title.replace('{', '').replace('}', '')
    
    if entry['type'] == 'article':
        journal = f.get('journal', '')
        vol = f.get('volume', '')
        number = f.get('number', '')
        pages = f.get('pages', '')
        doi = f.get('doi', '')
        
        ref = f"{author} ({year}). {title}."
        if journal:
            ref += f" *{journal}*"
            if vol:
                ref += f", *{vol}*"
                if number:
                    ref += f"({number})"
            if pages:
                # clean pages
                pages = pages.replace('--', '-')
                ref += f", {pages}."
            else:
                ref += "."
        
        if doi:
            if not doi.startswith('http'):
                doi = f"https://doi.org/{doi}"
            ref += f" {doi}"
        elif f.get('url'):
            ref += f" {f.get('url')}"
            
    elif entry['type'] in ['book', 'misc']:
        publisher = f.get('publisher', '')
        ref = f"{author} ({year}). *{title}*."
        if publisher:
            ref += f" {publisher}."
        if f.get('url') and not f.get('doi'):
            ref += f" Retrieved from {f.get('url')}"
            
    else:
        ref = f"{author} ({year}). {title}."
        if f.get('url'):
            ref += f" {f.get('url')}"
    return ref.strip()

references = []
ref_keys = []
for entry in entries:
    ref_str = generate_apa(entry)
    references.append(ref_str)
    ref_keys.append(entry['key'])

# Try to match citations to bib keys to filter only cited
# Let's see what keys are matched
# For simplicity, we can just include all entries since the user wants to check
# But wait, user said: "Double check to make sure you don't miss any citation in reference or having papers that not cited in text"
# And "Bổ sung vào cuối Manuscript Reference section và điền các paper đã được cited trong manuscript vào."
# This means we MUST filter the list. Let's do a simple substring match of the author's last name in the text
authors_in_bib = []
valid_entries = []

for entry in entries:
    authors_str = entry['fields'].get('author', '')
    last_names = []
    if authors_str:
        for a in authors_str.split(' and '):
            if ',' in a:
                last_names.append(a.split(',')[0].strip())
            else:
                last_names.append(a.strip().split()[-1])
    
    first_author_last_name = last_names[0] if last_names else "Unknown"
    year = entry['fields'].get('year', '')
    
    is_cited = False
    for c in authors_cited:
        # Moffatt case
        if "Moffatt" in c and "Moffatt" in entry['fields'].get('title', ''):
             is_cited = True
             break
        # General case
        if (first_author_last_name in c or first_author_last_name.replace('{', '').replace('}', '') in c) and year in c:
            is_cited = True
            break
        # Sometimes 'British Columbia Civil Resolution Tribunal'
        if "British Columbia" in c and "British" in first_author_last_name:
            is_cited = True
            break
            
    if is_cited:
        valid_entries.append(entry)
    else:
        print(f"NOT CITED (removing): {first_author_last_name} ({year})")

# Missing citations?
for c in authors_cited:
    if "e.g." in c: c = c.split("e.g.,")[1].strip()
    year_match = re.search(r'\d{4}', c)
    if not year_match: continue
    
    found = False
    for entry in valid_entries:
        authors_str = entry['fields'].get('author', '')
        last_names = [a.split(',')[0].strip() if ',' in a else a.strip().split()[-1] for a in authors_str.split(' and ')]
        first_ln = last_names[0] if last_names else "Unknown"
        if first_ln in c or first_ln.replace('{', '').replace('}', '') in c or "Moffatt" in c or "British" in c:
            found = True
            break
            
    if not found:
        print(f"MISSING FROM BIB: {c}")

valid_references = [generate_apa(e) for e in valid_entries]
valid_references.sort()

new_ref_section = "\n# References\n\n"
for ref in valid_references:
    new_ref_section += ref + "\n\n"

new_manuscript = main_text.rstrip() + "\n\n" + new_ref_section

with open('7_Manuscript_Draft/manuscript_updated.md', 'w', encoding='utf-8') as f:
    f.write(new_manuscript)

print(f"\nWritten {len(valid_references)} verified references to manuscript_updated.md")
