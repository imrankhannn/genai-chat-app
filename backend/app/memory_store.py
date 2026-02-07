# from langchain_classic.memory import ConversationBufferWindowMemory

# # session_id -> memories
# session_memories = {}

# def get_memories(session_id: str):
#     if session_id not in session_memories:
#         session_memories[session_id] = {
#             "llm": ConversationBufferWindowMemory(
#                 k=3,
#                 return_messages=True
#             ),
#             "doc": ConversationBufferWindowMemory(
#                 k=3,
#                 return_messages=True
#             )
#         }
#     return session_memories[session_id]