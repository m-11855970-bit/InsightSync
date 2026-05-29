import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import sys # Tambah ni

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get('MONGO_URI')

# Guna block try-except di luar terus
try:
    print("Cuba menyambung ke MongoDB...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test connection terus
    client.admin.command('ping')
    db = client['InsightMe']
    collection = db['scores']
    print("Berjaya sambung ke MongoDB!")
except Exception as e:
    print(f"RALAT KRITIKAL MONGODB: {e}")
    # Ini akan paksa Render Logs tunjuk apa yang tak kena
