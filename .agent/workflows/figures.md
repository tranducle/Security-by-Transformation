---
description: Create figures, charts, and data visualizations
---

# Figure Generation Workflow (SOP_FIGURE_GENERATION)

**Use when:** Creating publication-quality figures and charts.

---

## Step 1: Visualization Planning

Determine visualization needs:

- Data type (categorical, continuous, time series)
- Message to convey
- Target audience
- Publication requirements

---

## Step 2: Chart Type Selection

| Data Type | Best Charts |
|-----------|-------------|
| Comparison | Bar, grouped bar, radar |
| Distribution | Histogram, box plot, violin |
| Relationship | Scatter, bubble, heatmap |
| Composition | Pie, stacked bar, treemap |
| Trend | Line, area, sparkline |
| Flow | Sankey, chord, flow diagram |

---

## Step 3: Design Standards

Publication quality requirements:

- Resolution: 300+ DPI
- Font size: Readable at print size
- Color: Colorblind-friendly palette
- Labels: All axes labeled with units
- Legend: Clear and positioned well

---

## Step 4: Tool Selection

Choose appropriate tool:

- **Python (matplotlib, seaborn):** Statistical charts
- **TikZ/PGFPlots:** LaTeX integration
- **draw.io/Lucidchart:** Diagrams
- **R (ggplot2):** Publication-quality stats plots

---

## Step 5: Chart Creation

Create the visualization with code for reproducibility.

---

## Step 6: Polish & Export

Final touches:

- Remove chartjunk
- Ensure consistency across figures
- Export in required format (PDF, EPS, PNG)

---

## Step 7: Caption Writing

Write informative captions:

- What the figure shows
- Key takeaways
- Source/methodology note

---

## Output Artifacts

| File | Location |
|------|----------|
| figures/ | 7_Manuscript_Draft/ |
| figure_code.py | 6_Analysis_Results/ |

---



---

## Agent Routing

> **Primary Agent**: `VisualCommunicationArchitect`
> Load agent config: `agents/VisualCommunicationArchitect.json`

## Trigger Phrases

- "Create figure for [DATA]"
- "Visualize [RESULTS]"
- "Make a chart showing [X]"

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
