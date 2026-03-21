---
description: Comprehensive ethics audit using SOP_ETHICAL_AUDIT — 4-agent pipeline for IRB compliance, GDPR, dual-use screening, and regulatory audit
---

# Full Ethical Audit Workflow (SOP_ETHICAL_AUDIT)

**Use when:** Conducting a comprehensive ethics review covering IRB compliance, data privacy (GDPR/HIPAA), dual-use risk assessment, and regulatory compliance.

---

## Step 1: Ethics Screening

> **Agent:** `EthicalComplianceGuard`

- Screen research for ethical concerns
- Check IRB/ethics board requirements
- Assess informed consent procedures
- Review participant protection protocols
- Evaluate data handling and anonymization practices
- Flag potential conflicts of interest

---

## Step 2: Data Privacy Audit

> **Agent:** `DataPrivacyOfficer`

- GDPR compliance check (data minimization, right to erasure, DPIAs)
- HIPAA compliance (if health data)
- Data retention policy review
- Cross-border data transfer assessment
- Anonymization/pseudonymization adequacy
- Third-party data sharing agreements

---

## Step 3: Dual-Use & Harm Assessment

> **Agent:** `RedTeamEthicsDualUseGuard`

- Assess dual-use potential (civilian → military/surveillance)
- Evaluate misuse scenarios
- Check for bias amplification risks
- Assess environmental impact
- Review accessibility and equity implications
- Recommend safeguards and restrictions

---

## Step 4: Regulatory Compliance Final Audit

> **Agent:** `RegulatoryComplianceAuditor`

- Map to applicable regulatory frameworks
- Generate compliance checklist
- Identify remaining gaps
- Produce audit-ready documentation
- Recommend policy changes

---

## Output Artifacts

| File | Location |
|------|----------|
| ethics_screening.md | 8_Project_Management/ |
| privacy_audit.md | 8_Project_Management/ |
| dual_use_assessment.md | 8_Project_Management/ |
| compliance_report.md | 8_Project_Management/ |

---

## Agent Routing

> **Pipeline**: `EthicalComplianceGuard` → `DataPrivacyOfficer` → `RedTeamEthicsDualUseGuard` → `RegulatoryComplianceAuditor`

## Trigger Phrases

- "Full ethics audit"
- "Comprehensive ethics review"
- "Dual-use risk check"
- "GDPR compliance audit"
- "IRB review preparation"

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
