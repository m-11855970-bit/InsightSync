from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Ambil URI dari Environment Variables Render
MONGO_URI = os.environ.get('MONGO_URI')

# Setup MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['InsightMe']
    collection = db['scores']
except Exception as e:
    print(f"DATABASE CONNECTION ERROR: {e}")

@app.route('/')
def home():
    return "Server InsightMe Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        print(f"Data diterima dari Wix: {data}")
        
        if not data:
            return jsonify({"error": "Tiada data diterima"}), 400
        
        # Proses simpan
        result = collection.insert_one(data)
        print(f"Berjaya simpan! ID: {result.inserted_id}")
        
        return jsonify({"message": "SUCCESS"}), 200
        
    except Exception as e:
        print(f"CRASH ERROR: {e}") # Error ini akan muncul di Render Logs
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
