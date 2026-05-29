from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Pastikan MONGO_URI diambil dari Environment Variables Render
MONGO_URI = os.environ.get('MONGO_URI')

try:
    client = MongoClient(MONGO_URI)
    # Kita paksa guna nama database 'InsightMe'
    db = client['InsightMe']
    collection = db['scores']
except Exception as e:
    print(f"MongoDB Connection Error: {e}")

@app.route('/')
def home():
    return "Server InsightMe Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Tiada data"}), 400
        
        # Simpan ke MongoDB
        collection.insert_one(data)
        
        return jsonify({"message": "Berjaya!"}), 200
    except Exception as e:
        # Ini yang akan muncul dekat Render Logs kalau Error 500 berlaku lagi
        print(f"Error simpan data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
