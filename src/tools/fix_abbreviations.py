import re

file_path = "/Users/let/Documents/Security-in-Digital-Transformation/7_Manuscript_Draft/manuscript.md"
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

abstract_match = re.search(r'(# Abstract.*?)(# 1\. Introduction.*)', text, flags=re.DOTALL | re.IGNORECASE)

if abstract_match:
    pre_text = text[:abstract_match.start(2)]
    main_text = abstract_match.group(2)
else:
    pre_text = ""
    main_text = text

abbreviations = {
    "Generative Artificial Intelligence": "GenAI",
    "Large Language Models": "LLMs",
    "Large Language Model": "LLM",
    "Organizational Information Processing Theory": "OIPT",
    "Data Loss Prevention": "DLP",
    "Design Science Research": "DSR",
    "Identity and Access Management": "IAM",
    "Dynamic Algorithmic Threat Modeling": "DATM",
    "Information Systems": "IS"
}

for full_term, abbr in abbreviations.items():
    escaped_full = re.escape(full_term)
    escaped_abbr = re.escape(abbr)
    
    marker = f"___{abbr}___"
    
    pattern_def = re.compile(rf'{escaped_full}\s*\({escaped_abbr}\)', re.IGNORECASE)
    main_text = pattern_def.sub(marker, main_text)
    
    pattern_raw = re.compile(rf'{escaped_full}', re.IGNORECASE)
    main_text = pattern_raw.sub(marker, main_text)
    
    first_time = True
    def replace_marker(match):
        global first_time
        if first_time:
            first_time = False
            return f"{full_term} ({abbr})"
        else:
            return abbr
            
    main_text = re.sub(marker, replace_marker, main_text)

final_text = pre_text + main_text

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Abbreviations fixed successfully in manuscript.")
