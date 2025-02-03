from fastapi import FastAPI, UploadFile, File
import shutil
import os
from process_pdf import process_pdf, pdf_already_processed
from query_engine import query_database

app = FastAPI()

# Rutas y archivos de datos
DB_PATH = "./data/chroma_db"
UPLOAD_FOLDER = "./data/uploads"
STATIC_PDF = "./data/static_document.pdf"  # PDF estático incluido en el proyecto

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

@app.get("/init/")
def init_content():
    """
    Carga y procesa un PDF estático incluido en el proyecto.
    Llama a este endpoint para inicializar el contenido de forma interna.
    """
    pdf_name = os.path.basename(STATIC_PDF)
    
    # Verificar si el archivo existe
    if not os.path.exists(STATIC_PDF):
        return {"error": "No se encontró el documento estático."}
    
    # Procesar el PDF si aún no fue procesado
    if pdf_already_processed(pdf_name):
        return {"message": f"El documento {pdf_name} ya ha sido procesado."}
    else:
        return {"message": process_pdf(STATIC_PDF, pdf_name)}

@app.get("/query/")
def ask_question(q: str):
    """Consulta la base de conocimiento sin necesidad de volver a subir el PDF."""
    response = query_database(q)
    return {"response": response}

# Configuración para correr en local o en Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
