from flask import Flask, request, jsonify
from chatbot.chat_memory import ChatMemory
from chatbot.chatbot_engine import ChatbotEngine

# ✅ Create Flask app (THIS WAS MISSING ❗)
app = Flask(__name__)

# ✅ Initialize components
memory = ChatMemory()
engine = ChatbotEngine()


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message")
    context = data.get("context", "")   # ✅ for RAG
    session_id = data.get("session_id")

    # ✅ Get chat history
    history = memory.get_history(session_id)

    # ✅ Generate response (RAG + AI)
    response = engine.generate_response(message, history, context)

    # ✅ Save memory
    memory.add_message(session_id, "user", message)
    memory.add_message(session_id, "assistant", response)

    return jsonify({"response": response})


# ✅ Start server
if __name__ == "__main__":
    app.run(debug=True)