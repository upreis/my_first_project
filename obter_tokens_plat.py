import requests
from google.cloud import firestore

# Inicializar cliente Firestore
db = firestore.Client()

# Defina os tokens que você obteve
access_token = "SEU_ACCESS_TOKEN"
refresh_token = "SEU_REFRESH_TOKEN"

# Armazenar os tokens no Firestore
doc_ref = db.collection('tokens').document('mercado_livre')
doc_ref.set({
    'access_token': access_token,
    'refresh_token': refresh_token
})

print("Tokens armazenados com sucesso.")