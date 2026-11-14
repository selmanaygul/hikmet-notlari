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


def tree(x, base, fill="#050d10"):
    """Yaprakları sarkan yaşlı ağaç silueti."""
    r = random.Random(3)
    leaves = "".join(
        f'<ellipse cx="{x + r.uniform(-170, 190):.0f}" cy="{base - r.uniform(330, 520):.0f}" '
        f'rx="{r.uniform(50, 95):.0f}" ry="{r.uniform(30, 55):.0f}"/>' for _ in range(26))
    drapes = "".join(
        f'<path d="M{x+dx} {base-400} q {r.uniform(-8,8):.0f} 90 {r.uniform(-4,4):.0f} {r.uniform(150,230):.0f}" '
        f'stroke="{fill}" stroke-width="{r.uniform(1.5,3):.1f}" fill="none"/>' for dx in range(-170, 200, 22))
    return f"""<g fill="{fill}">
<path d="M{x-28} {base} C{x-22} {base-120} {x-40} {base-220} {x-10} {base-330} L{x+18} {base-330}
 C{x+20} {base-230} {x+30} {base-120} {x+40} {base} Z"/>
<path d="M{x-5} {base-280} C{x-60} {base-330} {x-110} {base-360} {x-150} {base-400} L{x-140} {base-410}
 C{x-90} {base-380} {x-40} {base-350} {x+5} {base-305} Z"/>
<path d="M{x+10} {base-300} C{x+70} {base-340} {x+120} {base-380} {x+160} {base-420} L{x+170} {base-410}
 C{x+130} {base-360} {x+80} {base-320} {x+20} {base-270} Z"/>
{leaves}</g>{drapes}"""


def reflection():
    """Hadis: kardeşini günahıyla ayıplama. Alacakaranlıkta durgun suya bakıp kendi aksini gören kişi."""
    shore = 930
    pond_top, pond_bot = 950, 1150
    fig_x = 430
    fig = figure(fig_x, shore, 1)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{sky(seed=21, top="#0a1b2b", mid="#2a3f4c", glow="#e59a55")}
<defs>
 <clipPath id="pond"><ellipse cx="560" cy="1030" rx="640" ry="112"/></clipPath>
 <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3b4c52"/><stop offset=".5" stop-color="#1b2d35"/><stop offset="1" stop-color="#0b171c"/>
 </linearGradient>
</defs>
<path d="M0 820 C 180 760 320 790 470 770 C 640 745 820 800 1080 760 V{shore} H0 Z" fill="#14262d"/>
<path d="M0 880 C 220 850 420 880 620 860 C 800 845 950 870 1080 850 V{shore} H0 Z" fill="#0c1b20"/>
<rect x="0" y="{shore}" width="{W}" height="{H-shore}" fill="#060f12"/>
<g clip-path="url(#pond)">
 <rect x="0" y="{shore}" width="{W}" height="{pond_bot-shore+60}" fill="url(#water)"/>
 <g transform="translate(0 {2*shore}) scale(1 -1)" opacity=".42">
  <path d="M0 820 C 180 760 320 790 470 770 C 640 745 820 800 1080 760 V{shore} H0 Z" fill="#14262d"/>
  <circle cx="690" cy="432" r="0"/>
 </g>
 <g transform="translate(0 {2*shore+10}) scale(1 -1)" opacity=".35">{fig}</g>
 <ellipse cx="690" cy="975" rx="46" ry="9" fill="#f6e3b4" opacity=".55"/><g stroke="#f6e3b4" stroke-width="3" opacity=".35"><path d="M660 995 h60"/><path d="M670 1012 h40"/><path d="M678 1028 h24"/></g>
 <g stroke="#e9c97a" stroke-width="2" opacity=".35" fill="none">
  <path d="M520 1010 q 40 -6 80 0"/><path d="M640 1045 q 60 -8 120 0"/><path d="M380 1075 q 70 -8 140 0"/>
  <path d="M600 1100 q 50 -6 100 0"/><path d="M250 1040 q 40 -5 80 0"/><path d="M820 1010 q 40 -5 80 0"/>
 </g>
</g>
<path d="M0 {shore+6} C 120 {shore-14} 260 {shore-8} 360 {shore+2} C 420 {shore+8} 470 {shore+2} 520 {shore+10}
 L 520 {shore+24} C 380 {shore+30} 200 {shore+40} 0 {shore+50} Z" fill="#040b0d"/>
<path d="M330 {shore+4} C 360 {shore-34} 470 {shore-38} 520 {shore+8} Z" fill="#040b0d"/>
{tree(170, shore+20)}
{fig}
<g fill="#040b0d">
 <path d="M880 {shore+10} l6 -60 l4 60 Z"/><path d="M900 {shore+10} l-8 -80 l14 80 Z"/><path d="M920 {shore+10} l10 -55 l-2 55 Z"/>
 <path d="M60 {shore+30} l4 -50 l6 50 Z"/><path d="M90 {shore+30} l-6 -70 l12 70 Z"/>
</g>
</svg>"""


SCENES = {"companions": companions, "reflection": reflection}


# ---------------- Medine: seher vakti Mescid-i Nebevî ----------------
def _medina_minaret(x, base, h, fill):
    top = base - h
    w = 26
    parts = [f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{h}"/>']
    for k, f in enumerate((0.38, 0.62, 0.82)):
        y = base - h * f
        parts.append(f'<rect x="{x-w/2-9}" y="{y}" width="{w+18}" height="7"/>')
        parts.append(f'<rect x="{x-w/2-7}" y="{y-14}" width="{w+14}" height="2.5"/>')
        for dx in range(-int(w/2)-6, int(w/2)+8, 7):
            parts.append(f'<rect x="{x+dx}" y="{y-14}" width="2" height="14"/>')
    parts.append(f'<rect x="{x-9}" y="{top-60}" width="18" height="60"/>')
    parts.append(f'<path d="M{x-14} {top-58} C{x-16} {top-90} {x+16} {top-90} {x+14} {top-58} Z"/>')
    parts.append(f'<path d="M{x-6} {top-84} L{x} {top-120} L{x+6} {top-84} Z"/>')
    parts.append(f'<path d="M{x} {top-136} a8 8 0 1 0 6 12 a6 6 0 1 1 -6 -12 Z" fill="#e9c97a"/>')
    return f'<g fill="{fill}">{"".join(parts)}</g>'


def _umbrella(x, base, w, h, lit="#f4e4d0", shade="#c9a99a", pole="#3a2a34"):
    top = base - h
    hw = w / 2
    scallop = " ".join(f"Q{x-hw+w*(i+0.5)/6:.0f} {top+52} {x-hw+w*(i+1)/6:.0f} {top+40}" for i in range(6))
    return (f'<rect x="{x-4}" y="{top+20}" width="8" height="{h-20}" fill="{pole}"/>'
            f'<path d="M{x-hw} {top+40} L{x} {top} L{x+hw} {top+40} {scallop} Z" fill="{lit}"/>'
            f'<path d="M{x} {top} L{x+hw} {top+40} Q{x+hw*0.84:.0f} {top+52} {x+hw*0.67:.0f} {top+40} Z" fill="{shade}" opacity=".7"/>'
            f'<path d="M{x} {top} L{x-hw*0.33:.0f} {top+44} M{x} {top} L{x+hw*0.33:.0f} {top+44}" stroke="{shade}" stroke-width="2"/>')


def _palm(x, base, h, fill="#2a1a28", lean=0.0):
    tx, ty = x + lean * h, base - h
    trunk = f'<path d="M{x-9} {base} Q{x+lean*h*0.4-6:.0f} {base-h*0.5:.0f} {tx-4:.0f} {ty} L{tx+4:.0f} {ty} Q{x+lean*h*0.4+6:.0f} {base-h*0.5:.0f} {x+9} {base} Z"/>'
    fronds = ""
    for ang, ln in [(-160, 120), (-130, 135), (-95, 110), (-60, 135), (-25, 120), (-195, 95), (10, 95)]:
        import math
        a = math.radians(ang)
        ex, ey = tx + ln * math.cos(a), ty + ln * math.sin(a) + 40
        mx, my = tx + ln * 0.55 * math.cos(a), ty + ln * 0.55 * math.sin(a) - 18
        fronds += (f'<path d="M{tx:.0f} {ty} Q{mx:.0f} {my:.0f} {ex:.0f} {ey:.0f} '
                   f'Q{mx+4:.0f} {my+34:.0f} {tx:.0f} {ty+10} Z"/>')
    return f'<g fill="{fill}">{trunk}{fronds}</g>'


def _dove(x, y, s, fill="#2b1d2e", flap=0):
    up = -10 if flap else 6
    return (f'<path transform="translate({x} {y}) scale({s})" fill="{fill}" '
            f'd="M-22 {up} Q-11 -8 0 2 Q11 -8 22 {up} Q12 -2 0 8 Q-12 -2 -22 {up} Z"/>')


def medina():
    """Hadis: kabr-i şerif ziyareti. Seher vakti Mescid-i Nebevî, Kubbe-i Hadrâ, şemsiyeler ve güvercinler."""
    r = random.Random(33)
    stars = "".join(f'<circle cx="{r.uniform(40, W-40):.0f}" cy="{r.uniform(30, 300):.0f}" r="{r.choice([1, 1.3, 1.8])}" '
                    f'fill="#fff4ea" opacity="{r.uniform(.25, .7):.2f}"/>' for _ in range(40))
    base = 900
    bld = "#3a2433"
    # Mescid gövdesi: kemerli uzun cephe ve çatıdaki küçük kubbeler
    arches = "".join(f'<path d="M{x} {base} v-62 a17 17 0 0 1 34 0 v62 Z" fill="#f2c08e" opacity=".42"/>'
                     for x in range(60, 1040, 52))
    small_domes = "".join(f'<path d="M{x-26} {base-118} a26 22 0 0 1 52 0 Z" fill="#4a3040"/>' for x in range(90, 1010, 74))
    # Kubbe-i Hadrâ (Yeşil Kubbe)
    gx, gy = 470, base - 150
    green = (f'<rect x="{gx-78}" y="{gy-60}" width="156" height="62" fill="#2d6b4c"/>'
             + "".join(f'<rect x="{gx-62+k*26}" y="{gy-48}" width="10" height="28" rx="5" fill="#173d2c"/>' for k in range(5))
             + f'<path d="M{gx-92} {gy-58} C{gx-92} {gy-170} {gx-30} {gy-215} {gx} {gy-240} '
               f'C{gx+30} {gy-215} {gx+92} {gy-170} {gx+92} {gy-58} Z" fill="url(#greendome)"/>'
             + "".join(f'<path d="M{gx+dx} {gy-60} Q{gx+dx*0.55:.0f} {gy-180} {gx} {gy-238}" stroke="#a5d9b8" stroke-width="2" fill="none" opacity=".35"/>'
                       for dx in (-60, -30, 30, 60))
             + f'<rect x="{gx-2}" y="{gy-290}" width="4" height="52" fill="#e9c97a"/>'
             + f'<circle cx="{gx}" cy="{gy-262}" r="7" fill="#e9c97a"/>'
             + f'<path d="M{gx} {gy-318} a14 14 0 1 0 10 22 a11 11 0 1 1 -10 -22 Z" fill="#e9c97a"/>')
    doves = "".join(_dove(x, y, s, flap=f) for x, y, s, f in
                    [(700, 470, 1.0, 0), (760, 430, .8, 1), (820, 480, .9, 1), (650, 520, .7, 1),
                     (880, 420, .6, 0), (590, 455, .55, 0), (930, 500, .5, 1)])
    umbrellas = "".join(_umbrella(x, 1130, w, h) for x, w, h in [(150, 250, 230), (420, 270, 250), (700, 270, 250), (960, 250, 230)])
    tiles = "".join(f'<path d="M540 960 L{x} 1350" stroke="#f4e4d0" stroke-width="1.2" opacity=".06"/>' for x in range(-600, 1700, 150))
    rows = "".join(f'<path d="M0 {y} H1080" stroke="#f4e4d0" stroke-width="1" opacity=".12"/>' for y in (990, 1035, 1095, 1170, 1265))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1f2140"/><stop offset=".35" stop-color="#5a3a5e"/>
  <stop offset=".55" stop-color="#b8708a"/><stop offset=".68" stop-color="#f0b48a"/><stop offset=".75" stop-color="#f7d6a8"/>
 </linearGradient>
 <radialGradient id="sun" cx=".62" cy=".64" r=".35"><stop offset="0" stop-color="#ffe7bf" stop-opacity=".9"/><stop offset="1" stop-color="#ffe7bf" stop-opacity="0"/></radialGradient>
 <linearGradient id="greendome" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#1f5a3c"/><stop offset=".55" stop-color="#3d9a68"/><stop offset="1" stop-color="#2a7350"/>
 </linearGradient>
 <linearGradient id="court" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#8a6070"/><stop offset=".4" stop-color="#4a2f40"/><stop offset="1" stop-color="#1e1019"/>
 </linearGradient>
</defs>
<rect width="{W}" height="{H}" fill="url(#dawn)"/>
<rect width="{W}" height="{H}" fill="url(#sun)"/>
{stars}
{_medina_minaret(130, base-110, 420, bld)}{_medina_minaret(880, base-110, 470, bld)}
{_medina_minaret(330, base-110, 350, "#4a2f40")}{_medina_minaret(1010, base-110, 330, "#4a2f40")}
<rect x="0" y="{base-120}" width="{W}" height="122" fill="{bld}"/>
{small_domes}
{green}
<rect x="0" y="{base-120}" width="{W}" height="6" fill="#5a3a4c"/>
{arches}
{doves}
<rect x="0" y="{base}" width="{W}" height="{H-base}" fill="url(#court)"/>
{tiles}{rows}
{_palm(40, 1000, 380, lean=0.05)}{_palm(1050, 1010, 360, lean=-0.06)}
{umbrellas}
<rect x="0" y="1130" width="{W}" height="220" fill="#1e1019" opacity=".55"/>
</svg>"""


SCENES["medina"] = medina
