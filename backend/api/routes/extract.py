from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.core.extractor import extract_text_from_pdf, extract_text_with_ocr

router = APIRouter(prefix="/extract", tags=["extract"])

@router.post("/pdf")
async def extract_pdf_text(file: UploadFile = File(...)):
    """
    Extrai texto de PDF usando PyMuPDF (texto nativo)
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
    
    try:
        content = await file.read()
        result = extract_text_from_pdf(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

@router.post("/pdf-ocr")
async def extract_pdf_ocr(file: UploadFile = File(...)):
    """
    Extrai texto de PDF usando EasyOCR (PDFs escaneados)
    """
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
    
    try:
        content = await file.read()
        result = extract_text_with_ocr(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")
