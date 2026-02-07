from langchain_ollama import OllamaLLM
from app.session_store import get_session
from app.memory_store import get_memories

llm = OllamaLLM(model="llama3.2:1b", temperature=0.3)

def ask_doc_chat(question: str, session_id: str):
    session = get_session(session_id)
    memory = get_memories(session_id)["doc"]

    if not session["doc_uploaded"]:
        return "No document uploaded for this session."

    retriever = session["vector_store"].as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(question)

    #Testing
    # print("🔍 Retrieved docs count:", len(docs))
    # for i, d in enumerate(docs):
    #     print(f"\n--- DOC {i+1} ---\n")
    #     print(d.page_content[:500])

    context = "\n".join(doc.page_content for doc in docs)
    chat_history = memory.load_memory_variables({}).get("history", "")

    prompt = f"""
You are a helpful AI assistant.

Use the context and chat history below to answer the question.
Your response MUST be a single, complete answer.
DO NOT add explanations about missing information.
Only say "I don't know" if the context is completely unrelated.

Chat history:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""
    answer = llm.invoke(prompt)

    if answer.strip().lower() != "i don't know":
        memory.save_context(
            {"input": question},
            {"output": answer}
        )

    return answer
