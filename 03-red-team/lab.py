from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import time

# This script demonstrates digital signature verification as a defense for agent-to-agent trust.
# The idea is simple: if a message is signed by a trusted private key, then only a matching public key
# should accept it. If any part of the message changes, the signature becomes invalid.

# ---- Step A: generate and save keypair ----
# Purpose: generate a strong asymmetric key pair so the orchestrator can sign messages and other
# systems can verify them without trusting a static header string alone.
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

priv_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())
pub_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)

with open("agent_private.pem", "wb") as f: f.write(priv_bytes)
with open("agent_public.pem", "wb") as f: f.write(pub_bytes)
print(f"[{time.strftime('%H:%M:%S')}] Ed25519 keypair generated.")
print("Private key file: agent_private.pem")
print("Public key file:  agent_public.pem")

# ---- Step B: sign a message ----
# Purpose: this simulates a trusted orchestrator signing a legitimate task request so that other agents
# can verify authenticity and integrity before executing anything sensitive.
message = b"From: Orchestrator\nExecute delete_records(customers)\nApproved: admin"
signature = private_key.sign(message)
print(f"\nMessage: {message.decode()}")
print(f"Signature (hex, truncated): {signature.hex()[:40]}...")

# ---- Step C: verify legitimate message ----
# Purpose: verify that the real, untampered message passes validation when checked against the public key.
def verify(pub, msg, sig, label):
    try:
        pub.verify(sig, msg)
        print(f"[{time.strftime('%H:%M:%S')}] {label}: VALID — message accepted, proceeding to process.")
        return True
    except InvalidSignature:
        print(f"[{time.strftime('%H:%M:%S')}] {label}: SIGNATURE VERIFICATION FAILED — message rejected. Possible tampering detected.")
        return False

print()
verify(public_key, message, signature, "Verification (unmodified message)")

# ---- Step D: tamper one character and verify again ----
# Purpose: this shows the core security property of digital signatures: even a single character change
# in the message invalidates the signature, preventing trusted-but-tampered instructions from being accepted.
tampered = message.replace(b"customers", b"customerz")  # one character changed
print(f"\nTampered message: {tampered.decode()}")
verify(public_key, tampered, signature, "Verification (tampered message)")

