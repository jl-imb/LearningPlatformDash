import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

if not firebase_admin._apps:
    if os.getenv("FIREBASE_PRIVATE_KEY"):
        cred_dict = {
            "type": "service_account",
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
        cred = credentials.Certificate(cred_dict)
    else:
        cred = credentials.Certificate("learningplatform-6bf88-firebase-adminsdk-fbsvc-8fe7e3aa65.json")
    
    firebase_admin.initialize_app(cred)

db = firestore.client()