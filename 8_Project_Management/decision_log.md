# Decision Log

| # | Date | Decision | Rationale | Alternatives | Impact |
|---|------|----------|-----------|--------------|--------|
| 1 | 2026-03-17 | Resolve keyword conflicts by making secondary keywords more specific | Prevents routing ambiguity | Remove duplicate keywords entirely | Low risk — more specific keywords still route correctly |
| 2 | 2026-03-17 | Create /harden-paper workflow | 23 hardening agents need a dedicated entry point | Rely only on SOP auto-routing | High value — users can explicitly trigger pipeline |
| 3 | 2026-03-17 | Add hardening steps to write-paper and peer-review workflows | Cross-reference improves discoverability | Keep workflows independent | Medium — better integration |
