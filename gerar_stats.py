"""Gera os cards de estatísticas do perfil (resumo e linguagens) a partir da API do GitHub.

Uso: python gerar_stats.py dist
Variáveis opcionais: GH_USER (padrão CauanDeveloper) e GITHUB_TOKEN (evita o limite de requisições).
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone
from html import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
USER = os.environ.get("GH_USER", "CauanDeveloper")
TOKEN = os.environ.get("GITHUB_TOKEN")

BG, BORDER, TITLE, TEXT, MUTED, ICON = "#0d1117", "#30363d", "#ec8a62", "#c9d1d9", "#8b949e", "#f7c07a"
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
LANG_COLORS = {
    "JavaScript": "#f1e05a", "Python": "#3572A5", "Java": "#b07219", "HTML": "#e34c26", "CSS": "#663399",
    "TypeScript": "#3178c6", "Shell": "#89e051", "C": "#555555", "C++": "#f34b7d", "C#": "#178600",
}
FALLBACK = ["#ec8a62", "#b8546a", "#f7c07a", "#9a4767", "#6a2c55", "#c96f78"]


def get(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "cauan-profile-stats"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return json.load(r)


user = get(f"https://api.github.com/users/{USER}")
repos = [r for r in get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
langs = {}
for r in repos:
    for name, size in get(r["languages_url"]).items():
        langs[name] = langs.get(name, 0) + size

stars = sum(r["stargazers_count"] for r in repos)
commits = get(f"https://api.github.com/search/commits?q=author:{USER}&per_page=1")["total_count"]
since = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00")).year
today = datetime.now(timezone.utc).strftime("%d/%m/%Y")


def card(title, inner, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="{h}" viewBox="0 0 440 {h}">'
            f'<defs><linearGradient id="faixa" x1="0" x2="1"><stop offset="0" stop-color="#5a2a55"/>'
            f'<stop offset=".5" stop-color="#b8546a"/><stop offset="1" stop-color="#f7c07a"/></linearGradient></defs>'
            f'<rect x=".5" y=".5" width="439" height="{h-1}" rx="6" fill="{BG}" stroke="{BORDER}"/>'
            f'<rect x="1" y="1" width="438" height="4" rx="2" fill="url(#faixa)"/>'
            f'<text x="24" y="38" font-family="{FONT}" font-size="17" font-weight="600" fill="{TITLE}">{escape(title)}</text>'
            f'{inner}'
            f'<text x="416" y="{h-14}" text-anchor="end" font-family="{FONT}" font-size="10" fill="{MUTED}">Atualizado em {today}</text>'
            f'</svg>')


# ---- resumo -----------------------------------------------------------------
rows = [
    ("Repositórios públicos", len(repos)),
    ("Commits públicos", commits),
    ("Seguidores", user["followers"]),
    ("Linguagens utilizadas", len(langs)),
    ("No GitHub desde", since),
]
if stars:
    rows.insert(2, ("Estrelas recebidas", stars))
inner = []
for i, (label, value) in enumerate(rows):
    y = 72 + i * 26
    inner.append(f'<rect x="24" y="{y-9}" width="8" height="8" rx="2" fill="{ICON}"/>'
                 f'<text x="42" y="{y}" font-family="{FONT}" font-size="14" fill="{TEXT}">{escape(label)}</text>'
                 f'<text x="416" y="{y}" text-anchor="end" font-family="{FONT}" font-size="14" font-weight="600" fill="{TEXT}">{value}</text>')
with open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8") as fh:
    fh.write(card("Resumo no GitHub", "".join(inner), 210))

# ---- linguagens -------------------------------------------------------------
total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
inner = []
x = 24
bar_w = 392
inner.append(f'<clipPath id="barra"><rect x="24" y="56" width="{bar_w}" height="10" rx="5"/></clipPath><g clip-path="url(#barra)">')
colors = {}
for i, (name, size) in enumerate(top):
    colors[name] = LANG_COLORS.get(name, FALLBACK[i % len(FALLBACK)])
    w = bar_w * size / sum(s for _, s in top)
    inner.append(f'<rect x="{x:.1f}" y="56" width="{w + 1:.1f}" height="10" fill="{colors[name]}"/>')
    x += w
inner.append("</g>")
for i, (name, size) in enumerate(top):
    col, row = i % 2, i // 2
    lx, ly = 24 + col * 200, 98 + row * 26
    inner.append(f'<circle cx="{lx+5}" cy="{ly-5}" r="5" fill="{colors[name]}"/>'
                 f'<text x="{lx+16}" y="{ly}" font-family="{FONT}" font-size="14" fill="{TEXT}">{escape(name)}</text>'
                 f'<text x="{lx+180}" y="{ly}" text-anchor="end" font-family="{FONT}" font-size="14" fill="{MUTED}">{100 * size / total:.1f}%</text>')
with open(os.path.join(OUT, "linguagens.svg"), "w", encoding="utf-8") as fh:
    fh.write(card("Linguagens mais usadas", "".join(inner), 210))

print(f"ok: {len(repos)} repositórios, {len(langs)} linguagens")
