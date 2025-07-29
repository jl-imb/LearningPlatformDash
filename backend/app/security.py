from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
from app.schemas import User
from app.firebase import db

SECRET_KEY = "secretkey123"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise Exception("No email in token")
        user_ref = db.collection("users").document(email)
        doc = user_ref.get()
        if not doc.exists:
            raise Exception("User not found in database")
        
        user_data = doc.to_dict()
        return User(
            id=0, 
            email=user_data["email"],
            name=user_data["name"],
            coins_earned=user_data["coins_earned"],
            created_at=user_data["created_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")