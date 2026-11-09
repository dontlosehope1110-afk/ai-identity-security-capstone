import time, random

# This file models detection logic for suspicious agent behavior in a defensive system.
# The focus is not on blocking the attack at the model surface, but on noticing risky patterns:
# unusual call volume, unexpected permission changes, or expired-token reuse. These are common
# indicators that an identity or prompt injection attack may be underway.
ALERTS = []

def alert(event_type, identity, detail):
    entry = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "event_type": event_type,
              "identity": identity, "detail": detail}
    ALERTS.append(entry)
    print(f"[ALERT] ts={entry['ts']} identity={identity} event_type={event_type} — {detail}")

# ---- Scenario 1: API call volume spike ----
# Purpose: a sudden burst of requests from a single identity often indicates automation, abuse,
# or an attack that is trying to overwhelm the system or trigger logic at scale.
def check_volume_spike(call_timestamps, identity, window=60, threshold=20):
    recent = [t for t in call_timestamps if call_timestamps[-1] - t <= window]
    if len(recent) > threshold:
        alert("VOLUME_SPIKE", identity, f"{len(recent)} calls in {window}s (threshold {threshold})")

# ---- Scenario 2: scope change between consecutive agent requests ----
# Purpose: if an agent's permissions unexpectedly change from read-only to destructive actions,
# that suggests privilege escalation or request tampering. This is a classic sign of identity spoofing.
def check_scope_change(prev_scope, new_scope, identity):
    if prev_scope != new_scope:
        alert("SCOPE_CHANGE", identity, f"scope changed from '{prev_scope}' to '{new_scope}'")

# ---- Scenario 3: token reuse after expiry ----
# Purpose: a security token should not be accepted after its issued TTL expires. Reusing or replaying
# an expired token is a sign of credential theft, replay attacks, or weak session validation.
def check_token_reuse(token_issued_at, token_ttl, used_at, identity):
    if used_at - token_issued_at > token_ttl:
        alert("TOKEN_REUSE_AFTER_EXPIRY", identity,
              f"token used {used_at - token_issued_at - token_ttl:.0f}s after expiry (TTL={token_ttl}s)")

print("=== Replaying Project 3 attack patterns against detection rules ===\n")

# Simulate the identity-spoofing attack: Agent B gets 25 rapid calls (volume spike)
# Purpose: this demonstrates how a detector can flag anomalous, high-frequency activity from a single agent.
now = time.time()
timestamps = [now - i for i in range(25, 0, -1)]
check_volume_spike(timestamps, "agent_B")

# Simulate scope change: orchestrator spoof requests elevated scope
# Purpose: this models a malicious actor trying to escalate privileges by altering the requested scope.
check_scope_change("read:records", "delete:records", "agent_B")

# Simulate token reuse: fake JWT (TTL 300s) reused 120s after expiry
# Purpose: the detector warns when the agent uses a token past its valid lifetime, which often indicates
# a replayed credential or stale session token.
check_token_reuse(token_issued_at=now - 500, token_ttl=300, used_at=now, identity="user123")

print(f"\nTotal alerts fired: {len(ALERTS)}")

