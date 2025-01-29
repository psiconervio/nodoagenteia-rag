Aquí tienes la estructura final del código para desplegar en Railway:

1️⃣ Estructura del Proyecto
bash
Copiar
Editar
📂 mi_agente_rag
 ├── 📄 main.py  # API con FastAPI
 ├── 📄 process_pdf.py  # Extraer texto del PDF y almacenarlo en ChromaDB
 ├── 📄 query_engine.py  # Buscar información relevante en ChromaDB
 ├── 📄 requirements.txt  # Dependencias del proyecto
 ├── 📄 Procfile  # Archivo para ejecutar la API en Railway
 ├── 📂 data  # Carpeta para la base de datos de ChromaDB (Railway la guarda automáticamente)
2️⃣ Código de los Archivos
📄 main.py (API con FastAPI)
python
Copiar
Editar
from fastapi import FastAPI, UploadFile, File
import shutil
from process_pdf import process_pdf
from query_engine import query_database

app = FastAPI()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Sube un PDF y procesa su contenido en ChromaDB."""
    file_path = f"./data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": process_pdf(file_path)}

@app.get("/query/")
async def ask_question(q: str):
    """Consulta la base de conocimiento con una pregunta."""
    response = query_database(q)
    return {"response": response}
📄 process_pdf.py (Procesar PDFs y Guardar en ChromaDB)
python
Copiar
Editar
import chromadb
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import os

DB_PATH = "./data/chroma_db"
os.makedirs(DB_PATH, exist_ok=True)

# Inicializar ChromaDB
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="documentos")

# Cargar modelo de embeddings
encoder = SentenceTransformer("all-MiniLM-L6-v2")

def process_pdf(pdf_path):
    """Extrae texto del PDF y lo almacena en ChromaDB."""
    reader = PdfReader(pdf_path)
    text_chunks = [page.extract_text() for page in reader.pages if page.extract_text()]

    for i, chunk in enumerate(text_chunks):
        embedding = encoder.encode(chunk).tolist()
        collection.add(ids=[f"doc_{i}"], embeddings=[embedding], metadatas=[{"text": chunk}])

    return f"PDF {pdf_path} procesado y almacenado en ChromaDB."
📄 query_engine.py (Búsqueda de Información en ChromaDB)
python
Copiar
Editar
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
📄 requirements.txt (Dependencias del Proyecto)
Copiar
Editar
fastapi
uvicorn
chromadb
sentence-transformers
pypdf
📄 Procfile (Ejecutar la API en Railway)
less
Copiar
Editar
web: uvicorn main:app --host 0.0.0.0 --port $PORT
3️⃣ Desplegar en Railway
Subir el Código a GitHub

bash
Copiar
Editar
git init
git add .
git commit -m "Primer commit"
git remote add origin https://github.com/tu-usuario/mi_agente_rag.git
git push -u origin main
Conectar Railway con GitHub

Ir a Railway.app
Crear un nuevo proyecto
Conectar tu repositorio
Deploy automático 🚀
4️⃣ Probar la API en Producción
Si Railway te da la URL https://mi-api.railway.app, puedes probar:

Subir un PDF

bash
Copiar
Editar
curl -X POST "https://mi-api.railway.app/upload/" -F "file=@archivo.pdf"
Consultar la base de conocimiento

bash
Copiar
Editar
curl "https://mi-api.railway.app/query/?q=¿Qué dice el PDF?"
✅ API RAG en producción con Railway! 🚀
Siguiente paso: ¿Quieres integrar WhatsApp ahora? 📲