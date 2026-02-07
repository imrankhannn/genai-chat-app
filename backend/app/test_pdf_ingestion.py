from rag import (
    load_documents,
    create_embedding,
    create_vector_store,
    chunk_documents,
    add_documents_to_vector_store,
    answer_with_rag,
    load_pdf_document
)

# 1️⃣ Base docs (optional)
base_docs = load_documents()
embeddings = create_embedding()
vector_store = create_vector_store(base_docs, embeddings)

# 2️⃣ Load PDF
pdf_docs = load_pdf_document("Moltbook.pdf")

# 3️⃣ Chunk PDF
pdf_chunks = chunk_documents(pdf_docs)

# 4️⃣ Add to FAISS
add_documents_to_vector_store(vector_store, pdf_chunks)

# 5️⃣ Ask question from PDF
question = "what is Moltbook?"
answer, sources = answer_with_rag(vector_store, question)

print("\nQUESTION:\n", question)
print("\nANSWER:\n", answer)
# print("\nSOURCES:")
# for s in sources:
    # print("-", s.metadata)


