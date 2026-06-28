import streamlit as st
import time

# ✅ RAG imports
from chatbot.rag_engine import process_pdf, get_relevant_chunks
from chatbot.chatbot_engine import ChatbotEngine

# ✅ Initialize engine
engine = ChatbotEngine()

# ✅ Page config (BROWSER TAB NAME)
st.set_page_config(
    page_title="Deepak AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ✅ Header (MAIN TITLE)
st.title("🤖 Deepak AI Assistant")

# ✅ Description
st.caption("Hey! I'm Deepak’s AI Assistant 🤖 — Ask me anything about AWS, DevOps, and AI 🚀")

# ✅ Sidebar branding (PRO LOOK 🔥)
st.sidebar.title("👨‍💻 About")
st.sidebar.write("Deepak AI Assistant")
st.sidebar.write("Built using RAG + FAISS + Transformers")
st.sidebar.write("🚀 Deployed on Streamlit Cloud")

# ✅ Initialize uploader key
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0

# ✅ RESET BUTTON (FINAL FIX)
if st.button("🔄 Reset Documents"):
    # ✅ Create new uploader key → clears file uploader
    st.session_state["uploader_key"] += 1

    # ✅ Clear only required data
    for key in ["index", "chunks", "messages"]:
        if key in st.session_state:
            del st.session_state[key]

    # ✅ Refresh UI
    st.rerun()

# ✅ File uploader
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

# ✅ Chat history init
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ✅ Display chat messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Chat input
prompt = st.chat_input("Ask anything about AWS, DevOps, AI...")

# ✅ Chat logic
if prompt:
    st.session_state["messages"].append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ Get context from RAG
    context = ""
    if "index" in st.session_state:
        context = get_relevant_chunks(
            prompt,
            st.session_state["index"],
            st.session_state["chunks"]
        )

    # ✅ AI response
    answer = engine.generate_response(
        prompt,
        history=[],
        context=context
    )

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