"""Gera os SVGs animados do perfil metroidvania."""
import os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

W, H = 960, 300
GROUND = 240
T = 16  # duracao do ciclo (s)
SCALE = 4

PAL = {
    "r": "#ff6a3d", "R": "#c8321e", "S": "#f5c39a", "E": "#1a1020",
    "W": "#e8e0d0", "B": "#2e5aa8", "C": "#5b2a86", "Y": "#f2c14e",
    "P": "#3a2d4f", "K": "#7a4524",
}

HEAD = [
    "....rrrr....",
    "..rrRRRRrr..",
    ".rRRRRRRRRr.",
    "rRRRRSSSSR..",
    "RRRRSSSESS..",
    ".RRRSSSSSS..",
]
FRAME_A = HEAD + [
    "RR.RRSSSS...",
    "R..WWWWWW...",
    ".CCBBBBBBS..",
    "CCCBBBBBBSS.",
    "CC.BYYYYB...",
    "C..BBBBBB...",
    "...PPP.PPP..",
    "..PPP...PPP.",
    ".KKK.....KKK",
    ".KK.......KK",
]
FRAME_B = HEAD + [
    ".RR.RSSSS...",
    "RR.WWWWWW...",
    ".CCBBBBBBS..",
    "CCCBBBBBBSS.",
    "C..BYYYYB...",
    "CC.BBBBBB...",
    "...PPPPP....",
    "....PPPP....",
    "...KKK.KK...",
    "...KKK......",
]


def sprite(rows, scale):
    out = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            run = 1
            while x + run < len(row) and row[x + run] == c:
                run += 1
            out.append(f'<rect x="{x*scale}" y="{y*scale}" width="{run*scale}" height="{scale}" fill="{PAL[c]}"/>')
            x += run
    return "".join(out)


# ---- reliquias -------------------------------------------------------------
def relic_java():
    return ('<rect x="4" y="26" width="26" height="4" fill="#5382a1"/>'
            '<rect x="7" y="12" width="18" height="15" fill="#f89820"/>'
            '<rect x="7" y="12" width="18" height="3" fill="#ffc06b"/>'
            '<rect x="25" y="15" width="5" height="3" fill="#f89820"/>'
            '<rect x="28" y="15" width="3" height="9" fill="#f89820"/>'
            '<rect x="25" y="21" width="5" height="3" fill="#f89820"/>'
            '<g class="steam"><rect x="11" y="2" width="3" height="3" fill="#e8e0d0"/>'
            '<rect x="13" y="6" width="3" height="3" fill="#e8e0d0"/>'
            '<rect x="18" y="1" width="3" height="3" fill="#e8e0d0"/>'
            '<rect x="16" y="5" width="3" height="3" fill="#e8e0d0"/></g>')


def relic_shield(color, light, digit):
    return (f'<polygon points="3,2 29,2 27,25 16,31 5,25" fill="{color}"/>'
            f'<polygon points="16,4 27,4 25.4,24 16,29" fill="{light}"/>'
            f'<text x="16" y="22" text-anchor="middle" class="px" font-size="16" fill="#fff">{digit}</text>')


def relic_js():
    return ('<rect x="2" y="2" width="28" height="28" fill="#f7df1e"/>'
            '<text x="28" y="27" text-anchor="end" class="px" font-size="14" fill="#1a1020">JS</text>')


RELICS = [
    # nome, centro x, svg, cor do brilho
    ("JAVA", 170, relic_java(), "#f89820"),
    ("HTML", 380, relic_shield("#e34f26", "#f06529", "5"), "#e34f26"),
    ("CSS", 590, relic_shield("#1572b6", "#33a9dc", "3"), "#33a9dc"),
    ("JAVASCRIPT", 800, relic_js(), "#f7df1e"),
]

START_X, END_X = -60, 1000
SPRITE_W = 12 * SCALE
SPRITE_H = 16 * SCALE


def pct(cx):
    return (cx - SPRITE_W / 2 - START_X) / (END_X - START_X) * 100


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


css = []
body = []

# ---- fundo -------------------------------------------------------------------
defs = f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#07030f"/><stop offset=".6" stop-color="#1e0b33"/><stop offset="1" stop-color="#3a1240"/>
</linearGradient>
<radialGradient id="moonGlow"><stop offset="0" stop-color="#ffe9b0" stop-opacity=".45"/><stop offset="1" stop-color="#ffe9b0" stop-opacity="0"/></radialGradient>
<radialGradient id="torchGlow"><stop offset="0" stop-color="#ff9a3d" stop-opacity=".55"/><stop offset="1" stop-color="#ff9a3d" stop-opacity="0"/></radialGradient>
<pattern id="bricks" width="48" height="24" patternUnits="userSpaceOnUse">
  <rect width="48" height="24" fill="#2b1d3d"/>
  <rect x="1" y="1" width="46" height="10" fill="#3b2a52"/>
  <rect x="-23" y="13" width="46" height="10" fill="#34254a"/>
  <rect x="25" y="13" width="46" height="10" fill="#34254a"/>
</pattern>
''' + "".join(
    f'<radialGradient id="g{i}"><stop offset="0" stop-color="{c}" stop-opacity=".7"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
    for i, (_, _, _, c) in enumerate(RELICS)) + "</defs>"

body.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

# estrelas
import random
random.seed(7)
stars = []
for i in range(46):
    x, y = random.randint(0, W), random.randint(0, 150)
    s = random.choice([2, 2, 2, 3])
    d = random.choice([1.6, 2.4, 3.1, 4.2])
    delay = round(random.random() * 3, 2)
    stars.append(f'<rect class="tw" style="animation-duration:{d}s;animation-delay:-{delay}s" x="{x}" y="{y}" width="{s}" height="{s}" fill="#f4e7ff"/>')
body.append("".join(stars))

# lua
body.append('<circle cx="860" cy="70" r="80" fill="url(#moonGlow)"/>'
            '<circle cx="860" cy="70" r="34" fill="#f4e3b5"/>'
            '<circle cx="848" cy="60" r="7" fill="#e2cc95"/><circle cx="872" cy="82" r="5" fill="#e2cc95"/><circle cx="866" cy="56" r="3" fill="#e2cc95"/>')

# castelo distante
castle = ("M0,240 L0,190 L40,190 L40,170 L60,170 L60,190 L110,190 L110,140 L120,120 L130,140 L130,190 "
          "L200,190 L200,175 L230,175 L230,190 L300,190 L300,120 L310,120 L310,110 L320,110 L320,120 L330,120 L330,90 L345,60 L360,90 "
          "L360,120 L370,120 L370,110 L380,110 L380,120 L390,120 L390,190 L460,190 L460,150 L475,130 L490,150 L490,190 "
          "L560,190 L560,100 L572,100 L572,92 L584,92 L584,100 L596,100 L596,190 L640,190 L640,160 L660,135 L680,160 L680,190 "
          "L760,190 L760,130 L780,105 L800,130 L800,190 L900,190 L900,165 L930,165 L930,190 L960,190 L960,240 Z")
body.append(f'<path d="{castle}" fill="#160a26"/>')
# janelas acesas do castelo
for (x, y) in [(340, 100), (348, 100), (575, 115), (775, 140), (115, 150), (470, 160), (655, 168)]:
    body.append(f'<rect class="win" x="{x}" y="{y}" width="4" height="7" fill="#ffb347"/>')

# morcegos
for i, (y, dur, delay) in enumerate([(70, 11, 0), (110, 15, 6), (45, 19, 3)]):
    body.append(f'<g class="bat" style="animation-duration:{dur}s;animation-delay:-{delay}s"><g transform="translate(0,{y})">'
                f'<g class="flap"><polygon points="0,4 8,0 12,4 16,0 24,4 14,8 12,6 10,8" fill="#0a0414"/></g></g></g>')

# pilares com tochas
for px in [65, 275, 485, 695, 905]:
    body.append(f'<rect x="{px-10}" y="150" width="20" height="90" fill="#251838"/>'
                f'<rect x="{px-10}" y="150" width="4" height="90" fill="#3a2a55"/>'
                f'<rect x="{px-14}" y="144" width="28" height="8" fill="#3a2a55"/>'
                f'<circle class="glow" cx="{px}" cy="128" r="34" fill="url(#torchGlow)"/>'
                f'<rect x="{px-4}" y="132" width="8" height="12" fill="#6b4a2a"/>'
                f'<g class="flame"><rect x="{px-5}" y="122" width="10" height="10" fill="#ff7a1a"/>'
                f'<rect x="{px-3}" y="116" width="6" height="8" fill="#ffc23d"/>'
                f'<rect x="{px-1}" y="112" width="2" height="5" fill="#fff1a8"/></g>')

# chao
body.append(f'<rect y="{GROUND}" width="{W}" height="{H-GROUND}" fill="url(#bricks)"/>'
            f'<rect y="{GROUND}" width="{W}" height="3" fill="#6b4f86"/>')

# ---- reliquias + placas + popups ---------------------------------------------
for i, (name, cx, svg, color) in enumerate(RELICS):
    p = pct(cx)
    # placa no chao
    pw = 14 + len(name) * 9
    body.append(f'<rect x="{cx-pw/2}" y="256" width="{pw}" height="20" fill="#1a1020" stroke="#f2c14e" stroke-width="2"/>'
                f'<text x="{cx}" y="271" text-anchor="middle" class="px" font-size="13" fill="#f2c14e">{name}</text>')
    # reliquia flutuante
    body.append(f'<g class="relic{i}"><g class="bob">'
                f'<circle class="pulse" cx="{cx}" cy="134" r="26" fill="url(#g{i})"/>'
                f'<g transform="translate({cx-16},118)">{svg}</g></g></g>')
    # anel ao coletar
    body.append(f'<circle class="ring{i}" cx="{cx}" cy="134" r="20" fill="none" stroke="{color}" stroke-width="3"/>')
    # popup
    body.append(f'<text class="pop{i} px" x="{cx}" y="104" text-anchor="middle" font-size="14" fill="{color}">+1 {name}</text>')
    gone = p + 0.3
    css.append(f".relic{i}{{animation:relic{i} {T}s linear infinite}}"
               f"@keyframes relic{i}{{0%,{f(p)}%{{opacity:1}}{f(gone)}%,96%{{opacity:0}}99%,100%{{opacity:1}}}}")
    css.append(f".ring{i}{{transform-box:fill-box;transform-origin:center;opacity:0;animation:ring{i} {T}s linear infinite}}"
               f"@keyframes ring{i}{{0%,{f(p)}%{{opacity:0;transform:scale(.4)}}{f(p+0.2)}%{{opacity:1;transform:scale(.6)}}"
               f"{f(p+3)}%{{opacity:0;transform:scale(2.6)}}100%{{opacity:0;transform:scale(2.6)}}}}")
    css.append(f".pop{i}{{opacity:0;animation:pop{i} {T}s linear infinite}}"
               f"@keyframes pop{i}{{0%,{f(p)}%{{opacity:0;transform:translateY(0)}}{f(p+0.5)}%{{opacity:1}}"
               f"{f(p+7)}%{{opacity:0;transform:translateY(-26px)}}100%{{opacity:0;transform:translateY(-26px)}}}}")

# ---- personagem --------------------------------------------------------------
jump = ["0%{transform:translateY(0)}"]
for (_, cx, _, _) in RELICS:
    p = pct(cx)
    for dp, dy in [(-4.2, 0), (-3, -30), (-2, -50), (-1, -62), (0, -66), (1, -62), (2, -50), (3, -30), (4.2, 0)]:
        jump.append(f"{f(p+dp)}%{{transform:translateY({dy}px)}}")
jump.append("100%{transform:translateY(0)}")
css.append(f".hero{{animation:run {T}s linear infinite}}"
           f"@keyframes run{{from{{transform:translateX({START_X}px)}}to{{transform:translateX({END_X}px)}}}}"
           f".jump{{animation:jump {T}s linear infinite}}@keyframes jump{{{''.join(jump)}}}")

body.append(f'<g class="hero"><ellipse cx="{SPRITE_W/2}" cy="{GROUND+1}" rx="18" ry="4" fill="#000" opacity=".35"/>'
            f'<g class="jump"><g transform="translate(0,{GROUND-SPRITE_H})">'
            f'<g class="fa">{sprite(FRAME_A, SCALE)}</g><g class="fb">{sprite(FRAME_B, SCALE)}</g>'
            f'</g></g></g>')

# ---- HUD ---------------------------------------------------------------------
body.append('<g class="hud">'
            '<rect x="14" y="12" width="250" height="58" fill="#0b0618" fill-opacity=".85" stroke="#f2c14e" stroke-width="2"/>'
            '<text x="26" y="34" class="px" font-size="17" fill="#ff6a3d">CAUAN DEV</text>'
            '<text x="160" y="34" class="px" font-size="12" fill="#e8e0d0">LV ∞</text>'
            '<text x="26" y="52" class="px" font-size="11" fill="#e8e0d0">HP</text>'
            '<rect x="48" y="44" width="200" height="8" fill="#3a1020"/><rect class="hp" x="48" y="44" width="200" height="8" fill="#e0303a"/>'
            '<text x="26" y="64" class="px" font-size="11" fill="#e8e0d0">MP</text>'
            '<rect x="48" y="57" width="200" height="6" fill="#10203a"/><rect class="mp" x="48" y="57" width="200" height="6" fill="#3d8bff"/>'
            '</g>')
body.append('<rect x="690" y="12" width="256" height="58" fill="#0b0618" fill-opacity=".85" stroke="#f2c14e" stroke-width="2"/>'
            '<text x="702" y="30" class="px" font-size="12" fill="#f2c14e">RELÍQUIAS</text>')
for i, (name, cx, svg, color) in enumerate(RELICS):
    sx = 760 + i * 46
    p = pct(cx)
    body.append(f'<rect x="{sx}" y="20" width="40" height="42" fill="#160c28" stroke="#4a3a6a" stroke-width="2"/>'
                f'<g class="slot{i}" transform="translate({sx+4},25) scale(1)">{svg}</g>')
    css.append(f".slot{i}{{opacity:0;animation:slot{i} {T}s linear infinite}}"
               f"@keyframes slot{i}{{0%,{f(p)}%{{opacity:0}}{f(p+0.3)}%,96%{{opacity:1}}99%,100%{{opacity:0}}}}")

# ---- css geral ---------------------------------------------------------------
css.insert(0, """
.px{font-family:'Courier New',Courier,monospace;font-weight:700;letter-spacing:1px}
.tw{animation:tw 3s steps(2) infinite}@keyframes tw{50%{opacity:.15}}
.win{animation:tw 5s steps(2) infinite}
.bat{animation:bat 12s linear infinite}@keyframes bat{from{transform:translateX(-40px)}to{transform:translateX(1000px)}}
.flap{transform-box:fill-box;transform-origin:center;animation:flap .25s steps(2) infinite}@keyframes flap{50%{transform:scaleY(-.6)}}
.flame{animation:flame .4s steps(2) infinite}@keyframes flame{50%{transform:translateY(-2px) scaleY(1.08)}}
.flame{transform-box:fill-box;transform-origin:bottom}
.glow{animation:glow 1.2s ease-in-out infinite alternate}@keyframes glow{to{opacity:.55}}
.bob{animation:bob 1.6s ease-in-out infinite alternate}@keyframes bob{to{transform:translateY(-6px)}}
.pulse{animation:glow .9s ease-in-out infinite alternate}
.steam{animation:tw 1s steps(2) infinite}
.fa{animation:fa .36s steps(1) infinite}@keyframes fa{50%{opacity:0}}
.fb{opacity:0;animation:fb .36s steps(1) infinite}@keyframes fb{50%{opacity:1}}
.mp{transform-box:fill-box;transform-origin:left;animation:mp 4s ease-in-out infinite alternate}@keyframes mp{to{transform:scaleX(.55)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
""")

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges">'
       f'<title>Cauan Dev - metroidvania</title><style>{"".join(css)}</style>{defs}{"".join(body)}</svg>')
with open(os.path.join(OUT, "metroidvania-hero.svg"), "w", encoding="utf-8") as fh:
    fh.write(svg)


# =============================================================================
# Mapa do castelo (estilo mapa de Symphony of the Night)
# =============================================================================
CW, CH = 36, 22  # celula
OX, OY = 30, 50

# (col, row, w, h, cor, rotulo)
rooms = [
    (0, 3, 3, 1, "#2b4fd8", ""),             # entrada
    (3, 3, 4, 2, "#e34f26", "HTML"),
    (7, 2, 1, 3, "#2b4fd8", ""),             # corredor vertical
    (8, 1, 4, 2, "#1572b6", "CSS"),
    (12, 1, 1, 1, "#d02c3a", "S"),           # save room
    (13, 0, 2, 4, "#c9a400", "JS"),
    (8, 4, 5, 1, "#2b4fd8", ""),
    (9, 5, 5, 2, "#f89820", "JAVA"),
    (14, 5, 1, 1, "#c9a400", "W"),           # warp
]
unknown = [(15, 1, 2, 1), (15, 4, 2, 2), (5, 5, 3, 1), (0, 1, 3, 2)]

mw = W
mh = 250
m = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {mw} {mh}" width="{mw}" height="{mh}" shape-rendering="crispEdges">',
     '<title>Mapa do castelo</title>',
     "<style>.px{font-family:'Courier New',Courier,monospace;font-weight:700;letter-spacing:1px}"
     ".you{animation:blink .8s steps(2) infinite}@keyframes blink{50%{opacity:0}}"
     ".unk{animation:unk 3s ease-in-out infinite alternate}@keyframes unk{to{opacity:.35}}"
     "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>",
     f'<rect width="{mw}" height="{mh}" fill="#07030f"/>',
     f'<rect x="4" y="4" width="{mw-8}" height="{mh-8}" fill="none" stroke="#f2c14e" stroke-width="2"/>',
     '<text x="30" y="34" class="px" font-size="16" fill="#f2c14e">MAPA DO CASTELO</text>']

# grade
for c in range(18):
    for r in range(8):
        m.append(f'<rect x="{OX+c*CW}" y="{OY+r*CH}" width="{CW}" height="{CH}" fill="none" stroke="#140c24" stroke-width="1"/>')
for (c, r, w, h) in unknown:
    m.append(f'<rect class="unk" x="{OX+c*CW+2}" y="{OY+r*CH+2}" width="{w*CW-4}" height="{h*CH-4}" fill="none" stroke="#4a3a6a" stroke-width="2" stroke-dasharray="4 4"/>'
             f'<text class="px unk" x="{OX+(c+w/2)*CW}" y="{OY+(r+h/2)*CH+5}" text-anchor="middle" font-size="13" fill="#4a3a6a">?</text>')
for (c, r, w, h, col, label) in rooms:
    x, y = OX + c * CW, OY + r * CH
    m.append(f'<rect x="{x+2}" y="{y+2}" width="{w*CW-4}" height="{h*CH-4}" fill="{col}" fill-opacity=".85" stroke="#f4f0ff" stroke-width="2"/>')
    if label:
        fs = 13 if len(label) > 1 else 12
        m.append(f'<text x="{x+w*CW/2}" y="{y+h*CH/2+5}" text-anchor="middle" class="px" font-size="{fs}" fill="#fff">{label}</text>')
# jogador piscando na sala JS
m.append(f'<rect class="you" x="{OX+13*CW+CW-5}" y="{OY+2*CH+5}" width="10" height="10" fill="#ff6a3d" stroke="#fff" stroke-width="2"/>')

# legenda
lx = 720
legend = [("#e34f26", "HTML  · Átrio"), ("#1572b6", "CSS   · Galeria"), ("#c9a400", "JS    · Torre"),
          ("#f89820", "JAVA  · Catacumbas"), ("#d02c3a", "S     · Save room"), ("#4a3a6a", "?     · Inexplorado")]
m.append(f'<text x="{lx}" y="62" class="px" font-size="13" fill="#e8e0d0">LEGENDA</text>')
for i, (col, txt) in enumerate(legend):
    y = 80 + i * 22
    m.append(f'<rect x="{lx}" y="{y}" width="14" height="14" fill="{col}" stroke="#f4f0ff" stroke-width="1.5"/>'
             f'<text x="{lx+24}" y="{y+12}" class="px" font-size="12" fill="#e8e0d0">{txt}</text>')
m.append(f'<rect class="you" x="{lx+2}" y="{80+6*22+2}" width="10" height="10" fill="#ff6a3d" stroke="#fff" stroke-width="2"/>'
         f'<text x="{lx+24}" y="{80+6*22+12}" class="px" font-size="12" fill="#ff6a3d">VOCÊ ESTÁ AQUI</text>')
m.append("</svg>")
with open(os.path.join(OUT, "castle-map.svg"), "w", encoding="utf-8") as fh:
    fh.write("".join(m))
print("ok")
