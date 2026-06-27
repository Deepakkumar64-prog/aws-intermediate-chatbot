import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000/chat"

st.set_page_config(
    page_title="AWS Intermediate Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AWS Intermediate Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything about AWS...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        BACKEND_URL,
        json={
            "message": prompt,
            "session_id": "deepak"
        }
    )

    answer = response.json()["response"]

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
