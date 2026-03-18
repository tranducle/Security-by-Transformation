# Research Agent System - Quick Start

## 🚀 First Time Setup (New Machine)

1. **Clone/Copy project**
2. **Run `/init`** - This will:
   - Install dependencies (mem0ai package)
   - Load memory and routing rules
   - Check project files

That's it! The system handles everything automatically.

---

## 📋 Daily Usage

| Action | Command |
|--------|---------|
| Start session | `/init` |
| Start new project | `/project-kickoff` |
| Check progress | `/progress-check` |

After `/init`, just describe what you need in natural language.

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.memory/memory.json` | Local memory storage |
| `.agent/rules/memory-rule.md` | Antigravity routing rule |
| `src/tools/mem0_loader.py` | Memory loader script |
| `agents/MasterOrchestrator.json` | Main routing configuration |

---

## 🔧 Manual Memory Check

```bash
python src/tools/mem0_loader.py
```

---

## ⚠️ Troubleshooting

### "Module not found" error

```bash
pip install mem0ai
```

### Memory not loading

Check if `.memory/memory.json` exists. If not:

```bash
python src/tools/mem0_loader.py --init "Project Name" "Topic"
```
