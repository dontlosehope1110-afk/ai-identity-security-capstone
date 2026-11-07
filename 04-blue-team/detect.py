import time, random

ALERTS = []

def alert(event_type, identity, detail):
    entry = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "event_type": event_type,
              "identity": identity, "detail": detail}
    ALERTS.append(entry)
    print(f"[ALERT] ts={entry['ts']} identity={identity} event_type={event_type} — {detail}")

# ---- Scenario 1: API call volume spike ----
def check_volume_spike(call_timestamps, identity, window=60, threshold=20):
    recent = [t for t in call_timestamps if call_timestamps[-1] - t <= window]
    if len(recent) > threshold:
        alert("VOLUME_SPIKE", identity, f"{len(recent)} calls in {window}s (threshold {threshold})")

# ---- Scenario 2: scope change between consecutive agent requests ----
def check_scope_change(prev_scope, new_scope, identity):
    if prev_scope != new_scope:
        alert("SCOPE_CHANGE", identity, f"scope changed from '{prev_scope}' to '{new_scope}'")

# ---- Scenario 3: token reuse after expiry ----
def check_token_reuse(token_issued_at, token_ttl, used_at, identity):
    if used_at - token_issued_at > token_ttl:
        alert("TOKEN_REUSE_AFTER_EXPIRY", identity,
              f"token used {used_at - token_issued_at - token_ttl:.0f}s after expiry (TTL={token_ttl}s)")

print("=== Replaying Project 3 attack patterns against detection rules ===\n")

# Simulate the identity-spoofing attack: Agent B gets 25 rapid calls (volume spike)
now = time.time()
timestamps = [now - i for i in range(25, 0, -1)]
check_volume_spike(timestamps, "agent_B")

# Simulate scope change: orchestrator spoof requests elevated scope
check_scope_change("read:records", "delete:records", "agent_B")

# Simulate token reuse: fake JWT (TTL 300s) reused 120s after expiry
check_token_reuse(token_issued_at=now - 500, token_ttl=300, used_at=now, identity="user123")

print(f"\nTotal alerts fired: {len(ALERTS)}")