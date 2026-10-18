"""Generate the Art of War mind map as SVG and render it to PNG via headless Chrome."""
import math
import subprocess
import textwrap
from pathlib import Path

OUT_DIR = Path(__file__).parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 3400, 2400
CX, CY = W / 2, H / 2
RX, RY = 1330, 900
CARD_W, WRAP = 400, 36
FONT = "Segoe UI, Arial, sans-serif"

CHAPTERS = [
    ("1 · Planejamento", ["5 fatores: Caminho, Céu, Terra, Comandante, Método",
                          "Comparar as forças antes de lutar",
                          "Toda guerra se baseia no engano"]),
    ("2 · Fazer a guerra", ["Guerra longa esgota o Estado",
                            "Vitória rápida, não campanha longa",
                            "Abastecer-se no território inimigo"]),
    ("3 · Estratégia ofensiva", ["Vencer sem lutar é o ideal",
                                 "Atacar a estratégia, depois as alianças, o exército e, por último, as cidades",
                                 "Conhecer o inimigo e a si mesmo"]),
    ("4 · Disposições", ["Primeiro tornar-se invencível",
                         "Esperar a vulnerabilidade do inimigo",
                         "Vencer antes de lutar"]),
    ("5 · Energia", ["Forças diretas e indiretas",
                     "Combinações infinitas",
                     "Força do conjunto, não do indivíduo"]),
    ("6 · Pontos fortes e fracos", ["Chegar primeiro e impor o terreno",
                                    "Atacar onde o inimigo não defende",
                                    "Adaptar-se como a água"]),
    ("7 · Manobras", ["Transformar o desvio em atalho",
                      "Comunicação: bandeiras e tambores",
                      "Não atacar tropas descansadas ou motivadas"]),
    ("8 · Variações táticas", ["Há ordens que não se obedecem",
                               "Pesar vantagem e risco",
                               "5 defeitos fatais do comandante"]),
    ("9 · O exército em marcha", ["Ler os sinais do terreno e do inimigo",
                                  "Disciplina com humanidade"]),
    ("10 · Terreno", ["6 tipos de terreno",
                      "6 causas de derrota que são culpa do comandante",
                      "Cuidar dos soldados como filhos"]),
    ("11 · As nove situações", ["Do terreno disperso ao terreno mortal",
                                "Sem saída, a tropa luta com tudo",
                                "Velocidade e surpresa"]),
    ("12 · Ataque com fogo", ["5 alvos do fogo",
                              "Não agir por raiva",
                              "Mover-se só se houver vantagem"]),
    ("13 · Espiões", ["Informação vale mais que batalhas",
                      "5 tipos de espiões",
                      "O agente duplo é o mais valioso"]),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(x, y, title, items, hue):
    lines = []
    for it in items:
        wrapped = textwrap.wrap(it, WRAP)
        lines.append(("• " + wrapped[0], True))
        lines += [("   " + w, False) for w in wrapped[1:]]
    h = 70 + len(lines) * 30 + 18
    left, top = x - CARD_W / 2, y - h / 2
    color = f"hsl({hue},62%,42%)"
    out = [
        f'<rect x="{left}" y="{top}" width="{CARD_W}" height="{h}" rx="18" fill="hsl({hue},70%,97%)" stroke="{color}" stroke-width="3"/>',
        f'<rect x="{left}" y="{top}" width="{CARD_W}" height="54" rx="18" fill="{color}"/>',
        f'<rect x="{left}" y="{top + 36}" width="{CARD_W}" height="18" fill="{color}"/>',
        f'<text x="{x}" y="{top + 36}" text-anchor="middle" font-size="25" font-weight="700" fill="#fff">{esc(title)}</text>',
    ]
    ty = top + 54 + 34
    for text, _ in lines:
        out.append(f'<text x="{left + 18}" y="{ty}" font-size="21" fill="#222" xml:space="preserve">{esc(text)}</text>')
        ty += 30
    return "\n".join(out)


def build_svg():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="{FONT}">',
             f'<rect width="{W}" height="{H}" fill="#faf7f0"/>']
    n = len(CHAPTERS)
    positions = []
    for i in range(n):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        positions.append((CX + RX * math.cos(ang), CY + RY * math.sin(ang)))
    for i, (x, y) in enumerate(positions):
        hue = int(360 * i / n)
        mx, my = (CX + x) / 2, (CY + y) / 2
        parts.append(f'<path d="M{CX},{CY} Q{mx + (y - CY) * 0.12},{my - (x - CX) * 0.12} {x},{y}" '
                     f'stroke="hsl({hue},55%,55%)" stroke-width="7" fill="none" stroke-linecap="round"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="210" fill="#7a1f1f" stroke="#c9a227" stroke-width="10"/>')
    parts.append(f'<text x="{CX}" y="{CY - 20}" text-anchor="middle" font-size="58" font-weight="800" fill="#fff">A Arte</text>')
    parts.append(f'<text x="{CX}" y="{CY + 45}" text-anchor="middle" font-size="58" font-weight="800" fill="#fff">da Guerra</text>')
    parts.append(f'<text x="{CX}" y="{CY + 105}" text-anchor="middle" font-size="34" fill="#f3e3a6">Sun Tzu</text>')
    for i, ((title, items), (x, y)) in enumerate(zip(CHAPTERS, positions)):
        parts.append(card(x, y, title, items, int(360 * i / n)))
    parts.append(f'<text x="{W - 30}" y="{H - 25}" text-anchor="end" font-size="20" fill="#888">'
                 'Resumo próprio · texto original em domínio público</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def build_svg_vertical():
    """Phone layout: 1080 px wide, chapters stacked along a vertical spine."""
    vw, spine, card_x, card_w, wrap = 1080, 90, 150, 890, 46
    body = []
    y = 470
    n = len(CHAPTERS)
    for i, (title, items) in enumerate(CHAPTERS):
        hue = int(360 * i / n)
        color = f"hsl({hue},62%,42%)"
        lines = []
        for it in items:
            wrapped = textwrap.wrap(it, wrap)
            lines.append("• " + wrapped[0])
            lines += ["   " + w for w in wrapped[1:]]
        h = 84 + len(lines) * 44 + 26
        body += [
            f'<line x1="{spine}" y1="{y + 42}" x2="{card_x}" y2="{y + 42}" stroke="{color}" stroke-width="6"/>',
            f'<circle cx="{spine}" cy="{y + 42}" r="20" fill="{color}" stroke="#faf7f0" stroke-width="6"/>',
            f'<rect x="{card_x}" y="{y}" width="{card_w}" height="{h}" rx="24" fill="hsl({hue},70%,97%)" stroke="{color}" stroke-width="4"/>',
            f'<rect x="{card_x}" y="{y}" width="{card_w}" height="84" rx="24" fill="{color}"/>',
            f'<rect x="{card_x}" y="{y + 60}" width="{card_w}" height="24" fill="{color}"/>',
            f'<text x="{card_x + 30}" y="{y + 56}" font-size="40" font-weight="700" fill="#fff">{esc(title)}</text>',
        ]
        ty = y + 84 + 50
        for text in lines:
            body.append(f'<text x="{card_x + 28}" y="{ty}" font-size="32" fill="#222" xml:space="preserve">{esc(text)}</text>')
            ty += 44
        y += h + 46
    vh = y + 70
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw}" height="{vh}" font-family="{FONT}">',
        f'<rect width="{vw}" height="{vh}" fill="#faf7f0"/>',
        f'<rect x="40" y="40" width="{vw - 80}" height="350" rx="36" fill="#7a1f1f" stroke="#c9a227" stroke-width="10"/>',
        f'<text x="{vw / 2}" y="185" text-anchor="middle" font-size="96" font-weight="800" fill="#fff">A Arte da Guerra</text>',
        f'<text x="{vw / 2}" y="260" text-anchor="middle" font-size="50" fill="#f3e3a6">Sun Tzu</text>',
        f'<text x="{vw / 2}" y="330" text-anchor="middle" font-size="32" fill="#f3e3a6">13 capítulos em um mapa</text>',
        f'<line x1="{spine}" y1="420" x2="{spine}" y2="{y - 60}" stroke="#c9a227" stroke-width="8" stroke-linecap="round"/>',
    ]
    foot = [f'<text x="{vw / 2}" y="{vh - 30}" text-anchor="middle" font-size="24" fill="#888">'
            'Resumo próprio · texto original em domínio público</text>', "</svg>"]
    return "\n".join(head + body + foot), vw, vh


def render(svg_text, name, w, h):
    svg = OUT_DIR / f"{name}.svg"
    html = OUT_DIR / "_render.html"
    png = OUT_DIR / f"{name}.png"
    svg.write_text(svg_text, encoding="utf-8")
    html.write_text(f'<body style="margin:0"><img src="{svg.name}" style="display:block;width:{w}px;height:{h}px">',
                    encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()], check=True)
    html.unlink()
    print(png)


def render_pdf_a3(name):
    """Print the existing SVG to a single A3 landscape page (vector, via headless Chrome)."""
    html = OUT_DIR / "_render.html"
    pdf = OUT_DIR / f"{name}_A3.pdf"
    html.write_text('<style>@page{size:A3 landscape;margin:0}body{margin:0}'
                    'img{display:block;width:420mm;height:297mm;object-fit:contain}</style>'
                    f'<img src="{name}.svg">', encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", html.as_uri()], check=True)
    html.unlink()
    print(pdf)


def main():
    render(build_svg(), "mapa_mental_arte_da_guerra", W, H)
    render_pdf_a3("mapa_mental_arte_da_guerra")
    svg_text, vw, vh = build_svg_vertical()
    render(svg_text, "mapa_mental_arte_da_guerra_celular", vw, vh)


if __name__ == "__main__":
    main()
