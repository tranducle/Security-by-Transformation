---
description: Design defense-in-depth security architecture using SOP_DEFENSE_ARCH — from architecture design through incident response and compliance
---

# Defense Architecture Workflow (SOP_DEFENSE_ARCH)

**Use when:** Designing a security architecture with defense-in-depth, incident response playbooks, and regulatory compliance verification.

---

## Step 1: Security Architecture Design

> **Agent:** `CyberSecurityArchitect`

- Design defense-in-depth architecture (network, host, application, data)
- Define security zones and trust boundaries
- Select security controls per layer
- Design authentication and authorization framework
- Specify encryption at rest and in transit

---

## Step 2: SME-Appropriate Simplification

> **Agent:** `MinViableSecurityArchitect`

- Tailor architecture to organization size and budget
- Identify minimum viable security controls
- Prioritize quick wins vs long-term investments
- Create phased implementation roadmap
- Design lightweight monitoring strategy

---

## Step 3: Incident Response Playbooks

> **Agent:** `IncidentReadinessPlaybookGenerator`

- Design incident response plan (NIST SP 800-61)
- Create playbooks per threat type:
  - Ransomware response
  - Data breach containment
  - DDoS mitigation
  - Insider threat handling
- Define escalation procedures and communication templates
- Design tabletop exercise scenarios

---

## Step 4: Regulatory Compliance Audit

> **Agent:** `RegulatoryComplianceAuditor`

- Map architecture to applicable regulations (GDPR, HIPAA, PCI-DSS, SOX)
- Verify compliance of designed controls
- Identify regulatory gaps and remediation steps
- Generate compliance documentation

---

## Output Artifacts

| File | Location |
|------|----------|
| security_architecture.md | 3_Theoretical_Framework/ |
| mvs_plan.md | 4_Methodology_Design/ |
| ir_playbooks.md | 5_Experiments_Simulations/ |
| compliance_audit.md | 6_Analysis_Results/ |

---

## Agent Routing

> **Pipeline**: `CyberSecurityArchitect` → `MinViableSecurityArchitect` → `IncidentReadinessPlaybookGenerator` → `RegulatoryComplianceAuditor`

## Trigger Phrases

- "Defense architecture"
- "Security architecture design"
- "Zero trust architecture"
- "Incident response planning"
- "Defense in depth"

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
