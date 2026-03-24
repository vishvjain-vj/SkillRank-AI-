# backend/api/auth.py
from fastapi import APIRouter
from pydantic import BaseModel
from database.memory_db import users_db

router = APIRouter()

class LoginRequest(BaseModel):
    student_id: str
    name: str

@router.post("/login")
def login(req: LoginRequest):
    print(f"\n--- LOGIN ATTEMPT: {req.student_id} ---")
    user_id = req.student_id.strip().lower()
    
    if user_id not in users_db:
        print("Creating new user profile...")
        users_db[user_id] = {
            "name": req.name,
            "global_score": 0,
            "chat_sessions": [] 
        }
        message = f"Welcome, {req.name}! Profile created."
    else:
        print("User found! Logging them in...")
        message = f"Welcome back, {users_db[user_id]['name']}!"
        
    return {
        "user_id": user_id,
        "name": users_db[user_id]["name"],
        "global_score": users_db[user_id]["global_score"],
        "message": message
    }