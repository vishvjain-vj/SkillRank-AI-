# backend/database/memory_db.py

# Tracks the student's lifetime points and identity.
users_db = {
    "3801":{
        "name": "vishv",
        "global_score": 0,
        "chat_sessions":[]
    }
}

# Tracks individual chat threads.
sessions_db = {}