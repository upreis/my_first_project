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

# Fazer uma chamada à API do Mercado Livre para obter as informações do usuário
url_user_info = 'https://api.mercadolibre.com/users/me'
response_user_info = requests.get(url_user_info, headers=headers)

if response_user_info.status_code == 200:
    user_data = response_user_info.json()
    print("Informações do usuário:", user_data)
else:
    print('Error ao obter informações do usuário:', response_user_info.status_code, response_user_info.text)

# Verificar permissões do token
url_permissions = 'https://api.mercadolibre.com/users/me'
response_permissions = requests.get(url_permissions, headers=headers)

if response_permissions.status_code == 200:
    permissions_data = response_permissions.json()
    print("Permissões do token:", permissions_data)
else:
    print('Error ao verificar permissões:', response_permissions.status_code, response_permissions.text)

# Verificar se o token tem permissão para ler vendas
url_sales_permission = 'https://api.mercadolibre.com/orders/search?seller=me&order.status=paid'
response_sales_permission = requests.get(url_sales_permission, headers=headers)

if response_sales_permission.status_code == 200:
    print("Permissão de leitura de vendas confirmada.")
else:
    print('Error ao verificar permissão de leitura de vendas:', response_sales_permission.status_code, response_sales_permission.text)