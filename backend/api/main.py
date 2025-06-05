from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.extract import router as extract_router

app = FastAPI(
    title="PDF Text Extractor - 8GB Railway",
    description="API para extração de texto de PDFs usando PyMuPDF e EasyOCR - Otimizado para 8GB RAM",
    version="2.0.0"
)

# CORS configurado para GitHub Pages + desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://felipeJr2005.github.io",
        "http://localhost:8080",
        "http://localhost:3000", 
        "http://127.0.0.1:8080",
        "*"  # Permitir todos para teste - remover em produção
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir rotas de extração
app.include_router(extract_router)

@app.get("/")
def root():
    return {
        "message": "PDF Extractor funcionando com 8GB RAM!", 
        "status": "ok",
        "memory": "8GB available",
        "cpu": "8 vCPU available"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "specs": {
            "memory": "8GB",
            "cpu": "8 vCPU",
            "optimized": True
        }
    }
