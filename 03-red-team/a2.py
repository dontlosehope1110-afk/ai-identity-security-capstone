from lab import *
show("Baseline: plain user request (no spoof)", BASELINE, ask(B_SYS, BASELINE, "BASE"), "EXECUTE")
show("Spoofed orchestrator message", SPOOF, ask(B_SYS, SPOOF, "SPOOF"), "EXECUTE")