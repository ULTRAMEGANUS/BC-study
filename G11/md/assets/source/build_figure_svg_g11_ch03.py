# -*- coding: utf-8 -*-
"""
G11 Ch.3 figure builder — functional groups: the organic vocabulary.
Canvas height computed from content (never hard-coded).

Figures:
  ch03-nine-functional-groups.svg  Nine families, structure + naming + example
  ch03-naming-priority.svg         Suffix vs prefix; the lowest-locant rule
  ch03-ester-bilingual.svg         Ester naming: English and Chinese REVERSE
  ch03-boiling-ladder.svg          Boiling point across families, same carbon count
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


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_nine_groups():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Nine Functional Groups｜九大官能团", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "A functional group is the atom cluster that names the family and sets its properties.",
                  12, MUTED))
    y += 17
    b.append(text(40, y, "官能团既决定「叫什么」（后缀/前缀），也决定「什么性质」（极性、氢键、沸点）。",
                  11.5, MUTED))
    y += 24

    CX = [50, 196, 300, 420]
    b.append(rect(40, y, W - 80, 26, HEAD, "#CBD2D9", 1.0, 6))
    for t, x in zip(("Family｜类别", "Structure｜结构", "Naming｜名尾", "Example｜例"), CX):
        b.append(text(x, y + 18, t, 11.5, MUTED, "700"))
    y += 26

    rows = [
        ("卤代 halogen", "R–X", "chloro- bromo- (prefix)", "chloroethane 氯乙烷", BLUE, BLUE_F),
        ("醇 alcohol", "R–OH", "-anol (suffix)", "ethanol 乙醇", GREEN, GREEN_F),
        ("醚 ether", "R–O–R′", "alkoxy- (prefix)", "methoxyethane 甲氧基乙烷", BLUE, BLUE_F),
        ("醛 aldehyde", "R–CHO", "-anal (suffix)", "ethanal 乙醛", AMBER, AMBER_F),
        ("酮 ketone", "R–CO–R′", "-anone (suffix)", "propanone 丙酮", AMBER, AMBER_F),
        ("羧酸 acid", "R–COOH", "-anoic acid (suffix)", "ethanoic acid 乙酸", RED, RED_F),
        ("酯 ester", "R–COO–R′", "alkyl alkanoate", "methyl ethanoate 乙酸甲酯", PURPLE, PURPLE_F),
        ("胺 amine", "R–NH₂", "-anamine (suffix)", "ethanamine 乙胺", GREEN, GREEN_F),
        ("酰胺 amide", "R–CONH₂", "-anamide (suffix)", "ethanamide 乙酰胺", GREEN, GREEN_F),
    ]
    rh = 28
    for i, (fam, st, nm, ex, col, fl) in enumerate(rows):
        b.append(rect(40, y, W - 80, rh, fl if i % 2 == 0 else BG, "#E1E7EC", 0.8, 4))
        b.append(text(CX[0], y + 19, fam, 11, col, "700"))
        b.append(text(CX[1], y + 19, st, 11.5, INK, "600"))
        b.append(text(CX[2], y + 19, nm, 10.5, MUTED))
        b.append(text(CX[3], y + 19, ex, 10.5, INK))
        y += rh
    y += 16

    b.append(rect(40, y, W - 80, 62, AMBER_F, AMBER, 1.2, 8))
    b.append(text(58, y + 24, "💡 R = any carbon chain｜R 代表任意碳链；R′ = a second, possibly different chain",
                  11.5, AMBER, "600"))
    b.append(text(58, y + 44, "记住这条分水岭：拿到名尾定家族，拿到前缀只是「挂件」。", 11.5, MUTED))
    y += 78
    return svg(W, y, "".join(b))


# --------------------------------------------------------------------------
def build_naming_priority():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Naming Priority｜命名优先级", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Rule 1 — the parent chain must CONTAIN the functional group.", 12.5, MUTED))
    y += 17
    b.append(text(40, y, "规则一：主链必须「包含」官能团——不是单纯的「最长链」。", 11.5, MUTED))
    y += 17
    b.append(text(40, y, "Rule 2 — number so the functional group gets the LOWEST locant.", 12.5, MUTED))
    y += 17
    b.append(text(40, y, "规则二：编号要让官能团位次「最小」——它比取代基优先。", 11.5, MUTED))
    y += 26

    # two columns: suffix groups vs prefix groups
    colw = (W - 80 - 18) / 2
    b.append(rect(40, y, colw, 150, GREEN_F, GREEN, 1.3, 10))
    b.append(text(58, y + 26, "SUFFIX groups｜用后缀（吃编号）", 12, GREEN, "700"))
    for i, s in enumerate(("-anol  alcohol 醇", "-anal  aldehyde 醛", "-anone  ketone 酮",
                           "-anoic acid  羧酸", "-anamine  amine 胺", "-anamide  amide 酰胺")):
        b.append(text(58, y + 52 + i * 17, s, 11, INK))

    x2 = 40 + colw + 18
    b.append(rect(x2, y, colw, 150, BLUE_F, BLUE, 1.3, 10))
    b.append(text(x2 + 18, y + 26, "PREFIX groups｜用前缀（不吃编号）", 12, BLUE, "700"))
    for i, s in enumerate(("-chloro-  卤代", "-bromo-   卤代", "-methoxy-  醚", "R–O–R′  醚（无编号）")):
        b.append(text(x2 + 18, y + 52 + i * 17, s, 11, INK))
    b.append(text(x2 + 18, y + 130, "只有这两族降级为前缀。", 10.5, MUTED))
    y += 166

    b.append(rect(40, y, W - 80, 104, PURPLE_F, PURPLE, 1.3, 10))
    b.append(text(58, y + 26, "Worked example｜实例：CH₃—CH(OH)—CH₃", 12.5, PURPLE, "700"))
    b.append(text(58, y + 50, "✗ propan-1-ol  ← numbering from the wrong end", 11.5, RED))
    b.append(text(58, y + 72, "✓ propan-2-ol  ← –OH sits at C2, the lowest possible locant", 11.5, GREEN))
    b.append(text(58, y + 94, "–OH 在 2 位；从右端编号得到 2，从左端得到 3——取 2。", 11, MUTED))
    y += 120

    b.append(rect(40, y, W - 80, 58, RED_F, RED, 1.2, 8))
    b.append(text(58, y + 24, "⚠ The suffix position number CANNOT be omitted for C₃ and above.", 12, RED, "600"))
    b.append(text(58, y + 44, "3 个碳起，官能团位次必须写出来：ethANOL 只有一个位置所以可省，但 propan-2-ol 的「2」不能省。",
                  10.5, MUTED))
    y += 74
    return svg(W, y, "".join(b))


# --------------------------------------------------------------------------
def build_ester_bilingual():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Ester Naming: Two Languages, Two Orders｜酯的英中语序陷阱", 14.5, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "This is the ONE place in organic chemistry where English and Chinese run in opposite directions.",
                  12, MUTED))
    y += 17
    b.append(text(40, y, "这是有机化学里唯一一处英中语序「相反」的地方——其余官能团都是同向的。",
                  11.5, MUTED))
    y += 26

    rows = [
        ("English order｜英文语序", "ALCOHOL part  +  ACID part", "→  methyl ethanoate", BLUE, BLUE_F),
        ("Chinese order｜中文语序", "ACID part  +  ALCOHOL part", "→  乙酸甲酯", RED, RED_F),
    ]
    for t, seq, res, col, fl in rows:
        b.append(rect(40, y, W - 80, 60, fl, col, 1.3, 10))
        b.append(text(58, y + 26, t, 12, col, "700"))
        b.append(text(58, y + 48, seq, 12, INK, "600"))
        b.append(text(W - 58, y + 40, res, 12.5, col, "700", "end"))
        y += 72

    b.append(rect(40, y, W - 80, 158, PURPLE_F, PURPLE, 1.3, 10))
    b.append(text(58, y + 26, "Decoding｜逐词拆解", 12.5, PURPLE, "700"))
    pairs = [
        ("methyl ethanoate", "methyl = 甲（醇部分）", "ethanoate = 乙酸（酸部分）", "乙酸甲酯"),
        ("ethyl methanoate", "ethyl = 乙（醇部分）", "methanoate = 甲酸（酸部分）", "甲酸乙酯"),
    ]
    yy = y + 50
    for name, a, bb, cn in pairs:
        b.append(text(58, yy, name, 12, INK, "700"))
        b.append(text(230, yy, a, 10.5, MUTED))
        b.append(text(400, yy, bb, 10.5, MUTED))
        b.append(text(W - 58, yy, cn, 12, PURPLE, "700", "end"))
        yy += 34
        if name.startswith("methyl"):
            b.append(line(58, yy - 22, W - 58, yy - 22, "#D6BCFA", 1.0, "3,3"))
    b.append(text(58, yy + 6, "换成中文：把两部分**颠倒**过来念——acid first, then alcohol.", 11, MUTED))
    y += 174

    b.append(rect(40, y, W - 80, 76, AMBER_F, AMBER, 1.2, 8))
    b.append(text(58, y + 24, "🔭 Extension｜超纲【Extension → Chemistry 12】", 11.5, AMBER, "700"))
    b.append(text(58, y + 44, "Esters form from an acid + an alcohol (esterification). The REACTION belongs to Chemistry 12 —",
                  11, MUTED))
    b.append(text(58, y + 62, "this chapter only names and recognises them.  本章只做命名与识别，不写酯化反应式。",
                  11, MUTED))
    y += 92
    return svg(W, y, "".join(b))


# --------------------------------------------------------------------------
def build_boiling_ladder():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Boiling Point Across Families｜同碳数沸点阶梯", 15, INK, "600", "middle"))
    y = 46
    b.append(text(40, y, "All five compounds below have TWO carbons. Only the functional group changes.",
                  12, MUTED))
    y += 17
    b.append(text(40, y, "下面五种化合物都只有 2 个碳——唯一变量是官能团。沸点差异全部来自分子间作用力。",
                  11.5, MUTED))
    y += 26

    data = [
        ("ethane｜乙烷", "CH₃CH₃", -89, "dispersion only｜只有色散力", BLUE, BLUE_F),
        ("methoxymethane｜甲氧基甲烷", "CH₃OCH₃", -25, "weak dipole｜弱偶极", BLUE, BLUE_F),
        ("ethanal｜乙醛", "CH₃CHO", 20, "strong dipole｜强偶极", AMBER, AMBER_F),
        ("ethanol｜乙醇", "CH₃CH₂OH", 78, "hydrogen bonding｜氢键", GREEN, GREEN_F),
        ("ethanoic acid｜乙酸", "CH₃COOH", 118, "H-bond dimers｜氢键二聚体", RED, RED_F),
    ]
    # scale: -89 .. 118  ->  bar length 40 .. 400
    lo, hi = -100, 130
    bx = 250
    maxw = 330
    for nm, fm, bp, why, col, fl in data:
        b.append(rect(40, y, W - 80, 44, fl, col, 1.0, 6))
        b.append(text(56, y + 20, nm, 11, col, "700"))
        b.append(text(56, y + 36, fm, 10.5, MUTED))
        w = maxw * (bp - lo) / (hi - lo)
        b.append(rect(bx, y + 10, w, 14, col, col, 0, 3))
        b.append(text(bx + w + 8, y + 21, f"{bp} °C", 11, col, "700"))
        b.append(text(bx, y + 38, why, 10, MUTED))
        y += 52
    y += 6

    b.append(rect(40, y, W - 80, 78, PURPLE_F, PURPLE, 1.2, 8))
    b.append(text(58, y + 24, "📏 Same carbons, rising boiling point: alkane < ether < aldehyde ≈ ketone < alcohol < acid",
                  11.5, PURPLE, "700"))
    b.append(text(58, y + 46, "分子间作用力越强，越难把分子拉开 → 沸点越高。氢键（O–H）是这里的转折点：",
                  11, MUTED))
    b.append(text(58, y + 64, "从乙醛到乙醇，多了 O–H，沸点从 20 °C 跳到 78 °C。", 11, MUTED))
    y += 94
    return svg(W, y, "".join(b))


def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "ch03-nine-functional-groups.svg": build_nine_groups(),
        "ch03-naming-priority.svg": build_naming_priority(),
        "ch03-ester-bilingual.svg": build_ester_bilingual(),
        "ch03-boiling-ladder.svg": build_boiling_ladder(),
    }
    for name, data in figs.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(data)
        print(f"wrote {name}  ({len(data)} bytes)")


if __name__ == "__main__":
    main()
