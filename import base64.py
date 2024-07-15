import base64
import hashlib
import os

def generate_code_verifier_and_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

code_verifier, code_challenge = generate_code_verifier_and_challenge()
print(f"Code Verifier: {code_verifier}")
print(f"Code Challenge: {code_challenge}")