import sqlite3
from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

def veritabani_olustur():
    conn = sqlite3.connect("dokumanlar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parcalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dosya_adi TEXT,
            icerik TEXT,
            embedding TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Veritabani ve tablo olusturuldu.")

def dokuman_ekle(dosya_adi, icerik):
    vektor = model.encode(icerik).tolist()
    vektor_json = json.dumps(vektor)

    conn = sqlite3.connect("dokumanlar.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO parcalar (dosya_adi, icerik, embedding) VALUES (?, ?, ?)",
        (dosya_adi, icerik, vektor_json)
    )
    conn.commit()
    conn.close()
    print(f"{dosya_adi} eklendi (embedding ile).")

if __name__ == "__main__":
    veritabani_olustur()

    with open("docs/ornek1.txt", "r", encoding="utf-8") as f:
        icerik = f.read()

    dokuman_ekle("ornek1.txt", icerik)