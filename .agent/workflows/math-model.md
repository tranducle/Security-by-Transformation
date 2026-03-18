---
description: Mathematical model formulation and verification
---

# Mathematical Modeling Workflow (SOP_MATH_FORMULATION)

**Use when:** Building formal mathematical models for research.

---

## Step 1: Problem Formalization

Translate research problem to math:

- Define decision variables
- Specify parameters
- Identify constraints
- Define objective function

---

## Step 2: Model Type Selection

| Type | Use Case | Form |
|------|----------|------|
| **Linear Programming (LP)** | Resource allocation | min cᵀx s.t. Ax ≤ b |
| **Integer Programming (IP)** | Discrete decisions | x ∈ Z |
| **Nonlinear Optimization** | Complex relationships | min f(x) |
| **Dynamic Programming** | Sequential decisions | Bellman equation |
| **Game Theory** | Strategic interaction | Nash equilibrium |
| **Stochastic Models** | Uncertainty | E[f(x,ξ)] |

---

## Step 3: Model Formulation

### Notation Table

| Symbol | Definition | Domain |
|--------|------------|--------|
| x | Decision variable | x ∈ ℝⁿ |
| c | Cost vector | c ∈ ℝⁿ |

### Objective Function

```
minimize/maximize Z = f(x₁, x₂, ..., xₙ)
```

### Constraints

```
subject to:
  g₁(x) ≤ b₁
  g₂(x) = b₂
  x ≥ 0
```

---

## Step 4: Mathematical Structure Analysis

Analyze model properties:

- Convexity
- Linearity
- Feasibility
- Boundedness
- Complexity class

---

## Step 5: Proof Verification

For theoretical claims:

- State theorem clearly
- List assumptions
- Provide step-by-step proof
- Verify edge cases

---

## Step 6: Numerical Solution

Solve the model:

- Select appropriate solver
- Implement in Python/MATLAB
- Verify solution quality

```python
from scipy.optimize import linprog, minimize
# or using cvxpy, gurobipy, etc.
```

---

## Step 7: Sensitivity Analysis

- Parameter sensitivity
- Shadow prices (for LP)
- Stability analysis

---

## Output Artifacts

| File | Location |
|------|----------|
| model_formulation.md | 3_Theoretical_Framework/ |
| proofs.md | 3_Theoretical_Framework/ |
| numerical_solution.md | 6_Analysis_Results/ |

---



---

## Agent Routing

> **Primary Agent**: `AppliedMathModeler`
> Load agent config: `agents/AppliedMathModeler.json`

## Trigger Phrases

- "Formulate a mathematical model for [PROBLEM]"
- "Optimize [OBJECTIVE]"
- "Prove [THEOREM]"

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
