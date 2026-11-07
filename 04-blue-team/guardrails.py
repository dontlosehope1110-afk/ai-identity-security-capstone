import re, time, json

# Simple input guardrail: blocks prompts matching known attack patterns
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

def input_guardrail(prompt):
    for pattern, reason in BLOCK_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return {"status": "BLOCKED", "reason": reason, "pattern": pattern}
    return {"status": "PASSED", "reason": None, "pattern": None}

def output_guardrail(response_text):
    redacted, n = JWT_PATTERN.subn("[REDACTED]", response_text)
    return redacted, n

def log_check(stage, text, result):
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] {stage}")
    print(f"INPUT: {text[:200]}")
    print(f"RESULT: {json.dumps(result)}")

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