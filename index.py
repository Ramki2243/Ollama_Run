import requests

BASE_URL = "https://ollama-run.onrender.com"

def pull_model(model_name="mistral"):
    url = f"{BASE_URL}/api/pull"
    resp = requests.post(url, json={"name": model_name}, stream=True)
    for line in resp.iter_lines():
        if line:
            print(line.decode("utf-8"))

def generate(model_name="mistral", prompt="Hello from Python frontend!"):
    url = f"{BASE_URL}/api/generate"
    payload = {"model": model_name, "prompt": prompt}
    resp = requests.post(url, json=payload, stream=True)
    for line in resp.iter_lines():
        if line:
            print(line.decode("utf-8"))

if __name__ == "__main__":
    model = "mistral"
    print(f"Pulling model: {model}")
    pull_model(model)

    print("\nGenerating response...")
    generate(model, "Explain quantum computing in simple terms.")