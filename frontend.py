import streamlit as st
import requests
import time

# ✅ RAG imports
from chatbot.rag_engine import process_pdf, get_relevant_chunks

BACKEND_URL = "http://127.0.0.1:5000/chat"

st.set_page_config(
    page_title="AWS AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ✅ Title
st.title("🤖 AWS AI Assistant")
st.caption("Ask me anything about AWS, DevOps, Linux, and Python 🚀")

# ✅ PDF uploader
uploaded_file = st.file_uploader("📄 Upload a PDF", type="pdf")

# ✅ Process PDF only once
if uploaded_file:
    if "index" not in st.session_state:
        with st.spinner("Processing PDF..."):
            index, chunks = process_pdf(uploaded_file)
            st.session_state.index = index
            st.session_state.chunks = chunks
        st.success("✅ PDF processed successfully!")

# ✅ Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Input box
prompt = st.chat_input("Ask about EC2, S3, Lambda, DevOps, etc...")

# ✅ RAG + AI chat logic
if prompt:
    # ✅ Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ Get RAG context
    context = ""

    if "index" in st.session_state:
        context = get_relevant_chunks(
            prompt,
            st.session_state.index,
            st.session_state.chunks
        )

    # ✅ Call backend (IMPORTANT CHANGE)
    response = requests.post(
        BACKEND_URL,
        json={
            "message": prompt,
            "context": context,   # ✅ NEW (send context separately)
            "session_id": "deepak"
        }
    )

    answer = response.json()["response"]

    # ✅ Show AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            time.sleep(1)
            st.markdown(answer)

    # ✅ Save assistant reply
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )