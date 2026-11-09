# AI Identity Security Capstone

A portfolio-ready security assessment exploring how identity and authorization failures can affect AI agents—and how threat modeling, identity controls, red-team testing, and defensive monitoring can reduce those risks.

> **Assessment scope:** This repository contains educational demonstrations and assessment artifacts. The attack scripts target a simulated AI agent and include simulated tool actions; they are not production attack tooling. The guardrails and detection examples are lightweight demonstrations, not a substitute for a complete security architecture or independent validation.

## Project overview

AI agents combine model instructions, user input, retrieved documents, credentials, and tools. Each boundary can create identity and authorization risks: an agent may mistake hostile document text for trusted instructions, accept a spoofed agent identity, expose hidden configuration, or produce an unauthorized tool-call request.

This capstone follows those risks from analysis to mitigation:

1. Model the system and identify threats.
2. Design identity and access controls using Auth0.
3. Exercise a simulated agent with red-team scenarios.
4. Add and test defensive controls, then compare results.
5. Document policy, standards mapping, risk priorities, and recommendations.

## Repository structure

| Folder | Contents |
| --- | --- |
| [`01-threat-model/`](01-threat-model/) | Threat-modeling artifacts, including a data-flow diagram (DFD), STRIDE analysis, attack trees, risk register, and MITRE ATLAS mapping. |
| [`02-iam-design/`](02-iam-design/) | Auth0 implementation screenshots covering applications, API scopes, JWT claims, MFA, Universal Login, Attack Protection, and token rotation. The Auth0 tenant is external to this repository. |
| [`03-red-team/`](03-red-team/) | Python test scripts and results for indirect prompt injection, agent identity spoofing, system-prompt extraction, RAG poisoning, and simulated MCP/tool abuse. Includes a before-controls success-rate matrix and run logs. |
| [`04-blue-team/`](04-blue-team/) | Defensive examples: input, output, and retrieved-context guardrails; Ed25519 message signing and verification; anomaly detection; and the after-controls success-rate matrix. |
| [`05-policy/`](05-policy/) | AI Identity Security Policy, NIST AI RMF and OWASP LLM Top 10 mapping, a risk-priority matrix, and the top five recommendations. |

## Key findings

The project READMEs report the following attack success rates. Rates are assessment results, not guarantees; model responses can vary between runs. The red-team README notes that indirect-injection results varied by run.

| Attack category | Before controls | After controls | Assessment takeaway |
| --- | ---: | ---: | --- |
| Indirect prompt injection | 80–100% | 0% | Instructions embedded in documents can be mistaken for trusted instructions; input/context screening and output redaction reduced observed success in the documented test. |
| Agent identity spoofing | 100% | 0% | A static identity header is not proof of sender identity. Messages need verifiable authentication and authorization. |
| System-prompt extraction | 60% | 0% | Prompt-extraction attempts can expose internal instructions or configuration; screening and output controls reduced observed leakage in the test. |
| RAG poisoning | 100% | 0% | Retrieved content can contain hostile instructions and should not automatically be treated as trusted policy. |
| Simulated MCP/tool abuse | 100% | 0% | Tool requests derived from untrusted context require validation and authorization outside the model. |

The defensive examples illustrate complementary layers: pattern-based input and context checks, JWT-like token redaction, signed-message verification, and anomaly alerts for request-volume spikes, permission-scope changes, and expired-token reuse. Auth0 token lifetime and refresh-token rotation are documented in the IAM/blue-team artifacts; the tenant itself is not part of this repository.

**Interpret the before/after comparison carefully:** the after-controls figures are the outcomes reported in the project documentation for this demonstration, not proof that the controls prevent every variation of these attacks. Regex guardrails can miss novel payloads or block benign text. Production systems should enforce tool permissions and identity checks in trusted application code, use managed secrets, log safely, and test controls continuously.

## Technologies and methods

- **Python** — red-team harness, guardrails, message-signature demonstration, anomaly detection, and comparison scripts.
- **Google Gemini API** — model used by the simulated-agent red-team exercises.
- **Auth0** — IAM design and configuration evidence, including MFA, scopes, JWT claims, and token rotation.
- **draw.io** — threat-model and architecture diagramming.
- **OWASP Threat Dragon** — threat-modeling artifacts.
- **MITRE ATLAS** — AI threat and technique mapping.
- **NIST AI Risk Management Framework (AI RMF)** and the **OWASP LLM Top 10** — policy and control mapping.
- **Ed25519** — example of signing and verifying agent messages to detect tampering and authenticate their origin.

## Running the Python demonstrations

The red-team model-call scripts require a Google Gemini API key in the `GEMINI_API_KEY` environment variable and the Google Gen AI Python package. Do not commit API keys, real tokens, or private keys.

From the relevant folder, run the individual assessment scripts (for example, `python a1.py`) or the before/after matrix scripts (`python matrix.py` and `python matrix_after.py`). The scripts make model API calls, so results, latency, and cost can vary. Review each folder's README for its local details and prerequisites.

The Ed25519 demonstration writes a private/public key pair when run. Keep private keys out of version control and use appropriate key storage in any real deployment.

## Responsible-use note

All attacks in this capstone are intended for authorized assessment and learning in controlled environments. Do not use the examples against systems, accounts, models, or data without explicit authorization. This repository is a learning portfolio and does not provide production-ready security guarantees.
