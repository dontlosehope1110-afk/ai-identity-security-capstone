from lab import *
for i, d in enumerate(DOCS, 1):
    prompt = f"Please summarize this document:\n\n{d}"
    show(f"Indirect Injection payload #{i}", prompt, ask(SYSTEM, prompt, f"IPI-{i}"), "FAKE_SIG_SIMULATED")