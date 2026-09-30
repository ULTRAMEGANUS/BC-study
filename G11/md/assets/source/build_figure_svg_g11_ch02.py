# -*- coding: utf-8 -*-
"""
G11 Ch.2 figure builder — hydrocarbons: structure, naming, isomers.
Canvas height computed from content (never hard-coded).

Figures:
  ch02-carbon-four-bonds.svg    Carbon's four bonds -> chains, branches, rings
  ch02-three-formulas.svg       Molecular vs condensed vs skeletal
  ch02-iupac-four-steps.svg     IUPAC naming four-step procedure
  ch02-isomers-c4c5.svg         Structural isomers of C4H10 and C5H12
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "figures"))

BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#52606D"
LINE = "#9AA5B1"
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


def circle(cx, cy, r, fill=BG, stroke=LINE, sw=1.4):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, color=LINE, sw=1.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}"{d}/>')


def arrow_defs(cid, color):
    return (f'<defs><marker id="{cid}" markerWidth="10" markerHeight="8" refX="9" refY="4" '
            f'orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="{color}"/></marker></defs>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


def build_carbon_four_bonds():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Carbon's Four Bonds｜碳的四个键", 15, INK, "600", "middle"))
    y = 50
    b.append(text(40, y, "Carbon has 4 valence electrons, so it forms 4 covalent bonds —", 12.5, MUTED))
    y += 18
    b.append(text(40, y, "and it can bond to other carbons, building long chains.", 12.5, MUTED))
    y += 22
    b.append(text(40, y, "碳有 4 个价电子，因此形成 4 个共价键——并且能与其它碳原子相连。这是有机化学化合物数量庞大的根本原因。", 12, MUTED))
    y += 30

    panels = [
        ("CHAIN｜链", "C—C—C—C—C", "直链：碳首尾相连", BLUE, BLUE_F),
        ("BRANCH｜支链", "C—C—C\n    |\n    C", "支链：从主链分岔", GREEN, GREEN_F),
        ("RING｜环", "C—C\n|   |\nC—C", "成环：首尾闭合", PURPLE, PURPLE_F),
    ]
    pw = (W - 80 - 2 * 20) / 3
    ph = 120
    for i, (t, sub, cn, col, fl) in enumerate(panels):
        x = 40 + i * (pw + 20)
        b.append(rect(x, y, pw, ph, fl, col, 1.3, 10))
        b.append(text(x + pw / 2, y + 26, t, 13, col, "700", "middle"))
        for j, s in enumerate(sub.split("\n")):
            b.append(text(x + pw / 2, y + 54 + j * 18, s, 13, INK, "600", "middle"))
        b.append(text(x + pw / 2, y + ph - 14, cn, 11.5, MUTED, "400", "middle"))
    y += ph + 22

    b.append(rect(40, y, W - 80, 66, AMBER_F, AMBER, 1.2, 8))
    b.append(text(58, y + 24, "📏 Rule｜规则：every carbon shows exactly FOUR bonds in a structure.", 12.5, AMBER, "600"))
    b.append(text(58, y + 46, "骨架式里每个顶点就是 1 个碳；氢不画出来，但要按 4 键补齐。这是检查结构图画错没画错的第一把尺子。", 11.5, MUTED))
    y += 82
    return svg(W, y, "".join(b))


def build_three_formulas():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Three Ways to Write the Same Molecule｜同一个分子的三种写法", 15, INK, "600", "middle"))
    y = 52

    rows = [
        ("Molecular｜分子式", "C₄H₁₀", "只给原子种类与个数；看不出结构", BLUE, BLUE_F),
        ("Condensed｜凝聚结构式", "CH₃CH₂CH₂CH₃", "按连接顺序写出各基团", GREEN, GREEN_F),
        ("Skeletal｜骨架式", "(zig-zag line)", "只画碳骨架，顶点=碳，氢省略", PURPLE, PURPLE_F),
    ]
    for t, val, cn, col, fl in rows:
        h = 78
        b.append(rect(40, y, W - 80, h, fl, col, 1.3, 10))
        b.append(text(58, y + 28, t, 13, col, "700"))
        b.append(text(58, y + 56, val, 14, INK, "600"))
        b.append(text(320, y + 28, cn, 11.5, MUTED))
        # mini drawing on the right for skeletal row
        if "Skeletal" in t:
            pts = [(500, y + 56), (535, y + 30), (570, y + 56), (605, y + 30), (640, y + 56)]
            for i in range(len(pts) - 1):
                b.append(line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], INK, 2))
            for px, py in pts:
                b.append(circle(px, py, 3, INK, INK, 1))
        elif "Condensed" in t:
            b.append(text(520, y + 56, "CH₃-CH₂-CH₂-CH₃", 12.5, INK, "500"))
        else:
            b.append(text(560, y + 56, "C=4  H=10", 12.5, INK, "500"))
        y += h + 12

    b.append(rect(40, y, W - 80, 60, RED_F, RED, 1.2, 8))
    b.append(text(58, y + 24, "⚠ Molecular formula alone is NOT enough to identify a compound.", 12.5, RED, "600"))
    b.append(text(58, y + 44, "只看分子式认不出物质——C₄H₁₀ 有两种不同的结构（见后页异构体）。", 11.5, MUTED))
    y += 76
    return svg(W, y, "".join(b))


def build_iupac_steps():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "IUPAC Naming in Four Steps｜IUPAC 命名四步", 15, INK, "600", "middle"))
    y = 50

    steps = [
        ("Step 1", "Find the LONGEST carbon chain.", "找**最长**的碳链作主链（不是「最直」的那条）。",
         "→ butane (4 C)", BLUE, BLUE_F),
        ("Step 2", "Number the chain so substituents get the LOWEST numbers.", "编号方向要让**取代基位次最小**。",
         "→ 2-methyl, not 3-methyl", GREEN, GREEN_F),
        ("Step 3", "Name each substituent as an alkyl group (methyl, ethyl…).", "把每个取代基写成烷基名（甲基、乙基…）。",
         "→ methyl group", AMBER, AMBER_F),
        ("Step 4", "Assemble: substituent position + name + parent + family suffix.", "拼装：取代基位次 + 名称 + 主链 + 家族后缀。",
         "→ 2-methylbutane", PURPLE, PURPLE_F),
    ]
    for tag, en, cn, res, col, fl in steps:
        h = 74
        b.append(rect(40, y, W - 80, h, fl, col, 1.3, 10))
        b.append(text(58, y + 26, tag, 12, col, "700"))
        b.append(text(122, y + 26, en, 12.5, INK, "600"))
        b.append(text(122, y + 50, cn, 11.5, MUTED))
        b.append(text(W - 58, y + 40, res, 12, col, "700", "end"))
        y += h + 10

    b.append(rect(40, y + 6, W - 80, 58, BLUE_F, BLUE, 1.2, 8))
    b.append(text(58, y + 30, "💡 Prefixes 1–10｜前缀：meth eth prop but pent hex hept oct non dec", 12, BLUE, "600"))
    b.append(text(58, y + 50, "多个相同取代基用 di- / tri- / tetra-（2,3-dimethylbutane）。", 11.5, MUTED))
    y += 78
    return svg(W, y, "".join(b))


def build_isomers():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Structural Isomers｜结构异构体", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Same molecular formula, different connectivity — so different properties.", 12.5, MUTED))
    y += 20
    b.append(text(40, y, "分子式相同、连接方式不同——因此性质也不同（沸点、熔点、反应性都会有差异）。", 11.5, MUTED))
    y += 28

    # C4H10: 2 isomers
    b.append(rect(40, y, W - 80, 118, BLUE_F, BLUE, 1.3, 10))
    b.append(text(58, y + 26, "C₄H₁₀  →  TWO isomers｜两种", 13, BLUE, "700"))
    b.append(text(58, y + 50, "butane｜正丁烷", 12, INK, "600"))
    b.append(text(58, y + 72, "CH₃CH₂CH₂CH₃", 12.5, INK, "500"))
    b.append(text(58, y + 94, "bp −0.5 °C", 11.5, MUTED))
    b.append(text(370, y + 50, "2-methylpropane (isobutane)｜异丁烷", 12, INK, "600"))
    b.append(text(370, y + 72, "CH₃CH(CH₃)CH₃", 12.5, INK, "500"))
    b.append(text(370, y + 94, "bp −11.7 °C", 11.5, MUTED))
    y += 130

    # C5H12: 3 isomers
    b.append(rect(40, y, W - 80, 128, GREEN_F, GREEN, 1.3, 10))
    b.append(text(58, y + 26, "C₅H₁₂  →  THREE isomers｜三种", 13, GREEN, "700"))
    names = [
        ("pentane｜正戊烷", "CH₃CH₂CH₂CH₂CH₃", "bp 36 °C"),
        ("2-methylbutane｜异戊烷", "CH₃CH(CH₃)CH₂CH₃", "bp 28 °C"),
        ("2,2-dimethylpropane｜新戊烷", "C(CH₃)₄", "bp 10 °C"),
    ]
    for i, (nm, fm, bp) in enumerate(names):
        x = 58 + i * 200
        b.append(text(x, y + 56, nm, 11.5, INK, "600"))
        b.append(text(x, y + 78, fm, 12, INK, "500"))
        b.append(text(x, y + 100, bp, 11, MUTED))
    y += 144

    b.append(rect(40, y, W - 80, 58, AMBER_F, AMBER, 1.2, 8))
    b.append(text(58, y + 24, "📏 As branching increases, boiling point DECREASES.", 12.5, AMBER, "600"))
    b.append(text(58, y + 44, "支链越多，分子越「圆」、接触面越小 → 色散力越弱 → 沸点越低（预埋 Ch.7）。", 11.5, MUTED))
    y += 74
    return svg(W, y, "".join(b))


def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "ch02-carbon-four-bonds.svg": build_carbon_four_bonds(),
        "ch02-three-formulas.svg": build_three_formulas(),
        "ch02-iupac-four-steps.svg": build_iupac_steps(),
        "ch02-isomers-c4c5.svg": build_isomers(),
    }
    for name, data in figs.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(data)
        print(f"wrote {name}  ({len(data)} bytes)")


if __name__ == "__main__":
    main()
