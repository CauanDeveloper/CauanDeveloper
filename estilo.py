"""Estilo compartilhado pelos cards do perfil (cores, fontes, ícones e moldura)."""
import os, re

ICONES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icones")
FONT = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
CARD, BORDER, TITLE, TEXT, MUTED, ACCENT = "#161b22", "#30363d", "#e6edf3", "#c9d1d9", "#8b949e", "#ec8a62"
W = 880  # largura padrão dos cards de largura total

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


def moldura(w, h, rx=14):
    """Fundo do card com a faixa do pôr do sol no topo."""
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{CARD}" stroke="{BORDER}"/>'
            f'<rect x="{rx}" y=".5" width="{w-2*rx}" height="2.5" rx="1.25" fill="url(#faixa)"/>')


def selo(x, y, icone, tam=40, classe="selo", atraso=0):
    """Quadrado com degradê do pôr do sol e um ícone Lucide branco no centro."""
    escala = tam * 0.55 / 24
    off = (tam - 24 * escala) / 2
    return (f'<g class="{classe}" style="animation-delay:-{atraso:.2f}s">'
            f'<rect x="{x}" y="{y}" width="{tam}" height="{tam}" rx="{tam*0.25:.1f}" fill="url(#por-do-sol)"/>'
            f'<rect x="{x}" y="{y}" width="{tam}" height="{tam}" rx="{tam*0.25:.1f}" fill="none" stroke="#fff" stroke-opacity=".25"/></g>'
            f'<g transform="translate({x+off:.1f},{y+off:.1f}) scale({escala:.3f})" fill="none" stroke="#fff" stroke-width="{1.8/escala*0.9:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">{lucide(icone)}</g>')


def titulo(x, y, texto, tam=18):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{tam}" font-weight="600" fill="{TITLE}">{texto}</text>'


def salvar(caminho, w, h, nome, css, corpo, defs=""):
    css += ".selo{animation:selo 3.2s ease-in-out infinite alternate}@keyframes selo{to{opacity:.72}}"
    css += "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<title>{nome}</title><style>{css}</style><defs>{GRADIENTES}{defs}</defs>{corpo}</svg>')
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(svg)
