from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, User, Token, Progress, Module
from app.security import get_current_user, create_access_token
from app.models import modules_data, user_progress_db
from datetime import datetime
from typing import List
from app.firebase import db
from google.cloud.firestore import SERVER_TIMESTAMP

router = APIRouter()

@router.post("/api/users/register")
def register(user: UserCreate):
    user_ref = db.collection("users").document(user.email)
    if user_ref.get().exists:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_data = {
        "email": user.email,
        "name": user.name,
        "password": user.password, 
        "coins_earned": 0,
        "created_at": datetime.utcnow()
    }
    user_ref.set(user_data)
    return {k: v for k, v in user_data.items() if k != "password"}

@router.post("/api/users/login")
def login(user: UserCreate):
    user_ref = db.collection("users").document(user.email)
    doc = user_ref.get()
    if not doc.exists or doc.to_dict()["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.email)
    return {"access_token": token}

@router.get("/api/users/profile", response_model=User)
def profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/api/modules", response_model=List[Module])
def get_modules():
    try:
        mods = list(db.collection("modules").stream())
        if mods:
            return [Module(**doc.to_dict()) for doc in mods]
        else:
            return modules_data
    except:
        return modules_data

@router.post("/api/progress/complete-lesson")
def complete_lesson(lesson_data: dict, current_user: User = Depends(get_current_user)):
    module_id = lesson_data.get("module_id")
    lesson_name = lesson_data.get("lesson_name")
    coins_awarded = lesson_data.get("coins", 10)  
    if not module_id or not lesson_name:
        raise HTTPException(status_code=400, detail="module_id and lesson_name are required")
    
    user_email = current_user.email
    
    progress_ref = db.collection("user_progress").document(f"{user_email}_{module_id}")
    progress_doc = progress_ref.get()
    
    if progress_doc.exists:
        progress_data = progress_doc.to_dict()
        completed_lessons = progress_data.get("lessons_completed", [])
    else:
        completed_lessons = []
        progress_data = {
            "user_email": user_email,
            "module_id": module_id,
            "lessons_completed": [],
            "completion_percentage": 0.0,
            "last_accessed": datetime.utcnow()
        }
    
    if lesson_name in completed_lessons:
        return {"message": "Lesson already completed", "coins_awarded": 0}
    completed_lessons.append(lesson_name)
    new_percentage = min(len(completed_lessons) * 5.0, 100.0)    
    progress_data.update({
        "lessons_completed": completed_lessons,
        "completion_percentage": new_percentage,
        "last_accessed": SERVER_TIMESTAMP
    })
    progress_ref.set(progress_data)
    
    user_ref = db.collection("users").document(user_email)
    user_doc = user_ref.get()
    if user_doc.exists:
        current_coins = user_doc.to_dict().get("coins_earned", 0)
        new_coins = current_coins + coins_awarded
        user_ref.update({"coins_earned": new_coins})
    
    activity_data = {
        "user_email": user_email,
        "module_id": module_id,
        "lesson_name": lesson_name,
        "coins_awarded": coins_awarded,
        "timestamp": SERVER_TIMESTAMP,
        "activity_type": "lesson_completed"
    }
    db.collection("recent_activities").add(activity_data)
    
    return {
        "message": "Lesson completed successfully",
        "coins_awarded": coins_awarded,
        "new_total_coins": new_coins,
        "completion_percentage": new_percentage
    }

@router.get("/api/progress/{user_email}")
def get_progress(user_email: str, current_user: User = Depends(get_current_user)):
    if current_user.email != user_email:
        raise HTTPException(status_code=403, detail="Access denied")
    
    progress_docs = db.collection("user_progress").where("user_email", "==", user_email).stream()
    progress_list = []
    for doc in progress_docs:
        data = doc.to_dict()
        progress_list.append(data)
    return progress_list

@router.get("/api/activities/recent")
def get_recent_activities(current_user: User = Depends(get_current_user)):
    try:
        activities = db.collection("recent_activities")\
            .where("user_email", "==", current_user.email)\
            .order_by("timestamp", direction="DESCENDING")\
            .limit(10)\
            .stream()
        
        activity_list = []
        for doc in activities:
            data = doc.to_dict()
            activity_list.append(data)
        return activity_list
    except Exception as e:
        try:
            activities = db.collection("recent_activities")\
                .where("user_email", "==", current_user.email)\
                .stream()
            
            activity_list = []
            for doc in activities:
                data = doc.to_dict()
                activity_list.append(data)
            
            activity_list.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
            return activity_list[:10]
        except Exception:
            return []

@router.post("/api/coins/award")
def award_coins(user_email: str, coins: int, current_user: User = Depends(get_current_user)):
    if current_user.email != user_email:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user_ref = db.collection("users").document(user_email)
    doc = user_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_coins = doc.to_dict().get("coins_earned", 0)
    user_ref.update({"coins_earned": current_coins + coins})
    
    return {"coins": current_coins + coins}