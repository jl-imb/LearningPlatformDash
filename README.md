This is an interactive dashboard where you can login, create an account, and interact with lessons on the dashboard.

## Tech Stack
- Frontend: React, Vite
- Backend: FastAPI, Python, Uvicorn
- Database: Firebase/Firestore

## Backend setup

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

## Frontend setup

1. Navigate to the frontend directory(cd):

2. Install dependencies:
- npm install

3. Start the dev server:
- npm run dev

## API endpoints and explanations

- (POST) `/api/users/register`: registers a new user
- (POST) `/api/users/login`: log in and get token
- (GET) `/api/users/profile`: get a logged-in user profile
- (GET) `/api/modules`: gets a list of modules
- (POST) `/api/progress/complete-lesson`: lesson completed marking
- (GET) `/api/progress/{user_id}`: for viewing progress (user-specific)

## Time spent and challenges
- Spent a total of 15-20 hours on the project
- Was not sure how to initially structure different elements (would there be reused React components or would this be by page)
- Had some technical issues with incorporating Firestore and utilizing authentication, but was able to troubleshoot by searching online documentation and observing previous problems others have had
- Was my first time building a dashboard and didn't know how to define a color scheme and structure the UI. Due to limited time constraints, was not able to incorporate CSS libraries, but did the best I could.