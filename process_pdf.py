import chromadb
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import os

DB_PATH = "./data/chroma_db"
PROCESSED_PDFS = "./data/processed_pdfs.txt"
os.makedirs(DB_PATH, exist_ok=True)

# Inicializar ChromaDB
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="documentos")
encoder = SentenceTransformer("all-MiniLM-L6-v2")

def pdf_already_processed(pdf_name):
    """Verifica si un PDF ya ha sido procesado antes."""
    if os.path.exists(PROCESSED_PDFS):
        with open(PROCESSED_PDFS, "r") as f:
            processed = f.read().splitlines()
        return pdf_name in processed
    return False

def process_pdf(pdf_path, pdf_name):
    """Extrae texto del PDF y lo almacena en ChromaDB si no ha sido procesado antes."""
    if pdf_already_processed(pdf_name):
        return f"El PDF {pdf_name} ya ha sido procesado."
    
    reader = PdfReader(pdf_path)
    text_chunks = [page.extract_text() for page in reader.pages if page.extract_text()]

    for i, chunk in enumerate(text_chunks):
        embedding = encoder.encode(chunk).tolist()
        collection.add(
            ids=[f"{pdf_name}_doc_{i}"],
            embeddings=[embedding],
            metadatas=[{"text": chunk, "source": pdf_name}]
        )
    
    # Registrar el PDF como procesado
    with open(PROCESSED_PDFS, "a") as f:
        f.write(pdf_name + "\n")
    
    return f"PDF {pdf_name} procesado y almacenado en ChromaDB."
