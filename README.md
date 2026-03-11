# SkillRank AI

SkillRank AI is an experimental AI learning assistant that not only answers questions but also evaluates the quality of the questions being asked.

Instead of simply chatting with an AI, the system attempts to measure how thoughtful, analytical, or complex a user's question is and awards a "SkillRank" score accordingly.

The idea behind the project is simple:  
**better questions lead to better learning.**

---

## Project Aim

The main aim of SkillRank AI is to encourage deeper thinking while learning.

Most AI chat systems focus only on giving answers.  
This project explores a different idea — evaluating **how users ask questions**.

By rewarding curiosity, reasoning, and analytical questioning, the system tries to guide users toward more meaningful learning interactions.

The goal is to move from:   Ask question → Get answer

to something closer to:   Ask better questions → Learn better


## What This Project Does

- Provides an AI tutor interface for asking questions
- Uses a local large language model to generate explanations
- Analyzes user questions for reasoning and complexity
- Awards SkillRank points based on question quality
- Tracks conversation history so the AI remembers context

---

## System Architecture

The system runs locally and consists of three main components.
User
↓
Streamlit Frontend
↓
FastAPI Backend
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
- Mistral 7B Instruct v0.2 Q4_K_S

Utilities
- tiktoken (token counting)
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

### Conversation Memory
The chatbot remembers the conversation by passing message history to the model.

### Local LLM
The entire system runs locally using LM Studio.

---

## How It Works

1. User sends a message through the Streamlit interface
2. The message and conversation history are sent to the backend
3. The backend sends the prompt to the local LLM
4. The LLM generates a response
5. The system analyzes the user's question
6. SkillRank score is updated
7. The response and updated score are returned to the UI

---

## Running the Project

Start the backend:  uvicorn main:app --reload


Start the frontend:  streamlit run frontend/streamlit_app.py


Make sure LM Studio is running with a loaded model.

---

## Current Limitations

- SkillRank scoring is currently rule-based
- Conversation history grows and needs trimming
- No database storage yet (sessions reset after restart)

---

## Future Improvements

- LLM-based semantic scoring
- Long-term conversation memory
- Automatic conversation summarization
- SkillRank progress dashboard
- Multiple AI tutor modes

---

## Motivation

Learning is not only about getting answers.  
It is about asking better questions.

SkillRank AI is an attempt to build a system that encourages curiosity, deeper thinking, and more meaningful learning conversations.

---

## License

MIT
