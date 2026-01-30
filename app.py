from flask import Flask, request, jsonify
from ollama import Client
import pandas as pd
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)
client = Client()

# ---------- HOME ----------
@app.route('/')
def home():
    return """
    <h1>AI Data Science Assistant</h1>
    <p>Use these endpoints:</p>
    <ul>
        <li>/chat - POST JSON {"message": "your question"}</li>
        <li>/analyze_csv - POST CSV file</li>
        <li>/analyze_image - POST image file</li>
    </ul>
    """

# ---------- TEXT CHAT ----------
@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json['message']
    response = client.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': msg}]
    )
    reply = response['message']['content']
    return jsonify({'response': reply})

# ---------- IMAGE ANALYSIS ----------
@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file received"}), 400

    file = request.files['image']
    img = Image.open(file.stream)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    response = client.chat(
        model='bakllava',
        messages=[{
            'role': 'user',
            'content': 'Analyze this image.',
            'images': [img_base64]
        }]
    )

    caption = response['message']['content']
    return jsonify({'caption': caption})


# ---------- CSV ANALYSIS ----------
@app.route("/analyze_csv", methods=["POST"])
def analyze_csv():
    file = request.files["csv"]
    df = pd.read_csv(file)
    summary = df.describe(include="all").to_dict()
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
