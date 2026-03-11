from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from skillrank_engine import SkillRankEngine
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
engine = SkillRankEngine()

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    timeout=60.0
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list | None = None
# Token Count 
def token_count(text):
    return len(enc.encode(text))

#  LLM RESPONSE GENERATION

def generate_reply(messages):

    print("STEP 1 → Calling LLM")

    response = client.chat.completions.create(
        model="mistral-7b-instruct-v0.2",
        messages=messages,
        temperature=0.7,
        max_tokens=30000
    )

    reply = response.choices[0].message.content

    print("STEP 1 DONE → Reply Generated")
    response_tokens = token_count(reply)
    print("\n================ TOKEN DEBUG ================")
    print("Response tokens:", response_tokens)
    print("============================================\n")
    return reply



# SEMANTIC ANALYSIS


def semantic_analysis(prompt):

    print("STEP 2 → Semantic Analysis")

    text = prompt.lower()
    words = len(text.split())

    if words < 4:
        score = 1
        reason = "very basic question"

    elif "difference" in text or "compare" in text:
        score = 5
        reason = "comparative reasoning"

    elif "why" in text or "how" in text:
        score = 4
        reason = "conceptual reasoning"

    elif words > 15:
        score = 6
        reason = "complex multi-topic question"

    else:
        score = 2
        reason = "normal question"

    print("STEP 2 DONE → Score:", score)

    return score, reason



#  UPDATE SKILLRANK


def update_score(score):

    print("STEP 3 → Updating SkillRank")

    engine.total_score += score

    print("STEP 3 DONE → Total Score:", engine.total_score)

    return engine.total_score



# MAIN CHAT ENDPOINT

@app.post("/chat")
def chat(req: ChatRequest):

    messages = []

    if req.history:
        messages.extend(req.history)
    SYSTEM_PROMPT = """
You are an AI tutor.

Rules:
- Give short responses unless the user asks for details.
- If the message is a any type of greeting , reply briefly.
- Only explain in detail when the user asks a learning question.
"""

    messages.append({
        "role": "user",
        "content": SYSTEM_PROMPT + "\nUser question: " + req.message
    })

    print("USER MESSAGE:", req.message)

    # -----------------------------
    # STEP 1 → LLM REPLY
    # -----------------------------
    try:
        reply = generate_reply(messages)

    except Exception as e:

        print("LLM ERROR:", e)

        return {
            "reply": "Model error occurred",
            "score_added": 0,
            "total_score": engine.total_score,
            "reason": "llm_error"
        }

    # -----------------------------
    # STEP 2 → SEMANTIC SCORING
    # -----------------------------
    try:
        score_added, reason = semantic_analysis(req.message)

        total_score = update_score(score_added)

    except Exception as e:

        print("SCORING ERROR:", e)

        score_added = 0
        reason = "scoring_error"
        total_score = engine.total_score

    # -----------------------------
    # FINAL RESPONSE
    # -----------------------------
    return {
        "reply": reply,
        "score_added": score_added,
        "total_score": total_score,
        "reason": reason
    }