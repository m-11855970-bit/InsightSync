import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi

app = Flask(__name__)
CORS(app)

# Ujian Manual: Buka link render anda /test-db dalam browser
@app.route('/test-db')
def test_db():
    try:
        uri = os.environ.get('MONGO_URI')
        client = MongoClient(uri, tlsCAFile=certifi.where())
        client.admin.command('ping')
        return "SAMBUNGAN MONGODB BERJAYA! ✅"
    except Exception as e:
        return f"SAMBUNGAN GAGAL: {str(e)}"

@app.route('/')
def home():
    return "Server Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Data kosong"}), 400
            
        uri = os.environ.get('MONGO_URI')
        client = MongoClient(uri, tlsCAFile=certifi.where())
        db = client['InsightMe']
        db['scores'].insert_one(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"RALAT: {str(e)}") # Ini sepatutnya keluar di log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
