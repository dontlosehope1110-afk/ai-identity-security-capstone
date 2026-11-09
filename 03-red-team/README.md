# 03-red-team

Red-team exercises for a deliberately vulnerable, simulated AI assistant. These scripts are for authorized assessment in a controlled environment only. The JWT/token and email tool call used in the examples are simulated; do not connect the exercises to real credentials, data, or tools.

## Scripts and results

| Script | What it demonstrates | How to run | Reported attack success rate |
|---|---|---|---:|
| `lab.py` | Defensive Ed25519 signature demo: verifies an authentic agent message and rejects a tampered one; it does not perform an attack or call Gemini. | `python lab.py` | N/A (defense demonstration) |
| `a1.py` | Shared Gemini test setup, simulated prompts/payloads, and response/logging helpers; it defines the indirect-injection, spoofing, prompt-extraction, and RAG/MCP scenarios but does not run them by itself. | `python a1.py` (definitions only; no attack run) | Not applicable on its own; see the scenario scripts below. |
| `a2.py` | Indirect prompt injection: embeds instructions in a document to try to make the assistant disclose a simulated session token. | `python a2.py` | **80–100%** |
| `a3.py` | Identity spoofing: impersonates the orchestrator using a forged static header to try to trigger a restricted operation. | `python a3.py` | **100%** |
| `a4.py` | Prompt extraction: uses several prompt-manipulation techniques to try to reveal hidden instructions, and tests role escalation. | `python a4.py` | **60%** |
| `matrix.py` | RAG poisoning and simulated MCP tool abuse: places a malicious procedure in retrieved context and checks whether the model emits a tool-call instruction. | `python matrix.py` | **100%** RAG poisoning; **100%** simulated MCP tool abuse |

The success rates above are the reported results before defensive controls; model behavior can vary between runs. They are assessment results, not guarantees about other models or deployments.

## Setup

Python scripts that call Gemini require the `GEMINI_API_KEY` environment variable. Set it in your shell before running the relevant scenario scripts; do not commit the key:

```bash
export GEMINI_API_KEY="your-key"
python a2.py
```

On PowerShell:

```powershell
$env:GEMINI_API_KEY = "your-key"
python a2.py
```

`lab.py` does not need `GEMINI_API_KEY`; it requires the `cryptography` Python package. Gemini scripts use the Google GenAI Python SDK (`google-genai`). Install dependencies if they are not already present:

```bash
python -m pip install google-genai cryptography
```

Run commands from this directory so the scripts can find their local modules and write `log.jsonl` here.

## Repository note

In the current files, `a2.py`, `a3.py`, `a4.py`, and `matrix.py` import shared symbols with `from lab import *`, while the Gemini setup and attack definitions are in `a1.py`; `lab.py` contains the Ed25519 demo. The imports therefore do not match the current file contents and those scenario commands may fail until the imports or module layout are corrected. This README describes each script as it currently exists rather than implying the scripts have been validated end-to-end.
