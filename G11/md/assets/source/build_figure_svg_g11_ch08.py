# -*- coding: utf-8 -*-
"""
G11 Ch.8 figure builder — the mole.
Canvas height computed from content (never hard-coded).

Figures:
  ch08-mole-three-bridges.svg   Particles - mole - mass conversion map
  ch08-percent-composition.svg  Percent composition worked example (NH3)
  ch08-empirical-flow.svg       Empirical/molecular formula workflow
  ch08-mole-scale.svg           What 1 mol looks like for common substances
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


def arrow_defs():
    return ('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#52606D"/></marker></defs>')


def arrow(x1, y1, x2, y2, color="#52606D", sw=1.6):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#ar)" marker-start="url(#ar)"/>')


def arrow1(x1, y1, x2, y2, color="#52606D", sw=1.6):
    """One-directional arrow."""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#ar)"/>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_three_bridges():
    """The central conversion map of the whole course."""
    W = 680
    b = [arrow_defs()]
    y = 34
    b.append(text(340, y, "The Three Bridges｜三桥换算图", 17, INK, "700", "middle"))
    y += 30
    b.append(text(340, y, "Everything goes through the mole — never particle-to-mass directly.",
                  11.5, MUTED, "400", "middle"))
    y += 10

    box_w, box_h = 150, 92
    by = y + 26
    boxes = [
        (40,  "Particles｜粒子", "atoms, molecules, ions", BLUE, BLUE_F),
        (265, "Mole｜摩尔", "mol", GREEN, GREEN_F),
        (490, "Mass｜质量", "grams (g)", AMBER, AMBER_F),
    ]
    for bx, t1, t2, col, fl in boxes:
        b.append(rect(bx, by, box_w, box_h, fl, col, 1.6, 10))
        b.append(text(bx + box_w / 2, by + 36, t1, 15, col, "700", "middle"))
        b.append(text(bx + box_w / 2, by + 62, t2, 11.5, MUTED, "400", "middle"))

    ay = by + box_h / 2
    # bridge 1
    b.append(arrow(194, ay, 261, ay))
    b.append(text(227, ay - 14, "÷6.02×10²³", 10, INK, "700", "middle"))
    b.append(text(227, ay + 32, "×6.02×10²³", 10, MUTED, "400", "middle"))
    # bridge 2
    b.append(arrow(419, ay, 486, ay))
    b.append(text(452, ay - 14, "× molar mass", 10, INK, "700", "middle"))
    b.append(text(452, ay + 32, "÷ molar mass", 10, MUTED, "400", "middle"))
    b.append(text(452, ay + 48, "(g/mol)", 9.5, MUTED, "400", "middle"))

    y = by + box_h + 34
    b.append(rect(60, y, 560, 118, HEAD, LINE, 1.2, 8))
    b.append(text(80, y + 26, "Worked example｜算例：9.6 g of magnesium, how many atoms?", 13, INK, "700"))
    steps = [
        "①  9.6 g Mg × (1 mol Mg / 24.3 g Mg) = 0.395 mol Mg        ← Bridge 2 (÷ molar mass)",
        "②  0.395 mol × (6.02×10²³ atoms / 1 mol) = 2.4×10²³ atoms  ← Bridge 1 (× N_A)",
        "③  sig figs: 9.6 has 2 s.f. → answer 2.4×10²³ (2 s.f.) ✔",
    ]
    for i, s in enumerate(steps):
        b.append(text(80, y + 50 + i * 24, s, 11.5, INK if i < 2 else GREEN, "400"))

    y += 118 + 30
    b.append(rect(60, y, 560, 46, RED_F, RED, 1.2, 8))
    b.append(text(80, y + 19, "⛔ Trap：particles ⇄ mass must pass through the mole. There is no direct bridge.",
                  12, RED, "700"))
    b.append(text(80, y + 37, "陷阱：粒子与质量之间必须经过摩尔中转，不存在直达桥。", 11, INK))
    return svg(W, y + 66, "".join(b))


# --------------------------------------------------------------------------
def build_percent_composition():
    """Worked example: percent composition of NH3."""
    W = 680
    b = []
    y = 34
    b.append(text(340, y, "Percent Composition｜百分组成 — worked example: NH₃", 17, INK, "700", "middle"))
    y += 30
    b.append(text(340, y, "Question: what percent by mass of ammonia is nitrogen?", 12, MUTED, "400", "middle"))
    y += 22

    # Step rows
    steps = [
        ("Step 1｜定式量", "M(NH₃) = 14.01 + 3 × 1.008 = 17.03 g/mol",
         "one N plus three H — count every atom in the formula", BLUE, BLUE_F),
        ("Step 2｜各元素质量", "mass N = 14.01 g ; mass H = 3.024 g  (per 1 mol)",
         "multiply each element's molar mass by its subscript", GREEN, GREEN_F),
        ("Step 3｜算百分比", "%N = 14.01 / 17.03 × 100% = 82.3 %",
         "%H = 3.024 / 17.03 × 100% = 17.8 %", AMBER, AMBER_F),
    ]
    for t, formula, note, col, fl in steps:
        h = 84
        b.append(rect(55, y, 570, h, fl, col, 1.4, 8))
        b.append(text(75, y + 26, t, 13, col, "700"))
        b.append(text(75, y + 50, formula, 13, INK, "700"))
        b.append(text(75, y + 70, note, 10.5, MUTED))
        y += h + 14

    # composition bar
    y += 6
    b.append(text(340, y, "Check: the parts must sum to 100%｜自检：各部分之和必须是 100%", 12.5, INK, "700", "middle"))
    y += 14
    bx, bw, bh = 55, 570, 38
    wn = 570 * 0.823
    b.append(rect(bx, y, wn, bh, GREEN_F, GREEN, 1.4, 0))
    b.append(text(bx + wn / 2, y + bh / 2 + 5, "N  82.3 %", 13, GREEN, "700", "middle"))
    b.append(rect(bx + wn, y, 570 - wn, bh, AMBER_F, AMBER, 1.4, 0))
    b.append(text(bx + wn + (570 - wn) / 2, y + bh / 2 + 5, "H 17.8%", 11.5, AMBER, "700", "middle"))
    y += bh + 26
    b.append(text(340, y, "82.3 + 17.8 = 100.1 % ✔ (rounding) — 不等于 100% 就先停下检查", 11.5, MUTED, "400", "middle"))
    return svg(W, y + 28, "".join(b))


# --------------------------------------------------------------------------
def build_empirical_flow():
    """% composition -> empirical formula -> molecular formula flowchart."""
    W = 680
    b = [arrow_defs()]
    y = 34
    b.append(text(340, y, "From % to Formula｜从百分组成到化学式", 17, INK, "700", "middle"))
    y += 28

    steps = [
        ("1  Assume 100 g sample｜设样品 100 g", "% → grams directly：27.3 % C → 27.3 g C", BLUE, BLUE_F),
        ("2  Convert each mass to moles｜各质量换摩尔", "g ÷ molar mass = mol（C: 27.3/12.01 = 2.27）", GREEN, GREEN_F),
        ("3  Divide by the smallest｜除以最小值", "2.27 / 2.27 = 1 ; 5.44 / 2.27 = 2.4", AMBER, AMBER_F),
        ("4  Clear fractions to whole numbers｜清分数", "×5 → 5 : 12 → empirical formula C₅H₁₂", PURPLE, PURPLE_F),
    ]
    for i, (t, s, col, fl) in enumerate(steps):
        b.append(rect(70, y, 540, 58, fl, col, 1.4, 8))
        b.append(text(90, y + 24, t, 13, col, "700"))
        b.append(text(90, y + 45, s, 12, INK))
        if i < 3:
            b.append(arrow1(340, y + 58, 340, y + 58 + 22))
        y += 58 + 22

    # branch: empirical vs molecular
    y += 4
    # junction: vertical drop then split to the two boxes
    junction_y = y + 8
    b.append(arrow1(340, y - 22, 340, junction_y))
    b.append(line(200, junction_y, 480, junction_y, "#52606D", 1.6))
    box_y = y + 30
    b.append(arrow1(200, junction_y, 200, box_y))
    b.append(arrow1(480, junction_y, 480, box_y))

    b.append(rect(70, box_y, 260, 74, GREEN_F, GREEN, 1.4, 8))
    b.append(text(200, box_y + 26, "Empirical formula｜实验式", 12.5, GREEN, "700", "middle"))
    b.append(text(200, box_y + 48, "simplest whole-number ratio", 10.5, MUTED, "400", "middle"))
    b.append(text(200, box_y + 64, "C₅H₁₂", 12, INK, "700", "middle"))

    b.append(rect(350, box_y, 260, 74, AMBER_F, AMBER, 1.4, 8))
    b.append(text(480, box_y + 26, "Molecular formula｜分子式", 12.5, AMBER, "700", "middle"))
    b.append(text(480, box_y + 48, "= empirical × n   (n = M / M_empirical)", 10.5, MUTED, "400", "middle"))
    b.append(text(480, box_y + 64, "M = 72 → n = 72/72 = 1 → C₅H₁₂", 11, INK, "700", "middle"))
    y = box_y + 74 + 26
    b.append(text(340, y, "Example chain: CH₂ (empirical) × 6 → C₆H₁₂ (molecular, if M = 84)",
                  11.5, MUTED, "400", "middle"))
    return svg(W, y + 24, "".join(b))


# --------------------------------------------------------------------------
def build_mole_scale():
    """1 mol of common substances — build physical intuition."""
    W = 680
    b = []
    y = 34
    b.append(text(340, y, "One Mole on the Lab Bench｜一摩尔的分量", 17, INK, "700", "middle"))
    y += 26
    b.append(text(340, y, "All five samples contain 6.02×10²³ particles — only the masses differ.",
                  11.5, MUTED, "400", "middle"))
    y += 20

    items = [
        ("C (graphite)｜碳", "12.01 g", "a small spoonful", BLUE, BLUE_F),
        ("H₂O｜水", "18.02 g", "18 mL — one large gulp", GREEN, GREEN_F),
        ("NaCl｜氯化钠", "58.44 g", "about 3 tablespoons", AMBER, AMBER_F),
        ("S (sulfur)｜硫", "32.06 g", "a heaped teaspoon", PURPLE, PURPLE_F),
        ("Cu (copper)｜铜", "63.55 g", "a short cube, 2.3 cm", RED, RED_F),
    ]
    row_h = 62
    for name, mass, sense, col, fl in items:
        b.append(rect(55, y, 570, row_h - 10, fl, col, 1.3, 8))
        b.append(text(80, y + 26, "1 mol", 13, col, "700"))
        b.append(text(140, y + 26, name, 13, INK, "700"))
        b.append(text(360, y + 26, mass, 13, INK, "700"))
        b.append(text(455, y + 26, sense, 11, MUTED))
        y += row_h

    y += 8
    b.append(rect(55, y, 570, 64, HEAD, LINE, 1.2, 8))
    b.append(text(75, y + 24, "Same count, different mass｜数量相同、质量不同", 12.5, INK, "700"))
    b.append(text(75, y + 45, "1 mol of anything = 6.02×10²³ particles. Its mass in grams = its molar mass.",
                  11, MUTED))
    return svg(W, y + 84, "".join(b))


# --------------------------------------------------------------------------
def main():
    figs = {
        "ch08-mole-three-bridges.svg": build_three_bridges,
        "ch08-percent-composition.svg": build_percent_composition,
        "ch08-empirical-flow.svg": build_empirical_flow,
        "ch08-mole-scale.svg": build_mole_scale,
    }
    for name, fn in figs.items():
        s = fn()
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)


if __name__ == "__main__":
    main()
