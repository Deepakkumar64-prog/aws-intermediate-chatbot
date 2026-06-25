class ChatbotEngine:
    def __init__(self):
        pass

    def generate_response(self, message, history):
        """
        Simple rule-based response (we will upgrade to AWS/OpenAI later)
        """

        message = message.lower()

        if "aws" in message:
            return "AWS is a cloud platform offering EC2, S3, Lambda, and more."

        if "hello" in message or "hi" in message:
            return "Hello! I am your AWS Intermediate Chatbot."

        if "help" in message:
            return "You can ask me about AWS services or general questions."

        return f"You said: {message}. (AI integration will be added soon)"
