from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)
BASE_URL = "https://ollama-run.onrender.com"  # your Render Ollama URL

# HTML template with dark theme
HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Ollama Chat</title>
  <style>
    body {
      background-color: #121212;
      color: #e0e0e0;
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px;
    }
    #chatbox {
      width: 80%;
      height: 400px;
      background: #1e1e1e;
      border: 1px solid #333;
      padding: 10px;
      overflow-y: auto;
      margin-bottom: 10px;
      border-radius: 6px;
    }
    #controls {
      display: flex;
      width: 80%;
      gap: 10px;
    }
    textarea {
      flex: 1;
      background: #1e1e1e;
      color: #e0e0e0;
      border: 1px solid #333;
      border-radius: 6px;
      padding: 8px;
    }
    select, button {
      background: #333;
      color: #e0e0e0;
      border: none;
      padding: 8px 12px;
      border-radius: 6px;
      cursor: pointer;
    }
    button:hover {
      background: #444;
    }
  </style>
</head>
<body>
  <h1>Ollama Chat</h1>
  <div id="chatbox"></div>
  <div id="controls">
    <select id="model"></select>
    <textarea id="prompt" rows="2"></textarea>
    <button onclick="sendPrompt()">Send</button>
  </div>

  <script>
    async function loadModels() {
      const res = await fetch("/models");
      const models = await res.json();
      const dropdown = document.getElementById("model");
      models.forEach(m => {
        let opt = document.createElement("option");
        opt.value = m;
        opt.textContent = m;
        dropdown.appendChild(opt);
      });
    }

    async function sendPrompt() {
      const model = document.getElementById("model").value;
      const prompt = document.getElementById("prompt").value;
      const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({model, prompt})
      });
      const data = await res.json();
      const chatbox = document.getElementById("chatbox");
      chatbox.innerHTML += "<b>You:</b> " + prompt + "<br>";
      chatbox.innerHTML += "<b>Ollama:</b> " + data.response + "<br><br>";
      chatbox.scrollTop = chatbox.scrollHeight;
      document.getElementById("prompt").value = "";
    }

    loadModels();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/models")
def get_models():
    r = requests.get(f"{BASE_URL}/api/tags")
    tags = [m["name"] for m in r.json()["models"]]
    return jsonify(tags)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    model = data["model"]
    prompt = data["prompt"]

    # Ensure model is pulled
    requests.post(f"{BASE_URL}/api/pull", json={"name": model})

    # Generate response
    r = requests.post(f"{BASE_URL}/api/generate", json={"model": model, "prompt": prompt})
    return jsonify({"response": r.text})

if __name__ == "__main__":
    app.run(debug=True, port=5000)