from fastapi import APIRouter, UploadFile, File
from backend.core.extractor import extract_text_from_pdf, extract_text_with_ocr

router = APIRouter(prefix="/extract", tags=["extract"])

@router.post("/pdf")
async def extract_pdf_text(file: UploadFile = File(...)):
    """
    Extrai texto de PDF usando PyMuPDF (texto nativo)
    """
    if not file.filename.endswith('.pdf'):
        return {"error": "Apenas arquivos PDF são aceitos"}
    
    content = await file.read()
    result = extract_text_from_pdf(content)
    
    return result

@router.post("/pdf-ocr")
async def extract_pdf_ocr(file: UploadFile = File(...)):
    """
    Extrai texto de PDF usando EasyOCR (PDFs escaneados)
    """
    if not file.filename.endswith('.pdf'):
        return {"error": "Apenas arquivos PDF são aceitos"}
    
    content = await file.read()
    result = extract_text_with_ocr(content)
    
    return result
