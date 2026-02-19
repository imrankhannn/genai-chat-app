from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

from app.llm.llm_chat import ask_llm
from app.rag.document_loader import load_document
from app.rag.vector_store import create_vector_store
from app.rag.rag_chat import ask_rag

from app.rag.web_loader import load_website
from app.rag.vector_store import create_vector_store


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    session_id: str

session_vector_store = None
current_session_id = None

web_vector_store = None
current_web_session = None

@app.get("/")
def home():
    return {"status":"ok"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...), session_id: str = None):
    global session_vector_store, current_session_id

    # Reset everything on new upload
    session_vector_store = None
    current_session_id = None

    file_location = f"temp_{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents = load_document(file_location)
    session_vector_store = create_vector_store(documents)

    current_session_id = session_id

    os.remove(file_location)

    return {"message": "File processed and old session cleared"}

@app.post("/load-website")
def load_website_api(url: str, session_id: str):
    global web_vector_store, current_web_session

    web_vector_store = None
    current_web_session = None

    documents = load_website(url)
    web_vector_store = create_vector_store(documents)

    current_web_session = session_id

    return {"message": "Website loaded successfully"}


@app.post("/ask-llm")
def ask_llm_api(req: QuestionRequest):
    return {"answer": ask_llm(req.question, req.session_id)}

@app.post("/ask-doc-chat")
def ask_doc_api(req: QuestionRequest):
    global session_vector_store, current_session_id

    if not session_vector_store:
        return {"error": "No document uploaded"}

    if req.session_id != current_session_id:
        return {"error": "Session expired. Please upload document again."}

    return {
        "answer": ask_rag(req.question, req.session_id, session_vector_store)
    }

@app.post("/ask-web-chat")
def ask_web_api(req: QuestionRequest):
    global web_vector_store, current_web_session

    if not web_vector_store:
        return {"error": "No website loaded"}

    if req.session_id != current_web_session:
        return {"error": "Session expired. Load website again."}

    answer = ask_rag(req.question, req.session_id, web_vector_store)

    return {"answer": answer}

