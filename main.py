import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi

app = Flask(__name__)
CORS(app)

MONGO_URI = os.environ.get('MONGO_URI')

# Fungsi untuk tentukan teks penerangan (diambil dari kod asal anda)
def dapatkan_penerangan(jenis):
    penerangan = {
        "ISTJ": "This character is like a kid who likes to make a study schedule, follow rules, and make sure all homework is done on time. Likes real things, not just talk.",
        "ISFJ": "This character is very kind, likes to take care of their friends, and makes sure everyone is comfortable and not fighting. Likes doing things right and neatly.",
        "INFJ": "This character likes to think quietly, has many great ideas in their head, and wants to help others become better. It's like they have a special power to know what others feel.",
        "INTJ": "This character is like a genius kid who likes to think of the smartest ways to solve difficult problems. Likes to make big plans for the future.",
        "ISTP": "This character is like a kid who likes playing with LEGOs, fixing bikes, and figuring out how things work. Likes to do things when needed, doesn't talk much.",
        "ISFP": "This character is like a kid who likes to draw or play music, likes beautiful things, and is very kind. Likes to live in the moment and do what they enjoy.",
        "INFP": "This character is like a kid who likes reading fantasy stories, believes in the good in everyone, and is very creative. Has special values deep in their heart.",
        "INTP": "This character is like a kid who always asks why?, likes to think about strange and great ideas. Is good at using their logical brain to understand the world.",
        "ESTP": "This character is like the most fun kid in a race or a game, acts fast, and is good at solving problems when things go wrong. Likes exciting stuff!",
        "ESFP": "This character is like the kid who loves telling jokes, likes being the center of attention, and is good at making everyone happy. Likes to play and have fun.",
        "ENFP": "This character is like a kid who likes sharing fun new ideas, is good at making friends feel excited, and likes trying new things.",
        "ENTP": "This character is like a kid who likes to debate (in a good way!), likes sharing wild new ideas, and is good at finding different ways to do things.",
        "ESTJ": "This character is like a kid who likes to be the class leader, likes making rules, and makes sure everyone follows instructions. Is good at getting things done right and fast.",
        "ESFJ": "This character is like a kid who likes organizing parties or events, is good at caring for friends' feelings, and makes sure everyone gets along.",
        "ENFJ": "This character is like a kid who is good at speaking in front of people, can make others feel confident, and likes helping everyone become better.",
        "ENTJ": "This character is like a kid who can make big plans for the future, is good at telling people what to do to reach goals, and isn't afraid to make tough decisions."
    }
    return penerangan.get(jenis, "Penerangan tidak ditemui.")

@app.route('/proses-kuiz', methods=['POST'])
def proses_kuiz():
    try:
        data = request.json
        nama = data.get('nama')
        jawapan_user = data.get('jawapan') # Wix hantar senarai ["A", "B", "A"...]

        # Logik skor dari main.py.py anda
        skor = {'E':0, 'I':0, 'S':0, 'N':0, 'T':0, 'F':0, 'J':0, 'P':0}
        
        # Pemetaan soalan ke dimensi (S1-S35)
        map_dimensi = ['E/I', 'S/N', 'S/N', 'T/F', 'T/F', 'J/P', 'J/P', 'E/I', 'S/N', 'S/N',
                       'T/F', 'T/F', 'J/P', 'J/P', 'E/I', 'S/N', 'S/N', 'T/F', 'T/F', 'J/P',
                       'J/P', 'E/I', 'S/N', 'S/N', 'T/F', 'T/F', 'J/P', 'J/P', 'E/I', 'S/N',
                       'S/N', 'T/F', 'T/F', 'J/P', 'J/P']

        for i, jawapan in enumerate(jawapan_user):
            dimensi = map_dimensi[i].split('/')
            if jawapan.upper() == "A":
                skor[dimensi[0]] += 1
            else:
                skor[dimensi[1]] += 1

        # Tentukan jenis
        jenis = ("E" if skor['E'] > skor['I'] else "I") + \
                ("S" if skor['S'] > skor['N'] else "N") + \
                ("T" if skor['T'] > skor['F'] else "F") + \
                ("J" if skor['J'] > skor['P'] else "P")

        info = dapatkan_penerangan(jenis)

        # Simpan ke MongoDB
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        db = client['InsightMe']
        db['scores'].insert_one({
            "nama": nama,
            "jenis": jenis,
            "skor": skor
        })

        return jsonify({"jenis": jenis, "penerangan": info}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
