import easyocr
import fitz
from PIL import Image
import io

def extract_text_with_ocr(pdf_bytes: bytes) -> Dict:
    """Extrai texto de PDF escaneado usando EasyOCR"""
    try:
        reader = easyocr.Reader(['pt', 'en'])  # Português e Inglês
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text_content = []
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Converter página para imagem
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom
            img_data = pix.tobytes("png")
            
            # EasyOCR
            results = reader.readtext(img_data)
            
            # Extrair texto
            page_text = ' '.join([result[1] for result in results])
            
            if page_text.strip():
                text_content.append({
                    "page": page_num + 1,
                    "text": page_text.strip()
                })
        
        pdf_document.close()
        
        return {
            "success": True,
            "method": "OCR",
            "pages": len(text_content),
            "content": text_content
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
