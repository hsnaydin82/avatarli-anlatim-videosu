"""Ses dosyalarının süresini ölçüp sahnelerin data-dur / data-alen değerlerini günceller.
Ses sahne başından 0,3 sn sonra başlar; sahne süresi = max(mevcut, 0,3 + ses + 0,5).
Kullanım: python sure.py <video.html> <ses_klasoru>   (dosyalar: ses-01.mp3, ses-02.mp3 ...)"""
import pathlib
import re
import subprocess
import sys

from ortak import ses_dosyasi

html_yolu, ses = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
html = html_yolu.read_text(encoding="utf-8")
parcalar, son = [], 0
for i, m in enumerate(re.finditer(r'<section class="scene"[^>]*>', html), 1):
    etiket = m.group(0)
    al = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                        "-of", "csv=p=0", str(ses_dosyasi(ses, i))]).decode().strip())
    dur = float(re.search(r'data-dur="([\d.]+)"', etiket).group(1))
    yeni = max(dur, round(.3 + al + .5, 2))
    etiket = re.sub(r'data-dur="[\d.]+"', f'data-dur="{yeni}"', etiket)
    etiket = re.sub(r'data-alen="[\d.]*"', f'data-alen="{al:.2f}"', etiket)
    parcalar += [html[son:m.start()], etiket]
    son = m.end()
    print(f"sahne {i}: ses {al:.2f} sn, süre {dur} -> {yeni}")
parcalar.append(html[son:])
html_yolu.write_text("".join(parcalar), encoding="utf-8", newline="\n")
