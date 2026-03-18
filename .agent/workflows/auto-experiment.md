---
description: Autonomous experiment loop — setup, kick off, and analyze results
---
<!-- SOP: SOP_AUTO_EXPERIMENT -->


# Autonomous Experiment Runner

Inspired by karpathy/autoresearch. Antigravity sets up everything, launches a standalone
Python process that calls MiniMax-M2.5 to iteratively modify code + train + evaluate,
then Antigravity analyzes results in the next session.

// turbo-all

## Step 1: Understand Requirements

Ask user (if not already clear):

1. **What type of experiment?** (ML training, simulation, benchmark, etc.)
2. **Where is the dataset?** (path to processed data, or raw data to preprocess)
3. **What metric are you tracking?** (val_loss, F1, accuracy, etc.)
4. **Minimize or maximize?**
5. **Which file(s) should the AI modify?** (e.g., `train.py`)
6. **Which file(s) are read-only context?** (e.g., `prepare.py`, `data_loader.py`)
7. **How many experiments?** (default: 100, or -1 for unlimited)

## Step 2: Prepare Dataset (if needed)

If user provides raw data:

```bash
# Create experiment directory
mkdir -p 5_Experiments_Simulations/{EXPERIMENT_NAME}/data

# Write and run preprocessing script
python 5_Experiments_Simulations/{EXPERIMENT_NAME}/prepare.py
```

If data is already processed, skip to Step 3.

## Step 3: Write Training Code

Create or verify the training script:

```
5_Experiments_Simulations/{EXPERIMENT_NAME}/
├── prepare.py       ← Data prep + evaluation (READONLY)
├── train.py         ← Model + training loop (AI MODIFIES THIS)
├── data/            ← Processed dataset
└── requirements.txt ← Dependencies
```

**Critical**: The training script MUST print the metric in this format:
```
metric_name: 0.123456
```

Example: `val_loss: 0.847200` or `f1_score: 0.923100`

## Step 4: Run Baseline

```bash
cd 5_Experiments_Simulations/{EXPERIMENT_NAME}
python train.py
```

Verify: metric is printed, no crashes, runs within timeout.

## Step 5: Create Config

Create `experiment_config.yaml`:

```yaml
experiment:
  name: "{EXPERIMENT_NAME}"
  editable_files: ["train.py"]
  readonly_files: ["prepare.py"]
  run_command: "python train.py"
  timeout_seconds: 300
  metric_name: "val_loss"
  metric_direction: "minimize"
  max_experiments: 100
  results_file: "results.tsv"
  work_dir: "5_Experiments_Simulations/{EXPERIMENT_NAME}"

ai:
  # Auto-loaded from .aimodel — no need to repeat here

git:
  enabled: true
  branch_prefix: "autoresearch"
  auto_create_branch: true
```

## Step 6: Initialize Git Branch

```bash
cd 5_Experiments_Simulations/{EXPERIMENT_NAME}
git init
git add -A
git commit -m "initial: experiment setup"
```

## Step 7: Launch Autonomous Runner

```bash
python src/tools/auto_experiment_tools.py --config experiment_config.yaml --max-experiments 100
```

**Or launch as background process (for overnight runs):**

```powershell
# Windows
Start-Process -NoNewWindow -FilePath python -ArgumentList "src/tools/auto_experiment_tools.py --config experiment_config.yaml" -RedirectStandardOutput "autoresearch_session.log" -RedirectStandardError "autoresearch_errors.log"
```

## Step 8: Notify User

Tell the user:
> "Thực nghiệm tự động đã được khởi chạy! 🚀
>  - Experiment: {EXPERIMENT_NAME}
>  - Max runs: {N}
>  - Estimated time: ~{N * timeout / 60} hours
>  - Results file: results.tsv
>  - Session log: autoresearch_session.log
>
> Bạn có thể đi ngủ. Sáng mai gọi /init rồi nói 'phân tích kết quả thực nghiệm'."

## Step 9: Analyze Results (Next Session)

When user returns:

```bash
# Quick summary
cat 5_Experiments_Simulations/{EXPERIMENT_NAME}/results.tsv

# Or use Python
python -c "
import csv
with open('results.tsv') as f:
    reader = csv.DictReader(f, delimiter='\t')
    rows = list(reader)
    kept = [r for r in rows if r['status'] == 'keep']
    print(f'Total: {len(rows)}, Kept: {len(kept)}, Best: {min(r[\"metric_value\"] for r in kept if float(r[\"metric_value\"]) > 0):.6f}')
"
```

Create analysis report in `6_Analysis_Results/`.

---

## When to Use This Workflow

| Trigger | Example |
|---------|---------|
| "triển khai thực nghiệm" | Vietnamese trigger |
| "run experiments overnight" | English trigger |
| "tối ưu model tự động" | Auto-optimize |
| "chạy autoresearch" | Direct reference |
| `/auto-experiment` | Slash command |

## Token Cost Breakdown

| Component | Tokens Used |
|-----------|------------|
| GPU training (subprocess) | **0** |
| Git operations | **0** |
| File read/write | **0** |
| Results logging | **0** |
| LLM code analysis (per experiment) | ~1K-3K MiniMax tokens |
| Total per 100 experiments | ~100K-300K MiniMax tokens |
