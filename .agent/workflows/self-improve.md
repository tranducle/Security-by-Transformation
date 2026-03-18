---
description: Automated feedback detection and continuous improvement loop for the AI Research Agent System
---
<!-- SOP: SOP_SELF_REPAIR -->


# Self-Improvement Workflow

## Purpose
Automated feedback detection and continuous improvement loop for the AI Research Agent System.

## Trigger Conditions

### User-Triggered (Explicit Feedback)
- User complains about results ("wrong", "incorrect", "fix this", "not working")
- User says something is not good enough ("chua tot", "sai roi", "lam lai")
- User requests re-execution with corrections

### Self-Triggered (Quality Assessment)
- All tools in execution failed
- Error ratio exceeds 50%
- Results are empty when they shouldn't be
- All tools were skipped (agent-tool mapping issue)

## Pipeline Flow

```
User Message
    ↓
[feedback_detector] ← NEW: First node in pipeline
    ├─ detect_feedback(message) → is_feedback, patterns
    ├─ load_previous_execution() → previous context
    └─ build_feedback_context() → feedback_context dict
    ↓
[optimize_prompt]
    ├─ Steps 0-3: Language, Intent, Domain, Restructure
    └─ Step 4 (NEW): inject_lessons_into_prompt()
        ├─ search_lessons(query) → relevant past lessons
        └─ format as "## SYSTEM LESSONS LEARNED" block
    ↓
[... normal pipeline ...]
    ↓
[output_builder] ← Enhanced with quality assessment
    ├─ assess_execution_quality() → quality_score, issues
    ├─ save_auto_lessons() → persist for future runs
    └─ save feedback-triggered lesson if is_feedback=True
```

## Lessons Learned Database

**Location**: `.memory/lessons/lessons_learned.json`

**Lesson Schema**:
```json
{
  "id": "8-char-uuid",
  "timestamp": "ISO datetime",
  "trigger": "user | auto",
  "agent": "agent_name",
  "issue": "description of what went wrong",
  "resolution": "how to avoid/fix in future",
  "keywords": ["searchable", "terms"],
  "applied_count": 0
}
```

**Limits**: Max 200 lessons. Pruned by lowest applied_count + oldest timestamp.

## Integration Points

| Component | File | Change |
|-----------|------|--------|
| State fields | `state.py` | `is_feedback`, `feedback_context`, `lessons_applied`, `quality_assessment` |
| Core logic | `feedback_handler.py` | Detection, lessons DB, quality assessment |
| Pipeline entry | `graph.py` | `feedback_detection_node` as first node |
| Prompt injection | `prompt_optimizer.py` | `inject_lessons_into_prompt()` at Step 4 |
| Quality check | `output_builder.py` | Post-execution assessment + auto-lesson saving |
| Context snapshot | `memory.py` | Lessons summary in context snapshot |
| Agent config | `agents/SelfImprover.json` | Agent definition |
| System config | `config.yaml` | `self_improvement` section |

## Configuration

In `config.yaml`:
```yaml
self_improvement:
  enabled: true
  max_lessons: 200
  auto_detect: true
  feedback_detection: true
```

## Example Scenarios

### Scenario 1: User Complaint
```
User: "The search results were wrong, it didn't find any cybersecurity papers"
→ feedback_detector: is_feedback=True, loads previous execution
→ prompt_optimizer: injects lesson "Ensure cybersecurity queries use all 4 academic databases"
→ Pipeline re-runs with corrective context
→ output_builder: saves lesson for future reference
```

### Scenario 2: Auto-Detection
```
Pipeline executes → all 3 tools fail with timeout errors
→ output_builder: quality_score=0.0, issues=["all_tools_failed"]
→ Auto-saves lesson: "Tool timeouts detected for agent X — check API connectivity"
→ Next execution: lesson injected into prompt as warning
```
