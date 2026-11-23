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
- `audio/jamendo/` — Jamendo'dan (Openverse üzerinden) indirilen parçalar; yine `"ambient_file"` ile seçilir
- `audio/freesound/` — Freesound'dan indirilen gerçek kayıtlar; gönderide `"ambient_file"` ile seçilir (sentez sesin yerine geçer), künyesi `"ambient_credit"` alanına yazılır

## Renk paletleri
Her gönderi `posts/<id>.json` içinde `"palette"` ile kendi rengini seçer. Koyu: zumrut, gece, seher, bordo, erguvan, firuze, toprak, zeytin, lacivert. Açık (siyah yazılı, 011 ve sonrası): fildisi, kum, nane, gul, gokyuzu, lavanta.

## Gönderi geçmişi
| No | Konu | Sahne | Palet | Ses |
|---|---|---|---|---|
| 001 | En hayırlı dost | companions | zumrut | gece |
| 002 | Kardeşini ayıplama | reflection | zumrut | gol |
| 003 | Kabr-i şerif ziyareti | medina | seher | guvercin |
| 004 | Hac ve umre yapanlar Allah'ın misafirleri | foto: Kâbe tavafı (Unsplash) | toprak | çöl rüzgârı (Freesound, CC0) |
| 005 | Ekmeğe hürmet | foto: ekmek ve başaklar (Unsplash) | zeytin | "Wheat Field Sway" arp (Jamendo, CC BY) |
| 006 | Helal lokma, makbul dua | foto: duaya açılmış eller (Unsplash) | erguvan | "Les grandes marches" piyano (Jamendo, CC BY) |
| 007 | Gıyabında kardeşlik | foto: sonbaharda yürüyen iki kişi (Unsplash) | firuze | "Music For Reunion Of Long Friendship" (Jamendo, CC BY) |
| 008 | Kalbi yumuşatan iki amel | foto: ellerde yemek kâsesi (Unsplash) | bordo | "Deep Study of a Calm Mind" piyano-yaylı (Jamendo, CC BY) |
| 009 | Hasta ziyareti | foto: torunun büyükannesinin elini tutması (Unsplash) | lacivert | "Diamonds (Early Mix)" gitar-yaylı (Jamendo, CC BY) |
| 010 | Kardeşini ayıplama (002 yeni haliyle) | foto: alacakaranlıkta durgun göl (Unsplash) | gece | "Reflection" piyano (Jamendo, CC BY) |
| 011 | Kardeşini dinlemek | foto: bankta sohbet eden iki yaşlı adam (Unsplash) | fildisi | "Morar" flüt-yaylı (Jamendo, CC BY) |
| 012 | Dilini ve namusunu koru | foto: açık kapıdan bahçe yolu (Unsplash) | kum | "Quiet Shroud" piyano (Jamendo, CC BY) |
| 013 | Birbirinize zulmetmeyin (hadis-i kudsî) | foto: eski bir terazi (Unsplash) | nane | "Un petit poème" piyano-yaylı (Jamendo, CC BY) |
| 014 | Birbirinize zulmetmeyin (013, HADÎS-İ KUDSÎ başlığıyla yeniden) | foto: eski bir terazi (Unsplash) | nane | "Un petit poème" piyano-yaylı (Jamendo, CC BY) |
| 015 | Kardeşine gıyaben dua | foto: elde tesbih (Unsplash) | gul | "Words Fall Apart" piyano (Jamendo, CC BY) |
| 016 | Rızkı helalinden iste | foto: yaşlı ustanın elleri, tahta çerçeve (Unsplash) | gokyuzu | "To The Light" yaylı (Jamendo, CC BY) |
| 017 | Dinin direği fıkıhtır | foto: müzede Osmanlı hat albümü (Unsplash) | lavanta | "passagé du vent" arp (Jamendo, CC BY) |
| 018 | İhsan | foto: camide minber ve pencereden süzülen ışık (Unsplash) | fildisi | "nuage" piyano-keman (Jamendo, CC BY) |
| 019 | Üç öğüt: farz, takva, kanaat | foto: sisli sahilde dengeli taşlar (Unsplash) | kum | "Dream keeper (dreamy version)" piyano (Jamendo, CC BY) |

## Fotoğraflı kapak (Unsplash)
Kapak slaytında `"kind": "photo"` kullanılır: `photo` (photos/ altındaki dosya), `title`, `subtitle`, `credit` ("Fotoğraf: Ad Soyad / Unsplash"), isteğe bağlı `focus` (ör. "center 30%"). Fotoğraflar `images.unsplash.com`'dan indirilir; bu adres `hikmet-notlari` bulut ortamında izinlidir.
