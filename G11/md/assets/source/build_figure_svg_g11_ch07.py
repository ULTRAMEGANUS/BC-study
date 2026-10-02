# -*- coding: utf-8 -*-
"""
G11 Ch.7 figure builder — Lewis structures, electronegativity, bonding, IMF.
Canvas height computed from content (never hard-coded).

Figures:
  ch07-lewis-workflow.svg    Four-step Lewis workflow + NH3 worked example
  ch07-bond-continuum.svg    Delta-EN continuum from covalent to ionic
  ch07-shape-polarity.svg    Four shapes: bond dipoles add or cancel
  ch07-imf-ladder.svg        Intramolecular vs intermolecular; the IMF ladder
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
def build_lewis_workflow():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Four Steps to Any Lewis Structure｜路易斯结构四步法",
                  15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Works for molecules and for polyatomic ions (add or remove electrons for the charge first).",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "分子和多原子离子通用（若是离子，第一步先按电荷加减电子）。", 11.5, MUTED))
    y += 24

    steps = [
        ("1 · Count｜数价电子", "Sum valence electrons of every atom.", "NH₃: 5 + 3×1 = 8", BLUE, BLUE_F),
        ("2 · Skeleton｜摆骨架", "Least electronegative atom in the centre; H never central.",
         "N in the middle, 3 H around", GREEN, GREEN_F),
        ("3 · Octets｜补八隅", "Bond outer atoms to centre, then finish their octets.",
         "3 bonds use 6 e⁻; give each H its duet", AMBER, AMBER_F),
        ("4 · Leftovers｜余电子", "Leftover electrons go on the central atom.",
         "8 − 6 = 2 left → one lone pair on N", PURPLE, PURPLE_F),
    ]
    lx, lw, lh, gap = 40, 300, 66, 10
    for i, (ttl, en, ap, col, fl) in enumerate(steps):
        cy = y + i * (lh + gap)
        b.append(rect(lx, cy, lw, lh, fl, col, 1.0, 6))
        b.append(text(lx + 10, cy + 19, ttl, 11.5, col, "700"))
        b.append(text(lx + 10, cy + 36, en, 10, MUTED))
        b.append(text(lx + 10, cy + 53, ap, 10, INK, "600"))
    bottom = y + 4 * (lh + gap)

    # right panel: NH3 drawing
    rx, rw = 356, 284
    ry = y
    rh = bottom - y - 4
    b.append(rect(rx, ry, rw, rh, HEAD, "#CBD2D9", 1.0, 8))
    b.append(text(rx + rw / 2, ry + 22, "NH₃ — the answer｜结果", 12, INK, "700", "middle"))
    nx = rx + rw / 2
    ny = ry + 96
    b.append(text(nx - 66, ny - 14, "..", 14, RED, "700"))          # lone pair above N
    b.append(text(nx, ny, "N", 16, INK, "700", "middle"))
    b.append(text(nx - 62, ny + 5, "H", 14, INK, "600"))
    b.append(text(nx + 62, ny + 5, "H", 14, INK, "600"))
    b.append(text(nx, ny + 44, "H", 14, INK, "600"))
    b.append(line(nx - 14, ny - 2, nx - 50, ny + 2, INK, 1.6))
    b.append(line(nx + 14, ny - 2, nx + 50, ny + 2, INK, 1.6))
    b.append(line(nx, ny + 12, nx, ny + 32, INK, 1.6))
    b.append(text(nx, ry + rh - 16, "lone pair（孤对）留在中心原子 N 上", 10.5, MUTED, "400", "middle"))

    yy = bottom + 12
    b.append(text(40, yy, "If the central atom still lacks an octet, move a lone pair into a bonding position —", 11, MUTED))
    yy += 15
    b.append(text(40, yy, "that is how double and triple bonds appear (see CO₂ in Fig. 7-3).", 11, MUTED))
    yy += 16
    b.append(text(40, yy, "若中心原子凑不满八隅，把外层孤对推进成键位置——双键、三键就是这么来的。", 10.5, MUTED))
    return svg(W, yy + 18, "".join(b))


# --------------------------------------------------------------------------
def build_bond_continuum():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Bonding Is a Continuum, Not a Switch｜键型是连续谱，不是开关",
                  15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Electronegativity difference, ΔEN, estimates where a bond sits on the slide.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "电负性差 ΔEN 估计化学键在滑轴上的位置——从共价滑到离子。", 11.5, MUTED))
    y += 30

    ax0, ax1, ay = 60, 620, y
    segs = [
        (0.0, 0.5, BLUE, BLUE_F, "covalent\nnon-polar｜非极性共价"),
        (0.5, 1.8, GREEN, GREEN_F, "covalent\npolar｜极性共价"),
        (1.8, 3.5, RED, RED_F, "ionic｜离子键"),
    ]
    def pos(v):
        return ax0 + (v / 3.5) * (ax1 - ax0)
    for v0, v1, col, fl, lab in segs:
        x0, x1 = pos(v0), pos(v1)
        b.append(rect(x0, ay, x1 - x0, 34, fl, col, 1.2, 0))
        parts = lab.split("\n")
        l1 = parts[0]
        l2 = parts[1] if len(parts) > 1 else ""
        b.append(text((x0 + x1) / 2, ay + 15, l1, 11, col, "700", "middle"))
        b.append(text((x0 + x1) / 2, ay + 29, l2, 10.5, col, "600", "middle"))
    for v in (0.0, 0.5, 1.8, 3.5):
        x = pos(v)
        b.append(line(x, ay + 34, x, ay + 40, MUTED, 1.2))
        b.append(text(x, ay + 52, f"{v:.1f}" if v else "0", 10, MUTED, "600", "middle"))

    py = ay + 84
    points = [
        (0.0, "H–H  0.0", True),
        (0.4, "C–H  0.4", False),
        (0.9, "H–Cl / N–H  0.9", True),
        (1.4, "O–H  1.4", False),
        (2.1, "Na–Cl  2.1", True),
        (3.3, "Cs–F  3.3", False),
    ]
    for v, lab, above in points:
        x = pos(v)
        b.append(circle(x, py, 4, PURPLE, PURPLE, 1))
        if above:
            b.append(line(x, py - 5, x, py - 14, PURPLE, 1))
            b.append(text(x, py - 18, lab, 9.5, INK, "600", "middle"))
        else:
            b.append(line(x, py + 5, x, py + 14, PURPLE, 1))
            b.append(text(x, py + 26, lab, 9.5, INK, "600", "middle"))
    y = py + 46

    b.append(text(40, y, "The cut-offs are empirical — HF (ΔEN = 1.9) crosses the line yet is still a", 10.5, MUTED))
    y += 14
    b.append(text(40, y, "molecular, polar-covalent substance. Read the number as a hint, not a verdict.", 10.5, MUTED))
    y += 16
    b.append(text(40, y, "阈值是经验线：HF（ΔEN=1.9）虽越线，仍是极性共价分子——数值是提示，不是判决。", 10.5, INK, "600"))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def build_shape_polarity():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Shape Decides Polarity｜形状决定分子极性", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Bond dipoles are arrows. If the shape is symmetric, the arrows cancel.", 11.5, MUTED))
    y += 16
    b.append(text(40, y, "键偶极是箭头：形状对称则互相抵消，不对称则留下净偶极。", 11.5, MUTED))
    y += 22

    panels = [
        # (cx, formula title, verdict, verdict color, verdict fill)
        (130, "CO₂", "NON-POLAR｜非极性", BLUE, BLUE_F),
        (295, "H₂O", "POLAR｜极性", RED, RED_F),
        (465, "CH₄", "NON-POLAR｜非极性", BLUE, BLUE_F),
        (618, "NH₃", "POLAR｜极性", RED, RED_F),
    ]
    py = y + 70
    for cx, f, verdict, col, fl in panels:
        b.append(text(cx, y + 8, f, 14, INK, "700", "middle"))
    # CO2
    cx = 130
    b.append(text(cx - 62, py, "O", 13, INK, "600", "middle"))
    b.append(text(cx, py, "C", 13, INK, "700", "middle"))
    b.append(text(cx + 62, py, "O", 13, INK, "600", "middle"))
    b.append(line(cx - 54, py - 4, cx - 12, py - 4, INK, 1.6))
    b.append(line(cx + 12, py - 4, cx + 54, py - 4, INK, 1.6))
    b.append(text(cx - 90, py - 26, "←", 13, BLUE, "700", "middle"))
    b.append(text(cx + 90, py - 26, "→", 13, BLUE, "700", "middle"))
    b.append(text(cx, py + 34, "arrows cancel｜抵消", 9.5, MUTED, "400", "middle"))
    # H2O
    cx = 295
    b.append(text(cx, py - 22, "O", 13, INK, "700", "middle"))
    b.append(text(cx - 46, py + 16, "H", 13, INK, "600", "middle"))
    b.append(text(cx + 46, py + 16, "H", 13, INK, "600", "middle"))
    b.append(line(cx - 12, py - 16, cx - 40, py + 10, INK, 1.6))
    b.append(line(cx + 12, py - 16, cx + 40, py + 10, INK, 1.6))
    b.append(text(cx, py - 44, "↑ net dipole｜净偶极朝 O", 9.5, RED, "600", "middle"))
    b.append(text(cx, py + 34, "bent｜角形，不对称", 9.5, MUTED, "400", "middle"))
    # CH4
    cx = 465
    b.append(text(cx, py - 16, "H", 13, INK, "600", "middle"))
    b.append(text(cx - 50, py + 10, "H", 13, INK, "600", "middle"))
    b.append(text(cx + 50, py + 10, "H", 13, INK, "600", "middle"))
    b.append(text(cx + 14, py + 40, "H", 13, INK, "600", "middle"))
    b.append(text(cx, py + 4, "C", 13, INK, "700", "middle"))
    b.append(line(cx - 6, py - 4, cx - 44, py + 6, INK, 1.6))
    b.append(line(cx + 6, py - 4, cx + 44, py + 6, INK, 1.6))
    b.append(line(cx, py - 8, cx, py - 10, INK, 1.6))
    b.append(line(cx + 6, py + 10, cx + 12, py + 30, INK, 1.6))
    b.append(text(cx, py + 58, "tetrahedral｜四面体对称", 9.5, MUTED, "400", "middle"))
    # NH3
    cx = 618
    b.append(text(cx, py - 20, "N", 13, INK, "700", "middle"))
    b.append(text(cx - 40, py + 18, "H", 13, INK, "600", "middle"))
    b.append(text(cx + 40, py + 18, "H", 13, INK, "600", "middle"))
    b.append(text(cx, py + 40, "H", 13, INK, "600", "middle"))
    b.append(line(cx - 12, py - 14, cx - 34, py + 12, INK, 1.6))
    b.append(line(cx + 12, py - 14, cx + 34, py + 12, INK, 1.6))
    b.append(line(cx, py - 8, cx, py + 30, INK, 1.6))
    b.append(text(cx, py - 42, ".. ｜净偶极朝 N", 9.5, RED, "600", "middle"))
    b.append(text(cx, py + 58, "pyramidal｜三角锥", 9.5, MUTED, "400", "middle"))
    # verdict tags
    for cx, f, verdict, col, fl in panels:
        vy = py + 76
        b.append(rect(cx - 62, vy, 124, 22, fl, col, 1.0, 11))
        b.append(text(cx, vy + 15, verdict, 9.5, col, "700", "middle"))
    y = py + 110

    b.append(text(40, y, "Bond polarity is necessary but not sufficient — a symmetric shape can cancel it.", 11, MUTED))
    y += 16
    b.append(text(40, y, "键有极性是必要条件，不是充分条件——对称形状可以把它整个抵消掉。", 11, MUTED))
    y += 16
    b.append(text(40, y, "先判键（ΔEN），再判形（VSEPR），最后合成分子极性——三步缺一不可。", 11, INK, "600"))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def build_imf_ladder():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Intramolecular vs Intermolecular｜分子内 vs 分子间", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Boiling water breaks the forces BETWEEN molecules — the O–H bonds survive.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "水沸腾断的是分子之间的力——分子内的 O–H 共价键完好无损。", 11.5, MUTED))
    y += 24

    # two compare boxes
    bw, bh = 290, 108
    b.append(rect(40, y, bw, bh, BLUE_F, BLUE, 1.2, 8))
    b.append(text(40 + bw / 2, y + 22, "Intramolecular｜分子内", 12.5, BLUE, "700", "middle"))
    b.append(text(40 + bw / 2, y + 44, "O–H covalent bond inside one molecule", 10.5, INK, "400", "middle"))
    b.append(text(40 + bw / 2, y + 62, "O–H 共价键（分子内部）", 10.5, MUTED, "400", "middle"))
    b.append(text(40 + bw / 2, y + 86, "≈ 463 kJ/mol · survives boiling｜沸腾不断", 10.5, BLUE, "700", "middle"))

    b.append(rect(350, y, bw, bh, RED_F, RED, 1.2, 8))
    b.append(text(350 + bw / 2, y + 22, "Intermolecular｜分子间", 12.5, RED, "700", "middle"))
    b.append(text(350 + bw / 2, y + 44, "hydrogen bond between two molecules", 10.5, INK, "400", "middle"))
    b.append(text(350 + bw / 2, y + 62, "分子之间的氢键", 10.5, MUTED, "400", "middle"))
    b.append(text(350 + bw / 2, y + 86, "≈ 20 kJ/mol · broken at boiling｜沸腾即断", 10.5, RED, "700", "middle"))
    y += bh + 10
    b.append(text(40, y, "That ~20× gap is why water boils at 100 °C instead of decomposing.", 10.5, MUTED))
    y += 14
    b.append(text(40, y, "约 20 倍的差距，就是水烧到 100 °C 只汽化、不分解的原因。", 10.5, MUTED))
    y += 24

    b.append(text(40, y, "The IMF ladder, weakest to strongest｜分子间作用力阶梯（由弱到强）",
                  12, INK, "700"))
    y += 14
    rows = [
        ("London dispersion｜色散力", "all molecules; grows with electron count｜所有分子都有，随电子数增大",
         150, BLUE, BLUE_F),
        ("Dipole-dipole｜偶极-偶极", "polar molecules only｜只存在于极性分子之间",
         250, GREEN, GREEN_F),
        ("Hydrogen bonding｜氢键", "H bonded to N, O or F｜H 直接连在 N、O、F 上",
         350, RED, RED_F),
    ]
    for i, (nm, note, wdt, col, fl) in enumerate(rows):
        b.append(rect(40, y, 230, 30, HEAD, "#CBD2D9", 0.9, 5))
        b.append(text(50, y + 20, nm, 11, INK, "700"))
        b.append(rect(286, y, wdt, 30, fl, col, 1.0, 5))
        b.append(text(296, y + 20, note, 10, MUTED))
        y += 38
    y += 6
    b.append(text(40, y, "All three are weak next to covalent bonds — that is why molecular compounds", 10.5, MUTED))
    y += 14
    b.append(text(40, y, "melt and boil so easily.", 10.5, MUTED))
    y += 16
    b.append(text(40, y, "三类作用力都远弱于共价键——这正是分子型物质熔沸点低的原因。", 10.5, MUTED))
    y += 16
    b.append(text(40, y, "溶解看「相似相溶」：极性溶剂抓极性/能氢键的溶质，非极性溶剂抓非极性溶质。", 10.5, INK, "600"))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "ch07-lewis-workflow.svg": build_lewis_workflow(),
        "ch07-bond-continuum.svg": build_bond_continuum(),
        "ch07-shape-polarity.svg": build_shape_polarity(),
        "ch07-imf-ladder.svg": build_imf_ladder(),
    }
    for name, data in figs.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(data)
        print("wrote", name, len(data), "bytes")


if __name__ == "__main__":
    main()
