---
description: Ethics review and IRB compliance check
---

# Ethics Audit Workflow (SOP_ETHICAL_AUDIT)

**Use when:** Reviewing research for ethical compliance.

---

## Step 1: Initial Screening

Check for sensitive elements:

- Human subjects research
- Personal data collection
- Vulnerable populations
- Deception involved
- Potential for harm

---

## Step 2: Data Privacy Assessment

### GDPR Compliance (if applicable)

- Lawful basis for processing
- Data minimization
- Purpose limitation
- Storage limitation
- Subject rights enabled

### HIPAA Compliance (if healthcare)

- PHI handling
- Minimum necessary standard
- Business associate agreements
- De-identification requirements

---

## Step 3: Dual-Use Assessment

Check for potential misuse:

- Cybersecurity research → attack tools
- AI research → harmful applications
- Biological research → weaponization

If dual-use concerns:

- Document safeguards
- Consider publication restrictions
- Consult ethics board

---

## Step 4: Informed Consent

Review consent process:

- Clear explanation of purpose
- Voluntary participation
- Right to withdraw
- Data usage explanation
- Compensation disclosure (if any)

---

## Step 5: Risk Assessment

| Risk | Likelihood | Severity | Mitigation |
|------|------------|----------|------------|
| Data breach | Low | High | Encryption |
| Psychological harm | Low | Medium | Debriefing |

---

## Step 6: Regulatory Compliance

Final audit against:

- Institutional IRB requirements
- National regulations
- Journal requirements
- Funding agency rules

---

## Step 7: Documentation

Produce ethics package:

- Ethics approval application
- Informed consent forms
- Data management plan
- Risk assessment summary

---

## Output Artifacts

| File | Location |
|------|----------|
| ethics_assessment.md | 4_Methodology_Design/ |
| consent_form.md | 4_Methodology_Design/ |
| irb_application.md | 8_Project_Management/ |

---



---

## Agent Routing

> **Primary Agent**: `EthicalComplianceGuard`
> Load agent config: `agents/EthicalComplianceGuard.json`

## Trigger Phrases

- "Ethics review for [RESEARCH]"
- "IRB application"
- "GDPR compliance check"

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
