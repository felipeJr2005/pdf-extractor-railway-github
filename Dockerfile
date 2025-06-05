FROM python:3.10-slim

# Instalar dependências básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY . /app

# Instalar dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pré-carregar modelos do EasyOCR (Português)
RUN python -c "import easyocr; easyocr.Reader(['pt'], gpu=False)"

# Expor porta
EXPOSE 8080

# Comando padrão
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
