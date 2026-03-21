---
description: Simulate cyber risk scenarios using SOP_CYBER_RISK_SIM — asset mapping, kill chain simulation, threat modeling, and compliance check
---

# Cyber Risk Simulation Workflow (SOP_CYBER_RISK_SIM)

**Use when:** Assessing cybersecurity posture through attack simulation, threat modeling, and compliance mapping.

---

## Step 1: Asset & Shadow IT Mapping

> **Agent:** `SaaSShadowITCartographer`

- Map all IT assets (hardware, software, cloud services)
- Discover shadow IT and unsanctioned SaaS
- Classify assets by criticality and data sensitivity
- Map data flows between systems
- Identify attack surface exposure points

---

## Step 2: Kill Chain Simulation

> **Agent:** `AdversarialAttackSimulator`

- Simulate MITRE ATT&CK kill chains
- Model attacker capabilities (script kiddie → APT)
- Execute red team attack scenarios:
  1. Initial access vectors
  2. Lateral movement paths
  3. Privilege escalation opportunities
  4. Data exfiltration routes
- Score exploitability per attack path

---

## Step 3: Threat Modeling

> **Agent:** `ThreatModeler`

- Apply STRIDE methodology per component
- Create threat taxonomy (category, likelihood, impact)
- Generate DREAD risk scores
- Map threats to MITRE ATT&CK techniques
- Produce data flow diagrams with trust boundaries

---

## Step 4: Compliance & Standards Check

> **Agent:** `SecurityStandardsChecker`

- Map controls to NIST CSF / ISO 27001 / CIS
- Identify compliance gaps
- Generate remediation priority matrix
- Produce audit-ready documentation

---

## Output Artifacts

| File | Location |
|------|----------|
| asset_map.md | 5_Experiments_Simulations/ |
| attack_simulation.md | 5_Experiments_Simulations/ |
| threat_model.md | 4_Methodology_Design/ |
| compliance_gap.md | 6_Analysis_Results/ |

---

## Agent Routing

> **Pipeline**: `SaaSShadowITCartographer` → `AdversarialAttackSimulator` → `ThreatModeler` → `SecurityStandardsChecker`

## Trigger Phrases

- "Cyber risk simulation"
- "Attack simulation"
- "Security risk assessment"
- "Red team simulation"

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
