import requests
from google.cloud import firestore

# Inicializar cliente Firestore
db = firestore.Client()

# Recuperar o token de acesso do Firestore
doc = db.collection('tokens').document('mercado_livre').get()
access_token = doc.to_dict().get('access_token')

# Definir o cabeçalho de autorização
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Verificar permissões do token
url = 'https://api.mercadolibre.com/users/me'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    user_data = response.json()
    print("Informações do usuário:", user_data)
else:
    print('Error:', response.status_code, response.text)

# Verificar se o token tem permissão para ler vendas
url = 'https://api.mercadolibre.com/orders/search?seller=me&order.status=paid'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Permissão de leitura de vendas confirmada.")
else:
    print('Error:', response.status_code, response.text)