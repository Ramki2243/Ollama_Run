FROM ollama/ollama:latest

# Set environment variable for model storage
ENV OLLAMA_MODELS=/root/.ollama/models

# Pre-pull a small model at build time (phi is ~1.8GB, gemma:2b is ~2.5GB)
RUN ollama pull phi || true

# Expose Ollama API port
EXPOSE 11434