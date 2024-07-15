from google.cloud import firestore

# Inicializar cliente Firestore
db = firestore.Client()

# Tokens obtidos do Postman
access_token = 'APP_USR-2702494944188523-071323-61a8410c095a2aef893e0e38c5ca4157-777093243'
refresh_token = 'TG-6693410b7b9eaf0001f8345d-777093243'

# Armazenar os tokens no Firestore
doc_ref = db.collection('tokens').document('mercado_livre')
doc_ref.set({
    'access_token': access_token,
    'refresh_token': refresh_token
})
print("Tokens armazenados com sucesso.")