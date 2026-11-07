"""Estilo compartilhado pelos cards do perfil (cores, fontes, ícones e moldura)."""
import os, re

ICONES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icones")
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
CARD, BORDER, TITLE, TEXT, MUTED, ACCENT = "#110a0c", "#3a1a1f", "#f5e6e6", "#e0cfd1", "#a3878a", "#ff4d4d"
# tons de vermelho do tema lua de sangue, do mais escuro ao mais claro
SANGUE = ["#3d0208", "#7a0a12", "#b3121b", "#e0242c", "#ff4d4d", "#ff8a7a"]
W = 880  # largura padrão dos cards de largura total

GRADIENTES = '''<linearGradient id="sangue" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#2a0206"/><stop offset=".55" stop-color="#9e0f18"/><stop offset="1" stop-color="#ff4d4d"/>
</linearGradient>
<linearGradient id="faixa" x1="0" x2="1"><stop offset="0" stop-color="#2a0206" stop-opacity="0"/><stop offset=".5" stop-color="#e0242c"/><stop offset="1" stop-color="#2a0206" stop-opacity="0"/></linearGradient>'''


def simple_icon(nome):
    """Caminho do Simple Icons (24x24, preenchido)."""
    svg = open(os.path.join(ICONES, nome + ".svg"), encoding="utf-8").read()
    return re.search(r'<path d="([^"]+)"', svg).group(1)


def lucide(nome):
    """Elementos internos do Lucide (24x24, traço)."""
    svg = open(os.path.join(ICONES, nome + ".svg"), encoding="utf-8").read()
    corpo = svg[svg.index(">", svg.index("<svg")) + 1:svg.rindex("</svg>")]
    return re.sub(r"\s+", " ", corpo).strip()


def moldura(w, h, rx=14):
    """Fundo do card com a faixa vermelha no topo."""
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{CARD}" stroke="{BORDER}"/>'
            f'<rect x="{rx}" y=".5" width="{w-2*rx}" height="2.5" rx="1.25" fill="url(#faixa)"/>')


def selo(x, y, icone, tam=40, classe="selo", atraso=0):
    """Quadrado com degradê vermelho e um ícone Lucide claro no centro."""
    escala = tam * 0.55 / 24
    off = (tam - 24 * escala) / 2
    return (f'<g class="{classe}" style="animation-delay:-{atraso:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{tam}" height="{tam}" rx="{tam*0.25:.1f}" fill="url(#sangue)"/>'
            f'<rect x="{x}" y="{y}" width="{tam}" height="{tam}" rx="{tam*0.25:.1f}" fill="none" stroke="#ff8a7a" stroke-opacity=".35"/></g>'
            f'<g transform="translate({x+off:.1f},{y+off:.1f}) scale({escala:.3f})" fill="none" stroke="#fff0ee" stroke-width="{1.8/escala*0.9:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{lucide(icone)}</g>')


def titulo(x, y, texto, tam=18):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{tam}" font-weight="600" fill="{TITLE}">{texto}</text>'


def salvar(caminho, w, h, nome, css, corpo, defs=""):
    css += ".selo{animation:selo 3.2s ease-in-out infinite alternate}@keyframes selo{to{opacity:.68}}"
    css += "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<title>{nome}</title><style>{css}</style><defs>{GRADIENTES}{defs}</defs>{corpo}</svg>')
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(svg)
