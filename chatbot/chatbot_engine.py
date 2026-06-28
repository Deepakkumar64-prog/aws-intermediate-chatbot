from chatbot.ai_provider import get_ai_response


class ChatbotEngine:
    def __init__(self):
        pass

    def generate_response(self, message, history, context=""):
        """
        Generate response using RAG context + AI model
        """

        # ✅ Ensure safe context
        if context is None:
            context = ""

        # ✅ Call AI with context + user question
        response = get_ai_response(context, message)

        return response
