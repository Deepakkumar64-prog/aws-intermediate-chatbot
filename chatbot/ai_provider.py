from transformers import pipeline

# ✅ Stable working model (compatible with your system)
generator = pipeline("text-generation", model="gpt2")


def get_ai_response(context, question):
    try:
        prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

        response = generator(
            prompt,
            max_length=200,
            temperature=0.7,
            do_sample=True
        )

        # ✅ Clean output
        answer = response[0]["generated_text"]
        answer = answer.replace(prompt, "").strip()

        return answer

    except Exception as e:
        return f"Error: {str(e)}"
