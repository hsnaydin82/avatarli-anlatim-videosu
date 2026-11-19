import pathlib
import re

# Oynatıcıyı durdurup dışarıdan zamana atlamayı sağlayan kanca (kare kare çizim için)
KANCA = """window.__seek=function(g){let i=0;while(i<durs.length-1&&g>=durs[i]){g-=durs[i];i++}
 if(i!==idx||!window.__shown){idx=i;show(i);window.__shown=true}
 t=Math.min(g,durs[i]);render();
 document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});};
window.__total=total;
document.body.classList.add('rec');fit();go(0);setPlay(false);"""
ANA = "fit();go(0);requestAnimationFrame(loop);"


def render_html(kaynak: pathlib.Path, hedef: pathlib.Path):
    """Kaynak sayfaya zaman atlama kancası ekleyip tam belge olarak yazar; sahne sürelerini döner."""
    html = kaynak.read_text(encoding="utf-8")
    if ANA not in html:
        raise SystemExit("Oynatıcı başlangıç satırı bulunamadı: " + ANA)
    hedef.write_text(
        '<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head><body>'
        + html.replace(ANA, KANCA) + "</body></html>", encoding="utf-8")
    return [float(x) for x in re.findall(r'<section class="scene"[^>]*?data-dur="([\d.]+)"', html)]


def ses_dosyasi(klasor: pathlib.Path, no: int) -> pathlib.Path:
    """ses-01.mp3 / ses-1.mp3 (yüklemede önek almış olabilir: *-ses-01.mp3)."""
    adaylar = sorted(klasor.glob(f"*ses-{no:02d}.mp3")) or sorted(klasor.glob(f"*ses-{no}.mp3"))
    if not adaylar:
        raise SystemExit(f"ses-{no:02d}.mp3 bulunamadı: {klasor}")
    return adaylar[0]
