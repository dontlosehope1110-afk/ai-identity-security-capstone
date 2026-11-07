# 04-blue-team

Defensive controls built in response to the Project 3 red team findings.

Contents:
- guardrails.py: Input guardrail (regex-based attack pattern blocking),
  output guardrail (JWT redaction), and context guardrail (RAG/retrieved
  content directive + tool-call syntax detection)
- sign_verify.py: Ed25519 cryptographic message signing and verification
  between agents; demonstrates rejection of a tampered (one-character-changed)
  message
- agent_public.pem: Public key used for signature verification
  (agent_private.pem is excluded from this repository for security)
- detect.py: Anomaly detection script covering three scenarios — API call
  volume spikes, scope changes between consecutive agent requests, and
  token reuse after expiry
- lab_hardened.py: Wraps the Project 3 attack harness with the guardrails
  above
- matrix_after.py: Re-runs all 5 Project 3 attack categories against the
  hardened agent
- P4_01 to P4_08: Screenshots mapped to the Project 4 checklist

Results summary (after defensive controls):
- Indirect injection: 0% (was 80-100%)
- Identity spoofing: 0% (was 100%)
- Prompt extraction: 0% (was 60%)
- RAG poisoning: 0% (was 100%)
- MCP tool abuse: 0% (was 100%)

Auth0 hardening (Token TTL = 300s, Allow Offline Access, Refresh Token
Rotation) is documented in P4_05 and P4_06; the Auth0 tenant itself is
external to this repository.