import streamlit as st
import requests
import time

BACKEND_URL = "http://127.0.0.1:5000/chat"

st.set_page_config(
    page_title="AWS AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ✅ Title + description
st.title("🤖 AWS AI Assistant")
st.caption("Ask me anything about AWS, DevOps, Linux, and Python 🚀")

# ✅ Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Input box
prompt = st.chat_input("Ask about EC2, S3, Lambda, DevOps, etc...")

if prompt:
    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ Call backend
    response = requests.post(
        BACKEND_URL,
        json={
            "message": prompt,
            "session_id": "deepak"
        }
    )

    answer = response.json()["response"]

    # ✅ Loader + fake thinking delay
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            time.sleep(1)
            st.markdown(answer)

    # Save assistant reply
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
