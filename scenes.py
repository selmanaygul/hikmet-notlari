"""Konuya özel SVG illüstrasyonları (1080x1350)."""
import random

W, H = 1080, 1350


def sky(seed=7, top="#081a24", mid="#14323d", glow="#e3a85a"):
    r = random.Random(seed)
    stars = "".join(
        f'<circle cx="{r.uniform(20, W-20):.0f}" cy="{r.uniform(20, 620):.0f}" r="{r.choice([1,1,1.4,2]):.1f}" '
        f'fill="#f5e6c4" opacity="{r.uniform(.35, .9):.2f}"/>' for _ in range(110))
    return f"""
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{top}"/><stop offset=".62" stop-color="{mid}"/><stop offset=".8" stop-color="#3a4a45"/>
 </linearGradient>
 <radialGradient id="horizon" cx=".5" cy=".72" r=".55">
  <stop offset="0" stop-color="{glow}" stop-opacity=".55"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/>
 </radialGradient>
 <radialGradient id="lamp" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#ffd58a" stop-opacity=".95"/><stop offset=".25" stop-color="#f0a948" stop-opacity=".45"/>
  <stop offset="1" stop-color="#f0a948" stop-opacity="0"/>
 </radialGradient>
 <mask id="moon"><rect width="{W}" height="{H}" fill="#fff"/><circle cx="712" cy="416" r="50" fill="#000"/></mask>
 <radialGradient id="moonglow"><stop offset=".3" stop-color="#f6e3b4" stop-opacity=".18"/><stop offset="1" stop-color="#f6e3b4" stop-opacity="0"/></radialGradient>
 <filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" fill="url(#horizon)"/>
{stars}
<circle cx="690" cy="432" r="56" fill="#f6e3b4" mask="url(#moon)"/>
<circle cx="690" cy="432" r="150" fill="url(#moonglow)"/>"""


def mosque(cx, base, s=1.0, fill="#0d2229"):
    """Kubbeli cami silueti; cx merkez, base zemin y'si."""
    def dome(x, y, rx, ry):
        return f'<path d="M{x-rx} {y} A{rx} {ry} 0 0 1 {x+rx} {y} Z"/><rect x="{x-2}" y="{y-ry-26}" width="4" height="28"/>' \
               f'<path d="M{x} {y-ry-38} a7 7 0 1 0 0.1 0" />'
    def minaret(x, h):
        top = base - h
        return (f'<rect x="{x-11}" y="{top}" width="22" height="{h}"/>'
                f'<rect x="{x-17}" y="{top+h*.32}" width="34" height="8"/>'
                f'<rect x="{x-17}" y="{top+h*.12}" width="34" height="7"/>'
                f'<path d="M{x-11} {top} L{x} {top-70} L{x+11} {top} Z"/>')
    body_w, body_h = 360, 150
    parts = [
        f'<rect x="{cx-body_w/2}" y="{base-body_h}" width="{body_w}" height="{body_h}"/>',
        f'<rect x="{cx-260}" y="{base-90}" width="520" height="90"/>',
        dome(cx, base-body_h, 125, 120),
        dome(cx-165, base-body_h+10, 52, 48),
        dome(cx+165, base-body_h+10, 52, 48),
        dome(cx-240, base-90, 34, 30),
        dome(cx+240, base-90, 34, 30),
        minaret(cx-310, 430), minaret(cx+310, 430),
    ]
    # pencereler
    win = "".join(f'<path d="M{cx+dx-9} {base-40} v-38 a9 9 0 0 1 18 0 v38 Z" fill="#e9b766" opacity=".35"/>'
                  for dx in (-120, -60, 0, 60, 120))
    return (f'<g fill="{fill}" transform="translate({cx} {base}) scale({s}) translate({-cx} {-base})">'
            + "".join(parts) + win + '</g>')


def figure(x, base, facing=1, fill="#03080a", rim="#f1b45c"):
    """Bağdaş kurup oturan, sarıklı kişi silueti. facing=1 sağa bakar."""
    shape = (
        '<ellipse cx="22" cy="-22" rx="98" ry="25"/>'
        '<path d="M-72 -24 C-82 -92 -68 -150 -32 -178 C-10 -194 22 -192 40 -172 C58 -150 64 -100 74 -24 Z"/>'
        '<path d="M34 -150 C60 -120 82 -100 106 -92 C114 -90 116 -80 108 -77 C80 -80 52 -98 24 -122 Z"/>'
        '<circle cx="8" cy="-208" r="27"/>'
        '<path d="M26 -204 C36 -190 28 -176 12 -178 C6 -186 12 -196 26 -204 Z"/>'
    )
    turban = ('<path d="M-24 -214 C-30 -250 2 -262 22 -256 C42 -250 46 -230 38 -214 '
              'C20 -224 -6 -226 -24 -214 Z" fill="#d8ccb2"/>'
              '<path d="M-20 -224 C0 -236 26 -236 40 -226 M-16 -240 C4 -250 26 -248 38 -238" '
              'fill="none" stroke="#a8987a" stroke-width="2.5"/>')
    rimline = (
        f'<g fill="none" stroke="{rim}" stroke-width="3.5" opacity=".85" filter="url(#soft)">'
        '<path d="M74 -24 C64 -100 58 -150 40 -172"/><path d="M34 -210 a27 27 0 0 0 -2 -14"/>'
        '<path d="M118 -24 a98 25 0 0 0 -30 -20"/></g>'
    )
    return (f'<g transform="translate({x} {base}) scale({facing} 1)"><g fill="{fill}">{shape}</g>{turban}{rimline}</g>')


def lantern(x, base):
    return f"""
<circle cx="{x}" cy="{base-60}" r="230" fill="url(#lamp)"/>
<g transform="translate({x} {base})">
 <rect x="-34" y="-8" width="68" height="8" rx="2" fill="#2b1a0e"/>
 <path d="M-26 -8 L-26 -78 L26 -78 L26 -8 Z" fill="#ffcf7a" opacity=".9"/>
 <path d="M-26 -8 L-26 -78 L26 -78 L26 -8 Z M-9 -8 V-78 M9 -8 V-78" fill="none" stroke="#3a2412" stroke-width="3"/>
 <path d="M-32 -78 L0 -112 L32 -78 Z" fill="#3a2412"/>
 <circle cx="0" cy="-120" r="8" fill="none" stroke="#3a2412" stroke-width="3"/>
 <ellipse cx="0" cy="-44" rx="9" ry="16" fill="#fff4d6"/>
</g>"""


def rahle_book(x, base):
    return f"""
<g transform="translate({x} {base})">
 <path d="M-60 0 L40 -70 M60 0 L-40 -70" stroke="#2a1708" stroke-width="9" stroke-linecap="round"/>
 <path d="M-62 -72 Q-30 -88 0 -72 Q30 -88 62 -72 L62 -60 Q30 -76 0 -60 Q-30 -76 -62 -60 Z" fill="#f3e2bd"/>
 <path d="M0 -72 V-60" stroke="#b58b4d" stroke-width="2"/>
</g>"""


def companions():
    """Hadis: en hayırlı arkadaş. Gece, cami önünde fener ışığında sohbet eden iki dost."""
    ground_y = 1080
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{sky()}
{mosque(540, 880, 0.82, "#1a3640")}
<path d="M0 {ground_y-150} Q 540 {ground_y-185} {W} {ground_y-150} V{H} H0 Z" fill="#0a1a1f"/>
<rect x="0" y="{ground_y-40}" width="{W}" height="{H}" fill="#06100f"/>
<path d="M0 {ground_y-40} H{W}" stroke="#c9a45c" stroke-width="1" opacity=".35"/>
{lantern(540, ground_y-38)}
{figure(355, ground_y-34, 1)}
{figure(725, ground_y-34, -1)}
{rahle_book(540, ground_y+78)}
</svg>"""


SCENES = {"companions": companions}
