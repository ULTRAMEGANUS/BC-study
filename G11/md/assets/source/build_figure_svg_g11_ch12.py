# -*- coding: utf-8 -*-
"""
G11 Ch.12 figure builder — solutions and solubility.
Canvas height computed from content (never hard-coded).

Figures:
  ch12-like-dissolves-like.svg   Polar vs nonpolar solute-solvent matrix
  ch12-dissociation.svg          Dissociation equation anatomy + hydration
  ch12-solubility-curve.svg      Reading a solubility curve
  ch12-precipitation-flow.svg    Predicting precipitates: swap & check
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


def arrow1(x1, y1, x2, y2, color="#52606D", sw=1.6):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#ar)"/>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_like_dissolves():
    """The 2x2 matrix of solute polarity x solvent polarity."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Like Dissolves Like｜相似相溶", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "Polar attracts polar; nonpolar attracts nonpolar. Mismatch = no dissolving.",
                  11, MUTED, "400", "middle"))
    y += 20

    # matrix
    x0, y0 = 150, y
    cw, chh = 240, 74
    # column headers
    b.append(rect(x0, y0, cw, 40, BLUE_F, BLUE, 1.3, 8))
    b.append(text(x0 + cw / 2, y0 + 25, "Polar solvent 极性溶剂 (water 水)", 11.5, BLUE, "700", "middle"))
    b.append(rect(x0 + cw + 10, y0, cw, 40, AMBER_F, AMBER, 1.3, 8))
    b.append(text(x0 + cw + 10 + cw / 2, y0 + 25, "Nonpolar solvent 非极性 (hexane 己烷)", 11.5, AMBER, "700", "middle"))
    y0 += 50

    # row 1: polar solute
    b.append(rect(40, y0, 100, chh, BLUE_F, BLUE, 1.3, 8))
    b.append(text(90, y0 + 28, "Polar solute", 11, BLUE, "700", "middle"))
    b.append(text(90, y0 + 48, "食盐 · 糖", 10.5, MUTED, "400", "middle"))
    b.append(rect(x0, y0, cw, chh, GREEN_F, GREEN, 1.4, 8))
    b.append(text(x0 + cw / 2, y0 + 32, "DISSOLVES ✔ 溶解", 13, GREEN, "700", "middle"))
    b.append(text(x0 + cw / 2, y0 + 54, "salt in water", 10, MUTED, "400", "middle"))
    b.append(rect(x0 + cw + 10, y0, cw, chh, RED_F, RED, 1.4, 8))
    b.append(text(x0 + cw + 10 + cw / 2, y0 + 32, "NO ✘ 不溶", 13, RED, "700", "middle"))
    b.append(text(x0 + cw + 10 + cw / 2, y0 + 54, "salt in gasoline", 10, MUTED, "400", "middle"))
    y0 += chh + 10

    # row 2: nonpolar solute
    b.append(rect(40, y0, 100, chh, AMBER_F, AMBER, 1.3, 8))
    b.append(text(90, y0 + 28, "Nonpolar", 11, AMBER, "700", "middle"))
    b.append(text(90, y0 + 48, "油 · 碘", 10.5, MUTED, "400", "middle"))
    b.append(rect(x0, y0, cw, chh, RED_F, RED, 1.4, 8))
    b.append(text(x0 + cw / 2, y0 + 32, "NO ✘ 不溶", 13, RED, "700", "middle"))
    b.append(text(x0 + cw / 2, y0 + 54, "oil & water — the classic", 10, MUTED, "400", "middle"))
    b.append(rect(x0 + cw + 10, y0, cw, chh, GREEN_F, GREEN, 1.4, 8))
    b.append(text(x0 + cw + 10 + cw / 2, y0 + 32, "DISSOLVES ✔ 溶解", 13, GREEN, "700", "middle"))
    b.append(text(x0 + cw + 10 + cw / 2, y0 + 54, "iodine in hexane", 10, MUTED, "400", "middle"))
    y0 += chh + 18

    b.append(rect(45, y0, 590, 58, HEAD, LINE, 1.2, 8))
    b.append(text(65, y0 + 23, "Why: IMF between solute & solvent must rival those inside each liquid.",
                  11.5, INK, "700"))
    b.append(text(65, y0 + 42, "原理（接 Ch.7）：溶质-溶剂间作用力必须强到能拆开各自的抱团。", 10.5, MUTED))
    return svg(W, y0 + 80, "".join(b))


# --------------------------------------------------------------------------
def build_dissociation():
    """Anatomy of a dissociation equation."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Dissociation Equation Anatomy｜电离方程式解剖", 17, INK, "700", "middle"))
    y += 44

    b.append(text(340, y, "NaCl(s)  →  Na⁺(aq)  +  Cl⁻(aq)", 22, INK, "700", "middle"))
    ey = y
    y += 20

    labels = [
        (150, ey + 44, "ionic solid — keep (s) 保留固态", BLUE),
        (330, ey + 68, "cation hydrated in solution 水合阳离子", GREEN),
        (520, ey + 44, "anion hydrated 水合阴离子", AMBER),
    ]
    anchors = [(168, ey - 14), (330, ey - 14), (505, ey - 14)]
    for (lx, ly, s, col), (ax, ay2) in zip(labels, anchors):
        b.append(line(ax, ay2, lx, ly - 4, col, 1.0, "2 2"))
        b.append(circle(ax, ay2 - 3, 2.5, col, col, 1.0))
        b.append(text(lx, ly, s, 10.5, col))
    y = ey + 92

    # side-by-side rules
    b.append(rect(45, y, 285, 118, GREEN_F, GREEN, 1.3, 8))
    b.append(text(187, y + 24, "Split only aqueous ionic compounds", 11.5, GREEN, "700", "middle"))
    b.append(text(187, y + 46, "strong electrolytes → ions", 10.5, INK, "400", "middle"))
    b.append(text(187, y + 66, " solids (s), liquids (l), gases (g)", 10.5, MUTED, "400", "middle"))
    b.append(text(187, y + 86, " stay intact — never split them", 10.5, MUTED, "400", "middle"))
    b.append(text(187, y + 106, "拆强电解质；固液气不拆", 11, INK, "700", "middle"))

    b.append(rect(350, y, 285, 118, RED_F, RED, 1.3, 8))
    b.append(text(492, y + 24, "Balance BOTH atoms and charge", 11.5, RED, "700", "middle"))
    b.append(text(492, y + 46, "CaCl₂(s) → Ca²⁺(aq) + 2 Cl⁻(aq)", 11, INK, "400", "middle"))
    b.append(text(492, y + 66, "charge: +2 and 2(−1) → net 0 ✔", 10.5, MUTED, "400", "middle"))
    b.append(text(492, y + 86, "subscripts become coefficients", 10.5, MUTED, "400", "middle"))
    b.append(text(492, y + 106, "原子与电荷双守恒", 11, INK, "700", "middle"))
    y += 118 + 20

    b.append(text(340, y + 4, "Conductivity: mobile ions carry current — that is why salt water conducts.",
                  10.5, MUTED, "400", "middle"))
    return svg(W, y + 28, "".join(b))


# --------------------------------------------------------------------------
def build_solubility_curve():
    """Reading a solubility curve: KNO3 steep, NaCl flat, gas decreasing."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Reading Solubility Curves｜溶解度曲线读图", 17, INK, "700", "middle"))
    y += 14

    # plot area
    px, py_, pw, ph = 90, y + 10, 330, 250
    b.append(line(px, py_, px, py_ + ph, MUTED, 1.4))
    b.append(line(px, py_ + ph, px + pw, py_ + ph, MUTED, 1.4))
    b.append(text(px - 8, py_ - 2, "g/100 mL", 10, MUTED, "700", "end"))
    b.append(text(px + pw, py_ + ph + 16, "temperature (°C) 温度", 10, MUTED, "400", "end"))
    # gridlines
    for i in range(1, 4):
        gy = py_ + ph * i / 4
        b.append(line(px, gy, px + pw, gy, "#E4E7EB", 1.0))
        b.append(text(px - 6, gy + 4, str(120 - i * 30), 9, MUTED, "400", "end"))

    # KNO3 steep curve
    pts_k = [(0, 170), (60, 140), (120, 105), (180, 70), (240, 35), (300, 12)]
    pts_k = [(px + x, py_ + y * ph / 250) for x, y in pts_k]
    b.append(f'<path d="M {pts_k[0][0]},{pts_k[0][1]} ' + " ".join(f"L {x},{y}" for x, y in pts_k[1:]) +
             '" fill="none" stroke="#C53030" stroke-width="2.2"/>')
    # NaCl flat curve
    pts_n = [(0, 185), (60, 183), (120, 180), (180, 178), (240, 176), (300, 173)]
    pts_n = [(px + x, py_ + y * ph / 250) for x, y in pts_n]
    b.append(f'<path d="M {pts_n[0][0]},{pts_n[0][1]} ' + " ".join(f"L {x},{y}" for x, y in pts_n[1:]) +
             '" fill="none" stroke="#2B6CB0" stroke-width="2.2"/>')
    # gas curve (decreasing)
    pts_g = [(0, 40), (60, 60), (120, 85), (180, 115), (240, 150), (300, 190)]
    pts_g = [(px + x, py_ + y * ph / 250) for x, y in pts_g]
    b.append(f'<path d="M {pts_g[0][0]},{pts_g[0][1]} ' + " ".join(f"L {x},{y}" for x, y in pts_g[1:]) +
             '" fill="none" stroke="#2F855A" stroke-width="2.2" stroke-dasharray="6 4"/>')

    b.append(text(px + 250, py_ + 8, "KNO₃ (solid)", 10.5, "#C53030", "700"))
    b.append(text(px + 250, py_ + 30, "NaCl (solid)", 10.5, "#2B6CB0", "700"))
    b.append(text(px + 250, py_ + 52, "O₂ (gas)", 10.5, "#2F855A", "700"))
    y = py_ + ph + 40

    # reading rules
    rules = [
        ("Above the curve 超饱和区", "supersaturated / crystallizes out 过饱和析出", PURPLE),
        ("On the curve 曲线上", "saturated 饱和 — exactly dissolved to the limit", AMBER),
        ("Below the curve 欠饱和区", "unsaturated — can still dissolve more 不饱和", GREEN),
    ]
    for t1, t2, col in rules:
        b.append(rect(60, y, 560, 42, BG, col, 1.2, 8))
        b.append(text(80, y + 18, t1, 11.5, col, "700"))
        b.append(text(80, y + 35, t2, 10.5, MUTED))
        y += 42 + 8
    y += 4
    b.append(text(340, y + 4, "Solids: most dissolve MORE when hot. Gases: opposite — warm water holds less O₂.",
                  11, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "固体多数升温增溶；气体反向——温水中溶氧少，鱼夏天浮头。", 10.5, MUTED, "400", "middle"))
    return svg(W, y + 22, "".join(b))


# --------------------------------------------------------------------------
def build_precip_flow():
    """Predicting precipitates: swap partners, check rules."""
    W = 680
    b = [arrow_defs()]
    y = 32
    b.append(text(340, y, "Will a Precipitate Form?｜沉淀预测四步", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "Example: mix AgNO₃(aq) with NaCl(aq).", 11.5, MUTED, "400", "middle"))
    y += 20

    steps = [
        ("1  Write both reactants with ions", "AgNO₃(aq) + NaCl(aq) — both aqueous, both split", BLUE, BLUE_F),
        ("2  Swap partners (double replacement)", "Ag⁺ pairs with Cl⁻ ; Na⁺ pairs with NO₃⁻", GREEN, GREEN_F),
        ("3  Check the solubility rules for BOTH products", "AgCl → INSOLUBLE 沉淀 ; NaNO₃ → soluble 留溶液", AMBER, AMBER_F),
        ("4  Write the equation with (s) for the precipitate", "AgNO₃(aq) + NaCl(aq) → AgCl(s)↓ + NaNO₃(aq)", PURPLE, PURPLE_F),
    ]
    for t, s, col, fl in steps:
        b.append(rect(55, y, 570, 56, fl, col, 1.3, 8))
        b.append(text(75, y + 24, t, 12.5, col, "700"))
        b.append(text(75, y + 44, s, 11.5, INK))
        y += 56 + 12

    b.append(arrow1(340, y - 22, 340, y - 22))
    b.append(rect(55, y, 570, 62, HEAD, LINE, 1.2, 8))
    b.append(text(75, y + 24, "Quick rules you must know cold｜必背速查（Data Booklet 版为准）", 12, INK, "700"))
    b.append(text(75, y + 46, "NO₃⁻ · NH₄⁺ · Group 1 → always soluble ; Cl⁻ except Ag⁺/Pb²⁺ ; SO₄²⁻ except Ba²⁺/Pb²⁺",
                  11, INK))
    y += 62 + 16
    b.append(rect(55, y, 570, 44, RED_F, RED, 1.2, 8))
    b.append(text(75, y + 19, "Both products soluble → NO precipitate, write “no reaction”. 两者都可溶 = 不反应。",
                  11.5, RED, "700"))
    b.append(text(75, y + 37, "沉淀 = 低溶解度的固体；不是“沉下去”就叫沉淀。", 10.5, INK))
    return svg(W, y + 64, "".join(b))


# --------------------------------------------------------------------------
def main():
    figs = {
        "ch12-like-dissolves-like.svg": build_like_dissolves,
        "ch12-dissociation.svg": build_dissociation,
        "ch12-solubility-curve.svg": build_solubility_curve,
        "ch12-precipitation-flow.svg": build_precip_flow,
    }
    for name, fn in figs.items():
        s = fn()
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)


if __name__ == "__main__":
    main()
