from sentence_transformers import SentenceTransformer
import chromadb

DB_PATH = "./data/chroma_db"
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="documentos")

encoder = SentenceTransformer("all-MiniLM-L6-v2")

def query_database(query):
    """Consulta ChromaDB y devuelve los fragmentos más relevantes."""
    query_embedding = encoder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    if results["ids"]:
        relevant_docs = [doc["text"] for doc in results["metadatas"][0]]
        return " ".join(relevant_docs)
    return "No encontré información relevante."
