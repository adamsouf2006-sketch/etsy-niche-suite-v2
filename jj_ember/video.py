# Vidéo de fiche : 1080x1080, 30 i/s, 13 s, HTML piloté par seek(t), capturé par Chromium puis encodé par ffmpeg.
# Usage : python3 video.py [produit ...]
import os, sys, asyncio, json, shutil, subprocess
from playwright.async_api import async_playwright
import pages as P
import build as B
import photos as PH

H = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(H, "out")
FPS, DUR = 30, 13.0

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>__FONTS__
*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1080px;overflow:hidden;background:#EFE3CC;color:#33241A}
.abs{position:absolute}.fell{font-family:'IM Fell English',serif}.sc{font-family:'IM Fell English SC',serif}.cor{font-family:'Cormorant Garamond',serif}
.pg{position:absolute;width:300px;box-shadow:0 10px 24px rgba(40,25,15,.35);border-radius:2px}
</style></head><body>
<div class="abs" style="inset:0;background:url(__BG__) center/cover"></div><div class="abs" style="inset:0;background:rgba(244,234,214,.5)"></div>
<div id="s1" class="abs" style="inset:0">
  <div id="t1" class="abs sc" style="left:0;right:0;top:70px;text-align:center;font-size:84px;line-height:1.02">__TITLE__</div>
  <div id="t2" class="abs cor" style="left:0;right:0;top:__SUBTOP__px;text-align:center;font-size:40px;font-style:italic;color:#9A4A24">__SUB__</div>
  <div id="hero" class="abs" style="left:0;right:0;top:0;bottom:0"><div style="position:absolute;inset:0;transform:translateY(-40px) scale(.8);transform-origin:50% 30%">__HERO__</div></div>
  <div id="badge" class="abs" style="left:820px;top:330px;width:200px;height:200px;border-radius:50%;background:#9A4A24;color:#F4EAD6;display:flex;flex-direction:column;align-items:center;justify-content:center;border:5px double #F4EAD6;box-shadow:0 8px 20px rgba(0,0,0,.3)"><div class="fell" style="font-size:76px;line-height:1">__NUM__</div><div class="sc" style="font-size:24px">__UNIT__</div></div>
</div>
<div id="s2" class="abs" style="inset:0;opacity:0"><div class="abs" style="inset:0;background:rgba(244,234,214,.5)"></div>__GRID__<div class="abs sc" style="left:0;right:0;bottom:40px;text-align:center;font-size:52px;text-shadow:0 0 18px #F4EAD6">__COUNT__</div></div>
<div id="s3" class="abs" style="inset:0;opacity:0;overflow:hidden"><img id="zoom" src="__ZOOM__" class="abs" style="left:0;top:0;width:1080px;transform-origin:__ZORIGIN__">
  <div class="abs" style="left:0;right:0;bottom:0;height:200px;background:linear-gradient(transparent,rgba(30,18,10,.8))"></div>
  <div id="zt" class="abs sc" style="left:0;right:0;bottom:50px;text-align:center;font-size:52px;color:#F4EAD6">Rich, print-ready detail</div></div>
<div id="s4" class="abs" style="inset:0;opacity:0"><div class="abs" style="inset:0;background:rgba(244,234,214,.72)"></div>
  <div class="abs sc" style="left:0;right:0;top:120px;text-align:center;font-size:66px">Print at home</div>
  <div id="f1" class="abs" style="left:110px;top:300px;width:400px;height:420px;background:#F6EEDC;border:3px solid #8a6a4a;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="sc" style="font-size:58px">US Letter</div><div class="cor" style="font-size:38px">8.5 x 11 in</div></div>
  <div id="f2" class="abs" style="left:570px;top:300px;width:400px;height:420px;background:#F6EEDC;border:3px solid #8a6a4a;display:flex;flex-direction:column;align-items:center;justify-content:center"><div class="sc" style="font-size:58px">A4</div><div class="cor" style="font-size:38px">210 x 297 mm</div></div>
  <div id="f3" class="abs cor" style="left:0;right:0;top:790px;text-align:center;font-size:44px">Printable PDF &#183; high resolution &#183; instant download</div></div>
<div id="s5" class="abs" style="inset:0;opacity:0"><div class="abs" style="inset:0;background:rgba(244,234,214,.72)"></div>
  __ARGS__
  <div id="shop" class="abs" style="left:0;right:0;top:820px;text-align:center"><div class="sc" style="font-size:40px;color:#9A4A24;letter-spacing:.12em">The Ember &amp; Oak Collection</div><div class="fell" style="font-size:76px">Oakfold</div></div></div>
<script>
const E = (t) => t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3);                  // easeOutCubic
const IO = (t) => t < 0 ? 0 : t > 1 ? 1 : t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
const BACK = (t) => { t = Math.min(Math.max(t, 0), 1); const c = 1.7; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
const $ = (i) => document.getElementById(i);
const fade = (t, a, b, d = .35) => Math.min(E((t - a) / d), 1 - E((t - b + d) / d));
window.seek = (t) => {
  $('s1').style.opacity = fade(t, -1, 3.0);
  $('t1').style.transform = `translateY(${(1 - E(t / .6)) * -40}px)`; $('t1').style.opacity = E((t + .25) / .5);
  $('t2').style.opacity = E((t - .3) / .5);
  $('hero').style.transform = `translateY(${(1 - E((t - .1) / .9)) * 120}px) scale(${1 + t * .015})`; $('hero').style.opacity = E((t + .35) / .5);
  $('badge').style.transform = `scale(${BACK((t - .8) / .5)})`;
  $('s2').style.opacity = fade(t, 2.7, 5.6);
  document.querySelectorAll('.cell').forEach((c, i) => { const k = E((t - 2.8 - i * .08) / .4); c.style.opacity = k; c.style.transform = `translateY(${(1 - k) * 60}px)`; });
  $('s2').style.transform = `translateX(${-IO((t - 4) / 1.6) * 60}px)`;
  $('s3').style.opacity = fade(t, 5.3, 8.9);
  $('zoom').style.transform = `scale(${1.15 + IO((t - 5.3) / 3.6) * 1.1})`;
  $('zt').style.opacity = E((t - 6) / .5);
  $('s4').style.opacity = fade(t, 8.6, 11.0);
  $('f1').style.transform = `translateX(${(1 - E((t - 8.8) / .6)) * -700}px)`;
  $('f2').style.transform = `translateX(${(1 - E((t - 9.0) / .6)) * 700}px)`;
  $('f3').style.opacity = E((t - 9.5) / .5);
  $('s5').style.opacity = fade(t, 10.7, 99);
  document.querySelectorAll('.arg').forEach((a, i) => { const k = E((t - 10.9 - i * .25) / .5); a.style.opacity = k; a.style.transform = `translateY(${(1 - k) * 40}px)`; });
  $('shop').style.opacity = E((t - 11.9) / .5);
};
</script></body></html>"""

ARGS = {"kit": ["124 matching pieces", "Envelopes, pockets &amp; cards", "Papers &amp; cut-apart ephemera"],
        "papers": ["20 coordinated papers", "Botanicals, patterns &amp; solids", "Full bleed, high resolution"],
        "envelopes": ["20 pieces to cut &amp; fold", "Solid line cut, dashed line fold", "Fits 2.5 x 3.5 in cards"],
        "cards": ["62 journaling cards", "Illustrated &amp; lined", "True size on both papers"]}

def html(key):
    info = PH.PHOTO[key]; t = PH.thumbs(key); c = PH.CUT.get(key) or {}
    s = 1080 / 2000   # même zone produit que la photo principale, réduite
    hero = PH.hero(key, info, t).replace("px", "PX")
    import re
    hero = re.sub(r"(-?\d+(?:\.\d+)?)PX", lambda m: f"{float(m.group(1)) * s:.1f}px", hero)
    pages_ = t[2:]; n = min(len(pages_), 12); cols = 4; w = 210
    grid = "".join(f'<img class="pg cell" src="{u}" style="left:{90 + (i % cols) * 235}px;top:{60 + (i // cols) * 290}px;width:{w}px">' for i, u in enumerate(pages_[:n]))
    zf = sorted(os.listdir(os.path.join(OUT, key, "pages_letter")))[info["zoom"]]
    args = "".join(f'<div class="arg abs sc" style="left:0;right:0;top:{170 + i * 170}px;text-align:center;font-size:62px">{a}</div>' for i, a in enumerate(ARGS[key]))
    count = {"kit": "124 pieces", "papers": "20 papers", "envelopes": "12 templates", "cards": "62 cards"}[key]
    return (TEMPLATE.replace("__FONTS__", P.FONT_CSS).replace("__BG__", P.art("p19_tea_stained_plain"))
            .replace("__TITLE__", info["title"]).replace("__SUB__", info["sub"]).replace("__SUBTOP__", str(70 + info["tl"] * 88 + 10))
            .replace("__HERO__", hero).replace("__NUM__", info["num"]).replace("__UNIT__", info["unit"])
            .replace("__GRID__", grid).replace("__COUNT__", count)
            .replace("__ZOOM__", "file://" + os.path.join(OUT, key, "pages_letter", zf)).replace("__ZORIGIN__", info.get("zpos", "40% 35%"))
            .replace("__ARGS__", args))

async def frames(key, d):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=B.CHROME)
        pg = await b.new_page(viewport={"width": 1080, "height": 1080})
        tmp = os.path.join(d, "v.html"); open(tmp, "w").write(html(key))
        await pg.goto("file://" + tmp); await pg.wait_for_load_state("networkidle"); await pg.evaluate("document.fonts.ready")
        for i in range(int(FPS * DUR)):
            await pg.evaluate(f"seek({i / FPS})")
            await pg.screenshot(path=os.path.join(d, f"f{i:04d}.jpg"), type="jpeg", quality=92)
        await b.close()

def run(key):
    if key != "papers" and key not in PH.CUT: PH.CUT[key] = PH.cutouts(key)
    d = os.path.join(OUT, key, "vframes"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    asyncio.run(frames(key, d))
    out = os.path.join(OUT, key, "video.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(d, "f%04d.jpg"),
                    "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-shortest",
                    "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart",
                    "-c:a", "aac", "-b:a", "64k", out], check=True)
    print(key, "video", round(os.path.getsize(out) / 1e6, 2), "Mo", flush=True)

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(PH.PHOTO)): run(k)
