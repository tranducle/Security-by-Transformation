# Literature-Grounded Knowledge Base Review Package

This directory contains the anonymized evidence package for the manuscript section titled **Literature-Grounded Knowledge Base**. It is designed for blind peer review and provides a compact, reviewer-facing trail from the manuscript's framework claims to the retained literature base.

## Package Purpose

The package documents how a refined literature corpus was narrowed to a core shortlist of 21 papers and how those papers were mapped to the manuscript's five guiding themes:

1. SME digital transformation
2. readiness and maturity
3. cybersecurity implications
4. resilience and continuity
5. resource or governance constraints

## Included Files

- `evidence_manifest.json` — machine-readable inventory of the review package
- `methodology_note.md` — short explanation of corpus refinement and theme assignment
- `core_shortlist_sanitized.json` — retained-paper metadata with theme mappings
- `claim_to_evidence_map.md` — reviewer-facing mapping from manuscript claims to evidence clusters

## Anonymity Note

This package intentionally omits author-identifying information, workstation paths, and project-internal operational notes. File references are package-local so reviewers can inspect the evidence without exposure to non-review materials.

## How to Use This Package

1. Start with `methodology_note.md` for the corpus-refinement logic.
2. Use `core_shortlist_sanitized.json` to inspect the retained papers and their theme mappings.
3. Use `claim_to_evidence_map.md` to trace framework claims to the relevant evidence clusters.
4. Use `evidence_manifest.json` to verify the package contents and file roles.
