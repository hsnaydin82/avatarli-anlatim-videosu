# avatarli-anlatim-videosu

Claude Code için bir skill. Konuşan çizgi film avatarı olan dikey (9:16) anlatım videoları üretir. Videolar Reels, TikTok ve Shorts için uygundur.

- Avatar sol altta durur; konuşurken ağzı oynar, göz kırpar, parmakla gösterir, el sallar, düşünür.
- Yazı sol üstte, seslendirmeyle eşzamanlı olarak kelime kelime akar.
- Ortada her sahneye özel animasyonlu görsel vardır.
- Video HTML olarak yazılır, tarayıcıda kare kare çizilir ve ffmpeg ile sesli MP4'e çevrilir.

## Kurulum

```bash
# klasörü ~/.claude/skills/ altına kopyalayın
git clone <bu-depo> ~/.claude/skills/avatarli-anlatim-videosu

pip install playwright
playwright install chromium
# ffmpeg ve ffprobe PATH'te olmalı
```

## Kullanım

Claude Code'da şöyle yazın:

> Ürünümü anlatan avatarlı bir Reels videosu yap. Referans video `ref.mp4`, avatar için `foto.jpg`.

Skill şu sırayla çalışır:
1. Referansı inceler.
2. Fotoğraftan SVG avatar çizer. Fotoğraf hiçbir dış servise gönderilmez.
3. Senaryoyu ve animasyonu yazar.
4. Seslendirme metinlerini verir ve sizden ses dosyalarını ister.
5. `ses-01.mp3 …` dosyaları gelince MP4'ü üretir.

Betikler elle de çalıştırılabilir:

```bash
python scripts/derle.py assets/sablon.html assets/logo-ornek.svg assets/avatar.svg video.html
python scripts/peek.py video.html kontrol/
python scripts/sure.py video.html sesler/
python scripts/render.py video.html sesler/ cikti.mp4 [muzik.mp3]
```

## Dosyalar

| Dosya | İçerik |
|---|---|
| `SKILL.md` | Claude'un izlediği yönerge |
| `assets/sablon.html` | Oynatıcı motoru ve örnek üç sahne |
| `assets/avatar.svg` | Örnek avatar. Yeni kişi için aynı parça yapısıyla yeniden çizilir |
| `assets/logo-ornek.svg` | Logo sembolü örneği |
| `scripts/` | Birleştirme, kontrol karesi, ses süresi eşitleme ve MP4 çıktısı |

Fontlar (Inter Tight, Instrument Serif, JetBrains Mono) Google Fonts'tan yüklenir. Render sırasında internet bağlantısı gerekir.
