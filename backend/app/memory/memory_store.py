from langchain_classic.memory import ConversationBufferWindowMemory

session_memories = {}

# Mode will be:

# "llm"

# "rag"

def get_memory(session_id: str, mode: str):
    key = f"{session_id}_{mode}"

    if key not in session_memories:
        session_memories[key] = ConversationBufferWindowMemory(
            k=3,
            return_messages=True
        )

    return session_memories[key]
