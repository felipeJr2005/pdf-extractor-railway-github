from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.extract import router as extract_router

app = FastAPI(
    title="PDF Text Extractor",
    description="API para extração de texto de PDFs usando PyMuPDF e EasyOCR",
    version="1.0.0"
)

# Configurar CORS para permitir GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://felipeJr2005.github.io",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "*"  # Para desenvolvimento - remover em produção
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Incluir rotas de extração
app.include_router(extract_router)

@app.get("/")
def root():
    return {"message": "PDF Extractor funcionando!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}
