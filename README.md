# SkillRank AI

SkillRank AI is an experimental AI learning assistant that not only answers questions but also evaluates the quality of the questions being asked and the effort put into reading the answers.

Instead of simply chatting with an AI, the system attempts to measure how thoughtful, analytical, or complex a user's question is. It also actively recognizes when a student is taking learning shortcuts (like speed-reading or skipping material) and intervenes to course-correct, awarding a "SkillRank" score based on genuine engagement.

The idea behind the project is simple:  
**Better effort and better questions lead to deeper understanding.**

---

## Project Aim

The main aim of SkillRank AI is to encourage deeper thinking while learning and to act as an Effort Tracker.

Most AI chat systems focus only on giving answers, which can inadvertently enable surface-level learning.  
This project explores a different idea — evaluating **how users ask questions and how they consume the answers**.

By rewarding curiosity, reasoning, and analytical questioning, and gently redirecting rushed or low-effort behavior, the system tries to guide users toward more meaningful learning interactions.

The goal is to move from:   Ask question → Get answer

to something closer to:   Show effort + Ask better questions → Learn deeply

---

## What This Project Does

- Provides an AI tutor interface for asking questions
- Uses a local large language model to generate explanations
- Analyzes user questions for reasoning and complexity
- Tracks user reading pace to encourage full comprehension
- Deploys engagement checks if rushed learning is detected
- Awards or adjusts SkillRank points based on effort and quality
- Tracks conversation history so the AI remembers context

---

## System Architecture

The system runs locally and consists of three main components.

User
↓
Streamlit Frontend
↓
FastAPI Backend (Velocity Tracking & Engagement Logic)
↓
Local LLM (LM Studio)
↓
Response + SkillRank Score

---

## Tech Stack

Frontend
- Streamlit

Backend
- FastAPI
- Python

LLM Inference
- LM Studio
- Meta Llama 3.1 8B Instruct

Utilities
- Standard Python Math/Time libraries (Velocity tracking)
- requests

---

## Features

### AI Tutor
Users can ask questions about topics they want to learn.

### SkillRank Scoring
Questions are analyzed for complexity and reasoning.

Examples:
- Basic question → small score  
- Conceptual question (why/how) → higher score  
- Comparative or multi-topic questions → highest score  

### Engagement Checks (Course Correction)
The backend uses math to recognize when a student is rushing, prompting them to slow down and engage with the material before waking up the LLM.
- **Pacing Check:** Calculates the AI's word count and sets a baseline reading time. Replying too fast flags that the user might be skipping the material.
- **Comprehension Check:** If a user triggers the pacing check or claims to read abnormally fast, the backend intercepts the prompt. It provides a focused reading passage and a short timer, challenging the user to demonstrate actual comprehension before moving forward.

### Conversation Memory
The chatbot remembers the conversation by passing message history to the model.

### Local LLM
The entire system runs locally using LM Studio to save costs and ensure privacy.

---

## How It Works

1. User sends a message through the Streamlit interface
2. The backend intercepts the message and calculates the time elapsed since the last AI response
3. If the user replies too quickly, the backend initiates a comprehension check to guide them back to focused reading
4. If the user is engaging at a healthy pace, the message and history are sent to the local LLM
5. The LLM generates a response
6. The system analyzes the user's question for curiosity
7. SkillRank score is updated and the new response's word count/timestamp is saved
8. The response and updated score are returned to the UI

---

## Running the Project

Start the AI Brain: Ensure LM Studio is running with a loaded model on port 1234.

Start the backend:  uvicorn main:app --reload

Start the frontend:  streamlit run frontend/streamlit_app.py

---

## Current Limitations

- SkillRank scoring is currently rule-based
- Conversation history grows and needs trimming
- No database storage yet (sessions and scores reset after server restart)
- Frontend cannot yet detect browser-level context (like switching tabs)

---

## Future Improvements

- **SQLite Database Integration:** Migrate from temporary RAM dictionaries to a permanent database for long-term score tracking.
- **Misdirection Checks:** Introduce fabricated concepts to detect when users are copy-pasting prompts into external tools, prompting a discussion about academic integrity.
- **Frontend Migration:** Move from Streamlit to React/Next.js to enable better environmental context for the tutor.
- **LLM-based Semantic Scoring:** Upgrade from rule-based scoring to advanced AI evaluation.
- **SkillRank Progress Dashboard:** A dedicated UI page to view long-term effort analytics.

---

## Motivation

Learning is not only about getting answers.  
It is about putting in the effort, staying focused, and asking better questions.

SkillRank AI is an attempt to build a system that encourages curiosity, verifies cognitive effort, and fosters a space where shortcuts are replaced with genuine understanding.

---

## License

MIT
