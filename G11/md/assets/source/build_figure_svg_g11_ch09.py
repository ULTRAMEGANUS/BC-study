# -*- coding: utf-8 -*-
"""
G11 Ch.9 figure builder — chemical reactions.
Canvas height computed from content (never hard-coded).

Figures:
  ch09-six-types-tree.svg    Decision tree for the six reaction types
  ch09-activity-series.svg   Activity series ladder with reading rules
  ch09-equation-anatomy.svg  Anatomy of a balanced equation (state symbols)
  ch09-combustion-branch.svg Complete vs incomplete combustion — O2 decides
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "figures"))

BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#52606D"
LINE = "#9AA5B1"
HEAD = "#F0F4F8"
BLUE = "#2B6CB0"
BLUE_F = "#EBF4FF"
GREEN = "#2F855A"
GREEN_F = "#F0FFF4"
AMBER = "#B7791F"
AMBER_F = "#FFFBEB"
RED = "#C53030"
RED_F = "#FFF5F5"
PURPLE = "#6B46C1"
PURPLE_F = "#F5F0FF"

FONT = "'Segoe UI','Helvetica Neue',Arial,'Microsoft YaHei',sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=13, fill=INK, weight="400", anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{st}>{esc(s)}</text>')


def rect(x, y, w, h, fill=BG, stroke=LINE, sw=1.2, rx=8):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, color=LINE, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}"{d}/>')


def circle(cx, cy, r, fill="none", stroke=LINE, sw=1.4):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def arrow_defs():
    return ('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#52606D"/></marker></defs>')


def arrow(x1, y1, x2, y2, color="#52606D", sw=1.6):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#ar)"/>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_six_types():
    """Six reaction types as pattern cards."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "The Six Reaction Types｜六类反应一览", 17, INK, "700", "middle"))
    y += 24
    b.append(text(340, y, "General pattern + one real example each — learn the shape, not the sample.",
                  11, MUTED, "400", "middle"))
    y += 18

    cards = [
        ("1  Synthesis 合成", "A + B → AB", "2 Mg + O₂ → 2 MgO", BLUE, BLUE_F),
        ("2  Decomposition 分解", "AB → A + B", "2 H₂O₂ → 2 H₂O + O₂", GREEN, GREEN_F),
        ("3  Single replacement 单置换", "A + BC → AC + B", "Zn + 2 HCl → ZnCl₂ + H₂", AMBER, AMBER_F),
        ("4  Double replacement 双置换", "AB + CD → AD + CB", "AgNO₃ + NaCl → AgCl↓ + NaNO₃", PURPLE, PURPLE_F),
        ("5  Neutralization 中和", "acid + base → salt + water", "HCl + NaOH → NaCl + H₂O", RED, RED_F),
        ("6  Combustion 燃烧", "CₓHᵧ + O₂ → CO₂ + H₂O", "CH₄ + 2 O₂ → CO₂ + 2 H₂O", "#C05621", "#FFFAF0"),
    ]
    row_h = 58
    for t1, pat, ex, col, fl in cards:
        b.append(rect(45, y, 590, row_h - 8, fl, col, 1.3, 8))
        b.append(text(65, y + 24, t1, 12.5, col, "700"))
        b.append(text(270, y + 24, pat, 12, INK, "700"))
        b.append(text(450, y + 24, ex, 11, MUTED))
        y += row_h
    y += 4
    b.append(text(340, y, "Neutralization is double replacement with H₂O as one product.", 10.5, MUTED, "400", "middle"))
    return svg(W, y + 22, "".join(b))


# --------------------------------------------------------------------------
def build_activity_series():
    """Activity series ladder with reading rules."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "The Activity Series｜金属活动性顺序", 17, INK, "700", "middle"))
    y += 24
    b.append(text(340, y, "A metal will displace any ion BELOW it. 高者置换低者。", 11.5, MUTED, "400", "middle"))
    y += 14

    series = ["Li", "K", "Ba", "Ca", "Na", "Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "H", "Cu", "Hg", "Ag"]
    colors = []
    for m in series:
        if m == "H":
            colors.append(AMBER)
        elif series.index(m) < 6:
            colors.append(RED)
        elif series.index(m) < 12:
            colors.append(BLUE)
        else:
            colors.append(GREEN)

    top = y + 6
    row_h = 26
    ladder_x = 250
    for i, m in enumerate(series):
        yy = top + i * row_h
        col = colors[i]
        if m == "H":
            b.append(line(345, yy + row_h / 2 - 2, 610, yy + row_h / 2 - 2, AMBER, 1.6, "6 4"))
            b.append(text(80, yy + row_h / 2 + 4, "(H) reference line｜基准线", 11, AMBER, "700"))
        b.append(rect(ladder_x, yy, 70, row_h - 6, BG, col, 1.3, 6))
        b.append(text(ladder_x + 35, yy + 15, m, 12.5, col, "700", "middle"))
    y = top + len(series) * row_h + 8

    # side notes
    ny = top + 4
    notes = [
        (RED, RED_F, "Very active｜极活泼", "explode in cold water", "Li K Ba Ca Na"),
        (BLUE, BLUE_F, "Active｜活泼", "react with acids", "Mg Al Zn Fe …"),
        (GREEN, GREEN_F, "Inactive｜不活泼", "no reaction with HCl", "Cu Hg Ag"),
    ]
    for col, fl, t1, t2, t3 in notes:
        b.append(rect(360, ny, 250, 74, fl, col, 1.3, 8))
        b.append(text(378, ny + 22, t1, 12, col, "700"))
        b.append(text(378, ny + 41, t2, 10.5, MUTED))
        b.append(text(378, ny + 59, t3, 11, INK, "700"))
        ny += 86

    b.append(text(340, y + 6, "Example: Zn (above H) + HCl → reacts ; Cu (below H) + HCl → NO reaction",
                  11.5, INK, "700", "middle"))
    return svg(W, y + 28, "".join(b))


# --------------------------------------------------------------------------
def build_equation_anatomy():
    """Anatomy of a balanced equation with state symbols."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Reading an Equation Like a Chemist｜方程式的每一个部件", 17, INK, "700", "middle"))
    y += 40

    # main equation, big
    b.append(text(340, y, "Zn(s) + 2 HCl(aq) → ZnCl₂(aq) + H₂(g)", 22, INK, "700", "middle"))
    y += 16
    ey = y
    # labels with leader lines
    labels = [
        (108, ey + 26, "state symbol: solid｜固", BLUE),
        (170, ey + 50, "coefficient: balances atoms｜系数", GREEN),
        (290, ey + 26, "aqueous = dissolved in water｜水溶液", AMBER),
        (395, ey + 50, "yield arrow｜生成箭头", PURPLE),
        (560, ey + 26, "gas｜气体", RED),
    ]
    # leader dots
    anchors = [(108, ey - 22), (176, ey - 22), (300, ey - 22), (404, ey - 22), (585, ey - 22)]
    for (lx, ly, s, col), (ax, ay2) in zip(labels, anchors):
        b.append(line(ax, ay2, lx, ly - 4, col, 1.0, "2 2"))
        b.append(circle(ax, ay2 - 3, 2.5, col, col, 1.0))
        w = 0
        b.append(text(lx, ly, s, 10.5, col, "400"))
    y = ey + 66

    # state symbol table
    b.append(rect(55, y, 290, 150, HEAD, LINE, 1.2, 8))
    b.append(text(75, y + 24, "State symbols｜状态符号", 12.5, INK, "700"))
    rows = [("(s)", "solid 固体"), ("(l)", "liquid 液体"), ("(g)", "gas 气体"), ("(aq)", "aqueous 水溶液")]
    for i, (sym, mean) in enumerate(rows):
        b.append(text(85, y + 48 + i * 24, sym, 12.5, BLUE, "700"))
        b.append(text(135, y + 48 + i * 24, mean, 11.5, INK))
    y += 150 + 16

    b.append(rect(365, y - 166, 260, 150, GREEN_F, GREEN, 1.2, 8))
    b.append(text(385, y - 142, "Counting check｜数原子自检", 12.5, GREEN, "700"))
    checks = [("Zn: 1 = 1", "OK"), ("H: 2 = 2", "OK"), ("Cl: 2 = 2", "OK")]
    for i, (s, v) in enumerate(checks):
        b.append(text(385, y - 118 + i * 24, s, 11.5, INK))
        b.append(text(600, y - 118 + i * 24, v, 11.5, GREEN, "700"))
    y += 16

    b.append(text(340, y + 8, "Balanced = every element has equal atoms on both sides. 配平 = 每种元素左右原子数相等。",
                  11.5, MUTED, "400", "middle"))
    return svg(W, y + 30, "".join(b))


# --------------------------------------------------------------------------
def build_combustion_branch():
    """Complete vs incomplete combustion — the O2 supply decides."""
    W = 680
    b = [arrow_defs()]
    y = 32
    b.append(text(340, y, "Combustion: Oxygen Supply Decides｜供氧决定产物", 17, INK, "700", "middle"))
    y += 24
    b.append(text(340, y, "Same fuel, different amount of O₂, different products — and different danger.",
                  11, MUTED, "400", "middle"))
    y += 18

    # fuel box
    b.append(rect(250, y, 180, 44, HEAD, LINE, 1.3, 8))
    b.append(text(340, y + 27, "Fuel 燃料  CH₄", 13, INK, "700", "middle"))
    y += 44

    y1 = y + 22
    b.append(arrow(300, y, 190, y1))
    b.append(arrow(380, y, 490, y1))
    b.append(text(210, y + 14, "O₂ PLENTY｜充足", 11, GREEN, "700"))
    b.append(text(415, y + 14, "O₂ LIMITED｜不足", 11, RED, "700"))

    # left: complete
    b.append(rect(60, y1, 260, 150, GREEN_F, GREEN, 1.4, 8))
    b.append(text(190, y1 + 26, "Complete combustion｜完全燃烧", 12.5, GREEN, "700", "middle"))
    b.append(text(190, y1 + 52, "CH₄ + 2 O₂ → CO₂ + 2 H₂O", 13, INK, "700", "middle"))
    b.append(text(190, y1 + 78, "Products: CO₂ + H₂O", 11.5, MUTED, "400", "middle"))
    b.append(text(190, y1 + 100, "Blue flame｜蓝色火焰", 11, GREEN, "400", "middle"))
    b.append(text(190, y1 + 120, "Releases the MOST energy", 11, GREEN, "700", "middle"))

    # right: incomplete
    b.append(rect(360, y1, 260, 150, RED_F, RED, 1.4, 8))
    b.append(text(490, y1 + 26, "Incomplete combustion｜不完全燃烧", 12.5, RED, "700", "middle"))
    b.append(text(490, y1 + 52, "2 CH₄ + 3 O₂ → 2 CO + 4 H₂O", 13, INK, "700", "middle"))
    b.append(text(490, y1 + 78, "Products: CO (or C) + H₂O", 11.5, MUTED, "400", "middle"))
    b.append(text(490, y1 + 100, "Yellow/orange flame｜黄色火焰", 11, AMBER, "400", "middle"))
    b.append(text(490, y1 + 120, "CO is a silent poison｜CO 无色无味有毒", 11, RED, "700", "middle"))
    y = y1 + 150 + 24

    b.append(rect(60, y, 560, 58, AMBER_F, AMBER, 1.2, 8))
    b.append(text(80, y + 23, "Safety link｜安全链接: faulty water heaters & idling cars in garages can produce CO.",
                  11.5, INK, "700"))
    b.append(text(80, y + 42, "燃气热水器故障、车库怠速暖车都可能产生 CO——冬季事故高发场景。", 10.5, MUTED))
    return svg(W, y + 80, "".join(b))


# --------------------------------------------------------------------------
def main():
    figs = {
        "ch09-six-types.svg": build_six_types,
        "ch09-activity-series.svg": build_activity_series,
        "ch09-equation-anatomy.svg": build_equation_anatomy,
        "ch09-combustion-branch.svg": build_combustion_branch,
    }
    for name, fn in figs.items():
        s = fn()
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)


if __name__ == "__main__":
    main()
