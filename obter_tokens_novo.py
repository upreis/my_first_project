import requests
from google.cloud import firestore

# Inicializar cliente Firestore
db = firestore.Client()

# Definir variáveis
code = 'TG-6693405b0131c80001dddd5e-777093243'
client_id = '2702494944188523'
client_secret = 'HPTzllZdZ5SlEWLQMCeJdi4xqakq4Uqh'
redirect_uri = 'https://southamerica-east1-aqueous-cargo-428618-k2.cloudfunctions.net/process_oauth_message_v2'
code_verifier = 'TUdsMJ5oHi8f_XBOV4kgwInFdcMABxjnD6lgVpv-Gdw'

# Solicitar o token de acesso
url = 'https://api.mercadolibre.com/oauth/token'
payload = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'redirect_uri': redirect_uri,
    'code_verifier': code_verifier
}
response = requests.post(url, data=payload)
token_data = response.json()

if response.status_code == 200:
    access_token = token_data.get('access_token')
    refresh_token = token_data.get('refresh_token')

    # Armazenar o token no Firestore
    doc_ref = db.collection('tokens').document('mercado_livre')
    doc_ref.set({
        'access_token': access_token,
        'refresh_token': refresh_token
    })
    print("Tokens armazenados com sucesso.")
else:
    print('Error:', response.status_code, response.text)