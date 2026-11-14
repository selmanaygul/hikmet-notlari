# hikmet_notlari

@hikmet_notlari Instagram sayfasının kartları ve kart üretici.

- `posts/<id>.json` — gönderi içeriği (metin, kaynak, sahne)
- `scenes.py` — konuya özel vektör illüstrasyonlar
- `render.py` — `python3 render.py <id>` → `cards/<id>-N.jpg` (1080×1350)
- `cards/` — Instagram'ın çektiği, herkese açık JPEG'ler

- `make_reel.sh <id>` → `reels/<id>.mp4` (1080×1920 Reels videosu)
- `make_reel_audio.sh <id>` → `reels/<id>-sesli.mp4` (gönderideki `ambient` sesiyle)
- `audio/ambient.py` — ortam sesi kütüphanesi: gece, gol, yagmur, dere, dalga, sabah, ates (sentez, müziksiz)
- `audio/ornekler/` — her sesin 12 sn'lik örneği
