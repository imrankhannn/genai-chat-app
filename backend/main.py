from fastapi import FastAPI
from app.only_llm import ask_llm
from pydantic import BaseModel
# from app.rag import (
#     load_documents,
#     create_embedding,
#     create_vector_store,
#     chunk_documents,
#     add_documents_to_vector_store,
#     answer_with_rag,
#     load_pdf_document
# )
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import shutil
import os

# from app.session_store import get_session
# from app.doc_ingestion import ingest_document

app=FastAPI()


UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload-doc")
# def upload_doc(session_id: str, file: UploadFile = File(...)):
#     session = get_session(session_id)

#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     session["vector_store"] = ingest_document(file_path)
#     session["doc_uploaded"] = True

#     return {"status": "Document uploaded and indexed"}


app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"], # for localhost
    allow_origins=["*"], # for cloud server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    session_id: str


# docs = load_documents()
# embeddings = create_embedding()
# vector_store = create_vector_store(docs, embeddings)

# # 2️⃣ Load PDF
# pdf_docs = load_pdf_document("Utils/Moltbook.pdf")

# # 3️⃣ Chunk PDF
# pdf_chunks = chunk_documents(pdf_docs)

# 4️⃣ Add to FAISS
# add_documents_to_vector_store(vector_store, pdf_chunks)

@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/ask-rag-chat")
def ask_rag_chat(req: QuestionRequest):
    question = req.question
    session_id = req.session_id

    if not question.strip():
        return {"error": "Question cannot be empty"}

    # answer, _ = answer_with_rag(vector_store, question, session_id)
    return {"answer": answer}

@app.post("/ask-llm")
def ask_llm_chat(req: QuestionRequest):
    if not req.question.strip():
        return {"error": "Question cannot be empty"}

    return {"answer": ask_llm(req.question, req.session_id)}

from app.doc_chat import ask_doc_chat

@app.post("/ask-doc-chat")
def ask_doc_chat_api(req: QuestionRequest):
    return {
        "answer": ask_doc_chat(req.question, req.session_id)
    }



# just for learning purpose

# @app.get("/")
# def run():
#     return {"msg":"Welcome"}

# @app.post("/ask")
# def ask(question):
#     if len(question.strip())<3:
#         return "Please ask proper question"
#     answer = ask_llm(question)
#     return {
#         "question":question,
#         "answer":answer
#         }

# without RAG

# @app.post("/ask")
# def ask(question):
#     if not question.strip():
#         return {"error": "Question cannot be empty"}

#     answer = ask_llm(question)
#     return {"answer": answer}