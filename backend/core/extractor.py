import fitz  # PyMuPDF
import easyocr
from PIL import Image
import PIL
import io
import numpy as np
from typing import Dict, List, Optional
import logging

# FIX para Pillow 10+ compatibilidade com EasyOCR
# Solução oficial do GitHub Issue #1077
PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

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
        
        logger.info(f"PyMuPDF extraiu texto de {len(text_content)} página(s)")
        
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
    Extrai texto de PDF escaneado usando EasyOCR - OTIMIZADO PARA 8GB RAILWAY
    
    Args:
        pdf_bytes: Bytes do arquivo PDF
        
    Returns:
        Dict com resultado da extração
    """
    try:
        logger.info("Iniciando extração de texto com EasyOCR - 8GB Mode")
        
        # CONFIGURAÇÃO OTIMIZADA PARA 8GB RAM + 8 vCPU
        # Com 8GB podemos usar configurações mais robustas
        reader = easyocr.Reader(
            ['pt'],  # Português
            gpu=False,  # CPU mode (Railway não tem GPU)
            detector=True, 
            recognizer=True, 
            verbose=False,
            quantize=True,  # Otimização de modelo
            download_enabled=True
        )
        
        logger.info("EasyOCR Reader inicializado com configurações 8GB")
        
        # Abrir PDF dos bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        text_content = []
        
        # Processar cada página
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Com 8GB podemos usar resolução ALTA para melhor qualidade
            # Matrix 2.5 para máxima qualidade (possível com 8GB)
            mat = fitz.Matrix(2.5, 2.5)  # Resolução alta para melhor OCR
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            logger.info(f"Processando página {page_num + 1} com resolução 2.5x")
            
            # Converter para numpy array (formato que EasyOCR prefere)
            image = Image.open(io.BytesIO(img_data))
            img_array = np.array(image)
            
            # EasyOCR com configurações ROBUSTAS para 8GB
            # Aproveitando toda a capacidade de processamento
            results = reader.readtext(
                img_array, 
                detail=0, 
                paragraph=True,
                width_ths=0.9,  # Alta precisão (possível com 8GB)
                height_ths=0.9, # Alta precisão
                batch_size=2,   # Maior batch com 8GB
                workers=4       # Usar mais workers com 8 vCPU
            )
            
            # Combinar todo o texto da página
            if results:
                if isinstance(results, list):
                    page_text = ' '.join(str(result) for result in results)
                else:
                    page_text = str(results)
                
                if page_text.strip():  # Se encontrou texto
                    text_content.append({
                        "page": page_num + 1,
                        "text": page_text.strip()
                    })
                    logger.info(f"Página {page_num + 1}: {len(page_text)} caracteres extraídos")
        
        pdf_document.close()
        
        logger.info(f"EasyOCR extraiu texto de {len(text_content)} página(s) - Modo 8GB")
        
        return {
            "success": True,
            "method": "EasyOCR-8GB",
            "pages": len(text_content),
            "content": text_content,
            "specs": {
                "resolution": "2.5x",
                "batch_size": 2,
                "workers": 4,
                "memory_mode": "8GB"
            }
        }
        
    except Exception as e:
        logger.error(f"Erro na extração EasyOCR: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "specs": {
                "memory_mode": "8GB",
                "failed_stage": "OCR processing"
            }
        }
