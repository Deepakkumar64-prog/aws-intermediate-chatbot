from chatbot.ai_provider import get_ai_response
from chatbot.rag_engine import get_relevant_chunks


class ChatbotEngine:
    def __init__(self):
        pass

    def generate_response(self, message, history, index=None, chunks=None):

        # ✅ Get RAG context
        context = ""

        if index is not None and chunks is not None:
            context = get_relevant_chunks(message, index, chunks)

        # ✅ Call AI with context
        response = get_ai_response(context, message)

        return response