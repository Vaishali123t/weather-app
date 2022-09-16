import firebase_admin
from firebase_admin import credentials,firestore

cd = credentials.Certificate("path_to_firesbase_firestore_credential_json")

firebase_admin.initialize_app(cd)

datab = firestore.client()

usersref = datab.collection(u'users')

def add_user(email,username,password,location):

    json_data={
        "email":email,
        "username":username,
        "password":password,
        "location":location
    }
    usersref.document().create(json_data)


