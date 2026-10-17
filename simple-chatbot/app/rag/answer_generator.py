import os

from ollama import chat

MODEL_NAME = os.getenv("OLLAMA_MODEL", "granite4.1:8b")

SYSTEM_PROMPT = """
You are a question-answering assistant for question-answering tasks.

Rules:
1. Respond in the same language as the user.
2. Only use the retrieved context to answer the question.
3. If you don't know the answer, or the answer is not contained in the retrieved context, just say that you don't know.
4. Use three sentences maximum and keep the answer concise. 
"""


def generate_answer(question: str, retrieved_documents: list[dict]) -> str:
    if not retrieved_documents:
        return (
            "I did not find relevant information "
            "in the knowledge base to answer your question."
        )

    user_prompt = f"""
    Use the following context to answer the question.

    <context>
    {retrieved_documents}
    </context>

    User question:
    {question}
    """

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        options={
            "temperature": 0.2
        }
    )

    return response.message.content.strip()
