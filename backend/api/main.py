from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "PDF Extractor funcionando!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}