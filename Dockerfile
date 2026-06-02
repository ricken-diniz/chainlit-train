# ─── Build args ───────────────────────────────────────────────────────────────
ARG OLLAMA_MODEL=llava:7b

# ─── Base image ───────────────────────────────────────────────────────────────
FROM python:3.11-slim

ARG OLLAMA_MODEL
ENV OLLAMA_MODEL=${OLLAMA_MODEL}

# ─── System deps ──────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ─── Install Ollama ───────────────────────────────────────────────────────────
RUN curl -fsSL https://ollama.com/install.sh | sh

# ─── Python deps ──────────────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ─── App source ───────────────────────────────────────────────────────────────
COPY app.py ./

# ─── Entrypoint: start Ollama, pull model, then run chainlit ──────────────────
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
