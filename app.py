from flask import Flask, request, jsonify, json
from PIL import Image
import io
import os
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/receipt-scan', methods=['POST'])
def scan_receipt():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    try:
        genai.configure(api_key=os.getenv('API_KEY'))
       

        model = genai.GenerativeModel('gemini-1.5-flash')

        img = Image.open(file.stream)

        response = model.generate_content(["Give me the address of the store/restaurant, the name of the store/restaurant, and the list of items and their respective prices in the form of json. For each item, let it be in the form of name: name of item, price: price of item.", img], stream=True)
        response.resolve()
        
        cleaned_text = response.text.strip('```json\n').strip('```').strip()
        cleaned_text = cleaned_text.replace('\n', '')

        return jsonify({"result": json.loads(cleaned_text) })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


