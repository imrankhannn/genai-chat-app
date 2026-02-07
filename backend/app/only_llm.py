from langchain_ollama import OllamaLLM
from app.memory_store import get_memories

llm = OllamaLLM(
    model="llama3.2:1b",
    temperature=0.4
)

def ask_llm(question: str, session_id: str) -> str:
    memory = get_memories(session_id)["llm"]

    chat_history = memory.load_memory_variables({}).get("history", "")

    prompt = f"""
You are a helpful AI assistant.
Answer clearly and concisely.

Chat history:
{chat_history}

Human:
{question}

AI:
"""

    answer = llm.invoke(prompt)

    memory.save_context(
        {"input": question},
        {"output": answer}
    )

    return answer