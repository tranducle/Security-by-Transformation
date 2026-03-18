---
description: Verify mathematical models and equations using local SymPy (free) or Wolfram Alpha
---
<!-- SOP: SOP_MATH_AUDIT -->


# Math Verification Workflow (SOP_MATH_VERIFY)

**Use when:** Verifying equations, proofs, or mathematical models for correctness.

---

## Step 1: Preparation

- Ensure `sympy` is installed: `pip install sympy`
- Have equations ready in LaTeX or standard math notation

---

## Step 2: Local Verification (SymPy)

Use `src/tools/sympy_tools.py` for purely symbolic math.

**Recommended for:**

- Equation balancing ($LHS = RHS$)
- Derivatives / Integrals
- Simplification
- Matrix operations

```python
from src.tools.sympy_tools import verify_equation_sympy
verify_equation_sympy("LHS", "RHS")
```

---

## Step 3: Remote Verification (Wolfram Alpha)

Use `src/tools/wolfram_tools.py` if SymPy fails or requires external data.

**Use for:**

- Questions involving units (physics)
- Real-world data ("population", "distance")
- Complex proofs not handled by SymPy

```python
from src.tools.wolfram_tools import wolfram_llm_query
wolfram_llm_query("verify that ...")
```

---

## Step 4: Auditing Report

- Record findings in the verification artifact (e.g., `audit_report.md`)
- Mark each equation as `[Verified Local]`, `[Verified Wolfram]`, or `[Failed]`

---

## Output Artifacts

| File | Location |
|------|----------|
| math_audit_report.md | 6_Analysis_Results/ |
| verification_log.md | 4_Methodology_Design/ |

---

## Agent Routing

> **Primary Agent**: `MathProofAuditor`
> Load agent config: `agents/MathProofAuditor.json`

---

## Trigger Phrases

- "Verify this equation"
- "Check my math"
- "Is this proof correct?"
- "Validate mathematical model"

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
