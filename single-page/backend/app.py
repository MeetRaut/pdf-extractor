from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
import io

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my application! This is Backend"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    if file:
        # Read the PDF content
        pdfReader = PdfReader(file)
        num_pages = len(pdfReader.pages)
        content = ""
        for page in range(num_pages):
            content += pdfReader.pages[page].extract_text()
        return jsonify(content=content)
    return jsonify(error="File upload failed"), 500

if __name__ == '__main__':
    app.run(debug=True)