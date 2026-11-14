#!/usr/bin/env python3
"""hikmet_notlari kart üretici: posts/<id>.json -> cards/<id>.jpg (1080x1350)"""
import json, sys, subprocess, html, pathlib
from scenes import SCENES

ROOT = pathlib.Path(__file__).resolve().parent

THEMES = {
    "hadis":   {"label": "HADİS-İ ŞERİF",    "bg1": "#0d2b2f", "bg2": "#071a1d"},
    "ayet":    {"label": "ÂYET-İ KERÎME",    "bg1": "#10263f", "bg2": "#081526"},
    "dua":     {"label": "DUÂ VE ZİKİR",     "bg1": "#2a1d36", "bg2": "#160f1e"},
    "ilmihal": {"label": "İLMİHÂL · HANEFÎ", "bg1": "#33201a", "bg2": "#1b100c"},
}

# Renk paletleri: her gönderi posts/<id>.json içinde "palette" ile kendi rengini seçer.
# bg1/bg2: zemin, accent: altın/vurgu, accent2: desen, text: metin, shade: kapak üst gölgesi
PALETTES = {
    "zumrut":   {"bg1": "#0d2b2f", "bg2": "#071a1d", "accent": "#c9a45c", "accent2": "#e9c97a", "text": "#efe4c8", "shade": "#071820"},
    "gece":     {"bg1": "#10263f", "bg2": "#081526", "accent": "#c9a45c", "accent2": "#e9c97a", "text": "#efe4c8", "shade": "#081526"},
    "seher":    {"bg1": "#3e2436", "bg2": "#1e1019", "accent": "#e3b48c", "accent2": "#f2c9a6", "text": "#f6e6dc", "shade": "#24152a"},
    "bordo":    {"bg1": "#3d1420", "bg2": "#1f0a10", "accent": "#d9b26a", "accent2": "#ecc988", "text": "#f3e3cf", "shade": "#1f0a10"},
    "erguvan":  {"bg1": "#2c1d3a", "bg2": "#150e1e", "accent": "#d4b37a", "accent2": "#e6cc98", "text": "#efe4d6", "shade": "#150e1e"},
    "firuze":   {"bg1": "#0f3b42", "bg2": "#06201f", "accent": "#e6c27a", "accent2": "#9fd8d2", "text": "#eaf2ec", "shade": "#06201f"},
    "toprak":   {"bg1": "#36221a", "bg2": "#1b100c", "accent": "#d8a866", "accent2": "#eec48a", "text": "#f1e4d2", "shade": "#1b100c"},
    "zeytin":   {"bg1": "#2c301a", "bg2": "#15170c", "accent": "#d6c07a", "accent2": "#e8d79a", "text": "#f0ecd6", "shade": "#15170c"},
    "lacivert": {"bg1": "#16244a", "bg2": "#0a1128", "accent": "#c9d2e3", "accent2": "#dfe6f2", "text": "#eef1f7", "shade": "#0a1128"},
}
DEFAULT_PALETTE = {"hadis": "zumrut", "ayet": "gece", "dua": "erguvan", "ilmihal": "toprak"}


def _rgb(h):
    h = h.lstrip("#"); return ",".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))


def recolor(doc, post):
    """Şablondaki varsayılan (zümrüt) renkleri gönderinin paletiyle değiştirir."""
    p = PALETTES[post.get("palette") or DEFAULT_PALETTE[post["type"]]]
    for old, new in [("#c9a45c", p["accent"]), ("rgba(201,164,92,", f"rgba({_rgb(p['accent'])},"),
                     ("#e9c97a", p["accent2"]), ("#efe4c8", p["text"]), ("#071820", p["shade"]),
                     ("#0d2b2f", p["bg1"]), ("#071a1d", p["bg2"]), ("#10263f", p["bg1"]), ("#081526", p["bg2"]),
                     ("#2a1d36", p["bg1"]), ("#160f1e", p["bg2"]), ("#33201a", p["bg1"]), ("#1b100c", p["bg2"])]:
        doc = doc.replace(old, new)
    return doc

STAR = "M50 0 L61.8 21.5 L85.4 14.6 L78.5 38.2 L100 50 L78.5 61.8 L85.4 85.4 L61.8 78.5 L50 100 L38.2 78.5 L14.6 85.4 L21.5 61.8 L0 50 L21.5 38.2 L14.6 14.6 L38.2 21.5 Z"

def star(x, y, s, fill="none", stroke="#c9a45c", sw=1.2):
    return (f'<svg class="orn" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px" viewBox="-4 -4 108 108">'
            f'<path d="{STAR}" fill="{fill}" stroke="{stroke}" stroke-width="{sw*100/s*1.0:.2f}"/>'
            f'<circle cx="50" cy="50" r="14" fill="none" stroke="{stroke}" stroke-width="{sw*100/s:.2f}"/></svg>')

def build(post):
    t = THEMES[post["type"]]
    ar = html.escape(post.get("arabic", ""))
    tr = html.escape(post["turkish"]).replace("\n", "<br>")
    src = html.escape(post["source"])
    ar_size = post.get("ar_size", 44)
    tr_size = post.get("tr_size", 33)
    W, H = 1080, 1350
    corners = "".join(star(x, y, 46) for x, y in [(37, 37), (W-83, 37), (37, H-83), (W-83, H-83)])
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<link rel="stylesheet" href="{ROOT}/fonts/fonts.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px}}
body{{background:radial-gradient(ellipse at 50% 40%, {t['bg1']} 0%, {t['bg2']} 100%);position:relative;overflow:hidden;color:#f1e7cf}}
.pattern{{position:absolute;inset:0;opacity:.07}}
.frame{{position:absolute;inset:60px;border:1.5px solid #c9a45c}}
.frame2{{position:absolute;inset:72px;border:.8px solid rgba(201,164,92,.55)}}
.orn{{position:absolute}}
.content{{position:absolute;inset:120px 130px 150px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
.label{{font:600 20px 'Inter';letter-spacing:.32em;color:#c9a45c;display:flex;align-items:center;gap:22px;margin-bottom:54px}}
.label i{{display:block;width:70px;height:1px;background:linear-gradient(90deg,transparent,#c9a45c)}}
.label i:last-child{{transform:scaleX(-1)}}
.ar{{font:400 {ar_size}px/1.95 'Amiri';direction:rtl;color:#f6eedb}}
.div{{margin:40px 0 38px;display:flex;align-items:center;gap:16px}}
.div i{{width:120px;height:1px;background:linear-gradient(90deg,transparent,#c9a45c)}}
.div i:last-child{{transform:scaleX(-1)}}
.div svg{{width:26px;height:26px}}
.tr{{font:500 {tr_size}px/1.5 'Cormorant Garamond';color:#efe4c8}}
.src{{margin-top:36px;font:italic 600 26px 'Cormorant Garamond';color:#c9a45c}}
.handle{{position:absolute;bottom:92px;left:0;right:0;text-align:center;font:500 19px 'Inter';letter-spacing:.18em;color:rgba(201,164,92,.85)}}
</style></head><body>
<svg class="pattern" width="{W}" height="{H}"><defs><pattern id="p" width="90" height="90" patternUnits="userSpaceOnUse">
<g transform="translate(5 5) scale(.8)"><path d="{STAR}" fill="none" stroke="#e9c97a" stroke-width="2"/></g>
<rect x="38" y="38" width="14" height="14" transform="rotate(45 45 45)" fill="none" stroke="#e9c97a" stroke-width="1.4"/>
</pattern></defs><rect width="100%" height="100%" fill="url(#p)"/></svg>
<div class="frame"></div><div class="frame2"></div>{corners}
<div class="content">
 <div class="label"><i></i>{t['label']}<i></i></div>
 {'<div class="ar">'+ar+'</div><div class="div"><i></i><svg viewBox="-4 -4 108 108"><path d="'+STAR+'" fill="#c9a45c"/></svg><i></i></div>' if ar else ''}
 <div class="tr">{tr}</div>
 <div class="src">{src}</div>
</div>
<div class="handle">@HIKMET_NOTLARI</div>
</body></html>"""

def build_cover(post, slide):
    t = THEMES[post["type"]]
    svg = SCENES[slide["scene"]]()
    title = html.escape(slide["title"])
    sub = html.escape(slide.get("subtitle", ""))
    W, H = 1080, 1350
    corners = "".join(star(x, y, 46) for x, y in [(37, 37), (W-83, 37), (37, H-83), (W-83, H-83)])
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<link rel="stylesheet" href="{ROOT}/fonts/fonts.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#06100f;position:relative}}
.scene{{position:absolute;inset:0}}
.shade{{position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(#071820ee,#07182000)}}
.frame{{position:absolute;inset:60px;border:1.5px solid #c9a45c}}
.frame2{{position:absolute;inset:72px;border:.8px solid rgba(201,164,92,.55)}}
.orn{{position:absolute}}
.top{{position:absolute;top:150px;left:120px;right:120px;text-align:center}}
.label{{font:600 20px 'Inter';letter-spacing:.32em;color:#c9a45c;display:flex;align-items:center;justify-content:center;gap:22px;margin-bottom:30px}}
.label i{{display:block;width:70px;height:1px;background:linear-gradient(90deg,transparent,#c9a45c)}}
.label i:last-child{{transform:scaleX(-1)}}
.title{{font:600 84px/1.05 'Cormorant Garamond';color:#f6ecd4;text-shadow:0 2px 20px #000a}}
.sub{{margin-top:22px;font:italic 500 34px/1.3 'Cormorant Garamond';color:#e2cf9f}}
.bottom{{position:absolute;bottom:96px;left:0;right:0;text-align:center;font:500 19px 'Inter';letter-spacing:.18em;color:rgba(201,164,92,.9)}}
.swipe{{position:absolute;bottom:150px;left:0;right:0;text-align:center;font:500 22px 'Inter';letter-spacing:.12em;color:#efe4c8;opacity:.85}}
</style></head><body>
<div class="scene">{svg}</div><div class="shade"></div>
<div class="frame"></div><div class="frame2"></div>{corners}
<div class="top"><div class="label"><i></i>{t['label']}<i></i></div>
<div class="title">{title}</div>{'<div class="sub">'+sub+'</div>' if sub else ''}</div>
<div class="swipe">{html.escape(slide.get("swipe","Kaydır →"))}</div>
<div class="bottom">@HIKMET_NOTLARI</div>
</body></html>"""

def build_photo(post, slide):
    """Fotoğraflı kapak: tam ekran fotoğraf, okunurluk için gölge, altın çerçeve, başlık ve fotoğraf künyesi."""
    t = THEMES[post["type"]]
    img = (ROOT / slide["photo"]).resolve()
    title = html.escape(slide["title"])
    sub = html.escape(slide.get("subtitle", ""))
    credit = html.escape(slide.get("credit", ""))
    pos = slide.get("focus", "center")
    W, H = 1080, 1350
    corners = "".join(star(x, y, 46) for x, y in [(37, 37), (W-83, 37), (37, H-83), (W-83, H-83)])
    return f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<link rel="stylesheet" href="{ROOT}/fonts/fonts.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#071820;position:relative}}
.photo{{position:absolute;inset:0;background:url('file://{img}') {pos}/cover no-repeat;filter:saturate(.92) contrast(1.03)}}
.tint{{position:absolute;inset:0;background:linear-gradient(180deg,#071820e6 0%,#07182099 22%,#07182000 45%,#07182000 62%,#071820cc 84%,#071820f2 100%)}}
.frame{{position:absolute;inset:60px;border:1.5px solid #c9a45c}}
.frame2{{position:absolute;inset:72px;border:.8px solid rgba(201,164,92,.55)}}
.orn{{position:absolute}}
.top{{position:absolute;top:150px;left:120px;right:120px;text-align:center}}
.label{{font:600 20px 'Inter';letter-spacing:.32em;color:#c9a45c;display:flex;align-items:center;justify-content:center;gap:22px;margin-bottom:30px}}
.label i{{display:block;width:70px;height:1px;background:linear-gradient(90deg,transparent,#c9a45c)}}
.label i:last-child{{transform:scaleX(-1)}}
.title{{font:600 84px/1.05 'Cormorant Garamond';color:#f8f0dc;text-shadow:0 2px 24px #000c}}
.sub{{margin-top:22px;font:italic 500 34px/1.3 'Cormorant Garamond';color:#efdcae;text-shadow:0 1px 12px #000c}}
.swipe{{position:absolute;bottom:150px;left:0;right:0;text-align:center;font:500 22px 'Inter';letter-spacing:.12em;color:#f3ead6}}
.bottom{{position:absolute;bottom:96px;left:0;right:0;text-align:center;font:500 19px 'Inter';letter-spacing:.18em;color:rgba(201,164,92,.95)}}
.credit{{position:absolute;bottom:22px;right:90px;font:400 15px 'Inter';color:#ffffffaa;letter-spacing:.02em}}
</style></head><body>
<div class="photo"></div><div class="tint"></div>
<div class="frame"></div><div class="frame2"></div>{corners}
<div class="top"><div class="label"><i></i>{t['label']}<i></i></div>
<div class="title">{title}</div>{'<div class="sub">'+sub+'</div>' if sub else ''}</div>
<div class="swipe">{html.escape(slide.get("swipe","Kaydır →"))}</div>
<div class="bottom">@HIKMET_NOTLARI</div>
{'<div class="credit">'+credit+'</div>' if credit else ''}
</body></html>"""


JS = """
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:+(process.argv[4]||1080),height:+(process.argv[5]||1350)},deviceScaleFactor:1});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const o=await p.evaluate(()=>{const c=document.querySelector('.content');return !!c && c.scrollHeight>c.clientHeight+2});
await p.screenshot({path:process.argv[3],type:'jpeg',quality:92});await b.close();if(o)console.log('UYARI: metin taşıyor');})();
"""

def main(pid):
    post = json.loads((ROOT / "posts" / f"{pid}.json").read_text())
    js = ROOT / "templates" / "shot.js"
    js.write_text(JS)
    slides = post.get("slides") or [{"kind": "text"}]
    for i, sl in enumerate(slides, 1):
        name = pid if len(slides) == 1 else f"{pid}-{i}"
        doc = (build_cover(post, sl) if sl["kind"] == "cover" else
               build_photo(post, sl) if sl["kind"] == "photo" else build({**post, **sl}))
        doc = recolor(doc, post)
        h = ROOT / "templates" / f"{name}.html"
        h.write_text(doc)
        out = ROOT / "cards" / f"{name}.jpg"
        subprocess.run(["node", str(js), str(h), str(out)], check=True)
        print(out)

if __name__ == "__main__":
    main(sys.argv[1])
