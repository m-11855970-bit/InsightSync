import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import traceback  # Penting untuk tengok punca ralat

app = Flask(__name__)
CORS(app)

# Ambil URI
MONGO_URI = os.environ.get('MONGO_URI')

@app.route('/')
def home():
    return "Server InsightMe Aktif!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        print(f"Data diterima: {data}")
        
        # Cuba sambung ke MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client['InsightMe']
        collection = db['scores']
        
        # Cuba simpan data
        result = collection.insert_one(data)
        print(f"Berjaya! ID: {result.inserted_id}")
        
        return jsonify({"status": "success"}), 200

    except Exception as e:
        # Kod di bawah akan paksa Render Logs tunjuk ralat yang 'tersembunyi'
        error_detail = traceback.format_exc()
        print("--- RALAT DIKESAN ---")
        print(error_detail)
        print("---------------------")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
