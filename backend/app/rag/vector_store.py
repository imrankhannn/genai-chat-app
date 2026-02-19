from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from app.rag.embedding import get_embeddings

def create_vector_store(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = get_embeddings()

    # test = embeddings.embed_documents(["test document"])
    # print("HF TEST EMBEDDING:", test)


    return FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
