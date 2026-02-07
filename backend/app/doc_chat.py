# Using Cloud LLM

from app.groq_client import get_groq_client
# from app.memory_store import get_memories
from app.session_store import get_session

client = get_groq_client()

def ask_doc_chat(question: str, session_id: str) -> str:
    session = get_session(session_id)
    # memory = get_memories(session_id)["doc"]

    retriever = session["vector_store"].as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(question)

    context = "\n".join(d.page_content for d in docs)

    # history = memory.load_memory_variables({}).get("history", [])

    messages = [
        {"role": "system", "content": """You are a helpful AI assistant.
Use the context and chat history below to answer the question.
Your response MUST be a single, complete answer.
DO NOT add explanations about missing information.
Only say "I don't know" if the context is completely unrelated.
Answer should not be more than 50 words."""}
    ]

    # for msg in history:
    #     messages.append({
    #         "role": "user" if msg.type == "human" else "assistant",
    #         "content": msg.content
    #     })

    messages.append({
        "role": "user",
        "content": f"""
Context:
{context}

Question:
{question}
"""
    })

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.3
    )

    answer = response.choices[0].message.content.strip()

    # if answer.lower() != "i don't know":
    #     memory.save_context(
    #         {"input": question},
    #         {"output": answer}
    #     )

    return answer


#Using Ollama LLM

# from langchain_ollama import OllamaLLM
# from app.session_store import get_session
# from app.memory_store import get_memories

# llm = OllamaLLM(model="llama3.2:1b", temperature=0.3)

# def ask_doc_chat(question: str, session_id: str):
#     session = get_session(session_id)
#     memory = get_memories(session_id)["doc"]

#     if not session["doc_uploaded"]:
#         return "No document uploaded for this session."

#     retriever = session["vector_store"].as_retriever(search_kwargs={"k": 3})
#     docs = retriever.invoke(question)

#     #Testing
#     # print("🔍 Retrieved docs count:", len(docs))
#     # for i, d in enumerate(docs):
#     #     print(f"\n--- DOC {i+1} ---\n")
#     #     print(d.page_content[:500])

#     context = "\n".join(doc.page_content for doc in docs)
#     chat_history = memory.load_memory_variables({}).get("history", "")

#     prompt = f"""
# You are a helpful AI assistant.

# Use the context and chat history below to answer the question.
# Your response MUST be a single, complete answer.
# DO NOT add explanations about missing information.
# Only say "I don't know" if the context is completely unrelated.

# Chat history:
# {chat_history}

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
#     answer = llm.invoke(prompt)

#     if answer.strip().lower() != "i don't know":
#         memory.save_context(
#             {"input": question},
#             {"output": answer}
#         )

#     return answer
