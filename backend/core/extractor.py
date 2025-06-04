import fitz  # PyMuPDF
from typing import Optional

def extract_text_from_pdf(pdf_bytes: bytes) -> dict:
    """Extrai texto de PDF usando PyMuPDF"""
    try:
        # Abrir PDF dos bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text_content = []
        
        # Extrair texto de cada página
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text = page.get_text()
            
            if text.strip():  # Se tem texto
                text_content.append({
                    "page": page_num + 1,
                    "text": text.strip()
                })
        
        pdf_document.close()
        
        return {
            "success": True,
            "pages": len(text_content),
            "content": text_content
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
