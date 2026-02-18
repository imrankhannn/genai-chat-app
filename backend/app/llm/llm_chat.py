from app.core.groq_client import get_groq_client
from app.memory.memory_store import get_memory

def ask_llm(question: str, session_id: str):

    client = get_groq_client()
    memory = get_memory(session_id, "llm")

    history = memory.load_memory_variables({}).get("history", [])

    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

    for msg in history:
        if msg.type == "human":
            messages.append({"role": "user", "content": msg.content})
        elif msg.type == "ai":
            messages.append({"role": "assistant", "content": msg.content})

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.4
    )

    answer = response.choices[0].message.content.strip()

    memory.save_context({"input": question}, {"output": answer})

    return answer
