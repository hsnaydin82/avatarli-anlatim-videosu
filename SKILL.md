---
name: avatarli-anlatim-videosu
description: Sol altta konuşan çizgi film avatarı olan, sol üstte kelime kelime akan yazılı, koyu zeminli 9:16 anlatım videosu (Reels/TikTok/Shorts) üretir. Kişinin fotoğrafından SVG avatar çizer, senaryoyu ve sahne animasyonlarını HTML olarak yazar, seslendirme metinlerini verir, sesler gelince sesli MP4 çıkarır. "Avatarlı video", "bu referans gibi anlatım videosu", "konuşan karakterli Reels", "fotoğrafımı avatar yap, ürünümü anlatsın" denince kullan.
---

# Avatarlı Anlatım Videosu (9:16)

Kişisel "ben bunu neden yaptım / bu nasıl çalışır" videoları: anlatıcı sol altta duran bir çizgi film avatarı, konuşurken ağzı oynar ve el hareketi yapar. Üstte seslendirmeyle eşzamanlı akan büyük yazı, ortada sahneye özel animasyonlu görsel vardır.

Kullanıcı genelde bir konu, bir referans video ve bir fotoğraf verir. Sen referansı incelersin, avatarı çizersin, senaryoyu ve animasyonu yazarsın, seslendirme metinlerini verirsin. Sesler gelince MP4'ü üretirsin.

## Klasör

```
assets/sablon.html     oynatıcı motoru + örnek 3 sahne (kanca, çözüm geçişi, kapanış)
assets/avatar.svg      parçaları sınıflarla ayrılmış örnek avatar (yeni kişi için yeniden çizilir)
assets/logo-ornek.svg  <symbol id="logo"> örneği; markanın logosuyla değiştir
scripts/derle.py       şablon + logo + avatar → tek HTML
scripts/peek.py        sahne sonlarından hızlı kontrol kareleri
scripts/sure.py        ses sürelerine göre sahne sürelerini günceller
scripts/render.py      1080x1920 / 30 fps kareler + sesler → MP4
```

Gerekenler: Python 3, `pip install playwright` ve `playwright install chromium`, PATH'te ffmpeg/ffprobe. Bunlar kurulu değilse kurmadan önce kullanıcıya sor.

## Akış

### 1. Referansı incele (varsa)

Videoyu izlemeye çalışma; kare panosu çıkar ve bir kez bak:

```bash
ffprobe -v error -show_entries format=duration:stream=width,height -of compact ref.mp4
ffmpeg -y -loglevel error -i ref.mp4 -vf "fps=1/3,scale=240:-1,tile=8x2" -frames:v 1 pano.jpg
```

Gerekirse tek bir tam kare de al (`-ss 4 -frames:v 1`). Şunları not et:
- zemin rengi ve dokusu
- vurgu renkleri
- yazının yeri ve boyutu, yazının nasıl değiştiği (öbek öbek mi, kelime kelime mi)
- avatarın yeri ve hareketleri
- sahne görsellerinin tarzı
- toplam süre

Şablon varsayılan olarak koyu noktalı zemin, limon yeşili vurgu ve pembe ikinci renk kullanır. Referans farklıysa `:root` token'larını değiştir.

### 2. Avatarı çiz

**Kişinin fotoğrafını hiçbir dış servise (avatar üretici, görsel yapay zekâ) gönderme.** Kişisel veridir; kullanıcı açıkça istemedikçe yükleme yapma. Fotoğrafa bakıp `assets/avatar.svg` yapısında elle SVG çiz:

- Fotoğraftan şunları al: saç rengi ve şekli, sakal/bıyık, gözlük, ten rengi, kıyafet rengi ve tipi, yüz şekli, gülüşün belirginliği.
- Avatar düz renkli olsun, kontur çizgisi kullanma. Hafif gölge tonu kullan.
- Kişi "bu ben değilim" demesin diye ayırt edici 2-3 özelliği abart: gözlük, sakal, saç şekli.
- Kullanıcının hazır bir avatarı varsa (Bitmoji, kendi çizimi) onu kullan. Ama pozlar ve ağız hareketi için yine bu parça yapısına çevir.

**Zorunlu yapı** (motor bu sınıflara bakar; viewBox `0 0 260 300`, kişi belden yukarı, alt kenarda kesik):

| Parça | Sınıf | Not |
|---|---|---|
| Gövde | `av-govde` | duran kollar: `kol-sol-dur`, `kol-sag-dur` |
| Baş | `av-bas` | dönme merkezi boyun (120,165) |
| Gözler | `gozler` | kırpma için scaleY; merkez (120,104) |
| Ağızlar | `agiz agiz-gulus`, `agiz-acik`, `agiz-yarim`, `agiz-o` | aynı anda yalnız biri görünür |
| Efektler | `av-ter`, `av-unlem` | ter damlası, baş üstünde ünlem çizgileri |
| Pozlar | `poz poz-isaret`, `poz-sun`, `poz-dusun` | |

Pozlar:
- `isaret`: ekranın sağındaki kol yukarı kalkar, işaret parmağı havada.
- `sun`: aynı kol açık avuçla yana uzanır (el sallama ya da sunma).
- `dusun`: ekranın solundaki kol çeneye gider.

`isaret` ve `sun` açıkken `kol-sag-dur` gizlenir, `dusun` açıkken `kol-sol-dur` gizlenir.

**Tek parmak kalkık yumruk ters anlaşılabilir.** Parmak tam ortadan çıkarsa orta parmak gibi okunur. İşaret parmağını yumruğun başa bakan kenarına koy, hafif eğ (`rotate(-8deg)`) ve boğum çizgilerini ekle.

Avatarı önce ayrı bir test sayfasında beş halde (sade, işaret+ünlem, o+ter, sun, düşün) yan yana çiz ve bir kez bak; sonra videoya geç.

### 3. Senaryo

- Uzunluk: 8–12 sahne, sahne başı 5–7 sn, toplam 45–65 sn.
- Yapı:
  - kanca (tanıdık bir soru veya cümle)
  - sorun (2–3 sahne: zaman kaybı, unutulan iş, kaçan müşteri)
  - dönüş ("İşte ben bu yüzden X'i yaptım": büyük vurgu dairesi + logo)
  - çözümün adımları (3–4 sahne)
  - kapanış (logo, teklif, alan adı)
- Anlatım birinci tekil şahısla yapılır; avatar kullanıcının kendisidir.
- Her sahnenin `data-sub` metni = seslendirme metni. Cümle başı ≤ 18 kelime. `|` ile 2–5 kelimelik öbeklere böl; yazı öbek öbek değişir.
- İşaretler: `*vurgu rengi*`, `_el yazısı_` (çoğu zaman öbeğin ilk kelimesi), `~soluk~` (olumsuz veya geride kalan şey).
- Ürün iddiaları:
  - Ürünün yapmadığı bir şeyi söyleme. Kod tabanı varsa iddiayı koddan doğrula, emin olmadıklarını kullanıcıya sor.
  - Uydurma istatistik yazma. Sayı yerine "onlarca kez" gibi ifadeler kullan.
  - Ekrandaki ad, plaka, saat gibi örnek verileri gerçekçi seç ve sahneler arasında tutarlı tut.

### 4. Animasyon

`assets/sablon.html`'i kopyala; örnek sahneleri kendi sahnelerinle değiştir. Sahne öznitelikleri şablondaki yorumda yazar:

```html
<section class="scene" data-dur="6" data-alen="" data-poz="dusun@0,dur@2.6" data-yuz="gulus" data-efekt="ter@1.4"
         data-sub="Bir oto serviste | en çok duyulan cümle: | *Usta, araba ne oldu?*">
  <div class="vis"> … sahne görseli … </div>
</section>
```

**Yerleşim** (kare 540x960, render'da 2x):

| Alan | Konum |
|---|---|
| Üst etiket | top 62 |
| Akan yazı | top 94, en çok 3 satır |
| Görsel alan `.vis` | y 236–676 |
| Avatar | sol alt, x 2–218, y 711–960 |

Görselleri avatarın üstüne taşırma. Avatarın sağındaki boşluğa (x 240–520, y 690–900) küçük bir çip ya da not konabilir.

**Zamanlama:**
- Görsel öğeler `class="a" style="--an:pop;--d:1.2s"` ile girer. Hazır keyframe'ler: rise, pop, fade, dus, slideR, stamp, buyu, yaz, soluk, titre, dalga, nabiz.
- Bir öğenin girişini, onu anlatan öbeğin ekrana geldiği ana denk getir.
- Ses yokken kelime j, `0.35 + dur*0.62*j/n` saniyesinde belirir.
- Avatar pozu da o öbekle değişsin: "ben yaptım"da `isaret`, gösterirken `sun`, sorun anlatırken `dusun` ve `ter`.

**Motor kuralları** (bozulursa render'da hata çıkar):
- **Opaklık:** `.a` ile kullanılan her keyframe `opacity:1` içermeli. Yalnız transform değiştiren keyframe öğeyi görünmez bırakır.
- **Deterministiklik:** Yazı, ağız, göz kırpma ve baş hareketi CSS geçişiyle değil, `render()` içinde t'den hesaplanır. Kare kare çizimde tüm animasyonlar duraklatılıp `currentTime` ile zamana atlanır. CSS `transition` kullanma, yalnız `@keyframes` kullan.
- **Konum:** `position:absolute` vermediğin öğe `.vis`'in tepesine yığılır; konuşma balonu gibi öğelerde unutma.
- **Sınıf adı çakışması:** Tüm sahneler tek CSS'i paylaşır. Sahneye özgü sınıflara sahne öneki ver (`.s3-takvim`).
- **Yazı yazma efekti:** `clip-path: inset(0 100% 0 0)` → `inset(0 0 0 0)` ve `steps(N)` ile yap; `width:Nch` son harfleri keser.
- **Son satır:** Oynatıcıdaki `fit();go(0);requestAnimationFrame(loop);` satırını değiştirme; betikler bu satıra kanca takar.

Birleştir ve kontrol et:

```bash
python scripts/derle.py sablon.html logo.svg avatar.svg video.html
python scripts/peek.py video.html kontrol/            # her sahne sonundan bir kare
python scripts/peek.py video.html kontrol/ 3.2 22.0   # yalnız belirli saniyeler
ffmpeg -y -loglevel error -i kontrol/peek00.png -i kontrol/peek01.png -i kontrol/peek02.png -i kontrol/peek03.png -i kontrol/peek04.png -filter_complex "hstack=5,scale=1800:-1" pA.jpg
```

Panoya bir kez bak. Kontrol listesi:
- çakışma ve taşma
- avatarla çakışan görsel
- görünmeyen öğe
- 3 satırı aşan yazı
- yanlış yazılmış marka

Yalnız sorunlu sahneleri yeniden kontrol et. Tam render yapma.

Ortam Artifact yayınlamayı destekliyorsa HTML'i oynatıcı olarak yayınla (kontroller: Duraklat, Baştan, Kayıt modu; Boşluk ve ←/→ tuşları).

### 5. Seslendirme metinlerini ver ve dur

Sahne sırasıyla şunları ver:
- Düz metinler (işaretsiz `data-sub`).
- ElevenLabs için telaffuzlu hâller: yalnız değişen satırları yaz. Model Multilingual, dil Türkçe; her cümleyi ayrı üret. Örnekler: WhatsApp → "vatsap", sayılar yazıyla ("14" → "on dört"), alan adı → "… nokta kom", kısaltmalar heceyle (SSL → "es-es-el").
- Anlatıcı kendisi olduğu için kullanıcıya şunu öner: kendi sesini telefonla sessiz bir odada kaydetmesi videoyu daha inandırıcı yapar.
- Tek bir paylaşım metni: kanca cümle, maddeli özet, CTA + alan adı, 8–10 hashtag.
- Kapak yazısı.
- Ses dosyası isteği: `ses-01.mp3 … ses-NN.mp3`.

**Sesler gelmeden MP4 render etme.** Sessiz taslak MP4 zaman ve token israfıdır; kullanıcı açıkça isterse üret.

### 6. Sesler gelince

```bash
python scripts/sure.py video.html sesler/            # data-dur / data-alen güncellenir
python scripts/peek.py video.html kontrol/           # uzayan sahnelere bir bakış
python scripts/render.py video.html sesler/ cikti.mp4 [muzik.mp3]
```

`render.py` ~60 sn video için birkaç dakika sürer; zaman aşımını uzun tut (10 dk). Çıktı 1080x1920, 30 fps, H.264 yuv420p, AAC 192k, +faststart. Müzik verilirse seslendirmenin altına %12 seviyede eklenir ve sonda 1,5 sn'de kısılır. Oynatıcı sayfası yayınlandıysa güncel sürelerle yeniden yayınla.

## Teslim

- **İlk tur:** oynatıcı bağlantısı, doğrulanması gereken ürün iddiaları (kısa liste), seslendirme metinleri (düz + telaffuzlu), paylaşım metni, kapak yazısı ve ses dosyası isteği.
- **İkinci tur:** MP4 dosyası, süre ve boyut. Süreci adım adım anlatma.
- Paylaşım önerisi: Instagram takipçi olmayanlara en çok Reels gösterir. Video Reels olarak paylaşılmalı; profesyonel hesapta "Deneme Reels" ile önce takipçi olmayanlara denenebilir.
