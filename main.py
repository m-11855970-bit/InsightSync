from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app) # Memberi kebenaran kepada Wix untuk hantar data

# Ambil URL MongoDB dari Environment Variable Render
MONGO_URI = os.environ.get('MONGO_URI')

client = MongoClient(MONGO_URI)
# Kita guna nama 'InsightMe' ikut gambar database anda
db = client['InsightMe']    
collection = db['scores']

@app.route('/')
def home():
    return "Server InsightMe Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Tiada data"}), 400
        
        # Simpan data 'nama', 'skor', 'date' ke MongoDB
        collection.insert_one(data)
        
        return jsonify({"message": "Berjaya!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
