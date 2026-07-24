# Arama Modulu
# Kullanicinin sorusunu embedding'e cevirir, veritabanindaki tum dokuman
# parcalariyla karsilastirir ve en alakali olanlari (top-k) dondurur.

import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Metinleri sayisal vektorlere (embedding) ceviren model.
model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(v1, v2):
    """Iki vektor arasindaki anlamsal benzerligi (-1 ile 1 arasi) hesaplar."""
    v1 = np.array(v1)
    v2 = np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def get_top_chunks(soru, k=3):
    """Veritabanindaki tum parcalar arasindan soruyla en alakali k tanesini bulur."""
    soru_vektor = model.encode(soru).tolist()

    conn = sqlite3.connect("dokumanlar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT dosya_adi, icerik, embedding FROM parcalar")
    satirlar = cursor.fetchall()
    conn.close()

    sonuclar = []
    for dosya_adi, icerik, embedding_json in satirlar:
        vektor = json.loads(embedding_json)
        skor = cosine_similarity(soru_vektor, vektor)
        sonuclar.append((skor, dosya_adi, icerik))

    # En yuksek benzerlik skoruna sahip olanlar basa gelecek sekilde sirala.
    sonuclar.sort(key=lambda x: x[0], reverse=True)
    return sonuclar[:k]


if __name__ == "__main__":
    # Bu dosya tek basina calistirilirsa, ornek bir arama testi yapar.
    soru = "Fourier serisi nedir?"
    top_chunks = get_top_chunks(soru, k=3)
    print(f"Soru: {soru}\n")
    for skor, dosya, icerik in top_chunks:
        print(f"[{dosya} - benzerlik: {skor:.4f}]")
        print(icerik)
        print("---")