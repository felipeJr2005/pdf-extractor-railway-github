FROM python:3.10-slim-bullseye

# Instalar dependências do sistema para EasyOCR
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copiar requirements primeiro para cache de layers
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar resto do código
COPY . ./

# Comando será definido pelo Railway via railway.toml
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
