# backend/services/ai_agent.py
from openai import OpenAI
import json
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio",
    timeout=60.0
)

def token_count(text):
    return len(enc.encode(text))

def generate_reply(messages):
    print("STEP 1 → Calling LLM for Chat Response")
    chat_messages = [
        {"role": "system", "content": "You are a helpful, intelligent, and concise tutor."}
    ]
    chat_messages.extend(messages)
    
    response = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",
        messages=chat_messages,
        temperature=0.7,
        max_tokens=2000 
    )
    print("STEP 1 DONE → Reply Generated")
    return response.choices[0].message.content

def evaluate_curiosity(user_prompt):
    print("STEP 2 → Calling LLM for Curiosity Score")
    SYSTEM_PROMPT = """
You are an expert behavioral analyst and educator. Your sole purpose is to evaluate the "Curiosity Depth" of the user's input on a scale of 1 to 10.
Evaluate the user's "Curiosity Depth" from 1 to 10 based on this rubric:

1-3 (Surface): Basic facts, simple trivia, or asking the AI to write/generate code.
4-7 (Exploring): Asking for broad explanations, summaries, or general tutorials.
8-10 (Deep): Highly specific questions exploring "how" or "why" complex concepts interact.

You must output ONLY valid JSON. No markdown, no conversational text.
Format:
{"score": <integer>, "reasoning": "<one short sentence>"}
"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",
            messages=messages,
            temperature=0.1, 
        )
        reply = response.choices[0].message.content
        
        # Clean the markdown backticks
        reply = reply.replace("```json", "").replace("```", "").strip()
        data = json.loads(reply)

        score = int(data.get("score", 1))
        reason = data.get("reasoning", "No reason provided")

        print(f"STEP 2 DONE → AI Score: {score} | Reason: {reason}")
        return score, reason

    except Exception as e:
        print("SCORING AI ERROR:", e)
        return 1, "Failed to parse AI score"