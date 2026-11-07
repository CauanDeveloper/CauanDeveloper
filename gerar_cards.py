"""Gera os cards "O que eu faço" e "Tecnologias" do perfil, no tema da capa.

Uso: python gerar_cards.py assets
Os ícones ficam em assets/icones (veja LICENCAS.txt).
"""
import os, re, sys

OUT = sys.argv[1]
ICONES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icones")
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
CARD, BORDER, TITLE, TEXT, MUTED = "#161b22", "#30363d", "#e6edf3", "#c9d1d9", "#8b949e"

GRADIENTES = '''<linearGradient id="por-do-sol" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#5a2a55"/><stop offset=".5" stop-color="#b8546a"/><stop offset="1" stop-color="#f7c07a"/>
</linearGradient>
<linearGradient id="faixa" x1="0" x2="1"><stop offset="0" stop-color="#5a2a55"/><stop offset=".5" stop-color="#b8546a"/><stop offset="1" stop-color="#f7c07a"/></linearGradient>'''


def simple_icon(nome):
    """Caminho do Simple Icons (24x24, preenchido)."""
    svg = open(os.path.join(ICONES, nome + ".svg"), encoding="utf-8").read()
    return re.search(r'<path d="([^"]+)"', svg).group(1)


def lucide(nome):
    """Elementos internos do Lucide (24x24, traço)."""
    svg = open(os.path.join(ICONES, nome + ".svg"), encoding="utf-8").read()
    corpo = svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]
    return re.sub(r"\s+", " ", corpo).strip()


def salvar(nome, w, h, titulo, css, corpo):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<title>{titulo}</title><style>{css}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
           f'<defs>{GRADIENTES}</defs>{corpo}</svg>')
    with open(os.path.join(OUT, nome), "w", encoding="utf-8") as fh:
        fh.write(svg)


# ---- O que eu faço ----------------------------------------------------------
SERVICOS = [
    ("workflow", "Automação de processos",
     ["Mapeio rotinas manuais e crio fluxos", "que rodam sozinhos, com menos erros", "e mais tempo livre para a equipe."]),
    ("plug-zap", "Integrações",
     ["Conecto sistemas que não conversam", "entre si usando APIs, webhooks e", "troca de dados automatizada."]),
    ("brain-circuit", "Inteligência artificial",
     ["Agentes e fluxos com IA que leem,", "classificam e respondem, aplicados", "a problemas reais do dia a dia."]),
    ("code-xml", "Desenvolvimento",
     ["Scripts e ferramentas em Python e", "JavaScript, e interfaces web para", "acompanhar e operar as automações."]),
]
W, CW, CH, GAP = 880, 432, 142, 16
corpo = []
for i, (icone, titulo, linhas) in enumerate(SERVICOS):
    x, y = (i % 2) * (CW + GAP), (i // 2) * (CH + GAP)
    corpo.append(f'<g transform="translate({x},{y})">'
                 f'<rect x=".5" y=".5" width="{CW-1}" height="{CH-1}" rx="14" fill="{CARD}" stroke="{BORDER}"/>'
                 f'<rect x="14" y=".5" width="{CW-28}" height="2.5" rx="1.25" fill="url(#faixa)"/>'
                 f'<g class="selo" style="animation-delay:-{i * 0.7:.1f}s">'
                 f'<rect x="22" y="26" width="64" height="64" rx="16" fill="url(#por-do-sol)"/>'
                 f'<rect x="22" y="26" width="64" height="64" rx="16" fill="none" stroke="#fff" stroke-opacity=".25"/></g>'
                 f'<g transform="translate(36,40) scale(1.5)" fill="none" stroke="#fff" stroke-width="1.8" '
                 f'stroke-linecap="round" stroke-linejoin="round">{lucide(icone)}</g>'
                 f'<text x="108" y="50" font-family="{FONT}" font-size="18" font-weight="600" fill="{TITLE}">{titulo}</text>'
                 + "".join(f'<text x="108" y="{78 + k * 21}" font-family="{FONT}" font-size="14" fill="{MUTED}">{t}</text>'
                           for k, t in enumerate(linhas))
                 + "</g>")
salvar("o-que-eu-faco.svg", W, 2 * CH + GAP, "O que eu faço",
       ".selo{animation:selo 3.2s ease-in-out infinite alternate}@keyframes selo{to{opacity:.72}}", "".join(corpo))

# ---- Tecnologias ------------------------------------------------------------
TECNOLOGIAS = [
    ("python", "Python", "#5a9fd4"),
    ("javascript", "JavaScript", "#f7df1e"),
    ("openjdk", "Java", "#f89820"),
    ("html5", "HTML5", "#e34f26"),
    ("css3", "CSS3", "#2965f1"),
    ("git", "Git", "#f05032"),
    ("githubactions", "Actions", "#2088ff"),
    ("webhook", "APIs", "#ec8a62"),
]
TW, TH = 100, 128
gap = (W - len(TECNOLOGIAS) * TW) / (len(TECNOLOGIAS) - 1)
defs = "".join(f'<radialGradient id="brilho{i}"><stop offset="0" stop-color="{cor}" stop-opacity=".35"/>'
               f'<stop offset="1" stop-color="{cor}" stop-opacity="0"/></radialGradient>'
               for i, (_, _, cor) in enumerate(TECNOLOGIAS))
corpo = [f"<defs>{defs}</defs>"]
for i, (icone, nome, cor) in enumerate(TECNOLOGIAS):
    x = i * (TW + gap)
    if icone == "webhook":
        desenho = (f'<g transform="translate(30,26) scale(1.67)" fill="none" stroke="{cor}" stroke-width="2" '
                   f'stroke-linecap="round" stroke-linejoin="round">{lucide(icone)}</g>')
    else:
        desenho = f'<g transform="translate(30,26) scale(1.67)"><path d="{simple_icon(icone)}" fill="{cor}"/></g>'
    corpo.append(f'<g transform="translate({x:.1f},6)"><g class="tile" style="animation-delay:-{i * 0.35:.2f}s">'
                 f'<rect x=".5" y=".5" width="{TW-1}" height="{TH-1}" rx="16" fill="{CARD}" stroke="url(#por-do-sol)" stroke-opacity=".7"/>'
                 f'<circle class="brilho" cx="50" cy="46" r="40" fill="url(#brilho{i})"/>'
                 f'{desenho}'
                 f'<text x="50" y="106" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="{TEXT}">{nome}</text>'
                 f'</g></g>')
salvar("tecnologias.svg", W, TH + 12, "Tecnologias",
       ".tile{animation:tile 2.8s ease-in-out infinite alternate}@keyframes tile{to{transform:translateY(-5px)}}"
       ".brilho{animation:selo 2.8s ease-in-out infinite alternate}@keyframes selo{to{opacity:.45}}",
       "".join(corpo))
print("ok")
