# Stage 1: Base con dependencias de sistema
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalamos dependencias de compilación solo en el builder
FROM base AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Imagen Final (Producción)
FROM base
# Copiamos el entorno virtual del builder
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copiamos el código fuente
COPY . .

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Ejecutamos con Uvicorn. 
# Importante: El path es app.main:app porque tu archivo está en app/main.py
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
