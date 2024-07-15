import csv
import requests
from google.cloud import firestore

def get_access_token():
    db = firestore.Client()
    doc = db.collection('tokens').document('mercado_livre').get()
    return doc.to_dict().get('access_token')

def fetch_sales_data(access_token):
    url = 'https://api.mercadolibre.com/orders/search/recent'  # Ajuste a URL conforme necessário
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_sales_data_to_csv(sales_data):
    keys = sales_data[0].keys()
    with open('sales_data.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(sales_data)

def main():
    access_token = get_access_token()
    sales_data = fetch_sales_data(access_token)
    save_sales_data_to_csv(sales_data)

if __name__ == '__main__':
    main()