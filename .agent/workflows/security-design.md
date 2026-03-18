---
description: Design security architecture with defense-in-depth
---

# Security Design Workflow (SOP_DEFENSE_ARCH)

**Use when:** Designing security architecture and controls.

---

## Step 1: Requirements Gathering

Security requirements:

- Confidentiality needs
- Integrity requirements
- Availability targets
- Compliance mandates

---

## Step 2: Architecture Design

Defense-in-depth layers:

```
┌─────────────────────────────────────┐
│         Physical Security           │
├─────────────────────────────────────┤
│         Network Security            │
│   (Firewalls, Segmentation, IDS)    │
├─────────────────────────────────────┤
│         Host Security               │
│   (Hardening, EDR, Patching)        │
├─────────────────────────────────────┤
│       Application Security          │
│   (Input validation, AuthZ/AuthN)   │
├─────────────────────────────────────┤
│          Data Security              │
│   (Encryption, DLP, Masking)        │
└─────────────────────────────────────┘
```

---

## Step 3: Minimum Viable Security

For resource-constrained environments:

- Core controls only
- Risk-based prioritization
- Quick wins first

---

## Step 4: Incident Response Planning

Playbook components:

1. Detection procedures
2. Triage criteria
3. Containment steps
4. Eradication process
5. Recovery procedures
6. Lessons learned

---

## Step 5: Compliance Mapping

Map controls to requirements:

| Control | NIST CSF | ISO 27001 | HIPAA |
|---------|----------|-----------|-------|
| MFA | PR.AC-7 | A.9.4.2 | 164.312(d) |
| Encryption | PR.DS-1 | A.10.1.1 | 164.312(a)(2)(iv) |

---

## Step 6: Implementation Roadmap

| Phase | Controls | Timeline |
|-------|----------|----------|
| Phase 1 | MFA, Backup | Month 1-2 |
| Phase 2 | Encryption, Monitoring | Month 3-4 |
| Phase 3 | SIEM, Pen Testing | Month 5-6 |

---

## Output Artifacts

| File | Location |
|------|----------|
| security_architecture.md | 3_Theoretical_Framework/ |
| incident_playbook.md | 4_Methodology_Design/ |
| implementation_roadmap.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `CyberSecurityArchitect`
> Load agent config: `agents/CyberSecurityArchitect.json`

## Trigger Phrases

- "Design security for [SYSTEM]"
- "Security architecture"
- "Incident response plan"

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
