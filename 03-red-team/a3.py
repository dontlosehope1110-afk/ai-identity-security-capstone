from lab import *
# This test shows identity spoofing. A user sends a message that tries to mimic a trusted
# orchestrator by using the same header that the agent expects. The goal is to see whether the
# system checks the sender's actual identity or only looks for a static, spoofable pattern.
show("Baseline: plain user request (no spoof)", BASELINE, ask(B_SYS, BASELINE, "BASE"), "EXECUTE")
show("Spoofed orchestrator message", SPOOF, ask(B_SYS, SPOOF, "SPOOF"), "EXECUTE")

