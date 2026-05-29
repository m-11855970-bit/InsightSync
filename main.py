from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import os

app = Flask(__name__)
CORS(app) # Supaya Wix dibenarkan hantar data ke sini

# Sambung ke MongoDB guna link yang anda letak kat Render tadi
client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
db = client.get_database('insight_db')
collection = db.scores

@app.route('/')
def home():
    return "Server InsightSync sedang berjalan!"

@app.route('/hantar-jawapan', methods=['POST'])
def hantar_jawapan():
    data = request.json
    # Simpan data yang diterima dari Wix ke MongoDB
    collection.insert_one(data)
    return jsonify({"status": "berjaya", "mesej": "Data disimpan ke MongoDB!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
