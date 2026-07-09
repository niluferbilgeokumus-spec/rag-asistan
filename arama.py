import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def en_benzer_parcayi_bul(soru):
    soru_vektor = model.encode(soru).tolist()

    conn = sqlite3.connect("dokumanlar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT dosya_adi, icerik, embedding FROM parcalar")
    satirlar = cursor.fetchall()
    conn.close()

    en_iyi_skor = -1
    en_iyi_icerik = None
    en_iyi_dosya = None

    for dosya_adi, icerik, embedding_json in satirlar:
        vektor = json.loads(embedding_json)
        skor = cosine_similarity(soru_vektor, vektor)

        if skor > en_iyi_skor:
            en_iyi_skor = skor
            en_iyi_icerik = icerik
            en_iyi_dosya = dosya_adi

    return en_iyi_dosya, en_iyi_icerik, en_iyi_skor

if __name__ == "__main__":
    soru = "Fourier serisi nedir?"
    dosya, icerik, skor = en_benzer_parcayi_bul(soru)
    print(f"Soru: {soru}")
    print(f"En benzer dosya: {dosya} (benzerlik skoru: {skor:.4f})")
    print(f"İçerik: {icerik}")