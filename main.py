# RAG Asistani - Ana Program
# Kullanicidan soru alir, en alakali dokuman parcalarini bulur,
# bu bilgiyi kullanarak Foundry Local uzerinden yerel bir modelden cevap uretir.

from foundry_local_sdk import Configuration, FoundryLocalManager
from arama import get_top_chunks

# Eger en iyi eslesme skoru bu degerin altindaysa, model hic cagrilmaz,
# sistem direkt "bilgim yok" der. Bu, alakasiz sorularda uydurma
# (halusinasyon) cevap verilmesini onlemek icindir.
ESIK_DEGERI = 0.45


def modeli_hazirla():
    """Foundry Local servisini baslatir ve Phi-3.5-mini modelini yukler."""
    config = Configuration(app_name="rag-asistan")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model("phi-3.5-mini")
    model.download()
    model.load()

    return model


def cevap_uret(client, soru):
    """Verilen soru icin en alakali dokumanlari bulur ve modelden cevap alir."""
    top_chunks = get_top_chunks(soru, k=3)

    # Alakali bilgi yoksa veya cok zayifsa, modele hic sormadan cik.
    if not top_chunks or top_chunks[0][0] < ESIK_DEGERI:
        print("Cevap: Bu konuda dokumanlarimda yeterli bilgi bulamadim.")
        return

    baglam_parcalari = []
    for skor, dosya, icerik in top_chunks:
        print(f"[Bulunan kaynak: {dosya}, benzerlik: {skor:.4f}]")
        baglam_parcalari.append(icerik)

    baglam = "\n\n".join(baglam_parcalari)

    # Modele, sadece verilen baglami kullanmasini ve uydurmamasini soyluyoruz.
    sistem_mesaji = (
        "Sen sadece verilen baglami kullanarak soru cevaplayan bir asistansin. "
        "Eger cevap baglamda yoksa, bilmediğini soyle, tahmin yurutme veya uydurma bilgi verme. "
        "Cevaplarini kisa, net ve tek bir paragraf halinde tut. "
        "Sadece dogru, akici ve dilbilgisi kurallarina uygun Turkce kullan. "
        "Anlamsiz veya uydurma kelimeler kullanma, sadece bildigin gercek Turkce kelimeleri kullan."
    )

    kullanici_mesaji = f"""Baglam:
{baglam}

Soru: {soru}"""

    # Cevap streaming (parca parca) olarak uretiliyor.
    # Bunun sebebi: uzun cevaplarda tek seferlik bekleme zaman asimina (timeout) sebep oluyordu.
    print("Cevap: ", end="", flush=True)
    for chunk in client.complete_streaming_chat([
        {"role": "system", "content": sistem_mesaji},
        {"role": "user", "content": kullanici_mesaji}
    ]):
        if not chunk.choices:
            continue
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    print()


def main():
    print("RAG Asistani baslatiliyor, lutfen bekleyin...\n")
    model = modeli_hazirla()
    client = model.get_chat_client()

    print("Hazir! Sorunu yaz (cikmak icin /exit yaz)\n")

    while True:
        soru = input("Soru: ").strip()

        if soru.lower() == "/exit":
            print("Gorusuruz!")
            break

        if not soru:
            continue

        cevap_uret(client, soru)
        print()

    model.unload()


if __name__ == "__main__":
    main()