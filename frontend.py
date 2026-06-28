import streamlit as st
import time

# ✅ RAG imports
from chatbot.rag_engine import process_pdf, get_relevant_chunks
from chatbot.chatbot_engine import ChatbotEngine

# ✅ Initialize engine
engine = ChatbotEngine()

st.set_page_config(
    page_title="AWS AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ✅ Title
st.title("🤖 AWS AI Assistant")
st.caption("Ask me anything about AWS, DevOps, Linux, and Python 🚀")

# ✅ Initialize uploader key
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

# ✅ Reset button (FULLY FIXED ✅)
if st.button("🔄 Reset Documents"):
    # Clear session safely
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # Recreate uploader key
    st.session_state["uploader_key"] = 0

    # ✅ Correct rerun (NEW API)
    st.rerun()

# ✅ Multi-PDF uploader (with key)
uploaded_files = st.file_uploader(
    "📄 Upload multiple PDFs",
    type="pdf",
    accept_multiple_files=True,
    key=st.session_state["uploader_key"]
)

# ✅ Process PDFs
if uploaded_files:
    if "index" not in st.session_state:
        with st.spinner("Processing PDFs..."):

            all_chunks = []

            for file in uploaded_files:
                idx, chunks = process_pdf(file)

                if chunks:
                    for chunk in chunks:
                        all_chunks.append(f"[{file.name}] {chunk}")

            # ✅ Create embeddings
            from sentence_transformers import SentenceTransformer
            import numpy as np
            import faiss

            model = SentenceTransformer("all-MiniLM-L6-v2")

            embeddings = model.encode(all_chunks)
            embeddings = np.array(embeddings).astype("float32")

            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)

            st.session_state["index"] = index
            st.session_state["chunks"] = all_chunks

        st.success("✅ All PDFs processed successfully!")

# ✅ Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ✅ Display chat
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Input
prompt = st.chat_input("Ask about EC2, S3, Lambda, DevOps, etc...")

# ✅ Chat logic
if prompt:
    st.session_state["messages"].append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ Get context
    context = ""
    if "index" in st.session_state:
        context = get_relevant_chunks(
            prompt,
            st.session_state["index"],
            st.session_state["chunks"]
        )

    # ✅ Generate response
    answer = engine.generate_response(
        prompt,
        history=[],
        context=context
    )

    # ✅ Show response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            time.sleep(1)
            st.markdown(answer)

    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )