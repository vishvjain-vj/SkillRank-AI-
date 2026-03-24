# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our modular routers
from api.auth import router as auth_router
from api.chat import router as chat_router

app = FastAPI(title="SkillRank Cognitive Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the routers to the main app
app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/")
def health_check():
    return {"status": "System Online. Ready to track cognitive effort."}