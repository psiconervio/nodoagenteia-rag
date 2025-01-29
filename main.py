from fastapi import FastAPI, UploadFile, File
import shutil
import os
from process_pdf import process_pdf, pdf_already_processed
from query_engine import query_database

app = FastAPI()
DB_PATH = "./data/chroma_db"
UPLOAD_FOLDER = "./data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Sube un PDF y lo almacena en ChromaDB solo si no ha sido procesado."""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Guardar el PDF en el servidor
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Si el PDF ya fue procesado, no volver a hacerlo
    if pdf_already_processed(file.filename):
        return {"message": f"El PDF {file.filename} ya estaba procesado."}

    # Procesar el PDF y almacenarlo en ChromaDB
    return {"message": process_pdf(file_path, file.filename)}

@app.get("/query/")
async def ask_question(q: str):
    """Consulta la base de conocimiento sin necesidad de volver a subir el PDF."""
    response = query_database(q)
    return {"response": response}
