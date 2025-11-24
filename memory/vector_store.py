import chromadb
from chromadb.utils import embedding_functions
import os

class VectorMemory:
    def __init__(self, db_path="./memory_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        # Using a simple local embedding function
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(name="blog_knowledge", embedding_function=self.ef)

    def add_document(self, doc_id, text, metadata=None):
        if metadata is None:
            metadata = {}
        self.collection.upsert(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def search(self, query, n_results=2):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        if results['documents']:
            return results['documents'][0]
        return []