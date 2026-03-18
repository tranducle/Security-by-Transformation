---
description: SME cybersecurity risk assessment and insurance analysis
---

# SME Risk Assessment Workflow (SOP_SME_RISK_ASSESSMENT)

**Use when:** Assessing cybersecurity risk for Small/Medium Enterprises.

---

## Step 1: SME Typology Classification

Classify the SME:

| Factor | Options |
|--------|---------|
| Industry | Healthcare, Retail, Manufacturing, Finance, Services |
| Size | Micro (<10), Small (10-49), Medium (50-249) |
| Digital Maturity | Low, Medium, High |
| Data Sensitivity | Low, Medium, High, Critical |

---

## Step 2: Owner/Leadership Profile

Assess decision-maker characteristics:

- Risk tolerance level
- Cybersecurity awareness
- Investment appetite
- Technical background

---

## Step 3: Culture Audit

Evaluate security culture:

- Password practices
- Phishing susceptibility
- Shadow IT usage
- Policy compliance
- Training history

---

## Step 4: Supply Chain Risk

Assess vendor ecosystem:

| Vendor | Access Level | Assessment |
|--------|--------------|------------|
| Cloud provider | High | SOC 2 certified |
| IT support | High | BAA in place |
| Software vendor | Medium | Security unclear |

---

## Step 5: Risk Quantification

Calculate potential impact:

- Annual Loss Expectancy (ALE)
- Business interruption cost
- Data breach cost estimate
- Regulatory fine exposure

---

## Step 6: Insurance Analysis

Cyber insurance considerations:

- Coverage needs
- Policy gaps
- Premium factors
- Deductible optimization

---

## Step 7: Recommendations

Tiered recommendations:

- Tier 1: Immediate actions (low cost, high impact)
- Tier 2: Short-term improvements
- Tier 3: Long-term investments

---

## Output Artifacts

| File | Location |
|------|----------|
| sme_risk_assessment.md | 6_Analysis_Results/ |
| vendor_risk_matrix.md | 6_Analysis_Results/ |
| recommendations.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `SMETypologyArchitect`
> Load agent config: `agents/SMETypologyArchitect.json`

## Trigger Phrases

- "Risk assessment for [SME]"
- "Cybersecurity risk for small business"
- "SME security audit"

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
