import re

with open('7_Manuscript_Draft/manuscript.md', 'r') as f:
    text = f.read()

# Find parenthetical citations: (Author, Year) or (Author & Author, Year) or (Author et al., Year)
# Also multiple citations: (Author, Year; Author2, Year)
paren_cites = re.findall(r'\(([^)]*\d{4}[a-z]?[^)]*)\)', text)

# Find narrative citations: Author (Year) or Author et al. (Year)
narrative_cites = re.findall(r'([A-Z][a-z]+(?: et al\.)?)\s+\((\d{4}[a-z]?)\)', text)

citations = []
for cite in paren_cites:
    # cite could be "Author, 2020; Author2, 2021"
    parts = cite.split(';')
    for part in parts:
        part = part.strip()
        if re.search(r'\d{4}', part):
            citations.append(part)

for author, year in narrative_cites:
    citations.append(f"{author}, {year}")

authors_cited = set()
for c in citations:
    # simple extraction of the first author or main part
    c = re.sub(r', p\. \d+', '', c)
    c = c.strip()
    authors_cited.add(c)

print("--- EXTRACTED INLINE CITATIONS ---")
for a in sorted(authors_cited):
    print(a)

print("\n--- REFERENCES IN BIB ---")
try:
    with open('7_Manuscript_Draft/references.bib', 'r') as f:
        bib = f.read()
except FileNotFoundError:
    bib = ""
    print("references.bib not found at 7_Manuscript_Draft/references.bib")
    
# Extract simple author and year from bib to match
bib_entries = re.findall(r'@\w+\{([^,]+),.*?author\s*=\s*(?:\{|"|)([^}"]+).*?year\s*=\s*(?:\{|"|)(\d{4})', bib, re.IGNORECASE | re.DOTALL)
print(f"Found {len(bib_entries)} entries in references.bib")
for key, author, year in bib_entries:
    # simplify author list
    authors = author.split(' and ')
    first_author = authors[0].split(',')[-1].strip() + " " + authors[0].split(',')[0].strip()
    print(f"[{key}] {first_author} ({year})")

