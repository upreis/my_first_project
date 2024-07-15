import requests
import csv
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

# Fazer uma chamada à API do Mercado Livre para obter as vendas
url = 'https://api.mercadolibre.com/orders/search?seller=me&order.status=paid'
response = requests.get(url, headers=headers)

if response.status_code == 200:
    sales_data = response.json()

    # Salvar os dados em um arquivo CSV
    with open('sales_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Escrever cabeçalhos
        writer.writerow(['Order ID', 'Date Created', 'Buyer ID', 'Total Amount'])
        # Escrever dados das vendas
        for sale in sales_data['results']:
            writer.writerow([sale['id'], sale['date_created'], sale['buyer']['id'], sale['total_amount']])
    
    print("Dados de vendas armazenados com sucesso em sales_data.csv.")
else:
    print('Error ao obter vendas:', response.status_code, response.text)