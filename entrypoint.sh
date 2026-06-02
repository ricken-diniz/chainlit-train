#!/bin/bash
set -e

MODEL="${OLLAMA_MODEL:-llava:7b}"

echo "▶ Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait until Ollama is ready
echo "Waiting for Ollama to be ready..."
until curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; do
  sleep 1
done
echo "Ollama is ready."

echo "Pulling model: $MODEL"
ollama pull "$MODEL"

echo "Starting Chainlit app..."
exec chainlit run app.py --host 0.0.0.0 --port 8000
