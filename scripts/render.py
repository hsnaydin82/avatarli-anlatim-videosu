"""Kareleri 1080x1920 / 30 fps çizer, sesleri sahne başlarına yerleştirip sesli MP4 üretir.
Önce sure.py çalıştırılmış olmalı.
Kullanım: python render.py <video.html> <ses_klasoru> <cikti.mp4> [muzik.mp3]"""
import asyncio
import math
import pathlib
import shutil
import subprocess
import sys
import tempfile

from playwright.async_api import async_playwright
from ortak import render_html, ses_dosyasi

FPS = 30
kaynak, ses, cikti = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
muzik = pathlib.Path(sys.argv[4]) if len(sys.argv) > 4 else None
is_klasoru = pathlib.Path(tempfile.mkdtemp(prefix="anlatim-"))
kare = is_klasoru / "frames"
kare.mkdir()
sureler = render_html(kaynak, is_klasoru / "render.html")


async def kareler():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        pg.on("pageerror", lambda e: print("pageerror", e))
        await pg.goto((is_klasoru / "render.html").as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(1500)
        n = math.ceil(await pg.evaluate("window.__total") * FPS)
        for f in range(n):
            await pg.evaluate(f"window.__seek({f / FPS})")
            await pg.screenshot(path=str(kare / f"{f:05d}.jpg"), type="jpeg", quality=95)
            if f % 300 == 0:
                print("kare", f, "/", n, flush=True)
        await b.close()
    return n


n = asyncio.run(kareler())
girdi, filtre, etiket, bas = [], [], [], 0.0
for i, d in enumerate(sureler):
    girdi += ["-i", str(ses_dosyasi(ses, i + 1))]
    ms = round((bas + .3) * 1000)
    filtre.append(f"[{i + 1}:a]aresample=48000,adelay={ms}|{ms}[a{i}]")
    etiket.append(f"[a{i}]")
    bas += d
adet = len(sureler)
if muzik:
    girdi += ["-i", str(muzik)]
    filtre.append(f"[{adet + 1}:a]aresample=48000,volume=0.12,atrim=0:{bas:.2f},afade=t=out:st={max(0, bas - 1.5):.2f}:d=1.5[m]")
    etiket.append("[m]")
    adet += 1
fc = ";".join(filtre) + ";" + "".join(etiket) + f"amix=inputs={adet}:normalize=0,apad[aout]"
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(kare / "%05d.jpg"), *girdi,
                       "-filter_complex", fc, "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(cikti)])
shutil.rmtree(is_klasoru, ignore_errors=True)
print("BITTI", cikti, n, "kare", round(cikti.stat().st_size / 1048576, 1), "MB")
