"""Gera os cards dinâmicos do perfil a partir de dados públicos do GitHub.

  indicadores.svg  contribuições, commits, repositórios e sequências
  atividade.svg    mapa de contribuições do último ano
  linguagens.svg   linguagens mais usadas nos repositórios públicos
  cobrinha.svg     jogo da cobrinha caçando os dias com commits

Uso: python gerar_stats.py dist
Variáveis opcionais: GH_USER (padrão CauanDeveloper) e GITHUB_TOKEN (evita o limite de requisições).
"""
import json, os, re, sys, urllib.request
from datetime import date, datetime, timedelta, timezone
from html import escape
from estilo import FONT, TITLE, TEXT, MUTED, SANGUE, W, moldura, salvar, selo, titulo

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
USER = os.environ.get("GH_USER", "CauanDeveloper")
TOKEN = os.environ.get("GITHUB_TOKEN")
UA = {"User-Agent": "cauan-profile-stats"}

# cores das linguagens por posição no ranking, todas em tons de vermelho
CORES_LINGUAGENS = [SANGUE[4], SANGUE[3], SANGUE[5], SANGUE[2], "#ff6b5e", SANGUE[1]]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
NIVEIS = ["#1c0f12", "#5c0a12", "#9e0f18", "#e0242c", "#ff6b5e"]


def abrir(url, api=True):
    headers = dict(UA)
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read().decode("utf-8")


def get(url):
    return json.loads(abrir(url))


# ---- dados ------------------------------------------------------------------
repos = [r for r in get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
langs = {}
for r in repos:
    for name, size in get(r["languages_url"]).items():
        langs[name] = langs.get(name, 0) + size
commits = get(f"https://api.github.com/search/commits?q=author:{USER}&per_page=1")["total_count"]

# calendário público de contribuições (o mesmo que aparece no perfil)
pagina = abrir(f"https://github.com/users/{USER}/contributions", api=False)
dias = {}  # id do quadrado -> (data, nível)
for m in re.finditer(r'data-date="(\d{4}-\d\d-\d\d)" id="([^"]+)" data-level="(\d)"', pagina):
    dias[m.group(2)] = (date.fromisoformat(m.group(1)), int(m.group(3)))
qtd = {}
for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', pagina):
    n = re.match(r"(\d+) contribution", m.group(2))
    qtd[m.group(1)] = int(n.group(1)) if n else 0
if len(dias) < 300:
    sys.exit(f"Calendário de contribuições não reconhecido ({len(dias)} dias); nada foi publicado.")
calendario = sorted((d, nivel, qtd.get(i, 0)) for i, (d, nivel) in dias.items())

total_ano = sum(c for _, _, c in calendario)
maior = atual = seq = 0
for _, _, c in calendario:
    seq = seq + 1 if c else 0
    maior = max(maior, seq)
# a sequência atual não quebra só porque hoje ainda não teve contribuição
for d, _, c in reversed(calendario):
    if c:
        atual += 1
    elif d != calendario[-1][0]:
        break
hoje = datetime.now(timezone.utc).strftime("%d/%m/%Y")

# ---- indicadores ------------------------------------------------------------
INDICADORES = [
    ("activity", total_ano, "Contribuições no ano"),
    ("git-commit-horizontal", commits, "Commits públicos"),
    ("folder-git-2", len(repos), "Repositórios públicos"),
    ("flame", atual, "Sequência atual (dias)"),
    ("trophy", maior, "Maior sequência (dias)"),
]
KW, KH = 166, 124
gap = (W - len(INDICADORES) * KW) / (len(INDICADORES) - 1)
corpo = []
for i, (icone, valor, rotulo) in enumerate(INDICADORES):
    x = i * (KW + gap)
    corpo.append(f'<g transform="translate({x:.1f},0)">{moldura(KW, KH, 14)}{selo(16, 18, icone, 36, atraso=i * 0.6)}'
                 f'<text x="16" y="90" font-family="{FONT}" font-size="30" font-weight="700" fill="{TITLE}">{valor}</text>'
                 f'<text x="16" y="110" font-family="{FONT}" font-size="12" fill="{MUTED}">{escape(rotulo)}</text></g>')
salvar(os.path.join(OUT, "indicadores.svg"), W, KH, "Indicadores no GitHub", "", "".join(corpo))

# ---- atividade --------------------------------------------------------------
CEL, PASSO = 12, 15.2
X0, Y0 = 50, 92
semanas = []
for d, nivel, c in calendario:
    if not semanas or d.weekday() == 6:  # semana começa no domingo, como no GitHub
        semanas.append([])
    semanas[-1].append((d, nivel, c))
AH = Y0 + 7 * PASSO + 46
corpo = [moldura(W, AH), selo(24, 22, "activity", 40), titulo(76, 40, "Atividade no último ano"),
         f'<text x="76" y="60" font-family="{FONT}" font-size="13" fill="{MUTED}">Contribuições públicas dia a dia</text>',
         f'<text x="{W-24}" y="44" text-anchor="end" font-family="{FONT}" font-size="26" font-weight="700" fill="{TITLE}">{total_ano}</text>',
         f'<text x="{W-24}" y="62" text-anchor="end" font-family="{FONT}" font-size="12" fill="{MUTED}">contribuições</text>']
for rot, wd in (("seg", 1), ("qua", 3), ("sex", 5)):
    corpo.append(f'<text x="{X0-10}" y="{Y0 + wd * PASSO + 10}" text-anchor="end" font-family="{FONT}" font-size="11" fill="{MUTED}">{rot}</text>')
mes_anterior = None
for s, semana in enumerate(semanas):
    x = X0 + s * PASSO
    primeiro = semana[0][0]
    if primeiro.month != mes_anterior and primeiro.day <= 7 and s < len(semanas) - 2:
        corpo.append(f'<text x="{x:.1f}" y="{Y0-8}" font-family="{FONT}" font-size="11" fill="{MUTED}">{MESES[primeiro.month-1]}</text>')
    mes_anterior = primeiro.month
    for d, nivel, c in semana:
        y = Y0 + ((d.weekday() + 1) % 7) * PASSO
        corpo.append(f'<rect class="cel" style="animation-delay:{s * 0.012:.3f}s" x="{x:.1f}" y="{y:.1f}" width="{CEL}" height="{CEL}" rx="3" fill="{NIVEIS[nivel]}"/>')
ly = AH - 20
corpo.append(f'<text x="{X0}" y="{ly}" font-family="{FONT}" font-size="11" fill="{MUTED}">Atualizado em {hoje}</text>')
lx = W - 24 - 5 * 16 - 40
corpo.append(f'<text x="{lx-8}" y="{ly}" text-anchor="end" font-family="{FONT}" font-size="11" fill="{MUTED}">Menos</text>')
for k, cor in enumerate(NIVEIS):
    corpo.append(f'<rect x="{lx + k*16}" y="{ly-10}" width="{CEL}" height="{CEL}" rx="3" fill="{cor}"/>')
corpo.append(f'<text x="{lx + 5*16 + 4}" y="{ly}" font-family="{FONT}" font-size="11" fill="{MUTED}">Mais</text>')
salvar(os.path.join(OUT, "atividade.svg"), W, int(AH), "Atividade no último ano",
       ".cel{animation:cel .5s ease-out both}@keyframes cel{from{opacity:0;transform:translateY(4px)}}", "".join(corpo))

# ---- linguagens -------------------------------------------------------------
total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
linhas = (len(top) + 1) // 2
LH = 92 + linhas * 46 + 8
corpo = [moldura(W, LH), selo(24, 22, "code", 40), titulo(76, 40, "Linguagens mais usadas"),
         f'<text x="76" y="60" font-family="{FONT}" font-size="13" fill="{MUTED}">Volume de código nos repositórios públicos</text>']
colw = (W - 48 - 40) / 2
for i, (name, size) in enumerate(top):
    cor = CORES_LINGUAGENS[i % len(CORES_LINGUAGENS)]
    pct = 100 * size / total
    x, y = 24 + (i % 2) * (colw + 40), 104 + (i // 2) * 46
    corpo.append(f'<circle cx="{x+5}" cy="{y-5}" r="5" fill="{cor}"/>'
                 f'<text x="{x+16}" y="{y}" font-family="{FONT}" font-size="14" font-weight="600" fill="{TEXT}">{escape(name)}</text>'
                 f'<text x="{x+colw}" y="{y}" text-anchor="end" font-family="{FONT}" font-size="13" fill="{MUTED}">{pct:.1f}%</text>'
                 f'<rect x="{x}" y="{y+10}" width="{colw:.1f}" height="6" rx="3" fill="#2a1216"/>'
                 f'<rect class="barra" x="{x}" y="{y+10}" width="{max(colw * pct / 100, 6):.1f}" height="6" rx="3" fill="{cor}"/>')
salvar(os.path.join(OUT, "linguagens.svg"), W, LH, "Linguagens mais usadas",
       ".barra{transform-box:fill-box;transform-origin:left;animation:barra 1.2s ease-out both}"
       "@keyframes barra{from{transform:scaleX(0)}}", "".join(corpo))

# ---- jogo da cobrinha -------------------------------------------------------
# A cobra entra pela esquerda, vai até o dia com commit mais próximo (menor caminho
# em passos de grade), come, segue para o próximo e sai pela direita. O corpo é a
# mesma animação da cabeça, atrasada um passo por segmento.
MONO = "'Courier New',Courier,monospace"
GX0, GY0 = 37, 74
COLS = len(semanas)
GH = GY0 + 7 * PASSO + 42
celulas = {}
for s, semana in enumerate(semanas):
    for d, nivel, c in semana:
        celulas[(s, (d.weekday() + 1) % 7)] = (nivel, c)
alvos = [k for k, (_, c) in celulas.items() if c]

caminho = [(-3, 3), (-2, 3), (-1, 3)]
pos = (0, 3)
caminho.append(pos)
pendentes = set(alvos)
while pendentes:
    alvo = min(pendentes, key=lambda a: (abs(a[0] - pos[0]) + abs(a[1] - pos[1]), a))
    while pos != alvo:  # anda primeiro na direção com maior distância
        dx, dy = alvo[0] - pos[0], alvo[1] - pos[1]
        if abs(dx) >= abs(dy):
            pos = (pos[0] + (1 if dx > 0 else -1), pos[1])
        else:
            pos = (pos[0], pos[1] + (1 if dy > 0 else -1))
        caminho.append(pos)
    pendentes.discard(alvo)
while pos[0] < COLS + 3:
    pos = (pos[0] + 1, pos[1])
    caminho.append(pos)

SEGMENTOS = 7
DT = 0.11
TOTAL = (len(caminho) + SEGMENTOS) * DT
pct = lambda i: 100 * i * DT / TOTAL
frames = "".join(f"{pct(i):.3f}%{{transform:translate({GX0 + cx * PASSO:.1f}px,{GY0 + cy * PASSO:.1f}px)}}"
                 for i, (cx, cy) in enumerate(caminho))
ultimo = caminho[-1]
frames += f"100%{{transform:translate({GX0 + ultimo[0] * PASSO:.1f}px,{GY0 + ultimo[1] * PASSO:.1f}px)}}"
css = [f".seg{{animation:cobra {TOTAL:.2f}s linear infinite backwards}}@keyframes cobra{{{frames}}}",
       ".brilho-c{animation:selo 1.4s ease-in-out infinite alternate}",
       ".pisca{animation:pisca 1s steps(1) infinite}@keyframes pisca{50%{opacity:0}}"]

corpo = [f'<rect width="{W}" height="{GH:.0f}" rx="10" fill="#070304"/>',
         f'<rect x="5" y="5" width="{W-10}" height="{GH-10:.0f}" rx="8" fill="none" stroke="#7a0a12" stroke-width="3"/>',
         f'<rect x="12" y="12" width="{W-24}" height="{GH-24:.0f}" rx="5" fill="none" stroke="#e0242c" stroke-width="1.2" stroke-opacity=".8"/>',
         f'<rect x="28" y="-1" width="232" height="30" fill="#070304" stroke="#e0242c" stroke-width="1.5"/>',
         f'<text x="144" y="20" text-anchor="middle" font-family="{MONO}" font-size="16" font-weight="700" fill="#f5e6e6" letter-spacing="2">CAÇA AOS COMMITS</text>',
         f'<text x="{W-30}" y="44" text-anchor="end" font-family="{MONO}" font-size="13" font-weight="700" fill="{SANGUE[4]}" letter-spacing="1">'
         f'COMMITS NO ANO <tspan fill="#f5e6e6">{total_ano:03d}</tspan></text>',
         f'<text x="30" y="44" font-family="{MONO}" font-size="13" font-weight="700" fill="{SANGUE[4]}" letter-spacing="1">'
         f'1UP<tspan class="pisca" fill="#f5e6e6"> ▮</tspan></text>',
         f'<clipPath id="arena"><rect x="18" y="{GY0-8}" width="{W-36}" height="{7 * PASSO + 14:.0f}"/></clipPath>',
         '<g clip-path="url(#arena)">']
for (cx, cy), (nivel, c) in celulas.items():
    x, y = GX0 + cx * PASSO + CEL / 2, GY0 + cy * PASSO + CEL / 2
    if not c:
        corpo.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.6" fill="#4a1a20"/>')
for j, alvo in enumerate(alvos):
    nivel, c = celulas[alvo]
    x, y = GX0 + alvo[0] * PASSO + CEL / 2, GY0 + alvo[1] * PASSO + CEL / 2
    p = pct(caminho.index(alvo))
    css.append(f".a{j}{{animation:a{j} {TOTAL:.2f}s step-end infinite}}"
               f"@keyframes a{j}{{0%{{opacity:1}}{p:.3f}%{{opacity:0}}100%{{opacity:0}}}}"
               f".m{j}{{opacity:0;animation:m{j} {TOTAL:.2f}s linear infinite}}"
               f"@keyframes m{j}{{0%,{p:.3f}%{{opacity:0;transform:translateY(0)}}{p + 0.3:.3f}%{{opacity:1}}"
               f"{p + 6:.3f}%{{opacity:0;transform:translateY(-14px)}}100%{{opacity:0;transform:translateY(-14px)}}}}")
    corpo.append(f'<g class="a{j}"><circle class="brilho-c" cx="{x:.1f}" cy="{y:.1f}" r="8" fill="url(#halo)"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{NIVEIS[max(nivel, 2)]}" stroke="#ff8a7a" stroke-width="1"/></g>'
                 f'<text class="m{j}" x="{x:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-family="{MONO}" font-size="11" '
                 f'font-weight="700" fill="#ff8a7a">+{c}</text>')
for k in reversed(range(SEGMENTOS)):
    t = k / (SEGMENTOS - 1)
    cor = SANGUE[4] if k == 0 else ["#e0242c", "#c81e28", "#b3121b", "#9e0f18", "#7a0a12", "#5c0a12"][k - 1]
    tam = CEL if k == 0 else CEL - 1 - t * 2
    off = (CEL - tam) / 2
    peca = f'<rect x="{off:.1f}" y="{off:.1f}" width="{tam:.1f}" height="{tam:.1f}" rx="{3.5 if k else 4}" fill="{cor}"/>'
    if k == 0:
        peca = (f'<circle cx="{CEL/2}" cy="{CEL/2}" r="11" fill="url(#halo)"/>{peca}'
                f'<rect x="3" y="3" width="3" height="3" rx="1" fill="#fff0ee"/><rect x="7" y="3" width="3" height="3" rx="1" fill="#fff0ee"/>')
    corpo.append(f'<g class="seg" style="animation-delay:{k * DT:.2f}s">{peca}</g>')
corpo.append("</g>")
corpo.append(f'<text x="{W/2}" y="{GH-20:.0f}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#7a5a5e" letter-spacing="1">'
             f'CADA PONTO VERMELHO É UM DIA COM COMMIT NO ÚLTIMO ANO</text>')
salvar(os.path.join(OUT, "cobrinha.svg"), W, int(GH), "Caça aos commits", "".join(css), "".join(corpo),
       '<radialGradient id="halo"><stop offset="0" stop-color="#ff2a2a" stop-opacity=".55"/>'
       '<stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></radialGradient>')

print(f"ok: {len(repos)} repositórios, {len(langs)} linguagens, {total_ano} contribuições no ano, "
      f"sequência atual {atual}, maior {maior}")
