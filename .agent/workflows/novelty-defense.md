---
description: Defend the novelty of your research contribution against prior art using SOP_NOVELTY_DEFENSE — 4-agent pipeline for prior art scanning, baseline defense, and rebuttal strategy
---

# Novelty Defense Workflow (SOP_NOVELTY_DEFENSE)

**Use when:** You need to defend your research contribution's novelty, prepare for "lacks novelty" reviewer attacks, or verify your work is genuinely novel.

---

## Step 1: Prior Art Scan

> **Agent:** `PriorArtNoveltyScanner`

Comprehensive prior art analysis:

- Search academic databases (OpenAlex, Scopus, Semantic Scholar, Google Scholar)
- Search patent databases (Google Patents, USPTO)
- Check preprint servers (arXiv, SSRN, bioRxiv)
- Map citation neighborhoods of closest related work
- Identify potential "scoop" risks

**Output:** Prior art report with similarity scores

---

## Step 2: Baseline & Benchmark Defense

> **Agent:** `BaselineBenchmarkNoveltyDefender`

Position your contribution against existing baselines:

- Identify all relevant baselines and benchmarks
- Document what each baseline lacks vs your approach
- Build novelty delta table:

| Aspect | Closest Prior Work | Your Contribution | Delta |
|--------|-------------------|-------------------|-------|
| Method | [X does Y] | [You do Z] | [Improvement] |
| Scope | [Limited to A] | [Extends to B] | [Expansion] |

- Prepare "why not just use X?" responses

---

## Step 3: Innovation Positioning

> **Agent:** `InnovationStrategist`

Frame the contribution strategically:

- Classify contribution type (methodological, theoretical, empirical, applied)
- Articulate the "so what?" factor
- Position within the broader research trajectory
- Identify interdisciplinary novelty angles
- Generate elevator pitch for the contribution

---

## Step 4: Rebuttal Strategy

> **Agent:** `ReviewerStrategist`

Prepare pre-emptive reviewer defense:

- Anticipate "lacks novelty" attacks
- Draft rebuttal templates for common objections
- Create evidence-based response matrix
- Suggest additions to strengthen the novelty claim in the manuscript

---

## Output Artifacts

| File | Location |
|------|----------|
| prior_art_report.md | 2_Literature_Review/ |
| novelty_defense.md | 7_Manuscript_Draft/ |
| rebuttal_strategy.md | 8_Project_Management/ |

---

## Agent Routing

> **Primary Agent**: `PriorArtNoveltyScanner`
> Load agent config: `agents/PriorArtNoveltyScanner.json`
> **Pipeline**: `PriorArtNoveltyScanner` → `BaselineBenchmarkNoveltyDefender` → `InnovationStrategist` → `ReviewerStrategist`

## Trigger Phrases

- "Defend my novelty"
- "Prior art defense"
- "Is my research novel?"
- "Defend contribution"
- "Novelty check and defense"
- "Prepare for reviewer novelty attack"

---

## 📋 Post-Workflow Logging Reminder

> **IMPORTANT**: After completing this workflow, update project tracking:
>
> 1. Add entry to `8_Project_Management/project_log.md`
> 2. Update `8_Project_Management/milestone_tracker.md` if milestone status changed
> 3. Log significant decisions to `8_Project_Management/decision_log.md`
> 4. For major insights, update `0_Project_Admin/research_diary.md`
>
> **Quick command**: Run `/sync` to update all files at once.
