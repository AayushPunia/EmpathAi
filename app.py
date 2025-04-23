from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# Add CORS to allow requests from other domains
CORS(app)  # This will enable CORS for all routes

# Use environment variable for safety
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Loaded from .env file

@app.route("/")
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route("/hack", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {"role": "system", "content": "You are EmpathAI, an empathetic AI companion."},
                {"role": "user", "content": user_message}
            ],
            "model": "llama3-8b-8192"
        }

        # Debugging: Print payload and headers
        print("Payload:", payload)
        print("Headers:", headers)

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP errors
        response_data = response.json()

        reply = response_data["choices"][0]["message"]["content"].strip()
        return jsonify({"response": reply})
    except requests.exceptions.RequestException as e:
        return jsonify({"response": f"API Error: {str(e)}"}), 500

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))  # Render provides this
    app.run(host="0.0.0.0", port=port)
