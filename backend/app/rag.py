from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.memory import ConversationBufferWindowMemory
# Will implement this later, its advanvce option to use chat histroy
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


#for pdf as document
def load_pdf_document(pdf_path:str):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    return pages

#For text document
def chunk_documents(document):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(document)
    return chunks


def load_documents():
    docs = [
        Document(page_content="FastAPI is a modern, fast web framework for building APIs with Python."),
        Document(page_content="FastAPI supports async and sync endpoints."),
        Document(page_content="FastAPI is built on Starlette and Pydantic."),
    ]
    return docs

def create_embedding():
    embedding = OllamaEmbeddings(
        model="llama3.2:1b"
    )
    return embedding

def create_vector_store(documents, embeddings):
    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    return vector_store

def add_documents_to_vector_store(vector_store, documents):
    vector_store.add_documents(documents)


llm = OllamaLLM(
    model="llama3.2:1b",
    temperature=0.2
)

# memory
# session_id -> memory
session_memories = {}

def get_session_memory(session_id: str):
    if session_id not in session_memories:
        session_memories[session_id] = ConversationBufferWindowMemory(
            k=3,
            return_messages=True
        )
    return session_memories[session_id]



#useful

# Answer using the context below.
# If context is weak, still try to answer.

prompt = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template="""
You are a helpful assistant.

Rules:
- Use the CONTEXT below as the primary source of truth.
- Use CHAT HISTORY only to resolve references like "it", "this", "they".
- Do NOT require the question to appear in chat history.
- If the answer is not present in the context, say "I don't know".

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Answer:
"""
)



def answer_with_rag(vector_store, question:str, session_id: str):
    # 1️⃣ Retrieve relevant documents
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(question)

    # print("\n--- RETRIEVED DOCUMENTS ---")
    # for i, doc in enumerate(docs):
    #     print(f"\nChunk {i+1}:")
    #     print(doc.page_content[:500])

    # 2️⃣ Convert docs → plain text
    context = "\n".join(doc.page_content for doc in docs)
    memory = get_session_memory(session_id)
    chat_history = memory.load_memory_variables({}).get("history", "")

    # 3️⃣ Build final prompt
    final_prompt = prompt.format(
        context=context,
        chat_history=chat_history,
        question=question
    )

    # print("\n--- FINAL CONTEXT SENT TO LLM ---")
    # print(context)

    # 4️⃣ Call LLM
    answer = llm.invoke(final_prompt)

     # 5️⃣ Save conversation to memory
    memory.save_context(
    {"input": question},
    {"output": answer}
)
    return answer, docs


# def retrive_context(vector_store, question):
#     retriever = vector_store.as_retriever(search_kwargs={"k": 2})
#     docs = retriever.invoke(question)
#     return docs

