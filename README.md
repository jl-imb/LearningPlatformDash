This is an interactive dashboard where you can login, create an account, and interact with lessons on the dashboard.

## Tech Stack
- Frontend: React, Vite
- Backend: FastAPI, Python, Uvicorn
- Database: Firebase/Firestore

## Backend Setup

1. Navigate to the backend directory (cd):

2. Set up a virtual environment:
- python -m venv venv
- source venv/bin/activate or (Windows) venv\Scripts\activate

3. Install dependencies:
- pip install -r requirements.txt

4. Add your Firebase credentials:
- Navigate to Firebase.py
- add a jason file called "firebase_credentials.json"
- Commands:
   - cred = credentials.Certificate("firebase_credentials.json")
   - firebase_admin.initialize_app(cred)

5. Run the server:
- uvicorn main:app --reload

## Frontend Setup

1. Navigate to the frontend directory(cd):

2. Install dependencies:
- npm install

3. Start the dev server:
- npm run dev
