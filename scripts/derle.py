"""Şablonu, logo sembolünü ve avatar SVG'sini tek HTML dosyasında birleştirir.
Kullanım: python derle.py <sablon.html> <logo.svg> <avatar.svg> <cikti.html>"""
import pathlib
import sys

sablon, logo, avatar, cikti = map(pathlib.Path, sys.argv[1:5])
s = sablon.read_text(encoding="utf-8")
for yer, dosya in (("<!--LOGO-->", logo), ("<!--AVATAR-->", avatar)):
    if yer not in s:
        sys.exit(f"{yer} yer tutucusu şablonda yok")
    s = s.replace(yer, dosya.read_text(encoding="utf-8").rstrip())
cikti.write_text(s, encoding="utf-8", newline="\n")
print("yazildi", cikti, len(s), "karakter")
