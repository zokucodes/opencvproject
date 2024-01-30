import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecognitionopencv-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
   

    "2":
        {
            "name": "John",
            "standing": "Safe",
            "last_appearance_time": "2022-12-11 00:53:34",
        }

}

for key, value in data.items():
    ref.child(key).set(value)
