import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Guna MONGO_URI dari Render Environment
uri = os.environ.get('MONGO_URI')

@app.route('/')
def home():
    return "Server InsightMe Live!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    client = None
    try:
        data = request.json
        print(f"Data diterima: {data}")

        # Kita buka connection HANYA bila perlu
        client = MongoClient(uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
        db = client['InsightMe']
        collection = db['scores']
        
        collection.insert_one(data)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"!!! ERROR SEBENAR: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if client:
            client.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
