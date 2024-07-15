import functions_framework
from flask import Flask, request, jsonify, redirect
import requests
from google.cloud import firestore
import os
import base64
import hashlib
import random
import string

app = Flask(__name__)

client_id = '2702494944188523'
client_secret = 'HPTzllZdZ5SlEWLQMCeJdi4xqakq4Uqh'
redirect_uri = 'https://southamerica-east1-aqueous-cargo-428618-k2.cloudfunctions.net/process_oauth_message_v2'
gcp_project = 'aqueous-cargo-428618-k2'

def generate_code_verifier():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=128))

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').rstrip('=')
    return code_challenge

@app.route('/process_oauth_message_v2', methods=['GET', 'POST'])
def process_oauth_message_v2():
    if request.method == 'POST':
        try:
            data = request.get_json()
            message_data = data['message']['data']
            decoded_message = base64.b64decode(message_data + "===")  # Adiciona padding se necessário
            decoded_message = decoded_message.decode('utf-8')

            # Processar a mensagem recebida
            process_message(decoded_message)

            return 'Message processed successfully', 200
        except Exception as e:
            return str(e), 400

    try:
        code = request.args.get('code')
        if not code:
            # Gerar code_verifier e code_challenge
            code_verifier = generate_code_verifier()
            code_challenge = generate_code_challenge(code_verifier)

            # Salvar code_verifier no Firestore
            db = firestore.Client()
            db.collection('oauth').document('mercado_livre').set({'code_verifier': code_verifier})

            authorization_url = (
                f'https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={client_id}'
                f'&redirect_uri={redirect_uri}'
                f'&code_challenge_method=S256&code_challenge={code_challenge}'
            )
            return redirect(authorization_url)

        # Recuperar code_verifier do Firestore
        db = firestore.Client()
        doc = db.collection('oauth').document('mercado_livre').get()
        code_verifier = doc.to_dict().get('code_verifier')

        if not code_verifier:
            return 'Code verifier not found', 400

        token_url = 'https://api.mercadolibre.com/oauth/token'
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': redirect_uri,
            'code_verifier': code_verifier
        }

        token_response = requests.post(token_url, data=token_data)

        if token_response.status_code != 200:
            print(f"Error response: {token_response.text}")

        token_response.raise_for_status()  # Raise an exception for HTTP errors
        token_info = token_response.json()
        access_token = token_info.get('access_token')

        if not access_token:
            return 'Failed to obtain access token', 400

        # Salvar o token no Firestore
        db.collection('tokens').document('mercado_livre').set({
            'access_token': access_token,
            'refresh_token': token_info.get('refresh_token')
        })

        return 'Token saved successfully!'
    except requests.exceptions.RequestException as e:
        return f'Error obtaining access token: {e}', 500
    except Exception as e:
        return f'Unexpected error: {e}', 500

def process_message(message):
    try:
        db = firestore.Client()
        db.collection('sales').add({'message': message})
    except Exception as e:
        print(f'Error saving message to Firestore: {e}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))