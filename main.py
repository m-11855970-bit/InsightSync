import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi # Tambah ini untuk sekuriti tambahan

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get('MONGO_URI')

@app.route('/')
def home():
    return "Server Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        # Guna tlsCAFile untuk pastikan sambungan selamat & stabil
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
        
        db = client.get_database() # Dia akan ambil nama DB dari URI automatik
        collection = db['scores']
        
        collection.insert_one(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"RALAT DATABASE: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
