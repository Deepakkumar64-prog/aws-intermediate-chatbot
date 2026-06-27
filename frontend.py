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

# ✅ Process PDF
if uploaded_file:
    if "index" not in st.session_state:
        with st.spinner("Processing PDF..."):
            index, chunks = process_pdf(uploaded_file)
            st.session_state.index = index
            st.session_state.chunks = chunks

        st.success("✅ PDF processed successfully!")

# ✅ Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Input box (VERY IMPORTANT — this defines prompt ✅)
prompt = st.chat_input("Ask about EC2, S3, Lambda, DevOps, etc...")

# ✅ RAG-enabled chat
if prompt:
    # Add user message
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

    # ✅ Create final prompt
    final_prompt = f"""
    Answer the question based on the context below:

    Context:
    {context}

    Question:
    {prompt}
    """

    # ✅ Call backend
    response = requests.post(
        BACKEND_URL,
        json={
            "message": final_prompt,
            "session_id": "deepak"
        }
    )

    answer = response.json()["response"]

    # ✅ Show response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            time.sleep(1)
            st.markdown(answer)

    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )