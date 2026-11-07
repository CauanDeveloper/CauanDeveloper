"""Gera os cards fixos do perfil: "O que eu faço", "Tecnologias" e os projetos em destaque.

Uso: python gerar_cards.py assets
Os ícones ficam em assets/icones (veja LICENCAS.txt).
"""
import os, sys
from estilo import FONT, CARD, TITLE, TEXT, MUTED, W, lucide, moldura, salvar, selo, simple_icon, titulo

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

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
CW, CH, GAP = 432, 142, 16
corpo = []
for i, (icone, nome, linhas) in enumerate(SERVICOS):
    x, y = (i % 2) * (CW + GAP), (i // 2) * (CH + GAP)
    corpo.append(f'<g transform="translate({x},{y})">{moldura(CW, CH)}{selo(22, 26, icone, 64, atraso=i * 0.7)}'
                 f'{titulo(108, 50, nome)}'
                 + "".join(f'<text x="108" y="{78 + k * 21}" font-family="{FONT}" font-size="14" fill="{MUTED}">{t}</text>'
                           for k, t in enumerate(linhas))
                 + "</g>")
salvar(os.path.join(OUT, "o-que-eu-faco.svg"), W, 2 * CH + GAP, "O que eu faço", "", "".join(corpo))

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
corpo = []
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
salvar(os.path.join(OUT, "tecnologias.svg"), W, TH + 12, "Tecnologias",
       ".tile{animation:tile 2.8s ease-in-out infinite alternate}@keyframes tile{to{transform:translateY(-5px)}}"
       ".brilho{animation:selo 2.8s ease-in-out infinite alternate}",
       "".join(corpo), defs)

# ---- Projetos em destaque (um SVG por projeto, para cada card ser um link) ---
PROJETOS = [
    ("projeto-portfolio.svg", "gamepad-2", "Portfólio interativo",
     ["Portfólio em pixel art em que uma personagem", "percorre o cenário apresentando os projetos."],
     ("JavaScript", "#f1e05a"), "Repositório público"),
    ("projeto-computacao-visual.svg", "scan-eye", "computacao-visual",
     ["Experimentos de visão computacional", "rodando direto no navegador."],
     ("JavaScript", "#f1e05a"), "Repositório público"),
    ("projeto-artista-moveis.svg", "armchair", "Artista Móveis Rústicos",
     ["Site institucional desenvolvido para", "a empresa Artista Móveis Rústicos."],
     ("HTML", "#e34c26"), "Projeto para cliente"),
]
PW, PH = 432, 150
for arquivo, icone, nome, linhas, (lang, cor), tipo in PROJETOS:
    privado = tipo != "Repositório público"
    corpo = [moldura(PW, PH), selo(22, 24, icone, 48), titulo(86, 46, nome, 17)]
    corpo.append(f'<g transform="translate(398,22) scale(.75)" fill="none" stroke="{MUTED}" stroke-width="2" '
                 f'stroke-linecap="round" stroke-linejoin="round">{lucide("lock" if privado else "arrow-up-right")}</g>')
    corpo += [f'<text x="86" y="{72 + k * 20}" font-family="{FONT}" font-size="13.5" fill="{MUTED}">{t}</text>'
              for k, t in enumerate(linhas)]
    corpo.append(f'<line x1="22" y1="112" x2="{PW-22}" y2="112" stroke="#21262d"/>'
                 f'<circle cx="28" cy="130" r="6" fill="{cor}"/>'
                 f'<text x="40" y="135" font-family="{FONT}" font-size="13" fill="{TEXT}">{lang}</text>'
                 f'<text x="{PW-22}" y="135" text-anchor="end" font-family="{FONT}" font-size="12" fill="{MUTED}">{tipo}</text>')
    salvar(os.path.join(OUT, arquivo), PW, PH, nome, "", "".join(corpo))
print("ok")
