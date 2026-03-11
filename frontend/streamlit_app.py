import streamlit as st
import requests

st.set_page_config(page_title="SKILLRANK AI ", layout="centered")

st.title("SKILLRANK AI")

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "score" not in st.session_state:
    st.session_state.score = 0


# ---------------- SIDEBAR ----------------

with st.sidebar:

    if st.button("Reset Conversation"):

        st.session_state.messages = []
        st.session_state.score = 0

        st.rerun()


# ---------------- DISPLAY CHAT ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------- USER INPUT ----------------

prompt = st.chat_input("Ask something")

if prompt:

    # show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # send request BEFORE storing the assistant reply
    try:

        res = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "message": prompt,
                "history": st.session_state.messages
            }
        )

        data = res.json()

        reply = data["reply"]
        score_added = data["score_added"]
        total_score = data["total_score"]

        st.session_state.score = total_score

        # store messages ONLY ONCE
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        with st.chat_message("assistant"):
            st.markdown(reply)

    except:
        st.error("Backend connection failed")


st.write("SkillRank:", st.session_state.score)
