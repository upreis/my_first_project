import hashlib
import base64
import random
import string

def generate_code_verifier():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=128))

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').rstrip('=')
    return code_challenge

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

print(f"Code Verifier: {code_verifier}")
print(f"Code Challenge: {code_challenge}")