# -*- coding: utf-8 -*-
"""
G11 Ch.10 figure builder — stoichiometry.
Canvas height computed from content (never hard-coded).

Figures:
  ch10-mass-mass-steps.svg   The four-step mass-to-mass pipeline with example
  ch10-limiting-reagent.svg  Double-assumption method for limiting reagent
  ch10-yield-trio.svg        Theoretical vs actual vs percent yield
  ch10-purity.svg            Percent purity bar
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


def arrow1(x1, y1, x2, y2, color="#52606D", sw=1.6):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#ar)"/>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_mass_mass():
    """The only road between two substances runs through moles."""
    W = 680
    b = [arrow_defs()]
    y = 32
    b.append(text(340, y, "Mass-to-Mass: The Four-Step Road｜质量对质量四步路", 17, INK, "700", "middle"))
    y += 24
    b.append(text(340, y, "Example: what mass of H₂ forms when 6.0 g Mg reacts with excess HCl?",
                  11.5, MUTED, "400", "middle"))
    b.append(text(340, y + 18, "Mg + 2 HCl → MgCl₂ + H₂", 12.5, INK, "700", "middle"))
    y += 36

    stages = [
        ("Mass A", "6.0 g Mg", BLUE, BLUE_F),
        ("Mol A", "0.247 mol Mg", GREEN, GREEN_F),
        ("Mol B", "0.247 mol H₂", AMBER, AMBER_F),
        ("Mass B", "0.50 g H₂", PURPLE, PURPLE_F),
    ]
    bw, bh = 140, 74
    xs = [40, 200, 360, 520]
    by = y
    for (t1, t2, col, fl), bx in zip(stages, xs):
        b.append(rect(bx, by, bw, bh, fl, col, 1.5, 10))
        b.append(text(bx + bw / 2, by + 28, t1, 12.5, col, "700", "middle"))
        b.append(text(bx + bw / 2, by + 54, t2, 12.5, INK, "700", "middle"))
    labels = ["÷ molar mass\n24.3 g/mol", "× mole ratio\n1 : 1", "× molar mass\n2.016 g/mol"]
    for i, lab in enumerate(labels):
        x1 = xs[i] + bw + 4
        x2 = xs[i + 1] - 4
        b.append(arrow1(x1, by + bh / 2, x2, by + bh / 2))
        l1, l2 = lab.split("\n")
        b.append(text((x1 + x2) / 2, by + bh / 2 - 18, l1, 9.5, INK, "700", "middle"))
        b.append(text((x1 + x2) / 2, by + bh / 2 + 30, l2, 9.5, MUTED, "400", "middle"))
    y = by + bh + 26

    steps = [
        "① Balance first — all ratios come from the balanced equation. 先配平。",
        "② grams A → mol A:   6.0 g ÷ 24.3 g/mol = 0.247 mol",
        "③ mol A → mol B:     0.247 mol × (1 mol H₂ / 1 mol Mg) = 0.247 mol",
        "④ mol B → grams B:   0.247 mol × 2.016 g/mol = 0.499 → 0.50 g (2 s.f.)",
    ]
    b.append(rect(40, y, 600, 112, HEAD, LINE, 1.2, 8))
    for i, s in enumerate(steps):
        b.append(text(60, y + 26 + i * 24, s, 11.5, INK if i else GREEN, "700" if i == 0 else "400"))
    y += 112 + 24
    b.append(rect(40, y, 600, 46, RED_F, RED, 1.2, 8))
    b.append(text(60, y + 19, "⛔ No shortcut: mass A → mass B directly is the #1 exam error.",
                  12, RED, "700"))
    b.append(text(60, y + 37, "质量直接换质量是第一大扣分点——必须绕道摩尔。", 10.5, INK))
    return svg(W, y + 66, "".join(b))


# --------------------------------------------------------------------------
def build_limiting():
    """Double assumption: compute product from each reactant; smaller wins."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Limiting Reagent: Run Both Assumptions｜限量试剂：双假设法", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "4.0 g H₂ + 32.0 g O₂ burn to water. Which runs out first?  (2 H₂ + O₂ → 2 H₂O)",
                  11.5, MUTED, "400", "middle"))
    y += 20

    # two assumption boxes
    b.append(rect(45, y, 285, 130, BLUE_F, BLUE, 1.4, 8))
    b.append(text(187, y + 24, "Assume ALL the H₂ reacts", 12.5, BLUE, "700", "middle"))
    b.append(text(187, y + 48, "4.0 g ÷ 2.016 = 1.98 mol H₂", 11.5, INK, "400", "middle"))
    b.append(text(187, y + 70, "→ 1.98 mol H₂O", 12.5, INK, "700", "middle"))
    b.append(text(187, y + 94, "(ratio 2 : 2 = 1)", 10, MUTED, "400", "middle"))
    b.append(text(187, y + 114, "product possible: 1.98 mol", 10.5, BLUE, "700", "middle"))

    b.append(rect(350, y, 285, 130, AMBER_F, AMBER, 1.4, 8))
    b.append(text(492, y + 24, "Assume ALL the O₂ reacts", 12.5, AMBER, "700", "middle"))
    b.append(text(492, y + 48, "32.0 g ÷ 32.00 = 1.00 mol O₂", 11.5, INK, "400", "middle"))
    b.append(text(492, y + 70, "→ 2.00 mol H₂O", 12.5, INK, "700", "middle"))
    b.append(text(492, y + 94, "(ratio 1 : 2)", 10, MUTED, "400", "middle"))
    b.append(text(492, y + 114, "product possible: 2.00 mol", 10.5, AMBER, "700", "middle"))
    y += 130 + 20

    # verdict
    b.append(rect(45, y, 590, 78, GREEN_F, GREEN, 1.4, 8))
    b.append(text(340, y + 24, "SMALLER product wins → H₂ is limiting｜取小值 → H₂ 限量", 13.5, GREEN, "700", "middle"))
    b.append(text(340, y + 48, "Theoretical yield = 1.98 mol H₂O × 18.02 g/mol = 35.7 g H₂O (3 s.f.)",
                  12, INK, "700", "middle"))
    b.append(text(340, y + 68, "Leftover O₂: 1.00 − 1.98/2 = 0.01 mol unused｜O₂ 剩 0.01 mol", 10.5, MUTED, "400", "middle"))
    y += 78 + 22

    b.append(rect(45, y, 590, 46, RED_F, RED, 1.2, 8))
    b.append(text(65, y + 19, "⛔ Whichever reactant makes LESS product is limiting — compute yield from IT only.",
                  11.5, RED, "700"))
    b.append(text(65, y + 37, "产量算小的那个（限量试剂）；过量试剂的量只能用来算剩余。", 10.5, INK))
    return svg(W, y + 66, "".join(b))


# --------------------------------------------------------------------------
def build_yield_trio():
    """Theoretical / actual / percent yield relationship."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "The Yield Trio｜产量三兄弟", 17, INK, "700", "middle"))
    y += 26

    cards = [
        ("Theoretical yield｜理论产量", "from stoichiometry (limiting reagent)", "纸上最大值 — 纯算出来", BLUE, BLUE_F),
        ("Actual yield｜实际产量", "measured in the lab after the experiment", "实验称出来 — 总是更小", GREEN, GREEN_F),
        ("Percent yield｜百分产率", "= actual ÷ theoretical × 100%", "效率指标 — 永远 ≤ 100%", AMBER, AMBER_F),
    ]
    ch = 84
    for t1, t2, t3, col, fl in cards:
        b.append(rect(55, y, 570, ch, fl, col, 1.4, 8))
        b.append(text(80, y + 28, t1, 13.5, col, "700"))
        b.append(text(80, y + 52, t2, 11.5, INK))
        b.append(text(80, y + 72, t3, 10.5, MUTED))
        y += ch + 14

    y += 4
    b.append(rect(55, y, 570, 96, HEAD, LINE, 1.2, 8))
    b.append(text(75, y + 26, "Worked example｜算例", 12.5, INK, "700"))
    b.append(text(75, y + 50, "theoretical = 8.50 g ; actual = 7.65 g  →  % yield = 7.65 / 8.50 × 100% = 90.0 %",
                  12, INK, "700"))
    b.append(text(75, y + 74, "If you get > 100%: wet product, impurities, or weighing error — check before celebrating.",
                  10.5, MUTED))
    return svg(W, y + 116, "".join(b))


# --------------------------------------------------------------------------
def build_purity():
    """Percent purity bar."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Percent Purity｜百分纯度", 17, INK, "700", "middle"))
    y += 24
    b.append(text(340, y, "Real samples are never 100% pure. Only the pure part reacts.",
                  11.5, MUTED, "400", "middle"))
    y += 20

    # bar: sample = pure + impurity
    bx, bw, bh = 55, 570, 44
    pure_w = 570 * 0.86
    b.append(rect(bx, y, pure_w, bh, GREEN_F, GREEN, 1.4, 0))
    b.append(text(bx + pure_w / 2, y + bh / 2 + 5, "pure substance 纯物质  86%", 12.5, GREEN, "700", "middle"))
    b.append(rect(bx + pure_w, y, 570 - pure_w, bh, RED_F, RED, 1.4, 0))
    b.append(text(bx + pure_w + (570 - pure_w) / 2, y + bh / 2 + 5, "impurity", 11, RED, "700", "middle"))
    y += bh + 10
    b.append(text(340, y, "sample total mass 样品总质量 = 100%", 11, MUTED, "400", "middle"))
    y += 34

    formula = [
        ("% purity = mass of pure substance / mass of sample × 100%", 13, INK, "700"),
        ("stoichiometry uses ONLY the pure part:  mass pure = % purity × sample mass", 12, INK, "400"),
        ("Example: 5.00 g ore at 86.0% → 4.30 g real Zn → 4.30 / 65.38 = 0.0658 mol Zn", 11.5, MUTED, "400"),
    ]
    for i, (s, sz, col, wt) in enumerate(formula):
        b.append(text(340, y + i * 26, s, sz, col, wt, "middle"))
    y += 3 * 26 + 12

    b.append(rect(55, y, 570, 46, AMBER_F, AMBER, 1.2, 8))
    b.append(text(75, y + 19, "Purity ≠ concentration ≠ yield — three different ratios, keep them straight.",
                  11.5, AMBER, "700"))
    b.append(text(75, y + 37, "纯度、浓度、产率是三个不同的比值，考试最易混。", 10.5, INK))
    return svg(W, y + 66, "".join(b))


# --------------------------------------------------------------------------
def main():
    figs = {
        "ch10-mass-mass-steps.svg": build_mass_mass,
        "ch10-limiting-reagent.svg": build_limiting,
        "ch10-yield-trio.svg": build_yield_trio,
        "ch10-purity.svg": build_purity,
    }
    for name, fn in figs.items():
        s = fn()
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)


if __name__ == "__main__":
    main()
