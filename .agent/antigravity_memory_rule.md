# Antigravity Custom Rules - Memory Persistence

Add this content to your Antigravity settings under **User Rules** or **Custom System Instructions**.

---

## Memory Check Rule (Every 3 Messages)

```
CRITICAL SYSTEM RULE - AGENT ROUTING & MEMORY CHECK:

🧠 EVERY 3 USER MESSAGES, PAUSE and:

1. Run memory check:
   python src/tools/mem0_loader.py [PROJECT_ID]

2. Re-read routing rules from agents/MasterOrchestrator.json Section 6

3. For current task, IDENTIFY keywords and route to correct agent:

   ROUTING QUICK REFERENCE (All 10 Domains):
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 1: STRATEGY & OPERATIONS (Lead: StrategicArchitect)
   ══════════════════════════════════════════════════════════════════
   plan, roadmap, strategy, wbs         → StrategicArchitect
   research plan, detailed plan         → ResearchPlanGenerator
   track, status, log, progress         → ProjectStateKeeper / ProgressTracker
   agile, sprint, kanban                → ProjectPlanner
   scope, boundary                      → Scoper / ResearchScoper
   resource, budget, tco, feasibility   → ResourceConstraintAuditor
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 2: RESEARCH & DISCOVERY (Lead: LiteratureHunter)
   ══════════════════════════════════════════════════════════════════
   find papers, literature, academic    → LiteratureHunter (ACADEMIC FIRST!)
   semantic scholar                     → SemanticSearch
   google scholar                       → GoogleScholarSearch
   systematic review, slr, prisma       → SLRProtocolDroid
   gap, research gap                    → GapScout
   prior art, novelty check             → PriorArtNoveltyScanner
   research idea, find topic            → JournalIdeaScout
   dataset, find data                   → DatasetResearchSpecialist
   web search (EXPLICIT ONLY)           → GeneralWebSearcher
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 3: METHODOLOGY & ANALYSIS (Lead: MethodologyArchitect)
   ══════════════════════════════════════════════════════════════════
   methodology, research design         → MethodologyArchitect
   experiment, experiment design        → MethodologyExperimentDesigner
   statistics, p-value, anova, t-test   → StatisticalAnalyst
   survey, likert, questionnaire        → SurveyDesignerAnalyst
   qualitative, thematic, coding        → QualitativeCoder
   math model, optimization             → AppliedMathModeler
   proof, theorem, verify math          → MathProofAuditor
   econometrics, did, iv, rdd           → EconometricsModeler / CausalAnalyst
   game theory, nash                    → GameTheoryStrategist
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 4: SECURITY & RISK (Lead: CyberSecurityArchitect)
   ══════════════════════════════════════════════════════════════════
   security architecture, defense       → CyberSecurityArchitect
   attack, red team, kill chain         → AdversarialAttackSimulator
   threat model, stride, dread          → ThreatModeler
   shadow it, saas, cloud risk          → SaaSShadowITCartographer
   protocol, rfc, packet, network       → ProtocolNetworkSemanticsVerifier
   crypto, encryption, tls              → CryptoProtocolVerifier
   incident, playbook, ir               → IncidentReadinessPlaybookGenerator
   sme security, lightweight security   → MinViableSecurityArchitect
   supply chain, vendor risk, tprm      → SupplyChainRiskAnalyst
   cyber insurance, risk transfer       → CyberInsuranceAnalyst
   compliance, gdpr, hipaa, iso         → RegulatoryComplianceAuditor
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 5: WRITING & SYNTHESIS (Lead: PublicationReadyWriter)
   ══════════════════════════════════════════════════════════════════
   paper outline, structure paper       → PaperOutlineArchitect
   write paper, manuscript, draft       → PublicationReadyWriter / PaperWriter
   polish, refine, style, grammar       → WritingStylePolisher
   grant, proposal, funding             → GrantProposalStrategist
   abstract, title, summary             → AbstractTitleGenerator
   latex, bibtex, format paper          → LatexPaperGenerator
   references, bibliography             → ReferenceManager
   optimize bib, fix bibtex, doi        → BibTeXOptimizer
   revise manuscript, reviewer feedback → ManuscriptReviser
   synthesize, summarize                → DeepSynthesizer
   case study                           → CaseStudyArchivist
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 6: CODING & ENGINEERING (Lead: CoderReproAgent)
   ══════════════════════════════════════════════════════════════════
   pytorch, neural network, deep learning → PyTorchImplementer
   debug, error, fix code               → CoderReproAgent
   refactor, clean code                 → CoderReproAgent
   reproducibility, docker              → ReproducibilityArtifactEngineer
   framework, system design             → FrameworkArchitect
   gpu, hardware, memory estimate       → HardwareresourceEstimator
   which model, model selection         → ModelCapabilityRouter
   auto experiment, run overnight       → AutoExperimentRunner
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 7: VISUALIZATION (Lead: VisualCommunicationArchitect)
   ══════════════════════════════════════════════════════════════════
   plot, chart, visualize, figure       → VisualCommunicationArchitect
   tikz, latex diagram                  → TikZPlotter
   mermaid, flowchart, sequence         → HybridVisualizer
   presentation, slides, deck           → PresentationArchitect
   ascii diagram, text diagram          → HybridVisualizer
   explain, lay summary, simplify       → ExplainabilityTranslator
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 8: REVIEW & QUALITY (Lead: PeerReviewer)
   ══════════════════════════════════════════════════════════════════
   review, audit, check, verify         → PeerReviewer
   simulate reviewer, reviewer 2        → ReviewerSimulator / HarshReviewer
   respond to reviewer, rebuttal        → ReviewerStrategist
   citation check, verify references    → CitationVerifier
   rigor, soundness, feasibility        → FeasibilityRigorSoundnessChecker
   journal, venue, where to publish     → JournalSelector
   ethics, irb, consent                 → EthicalComplianceGuard
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 9: BUSINESS & ENTERPRISE (Lead: CostBenefitAnalyst)
   ══════════════════════════════════════════════════════════════════
   sme, small business, smb             → SMETypologyArchitect
   competitor, market analysis          → CostBenefitAnalyst
   cost benefit, roi, tco               → CostBenefitAnalyst
   cyber insurance, premium             → CyberInsuranceAnalyst / Actuary
   entrepreneur, owner bias             → EntrepreneurialPsychProfiler
   organizational culture               → HumanFactorCultureQuantifier
   business scenario, future planning   → FutureScenarioForecaster
   
   ══════════════════════════════════════════════════════════════════
   DOMAIN 10: INNOVATION & IDEATION (Lead: InnovationStrategist)
   ══════════════════════════════════════════════════════════════════
   innovate, novel idea, creative       → InnovationStrategist
   brainstorm, ideation, generate ideas → BrainstormingFacilitator
   design space, explore options        → IdeaMutationDesignSpaceExplorer
   system dynamics, feedback loop       → SystemDynamicsMapper
   missing, suggest, what's next        → MissingPartSuggester

4. LOAD the target agent's .json file from agents/ directory

5. ADOPT that agent's system_prompt for execution

⚠️ If you haven't checked routing in 3+ messages, STOP and verify NOW.
```

---

## How to Add to Antigravity

### Option 1: VS Code Settings

1. Open VS Code Settings (`Ctrl+,`)
2. Search for "Antigravity" or "Claude"
3. Find "Custom System Instructions" or "User Rules"
4. Paste the rule above

### Option 2: Settings JSON

Add to your `settings.json`:

```json
{
  "antigravity.customRules": [
    "CRITICAL SYSTEM RULE - AGENT ROUTING & MEMORY CHECK: Every 3 user messages, run python src/tools/mem0_loader.py, re-read routing rules from agents/MasterOrchestrator.json Section 6, identify keywords in request, route to correct agent, load agent's system_prompt and ADOPT it for execution."
  ]
}
```

---

## Verification

After adding the rule, test with:

1. Start a new session
2. Send 3 messages without /init
3. AI should pause and acknowledge memory check
4. Request "create tikz diagram" → should route to TikZPlotter
