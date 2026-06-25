from collections import defaultdict

class ChatMemory:
    def __init__(self):
        # stores chat history per session_id
        self.memory = defaultdict(list)

    def add_message(self, session_id, role, message):
        self.memory[session_id].append({
            "role": role,
            "message": message
        })

    def get_history(self, session_id):
        return self.memory[session_id]

    def clear_history(self, session_id):
        self.memory[session_id] = []
