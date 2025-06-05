# Use Python slim para base menor
FROM python:3.10-slim-bullseye

# Instalar dependências do sistema PRIMEIRO (raramente mudam)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Definir diretório de trabalho
WORKDIR /app

# CRÍTICO: Copiar requirements.txt PRIMEIRO (para cache de dependências)
COPY requirements.txt .

# Cache mount para pip - OTIMIZAÇÃO RAILWAY
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Pré-baixar modelos EasyOCR (cache entre deploys)
# Isso evita download a cada deploy
RUN python -c "import easyocr; print('Baixando modelos...'); reader = easyocr.Reader(['pt'], gpu=False, download_enabled=True); print('Modelos baixados e em cache!')"

# Copiar código da aplicação POR ÚLTIMO (muda frequentemente)
COPY . .

# Expor porta
EXPOSE 8080

# Comando de inicialização
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
