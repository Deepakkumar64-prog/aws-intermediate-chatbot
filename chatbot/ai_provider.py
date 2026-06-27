import os
from openai import OpenAI
from dotenv import load_dotenv
from chatbot.prompts import SYSTEM_PROMPT

# Load env variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_response(message, history):
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        # Add past conversation (memory)
        for msg in history:
            messages.append(msg)

        # Add current message
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
