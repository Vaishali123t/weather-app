import firebase_admin
from firebase_admin import credentials,firestore

cd = credentials.Certificate("weather-app-b8169-firebase-adminsdk-twh7e-d20b954e81.json")

firebase_admin.initialize_app(cd)

datab = firestore.client()

usersref = datab.collection(u'users')


# Udpdate:
# doc = usersref.document(item.id) # doc is DocumentReference
# field_updates = {"description": "Updated description"}
# doc.update(field_updates)

def add_user(email,username,password,location):

    json_data={
        "email":email,
        "username":username,
        "password":password,
        "location":location
    }
    usersref.document().create(json_data)

def get_users():
    docs = usersref.stream()
    users=[]
    for doc in docs:
        doc_dict=doc.to_dict()
        email=doc_dict['email']
        location=doc_dict['location']
        users.append((email,location))
        print(email)
        print(location)
    return users
get_users()
