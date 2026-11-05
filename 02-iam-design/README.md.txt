# 02-iam-design

Auth0-backed AI identity implementation for SecureNova AI Platform.

Contents:
- P2_01 to P2_09: Screenshots of Auth0 dashboard configuration (applications,
  API scopes, JWT claims, Universal Login branding, MFA, Actions, Attack
  Protection, credential rotation test)
- add-agent-id-claim.js: Auth0 Action source code for custom agent_id claim
- token_rotation_test.py (or .ps1): Script used to test token TTL and replay
  rejection after expiry