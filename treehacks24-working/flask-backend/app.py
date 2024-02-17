from flask import Flask, request, jsonify
from flask_cors import CORS
CORS(app)  # This will enable CORS for all routes and origins.
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        # Read the image via file.stream
        img = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(img)
        return jsonify(text=text), 200

if __name__ == '__main__':
    app.run(debug=True)
