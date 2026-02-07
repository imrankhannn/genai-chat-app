# Using cloud LLM

# from app.memory_store import get_memories
from app.groq_client import get_groq_client

client = get_groq_client()

def ask_llm(question: str, session_id: str) -> str:
    # memory = get_memories(session_id)["llm"]

    messages = [
        {"role": "system", "content": """You are a helpful AI assistant.
Answer clearly and concisely.
Answer should not be more than 50 words."""
         }
    ]

    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.4
    )

    answer = response.choices[0].message.content.strip()

    # if answer.lower() != "i don't know":
    #     memory.save_context(
    #         {"input": question},
    #         {"output": answer}
    #     )

    return answer



# Using Ollama LLM


# from langchain_ollama import OllamaLLM
# from app.memory_store import get_memories

# llm = OllamaLLM(
#     model="llama3.2:1b",
#     temperature=0.4
# )

# def ask_llm(question: str, session_id: str) -> str:
#     memory = get_memories(session_id)["llm"]

#     chat_history = memory.load_memory_variables({}).get("history", "")

#     prompt = f"""
# You are a helpful AI assistant.
# Answer clearly and concisely.
# Answer should not be more than 50 words.

# Chat history:
# {chat_history}

# Human:
# {question}

# AI:
# """

#     answer = llm.invoke(prompt)

#     memory.save_context(
#         {"input": question},
#         {"output": answer}
#     )

#     return answer