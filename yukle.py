import sqlite3
import os
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def veritabani_olustur():
    conn = sqlite3.connect("dokumanlar.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS parcalar")
    cursor.execute("""
        CREATE TABLE parcalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dosya_adi TEXT,
            icerik TEXT,
            embedding TEXT
        )
    """)
    conn.commit()
    conn.close()

def metni_parcala(metin):
    parcalar = [p.strip() for p in metin.split("\n\n") if p.strip()]
    if not parcalar:
        parcalar = [metin.strip()]
    return parcalar

def dokumanlari_yukle():
    veritabani_olustur()
    conn = sqlite3.connect("dokumanlar.db")
    cursor = conn.cursor()

    docs_klasoru = "docs"
    toplam = 0

    for dosya_adi in os.listdir(docs_klasoru):
        if not dosya_adi.endswith(".txt"):
            continue

        yol = os.path.join(docs_klasoru, dosya_adi)
        with open(yol, "r", encoding="utf-8") as f:
            metin = f.read()

        parcalar = metni_parcala(metin)

        for parca in parcalar:
            vektor = model.encode(parca).tolist()
            vektor_json = json.dumps(vektor)
            cursor.execute(
                "INSERT INTO parcalar (dosya_adi, icerik, embedding) VALUES (?, ?, ?)",
                (dosya_adi, parca, vektor_json)
            )
            toplam += 1

        print(f"{dosya_adi}: {len(parcalar)} parca eklendi.")

    conn.commit()
    conn.close()
    print(f"\nToplam {toplam} parca veritabanina eklendi.")

if __name__ == "__main__":
    dokumanlari_yukle()