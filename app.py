from flask import Flask, request, jsonify
from chatbot.chat_memory import ChatMemory
from chatbot.chatbot_engine import ChatbotEngine

app = Flask(__name__)

memory = ChatMemory()
engine = ChatbotEngine()


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message")
    session_id = data.get("session_id")

    history = memory.get_history(session_id)

    response = engine.generate_response(message, history)

    memory.add_message(session_id, "user", message)
    memory.add_message(session_id, "assistant", response)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)