"""Gera os cards dinâmicos do perfil a partir de dados públicos do GitHub.

  indicadores.svg  contribuições, commits, repositórios e sequências
  atividade.svg    mapa de contribuições do último ano
  linguagens.svg   linguagens mais usadas nos repositórios públicos

Uso: python gerar_stats.py dist
Variáveis opcionais: GH_USER (padrão CauanDeveloper) e GITHUB_TOKEN (evita o limite de requisições).
"""
import json, os, re, sys, urllib.request
from datetime import date, datetime, timedelta, timezone
from html import escape
from estilo import FONT, TITLE, TEXT, MUTED, W, moldura, salvar, selo, titulo

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
USER = os.environ.get("GH_USER", "CauanDeveloper")
TOKEN = os.environ.get("GITHUB_TOKEN")
UA = {"User-Agent": "cauan-profile-stats"}

LANG_COLORS = {
    "JavaScript": "#f1e05a", "Python": "#3572A5", "Java": "#b07219", "HTML": "#e34c26", "CSS": "#663399",
    "TypeScript": "#3178c6", "Shell": "#89e051", "C": "#555555", "C++": "#f34b7d", "C#": "#178600",
}
FALLBACK = ["#ec8a62", "#b8546a", "#f7c07a", "#9a4767", "#6a2c55", "#c96f78"]
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
NIVEIS = ["#21192b", "#5a2a55", "#9a4767", "#d06a6a", "#f7c07a"]


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
    cor = LANG_COLORS.get(name, FALLBACK[i % len(FALLBACK)])
    pct = 100 * size / total
    x, y = 24 + (i % 2) * (colw + 40), 104 + (i // 2) * 46
    corpo.append(f'<circle cx="{x+5}" cy="{y-5}" r="5" fill="{cor}"/>'
                 f'<text x="{x+16}" y="{y}" font-family="{FONT}" font-size="14" font-weight="600" fill="{TEXT}">{escape(name)}</text>'
                 f'<text x="{x+colw}" y="{y}" text-anchor="end" font-family="{FONT}" font-size="13" fill="{MUTED}">{pct:.1f}%</text>'
                 f'<rect x="{x}" y="{y+10}" width="{colw:.1f}" height="6" rx="3" fill="#21262d"/>'
                 f'<rect class="barra" x="{x}" y="{y+10}" width="{max(colw * pct / 100, 6):.1f}" height="6" rx="3" fill="{cor}"/>')
salvar(os.path.join(OUT, "linguagens.svg"), W, LH, "Linguagens mais usadas",
       ".barra{transform-box:fill-box;transform-origin:left;animation:barra 1.2s ease-out both}"
       "@keyframes barra{from{transform:scaleX(0)}}", "".join(corpo))

print(f"ok: {len(repos)} repositórios, {len(langs)} linguagens, {total_ano} contribuições no ano, "
      f"sequência atual {atual}, maior {maior}")
