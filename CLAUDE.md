# hikmet-notlari — çalışma talimatları

Bu depo @hikmet_notlari Instagram hesabının kartlarını ve Reels videolarını üretir. Hesap sahibiyle **Türkçe**, sade ve teknik terim kullanmadan konuş.

## "Yeni reels paylaş" denince

Kullanıcı genellikle bir hadis-i şerifin Arapça metnini, Türkçe mealini ve kaynağını verir. Akış:

1. `posts/<sonraki-no>.json` yaz (numara üç haneli: 008, 009, ...). Yapı için son gönderilere bak.
2. `python3 render.py <no>` → `cards/<no>-1.jpg` (kapak) ve `cards/<no>-2.jpg` (metin). Çıktıyı görsel olarak kontrol et (metin taşması, tek kelimelik yetim satır, başlığın okunurluğu); gerekirse `ar_size` / `tr_size` ayarla.
3. `./make_reel.sh <no>` → `reels/<no>.mp4`. Metin uzunsa metin kartının süresini uzat: `T2=16 ./make_reel.sh <no>`.
4. `./make_reel_audio.sh <no>` → `reels/<no>-sesli.mp4`.
5. README'deki gönderi geçmişi tablosuna satır ekle, commit et ve geliştirme dalına push et.
6. Instagram'a Windsor (`mcp__Windsor_ai_for_Social_Media__execute_action`, `create_video_post`) ile **doğrudan paylaş**. "Paylaş" talimatı onaydır; ayrıca sorma.
   - `video_url` / `cover_url`: `https://raw.githubusercontent.com/selmanaygul/hikmet-notlari/<dal>/reels/<no>-sesli.mp4` ve `.../reels/<no>-cover.jpg`. Önce adresin 200/206 döndüğünü kontrol et.
   - `share_to_feed: true`.
   - Paylaşım zaman aşımına uğrarsa **tekrar gönderme**; önce Windsor `get_data` ile son medyaya bakıp yayınlanıp yayınlanmadığını doğrula (çift paylaşım olmasın).

## Görsel

- Her reelde **farklı bir görsel**: kapak, Unsplash fotoğrafıdır (`"kind": "photo"`). Unsplash MCP ile ara, `download_asset` ile indir, `photos/<no>-<konu>.jpg` olarak kaydet.
- Konuya uygun, edepli, İslami hassasiyete aykırı olmayan fotoğraf seç (başka dinlere ait ibadet sahneleri, kadın-erkek yakınlığı vb. olmasın).
- Kapakta künye: `"credit": "Fotoğraf: <Ad> / Unsplash"`.
- **Renk:** Çoğunlukla **açık paletler** (zemin açık, yazılar siyah): `fildisi, kum, nane, gul, gokyuzu, lavanta`. Hesap sahibi **ara sıra koyu tema** da istiyor: kabaca her 4 gönderiden birinde (son 3 gönderi açıksa) ya da konu/fotoğraf koyuya uygunsa (gece, akşam, ahiret, tefekkür gibi) bir **koyu palet** seç: `zumrut, gece, seher, bordo, erguvan, firuze, toprak, zeytin, lacivert`. Koyu palette kartlar koyu zemin, açık renk yazı olur. Art arda iki koyu kullanma.
- **Kapak fotoğrafı koyu olabilir.** Açık palette koyu fotoğraf seçilirse kapak otomatik olarak koyu temaya geçer (koyu gölge, krem başlık, altın süs); orta/açık fotoğrafta açık tül ve siyah yazı kalır. Açık palette hadis metni karesi açık zemin, siyah yazıdır. Gerekirse kapak slaytına `"cover": "dark"` veya `"light"` yazarak elle seç.
- Paleti seçerken README tablosuna bak: o gruptan (açık ya da koyu) **daha önce kullanılmamış** olanı, hepsi kullanıldıysa **en uzun süredir kullanılmayanı** seç.

## Ses

- Her reelde **farklı bir ses**. Ses kaynağı **Jamendo**: Openverse API ile ara (`https://api.openverse.org/v1/audio/?q=...&source=jamendo&license=by,cc0`), dosyayı `https://prod-1.storage.jamendo.com/?trackid=<id>&format=mp32` adresinden indir, `audio/jamendo/<id>.mp3` olarak kaydet.
- Yalnızca **CC BY veya CC0** lisanslı parçalar. **ND (türetilemez) lisanslıları kullanma** (videoya eklemek türetme sayılır). NC ve SA'dan da kaçın.
- Sözsüz (vocal etiketi olmayan), sakin, ağır tempolu parçalar. İndirdikten sonra ses seviyesine ve dalga biçimine bak: uzun sessizlikli, seyrek parçaları ele.
- Gönderi dosyasında: `"ambient_file"`, gerekirse baştaki sessizliği atlamak için `"ambient_start"` (saniye), künye için `"ambient_credit"`.
- Freesound bu bulut ortamından erişilemiyor (403); deneme. `audio/ambient.py` sentez sesleri yalnızca kullanıcı isterse kullanılır.

## Metin ve açıklama

- Kullanıcının verdiği Arapça metni ve meali **değiştirme**. Meal yarım kalmışsa Arapçaya göre tamamla ve kullanıcıya söyle. Kaynak kısaltmalarını açık yaz (ör. (هـ) → Sünen-i İbn Mâce, (هق) → Beyhakî, (طس) → Taberânî, el-Mu’cemü’l-Evsat, (ج) → Süyûtî, el-Câmiu’s-Sağîr); kullanıcı kaynağı yazdıysa onu kullan.
- **Kalın yazı:** Mealde tırnak içindeki asıl hadis-i şerif cümlesini (ayet-i kerime ise ayetin kendi cümlesini) kalın göster. Gönderi dosyasında `"turkish"` alanında o kısmı `**…**` arasına al (tırnak işaretleri dışarıda kalsın); `render.py` bunu kartta kalın basar. Instagram açıklamasında gerçek kalın yazı yok; açıklamadaki meal düz kalır.
- **Hadis-i kudsî:** Metin "Allâhü Teâlâ şöyle buyurdu" gibi Allah'ın sözünü naklediyorsa gönderi dosyasına `"label": "HADÎS-İ KUDSÎ"` yaz (kapakta ve metin karesinde bu başlık çıkar), kapaktaki kaydırma yazısını "Hadis-i kudsîyi okumak için kaydır  →" yap ve kalın kısmı Allah'ın sözü olan cümle yap. Açıklamaya `#hadisikudsi` etiketini ekle.
- **Hicrî tarih:** Kullanıcı mesajın sonunda tarih (ör. "06 Cemâziyelâhir 1448") verirse gönderi dosyasına `"date"` olarak yaz; metin kartında kaynağın altında küçük basılır.
- Instagram açıklaması şu düzende:
  1. Başlık + konuya uygun emoji
  2. Arapça metin
  3. Türkçe meal
  4. `📖 <Kaynak>`
  5. Kısa bir öğüt cümlesi ve dua (🤲)
  6. **İngilizce bölüm** (Türkçe metnin altında, `🇬🇧` ile başlar): başlığın İngilizcesi, mealin sadık İngilizce çevirisi (anlamı değiştirme; parantez içi açıklamaları da çevir), `📖 <Source>` (ör. Sunan al-Tirmidhi, Sahih Muslim, Musnad Ahmad, al-Jami' al-Saghir (al-Suyuti), Shu'ab al-Iman (al-Bayhaqi)), öğüt ve duanın İngilizcesi (🤲). Peygamber Efendimizin adından sonra "ﷺ" kullan. Arapça metni tekrar yazma.
  7. `📷 Fotoğraf: <Ad> / Unsplash` ve `🎵 Müzik: "<Parça>" – <Sanatçı> / Jamendo (CC BY 3.0)`
  8. Türkçe etiketler: `#hadis #hadisişerif #hadisler` + konuya özel 3–4 etiket + `#peygamberimiz #sünnet #hikmetnotlari`. `#reels` kullanma.
  9. İngilizce etiketler (Türkçelerin hemen ardından, aynı satırda): `#hadith #hadiths #prophetmuhammad #sunnah #islam #islamicreminders` + konuya özel 2–3 İngilizce etiket. Toplam etiket sayısı 30'u geçmesin (Instagram sınırı).
- Açıklama 2200 karakteri geçmemeli (Instagram sınırı); uzun hadislerde öğüt cümlesini kısalt.
- Açıklamada **yorum isteyen soru cümlesi kullanma** ("… nedir? Yorumlarda paylaşın.", "Siz ne düşünüyorsunuz?", "Dostunu etiketle" gibi). Hesap sahibi bunu istemiyor.

## Genel

- Paylaştıktan sonra kullanıcıya kısa özet ver: görsel, ses (lisansıyla), süre, açıklamada neler var.
- Bir adımı başaramadıysan (ör. bir servis erişilemiyor) bunu açıkça söyle; başarmış gibi gösterme. Onay penceresi gibi göremediğin şeyler hakkında tahminde bulunma.
- Paylaşım saati için öneri: Türkiye saatiyle akşam 19:00–21:00 arası; aynı gün art arda çok sayıda reel paylaşmaktan kaçın.
