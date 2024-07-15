import requests
from google.cloud import firestore

def get_access_token(client_id, client_secret, code, redirect_uri, code_verifier):
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }
    response = requests.post(url, data=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")
        raise
    return response.json()

def get_code_verifier():
    db = firestore.Client()
    doc = db.collection('oauth').document('mercado_livre').get()
    if doc.exists:
        code_verifier = doc.to_dict().get('code_verifier')
        if code_verifier:
            return code_verifier
        else:
            raise ValueError("Code verifier not found in the Firestore document")
    else:
        raise ValueError("Firestore document not found")

# Substitua pelos seus valores
client_id = "2702494944188523"
client_secret = "HPTzllZdZ5SlEWLQMCeJdi4xqakq4Uqh"
code = "TG-6695972d86160a000172fabe-1754791584"  # Substitua pelo código que você obteve
redirect_uri = "https://process-oauth-message-v2-7wpwxnwk5q-rj.a.run.app"

try:
    code_verifier = get_code_verifier()
    print(f"Code Verifier: {code_verifier}")
    
    token_info = get_access_token(client_id, client_secret, code, redirect_uri, code_verifier)
    access_token = token_info['access_token']
    print(f"Access Token: {access_token}")
except ValueError as val_err:
    print(f"Value error: {val_err}")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"Other error occurred: {err}")