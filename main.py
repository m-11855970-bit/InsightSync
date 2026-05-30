import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi

app = Flask(__name__)
CORS(app)

# Ambil URI panjang dari Render Environment
MONGO_URI = os.environ.get('MONGO_URI')

@app.route('/')
def home():
    return "Server InsightMe Aktif & Stabil!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    client = None
    try:
        data = request.json
        # Tambah directConnection=True untuk paksa sambungan terus ke shard
        client = MongoClient(
            MONGO_URI, 
            tlsCAFile=certifi.where(), 
            serverSelectionTimeoutMS=5000,
            directConnection=False # Biarkan False untuk cluster, tetapi pastikan URI betul
        )
        
        # Nyatakan nama database secara eksplisit
        db = client['InsightMe']
        collection = db['scores']
        
        # Simpan data
        collection.insert_one(data)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"RALAT DATABASE: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if client:
            client.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
