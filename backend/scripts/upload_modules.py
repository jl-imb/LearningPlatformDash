import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

sample_modules = [
    {
        "id": "mod_1",
        "title": "Home Buying Basics",
        "lessons": ["What is a Mortgage?", "Down Payments 101", "Credit Scores"],
        "total_coins": 75,
        "difficulty": "Beginner"
    },
    {
        "id": "mod_2",
        "title": "Home Inspections",
        "lessons": ["Types of Inspections", "Red Flags", "Negotiating Repairs"],
        "total_coins": 100,
        "difficulty": "Intermediate"
    }
]

for module in sample_modules:
    db.collection("modules").document(module["id"]).set(module)

