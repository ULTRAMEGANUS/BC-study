# -*- coding: utf-8 -*-
"""
G11 Ch.6 figure builder — periodic table and periodic trends.
Canvas height computed from content (never hard-coded).

Figures:
  ch06-trends-overview.svg   Five trends, direction across and down
  ch06-radius-ie.svg         Period 3 radius vs first ionization energy (real data)
  ch06-zeff-shielding.svg    Why trends happen: charge vs shielding
  ch06-ie-staircase.svg      The IE staircase and its two dips (periods 2 and 3)
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


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_trends_overview():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Five Periodic Trends｜五大周期性趋势", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Same map for every trend: what happens across a period, and what happens down a group.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "每条趋势都用同一张地图读：横着（同周期）怎样，竖着（同主族）怎样。", 11.5, MUTED))
    y += 24

    CX = [55, 250, 460]
    b.append(rect(40, y, W - 80, 26, HEAD, "#CBD2D9", 1.0, 6))
    for t, x in zip(("Trend｜趋势", "Across (L→R)｜横向（左→右）", "Down (T→B)｜纵向（上→下）"), CX):
        b.append(text(x, y + 18, t, 11.5, MUTED, "700"))
    y += 26

    rows = [
        ("Atomic radius｜原子半径", "Decreases｜减小", "Increases｜增大", BLUE, BLUE_F),
        ("Ionization energy｜第一电离能", "Increases｜增大", "Decreases｜减小", GREEN, GREEN_F),
        ("Electronegativity｜电负性", "Increases｜增大", "Decreases｜减小", GREEN, GREEN_F),
        ("Metallic character｜金属性", "Decreases｜减小", "Increases｜增大", AMBER, AMBER_F),
        ("Ionic radius｜离子半径", "Cation < atom｜阳离子<原子", "Anion > atom｜阴离子>原子", PURPLE, PURPLE_F),
    ]
    rh = 32
    for i, (tr, ac, dn, col, fl) in enumerate(rows):
        b.append(rect(40, y, W - 80, rh, fl if i % 2 == 0 else BG, "#E1E7EC", 0.8, 4))
        b.append(text(CX[0], y + 21, tr, 11.5, col, "700"))
        b.append(text(CX[1], y + 21, ac, 11, INK))
        b.append(text(CX[2], y + 21, dn, 11, INK))
        y += rh
    y += 18
    b.append(text(40, y, "Across: same shells, more protons — the pull on outer electrons grows.", 11.5, MUTED))
    y += 16
    b.append(text(40, y, "Down: new shells added — outer electrons sit farther and are shielded.", 11.5, MUTED))
    y += 16
    b.append(text(40, y, "横向：层数不变、核电荷增大 → 对最外层电子的引力增强。", 11.5, MUTED))
    y += 16
    b.append(text(40, y, "纵向：层数增多、内层电子把核挡住 → 外层电子被拉得松。", 11.5, MUTED))
    y += 16
    b.append(text(40, y, "离子半径一行比较的是「离子 vs 它自己的原子」，不是左右趋势。", 10.5, MUTED))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def build_radius_ie():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Period 3: Radius Falls, Ionization Rises｜第三周期：半径降、电离能升",
                  15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Real values for Na → Cl. Same electron shells, growing nuclear charge.", 11.5, MUTED))
    y += 16
    b.append(text(40, y, "Na → Cl 的真实数据：电子层数相同，核电荷逐一增大。", 11.5, MUTED))
    y += 20

    names = ["Na", "Mg", "Al", "Si", "P", "S", "Cl"]
    radii = [186, 160, 143, 118, 110, 104, 99]
    ies = [496, 738, 578, 787, 1012, 1000, 1251]
    dip = {"Al", "S"}
    x0, bw, gap = 92, 42, 24

    b.append(text(40, y, "Atomic radius (pm)｜原子半径（pm）", 12, BLUE, "700"))
    y += 8
    base1 = y + 128
    for i, (nm, v) in enumerate(zip(names, radii)):
        x = x0 + i * (bw + gap)
        h = v / 186 * 120
        b.append(rect(x, base1 - h, bw, h, BLUE, "#CBD2D9", 0.8, 3))
        b.append(text(x + bw / 2, base1 - h - 5, str(v), 9.5, MUTED, "600", "middle"))
        b.append(text(x + bw / 2, base1 + 15, nm, 11, INK, "700", "middle"))
    b.append(line(70, base1, 640, base1, "#CBD2D9", 1.2))
    y = base1 + 34

    b.append(text(40, y, "First ionization energy (kJ/mol)｜第一电离能（kJ/mol）", 12, GREEN, "700"))
    y += 8
    base2 = y + 118
    for i, (nm, v) in enumerate(zip(names, ies)):
        x = x0 + i * (bw + gap)
        h = v / 1251 * 110
        col = AMBER if nm in dip else GREEN
        b.append(rect(x, base2 - h, bw, h, col, "#CBD2D9", 0.8, 3))
        b.append(text(x + bw / 2, base2 - h - 5, str(v), 9.5, MUTED, "600", "middle"))
        b.append(text(x + bw / 2, base2 + 15, nm, 11, INK, "700", "middle"))
    b.append(line(70, base2, 640, base2, "#CBD2D9", 1.2))
    y = base2 + 36

    b.append(text(40, y, "Ar is omitted (noble-gas radius is not comparable); its IE 1527 kJ/mol is the period high.",
                  10.5, MUTED))
    y += 15
    b.append(text(40, y, "稀有气体 Ar 未画（半径不可比）；其电离能 1527 kJ/mol 为全周期最高。", 10.5, MUTED))
    y += 15
    b.append(text(40, y, "橙色两处回落（Al 低于 Mg、S 低于 P）见图 6-4 的解释。", 10.5, AMBER))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def build_zeff_shielding():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Why Trends Happen: Charge vs Shielding｜趋势从哪来：电荷与屏蔽",
                  15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "An outer electron feels roughly: nuclear charge minus shielding by inner electrons.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "外层电子感受到的引力 ≈ 核电荷 − 内层电子的屏蔽。", 11.5, MUTED))
    y += 22

    def atom(cx, cy, shell_ns, z, col):
        parts = []
        n = len(shell_ns)
        rmax = 40 if n <= 3 else 47
        for i, cnt in enumerate(shell_ns):
            r = rmax * (i + 1) / n
            parts.append(circle(cx, cy, r, "none", col, 1.3))
            lx = cx + r * 0.72 + 4
            ly = cy - r * 0.72 - 2
            parts.append(text(lx, ly, str(cnt), 9, col, "700"))
        parts.append(text(cx, cy + 4, "+" + str(z), 11, INK, "700", "middle"))
        return parts

    # Across a period: Na -> Cl
    b.append(text(40, y, "Across a period (Na → Cl)｜横向（Na → Cl）", 12, BLUE, "700"))
    y += 12
    cy1 = y + 58
    b += atom(150, cy1, [2, 8, 1], 11, BLUE)
    b.append(line(215, cy1, 285, cy1, MUTED, 2))
    b.append(text(250, cy1 - 8, "→", 15, MUTED, "700", "middle"))
    b += atom(370, cy1, [2, 8, 7], 17, BLUE)
    tx = 470
    for j, ln in enumerate(["shells: 3 → 3｜层数不变",
                            "shielding ≈ same｜屏蔽不变",
                            "charge 11 → 17｜核电荷增大",
                            "pull stronger｜引力更强"]):
        b.append(text(tx, cy1 - 26 + j * 18, ln, 10.5, MUTED if j < 3 else BLUE, "700" if j == 3 else "400"))
    y = cy1 + 68

    # Down a group: Na -> K
    b.append(text(40, y, "Down a group (Na → K)｜纵向（Na → K）", 12, GREEN, "700"))
    y += 12
    cy2 = y + 62
    b += atom(150, cy2, [2, 8, 1], 11, GREEN)
    b.append(line(215, cy2, 285, cy2, MUTED, 2))
    b.append(text(250, cy2 - 8, "→", 15, MUTED, "700", "middle"))
    b += atom(370, cy2, [2, 8, 8, 1], 19, GREEN)
    for j, ln in enumerate(["shells: 3 → 4｜层数 +1",
                            "shielding: 8 → 18｜屏蔽增大",
                            "outer shell farther｜外层更远",
                            "pull weaker｜引力更弱"]):
        b.append(text(tx, cy2 - 26 + j * 18, ln, 10.5, MUTED if j < 3 else GREEN, "700" if j == 3 else "400"))
    y = cy2 + 78

    b.append(text(40, y, "同一张图读两条趋势：横向看「电荷加码」，纵向看「层数与屏蔽加码」。", 10.5, MUTED))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def build_ie_staircase():
    W = 680
    b = []
    b.append(text(W / 2, 26, "The Ionization Staircase and Its Dips｜电离能的台阶与回落",
                  15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "IE climbs across each period — except at two predictable spots (circled).",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "电离能沿周期爬升——只有两处规律性回落（红圈处）。", 11.5, MUTED))
    y += 18

    names2 = ["Li", "Be", "B", "C", "N", "O", "F", "Ne"]
    ie2 = [520, 900, 801, 1086, 1402, 1314, 1681, 2081]
    names3 = ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"]
    ie3 = [496, 738, 578, 787, 1012, 1000, 1251, 1527]
    dip = {"B", "O", "Al", "S"}
    xs = [100 + i * 74 for i in range(8)]

    def plot(names, ies, vmax, top, base, col):
        pts = []
        for i, v in enumerate(ies):
            yy = base - v / vmax * 100
            pts.append((xs[i], yy))
        poly = " ".join(f"{x:.0f},{yy:.0f}" for x, yy in pts)
        s = f'<polyline points="{poly}" fill="none" stroke="{col}" stroke-width="2"/>'
        for i, (x, yy) in enumerate(pts):
            nm = names[i]
            c = RED if nm in dip else col
            s += circle(x, yy, 3.5, c, c, 1)
            s += text(x, yy - 7, str(ies[i]), 8.5, MUTED, "600", "middle")
            if nm in dip:
                s += circle(x, yy, 9, "none", RED, 1.6)
            s += text(x, base + 16, nm, 10.5, INK, "700", "middle")
        return s, pts

    b.append(text(40, y, "Period 2｜第二周期", 12, BLUE, "700"))
    y += 8
    base1 = y + 112
    s, p2 = plot(names2, ie2, 2081, 0, base1, BLUE)
    b.append(s)
    b.append(line(70, base1, 650, base1, "#CBD2D9", 1.2))
    # annotations
    bx, by = p2[2]
    b.append(text(bx + 12, by + 22, "B < Be: new p subshell", 9, RED))
    ox, oy = p2[5]
    b.append(text(ox + 12, oy + 22, "O < N: pairing repulsion", 9, RED))
    y = base1 + 34

    b.append(text(40, y, "Period 3｜第三周期", 12, GREEN, "700"))
    y += 8
    base2 = y + 112
    s, p3 = plot(names3, ie3, 1527, 0, base2, GREEN)
    b.append(s)
    b.append(line(70, base2, 650, base2, "#CBD2D9", 1.2))
    ax, ay = p3[2]
    b.append(text(ax + 12, ay + 24, "Al < Mg: new p subshell", 9, RED))
    sx, sy = p3[5]
    b.append(text(sx + 12, sy + 24, "S < P: pairing repulsion", 9, RED))
    y = base2 + 36

    b.append(text(40, y, "B/Al：新电子进入 p 亚层，能量略高、更易失去。", 10.5, MUTED))
    y += 15
    b.append(text(40, y, "O/S：第 4 个 p 电子开始配对，成对排斥使它更易失去。", 10.5, MUTED))
    y += 15
    b.append(text(40, y, "两处回落都能用电子排布预言——这是模型威力的最好证据。", 10.5, INK, "600"))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "ch06-trends-overview.svg": build_trends_overview(),
        "ch06-radius-ie.svg": build_radius_ie(),
        "ch06-zeff-shielding.svg": build_zeff_shielding(),
        "ch06-ie-staircase.svg": build_ie_staircase(),
    }
    for name, data in figs.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(data)
        print("wrote", name, len(data), "bytes")


if __name__ == "__main__":
    main()
