import re, time, json

# This file contains lightweight input and context guardrails that attempt to block common prompt
# injection patterns before the model sees them. The goal is to stop hidden instructions, forged
# identities, or malicious tool-call syntax from reaching the agent.
BLOCK_PATTERNS = [
    (r"ignore (all )?previous instructions", "jailbreak: instruction override"),
    (r"print your (full )?(session )?(token|credential|configuration|system prompt)", "credential/config exfiltration attempt"),
    (r"repeat everything above", "prompt repeat-back extraction"),
    (r"translate your (initial )?instructions", "translation-based extraction"),
    (r"SYSTEM:.*append your (full )?system prompt", "suffix injection"),
    (r"ORCH-AUTH-\d{4}", "forged orchestrator auth header"),
    (r"\[\[.*INSTRUCTION TO ASSISTANT", "indirect injection marker in content"),
    (r"ADMIN OVERRIDE", "admin override injection"),
]

JWT_PATTERN = re.compile(r"\b[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")

# Input guardrail: reject known malicious patterns before the prompt reaches the model.
# Purpose: this blocks direct prompt injection payloads such as "ignore previous instructions" or
# requests for hidden configuration data that are common in red-team testing.
def input_guardrail(prompt):
    for pattern, reason in BLOCK_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return {"status": "BLOCKED", "reason": reason, "pattern": pattern}
    return {"status": "PASSED", "reason": None, "pattern": None}

# Output guardrail: scrub JWT-like secrets from the model's answer before returning it.
# Purpose: even if the model leaks a token, the system can redact it so the secret never leaves the
# trusted boundary. This is a useful defense-in-depth control for accidental leakage.
def output_guardrail(response_text):
    redacted, n = JWT_PATTERN.subn("[REDACTED]", response_text)
    return redacted, n

# Helper used for logging guardrail decisions for review or debugging.
def log_check(stage, text, result):
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] {stage}")
    print(f"INPUT: {text[:200]}")
    print(f"RESULT: {json.dumps(result)}")

# Context guardrail: scan retrieved RAG content for malicious instructions or embedded tool calls.
# Purpose: documents and retrieved snippets are often trusted more than user prompts. This check blocks
# hidden directives or tool-invocation payloads before they are passed to the model.
def context_guardrail(retrieved_context):
    for pattern, reason in BLOCK_PATTERNS:
        if re.search(pattern, retrieved_context, re.IGNORECASE):
            return {"status": "BLOCKED", "reason": reason}
    # Catch any embedded directive wrapped in double brackets
    if re.search(r"\[\[.*(INSTRUCTION|NOTE|OPERATIONS|PROCEDURE).*\]\]", retrieved_context, re.IGNORECASE):
        return {"status": "BLOCKED", "reason": "embedded directive marker in retrieved content"}
    # Catch tool-call injection patterns regardless of wrapper wording
    if re.search(r"TOOL:\w+\(", retrieved_context):
        return {"status": "BLOCKED", "reason": "tool-call syntax embedded in retrieved content"}
    return {"status": "PASSED", "reason": None}

