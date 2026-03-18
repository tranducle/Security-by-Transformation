---
description: Threat modeling and cyber risk simulation
---

# Threat Model Workflow (SOP_CYBER_RISK_SIM)

**Use when:** Conducting security threat assessment and risk analysis.

---

## Step 1: Asset Mapping

Identify and categorize assets:

- Critical systems
- Data assets (PHI, PII, financial)
- Network infrastructure
- Third-party services/SaaS

---

## Step 2: Attack Surface Analysis

Map potential entry points:

- External interfaces
- Internal access points
- Supply chain vectors
- Human factors

---

## Step 3: Threat Actor Profiling

Define adversary types:

| Actor | Motivation | Capability | Target |
|-------|------------|------------|--------|
| APT | Espionage | High | IP, strategic data |
| Cybercriminal | Financial | Medium-High | Ransomware, fraud |
| Insider | Various | High (access) | Data exfiltration |
| Hacktivist | Ideology | Low-Medium | Disruption |

---

## Step 4: Kill Chain Simulation

Model attack paths (MITRE ATT&CK):

1. Reconnaissance
2. Initial Access
3. Execution
4. Persistence
5. Privilege Escalation
6. Defense Evasion
7. Lateral Movement
8. Exfiltration/Impact

---

## Step 5: STRIDE Analysis

For each component:

| Threat | Question |
|--------|----------|
| **S**poofing | Can identity be faked? |
| **T**ampering | Can data be modified? |
| **R**epudiation | Can actions be denied? |
| **I**nfo Disclosure | Can data leak? |
| **D**enial of Service | Can service be disrupted? |
| **E**levation | Can privileges be gained? |

---

## Step 6: Risk Quantification

| Threat | Likelihood | Impact | Risk Score |
|--------|------------|--------|------------|
| [Threat 1] | High | Critical | 25 |
| [Threat 2] | Medium | High | 15 |

---

## Step 7: Compliance Check

Map to standards:

- NIST CSF
- ISO 27001
- Industry-specific (HIPAA, PCI-DSS)

---

## Output Artifacts

| File | Location |
|------|----------|
| threat_model.md | 4_Methodology_Design/ |
| attack_scenarios.md | 5_Experiments_Simulations/ |
| risk_matrix.md | 6_Analysis_Results/ |

---



---

## Agent Routing

> **Primary Agent**: `ThreatModeler`
> Load agent config: `agents/ThreatModeler.json`

## Trigger Phrases

- "Threat model for [SYSTEM]"
- "Security risk assessment"
- "STRIDE analysis"

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
