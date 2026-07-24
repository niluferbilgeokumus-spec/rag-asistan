# RAG Asistanı

Yerel olarak calisan, kendi dokumanlarindan bilgi cekerek soru cevaplayan bir yapay zeka asistani. Microsoft Foundry Local ve Phi-3.5-mini modeli kullanilarak gelistirilmistir. Tamamen internetsiz calisir.

## Amac

Bu proje, RAG (Retrieval-Augmented Generation) mimarisini uygulamali olarak ogrenmek amaciyla gelistirilmistir. Sistem, kendi dokumanlarindaki bilgilere dayanarak sorulari cevaplar; dokumanlarda olmayan konularda ise "bilmiyorum" der, uydurma bilgi vermez.

## Nasil Calisir

1. Kullanici bir soru sorar
2. Soru, embedding modeliyle (sentence-transformers) sayisal bir vektore cevrilir
3. Veritabanindaki tum dokuman parcalarinin vektorleriyle karsilastirilir (cosine similarity)
4. En alakali 3 parca bulunur (top-k arama)
5. Eger en iyi eslesme skoru cok dusukse, sistem "bilgim yok" der
6. Yeterince alakali bilgi bulunursa, bu bilgi + soru, Phi-3.5-mini modeline gonderilir
7. Model, sadece verilen baglama dayanarak cevap uretir

## Kullanilan Teknolojiler

- Python 3.14
- Microsoft Foundry Local (yerel LLM calistirma)
- Phi-3.5-mini (dil modeli)
- sentence-transformers (embedding)
- SQLite (veritabani)

## Kurulum

1. Python 3.10+ kurulu olmali
2. Foundry Local runtime kurulu olmali: winget install Microsoft.FoundryLocal
3. Gerekli Python paketlerini kur: pip install foundry-local-sdk sentence-transformers

## Kullanim

1. Dokumanlarini docs/ klasorune .txt dosyalari olarak ekle
2. Dokumanlari veritabanina yukle: python yukle.py
3. Asistani baslat: python main.py
4. Sorularini yaz, cikmak icin /exit yaz

## Proje Dosyalari

- main.py: ana program, sohbet dongusu ve RAG mantigi
- arama.py: soru-dokuman benzerlik arama fonksiyonu
- yukle.py: dokumanlari parcalayip veritabanina ekleyen script
- docs/: kaynak dokumanlar
- dokumanlar.db: SQLite veritabani (dokuman parcalari ve embedding'ler)

## Tasarim Kararlari ve Sinirlamalar

- Benzerlik esigi (0.45): Eger en alakali dokuman bile yeterince benzer degilse, sistem modele sormadan "bilmiyorum" der. Bu, uydurma (halusinasyon) cevaplari onlemek icin eklendi.
- Streaming kullanimi: Uzun cevaplarda yasanan zaman asimi (timeout) sorunu nedeniyle, cevaplar parca parca (streaming) uretiliyor.
- Kucuk model sinirlamasi: Phi-3.5-mini, kucuk ve hizli bir model oldugu icin, bazen Turkce dilbilgisi acisindan tutarsiz cevaplar uretebiliyor. Sistem promptuna eklenen talimatlarla bu kismen iyilestirildi ancak tamamen cozulemedi.
- Chunk'lama: Dokumanlar bos satirlara gore parcalara bolunuyor; kisa dokumanlarda genelde tek parca olarak kaliyor.

## Test Sonuclari

Sistem, cevaplanabilir sorularda (dokuman icerigiyle ilgili) dogru kaynagi bulup anlamli cevaplar uretti. Cevaplanamaz sorularda (dokumanlarda olmayan konular) tutarli sekilde "bilgim yok" cevabini verdi. Bos soru gibi kenar durumlarda sistem cokmedi.