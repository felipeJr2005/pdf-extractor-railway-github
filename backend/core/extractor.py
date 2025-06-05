import fitz  # PyMuPDF
import easyocr
from PIL import Image
import io
from typing import Dict, List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_bytes: bytes) -> Dict:
    """
    Extrai texto de PDF usando PyMuPDF (texto nativo)
    
    Args:
        pdf_bytes: Bytes do arquivo PDF
        
    Returns:
        Dict com resultado da extração
    """
    try:
        logger.info("Iniciando extração de texto com PyMuPDF")
        
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
            "method": "PyMuPDF",
            "pages": len(text_content),
            "content": text_content
        }
        
    except Exception as e:
        logger.error(f"Erro na extração PyMuPDF: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def extract_text_with_ocr(pdf_bytes: bytes) -> Dict:
    """
    Extrai texto de PDF escaneado usando EasyOCR
    
    Args:
        pdf_bytes: Bytes do arquivo PDF
        
    Returns:
        Dict com resultado da extração
    """
    try:
        logger.info("Iniciando extração de texto com EasyOCR")
        
        # Inicializar EasyOCR - CPU mode para Railway
        reader = easyocr.Reader(['pt', 'en'], gpu=False)
        
        # Abrir PDF dos bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text_content = []
        
        # Processar cada página
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Converter página para imagem com alta resolução
            mat = fitz.Matrix(2, 2)  # Zoom 2x para melhor qualidade OCR
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Converter para PIL Image
            image = Image.open(io.BytesIO(img_data))
            
            # Extrair texto com EasyOCR
            results = reader.readtext(image, detail=0, paragraph=True)
            
            # Combinar todo o texto da página
            page_text = ' '.join(results) if results else ""
            
            if page_text.strip():  # Se encontrou texto
                text_content.append({
                    "page": page_num + 1,
                    "text": page_text.strip()
                })
        
        pdf_document.close()
        
        return {
            "success": True,
            "method": "EasyOCR",
            "pages": len(text_content),
            "content": text_content
        }
        
    except Exception as e:
        logger.error(f"Erro na extração EasyOCR: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
