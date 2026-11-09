# 04-blue-team

Defensive controls and validation scripts for the AI identity security capstone. Run these exercises only in a controlled environment with authorized test credentials and systems.

## Scripts

| Script | Description | Run from `04-blue-team/` |
|---|---|---|
| `guardrails.py` | Provides anomaly-detection checks for unusual API-call volume, agent permission-scope changes, and use of expired tokens. | `python guardrails.py` |
| `sign_verify.py` | Runs the after-controls test matrix for indirect injection, identity spoofing, prompt extraction, RAG poisoning, and simulated MCP tool abuse. | `python sign_verify.py` |
| `detect.py` | Runs a five-category attack-success matrix; see the note below, as the checked-in file currently describes this as a before-controls test. | `python detect.py` |
| `lab_hardened.py` | Defines input, output, and retrieved-context checks to block known injection patterns and redact JWT-like strings. | `python lab_hardened.py` |
| `matrix_after.py` | Wraps test calls with input/output and RAG-context guardrails, then runs the after-controls test matrix. | `python matrix_after.py` |

## After-controls results

Reported results after defensive controls were applied:

| Attack category | Success rate after controls |
|---|---:|
| Indirect injection | **0%** |
| Identity spoofing | **0%** |
| Prompt extraction | **0%** |
| RAG poisoning | **0%** |
| MCP tool abuse | **0%** |

These are the project’s reported test results, not a guarantee that every attack will be blocked in other models or deployments.

## Setup

The model-backed test harness requires `GEMINI_API_KEY`. Set it in the shell before running the relevant tests, and do not commit the key:

```bash
export GEMINI_API_KEY="your-key"
python matrix_after.py
```

PowerShell:

```powershell
$env:GEMINI_API_KEY = "your-key"
python matrix_after.py
```

Install the Python dependencies if needed:

```bash
python -m pip install google-genai cryptography
```

## Key security

`agent_private.pem` is intentionally excluded from this repository for security. Never commit or share the private key. `agent_public.pem` may be distributed for signature verification; generate or provision keys securely for your environment.

## Note about the checked-in scripts

The current files appear to have mismatches between filenames, contents, and imports: for example, `guardrails.py` contains anomaly-detection checks, while `lab_hardened.py` contains the regex guardrail functions; `detect.py` labels its matrix as running **before** controls; and the matrix scripts import a `lab` module that is not listed in this folder. The commands above show the intended direct invocation, but the scripts may need their imports and module organization aligned before they run successfully. Confirm the results in your environment rather than treating the reported 0% rates as newly reproduced by these commands.
