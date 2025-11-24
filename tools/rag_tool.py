from memory.vector_store import VectorMemory
import uuid

def ingest_knowledge(text: str, source: str = "user_input"):
    """
    Adds text to the RAG vector store.
    """
    mem = VectorMemory()
    doc_id = f"doc_{str(uuid.uuid4())[:8]}"
    mem.add_document(doc_id, text, {"source": source})
    return f"Stored document {doc_id}."

def retrieve_context(query: str):
    """
    Retrieves relevant context from the RAG store.
    """
    mem = VectorMemory()
    results = mem.search(query, n_results=2)
    if not results:
        return "No relevant memory found."
    return "\n".join(results)