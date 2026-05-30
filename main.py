import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi

app = Flask(__name__)
CORS(app)

# Ambil URI dari Render
MONGO_URI = os.environ.get('MONGO_URI')

@app.route('/')
def home():
    return "Server InsightMe Aktif!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    client = None
    try:
        data = request.json
        # Guna timeout 15 saat untuk beri ruang pada rangkaian Render
        client = MongoClient(
            MONGO_URI, 
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=15000,
            tlsAllowInvalidCertificates=True # Tambahan untuk bypass isu SSL Render
        )
        
        # Paksa pilih database 'InsightMe' secara manual
        db = client['InsightMe']
        collection = db['scores']
        
        # Simpan data
        collection.insert_one(data)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        # Ini akan keluar di log Render anda
        print(f"DEBUG_UTAMA: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if client:
            client.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
