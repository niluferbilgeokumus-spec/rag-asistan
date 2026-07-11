from foundry_local_sdk import Configuration, FoundryLocalManager
from arama import en_benzer_parcayi_bul

def cevap_uret(soru):
    dosya, icerik, skor = en_benzer_parcayi_bul(soru)
    print(f"[Bulunan kaynak: {dosya}, benzerlik: {skor:.4f}]")

    config = Configuration(app_name="rag-asistan")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model("phi-3.5-mini")
    model.download()
    model.load()

    client = model.get_chat_client()

    prompt = f"""Asagidaki baglami kullanarak soruyu cevapla. Eger baglamda cevap yoksa, bilmediğini soyle.

Baglam:
{icerik}

Soru: {soru}
"""

    print("\nCevap: ", end="", flush=True)
    for chunk in client.complete_streaming_chat([{"role": "user", "content": prompt}]):
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