"""
Autonomous Experiment Runner — inspired by karpathy/autoresearch.

This module runs experiments autonomously using an LLM (via OpenAI-compatible API)
to iteratively modify experiment code, evaluate results, and keep/discard changes.

GPU training runs as a subprocess (0 AI tokens). Only code reading/modification
calls the LLM API.

Usage:
    # From Antigravity (kick off and walk away):
    python src/tools/auto_experiment_tools.py --config experiment_config.yaml

    # Dry-run (no actual training, tests the pipeline):
    python src/tools/auto_experiment_tools.py --config experiment_config.yaml --dry-run

    # Limit experiments:
    python src/tools/auto_experiment_tools.py --config experiment_config.yaml --max-experiments 10

SECURITY NOTE:
    Commands are executed with shell=True for flexibility (supports pipes, &&, etc).
    Commands must come from trusted configuration files only.
    The following dangerous patterns are blocked:
    - rm -rf /
    - sudo
    - curl | bash
    - eval, exec
"""

import json
import logging
import os
import re
import shlex
import subprocess
import sys
import time
import datetime
import shutil
import urllib.request
import urllib.error
import traceback
from pathlib import Path
from typing import Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dangerous command patterns that should never be allowed
BLOCKED_PATTERNS = [
    r'\brm\s+-rf\s+/',
    r'\bsudo\b',
    r'\bcurl\s+.*\|\s*bash\b',
    r'\bwget\s+.*\|\s*bash\b',
    r'\beval\b',
    r'\bexec\b',
    r'\bchmod\s+777\b',
]


def _validate_command(cmd: str) -> None:
    """
    Validate that a command is safe to execute.

    Args:
        cmd: Command string to validate

    Raises:
        ValueError: If command contains dangerous patterns
    """
    cmd_lower = cmd.lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, cmd_lower):
            raise ValueError(
                f"Security: Command contains blocked pattern '{pattern}'. "
                f"Command: {cmd[:100]}..."
            )

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "experiment": {
        "name": "unnamed_experiment",
        "editable_files": ["train.py"],
        "readonly_files": ["prepare.py"],
        "run_command": "python train.py",
        "timeout_seconds": 300,
        "metric_name": "val_loss",
        "metric_direction": "minimize",  # "minimize" or "maximize"
        "max_experiments": 100,
        "results_file": "results.tsv",
        "work_dir": ".",
    },
    "ai": {
        "api_key": "",
        "base_url": "https://coding-intl.dashscope.aliyuncs.com/v1",
        "model": "MiniMax-M2.5",
        "max_tokens": 4096,
        "temperature": 0.7,
    },
    "git": {
        "enabled": True,
        "branch_prefix": "autoresearch",
        "auto_create_branch": True,
    },
    "hardware": {
        "gpu_name": "auto",          # "auto" = detect, or manual e.g. "RTX 3090"
        "gpu_vram_gb": 0,            # 0 = auto-detect, or manual e.g. 24
        "ram_gb": 0,                  # 0 = auto-detect, or manual e.g. 128
        "cuda_version": "auto",      # "auto" = detect
        "default_gpu_name": "NVIDIA GeForce RTX 3090",
        "default_gpu_vram_gb": 24,
        "default_ram_gb": 128,
    },
}


def load_config(config_path: str) -> dict:
    """Load experiment config from YAML file, merging with defaults."""
    config = DEFAULT_CONFIG.copy()

    if not os.path.exists(config_path):
        print(f"[WARN] Config file not found: {config_path}, using defaults")
        return config

    # Simple YAML parser (avoid external dependency)
    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
    except ImportError:
        # Fallback: try JSON
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = json.load(f)

    # Deep merge
    for section in ["experiment", "ai", "git", "hardware"]:
        if section in user_config:
            config[section].update(user_config[section])

    return config


def load_aimodel_config(project_root: str) -> dict:
    """Load API config from .aimodel file."""
    aimodel_path = os.path.join(project_root, ".aimodel")
    result = {}

    if not os.path.exists(aimodel_path):
        return result

    with open(aimodel_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or not line:
                continue
            # Parse: export KEY="VALUE"
            match = re.match(r'export\s+(\w+)="([^"]*)"', line)
            if match:
                key, value = match.groups()
                if key == "OPENAI_API_KEY":
                    result["api_key"] = value
                elif key == "OPENAI_BASE_URL":
                    result["base_url"] = value
            # Parse: model = "VALUE"
            match = re.match(r'model\s*=\s*"([^"]*)"', line)
            if match:
                result["model"] = match.group(1)

    return result


# ---------------------------------------------------------------------------
# Hardware Detection (0 tokens — runs locally)
# ---------------------------------------------------------------------------

def detect_hardware(config: dict) -> dict:
    """
    Detect hardware specs (GPU, RAM, CUDA) to maximize utilization.
    Falls back to config defaults if detection fails.

    THIS COSTS 0 AI TOKENS. Pure local detection.

    Returns dict with: gpu_name, gpu_vram_gb, ram_gb, cuda_version
    """
    hw_cfg = config.get("hardware", {})
    result = {
        "gpu_name": hw_cfg.get("default_gpu_name", "Unknown GPU"),
        "gpu_vram_gb": hw_cfg.get("default_gpu_vram_gb", 24),
        "ram_gb": hw_cfg.get("default_ram_gb", 128),
        "cuda_version": "unknown",
    }

    # --- GPU Detection via nvidia-smi ---
    if hw_cfg.get("gpu_name", "auto") == "auto" or hw_cfg.get("gpu_vram_gb", 0) == 0:
        try:
            smi = subprocess.run(
                "nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits",
                shell=True, capture_output=True, text=True, timeout=10,
            )
            if smi.returncode == 0 and smi.stdout.strip():
                parts = smi.stdout.strip().split(",")
                if len(parts) >= 2:
                    result["gpu_name"] = parts[0].strip()
                    vram_mb = float(parts[1].strip())
                    result["gpu_vram_gb"] = round(vram_mb / 1024, 1)
        except Exception:
            pass  # Fall back to defaults
    else:
        # Use manual config values
        if hw_cfg.get("gpu_name", "auto") != "auto":
            result["gpu_name"] = hw_cfg["gpu_name"]
        if hw_cfg.get("gpu_vram_gb", 0) > 0:
            result["gpu_vram_gb"] = hw_cfg["gpu_vram_gb"]

    # --- RAM Detection ---
    if hw_cfg.get("ram_gb", 0) == 0:
        try:
            import platform
            if platform.system() == "Windows":
                wmic = subprocess.run(
                    "wmic ComputerSystem get TotalPhysicalMemory /value",
                    shell=True, capture_output=True, text=True, timeout=10,
                )
                for line in wmic.stdout.strip().split("\n"):
                    if "TotalPhysicalMemory" in line:
                        bytes_val = int(line.split("=")[1].strip())
                        result["ram_gb"] = round(bytes_val / (1024**3))
            else:
                with open("/proc/meminfo") as f:
                    for line in f:
                        if line.startswith("MemTotal"):
                            kb = int(line.split()[1])
                            result["ram_gb"] = round(kb / (1024**2))
                            break
        except Exception:
            pass  # Fall back to defaults
    else:
        result["ram_gb"] = hw_cfg["ram_gb"]

    # --- CUDA Version ---
    if hw_cfg.get("cuda_version", "auto") == "auto":
        try:
            nvcc = subprocess.run(
                "nvcc --version", shell=True, capture_output=True, text=True, timeout=10,
            )
            if nvcc.returncode == 0:
                match = re.search(r'release (\d+\.\d+)', nvcc.stdout)
                if match:
                    result["cuda_version"] = match.group(1)
        except Exception:
            # Try nvidia-smi fallback
            try:
                smi = subprocess.run(
                    "nvidia-smi --query-gpu=driver_version --format=csv,noheader",
                    shell=True, capture_output=True, text=True, timeout=10,
                )
                if smi.returncode == 0:
                    result["cuda_version"] = f"driver {smi.stdout.strip()}"
            except Exception:
                pass
    else:
        result["cuda_version"] = hw_cfg["cuda_version"]

    return result


def format_hardware_info(hw: dict) -> str:
    """Format hardware info as a readable string."""
    lines = [
        f"  GPU:         {hw['gpu_name']}",
        f"  GPU VRAM:    {hw['gpu_vram_gb']} GB",
        f"  System RAM:  {hw['ram_gb']} GB",
        f"  CUDA:        {hw['cuda_version']}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM Client (OpenAI-compatible — the ONLY part that costs tokens)
# ---------------------------------------------------------------------------

def call_llm(
    messages: list[dict],
    config: dict,
    max_tokens: int = 4096,
    temperature: float = 0.7,
) -> str:
    """
    Call LLM via OpenAI-compatible API. Returns the assistant's response text.

    THIS IS THE ONLY FUNCTION THAT COSTS AI TOKENS.
    GPU training, file I/O, git operations — all free.
    """
    url = f"{config['ai']['base_url']}/chat/completions"

    payload = {
        "model": config["ai"]["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['ai']['api_key']}",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            tokens_used = usage.get("total_tokens", "?")
            print(f"    [LLM] {config['ai']['model']} | tokens: {tokens_used}")
            return content
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"    [LLM ERROR] HTTP {e.code}: {body[:300]}")
        raise
    except Exception as e:
        print(f"    [LLM ERROR] {type(e).__name__}: {e}")
        raise


# ---------------------------------------------------------------------------
# File Operations (0 tokens)
# ---------------------------------------------------------------------------

def read_files(file_list: list[str], work_dir: str) -> dict[str, str]:
    """Read multiple files and return {filename: content}."""
    result = {}
    for fname in file_list:
        fpath = os.path.join(work_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                result[fname] = f.read()
        else:
            print(f"    [WARN] File not found: {fpath}")
    return result


def write_file(filepath: str, content: str) -> None:
    """Write content to file."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def backup_files(file_list: list[str], work_dir: str) -> dict[str, str]:
    """Create in-memory backup of files before modification."""
    return read_files(file_list, work_dir)


def restore_files(backups: dict[str, str], work_dir: str) -> None:
    """Restore files from backup."""
    for fname, content in backups.items():
        write_file(os.path.join(work_dir, fname), content)


# ---------------------------------------------------------------------------
# Code Modification (uses LLM — costs tokens)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an autonomous experiment runner. Your job is to modify
experiment code to improve the target metric.

RULES:
1. You ONLY modify the editable files listed below. Never modify readonly files.
2. Each change should be ONE focused idea (e.g., change learning rate, add dropout,
   modify architecture). Don't make multiple unrelated changes at once.
3. Keep changes small and reviewable. Prefer simplicity.
4. If removing code achieves equal or better results, that's a WIN.
5. Learn from previous experiment results to guide your next idea.
6. Be creative but practical -- OOM crashes waste time.
7. MAXIMIZE HARDWARE UTILIZATION: Use the hardware specs provided below to choose
   appropriate batch sizes, model sizes, and memory settings. Don't be conservative
   -- push the hardware to its limits while avoiding OOM. For example:
   - With 24GB VRAM: use larger batch sizes, enable mixed precision (fp16/bf16)
   - With 128GB RAM: use larger datasets in memory, more data workers
   - Use gradient accumulation if single-batch OOMs but you want a larger effective batch

OUTPUT FORMAT:
You MUST respond with a JSON object containing:
{
    "idea": "Brief description of what you're trying",
    "changes": [
        {
            "file": "filename.py",
            "search": "exact text to find (multi-line ok)",
            "replace": "replacement text"
        }
    ]
}

Do NOT include any text outside the JSON object. No markdown fences, no explanation."""


def build_experiment_prompt(
    editable_files: dict[str, str],
    readonly_files: dict[str, str],
    results_history: str,
    config: dict,
) -> list[dict]:
    """Build the prompt for the LLM to propose a code change."""
    exp = config["experiment"]

    context_parts = []

    # Readonly files (context only)
    for fname, content in readonly_files.items():
        context_parts.append(f"=== READONLY: {fname} ===\n{content}\n")

    # Editable files
    for fname, content in editable_files.items():
        context_parts.append(f"=== EDITABLE: {fname} ===\n{content}\n")

    # Results history
    if results_history.strip():
        context_parts.append(f"=== EXPERIMENT HISTORY (results.tsv) ===\n{results_history}\n")
    else:
        context_parts.append("=== EXPERIMENT HISTORY ===\nNo experiments run yet. First run should establish a baseline WITHOUT changes.\n")

    user_msg = "\n".join(context_parts)
    user_msg += f"\n\nTarget metric: {exp['metric_name']} (goal: {exp['metric_direction']})"
    user_msg += f"\nTimeout: {exp['timeout_seconds']} seconds per experiment"

    # Inject hardware info so LLM can optimize for the machine
    hw = config.get("_hardware_info")
    if hw:
        user_msg += f"\n\n=== HARDWARE SPECS ==="
        user_msg += f"\nGPU: {hw['gpu_name']} ({hw['gpu_vram_gb']} GB VRAM)"
        user_msg += f"\nRAM: {hw['ram_gb']} GB"
        user_msg += f"\nCUDA: {hw['cuda_version']}"
        user_msg += f"\nMaximize utilization of this hardware. Use large batch sizes, fp16/bf16 if applicable."

    user_msg += "\n\nPropose ONE focused code change to improve the metric. Respond with JSON only."

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]


def apply_changes(changes: list[dict], work_dir: str) -> tuple[bool, str]:
    """
    Apply search-and-replace changes from LLM response.
    Returns (success, description).
    """
    for change in changes:
        fname = change.get("file", "")
        search = change.get("search", "")
        replace = change.get("replace", "")

        fpath = os.path.join(work_dir, fname)
        if not os.path.exists(fpath):
            return False, f"File not found: {fname}"

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        if search not in content:
            # Try with normalized whitespace
            search_normalized = re.sub(r'\s+', ' ', search.strip())
            content_normalized = re.sub(r'\s+', ' ', content)
            if search_normalized not in content_normalized:
                return False, f"Search text not found in {fname}"
            # If normalized match works, do line-by-line matching
            # Fall back to writing the whole replacement
            content = content.replace(search.strip(), replace.strip())
        else:
            content = content.replace(search, replace, 1)

        write_file(fpath, content)

    return True, "Changes applied successfully"


def parse_llm_response(response: str) -> Optional[dict]:
    """Parse JSON from LLM response, handling markdown fences."""
    # Strip markdown code fences if present
    response = response.strip()
    if response.startswith("```"):
        lines = response.split("\n")
        # Remove first and last fence lines
        lines = [l for l in lines if not l.strip().startswith("```")]
        response = "\n".join(lines)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from mixed content
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return None


# ---------------------------------------------------------------------------
# Experiment Execution (0 tokens — GPU only)
# ---------------------------------------------------------------------------

def run_experiment(config: dict, dry_run: bool = False) -> dict:
    """
    Run the experiment command as a subprocess.

    THIS COSTS 0 AI TOKENS. Only GPU/CPU compute.

    Returns dict with keys: success, metric_value, peak_memory, output, duration
    """
    exp = config["experiment"]
    work_dir = exp.get("work_dir", ".")
    timeout = exp["timeout_seconds"] + 60  # Extra buffer for startup

    if dry_run:
        print("    [DRY-RUN] Simulating experiment...")
        time.sleep(2)
        import random
        fake_metric = round(random.uniform(0.5, 1.5), 6)
        return {
            "success": True,
            "metric_value": fake_metric,
            "peak_memory_mb": 0,
            "output": f"[DRY-RUN] {exp['metric_name']}: {fake_metric}",
            "duration_seconds": 2.0,
        }

    cmd = exp["run_command"]
    log_file = os.path.join(work_dir, "run.log")

    # Security: Validate command before execution
    try:
        _validate_command(cmd)
    except ValueError as e:
        logger.error(f"Command validation failed: {e}")
        return {
            "success": False,
            "metric_value": 0.0,
            "peak_memory_mb": 0,
            "output": f"SECURITY: {str(e)}",
            "duration_seconds": 0.0,
        }

    logger.info(f"Executing command: {cmd}")
    print(f"    [RUN] {cmd} (timeout: {exp['timeout_seconds']}s)")
    start = time.time()

    try:
        # SECURITY: shell=True is used for flexibility (pipes, &&, etc)
        # Commands are validated above to block dangerous patterns
        # Commands must come from trusted configuration files only
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        duration = time.time() - start
        output = result.stdout + "\n" + result.stderr

        # Save log
        write_file(log_file, output)

        if result.returncode != 0:
            return {
                "success": False,
                "metric_value": 0.0,
                "peak_memory_mb": 0,
                "output": output[-2000:],  # Last 2000 chars
                "duration_seconds": duration,
            }

        # Parse metric from output
        metric_value = parse_metric(output, exp["metric_name"])
        peak_memory = parse_metric(output, "peak_vram_mb") or parse_metric(output, "peak_memory_mb") or 0

        return {
            "success": True,
            "metric_value": metric_value,
            "peak_memory_mb": peak_memory,
            "output": output[-2000:],
            "duration_seconds": duration,
        }

    except subprocess.TimeoutExpired:
        duration = time.time() - start
        return {
            "success": False,
            "metric_value": 0.0,
            "peak_memory_mb": 0,
            "output": f"TIMEOUT after {duration:.0f}s",
            "duration_seconds": duration,
        }
    except Exception as e:
        duration = time.time() - start
        return {
            "success": False,
            "metric_value": 0.0,
            "peak_memory_mb": 0,
            "output": f"{type(e).__name__}: {e}",
            "duration_seconds": duration,
        }


def parse_metric(output: str, metric_name: str) -> Optional[float]:
    """Extract a metric value from experiment output."""
    # Pattern: metric_name: 0.12345 or metric_name=0.12345
    patterns = [
        rf'{metric_name}\s*[:=]\s*([\d.]+(?:e[+-]?\d+)?)',
        rf'"{metric_name}"\s*[:=]\s*([\d.]+(?:e[+-]?\d+)?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                continue
    return None


# ---------------------------------------------------------------------------
# Git Operations (0 tokens)
# ---------------------------------------------------------------------------

def git_run(cmd: str, work_dir: str) -> tuple[bool, str]:
    """Run a git command and return (success, output)."""
    try:
        result = subprocess.run(
            f"git {cmd}",
            shell=True,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)


def git_setup_branch(config: dict) -> bool:
    """Create experiment branch if configured."""
    git_cfg = config["git"]
    exp_cfg = config["experiment"]
    work_dir = exp_cfg.get("work_dir", ".")

    if not git_cfg.get("enabled"):
        return True

    if not git_cfg.get("auto_create_branch"):
        return True

    today = datetime.date.today().strftime("%b%d").lower()
    branch = f"{git_cfg['branch_prefix']}/{today}"

    ok, _ = git_run(f"checkout -b {branch}", work_dir)
    if not ok:
        # Branch might already exist
        ok, _ = git_run(f"checkout {branch}", work_dir)

    return ok


def git_commit(message: str, config: dict) -> Optional[str]:
    """Commit current changes. Returns short commit hash or None."""
    work_dir = config["experiment"].get("work_dir", ".")
    if not config["git"].get("enabled"):
        return "no-git"

    git_run("add -A", work_dir)
    ok, _ = git_run(f'commit -m "{message}"', work_dir)
    if ok:
        _, hash_str = git_run("rev-parse --short HEAD", work_dir)
        return hash_str
    return None


def git_reset_last(config: dict) -> bool:
    """Reset last commit (discard experiment)."""
    work_dir = config["experiment"].get("work_dir", ".")
    if not config["git"].get("enabled"):
        return True
    ok, _ = git_run("reset --hard HEAD~1", work_dir)
    return ok


# ---------------------------------------------------------------------------
# Results Logging (0 tokens)
# ---------------------------------------------------------------------------

RESULTS_HEADER = "experiment\tcommit\tmetric_value\tmemory_gb\tduration_s\tstatus\tdescription\n"


def init_results_file(config: dict) -> None:
    """Create results.tsv with header if it doesn't exist."""
    results_path = os.path.join(
        config["experiment"].get("work_dir", "."),
        config["experiment"]["results_file"],
    )
    if not os.path.exists(results_path):
        write_file(results_path, RESULTS_HEADER)


def log_result(
    experiment_num: int,
    commit_hash: str,
    metric_value: float,
    memory_mb: float,
    duration: float,
    status: str,
    description: str,
    config: dict,
) -> None:
    """Append one result row to results.tsv."""
    results_path = os.path.join(
        config["experiment"].get("work_dir", "."),
        config["experiment"]["results_file"],
    )
    memory_gb = round(memory_mb / 1024, 1) if memory_mb else 0.0
    # Sanitize description (no tabs/newlines)
    description = description.replace("\t", " ").replace("\n", " ")[:200]

    row = f"{experiment_num}\t{commit_hash}\t{metric_value:.6f}\t{memory_gb}\t{duration:.1f}\t{status}\t{description}\n"

    with open(results_path, "a", encoding="utf-8") as f:
        f.write(row)


def read_results_history(config: dict) -> str:
    """Read current results.tsv content."""
    results_path = os.path.join(
        config["experiment"].get("work_dir", "."),
        config["experiment"]["results_file"],
    )
    if os.path.exists(results_path):
        with open(results_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# ---------------------------------------------------------------------------
# Main Experiment Loop
# ---------------------------------------------------------------------------

def is_better(new_value: float, best_value: float, direction: str) -> bool:
    """Check if new metric is better than best."""
    if direction == "minimize":
        return new_value < best_value
    else:
        return new_value > best_value


def run_loop(config: dict, max_experiments: Optional[int] = None, dry_run: bool = False) -> dict:
    """
    Main autonomous experiment loop.

    Token usage:
        - LLM calls (code read + modify): costs MiniMax tokens
        - GPU training: 0 tokens
        - Git operations: 0 tokens
        - File I/O: 0 tokens

    Returns summary dict.
    """
    exp_cfg = config["experiment"]
    work_dir = exp_cfg.get("work_dir", ".")
    max_exp = max_experiments or exp_cfg.get("max_experiments", 100)
    direction = exp_cfg.get("metric_direction", "minimize")
    metric_name = exp_cfg["metric_name"]

    print("=" * 70)
    print(f"  AUTONOMOUS EXPERIMENT RUNNER")
    print(f"  Experiment:  {exp_cfg['name']}")
    print(f"  Metric:      {metric_name} ({direction})")
    print(f"  Max runs:    {max_exp}")
    print(f"  Timeout:     {exp_cfg['timeout_seconds']}s per experiment")
    print(f"  AI Model:    {config['ai']['model']}")
    print(f"  Work dir:    {os.path.abspath(work_dir)}")
    print(f"  Dry run:     {dry_run}")
    print("=" * 70)

    # Hardware detection (0 tokens)
    hw = detect_hardware(config)
    config["_hardware_info"] = hw  # Inject for LLM prompt
    print(f"  --- Hardware Profile ---")
    print(format_hardware_info(hw))
    print("=" * 70)

    # Setup
    init_results_file(config)
    if config["git"].get("enabled") and not dry_run:
        git_setup_branch(config)

    best_value = float("inf") if direction == "minimize" else float("-inf")
    backups = {}  # Initialize before loop to avoid NameError on early crash
    stats = {
        "total": 0, "kept": 0, "discarded": 0, "crashed": 0,
        "best_value": None, "start_time": time.time(),
    }

    for exp_num in range(1, max_exp + 1):
        print(f"\n{'-' * 70}")
        print(f"  EXPERIMENT {exp_num}/{max_exp}")
        print(f"  Time elapsed: {(time.time() - stats['start_time']) / 60:.1f} min")
        print(f"  Best so far: {best_value if stats['best_value'] is not None else 'N/A'}")
        print(f"{'-' * 70}")

        try:
            # Step 1: Read files (0 tokens)
            editable = read_files(exp_cfg["editable_files"], work_dir)
            readonly = read_files(exp_cfg.get("readonly_files", []), work_dir)
            history = read_results_history(config)

            # Step 2: Ask LLM for code change (COSTS TOKENS)
            if exp_num == 1 and not history.strip().replace(RESULTS_HEADER.strip(), "").strip():
                # First run: establish baseline without changes
                print("  [BASELINE] Running without modifications...")
                idea = "baseline -- no changes"
            else:
                print("  [LLM] Requesting code modification...")
                messages = build_experiment_prompt(editable, readonly, history, config)
                response = call_llm(messages, config)

                parsed = parse_llm_response(response)
                if parsed is None:
                    print("  [SKIP] Failed to parse LLM response")
                    log_result(exp_num, "n/a", 0.0, 0, 0, "crash",
                              "LLM response parse error", config)
                    stats["crashed"] += 1
                    stats["total"] += 1
                    continue

                idea = parsed.get("idea", "unknown change")
                changes = parsed.get("changes", [])
                print(f"  [IDEA] {idea}")

                if changes:
                    # Backup before modification
                    backups = backup_files(exp_cfg["editable_files"], work_dir)

                    ok, msg = apply_changes(changes, work_dir)
                    if not ok:
                        print(f"  [SKIP] Failed to apply changes: {msg}")
                        restore_files(backups, work_dir)
                        log_result(exp_num, "n/a", 0.0, 0, 0, "crash",
                                  f"Apply failed: {msg}", config)
                        stats["crashed"] += 1
                        stats["total"] += 1
                        continue

            # Step 3: Run experiment (0 TOKENS -- GPU only)
            result = run_experiment(config, dry_run=dry_run)
            stats["total"] += 1

            if not result["success"]:
                print(f"  [CRASH] {result['output'][:200]}")
                if exp_num > 1:
                    restore_files(backups, work_dir)
                commit_hash = "n/a"
                log_result(exp_num, commit_hash, 0.0,
                          result["peak_memory_mb"], result["duration_seconds"],
                          "crash", f"CRASH: {idea}", config)
                stats["crashed"] += 1
                continue

            metric_val = result["metric_value"]
            if metric_val is None:
                print(f"  [WARN] Could not parse {metric_name} from output")
                if exp_num > 1:
                    restore_files(backups, work_dir)
                log_result(exp_num, "n/a", 0.0,
                          result["peak_memory_mb"], result["duration_seconds"],
                          "crash", f"Metric not found: {idea}", config)
                stats["crashed"] += 1
                continue

            print(f"  [RESULT] {metric_name} = {metric_val:.6f} | "
                  f"duration = {result['duration_seconds']:.1f}s | "
                  f"memory = {result['peak_memory_mb']:.0f} MB")

            # Step 4: Evaluate (0 tokens)
            if exp_num == 1:
                # Baseline always kept
                best_value = metric_val
                stats["best_value"] = metric_val
                status = "keep"
                commit_hash = git_commit(f"exp{exp_num}: baseline", config) or "n/a"
                print(f"  [KEEP] Baseline established: {metric_val:.6f}")
                stats["kept"] += 1
            elif is_better(metric_val, best_value, direction):
                improvement = abs(metric_val - best_value)  # Calculate BEFORE updating best_value
                best_value = metric_val
                stats["best_value"] = metric_val
                status = "keep"
                commit_hash = git_commit(f"exp{exp_num}: {idea}", config) or "n/a"
                print(f"  [KEEP] >> Improved by {improvement:.6f}! New best: {metric_val:.6f}")
                stats["kept"] += 1
            else:
                status = "discard"
                print(f"  [DISCARD] x No improvement ({metric_val:.6f} vs best {best_value:.6f})")
                restore_files(backups, work_dir)
                if config["git"].get("enabled") and not dry_run:
                    git_run("checkout -- .", work_dir)
                commit_hash = "n/a"
                stats["discarded"] += 1

            log_result(exp_num, commit_hash, metric_val,
                      result["peak_memory_mb"], result["duration_seconds"],
                      status, idea, config)

        except KeyboardInterrupt:
            print("\n\n  [STOP] Interrupted by user.")
            break
        except Exception as e:
            print(f"  [ERROR] {type(e).__name__}: {e}")
            traceback.print_exc()
            stats["crashed"] += 1
            stats["total"] += 1
            if exp_num > 1 and backups:
                restore_files(backups, work_dir)
            continue

    # Summary
    elapsed = (time.time() - stats["start_time"]) / 60
    print(f"\n{'=' * 70}")
    print(f"  EXPERIMENT SESSION COMPLETE")
    print(f"{'=' * 70}")
    print(f"  Total experiments: {stats['total']}")
    print(f"  Kept:              {stats['kept']}")
    print(f"  Discarded:         {stats['discarded']}")
    print(f"  Crashed:           {stats['crashed']}")
    print(f"  Best {metric_name}:  {stats['best_value']}")
    print(f"  Total time:        {elapsed:.1f} minutes")
    print(f"  Results saved to:  {exp_cfg['results_file']}")
    print(f"{'=' * 70}")

    return stats


# ---------------------------------------------------------------------------
# Utility: launch from Antigravity
# ---------------------------------------------------------------------------

def launch_autonomous(config_path: str, max_experiments: int = -1, dry_run: bool = False) -> str:
    """
    Launch the experiment runner as a background process.
    Called by Antigravity to kick off and walk away.

    Returns the process info string.
    """
    script_path = os.path.abspath(__file__)
    cmd = f'python "{script_path}" --config "{config_path}"'
    if max_experiments > 0:
        cmd += f" --max-experiments {max_experiments}"
    if dry_run:
        cmd += " --dry-run"

    # Log file for the session
    log_path = os.path.join(os.path.dirname(config_path), "autoresearch_session.log")
    cmd += f' > "{log_path}" 2>&1'

    print(f"[LAUNCH] Starting autonomous experiment runner...")
    print(f"[LAUNCH] Command: {cmd}")
    print(f"[LAUNCH] Log: {log_path}")

    if sys.platform == "win32":
        # Windows: start detached process
        subprocess.Popen(
            cmd,
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
            close_fds=True,
        )
    else:
        # Unix: nohup background
        subprocess.Popen(
            f"nohup {cmd} &",
            shell=True,
            close_fds=True,
        )

    return f"Autonomous runner started. Check log: {log_path}"


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Autonomous Experiment Runner")
    parser.add_argument("--config", required=True, help="Path to experiment_config.yaml")
    parser.add_argument("--max-experiments", type=int, default=None,
                        help="Max experiments to run (overrides config)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate experiments without actual training")
    args = parser.parse_args()

    # Load config
    config = load_config(args.config)

    # Merge .aimodel config (API keys)
    project_root = os.path.dirname(os.path.abspath(args.config))
    # Search upward for .aimodel
    search_dir = project_root
    for _ in range(5):
        aimodel = load_aimodel_config(search_dir)
        if aimodel:
            config["ai"].update(aimodel)
            break
        parent = os.path.dirname(search_dir)
        if parent == search_dir:
            break
        search_dir = parent

    if not config["ai"].get("api_key"):
        print("[ERROR] No API key found. Set in config or .aimodel file.")
        sys.exit(1)

    # Run
    run_loop(config, max_experiments=args.max_experiments, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
