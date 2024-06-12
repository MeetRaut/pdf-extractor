from flask import Flask, render_template, request, redirect, url_for
import os
from PyPDF2 import PdfReader

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return redirect(url_for('display_pdf', filename=file.filename))
    return redirect(request.url)

@app.route('/display/<filename>')
def display_pdf(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pdf_text = extract_text_from_pdf(filepath)
    return render_template('display.html', filename=filename, pdf_text=pdf_text)

def extract_text_from_pdf(filepath):
    with open(filepath, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)