import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Ambil URI dan terus buat sambungan
uri = os.environ.get('MONGO_URI')
client = MongoClient(uri)
db = client['InsightMe'] # Nama database ditentukan di sini
collection = db['scores']

@app.route('/')
def home():
    return "Server Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        if data:
            collection.insert_one(data)
            return jsonify({"status": "SUCCESS"}), 200
        return jsonify({"status": "FAILED", "reason": "No data"}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
