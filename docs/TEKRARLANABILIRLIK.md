# Tekrarlanabilirlik ve sınırlar

**Yeniden hesaplama (ücretsiz):** Bu paket içindeki `veriler/*.jsonl` dosyalarından metrikleri `ozet_metrikler.csv` üzerinden kontrol edin. V5'te iki model arasında karşılaştırılan anahtar `(case_id, orientation, condition, repeat)` olup girdiler birebir aynıydı.

**Yeniden çalıştırma (isteğe bağlı):** `kod/` içindeki V5 deneyini yerel Ollama veya OpenAI API ile tekrar çalıştırabilirsiniz. API çağrıları ücretlidir. Anahtarınızı koda, ZIP içine veya yayın dosyalarına koymayın. Komutlar örnektir; var olan sonuç dosyalarını ezmeyin:

```bash
cd kod
python3 -m unittest -v test_v5.py
python3 lab_v5.py --backend ollama --model qwen3:8b --repeats 1 --output ../yeni_qwen.jsonl
python3 lab_v5.py --backend openai --model gpt-4.1-mini --repeats 1 --output ../yeni_openai.jsonl
```

**Önemli:** V4.1'in kaynak kodu ve verileri pakette bulunur, fakat onunla çalışan `cases.json` dosyasının adının `cases.json` olması ve yanında `lab_base.py` bulunması gerekir; `kod/` içindeki `v4_1_` önekli dosyalar bu nedenle bağımsız olarak doğrudan çalıştırılamaz. Özgün V4.1 proje ZIP'iyle yeniden çalıştırmak daha uygundur. Mevcut veriyi incelemek için bu gerekmez.

**Sınırlar:** Önceden oluşturulmuş kayıtları okuma anında karşılaştıran sentetik testtir; yazma-anı saldırısı veya ajan ele geçirme testi değildir. Bir örneğin beş koşulu ve iki yönü eşleştirilmiştir; bağımsız deney gözlemleri değildir. Her kombinasyon tek kez koşulmuştur. Modellerin altyapı ve örnekleme ayarları tamamen eşit değildir. Model çıktıları servis sürümleri nedeniyle tekrar koşulunca değişebilir. `filtered` başarı oranı uygulama filtrelemesinin sonucudur; modelin kendi kendine saldırıyı yakaladığı anlamına gelmez.
