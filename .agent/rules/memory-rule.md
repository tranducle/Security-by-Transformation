---
trigger: always_on
---

## Memory Check Rule (Every 3 Messages)

```
CRITICAL SYSTEM RULE - AGENT ROUTING & MEMORY CHECK:

🧠 EVERY 3 USER MESSAGES, PAUSE and:

1. Run memory check:
   python src/tools/mem0_loader.py [PROJECT_ID]

2. Re-read routing rules from agents/MasterOrchestrator.json Section 6

3. For current task, IDENTIFY keywords and route to correct agent:

   ROUTING QUICK REFERENCE (206 Agents across 10 Domains):
   Source of truth: agents/MasterOrchestrator.json
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 1: STRATEGY & OPERATIONS (Lead: StrategicArchitect)
   ══════════════════════════════════════════════════════════════════
   plan, roadmap, strategy, wbs         → StrategicArchitect
   research plan, detailed plan         → ResearchPlanGenerator → SOP_RESEARCH_PLAN_CREATION
   track, status, log, progress         → ProjectStateKeeper / ProgressTracker
   agile, sprint, kanban, scrum         → ProjectPlanner
   logic, mece, hypothesis, problem solve → LogicStrategist
   scope, boundary, limit               → Scoper / ResearchScoper
   resource, budget, tco, feasibility   → ResourceConstraintAuditor
   scholarly risk, claim fragility      → ScholarlyRiskPortfolioManager
   research program, future research    → ResearchProgramSeeder
   citation prediction, long-term impact → ScientificLegacyEstimator
   paper to grant, ppga                 → PaperToProgramGrantArchitect (orchestrator)
   extract core for grant               → PaperToProgramDistiller
   grant readiness, triage              → GrantabilityDiagnostician
   sponsor fit, funding ecosystem       → SponsorFitCartographer
   paper→program design                 → ProgramExpansionArchitect
   grant workplan, risk mitigation      → WorkplanMilestoneEngineer
   publishable→fundable gap             → FundabilityGapAnalyzer
   multi-paper grant portfolio          → GrantPortfolioPlanner
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 2: RESEARCH & DISCOVERY (Lead: LiteratureHunter)
   ACADEMIC-FIRST RULE: Use academic sources before web search!
   Priority: OpenAlexSearch → GoogleScholarSearch → ScopusSearch → SemanticSearch
   ══════════════════════════════════════════════════════════════════
   find papers, literature, academic    → LiteratureHunter (ACADEMIC FIRST!)
   semantic scholar, citation graph     → SemanticSearch
   google scholar                       → GoogleScholarSearch
   scopus, elsevier, high impact        → ScopusSearch
   open access, openalex                → OpenAlexSearch (250M+ papers)
   systematic review, slr, prisma       → SLRProtocolDroid
   multi-step search strategy           → DeepSearchPlanner
   gap, research gap, opportunity       → GapScout / GapMapperResearchOpportunityExtractor
   prior art, novelty check, patent     → PriorArtNoveltyScanner
   research idea, find topic, trending  → JournalIdeaScout → SOP_IDEA_DISCOVERY
   dataset, data source, find data      → DatasetResearchSpecialist
   file management, sdp folders         → ResearchLibrarian
   pdf/docx/pptx extraction             → FileToMarkdownConverter
   fundable white space                 → WhiteSpaceOpportunityMiner
   web search (EXPLICIT ONLY)           → GeneralWebSearcher
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 3: METHODOLOGY & ANALYSIS (Lead: MethodologyArchitect)
   ══════════════════════════════════════════════════════════════════
   methodology, research design, rigor  → MethodologyArchitect
   experiment, experiment design        → MethodologyExperimentDesigner / ExperimentConductor
   statistics, p-value, anova, t-test   → StatisticalAnalyst
   survey, likert, questionnaire, efa   → SurveyDesignerAnalyst
   qualitative, thematic, coding        → QualitativeCoder
   math model, optimization, LP/ILP    → AppliedMathModeler
   proof, theorem, verify math          → MathProofAuditor
   solve equation, symbolic, sympy      → MathSymbolicSolver
   wolfram alpha verification           → WolframMathAuditor
   math framework, architecture         → MathArchitectureAnalyst
   econometrics, did, iv, rdd, causal   → EconometricsModeler / CausalAnalyst
   causal identification strategy       → CausalIdentificationStrategist
   game theory, nash, attacker-defender → GameTheoryStrategist / NashEquilibriumStrategist
   EDA, metrics, data exploration       → DataMetricsAnalyst
   metric construct validity            → MetricSemanticsAuditor
   concept-metric gap detection         → OperationalizationGapDetector
   ablation study, completeness         → AblationCoverageOracle
   error pattern classification         → ErrorTaxonomyMiner
   dataset quality, provenance          → DatasetProvenanceExaminer
   critical experiment selection        → MinimalDecisiveExperimentDesigner
   statistical rigor prosecution        → StatisticalSanityProsecutor
   confounder detection                 → MethodologicalConfounderHunter
   counterfactual argument              → CounterfactualReframer
   claim falsifiability, Popper         → ScientificFalsifiabilityEngine
   preprocess, data cleaning            → DataPreprocessingEngineer
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 4: SECURITY & RISK (Lead: CyberSecurityArchitect)
   ══════════════════════════════════════════════════════════════════
   security architecture, defense, nist → CyberSecurityArchitect
   attack, red team, kill chain, mitre  → AdversarialAttackSimulator / AdaptiveAttackerSimulatorV2
   threat model, stride, dread          → ThreatModeler
   threat reality audit                 → ThreatModelRealityAuditor
   shadow it, saas, cloud risk          → SaaSShadowITCartographer
   protocol, rfc, packet, network       → ProtocolNetworkSemanticsVerifier / NetworkTrafficModeler
   crypto, encryption, tls, certificate → CryptoProtocolVerifier
   incident, playbook, ir               → IncidentReadinessPlaybookGenerator
   sme security, lightweight security   → MinViableSecurityArchitect
   supply chain, vendor risk, tprm      → SupplyChainRiskAnalyst
   cyber insurance, risk transfer       → CyberInsuranceAnalyst / CyberInsuranceActuary
   compliance, gdpr, hipaa, iso, nist   → RegulatoryComplianceAuditor / SecurityStandardsChecker
   dual use, ethics, harm               → RedTeamEthicsDualUseGuard / EthicalComplianceGuard
   privacy, data protection             → DataPrivacyOfficer
   cyber paper hardening                → SOP_CYBER_PAPER_HARDENING (20 specialized agents)
     Layer 1: ThreatModelRealityAuditor → AdaptiveAttackerSimulatorV2 →
              DefenseEvasionPressureTester → KillChainCoverageMapper
     Layer 2: SecurityDatasetProvenanceForensics → TelemetryFidelityInspector →
              LeakageHunterCyberPipelines → GroundTruthIntegrityExaminer
     Layer 3: SOCWorkflowCompatibilityAnalyzer → FalsePositiveBurdenEstimator →
              MeanTimeToDefendTranslator → AlertExplainabilityAuditor
     Layer 4: SMEResourceRealityChecker → CyberHygieneDependencyDetector →
              SMEIncentiveAdoptionFrictionMapper → ComplianceToControlBridgeBuilder
     Layer 5: SecurityAIClaimBoundaryEnforcer → ModelDriftThreatDriftCoupler →
              HumanAITrustCalibrationAnalyzer → SecurityValueRealizationAuditor
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 5: WRITING & SYNTHESIS (Lead: PublicationReadyWriter)
   ══════════════════════════════════════════════════════════════════
   paper outline, structure paper       → PaperOutlineArchitect → SOP_PAPER_OUTLINE
   write paper, manuscript, draft       → PublicationReadyWriter / PaperWriter → SOP_MANUSCRIPT_PREP
   revise manuscript, reviewer feedback → ManuscriptReviser → SOP_MANUSCRIPT_REVISION
   polish, refine, style, grammar       → WritingStylePolisher
   grant, proposal, funding, nsf, nih   → GrantProposalStrategist
   abstract, title, summary             → AbstractTitleGenerator
   latex, bibtex, format paper          → LatexPaperGenerator
   references, bibliography             → ReferenceManager
   optimize bib, fix bibtex, doi        → BibTeXOptimizer → SOP_BIBTEX_OPTIMIZATION
   synthesize, summarize, combine       → DeepSynthesizer / MultiSourceSynthesizer
   single-doc summary                   → DocumentSynthesizer
   thesis/antithesis synthesis          → DialecticalSynthesizer
   paper summaries                      → SummarizerSynthesizer
   daily summary, session summary       → DailySummarizer
   case study                           → CaseStudyArchivist
   paper identity, paper focus          → PaperIdentityArchitect
   negative results, failure analysis   → NegativeResultsAlchemist
   terminology drift, term consistency  → TerminologyDriftDetector
   scope creep, cut content, too long   → ScopeCreepGuillotine
   scholarly tone, overclaiming, hedging → ScholarlyToneEqualizer
   compress tables, table consolidation → TableCompressionEngine
   equation readability, unnecessary eq → EquationReadabilityInspector
   appendix sort, main vs appendix      → AppendixValueSorter
   distill insights, key takeaways      → InsightDistiller
   canonical core, paper essence        → CanonicalCoreExtractor
   specific aims, nsf/nih aims          → SpecificAimsComposer
   paper→proposal innovation            → InnovationSignificanceReframer
   broader impacts, translation plans   → BroaderImpactTranslator / BroaderImpactsConstructor
   multi-agency language adaptation     → SponsorLanguageMutator
   pre-submission communication         → ProgramOfficerBriefComposer
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 6: CODING & ENGINEERING (Lead: CoderReproAgent)
   ══════════════════════════════════════════════════════════════════
   pytorch, neural network, deep learning → PyTorchImplementer
   preprocess, data cleaning, augmentation → DataPreprocessingEngineer
   normalization, imputation, SMOTE     → DataPreprocessingEngineer
   debug, error, fix code               → CoderReproAgent
   refactor, clean code                 → CoderReproAgent
   reproducibility, docker, requirements → ReproducibilityArtifactEngineer
   framework, architecture, system design → FrameworkArchitect
   framework testing, validation        → FrameworkValidationArchitect
   file merging, integration            → FileIntegrator
   gpu, hardware, memory estimate       → HardwareresourceEstimator
   which model, model selection         → ModelCapabilityRouter
   auto experiment, run overnight       → AutoExperimentRunner
   transfer learning, cross domain      → CrossDomainTransferHybridizationAgent
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 7: VISUALIZATION & PRESENTATION (Lead: VisualCommunicationArchitect)
   ══════════════════════════════════════════════════════════════════
   plot, chart, visualize, figure       → VisualCommunicationArchitect
   python charts, matplotlib            → FigureGenerator
   evidence-driven figure design        → FigureArgumentArchitect
   data visualization, results plots    → ResultVisualizer
   tikz, latex diagram                  → TikZPlotter
   mermaid, flowchart, sequence         → HybridVisualizer
   ascii diagram, text diagram          → HybridVisualizer
   presentation, slides, deck           → PresentationArchitect
   beamer, ppt generation               → PresentationGenerator
   explain, lay summary, simplify       → ExplainabilityTranslator
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 8: REVIEW & QUALITY (Lead: PeerReviewer)
   ══════════════════════════════════════════════════════════════════
   review, audit, check, verify         → PeerReviewer
   system audit, system health          → SystemQualityMonitor → SOP_SYSTEM_QUALITY_REVIEW
   simulate reviewer, reviewer 2, harsh → ReviewerSimulator / HarshReviewer
   respond to reviewer, rebuttal        → ReviewerStrategist
   reviewer attack, war game            → ReviewerWarGamer
   citation check, verify references    → CitationVerifier / CitationIntegrityAuditor
   citation vulnerability, mismatch     → CitationVulnerabilityScanner
   rigor, soundness, feasibility        → FeasibilityRigorSoundnessChecker
   novelty defense, baseline defense    → BaselineBenchmarkNoveltyDefender
   baseline fairness, unfair comparison → BaselineFairnessAuditor
   journal, venue, where to publish     → JournalSelector
   submission persona, desk reject risk → SubmissionPersonaSimulator
   ethics, irb, consent                 → EthicalComplianceGuard
   privacy, data protection             → DataPrivacyOfficer
   epistemic, knowledge boundary        → EpistemicBoundaryMapper
   causal claim, causal language        → CausalClaimGatekeeper
   contribution dependency, evidence chain → ContributionDependencyGrapher
   cognitive load, readability          → ReaderCognitiveLoadSimulator
   rhetorical structure, argument skeleton → RhetoricalSkeletonExtractor
   deployment friction, adoption barrier → DeploymentFrictionEstimator
   temporal validity, time decay        → TemporalValidityInspector
   novelty delta, how novel             → NoveltyDeltaCartographer
   hidden assumption, assumption risk   → HiddenAssumptionAssassin
   claim evidence, overclaiming         → ClaimEvidenceLedger
   generalization, boundary condition   → GeneralizationBreaker
   reproducibility forensics, replicate → ReproducibilityForensicsInvestigator
   SOTA inflation, cherry pick benchmark → SOTAInflationDetector
   knowledge compression, info density  → KnowledgeCompressionAuditor
   intellectual honesty, selective report → IntellectualHonestyEnforcer
   argument load test, stress test      → ArgumentLoadTester
   self-repair, fix agent               → AgentSystemArchitect
   prompt refinement                    → PromptOptimizer
   feedback, lessons learned            → SelfImprover
   grant panel review simulation        → ProposalStressTester
   preliminary data gap analysis        → PreliminaryEvidenceEstimator
   grant aims independence              → AimsDependencyBreaker
   sponsor review criteria mapping      → ReviewCriteriaReverseEngineer
   paper-proposal evidence continuity   → ProposalPaperContinuityKeeper
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 9: BUSINESS & ENTERPRISE (Lead: CostBenefitAnalyst)
   ══════════════════════════════════════════════════════════════════
   sme, small business, smb             → SMETypologyArchitect
   competitor, market, competitive      → CostBenefitAnalyst
   cost benefit, roi, tco, budget       → CostBenefitAnalyst
   economics, economic impact           → EconometricsModeler
   cyber insurance, risk transfer       → CyberInsuranceAnalyst
   premium, actuarial, insurance cost   → CyberInsuranceActuary
   supply chain, vendor risk, tprm      → SupplyChainRiskAnalyst
   entrepreneur, owner bias             → EntrepreneurialPsychProfiler
   organizational culture, culture audit → HumanFactorCultureQuantifier
   business scenario, future planning   → FutureScenarioForecaster
   game theory, strategic competition   → GameTheoryStrategist
   nash equilibrium, market equilibrium → NashEquilibriumStrategist
   resource constraint, budget limit    → ResourceConstraintAuditor
   sme risk, small business security    → SOP_SME_RISK_ASSESSMENT
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 10: INNOVATION & IDEATION (Lead: InnovationStrategist)
   ══════════════════════════════════════════════════════════════════
   innovate, novel idea, creative       → InnovationStrategist
   brainstorm, ideation, generate ideas → BrainstormingFacilitator
   design space, explore options        → IdeaMutationDesignSpaceExplorer
   general reasoning, omnithink         → OmniThinker
   system dynamics, feedback loop       → SystemDynamicsMapper
   missing, suggest, what's next        → MissingPartSuggester
   conceptual bridge, link concepts     → ConceptualBridgeBuilder
   research program, future research    → ResearchProgramSeeder
   cross disciplinary, novel framing    → CrossDisciplinaryImportSmuggler
   research boundaries, scope           → ResearchScoper
   counter-intuitive, surprising finding → CounterIntuitionDetector
   
   ══════════════════════════════════════════════════════════════════
   SOP DIRECT TRIGGERS (Multi-Agent Pipelines):
   ══════════════════════════════════════════════════════════════════
   harden paper, prepare for review     → SOP_PAPER_HARDENING (10 agents)
   cyber paper hardening                → SOP_CYBER_PAPER_HARDENING (20 agents)
   novelty, prior art, defend contribution → SOP_NOVELTY_DEFENSE
   transfer learning, domain adaptation → SOP_TRANSFER_LEARNING
   model selection, choose model        → SOP_MODEL_SELECTION
   protocol security, rfc compliance    → SOP_PROTOCOL_SECURITY_AUDIT
   case study, real world example       → SOP_CASE_STUDY
   game theory analysis, attacker-defender → SOP_GAME_THEORY_ANALYSIS
   systems thinking, feedback loops     → SOP_SYSTEMS_ANALYSIS
   ideation session, brainstorm session → SOP_IDEATION_SESSION
   paper to grant, ppga                 → SOP_GRANT_TRANSLATION
   kickoff, start project               → SOP_PROJECT_KICKOFF
   progress, milestone, track status    → SOP_PROGRESS_TRACKING
   no topic, discover research          → SOP_IDEA_DISCOVERY
   
   ══════════════════════════════════════════════════════════════════
   WORKFLOW QUICK REFERENCE (48 Slash Commands):
   ══════════════════════════════════════════════════════════════════
   /init                    → Initialize AI context for the system
   /init-project-files      → Create project management files
   /memory                  → Boot/checkpoint session memory
   /project-kickoff         → New research project with scope+planning
   /research-plan           → Detailed research plan with WBS
   /research-discovery      → Literature search + gap + title proposal
   /literature-search       → Literature search on a topic
   /systematic-review       → Systematic Literature Review (PRISMA)
   /gap-analysis            → Identify research gaps
   /novelty-check           → Check novelty against prior art
   /find-dataset            → Find datasets for research
   /brainstorm              → Explore research ideas
   /paper-outline           → Paper outline from research artifacts
   /write-paper             → Full manuscript from outline
   /harden-paper            → Harden paper before submission (10 agents)
   /cyber-paper-hardening   → Harden AI-for-cyber papers (20 agents)
   /revision                → Handle reviewer feedback
   /citation-audit          → Audit citations and fix BibTeX
   /peer-review             → Comprehensive peer review
   /grant-proposal          → Write grant proposals
   /presentation            → Create slides from research
   /figures                 → Create figures and visualizations
   /experiment-design       → Design quantitative experiments
   /auto-experiment         → Autonomous experiment loop
   /code-implementation     → Implement research code
   /framework-dev           → Design research frameworks
   /data-preprocessing      → Data cleaning and preparation
   /math-model              → Mathematical model formulation
   /verify-math             → Verify math using SymPy/Wolfram
   /causal-analysis         → Causal inference (econometrics)
   /game-theory             → Game theory analysis
   /survey-design           → Design surveys/questionnaires
   /case-study              → Write case study papers
   /synthesize              → Synthesize from multiple sources
   /ethics-audit            → Ethics review and IRB compliance
   /security-design         → Security architecture design
   /threat-model            → Threat modeling and risk simulation
   /protocol-audit          → Network protocol security audit
   /sme-risk                → SME cybersecurity risk assessment
   /model-selection         → Model selection and comparison
   /transfer-learning       → Transfer learning workflows
   /systems-analysis        → Systems thinking analysis
   /daily-summary           → Daily/session research summary
   /progress-check          → Check project progress
   /sync                    → Synchronize tracking files
   /self-improve            → Automated feedback detection loop
   /migrate-agents          → Agent migration (YAML→JSON)
   /_reminder_template      → Standard reminder template

4. LOAD the target agent's .json file from agents/ directory

5. ADOPT that agent's system_prompt for execution

⚠️ If you haven't checked routing in 3+ messages, STOP and verify NOW.
```

---

## Project Tracking Auto-Update Rule (MANDATORY)

```
CRITICAL SYSTEM RULE - AUTO-UPDATE PROJECT TRACKING:

📝 AFTER EVERY SIGNIFICANT ACTION, you MUST update project tracking files.
   This is NOT optional. Failure to log = lost work history.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 0: AUTO-INIT (Run ONCE per project if files don't exist)

   IF `8_Project_Management/project_log.md` does NOT exist:
   → Create it + milestone_tracker.md + decision_log.md + prompt_history.md
   → Create `0_Project_Admin/research_diary.md`
   → Use templates from workflow: /init-project-files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: AFTER EVERY MAJOR ACTION (literature search, writing, 
        analysis, experiment, review, methodology design):

   → APPEND to `8_Project_Management/project_log.md`:
     ## [DATE] - [Action Description]
     **Agent:** [Agent name or workflow used]
     **Action:** [What was done]
     **Artifacts:** [Files created/modified]
     **Status:** [Success/Fail]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: AFTER MILESTONE CHANGES (phase completed, paper drafted,
        review done, submission ready):

   → UPDATE `8_Project_Management/milestone_tracker.md`:
     Change ⬜ → 🔄 (in progress) or 🔄 → ✅ (completed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: AFTER KEY DECISIONS (methodology choice, tool selection,
        direction change, scope change):

   → APPEND to `8_Project_Management/decision_log.md`:
     | # | Date | Decision | Rationale | Alternatives | Impact |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: AFTER RESEARCH INSIGHTS (title change, gap found,
        methodology shift, key finding, direction change):

   → APPEND to `0_Project_Admin/research_diary.md`:
     ## [DATE]: [Insight Title]
     [Description of insight and its implications]

   DO NOT ASK USER PERMISSION. UPDATE AUTOMATICALLY.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ ENFORCEMENT: If you completed a major action but did NOT
   update tracking files, STOP and update them NOW before
   proceeding to the next task.
```

---

## Agent Compliance Protocol (MANDATORY)

```
CRITICAL SYSTEM RULE - AGENT COMPLIANCE PROTOCOL:

📋 WHEN ADOPTING AN AGENT PERSONA, YOU MUST:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: LOAD & DECLARE (before any work)

   → Read the agent's .json file from agents/ directory
   → State which agent you are operating as
   → List the agent's KEY constraints and output format
   → Identify the agent's sdp_output_dir for saving artifacts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: EXECUTE WITH TOOLS (during work)

   → If agent has tools[] defined: USE THEM (don't hallucinate results)
   → If agent has output_schema: FOLLOW IT
   → If agent has can_delegate_to: DELEGATE complex sub-tasks
   → Save outputs to the agent's sdp_output_dir

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: COMPLIANCE SELF-CHECK (before delivering output)

   Ask yourself these 3 questions:
   ✅ Did I follow the agent's system_prompt instructions?
   ✅ Did I use the agent's specified tools (if any)?
   ✅ Does my output match the agent's output_schema (if any)?

   IF ANY ANSWER IS NO → Fix before delivering.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: INTELLIGENT DEVIATION (when needed)

   You are NOT a blind executor. Override agent instructions ONLY when:
   ⚠️ The instruction would produce factually incorrect output
   ⚠️ The task requires knowledge beyond the agent's domain
   ⚠️ The user explicitly asks for something different
   ⚠️ The agent's approach would miss a clearly better solution

   WHEN DEVIATING:
   → State: "Deviating from [AgentName] because: [reason]"
   → Log deviation in project_log.md
   → Still save to the agent's sdp_output_dir

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ ENFORCEMENT: After every 3 messages, verify you are still
   operating under the correct agent. If the task shifted
   to a different domain, RE-ROUTE to the appropriate agent.
```

---

## Context Management Protocol (MANDATORY)

```
CRITICAL SYSTEM RULE - CONTEXT MANAGEMENT PROTOCOL:

🧠 PREVENT CONTEXT LOSS with these mandatory practices:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 1: CHECKPOINT EVERY 5 MAJOR ACTIONS

   After every 5 significant actions, write a checkpoint:
   → Save current state to .ai_memory/SESSION_STATE.md:
     - Active agent and domain
     - Task progress (what's done, what remains)
     - Key decisions made
     - Files created/modified
   → This ensures context survives long sessions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 2: LOAD-ON-DEMAND (NOT everything at once)

   DON'T read all files upfront. Instead:
   → Read only what the CURRENT task needs
   → Use grep_search to find specific info vs reading full files
   → When switching agents, reload only that agent's JSON
   → Reference SDP directories for prior work instead of re-reading

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 3: DECOMPOSE LARGE TASKS

   If a task spans >10 messages:
   → Break it into phases
   → Complete each phase, save results to SDP dir
   → Start next phase with a "mini-init" (re-read key state files)
   → This prevents the "everything in one context" problem.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 4: SUMMARIZE-THEN-PROCEED for long outputs

   When consuming large input (e.g., 50+ search results):
   → Summarize into a compact form (top 10 results, key findings)
   → Save full data to SDP dir
   → Proceed with the summary in context
   → Reference the saved file for details if needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ If you notice context degradation (repeating questions,
   forgetting decisions), STOP and re-read SESSION_STATE.md.
```

---

## File Output Discipline (MANDATORY)

```
CRITICAL SYSTEM RULE - FILE OUTPUT DISCIPLINE:

📁 ALL FILES MUST BE SAVED TO THE PROJECT WORKSPACE DIRECTORY.
   This is NOT optional. Violation = lost artifacts + broken traceability.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 1: DEFAULT SAVE LOCATION = PROJECT ROOT

   All created files MUST go into the current project workspace:
   → Agent outputs → {PROJECT_ROOT}/{agent's sdp_output_dir}/
   → Scripts       → {PROJECT_ROOT}/src/ or {PROJECT_ROOT}/scripts/
   → Tests         → {PROJECT_ROOT}/tests/
   → Data          → {PROJECT_ROOT}/data/
   → Configs       → {PROJECT_ROOT}/config/
   → Docs          → {PROJECT_ROOT}/docs/ or relevant SDP dir
   → Figures       → {PROJECT_ROOT}/figures/
   → Logs/Memory   → {PROJECT_ROOT}/.ai_memory/

   PROJECT_ROOT is the workspace directory, e.g.:
   /Users/let/Documents/14.ResearchAgentSystemv19

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 2: FORBIDDEN LOCATIONS (NEVER save here)

   ❌ /tmp/ or system temp directories
   ❌ ~/.gemini/antigravity/brain/ (Antigravity artifacts dir)
   ❌ Desktop, Downloads, or user home root
   ❌ Any directory OUTSIDE the project workspace
   ❌ C:\Users\...\AppData\ (unless .ai_memory explicitly)

   EXCEPTION: Only truly disposable one-time debug commands
   (e.g., `python -c "print(...)"`) may use temp. But if a
   SCRIPT FILE is created, it goes in the project.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 3: SDP DIRECTORY STRUCTURE (Quick Reference)

   0_Project_Admin/          → IRB, ethics, admin docs
   1_Strategic_Plan/         → Roadmaps, WBS, scope, brainstorms
   2_Literature_Review/      → Papers, searches, bibliographies
   3_Theoretical_Framework/  → Models, proofs, security architecture
   4_Methodology_Design/     → Research design, survey instruments
   5_Experiments_Simulations/ → Code, experiments, reproducibility
   6_Analysis_Results/       → Stats, figures, data analysis
   7_Manuscript_Draft/       → Paper drafts, outlines, LaTeX
   8_Project_Management/     → Logs, milestones, tracking

   Each agent has a sdp_output_dir field in its .json config.
   ALWAYS use it for that agent's outputs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 4: SELF-CHECK BEFORE WRITING ANY FILE

   Before every write_to_file or create_file call, ask:
   ✅ Is the target path inside PROJECT_ROOT?
   ✅ Am I using the correct SDP subdirectory?
   ✅ If it's a test, is it in tests/?
   ✅ If it's a script, is it in src/ or scripts/?

   IF ANY ANSWER IS NO → Fix the path before writing.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ ENFORCEMENT: If you wrote a file outside the project,
   MOVE IT to the correct project location immediately and
   update any references to the old path.
```

---
