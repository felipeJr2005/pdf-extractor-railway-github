from fastapi import APIRouter, UploadFile, File
from backend.core.extractor import extract_text_from_pdf

router = APIRouter(prefix="/extract", tags=["extract"])

@router.post("/pdf")
async def extract_pdf_text(file: UploadFile = File(...)):
    """Extrai texto de PDF"""
    if not file.filename.endswith('.pdf'):
        return {"error": "Apenas arquivos PDF são aceitos"}
    
    content = await file.read()
    result = extract_text_from_pdf(content)
    
    return result
