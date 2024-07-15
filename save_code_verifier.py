import base64
import hashlib
import random
import string
from google.cloud import firestore

def generate_code_verifier():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=128))

def main():
    code_verifier = generate_code_verifier()
    print(f"Code Verifier: {code_verifier}")
    
    db = firestore.Client()
    db.collection('oauth').document('mercado_livre').set({'code_verifier': code_verifier})
    print("Code Verifier saved to Firestore.")

if __name__ == '__main__':
    main()