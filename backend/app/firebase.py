import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("learningplatform-6bf88-firebase-adminsdk-fbsvc-8fe7e3aa65.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
