"""Gera a capa animada do perfil: noite de lua de sangue sobre montanhas e floresta.

Montanhas e florestas são faixas que se repetem a cada W pixels e rolam para a
esquerda em velocidades diferentes (paralaxe). O subtítulo alterna, digitando e
apagando, entre as frases de FRASES.

Uso: python gerar_banner.py assets
"""
import os, random, sys
from html import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 400
random.seed(42)
FRASES = ["Desenvolvedor Full-Stack", "IA & Automações", "Automation Developer", "Criação de Sites"]


def ridge_tile(y, rough, depth=7):
    """Linha de montanha que começa e termina na mesma altura (repete sem emenda)."""
    pts = [(0, y), (W, y)]
    amp = rough
    for _ in range(depth):
        nxt = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            nxt.append((x1, y1))
            nxt.append(((x1 + x2) / 2, (y1 + y2) / 2 + random.uniform(-amp, amp)))
        nxt.append(pts[-1])
        pts = nxt
        amp *= 0.55
    dobro = pts + [(x + W, yy) for x, yy in pts[1:]]
    d = " ".join(f"{x:.1f},{yy:.1f}" for x, yy in dobro)
    return f"0,{H} {d} {2*W},{H}"


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


def forest_tile(base, count, hmin, hmax):
    """Floresta periódica: cada árvore é desenhada em x-W, x e x+W."""
    out = []
    for _ in range(count):
        x = random.uniform(0, W)
        h = random.uniform(hmin, hmax)
        w = h * random.uniform(0.38, 0.48)
        yb = base + random.uniform(-4, 4)
        out += [pine(x + k * W, yb, h, w) for k in (-1, 0, 1)]
    return "".join(out)


def camada(conteudo, dur, cls="rola"):
    return f'<g class="{cls}" style="animation-duration:{dur}s">{conteudo}</g>'


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
<linearGradient id="nevoa" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b3121b" stop-opacity="0"/><stop offset="1" stop-color="#b3121b" stop-opacity=".3"/></linearGradient>
<linearGradient id="cadente" x1="0" x2="1"><stop offset="0" stop-color="#ffd0c8" stop-opacity="0"/><stop offset="1" stop-color="#fff0ee"/></linearGradient>
<radialGradient id="fagulha"><stop offset="0" stop-color="#ffb0a0"/><stop offset=".4" stop-color="#ff3b2f"/><stop offset="1" stop-color="#ff3b2f" stop-opacity="0"/></radialGradient>
<filter id="sombra" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity=".85"/></filter>
<filter id="aura" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="desfoque"><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="neblina" x="-20%" y="-100%" width="140%" height="300%"><feGaussianBlur stdDeviation="18"/></filter>
</defs>''')
b.append(f'<rect width="{W}" height="{H}" fill="url(#ceu)"/>')

# relâmpago vermelho ao fundo
b.append(f'<rect class="raio" width="{W}" height="{H}" fill="#ff2a2a"/>')

# estrelas cintilando
for _ in range(80):
    x, y = random.uniform(0, W), random.uniform(0, 190)
    r = random.choice([0.6, 0.8, 1, 1.3])
    b.append(f'<circle class="tw" style="animation-duration:{random.uniform(2, 5):.1f}s;animation-delay:-{random.uniform(0, 5):.1f}s" '
             f'cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#ffe3e0"/>')

# estrelas cadentes
for (x, y, dur, delay) in [(240, 40, 7, 0), (620, 20, 11, 4), (880, 60, 13, 8)]:
    b.append(f'<g class="cadente" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
             f'<line x1="{x}" y1="{y}" x2="{x+90}" y2="{y+30}" stroke="url(#cadente)" stroke-width="1.6" stroke-linecap="round"/></g>')

# lua de sangue: aura pulsando, anel que se expande e crateras girando
LX, LY, LR = 985, 128, 74
b.append(f'<circle class="halo" cx="{LX}" cy="{LY}" r="270" fill="url(#brilho)"/>'
         f'<circle class="onda" cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="#ff4d4d" stroke-width="2"/>'
         f'<circle class="onda" style="animation-delay:-2s" cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="#ff4d4d" stroke-width="2"/>'
         f'<g class="lua"><circle cx="{LX}" cy="{LY}" r="{LR}" fill="url(#lua)"/>'
         f'<clipPath id="disco"><circle cx="{LX}" cy="{LY}" r="{LR}"/></clipPath><g clip-path="url(#disco)"><g class="crateras">')
for (dx, dy, r, o) in [(-28, -20, 13, .38), (18, -32, 7, .3), (24, 10, 16, .32), (-14, 30, 9, .38), (-40, 14, 6, .28),
                       (40, -8, 5, .28), (4, 46, 6, .22), (-52, -24, 8, .25), (50, 34, 10, .25), (-6, -52, 5, .25)]:
    b.append(f'<circle cx="{LX+dx}" cy="{LY+dy}" r="{r}" fill="#5e0710" opacity="{o}" filter="url(#desfoque)"/>')
b.append(f'</g></g><circle cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="#ff8a7a" stroke-opacity=".3" stroke-width="1.5"/></g>')

# nuvens atravessando o céu (na frente da lua)
nuvens = []
for (x, y, w) in [(30, 120, 240), (420, 70, 180), (760, 112, 260), (1000, 176, 210), (200, 210, 170)]:
    for k in (0, 1):
        nuvens.append(f'<rect x="{x + k*W}" y="{y}" width="{w}" height="7" rx="3.5" fill="#1a0306" opacity=".6" filter="url(#desfoque)"/>'
                      f'<rect x="{x + k*W + w*0.18:.0f}" y="{y-5}" width="{w*0.5:.0f}" height="5" rx="2.5" fill="#ff4d4d" opacity=".14"/>')
b.append(camada("".join(nuvens), 95))

# montanhas e florestas em paralaxe (do fundo para a frente, cada vez mais rápido)
b.append(camada(f'<polygon points="{ridge_tile(208, 75)}" fill="#22050a" stroke="#7a0a12" stroke-opacity=".6" stroke-width="1.2"/>', 240))
b.append(camada(f'<polygon points="{ridge_tile(245, 60)}" fill="#160307" stroke="#9e0f18" stroke-opacity=".5" stroke-width="1.2"/>', 160))
b.append(f'<rect y="200" width="{W}" height="140" fill="url(#nevoa)"/>')
b.append(camada(f'<polygon points="{ridge_tile(288, 45)}" fill="#0e0205"/>', 110))
b.append(camada(f'<g fill="#0a0103">{forest_tile(358, 70, 34, 66)}</g>', 70))

# neblina vermelha andando entre as camadas
for (cx, cy, rx, dur, delay) in [(250, 330, 260, 26, 0), (800, 345, 300, 34, 9), (520, 315, 220, 30, 17)]:
    b.append(f'<g class="neblina" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
             f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="26" fill="#b3121b" opacity=".16" filter="url(#neblina)"/></g>')

b.append(camada(f'<g fill="#050001">{forest_tile(380, 55, 52, 96)}</g>', 45))
b.append(f'<rect y="376" width="{W}" height="{H-376}" fill="#030001"/>')
b.append(camada(f'<g fill="#020001">{forest_tile(404, 9, 140, 200)}</g>', 28))

# fagulhas subindo da floresta
for _ in range(45):
    x = random.uniform(0, W)
    y = random.uniform(330, 395)
    r = random.uniform(1.2, 2.6)
    dur = random.uniform(5, 11)
    sobe = random.uniform(140, 260)
    deriva = random.uniform(-40, 40)
    b.append(f'<g class="fagulha" style="--sobe:-{sobe:.0f}px;--deriva:{deriva:.0f}px;animation-duration:{dur:.1f}s;'
             f'animation-delay:-{random.uniform(0, dur):.1f}s"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="url(#fagulha)"/></g>')

# morcegos
for (y, dur, delay, s) in [(150, 22, 0, 1), (182, 30, 7, .8), (110, 36, 15, .7), (205, 40, 24, .9), (90, 26, 12, .6), (235, 34, 3, 1.1)]:
    b.append(f'<g class="voo" style="animation-duration:{dur}s;animation-delay:-{delay}s"><g class="plana" style="animation-delay:-{delay/3:.1f}s">'
             f'<g transform="translate(0,{y}) scale({s})">'
             f'<path class="asa" d="M12,6 q-4,-7 -12,-5 q5,2 4,6 q4,-2 6,2 q1,-3 2,-3 q1,0 2,3 q2,-4 6,-2 q-1,-4 4,-6 q-8,-2 -12,5z" fill="#050001"/>'
             f'</g></g></g>')

# texto: título com aura vermelha, subtítulo digitando e apagando, tagline flutuando
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'Courier New',Courier,monospace"
CX = 560
b.append(f'<g class="flutua">'
         f'<text class="aura" x="{CX}" y="132" text-anchor="middle" font-family="{FONT}" font-size="48" font-weight="700" fill="#ff2a2a" filter="url(#aura)">Olá, eu sou o Cauan</text>'
         f'<text x="{CX}" y="132" text-anchor="middle" font-family="{FONT}" font-size="48" font-weight="700" fill="#f5e6e6" letter-spacing="1" filter="url(#sombra)">Olá, eu sou o Cauan</text></g>')

# máquina de escrever (SMIL): a largura do recorte cresce letra a letra
FS = 26
CW = FS * 0.6  # largura de um caractere em fonte monoespaçada
CICLO = 20.0
JANELA = CICLO / len(FRASES)
DIGITA, APAGA = 0.075, 0.035
larguras, cursor_x, tempos = [], [], []
for i, frase in enumerate(FRASES):
    n = len(frase)
    esq = CX - n * CW / 2
    t0 = i * JANELA
    passos = [(t0 + k * DIGITA, k) for k in range(n + 1)]
    fim_digita = t0 + n * DIGITA
    inicio_apaga = t0 + JANELA - n * APAGA - 0.4
    passos += [(inicio_apaga + k * APAGA, n - k) for k in range(1, n + 1)]
    for t, k in passos:
        tempos.append(t / CICLO)
        larguras.append((i, k * CW))
        cursor_x.append(esq + k * CW)
kt = ";".join(f"{t:.4f}" for t in tempos)
b.append('<g class="flutua2">')
for i, frase in enumerate(FRASES):
    vals = ";".join(f"{w:.1f}" if j == i else "0" for j, w in larguras)
    esq = CX - len(frase) * CW / 2
    b.append(f'<clipPath id="digita{i}"><rect x="{esq:.1f}" y="150" height="44" width="0">'
             f'<animate attributeName="width" dur="{CICLO}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/></rect></clipPath>'
             f'<g clip-path="url(#digita{i})"><text x="{esq:.1f}" y="180" font-family="{MONO}" font-size="{FS}" font-weight="700" fill="#ff4d4d" '
             f'filter="url(#sombra)">{escape(frase)}</text></g>')
b.append(f'<rect class="cursor" y="158" width="3" height="28" fill="#ff4d4d">'
         f'<animate attributeName="x" dur="{CICLO}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" '
         f'values="{";".join(f"{x + 2:.1f}" for x in cursor_x)}"/></rect>')
b.append('</g>')
b.append(f'<g class="flutua3"><text x="{CX}" y="216" text-anchor="middle" font-family="{FONT}" font-size="17" fill="#e0cfd1" '
         f'letter-spacing="2" filter="url(#sombra)">PROCESSOS  ·  INTEGRAÇÕES  ·  INTELIGÊNCIA ARTIFICIAL</text>'
         f'<rect class="risco" x="{CX-120}" y="230" width="240" height="2" rx="1" fill="#ff4d4d"/></g>')

css = f"""
.rola{{animation:rola linear infinite}}@keyframes rola{{to{{transform:translateX(-{W}px)}}}}
.tw{{animation:tw ease-in-out infinite alternate}}@keyframes tw{{from{{opacity:.85}}to{{opacity:.1}}}}
.raio{{opacity:0;animation:raio 13s linear infinite}}
@keyframes raio{{0%,61%{{opacity:0}}61.5%{{opacity:.14}}62%{{opacity:.02}}62.6%{{opacity:.1}}64%,100%{{opacity:0}}}}
.cadente{{opacity:0;animation:cadente linear infinite}}
@keyframes cadente{{0%{{opacity:0;transform:translate(0,0)}}2%{{opacity:1}}9%{{opacity:0;transform:translate(260px,86px)}}100%{{opacity:0;transform:translate(260px,86px)}}}}
.halo{{transform-box:fill-box;transform-origin:center;animation:halo 5s ease-in-out infinite alternate}}@keyframes halo{{from{{opacity:.75}}to{{opacity:1;transform:scale(1.08)}}}}
.onda{{transform-box:fill-box;transform-origin:center;animation:onda 4s ease-out infinite}}@keyframes onda{{from{{opacity:.55;transform:scale(1)}}to{{opacity:0;transform:scale(1.9)}}}}
.lua{{transform-box:fill-box;transform-origin:center;animation:lua 7s ease-in-out infinite alternate}}@keyframes lua{{to{{transform:translateY(-6px) scale(1.02)}}}}
.crateras{{transform-box:view-box;transform-origin:{LX}px {LY}px;animation:gira 90s linear infinite}}@keyframes gira{{to{{transform:rotate(360deg)}}}}
.neblina{{animation:neblina ease-in-out infinite alternate}}@keyframes neblina{{from{{transform:translateX(-120px)}}to{{transform:translateX(160px)}}}}
.fagulha{{opacity:0;animation:fagulha linear infinite}}
@keyframes fagulha{{0%{{opacity:0;transform:translate(0,0)}}15%{{opacity:1}}70%{{opacity:.8}}100%{{opacity:0;transform:translate(var(--deriva),var(--sobe))}}}}
.voo{{animation:voo linear infinite}}@keyframes voo{{from{{transform:translateX(-60px)}}to{{transform:translateX({W+60}px)}}}}
.plana{{animation:plana 3s ease-in-out infinite alternate}}@keyframes plana{{to{{transform:translateY(-18px)}}}}
.asa{{transform-box:fill-box;transform-origin:center;animation:asa .22s ease-in-out infinite alternate}}@keyframes asa{{to{{transform:scaleY(.3)}}}}
.flutua{{animation:flutua 4.5s ease-in-out infinite alternate}}@keyframes flutua{{from{{transform:translateY(4px)}}to{{transform:translateY(-6px)}}}}
.flutua2{{animation:flutua 4.5s ease-in-out infinite alternate;animation-delay:-1.4s}}
.flutua3{{animation:flutua 4.5s ease-in-out infinite alternate;animation-delay:-2.8s}}
.aura{{animation:aura 2.6s ease-in-out infinite alternate}}@keyframes aura{{from{{opacity:.25}}to{{opacity:.8}}}}
.cursor{{animation:pisca .9s steps(1) infinite}}@keyframes pisca{{50%{{opacity:0}}}}
.risco{{transform-box:fill-box;transform-origin:center;animation:risco 3.5s ease-in-out infinite alternate}}@keyframes risco{{from{{transform:scaleX(.15);opacity:.4}}to{{transform:scaleX(1);opacity:.9}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<title>Cauan Augusto - Desenvolvedor Full-Stack, IA e Automações</title><style>{css}</style>{"".join(b)}</svg>')
with open(os.path.join(OUT, "banner.svg"), "w", encoding="utf-8") as fh:
    fh.write(svg)
print("ok")
