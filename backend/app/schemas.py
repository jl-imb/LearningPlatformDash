from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class User(BaseModel):
    id: int
    email: str
    name: str
    coins_earned: int = 0
    created_at: datetime

class Token(BaseModel):
    access_token: str

class Module(BaseModel):
    id: str
    title: str
    lessons: List[str]
    total_coins: int
    difficulty: str

class Progress(BaseModel):
    user_id: int
    module_id: str
    lessons_completed: List[str]
    completion_percentage: float
    last_accessed: datetime
