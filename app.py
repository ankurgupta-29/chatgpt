# app.py
from flask import Flask, render_template, request
import pdfplumber
import requests

app = Flask(__name__)

# Configure Rasa server URL
rasa_server_url = 'http://localhost:5005/webhooks/rest/webhook'

@app.route('/')
def index():
    return render_template('index.html')

# this is a change\

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)
        
        # Send text to Rasa server
        chat_response = send_to_rasa(text)
        
        return render_template('result.html', chat_response=chat_response)

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def send_to_rasa(text):
    payload = {
        'sender': 'user',
        'message': text
    }
    response = requests.post(rasa_server_url, json=payload)
    if response.status_code == 200:
        data = response.json()
        # Assuming Rasa returns a list of responses, concatenate them into a single string
        return ' '.join([msg['text'] for msg in data])
    else:
        return 'Error: Unable to connect to Rasa server'

if __name__ == '__main__':
    app.run(debug=True)
