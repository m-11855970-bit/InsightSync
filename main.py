import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Ambil URI dari Environment Variables Render
MONGO_URI = os.environ.get('MONGO_URI')

@app.route('/')
def home():
    return "Server InsightMe sedia menerima data!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        # 1. Terima data dari Wix
        data = request.json
        print(f"Data diterima: {data}")
        
        if not data:
            return jsonify({"status": "error", "message": "Tiada data diterima"}), 400
        
        # 2. Sambung ke MongoDB secara 'on-the-fly'
        client = MongoClient(MONGO_URI, connectTimeoutMS=5000)
        db = client['InsightMe']
        collection = db['scores']
        
        # 3. Simpan data
        result = collection.insert_one(data)
        print(f"Berjaya simpan dengan ID: {result.inserted_id}")
        
        return jsonify({"status": "success", "id": str(result.inserted_id)}), 200

    except Exception as e:
        # Ini akan memaparkan error sebenar di Render Logs jika berlaku Error 500
        print(f"RALAT PROSES: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
