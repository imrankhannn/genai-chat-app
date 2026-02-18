from app.core.groq_client import get_groq_client
from app.memory.memory_store import get_memory

def ask_rag(question: str, session_id: str, vector_store):

    client = get_groq_client()
    memory = get_memory(session_id, "rag")

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)

    context = "\n".join([doc.page_content for doc in docs])

    history = memory.load_memory_variables({}).get("history", [])

    messages = [
        {
            "role": "system",
            "content": "Answer using only provided context. If not found, say I don't know."
        }
    ]

    for msg in history:
        if msg.type == "human":
            messages.append({"role": "user", "content": msg.content})
        elif msg.type == "ai":
            messages.append({"role": "assistant", "content": msg.content})

    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion:\n{question}"
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3
    )

    answer = response.choices[0].message.content.strip()

    memory.save_context({"input": question}, {"output": answer})

    return answer
