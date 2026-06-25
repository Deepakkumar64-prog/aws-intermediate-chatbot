from flask import Flask, request, jsonify
from flask_cors import CORS

from chat_memory import ChatMemory
from chatbot_engine import ChatbotEngine

app = Flask(__name__)
CORS(app)

memory = ChatMemory()
bot = ChatbotEngine()

# 🧠 Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_message = data.get("message")
    session_id = data.get("session_id", "default_user")

    # store user message
    memory.add_message(session_id, "user", user_message)

    # get history
    history = memory.get_history(session_id)

    # generate bot response
    response = bot.generate_response(user_message, history)

    # store bot response
    memory.add_message(session_id, "bot", response)

    return jsonify({
        "session_id": session_id,
        "response": response,
        "history": history
    })


# 🧹 Clear chat
@app.route("/clear", methods=["POST"])
def clear():
    data = request.get_json()
    session_id = data.get("session_id", "default_user")

    memory.clear_history(session_id)

    return jsonify({
        "message": "Chat cleared",
        "session_id": session_id
    })


# 🚀 Health check
@app.route("/", methods=["GET"])
def home():
    return "AWS Intermediate Chatbot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
