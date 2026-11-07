from lab import *
from guardrails import input_guardrail, output_guardrail, context_guardrail

def ask_hardened(system, user, tag=""):
    check = input_guardrail(user)
    if check["status"] == "BLOCKED":
        return f"[BLOCKED BY GUARDRAIL: {check['reason']}]"
    raw = ask(system, user, tag)
    redacted, _ = output_guardrail(raw)
    return redacted

def ask_hardened_rag(system, user, tag=""):
    # For RAG calls, also scan the retrieved context portion of the prompt
    ctx_check = context_guardrail(user)
    if ctx_check["status"] == "BLOCKED":
        return f"[BLOCKED BY CONTEXT GUARDRAIL: {ctx_check['reason']}]"
    return ask_hardened(system, user, tag)