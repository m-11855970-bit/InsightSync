import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Ambil MONGO_URI dari Render
MONGO_URI = os.environ.get('MONGO_URI')

@app.route('/')
def home():
    return "Server Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        print(f"Data diterima: {data}")

        # Gunakan setting 'retrywrites=false' jika DNS masih bermasalah
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        db = client['InsightMe']
        collection = db['scores']
        
        collection.insert_one(data)
        client.close() # Tutup connection selepas guna
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"RALAT TERAKHIR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
