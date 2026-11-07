"""Gera a capa do perfil: paisagem ao pôr do sol com montanhas e floresta.

Uso: python gerar_banner.py assets
"""
import os, random, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 400
random.seed(42)


def ridge(y_left, y_right, rough, depth=7):
    """Linha de montanha por deslocamento do ponto médio."""
    pts = [(0, y_left), (W, y_right)]
    amp = rough
    for _ in range(depth):
        nxt = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            nxt.append((x1, y1))
            nxt.append(((x1 + x2) / 2, (y1 + y2) / 2 + random.uniform(-amp, amp)))
        nxt.append(pts[-1])
        pts = nxt
        amp *= 0.55
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f"0,{H} {d} {W},{H}"


def pine(x, base, h, w):
    """Pinheiro em silhueta: camadas de triângulos sobre um tronco fino."""
    tiers = 4
    pts = []
    for t in range(tiers):
        top = base - h + t * h * 0.2
        bot = base - h * 0.15 - (tiers - 1 - t) * h * 0.17
        half = w * (0.35 + 0.65 * (t + 1) / tiers) / 2
        pts.append(f'<polygon points="{x:.1f},{top:.1f} {x-half:.1f},{bot:.1f} {x+half:.1f},{bot:.1f}"/>')
    pts.append(f'<rect x="{x-w*0.05:.1f}" y="{base-h*0.2:.1f}" width="{w*0.1:.1f}" height="{h*0.2:.1f}"/>')
    return "".join(pts)


def forest(base, count, hmin, hmax, xs=None):
    out = []
    xs = xs or sorted(random.uniform(-20, W + 20) for _ in range(count))
    for x in xs:
        h = random.uniform(hmin, hmax)
        out.append(pine(x, base + random.uniform(-4, 4), h, h * random.uniform(0.38, 0.48)))
    return "".join(out)


b = []
b.append('''<defs>
<linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1f1533"/>
  <stop offset=".35" stop-color="#5a2a55"/>
  <stop offset=".62" stop-color="#b8546a"/>
  <stop offset=".82" stop-color="#ec8a62"/>
  <stop offset="1" stop-color="#f7c07a"/>
</linearGradient>
<radialGradient id="brilho"><stop offset="0" stop-color="#ffd9a0" stop-opacity=".75"/><stop offset=".4" stop-color="#ffb07a" stop-opacity=".25"/><stop offset="1" stop-color="#ffb07a" stop-opacity="0"/></radialGradient>
<linearGradient id="sol" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1c9"/><stop offset="1" stop-color="#ffc27a"/></linearGradient>
<linearGradient id="nevoa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3a07a" stop-opacity="0"/><stop offset="1" stop-color="#f3a07a" stop-opacity=".35"/></linearGradient>
<filter id="sombra" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#1f1533" flood-opacity=".55"/></filter>
</defs>''')
b.append(f'<rect width="{W}" height="{H}" fill="url(#ceu)"/>')

# estrelas discretas no alto do céu
for _ in range(40):
    x, y = random.uniform(0, W), random.uniform(0, 110)
    r = random.choice([0.8, 1, 1.2])
    b.append(f'<circle class="tw" style="animation-delay:-{random.uniform(0, 4):.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity=".6"/>')

# sol
b.append('<circle class="halo" cx="975" cy="226" r="230" fill="url(#brilho)"/>'
         '<circle cx="975" cy="226" r="56" fill="url(#sol)"/>')

# nuvens finas
for (x, y, w, dur) in [(30, 128, 240, 70), (880, 92, 220, 90), (930, 182, 200, 80), (60, 228, 170, 100)]:
    b.append(f'<g class="nuvem" style="animation-duration:{dur}s"><rect x="{x}" y="{y}" width="{w}" height="7" rx="3.5" fill="#ffd0b0" opacity=".28"/>'
             f'<rect x="{x+w*0.18:.0f}" y="{y-6}" width="{w*0.5:.0f}" height="6" rx="3" fill="#ffd0b0" opacity=".2"/></g>')

# montanhas: perspectiva atmosférica do fundo para a frente
b.append(f'<polygon points="{ridge(215, 200, 75)}" fill="#c96f78"/>')
b.append(f'<polygon points="{ridge(250, 238, 60)}" fill="#9a4767"/>')
b.append(f'<rect y="200" width="{W}" height="140" fill="url(#nevoa)"/>')
b.append(f'<polygon points="{ridge(290, 280, 45)}" fill="#6a2c55"/>')

# floresta: três camadas
b.append(f'<g fill="#4a1f45">{forest(358, 70, 34, 66)}</g>')
b.append(f'<g fill="#2e1333">{forest(380, 55, 52, 96)}</g>')
b.append(f'<rect y="376" width="{W}" height="{H-376}" fill="#1c0b22"/>')
b.append(f'<g fill="#1c0b22">{forest(402, 0, 130, 185, xs=[20, 75, 130, 1060, 1120, 1175])}</g>')

# pássaros ao longe
for (y, dur, delay, s) in [(150, 38, 0, 1), (172, 46, 12, .8), (135, 52, 26, .7)]:
    b.append(f'<g class="voo" style="animation-duration:{dur}s;animation-delay:-{delay}s"><g transform="translate(0,{y}) scale({s})">'
             f'<path class="asa" d="M0,0 q6,-6 12,0 q6,-6 12,0" fill="none" stroke="#2a1230" stroke-width="2" stroke-linecap="round"/></g></g>')

# texto
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'Cascadia Code','Consolas','Courier New',monospace"
b.append(f'<g filter="url(#sombra)" text-anchor="middle">'
         f'<text x="600" y="132" font-family="{FONT}" font-size="48" font-weight="700" fill="#fff4ea" letter-spacing="1">Olá, eu sou o Cauan</text>'
         f'<text x="600" y="180" font-family="{MONO}" font-size="26" font-weight="600" fill="#ffe1c4">Engenheiro de Automações<tspan class="cursor">_</tspan></text>'
         f'<text x="600" y="214" font-family="{FONT}" font-size="17" fill="#ffe9d9" opacity=".9" letter-spacing="2">PROCESSOS  ·  INTEGRAÇÕES  ·  INTELIGÊNCIA ARTIFICIAL</text>'
         f'</g>')

css = """
.tw{animation:tw 4s ease-in-out infinite alternate}@keyframes tw{to{opacity:.15}}
.halo{transform-box:fill-box;transform-origin:center;animation:halo 6s ease-in-out infinite alternate}@keyframes halo{to{opacity:.75;transform:scale(1.05)}}
.nuvem{animation:nuvem linear infinite alternate}@keyframes nuvem{to{transform:translateX(70px)}}
.voo{animation:voo linear infinite}@keyframes voo{from{transform:translateX(-60px)}to{transform:translateX(1260px)}}
.asa{transform-box:fill-box;transform-origin:center;animation:asa .7s ease-in-out infinite alternate}@keyframes asa{to{transform:scaleY(.4)}}
.cursor{animation:cursor 1s steps(1) infinite}@keyframes cursor{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<title>Cauan Augusto - Engenheiro de Automações</title><style>{css}</style>{"".join(b)}</svg>')
with open(os.path.join(OUT, "banner.svg"), "w", encoding="utf-8") as fh:
    fh.write(svg)
print("ok")
