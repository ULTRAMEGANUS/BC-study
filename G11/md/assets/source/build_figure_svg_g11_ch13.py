# -*- coding: utf-8 -*-
"""
G11 Ch.13 figure builder — concentration and solution stoichiometry.
Canvas height computed from content (never hard-coded).

Figures:
  ch13-four-bridges.svg       The solution-era bridge map (mass-mol-M-V)
  ch13-dilution.svg           C1V1 = C2V2 — same molecules, more water
  ch13-net-ionic-workflow.svg Four steps to a net ionic equation
  ch13-titration.svg          Titration anatomy: setup + calculation chain
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
            f'stroke-width="{sw}" marker-end="url(#ar)" marker-start="url(#ar)"/>')


def arrow1(x1, y1, x2, y2, color="#52606D", sw=1.6):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#ar)"/>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_four_bridges():
    """Solution-era conversion map."""
    W = 680
    b = [arrow_defs()]
    y = 32
    b.append(text(340, y, "The Solution Four Bridges｜溶液版四桥图", 17, INK, "700", "middle"))
    y += 26

    boxes = [
        (40,  "Mass｜质量", "grams", AMBER, AMBER_F),
        (205, "Mole｜摩尔", "mol", GREEN, GREEN_F),
        (375, "Molarity｜浓度", "mol/L", BLUE, BLUE_F),
        (535, "Volume｜体积", "L (or mL)", PURPLE, PURPLE_F),
    ]
    bw, bh = 130, 84
    by = y
    for bx, t1, t2, col, fl in boxes:
        b.append(rect(bx, by, bw, bh, fl, col, 1.5, 10))
        b.append(text(bx + bw / 2, by + 34, t1, 13.5, col, "700", "middle"))
        b.append(text(bx + bw / 2, by + 58, t2, 11, MUTED, "400", "middle"))
    ay = by + bh / 2
    bridges = [
        (174, 201, "×M", "÷M"),
        (339, 371, "×V(L)", "÷V(L)"),
        (509, 531, "→", "←"),
    ]
    b.append(arrow(174, ay, 201, ay))
    b.append(text(187, ay - 12, "×M", 9.5, INK, "700", "middle"))
    b.append(text(187, ay + 24, "÷M", 9.5, MUTED, "400", "middle"))
    b.append(arrow(339, ay, 371, ay))
    b.append(text(355, ay - 12, "×V", 9.5, INK, "700", "middle"))
    b.append(text(355, ay + 24, "÷V", 9.5, MUTED, "400", "middle"))
    b.append(arrow(509, ay, 531, ay))
    b.append(text(520, ay - 12, "×1000", 9, INK, "700", "middle"))
    b.append(text(520, ay + 24, "÷1000", 9, MUTED, "400", "middle"))
    y = by + bh + 20

    b.append(rect(40, y, 600, 74, HEAD, LINE, 1.2, 8))
    b.append(text(60, y + 24, "M = mol ÷ V(L)   ↔   mol = M × V(L)", 13, INK, "700"))
    b.append(text(60, y + 48, "Everything you did in Ch.8–10 still works — you just reach the mole through M×V now.",
                  10.5, MUTED))
    y += 74 + 18
    b.append(rect(40, y, 600, 64, GREEN_F, GREEN, 1.2, 8))
    b.append(text(60, y + 24, "Solution stoichiometry:  M·V of A → mol A → mole ratio → mol B → M·V of B",
                  12, GREEN, "700"))
    b.append(text(60, y + 46, "与 Ch.10 四步完全同构，只是上下桥换成了浓度与体积。", 10.5, INK))
    return svg(W, y + 86, "".join(b))


# --------------------------------------------------------------------------
def build_dilution():
    """C1V1 = C2V2 visual."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Dilution: Add Water, Not Molecules｜稀释：加水不加分子", 17, INK, "700", "middle"))
    y += 26

    # stock beaker (concentrated) vs diluted beaker
    def beaker(bx, by, w_, h_, fill_level, dots, col, label1, label2):
        b.append(rect(bx, by, w_, h_, BG, INK, 1.6, 4))
        fy = by + h_ * (1 - fill_level)
        b.append(rect(bx + 3, fy, w_ - 6, h_ * fill_level - 3, col, "none", 0, 2))
        for dx, dy in dots:
            b.append(circle(bx + dx, fy + dy, 3.2, INK, INK, 0.8))
        b.append(text(bx + w_ / 2, by + h_ + 20, label1, 12, INK, "700", "middle"))
        b.append(text(bx + w_ / 2, by + h_ + 38, label2, 10.5, MUTED, "400", "middle"))

    dots1 = [(20, 15), (45, 30), (70, 18), (30, 42), (60, 48), (85, 35), (95, 15), (15, 35), (50, 12), (80, 55), (25, 55), (65, 25)]
    dots2 = dots1  # same count
    beaker(70, y, 120, 110, 0.8, dots1, BLUE_F, "Stock 储备液", "C₁ = 1.0 mol/L, V₁ = 100 mL")
    beaker(470, y, 120, 110, 0.8, dots2, "#FEF3E0", "Diluted 稀释液", "C₂ = 0.25 mol/L, V₂ = 400 mL")

    # arrow with water
    b.append(arrow1(210, y + 55, 450, y + 55))
    b.append(text(330, y + 40, "+ water 加水", 11.5, BLUE, "700", "middle"))
    b.append(text(330, y + 76, "400 mL total", 10.5, MUTED, "400", "middle"))
    y += 110 + 56

    b.append(rect(55, y, 570, 70, HEAD, LINE, 1.2, 8))
    b.append(text(75, y + 26, "C₁V₁ = C₂V₂      →      V₂ = C₁V₁ / C₂ = (1.0)(100) / 0.25 = 400 mL",
                  12.5, INK, "700"))
    b.append(text(75, y + 50, "Units just have to match on both sides (mL with mL) — no need to convert to L.",
                  10.5, MUTED))
    y += 70 + 16
    b.append(rect(55, y, 570, 44, RED_F, RED, 1.2, 8))
    b.append(text(75, y + 19, "Same molecules, bigger volume → lower concentration. Diluting never destroys solute.",
                  11.5, RED, "700"))
    b.append(text(75, y + 37, "分子数不变、体积变大 → 浓度变小。稀释前后溶质的量（mol）恒等。", 10.5, INK))
    return svg(W, y + 64, "".join(b))


# --------------------------------------------------------------------------
def build_net_ionic():
    """Four steps to a net ionic equation."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Net Ionic Equations in 4 Steps｜净离子方程式四步", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "AgNO₃(aq) + NaCl(aq) → AgCl(s) + NaNO₃(aq)", 13, INK, "700", "middle"))
    y += 24

    rows = [
        ("1  Balance the formula equation", "先配平分子方程式（此处已平）", BLUE, BLUE_F),
        ("2  Split ONLY strong aqueous electrolytes into ions",
         "Ag⁺ + NO₃⁻ + Na⁺ + Cl⁻ → AgCl(s) + Na⁺ + NO₃⁻   (AgCl 固体不拆)", GREEN, GREEN_F),
        ("3  Cancel spectator ions appearing on both sides",
         "Na⁺ 与 NO₃⁻ 两边都在 → 划掉（spectator ions 旁观离子）", AMBER, AMBER_F),
        ("4  Check atoms AND charge",
         "Ag⁺(aq) + Cl⁻(aq) → AgCl(s)   charge +1 + (−1) = 0 ✔", PURPLE, PURPLE_F),
    ]
    for t, s, col, fl in rows:
        b.append(rect(50, y, 580, 60, fl, col, 1.3, 8))
        b.append(text(70, y + 24, t, 12.5, col, "700"))
        b.append(text(70, y + 45, s, 11, INK))
        y += 60 + 10

    y += 4
    b.append(rect(50, y, 580, 62, HEAD, LINE, 1.2, 8))
    b.append(text(70, y + 24, "The net ionic equation shows the actual chemistry: only Ag⁺ meets Cl⁻.",
                  12, INK, "700"))
    b.append(text(70, y + 46, "Na⁺ 和 NO₃⁻ 只是“围观群众”——换一对旁观离子，反应照样发生。", 10.5, MUTED))
    y += 62 + 14
    b.append(text(340, y + 4, "Charge check catches most errors: left +1 + (−1) = 0 = right. 电荷守恒自查。",
                  10.5, MUTED, "400", "middle"))
    return svg(W, y + 26, "".join(b))


# --------------------------------------------------------------------------
def build_titration():
    """Titration: setup, endpoint vs equivalence point, calculation chain."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Titration Anatomy｜滴定解剖图", 17, INK, "700", "middle"))
    y += 20

    # burette
    bx, by, bw, bh = 150, y + 6, 44, 190
    b.append(rect(bx, by, bw, bh, BG, INK, 1.6, 4))
    b.append(rect(bx + 3, by + 30, bw - 6, bh - 40, "#DBEAFE", "none", 0, 2))
    b.append(text(bx + bw + 10, by + 26, "burette 滴定管", 11, INK, "700"))
    b.append(text(bx + bw + 10, by + 44, "standard NaOH 标准液", 10, MUTED))
    b.append(text(bx + bw + 10, by + 62, "read initial & final 读初读数与终读数", 10, MUTED))
    # flask
    fx, fy, fw, fh = 300, y + 96, 90, 100
    b.append(f'<path d="M {fx+25},{fy} L {fx+25},{fy+30} L {fx+5},{fy+fh} Q {fx+fw/2},{fy+fh+14} {fx+fw-5},{fy+fh} L {fx+fw-25},{fy+30} L {fx+fw-25},{fy} Z" fill="#FEE2E2" stroke="{INK}" stroke-width="1.6"/>')
    b.append(text(fx + fw / 2, fy + fh + 26, "flask 锥形瓶: HCl + indicator", 10.5, INK, "400", "middle"))
    b.append(text(fx + fw / 2, fy + fh + 44, "指示剂 2–3 滴即可", 10, MUTED, "400", "middle"))
    # drop
    b.append(f'<path d="M {bx+bw/2-3},{by+bh+6} q 3,6 3,9 a 3,3 0 1 1 -6,0 q 0,-3 3,-9" fill="#2B6CB0"/>')
    b.append(text(430, y + 60, "swirl while adding 边滴边摇", 10.5, MUTED))
    b.append(text(430, y + 78, "stop at first permanent colour", 10.5, MUTED))
    b.append(text(430, y + 96, "变色即停（且半分钟不褪）", 10.5, INK))
    y += 190 + 20

    # endpoint vs equivalence
    b.append(rect(45, y, 590, 58, AMBER_F, AMBER, 1.3, 8))
    b.append(text(65, y + 23, "Equivalence point 等当点: exactly stoichiometric moles 恰好按系数比反应完",
                  11.5, INK, "700"))
    b.append(text(65, y + 43, "End point 终点: the indicator changes colour 变色点 — ≈ but not exactly equal（误差来源）",
                  11.5, AMBER, "700"))
    y += 58 + 16

    # calculation chain
    b.append(rect(45, y, 590, 92, HEAD, LINE, 1.2, 8))
    b.append(text(65, y + 24, "Calculation chain｜计算链", 12.5, INK, "700"))
    b.append(text(65, y + 48, "V(base) × M(base) = 0.02500 L × 0.100 M = 0.002500 mol NaOH", 11.5, INK))
    b.append(text(65, y + 70, "→ 1:1 ratio → 0.002500 mol HCl ÷ V(acid) 0.02500 L = 0.100 M HCl", 11.5, GREEN, "700"))
    y += 92 + 16

    b.append(rect(45, y, 590, 44, RED_F, RED, 1.2, 8))
    b.append(text(65, y + 19, "Safety: ALWAYS acid into water when diluting. 稀释浓酸时“酸入水”，沿壁缓搅。",
                  11.5, RED, "700"))
    b.append(text(65, y + 37, "平行滴 2–3 次取平均；单次偏差超 0.05 mL 重滴。", 10.5, INK))
    return svg(W, y + 64, "".join(b))


# --------------------------------------------------------------------------
def main():
    figs = {
        "ch13-four-bridges.svg": build_four_bridges,
        "ch13-dilution.svg": build_dilution,
        "ch13-net-ionic-workflow.svg": build_net_ionic,
        "ch13-titration.svg": build_titration,
    }
    for name, fn in figs.items():
        s = fn()
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)


if __name__ == "__main__":
    main()
