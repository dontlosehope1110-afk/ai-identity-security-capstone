# 03-red-team

AI identity red team exercise against a simulated vulnerable agent (DocBot),
using Google Gemini (gemini-3.5-flash-lite) as the underlying model.

Contents:
- lab.py: shared setup (system prompts, attack payloads, API call wrapper)
- a1.py: Attack 1 — Indirect prompt injection (JWT exfiltration)
- a2.py: Attack 2 — Agent identity spoofing (forged orchestrator message)
- a3.py: Attack 3 — System prompt extraction (5 techniques) + role escalation
- a4.py: Attack 4 — RAG poisoning / simulated MCP tool abuse
- matrix.py: Attack success rate matrix across all 5 findings (before controls)
- log.jsonl: Full prompt/response log for all attack runs
- P3_01 to P3_08: Screenshots mapped to the Project 3 checklist

Results summary (before any defensive controls):
- Indirect injection: 80-100% success (model-dependent run variance)
- Identity spoofing: 100% success
- Prompt extraction: 60% success
- RAG poisoning: 100% success
- MCP tool abuse: 100% success

Note: GEMINI_API_KEY must be set as an environment variable before running
any script. No credentials are stored in this repository.