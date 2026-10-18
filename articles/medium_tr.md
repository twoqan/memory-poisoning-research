# Memory Poisoning: Yapay Zekânın Hatıraları Manipüle Edilebilir mi?

*İki dil modeli, iki kontrollü deney ve 800 yanıt: Güvenilmeyen bellek kayıtları bir yapay zekânın kararını değiştirebilir mi?*

## Aynı projeye ait iki not. Birbirine zıt iki karar.

Bir yazılım projesinde çalıştığınızı düşünün. Yapay zekâ asistanınıza basit bir soru soruyorsunuz: **“Bu özellik açık mı olmalı, kapalı mı?”**

Asistan, proje belleğinden iki kayıt getiriyor. İlki, yetkili ekip tarafından onaylanmış politika. İkincisi, sonradan içeri aktarılmış ve doğrulanmamış eski bir belge. İkisi aynı ayar hakkında tam tersini söylüyor.

Soru artık yalnızca asistanın metni anlayıp anlamadığı değil: **Hangi kayda güveneceği.**

Belge arama, Retrieval-Augmented Generation (RAG) ve uzun süreli bellek kullanan sistemlerde bu ayrım kritik. Dışarıdan gelen metin, bağlam sağlamak için yararlıdır; ancak yetkili bir karar kaynağı gibi ele alındığında yanlış sonuçlar üretebilir. Dolaylı prompt injection literatürü de, güvenilmeyen içeriğin uygulama davranışını etkileyebileceğini gösteriyor [1].

Biz bu geniş güvenlik probleminin küçük ama ölçülebilir bir bölümünü test ettik: **Bir dil modeli, aynı konu için çelişen iki bellek kaydından hangisini esas alıyor?**

> **Kapsam notu:** Bu çalışmada saldırganın gerçek bir ajanın kalıcı belleğine veri yazdığı bir saldırı gerçekleştirilmedi. Çelişkili kayıtlar test düzeneğinde önceden oluşturuldu. Ölçtüğümüz şey, *okuma anındaki bellek kaynağı çelişkisinin* karar üzerindeki etkisiydi.

## Deney tasarımı: Neden iki ayrı veri kümesi kullandık?

İki modeli karşılaştırdık:

- **Qwen3 8B:** MacBook Pro M2 Pro üzerinde Ollama ile yerel çalıştırıldı. JSON çıktı, düşünme kapalı, sıcaklık `0`, sabit tohum `42` ve çıktı sınırı `512` olarak yapılandırıldı.
- **GPT-4.1 mini:** OpenAI Responses API üzerinden çağrıldı; `max_output_tokens=240` ve `store=false` kullanıldı.

İlk veri kümesi **V4.1**, çok faktörlü kimlik doğrulama, yedekleme ve üretim ortamı güvenliği gibi **20 yazılım politikası** içeriyordu. Bu örneklerde modelin önceden öğrendiği güvenlik bilgisi kararları etkileyebilirdi. Bu nedenle ikinci veri kümesi **V5**'i oluşturduk: Güvenlik açısından doğal olarak doğru veya yanlış sayılmayan **20 kurgusal arayüz özelliği**.

Örneğin onaylı politika bir uygulamadaki mor etiketin etkin olduğunu belirtirken, içeri aktarılan eski belge devre dışı olduğunu söylüyordu. Böylece güvenlik çağrışımını azaltıp kaynak tercihini incelemeye çalıştık.

Her konuyu iki yönlü sınadık: `original` ve beklenen kararın tersine çevrildiği `reversed`. Bunlar aynı konunun eşleştirilmiş, sentetik karşı-olgusal örnekleridir; gerçek sistemlere uygulanması önerilen ayarlar değildir.

![Deneyin yüksek seviyeli işleyişi](gorseller/03_deney_mimarisi.png)

*Şekil 1 — Onaylı ve doğrulanmamış kayıtların farklı koşullarda modele iletildiği deney mimarisi. Sistem kayıtları önceden hazırlıyor; otonom bellek yazma aşaması yok.*

### Beş kontrol koşulu

| Koşul | Modele sunulan içerik |
|---|---|
| **Clean** | Yalnızca onaylı politika |
| **Untrusted First** | Önce doğrulanmamış belge, sonra onaylı politika |
| **Trusted First** | Önce onaylı politika, sonra doğrulanmamış belge |
| **Trust Instruction** | Doğrulanmamış belge önce; ayrıca sistem talimatında onaylı politikanın üstünlüğü belirtiliyor |
| **Filtered** | Uygulama doğrulanmamış kaydı ayıklıyor; yalnızca onaylı politika gönderiliyor |

Bir deney sürümünde, bir model için **20 konu × 2 karar yönü × 5 koşul = 200 çağrı** bulunuyor. İki model ve iki sürümün toplamı **800 yanıt**. Her benzersiz kombinasyon yalnızca bir kez çalıştırıldı; dolayısıyla bunlar 800 bağımsız saldırı örneği değil.

## İlk sonuç: Model farkı nötr senaryolarda da sürdü

| Model | V4.1: Güvenlik politikaları | V5: Nötr özellikler |
|---|---:|---:|
| Qwen3 8B | **150/200 (%75)** | **149/200 (%74,5)** |
| GPT-4.1 mini | **194/200 (%97)** | **196/200 (%98)** |

![Model ve deney sürümü karşılaştırması](gorseller/01_model_karsilastirma.png)

*Şekil 2 — V4.1 ve V5'te onaylı politika ile uyumlu karar oranları. Bu yüzdeler gerçek dünyadaki saldırı başarı oranları değildir.*

Farkın V5'te de sürmesi, V4.1 sonuçlarının **yalnızca** modellerin güvenlik konularındaki önceki bilgileriyle açıklanamayabileceğini düşündürüyor. Bununla birlikte, veri kümesinin sentetik yapısı ve iki modelin farklı çalışma ayarları nedeniyle doğrudan nedensellik iddiasında bulunamayız.

### Asıl fark, çelişkili kayıtlar birlikte verildiğinde ortaya çıkıyor

| V5 koşulu | Qwen3 8B | GPT-4.1 mini |
|---|---:|---:|
| Clean | 40/40 | 40/40 |
| Untrusted First | 20/40 | 36/40 |
| Trusted First | 29/40 | 40/40 |
| Trust Instruction | 20/40 | 40/40 |
| Filtered | 40/40 | 40/40 |

![V5 koşullarına göre model karşılaştırması](gorseller/02_v5_kosullar.png)

*Şekil 3 — V5'te koşul bazında doğru karar sayıları. Her koşulda model başına 40 eşleştirilmiş görev var.*

**Yalnızca çelişkili iki kaydın birlikte sunulduğu üç koşulu** dikkate aldığımızda:

- Qwen3 8B: **69/120 (%57,5)** doğru karar.
- GPT-4.1 mini: **116/120 (%96,7)** doğru karar.

Temiz girdilerde iki modelin de 40/40 doğru sonuç üretmesi önem taşıyor: Ayrışma, görevin basit biçiminde değil, **çelişen kayıtların birlikte bulunduğu bağlamlarda** belirginleşiyor.

## Aynı sorularda hangi model nerede yanıldı?

V5'te her iki modele verilen 200 girdiyi eşleştirerek inceledik:

| Eşleştirilmiş sonuç | Girdi sayısı |
|---|---:|
| İki model de doğru | 149 |
| Yalnızca GPT-4.1 mini doğru | 47 |
| Yalnızca Qwen3 8B doğru | 0 |
| İki model de yanlış | 4 |

GPT-4.1 mini'nin hata yaptığı **dört girdi**, Qwen3 8B'nin de yanlış cevapladığı girdiler arasındaydı. Ancak bu sonuç, GPT-4.1 mini'nin genel olarak her koşulda üstün olduğunu kanıtlamaz; yalnızca **bu veri kümesi ve yapılandırmada** ne gözlediğimizi açıklar.

### Dikkat çeken karar yönü: `DISABLE`

V5'te Qwen3 8B'nin **51 hatasının tamamında**, onaylı politikaya göre beklenen `ENABLE` yerine `DISABLE` yanıtı verildi. GPT-4.1 mini'nin dört hatasında da aynı yön vardı. Qwen3 8B'nin V4.1'deki 50 hatasının 49'u bu yöndeydi; bir hata ters yönde gerçekleşti.

Bu örüntü, kaynak çelişkisinin yanında karar etiketinin kendisine veya kullanılan ifade biçimine duyarlılık olabileceğini düşündürüyor. Fakat yalnızca `ENABLE` ve `DISABLE` etiketleriyle yapılan bir deney, bu eğilimin nedenini kesinleştiremez. Gelecek deneylerde etiketleri değiştirmek, eşdeğer ifadeler kullanmak ve sıra etkisini yeniden sınamak gerekir.

## Sistem talimatı mı, uygulama düzeyinde güven sınırı mı?

**Trust Instruction** koşulunda modele, `approved_policy` kaydının yetkili olduğu açıkça söylendi. V5 sonuçları GPT-4.1 mini için **40/40**, Qwen3 8B için **20/40** oldu. Bu, tek bir talimat kalıbının farklı modellerde farklı sonuçlar doğurabileceğini gösteriyor; talimatların her durumda etkili ya da etkisiz olduğunu değil.

**Filtered** koşulunda ise güvenilmeyen kayıt hiç modele gönderilmedi. Burada kritik ayrım şu: **`Clean` ile `Filtered` koşullarında modelin aldığı girdiler birebir aynıydı.** İkisinin de 40/40 çıkması, modelin kötü kaydı tanıyıp reddettiği anlamına gelmiyor. Kaydı uygulama kodu dışarıda bıraktı.

Bu, OWASP'ın güvenilmeyen dış içeriği ayırma, giriş/çıkış doğrulama ve yetkileri sınırlandırma önerileriyle uyumlu bir tasarım prensibi [3]. Bununla birlikte gerçek dünyada hangi kaydın `approved_policy` sayılacağına kimin karar verdiği ayrıca güvence altına alınmalıdır. Yanlış kaynak etiketleri, modelden önce başlayan ayrı bir güvenlik problemidir.

## Peki bu gerçekten “memory poisoning” mi?

**Dar anlamda bir bellek çelişkisi deneyi; tam kapsamlı bir bellek zehirleme saldırısı değil.** Dışarıdan getirilen içeriğin modele iletilmesiyle ortaya çıkan güven sınırı problemi, Greshake ve arkadaşlarının dolaylı prompt injection çalışmasıyla ilişkilidir [1]. Uzun süreli ajan belleğine zehirli deneyimlerin yerleştirilmesini araştıran MemoryGraft ise daha kapsamlı bir saldırı senaryosunu ele alır [2].

Bizim düzeneğimizde:

- Bellek kayıtları baştan oluşturuldu; **saldırganın belleğe yazma süreci** ölçülmedi.
- Uzun vadeli hatırlama, çok oturumlu etki, araç çağrıları ve yetkisiz sistem eylemleri test edilmedi.
- Kaynak etiketleri deney uygulaması tarafından atandı; gerçek dünyadaki köken doğrulaması sınanmadı.
- Her kombinasyon tek kez çalıştırıldı. Sıcaklık ve tohum ayarları, farklı sunucu/model koşullarını bütünüyle eşitlemez.
- Aynı konular koşullar arasında tekrar kullanıldığı için gözlemler bağımsız değil. Burada güven aralığı veya istatistiksel anlamlılık iddiasında bulunmuyoruz.

Dolayısıyla **%74,5 ve %98**, “bu modellere yapılan bellek saldırılarının başarı oranları” değil; belirlenmiş kontrollü görevlerde **onaylı politikayla uyumlu karar oranlarıdır**.

## Sonuç: Bir asistanın neyi hatırladığı kadar, kime inandığı da önemli

Bu deneyde iki model, aynı bellek çelişkilerine aynı şekilde tepki vermedi. GPT-4.1 mini mevcut testlerde daha yüksek uyum gösterdi; Qwen3 8B ise özellikle beklenen karar `ENABLE` iken çelişkili kayıtlardan daha sık etkilendi. Fark, güvenlik senaryolarının yerine kurgusal ve nötr özellikler konulduğunda da görüldü.

Ancak bundan çıkarılması gereken ders yalnızca “daha güçlü bir model seçmek” değil. **Bir yapay zekâ uygulamasının güvenilirliği; belleğe neyin yazıldığına, kayıtların kökeninin nasıl doğrulandığına ve güvenilmeyen içeriğin modelden önce nasıl denetlendiğine de bağlı.**

Bu çalışma, son söz olmaktan çok yeni ve daha iyi kontrol edilmiş deneyler için başlangıç noktası: Yapay zekâya bir şeyi hatırlatmak kolay olabilir. Asıl mesele, **ona neye güvenmesi gerektiğini güvenilir biçimde öğretip öğretemediğimiz.**

---

### Kaynaklar ve yöntem dosyaları

**[1]** Greshake, K. ve diğerleri (2023). *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*. https://arxiv.org/abs/2302.12173

**[2]** Srivastava, S. S. ve He, H. (2025). *MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval*. https://arxiv.org/abs/2512.16962

**[3]** OWASP GenAI Security Project. *LLM01:2025 Prompt Injection*. https://genai.owasp.org/llmrisk/llm01-prompt-injection/

**Tekrarlanabilirlik:** Deney kodu, dört koşunun ham JSONL kayıtları, manifestler, grafikler ve veri sözlüğü eşlik eden araştırma paketinde yer alıyor. *Yayın sırasında bu paket için erişilebilir bir bağlantı eklenmelidir; bu taslakta gerçek bir yayın adresi olmadığı için uydurulmamıştır.*
