# ============================================================
# Stage 1: Builder — dependencias de compilación y venv
# ============================================================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt

# ============================================================
# Stage 2: Producción
# ============================================================
FROM python:3.12-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

ARG ENV=production
ENV ENV=${ENV}

WORKDIR /app

# Dependencias runtime mínimas (libpq para psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Venv desde builder
COPY --from=builder /venv /venv

# App
COPY . .

# Usuario no-root
RUN groupadd -r taca && useradd -r -g taca -d /app -s /sbin/nologin taca \
    && chown -R taca:taca /app
USER taca

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import http.client; http.client.HTTPConnection('localhost', 8000).request('GET', '/');"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
