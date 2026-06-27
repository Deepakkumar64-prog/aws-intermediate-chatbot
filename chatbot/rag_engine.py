from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ✅ Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def split_text(text, chunk_size=500, overlap=100):
    """
    Custom text splitter (replaces LangChain dependency ✅)
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def process_pdf(file):
    """
    Reads PDF and creates embeddings index
    """

    reader = PdfReader(file)
    text = ""

    # ✅ Extract text
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    # ✅ Handle empty file
    if not text.strip():
        return None, []

    # ✅ Split text (no LangChain)
    chunks = split_text(text)

    # ✅ Convert chunks into embeddings
    embeddings = model.encode(chunks)

    embeddings = np.array(embeddings).astype("float32")

    # ✅ Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index, chunks


def get_relevant_chunks(query, index, chunks):
    """
    Retrieve most relevant chunks
    """

    if index is None or len(chunks) == 0:
        return "No document content available."

    # ✅ Encode query
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype("float32")

    # ✅ Search FAISS
    distances, indices = index.search(query_vector, k=3)

    results = []
    for i in indices[0]:
        if i < len(chunks):
            results.append(chunks[i])

    return "\n".join(results)
