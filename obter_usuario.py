import requests
from google.cloud import firestore

# Recuperar o token de acesso do Firestore
db = firestore.Client()
doc = db.collection('tokens').document('mercado_livre').get()
access_token = doc.to_dict().get('access_token')

# Definir o cabeçalho de autorização
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Fazer uma chamada à API do Mercado Livre (por exemplo, obter informações do usuário)
url = 'https://api.mercadolibre.com/users/me'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    user_info = response.json()
    print('User info:', user_info)
else:
    print('Error:', response.status_code, response.text)