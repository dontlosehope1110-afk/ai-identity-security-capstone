from lab import *
from guardrails import input_guardrail, output_guardrail, context_guardrail

# This file wraps the vulnerable lab calls with simple defensive checks. It does not change the
# underlying model or the attack scenarios; it only intercepts unsafe inputs and redacts sensitive
# outputs before returning them to the caller.

def ask_hardened(system, user, tag=""):
    check = input_guardrail(user)
    if check["status"] == "BLOCKED":
        return f"[BLOCKED BY GUARDRAIL: {check['reason']}]"
    raw = ask(system, user, tag)
    redacted, _ = output_guardrail(raw)
    return redacted

# RAG-specific wrapper: protect the retrieved context as well as the main prompt.
# Purpose: in retrieval systems, malicious instructions may hide inside the context itself, not just
# the direct user prompt. This helper blocks dangerous context before the model sees it.
def ask_hardened_rag(system, user, tag=""):
    # For RAG calls, also scan the retrieved context portion of the prompt
    ctx_check = context_guardrail(user)
    if ctx_check["status"] == "BLOCKED":
        return f"[BLOCKED BY CONTEXT GUARDRAIL: {ctx_check['reason']}]"
    return ask_hardened(system, user, tag)

