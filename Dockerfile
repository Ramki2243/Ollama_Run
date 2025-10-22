FROM ollama/ollama:latest

# Expose Ollama's default port
EXPOSE 11434

# Start Ollama server
CMD ["ollama", "serve"]