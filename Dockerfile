FROM ollama/ollama:latest
ENV OLLAMA_MODELS=/root/.ollama/models
COPY models /root/.ollama/models
EXPOSE 11434