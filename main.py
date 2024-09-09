# main.py
from flask import Flask, request, jsonify
from PIL import Image
import io
import json

import google.generativeai as genai

import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Path to your service account key file
cred = credentials.Certificate('./splitwise-30217-firebase-adminsdk-qv9kh-477959a13a.json')

# Initialize the Firebase app
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/receipt-scan', methods=['POST'])
def scan_receipt():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    try:
        genai.configure(api_key='AIzaSyBDY6NKnOugfvx_ZJvyoyMlQra0RUkwAtQ')

        model = genai.GenerativeModel('gemini-1.5-flash')

        img = Image.open(file.stream)

        response = model.generate_content(["Give me the address of the store/restaurant, the name of the store/restaurant, and the list of items and their respective prices in the form of json", img], stream=True)
        response.resolve()

        cleaned_text = response.text.strip('```json\n').strip('```').strip()
        cleaned_text = cleaned_text.replace('\n', '')

        return jsonify({"result": json.loads(cleaned_text) })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/post-receipt-split', methods=['POST'])
def post_receipt_split():
    try:
        # Get data from the POST request
        data = request.json

        # Validate the data (you can add your own validation here)
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Reference to the Firestore collection
        doc_ref = db.collection('test').document()

        # Push data to Firestore
        doc_ref.set(data)

        return jsonify({"success": True, "message": "Data added successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500