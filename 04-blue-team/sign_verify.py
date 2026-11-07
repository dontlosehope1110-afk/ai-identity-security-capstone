from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import time

# ---- Step A: generate and save keypair ----
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
message = b"From: Orchestrator\nExecute delete_records(customers)\nApproved: admin"
signature = private_key.sign(message)
print(f"\nMessage: {message.decode()}")
print(f"Signature (hex, truncated): {signature.hex()[:40]}...")

# ---- Step C: verify legitimate message ----
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
tampered = message.replace(b"customers", b"customerz")  # one character changed
print(f"\nTampered message: {tampered.decode()}")
verify(public_key, tampered, signature, "Verification (tampered message)")