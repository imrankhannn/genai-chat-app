from rag import (
    load_documents,
    create_embedding,
    create_vector_store,
    answer_with_rag
)

docs = load_documents()
embeddings = create_embedding()
vector_store = create_vector_store(docs, embeddings)

question = "what is FastAPI, expalin in 50 words?"
answer, sources = answer_with_rag(vector_store, question)

print("\nANSWER:\n", answer)
print("\nSOURCES:")
for s in sources:
    print("-", s.page_content)
