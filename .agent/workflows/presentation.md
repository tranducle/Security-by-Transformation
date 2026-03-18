---
description: Create presentation slides from research
---

# Presentation Workflow (SOP_PRESENTATION_GEN)

**Use when:** Creating conference presentations or slides.

---

## Step 1: Presentation Planning

Define parameters:

- Venue (conference, defense, seminar)
- Time limit (10 min, 20 min, 45 min)
- Audience (experts, mixed, general)
- Format (slides, poster)

---

## Step 2: Structure Design

Typical academic presentation:

| Section | Slides | Content |
|---------|--------|---------|
| Title | 1 | Title, authors, affiliation |
| Motivation | 2-3 | Problem, importance |
| Background | 2-3 | Key concepts, related work |
| Research Question | 1 | Clear statement |
| Methodology | 2-4 | Approach, design |
| Results | 3-5 | Key findings, figures |
| Discussion | 2-3 | Implications, limitations |
| Conclusion | 1 | Summary, future work |
| Questions | 1 | Contact info |

---

## Step 3: Content Simplification

Translate paper to presentation:

- One main idea per slide
- Minimal text (bullet points)
- Visuals over words
- Remove jargon for general audiences

---

## Step 4: Visual Design

Design principles:

- Consistent template
- High contrast
- Large fonts (24pt minimum)
- Quality images
- Simple animations (if any)

---

## Step 5: Figure Adaptation

Adapt paper figures:

- Simplify for projection
- Increase font sizes
- Highlight key points
- Add build-up if complex

---

## Step 6: TikZ Diagrams (if needed)

Create professional diagrams:

- Architecture diagrams
- Flow charts
- Conceptual models

---

## Step 7: Slide Generation

Create slides using:

- PowerPoint/Keynote
- LaTeX Beamer
- Google Slides

---

## Step 8: Practice Notes

Add speaker notes for each slide.

---

## Output Artifacts

| File | Location |
|------|----------|
| presentation.pptx/pdf | 9_Presentation/ |
| speaker_notes.md | 9_Presentation/ |

---



---

## Agent Routing

> **Primary Agent**: `PresentationArchitect`
> Load agent config: `agents/PresentationArchitect.json`

## Trigger Phrases

- "Create presentation for [PAPER]"
- "Make slides for [CONFERENCE]"
- "Prepare defense slides"

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
