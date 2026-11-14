#!/usr/bin/env python3
"""Profil resmi seçenekleri: profile/profil-<n>.jpg (1080x1080, daire kırpmaya uygun)"""
import pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from render import STAR, JS

def star_poly(r_out, r_in, n=8, rot=0):
    import math
    pts = []
    for i in range(2*n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi*i/n + rot
        pts.append(f"{540+r*math.sin(a):.1f},{540-r*math.cos(a):.1f}")
    return " ".join(pts)

def page(inner, bg="radial-gradient(circle at 50% 45%, #134046 0%, #08201f 70%, #051414 100%)"):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{ROOT}/fonts/fonts.css">
<style>*{{margin:0}}html,body{{width:1080px;height:1080px;overflow:hidden;background:{bg}}}
.ar{{font-family:'Amiri';font-weight:700}} .lat{{font-family:'Cormorant Garamond'}}</style></head>
<body><svg width="1080" height="1080" viewBox="0 0 1080 1080">
<defs><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#f3d48c"/><stop offset=".5" stop-color="#c9a24f"/><stop offset="1" stop-color="#e9c776"/></linearGradient>
<pattern id="p" width="90" height="90" patternUnits="userSpaceOnUse">
<g transform="translate(5 5) scale(.8)"><path d="{STAR}" fill="none" stroke="#e9c97a" stroke-width="2"/></g></pattern></defs>
{inner}</svg></body></html>"""

# 1) Sekiz köşeli yıldız (Rub'u'l-Hizb) içinde Osmanlıca "حكمت"
v1 = f"""
<rect width="1080" height="1080" fill="url(#p)" opacity=".06"/>
<polygon points="{star_poly(430, 330)}" fill="none" stroke="url(#gold)" stroke-width="10" stroke-linejoin="round"/>
<polygon points="{star_poly(400, 308)}" fill="#0b2a2c" stroke="url(#gold)" stroke-width="3" stroke-linejoin="round"/>
<circle cx="540" cy="540" r="262" fill="none" stroke="url(#gold)" stroke-width="3" opacity=".8"/>
<text x="540" y="600" text-anchor="middle" class="ar" font-size="250" fill="url(#gold)">حكمت</text>
"""

# 2) Açık kitap üzerinde kandil ışığı + yazı
v2 = f"""
<rect width="1080" height="1080" fill="url(#p)" opacity=".06"/>
<circle cx="540" cy="540" r="470" fill="none" stroke="url(#gold)" stroke-width="6"/>
<circle cx="540" cy="540" r="448" fill="none" stroke="url(#gold)" stroke-width="2" opacity=".6"/>
<radialGradient id="glow"><stop offset="0" stop-color="#ffd58a" stop-opacity=".7"/><stop offset="1" stop-color="#ffd58a" stop-opacity="0"/></radialGradient>
<circle cx="540" cy="360" r="210" fill="url(#glow)"/>
<path d="M540 250 C 585 300 590 345 540 400 C 490 345 495 300 540 250 Z" fill="url(#gold)"/>
<path d="M540 300 C 560 325 560 350 540 375 C 520 350 520 325 540 300 Z" fill="#fff3d1"/>
<path d="M240 560 Q 390 500 540 560 Q 690 500 840 560 L 840 720 Q 690 660 540 720 Q 390 660 240 720 Z" fill="#f2e3bf"/>
<path d="M540 560 V720" stroke="#a9874a" stroke-width="5"/>
<g stroke="#b99a5d" stroke-width="5" stroke-linecap="round" opacity=".7">
<path d="M290 590 Q 400 555 500 590"/><path d="M290 630 Q 400 595 500 630"/><path d="M290 670 Q 400 635 500 670"/>
<path d="M580 590 Q 680 555 790 590"/><path d="M580 630 Q 680 595 790 630"/><path d="M580 670 Q 680 635 790 670"/></g>
<path d="M240 720 Q 390 660 540 720 Q 690 660 840 720 L 840 740 Q 690 680 540 740 Q 390 680 240 740 Z" fill="url(#gold)"/>
<text x="540" y="860" text-anchor="middle" class="lat" font-size="84" font-weight="600" fill="url(#gold)" letter-spacing="6">hikmet</text>
"""

# 3) Modern monogram: geometrik halka + büyük "ح"
import math
rays = "".join(f'<line x1="{540+300*math.cos(a):.1f}" y1="{540+300*math.sin(a):.1f}" x2="{540+345*math.cos(a):.1f}" y2="{540+345*math.sin(a):.1f}"/>'
               for a in [i*math.pi/24 for i in range(48)])
v3 = f"""
<circle cx="540" cy="540" r="420" fill="none" stroke="url(#gold)" stroke-width="4"/>
<polygon points="{star_poly(395, 370, 16)}" fill="none" stroke="url(#gold)" stroke-width="3"/>
<g stroke="#c9a24f" stroke-width="3" opacity=".7">{rays}</g>
<circle cx="540" cy="540" r="290" fill="#0a2627" stroke="url(#gold)" stroke-width="3"/>
<text x="540" y="575" text-anchor="middle" class="ar" font-size="380" fill="url(#gold)">ح</text>
"""

js = ROOT / "templates" / "shot.js"; js.parent.mkdir(exist_ok=True); js.write_text(JS)
for n, v in enumerate([v1, v2, v3], 1):
    h = ROOT / "templates" / f"profil-{n}.html"; h.write_text(page(v))
    subprocess.run(["node", str(js), str(h), str(ROOT / "profile" / f"profil-{n}.jpg"), "1080", "1080"], check=True)

# Seçilen: 1 numara, koyu lacivert
NAVY_BG = "radial-gradient(circle at 50% 45%, #16294d 0%, #0b1733 70%, #060e22 100%)"
v1_navy = v1.replace('fill="#0b2a2c"', 'fill="#0d1b3a"')
h = ROOT / "templates" / "profil-secilen.html"; h.write_text(page(v1_navy, NAVY_BG))
subprocess.run(["node", str(js), str(h), str(ROOT / "profile" / "profil-secilen.jpg"), "1080", "1080"], check=True)
