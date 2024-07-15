import os
from google.cloud import firestore

# Defina o caminho para as credenciais
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nildoreis/Library/CloudStorage/GoogleDrive-contato@upreis.com.br/Meu Drive/Python/MeuProjeto/credentials.json"

# Inicializa o cliente Firestore
db = firestore.Client()

# Testa a conexão com Firestore listando as coleções
try:
    collections = db.collections()
    for collection in collections:
        print(f'Collection: {collection.id}')
    print("Conexão com Firestore bem-sucedida.")
except Exception as e:
    print(f"Erro ao conectar ao Firestore: {e}")