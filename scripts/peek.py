"""Ucuz görsel kontrol: her sahnenin bitişinden 0,4 sn önce (ya da verilen saniyelerde) 540x960 kare alır.
Kullanım: python peek.py <video.html> <cikti_klasoru> [saniye ...]"""
import asyncio
import pathlib
import sys

from playwright.async_api import async_playwright
from ortak import render_html

kaynak, klasor = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
klasor.mkdir(parents=True, exist_ok=True)
noktalar = [float(x) for x in sys.argv[3:]]
sureler = render_html(kaynak, klasor / "render.html")
if not noktalar:
    bas = 0
    for d in sureler:
        noktalar.append(bas + d - .4)
        bas += d


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=1)
        pg.on("console", lambda m: print("console", m.type, m.text) if m.type in ("error", "warning") else None)
        pg.on("pageerror", lambda e: print("pageerror", e))
        await pg.goto((klasor / "render.html").as_uri())
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(1500)
        for i, z in enumerate(noktalar):
            await pg.evaluate(f"window.__seek({z})")
            await pg.wait_for_timeout(60)
            await pg.screenshot(path=str(klasor / f"peek{i:02d}.png"))
        await b.close()
    print("toplam", round(sum(sureler), 2), "sn,", len(noktalar), "kare")


asyncio.run(main())
