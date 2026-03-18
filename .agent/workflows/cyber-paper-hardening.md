---
description: Harden AI-for-cybersecurity / SME-security research papers using 20 specialized agents across 5 layers
---

# Cybersecurity Paper Hardening Workflow (SOP_CYBER_PAPER_HARDENING)

This workflow hardens cybersecurity / AI-for-cybersecurity / SME-security papers
through a rigorous 5-layer audit pipeline. Each layer activates 4 specialized
agents that produce structured reports.

## Prerequisites
- Complete manuscript draft or near-final paper
- Paper must be in the cybersecurity, AI-for-security, or SME-security domain
- All SDP directories exist (run `/init` if needed)

## Workflow Steps

### Layer 1: Threat Realism & Adversarial Validity

1. **ThreatModelRealityAuditor** — Audit Thread Model
   - Check if the threat model is realistic (attacker capability, knowledge, access, dwell time, stealth, budget)
   - Flag unrealistic assumptions (too-weak or too-strong attacker)
   - Compare against MITRE ATT&CK real-world TTPs
   - Save report to `3_Theoretical_Framework/cyber_review/threat_model_audit.md`

2. **AdaptiveAttackerSimulatorV2** — Simulate Adaptive Adversary
   - Model how a rational attacker would adapt to the proposed defense
   - Identify evasion strategies paper doesn't consider
   - Flag "static attacker" assumptions
   - Save report to `3_Theoretical_Framework/cyber_review/adaptive_attacker_sim.md`

3. **DefenseEvasionPressureTester** — Red-Team Evasion Surface
   - Map the full evasion surface of the proposed defense
   - Design red-team experiments the paper should include
   - Identify bypass strategies via feature-space, model-space, and concept-drift attacks
   - Save report to `3_Theoretical_Framework/cyber_review/evasion_pressure_test.md`

4. **KillChainCoverageMapper** — Map Kill Chain Coverage
   - Map the solution to MITRE ATT&CK / Lockheed Kill Chain / Diamond Model
   - Identify which phases are covered and which are blind spots
   - Score coverage percentage with gap analysis
   - Save report to `3_Theoretical_Framework/cyber_review/kill_chain_coverage.md`

---

### Layer 2: Data & Evaluation Integrity

5. **SecurityDatasetProvenanceForensics** — Investigate Dataset Provenance
   - Check dataset age, representativeness, label quality, and attack coverage
   - Flag synthetic vs real traffic issues
   - Verify alignment with modern threat landscape
   - Save report to `6_Analysis_Results/cyber_data_audit/dataset_provenance.md`

6. **TelemetryFidelityInspector** — Verify Telemetry Signals
   - Check if proposed telemetry sources actually exist in target deployment
   - Verify signal availability, sampling rates, and fidelity
   - Flag "lab-only" signals unavailable in production
   - Save report to `6_Analysis_Results/cyber_data_audit/telemetry_fidelity.md`

7. **LeakageHunterCyberPipelines** — Detect Data Leakage
   - Scan for temporal leakage, label leakage, and feature leakage specific to cyber ML
   - Check train/test contamination via IP, session, or attack-campaign overlap
   - Flag future-information leakage in time-series security data
   - Save report to `6_Analysis_Results/cyber_data_audit/leakage_audit.md`

8. **GroundTruthIntegrityExaminer** — Analyze Ground Truth Labels
   - Evaluate label reliability (who labeled, what criteria, what agreement?)
   - Estimate label noise for security datasets
   - Check if ground truth reflects operational reality
   - Save report to `6_Analysis_Results/cyber_data_audit/ground_truth_integrity.md`

---

### Layer 3: SOC Operations & Deployment Viability

9. **SOCWorkflowCompatibilityAnalyzer** — Analyze SOC Integration
   - Evaluate how the tool fits into real SOC workflows (Tier 1/2/3)
   - Check SIEM/SOAR integration feasibility
   - Assess analyst skill requirements
   - Save report to `3_Theoretical_Framework/sme_analysis/soc_workflow.md`

10. **FalsePositiveBurdenEstimator** — Model FP Burden
    - Calculate operational cost of false positives (analyst hours, fatigue, trust erosion)
    - Model alert-to-investigation ratio
    - Compare against baseline FP rates in real SOCs
    - Save report to `3_Theoretical_Framework/sme_analysis/fp_burden.md`

11. **MeanTimeToDefendTranslator** — Translate ML Metrics to Defense
    - Convert accuracy/F1/AUC into MTTD (Mean Time To Detect), MTTR, MTTC
    - Map model performance to actual security improvement
    - Flag papers that report only ML metrics without defense translation
    - Save report to `3_Theoretical_Framework/sme_analysis/mttd_translation.md`

12. **AlertExplainabilityAuditor** — Audit Alert Interpretability
    - Check if alerts include actionable explanations for SOC analysts
    - Evaluate analyst trust calibration
    - Flag "black box alert" anti-patterns
    - Save report to `3_Theoretical_Framework/sme_analysis/alert_explainability.md`

---

### Layer 4: SME Realism & Adoption Friction

13. **SMEResourceRealityChecker** — Evaluate SME Feasibility
    - Check if SMEs (<250 employees) can actually deploy the proposed solution
    - Assess hardware, staffing, and skill requirements
    - Flag enterprise-grade assumptions applied to SME context
    - Save report to `3_Theoretical_Framework/sme_analysis/sme_resource_reality.md`

14. **CyberHygieneDependencyDetector** — Identify Hygiene Dependencies
    - Find baseline security hygiene assumptions (patching, logging, segmentation)
    - Check if these prerequisites exist in target SMEs
    - Identify "silent prerequisites" the paper doesn't acknowledge
    - Save report to `3_Theoretical_Framework/sme_analysis/hygiene_dependencies.md`

15. **SMEIncentiveAdoptionFrictionMapper** — Analyze Adoption Economics
    - Map stakeholder incentives and adoption barriers
    - Analyze cost-of-adoption vs cost-of-breach economics
    - Identify behavioral and organizational friction points
    - Save report to `3_Theoretical_Framework/sme_analysis/adoption_friction.md`

16. **ComplianceToControlBridgeBuilder** — Map to Governance Controls
    - Map research contributions to real compliance frameworks (NIST CSF, ISO 27001, CIS V8)
    - Identify which controls the research addresses
    - Flag compliance claims without control mapping evidence
    - Save report to `3_Theoretical_Framework/sme_analysis/compliance_bridge.md`

---

### Layer 5: AI-for-Cyber Scientific Rigor

17. **SecurityAIClaimBoundaryEnforcer** — Enforce Claim Boundaries
    - Separate AI claims from security claims
    - Flag conflation of "model improves" with "security improves"
    - Verify evidence chain from AI improvement to security outcome
    - Save report to `3_Theoretical_Framework/cyber_review/claim_boundary.md`

18. **ModelDriftThreatDriftCoupler** — Analyze Drift Coupling
    - Check if paper addresses model drift in context of evolving threats
    - Analyze retraining cost when threat landscape changes
    - Flag papers that assume static threat landscape for dynamic models
    - Save report to `3_Theoretical_Framework/cyber_review/drift_coupling.md`

19. **HumanAITrustCalibrationAnalyzer** — Analyze Trust Dynamics
    - Evaluate how the system affects analyst trust (over-trust, under-trust)
    - Check for automation bias risks
    - Flag systems that could cause learned helplessness or alarm fatigue
    - Save report to `3_Theoretical_Framework/cyber_review/trust_calibration.md`

20. **SecurityValueRealizationAuditor** — Audit Value Chain
    - Verify the complete value chain: technical improvement → operational improvement → security improvement
    - Flag "accuracy-only" papers with no security value argument
    - Check if claimed improvements translate to measurable security outcomes
    - Save report to `3_Theoretical_Framework/cyber_review/value_realization.md`

---

## Post-Hardening

After all 5 layers complete:
1. **Compile Findings** — Aggregate all 20 reports into a single cyber hardening summary
2. **Prioritize Fixes** — Rank issues by reviewer-attack probability × severity
3. **Generate Revision Plan** — Create actionable manuscript patches
4. Save consolidated report to `3_Theoretical_Framework/cyber_review/cyber_hardening_consolidated.md`

## Output Directories
- `3_Theoretical_Framework/cyber_review/` — Threat realism & AI rigor reports
- `3_Theoretical_Framework/sme_analysis/` — SOC/SME feasibility reports
- `6_Analysis_Results/cyber_data_audit/` — Data integrity reports

## Triggers
- "cyber paper hardening"
- "harden cyber paper"
- "security paper review"
- "cyber paper review"
- "kiểm tra bài báo cyber"
- "đánh giá bài báo bảo mật"
