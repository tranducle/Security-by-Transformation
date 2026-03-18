---
description: Network protocol security audit (RFC compliance, crypto verification)
---

# Protocol Audit Workflow (SOP_PROTOCOL_SECURITY_AUDIT)

**Use when:** Auditing network protocols for security vulnerabilities.

---

## Step 1: Protocol Identification

Document the protocol:

- Protocol name and version
- RFC specifications
- Implementation being audited
- Scope of audit

---

## Step 2: RFC Compliance Check

Verify conformance to standards:

- Message format compliance
- State machine correctness
- Error handling per spec
- Extension handling

---

## Step 3: Cryptographic Verification

Audit crypto implementation:

| Component | Check | Status |
|-----------|-------|--------|
| Algorithm | Current standards (no MD5, SHA1) | ✓/✗ |
| Key length | Sufficient (≥2048 RSA, ≥256 ECC) | ✓/✗ |
| Random number | CSPRNG used | ✓/✗ |
| Key exchange | Forward secrecy | ✓/✗ |
| Certificate | Valid chain | ✓/✗ |

---

## Step 4: Traffic Analysis

Examine protocol behavior:

- Message flow analysis
- Timing characteristics
- Metadata exposure
- Side-channel leakage

---

## Step 5: Vulnerability Assessment

Common protocol weaknesses:

- Downgrade attacks
- Replay attacks
- Man-in-the-middle
- Injection vulnerabilities
- Denial of service vectors

---

## Step 6: Threat Assessment

Map findings to threat model:

- Attack feasibility
- Required attacker capability
- Potential impact
- Exploitability

---

## Step 7: Remediation Recommendations

Priority-ranked fixes:

1. Critical vulnerabilities
2. High-risk issues
3. Medium-risk improvements
4. Best practice recommendations

---

## Output Artifacts

| File | Location |
|------|----------|
| protocol_audit.md | 6_Analysis_Results/ |
| vulnerability_report.md | 6_Analysis_Results/ |
| remediation_plan.md | 1_Strategic_Plan/ |

---



---

## Agent Routing

> **Primary Agent**: `ProtocolNetworkSemanticsVerifier`
> Load agent config: `agents/ProtocolNetworkSemanticsVerifier.json`

## Trigger Phrases

- "Audit [PROTOCOL] security"
- "RFC compliance check"
- "Crypto audit for [SYSTEM]"

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
