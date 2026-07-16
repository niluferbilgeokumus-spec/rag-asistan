from foundry_local_sdk import Configuration, FoundryLocalManager
from arama import get_top_chunks

def cevap_uret(soru):
    top_chunks = get_top_chunks(soru, k=3)

    baglam_parcalari = []
    for skor, dosya, icerik in top_chunks:
        print(f"[Bulunan kaynak: {dosya}, benzerlik: {skor:.4f}]")
        baglam_parcalari.append(icerik)

    baglam = "\n\n".join(baglam_parcalari)

    config = Configuration(app_name="rag-asistan")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model("phi-3.5-mini")
    model.download()
    model.load()

    client = model.get_chat_client()

    sistem_mesaji = (
        "Sen sadece verilen baglami kullanarak soru cevaplayan bir asistansin. "
        "Eger cevap baglamda yoksa, bilmediğini soyle, tahmin yurutme. "
        "Cevaplarini kisa ve net tut."
    )

    kullanici_mesaji = f"""Baglam:
{baglam}

Soru: {soru}"""

    print("\nCevap: ", end="", flush=True)
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

    model.unload()

def main():
    soru = "Fourier serisi nedir?"
    cevap_uret(soru)

if __name__ == "__main__":
    main()