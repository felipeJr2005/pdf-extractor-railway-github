@router.post("/pdf-ocr")
async def extract_pdf_ocr(file: UploadFile = File(...)):
    """Extrai texto de PDF usando OCR"""
    if not file.filename.endswith('.pdf'):
        return {"error": "Apenas arquivos PDF são aceitos"}
    
    content = await file.read()
    result = extract_text_with_ocr(content)
    
    return result
