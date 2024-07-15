import hashlib
import base64
import os

def generate_code_verifier():
    return base64.urlsafe_b64encode(os.urandom(40)).rstrip(b'=').decode('utf-8')

def generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('utf-8')

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

print("Code Verifier:", code_verifier)
print("Code Challenge:", code_challenge)