---
description: Automated Abbreviation Consistency Audit
---
# Abbreviation Consistency Audit Workflow

This workflow is designed to automatically correct the usage of full terms and abbreviations within a manuscript. It ensures that a term is defined on its first usage (e.g., "Generative Artificial Intelligence (GenAI)") and that all subsequent usages within the main text use ONLY the abbreviation (e.g., "GenAI").

1. Ensure the `AbbreviationConsistencyChecker` agent is active or you assume its role.
2. Locate the python script `src/tools/fix_abbreviations.py`.
3. Read the script with `view_file` to verify the target manuscript path and the dictionary of abbreviations to enforce.
4. If necessary, modify the python script to append or update any new abbreviations required by the specific paper context.
5. Execute the script:
   // turbo
   `python src/tools/fix_abbreviations.py`
6. Once the script finishes, use `git diff` or `view_file` to manually verify that the substitutions were performed accurately (e.g., checking that the Abstract was appropriately left unmodified while the main text was corrected).
7. Sync project status or respond to the user with the success confirmation.
