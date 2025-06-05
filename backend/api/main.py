from fastapi import FastAPI
from backend.api.routes.extract import router as extract_router

app = FastAPI(
    title="PDF Text Extractor",
    description="API para extração de texto de PDFs usando PyMuPDF e EasyOCR",
    version="1.0.0"
)

# Incluir rotas de extração
app.include_router(extract_router)

@app.get("/")
def root():
    return {"message": "PDF Extractor funcionando!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}
