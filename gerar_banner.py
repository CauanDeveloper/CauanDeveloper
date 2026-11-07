"""Gera a capa do perfil: noite de lua de sangue sobre montanhas e floresta.

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
  <stop offset="0" stop-color="#020001"/>
  <stop offset=".4" stop-color="#0f0306"/>
  <stop offset=".7" stop-color="#2a050b"/>
  <stop offset=".9" stop-color="#4a0710"/>
  <stop offset="1" stop-color="#5e0a12"/>
</linearGradient>
<radialGradient id="brilho"><stop offset="0" stop-color="#ff2a2a" stop-opacity=".55"/><stop offset=".35" stop-color="#b3121b" stop-opacity=".22"/><stop offset="1" stop-color="#b3121b" stop-opacity="0"/></radialGradient>
<radialGradient id="lua" cx=".4" cy=".38" r=".7"><stop offset="0" stop-color="#ff6a52"/><stop offset=".45" stop-color="#d0201f"/><stop offset=".85" stop-color="#8a0b14"/><stop offset="1" stop-color="#5e0710"/></radialGradient>
<linearGradient id="nevoa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b3121b" stop-opacity="0"/><stop offset="1" stop-color="#b3121b" stop-opacity=".28"/></linearGradient>
<filter id="sombra" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity=".8"/></filter>
<filter id="desfoque"><feGaussianBlur stdDeviation="1.2"/></filter>
</defs>''')
b.append(f'<rect width="{W}" height="{H}" fill="url(#ceu)"/>')

# estrelas discretas
for _ in range(55):
    x, y = random.uniform(0, W), random.uniform(0, 170)
    r = random.choice([0.7, 0.9, 1.1])
    b.append(f'<circle class="tw" style="animation-delay:-{random.uniform(0, 4):.1f}s" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#ffe3e0" opacity=".55"/>')

# lua de sangue com crateras
LX, LY, LR = 985, 128, 74
b.append(f'<circle class="halo" cx="{LX}" cy="{LY}" r="260" fill="url(#brilho)"/>'
         f'<circle cx="{LX}" cy="{LY}" r="{LR}" fill="url(#lua)"/>')
for (dx, dy, r, o) in [(-28, -20, 13, .35), (18, -32, 7, .3), (24, 10, 16, .3), (-14, 30, 9, .35), (-40, 14, 6, .25), (40, -8, 5, .25), (4, 46, 6, .2)]:
    b.append(f'<circle cx="{LX+dx}" cy="{LY+dy}" r="{r}" fill="#5e0710" opacity="{o}" filter="url(#desfoque)"/>')
b.append(f'<circle cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="#ff8a7a" stroke-opacity=".25" stroke-width="1.5"/>')

# nuvens finas, algumas cruzando a lua
for (x, y, w, dur) in [(30, 120, 240, 70), (860, 112, 240, 90), (930, 178, 200, 80), (80, 214, 170, 100)]:
    b.append(f'<g class="nuvem" style="animation-duration:{dur}s"><rect x="{x}" y="{y}" width="{w}" height="7" rx="3.5" fill="#1a0306" opacity=".55" filter="url(#desfoque)"/>'
             f'<rect x="{x+w*0.18:.0f}" y="{y-5}" width="{w*0.5:.0f}" height="5" rx="2.5" fill="#ff4d4d" opacity=".12"/></g>')

# montanhas em silhueta com o contorno iluminado pela lua
for (yl, yr, rough, cor) in [(215, 200, 75, "#22050a"), (250, 238, 60, "#160307")]:
    b.append(f'<polygon points="{ridge(yl, yr, rough)}" fill="{cor}" stroke="#7a0a12" stroke-opacity=".55" stroke-width="1.2"/>')
b.append(f'<rect y="200" width="{W}" height="140" fill="url(#nevoa)"/>')
b.append(f'<polygon points="{ridge(290, 280, 45)}" fill="#0e0205"/>')

# floresta: três camadas
b.append(f'<g fill="#0a0103">{forest(358, 70, 34, 66)}</g>')
b.append(f'<g fill="#050001">{forest(380, 55, 52, 96)}</g>')
b.append(f'<rect y="376" width="{W}" height="{H-376}" fill="#030001"/>')
b.append(f'<g fill="#030001">{forest(402, 0, 130, 185, xs=[20, 75, 130, 1060, 1120, 1175])}</g>')

# morcegos
for (y, dur, delay, s) in [(150, 30, 0, 1), (182, 38, 9, .8), (110, 44, 20, .7), (205, 50, 31, .9)]:
    b.append(f'<g class="voo" style="animation-duration:{dur}s;animation-delay:-{delay}s"><g transform="translate(0,{y}) scale({s})">'
             f'<path class="asa" d="M12,6 q-4,-7 -12,-5 q5,2 4,6 q4,-2 6,2 q1,-3 2,-3 q1,0 2,3 q2,-4 6,-2 q-1,-4 4,-6 q-8,-2 -12,5z" fill="#050001"/></g></g>')

# texto
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'Cascadia Code','Consolas','Courier New',monospace"
b.append(f'<g filter="url(#sombra)" text-anchor="middle">'
         f'<text x="560" y="132" font-family="{FONT}" font-size="48" font-weight="700" fill="#f5e6e6" letter-spacing="1">Olá, eu sou o Cauan</text>'
         f'<text x="560" y="180" font-family="{MONO}" font-size="26" font-weight="600" fill="#ff4d4d">Engenheiro de Automações<tspan class="cursor">_</tspan></text>'
         f'<text x="560" y="214" font-family="{FONT}" font-size="17" fill="#e0cfd1" opacity=".9" letter-spacing="2">PROCESSOS  ·  INTEGRAÇÕES  ·  INTELIGÊNCIA ARTIFICIAL</text>'
         f'</g>')

css = """
.tw{animation:tw 4s ease-in-out infinite alternate}@keyframes tw{to{opacity:.15}}
.halo{transform-box:fill-box;transform-origin:center;animation:halo 6s ease-in-out infinite alternate}@keyframes halo{to{opacity:.7;transform:scale(1.06)}}
.nuvem{animation:nuvem linear infinite alternate}@keyframes nuvem{to{transform:translateX(70px)}}
.voo{animation:voo linear infinite}@keyframes voo{from{transform:translateX(-60px)}to{transform:translateX(1260px)}}
.asa{transform-box:fill-box;transform-origin:center;animation:asa .25s ease-in-out infinite alternate}@keyframes asa{to{transform:scaleY(.35)}}
.cursor{animation:cursor 1s steps(1) infinite}@keyframes cursor{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<title>Cauan Augusto - Engenheiro de Automações</title><style>{css}</style>{"".join(b)}</svg>')
with open(os.path.join(OUT, "banner.svg"), "w", encoding="utf-8") as fh:
    fh.write(svg)
print("ok")
