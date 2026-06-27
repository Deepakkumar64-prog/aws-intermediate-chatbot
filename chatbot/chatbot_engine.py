from chatbot.ai_provider import get_ai_response


class ChatbotEngine:
    def __init__(self):
        pass

    def generate_response(self, message, history):
        return get_ai_response(message, history)