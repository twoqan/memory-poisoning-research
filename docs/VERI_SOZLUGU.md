# Veri sözlüğü

Her JSONL satırı bir model çağrısıdır. Ortak alanlar:

| Alan | Açıklama |
|---|---|
| `experiment` | Deney sürümü (`memory-v4.1` veya `memory-v5`) |
| `backend` | `ollama` veya `openai` |
| `model_requested` | İstenen model adı |
| `case_id` | Senaryo kimliği |
| `orientation` | `original` veya `reversed` (sentetik ters politika) |
| `condition` | Bellek sunum koşulu |
| `expected` | Onaylı kayda göre doğru karar |
| `repeat` | Aynı girdi kombinasyonunun tekrar numarası (tam deneyde 1) |
| `system_prompt` | Model sistem talimatı |
| `user_prompt` | Modele iletilen soru ve kayıtlar |
| `records` | Kaynak etiketi, `trusted` işareti ve kayıt içeriği |
| `raw_response` | Ham model metni |
| `decision` | Çözümlenmiş `ENABLE` / `DISABLE` |
| `correct_decision` / `wrong_decision` | Hedef karara göre değerlendirme |
| `valid_json` / `error` | Yanıt geçerliliği / çağrı hatası |
| `metadata` | Model türüne göre kullanım, süre ve dönüş kimliği |
| `timestamp_utc` | Çağrı zamanı |

Koşullar: `clean`: yalnızca güvenilir kayıt; `untrusted_first`: önce güvenilmeyen; `trusted_first`: önce güvenilir; `trust_instruction`: güvenilmeyen önce + sistemde açık güven kuralı; `filtered`: güvenilmeyen kayıt gönderilmez. `clean` ve `filtered` aynı model girdisini üretir.
