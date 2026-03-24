# backend/api/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from database.memory_db import users_db, sessions_db
from services.ai_agent import generate_reply, evaluate_curiosity
import time 
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: list | None = None
    # Defaults added so your current Streamlit app doesn't break
    user_id: str = "guest_student"     
    session_id: str = "guest_session_1" 

@router.post("/chat")
def chat(req: ChatRequest):
    print("\n--- NEW REQUEST ---")
    
    # 1. Safety Check: If user/session doesn't exist yet, create them quietly
    # 1. Safety Check & Setup
    if req.user_id not in users_db:
        users_db[req.user_id] = {"global_score": 0, "chat_sessions": []}
        
    if req.session_id not in sessions_db:
        # We add time tracking and trap states here!
        sessions_db[req.session_id] = {
            "session_score": 0, 
            "history": [],
            "last_reply_time": 0,
            "last_word_count": 0,
            "in_bluff_trap": False
        }

    # 2. Prepare History
    messages = []
    if req.history:
        messages.extend(req.history)
    messages.append({"role": "user", "content": req.message})


    # --- AI Usage In learning Protocol --- 
    session = sessions_db[req.session_id]
    current_time = time.time()
    user_msg_lower = req.message.lower()

    # --- TRAP PHASE 2: EVALUATING THE BLUFF ---
    if session.get("in_bluff_trap"):
        time_taken = current_time - session["last_reply_time"]
        
        # Reset the trap so they aren't stuck forever
        session["in_bluff_trap"] = False 
        
        # Did they answer correctly AND under 10 seconds? (We give 10s for typing)
        if "mitochondria" in user_msg_lower and time_taken <= 10:
            reply = "🤖 TRAP DEFEATED: Okay, color me impressed. You actually *are* a fast reader. +50 XP!"
            score_added = 50
        else:
            reply = f"🤖 TRAP FAILED: You took {int(time_taken)} seconds, or you got the answer wrong. Reading is about comprehension, not just speed. -20 XP penalty."
            score_added = -20
            
        session["session_score"] += score_added
        users_db[req.user_id]["global_score"] += score_added
        
        return {
            "reply": reply,
            "score_added": score_added,
            "total_score": users_db[req.user_id]["global_score"],
            "reason": "bluff_protocol_resolved"
        }


    # --- TRAP PHASE 1: SPRINGING THE TRAP ---
    # Math: Average reading speed is ~4 words per second.
    expected_read_time = session.get("last_word_count", 0) / 4.0
    actual_read_time = current_time - session.get("last_reply_time", current_time)
    
    # Are they skipping the reading? (Answering in less than 30% of expected time)
    is_speeding = (session.get("last_word_count", 0) > 50) and (actual_read_time < (expected_read_time * 0.3))
    is_cocky = "read fast" in user_msg_lower or "fast reader" in user_msg_lower

    if is_speeding or is_cocky:
        session["in_bluff_trap"] = True
        session["last_reply_time"] = current_time # Start the clock!
        
        bluff_text = """
        🤖 **SPEED READER DETECTED. INITIATING BLUFF PROTOCOL.** You claim to process information rapidly. Let us test that hypothesis. You have exactly 10 seconds to read this text and answer the question at the very end. 
        
        The cellular matrix of eukaryotic organisms is a highly complex web of organelles, each performing specialized functions critical to survival. The endoplasmic reticulum synthesizes proteins, while the Golgi apparatus packages them for transport. Lysosomes act as the cellular waste disposal system, breaking down macromolecules. However, the true powerhouse, responsible for generating adenosine triphosphate (ATP) through cellular respiration, operates independently with its own unique DNA. 
        
        **QUESTION: To disable a cell's primary energy production, which specific organelle must you target?** *(Reply immediately with the single word).*
        """
        
        return {
            "reply": bluff_text,
            "score_added": 0,
            "total_score": users_db[req.user_id]["global_score"],
            "reason": "bluff_protocol_initiated"
        }
    # 3. Call AI Agents
    try:
        reply = generate_reply(messages)
        score_added, reason = evaluate_curiosity(req.message)
    except Exception as e:
        print("LLM CHAT ERROR:", e)
        return {
            "reply": "Model error occurred while thinking.",
            "score_added": 0,
            "total_score": users_db[req.user_id]["global_score"],
            "reason": "llm_chat_error"
        }

    # 4. Update the Two-Tiered Database
    sessions_db[req.session_id]["session_score"] += score_added
    users_db[req.user_id]["global_score"] += score_added

    print(f"Session Score: {sessions_db[req.session_id]['session_score']} | Global Score: {users_db[req.user_id]['global_score']}")

    # 5. Return (We return global_score as total_score to keep UI happy)
    return {
        "reply": reply,
        "score_added": score_added,
        "total_score": users_db[req.user_id]["global_score"], 
        "reason": reason
    }