# Etapa 1: Imagem base
FROM python:3.10-slim

# Etapa 2: Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    poppler-utils \
    tesseract-ocr \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Etapa 3: Criar diretório de trabalho
WORKDIR /app

# Etapa 4: Copiar arquivos do projeto
COPY . /app

# Etapa 5: Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Etapa 6: Baixar modelos do EasyOCR durante o build
ENV HOME=/app
RUN python3 -c "import easyocr; easyocr.Reader(['pt'], gpu=False)"

# Etapa 7: Expor a porta usada pelo Uvicorn
EXPOSE 8080

# Etapa 8: Comando para rodar a API
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
