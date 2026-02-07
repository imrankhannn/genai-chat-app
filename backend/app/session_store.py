# session_id -> session data
sessions = {}

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "vector_store": None,
            "doc_uploaded": False
        }
    return sessions[session_id]

def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
