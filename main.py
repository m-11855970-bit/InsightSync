import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Pastikan MONGO_URI anda di Render adalah link panjang yang bermula dengan mongodb://
uri = os.environ.get('MONGO_URI')

# Sambungan secara manual untuk elak isu DNS srv
try:
    client = MongoClient(uri, connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
    db = client['InsightMe']
    collection = db['scores']
    print("Sistem sambungan sedia (Lazy Loading)")
except Exception as e:
    print(f"Error sambungan awal: {e}")

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    try:
        data = request.json
        if data:
            # Kita cuba masukkan data
            collection.insert_one(data)
            return jsonify({"status": "SUCCESS"}), 200
        return jsonify({"status": "NO DATA"}), 400
    except Exception as e:
        print(f"CRASH SAAT INSERT: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
