# -*- coding: utf-8 -*-
"""
G11 Ch.14 figure builder — analysis techniques & course synthesis.
Canvas height computed from content (never hard-coded).

Figures:
  ch14-qual-vs-quant.svg   Qualitative vs quantitative analysis
  ch14-ion-id-tree.svg     Ion identification flow (flame + precipitation)
  ch14-course-map.svg      The whole course in one map (five Big Ideas)
  ch14-technique-match.svg Matching techniques to real questions
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
def build_qual_quant():
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Qualitative vs Quantitative｜定性与定量", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "First ask: WHAT is it? Then ask: HOW MUCH is there?", 11.5, MUTED, "400", "middle"))
    y += 20

    # left card
    b.append(rect(45, y, 285, 210, BLUE_F, BLUE, 1.4, 8))
    b.append(text(187, y + 26, "Qualitative 定性", 13.5, BLUE, "700", "middle"))
    b.append(text(187, y + 46, "answers “what is present?”", 10.5, MUTED, "400", "middle"))
    items = [
        "flame test 焰色试验",
        "precipitation tests 沉淀检验",
        "indicator colour 指示剂判酸碱",
        "litmus / pH paper 定性酸碱",
    ]
    for i, s in enumerate(items):
        b.append(text(65, y + 74 + i * 24, "•  " + s, 11, INK))
    y += 210 + 14

    # right card
    y2 = y - 224
    b.append(rect(350, y2, 285, 210, GREEN_F, GREEN, 1.4, 8))
    b.append(text(492, y2 + 26, "Quantitative 定量", 13.5, GREEN, "700", "middle"))
    b.append(text(492, y2 + 46, "answers “how much is there?”", 10.5, MUTED, "400", "middle"))
    items2 = [
        "titration 滴定（浓度）",
        "gravimetric analysis 重量分析",
        "mass & volume measurements 称量量体积",
        "uncertainty & parallel trials 不确定度",
    ]
    for i, s in enumerate(items2):
        b.append(text(370, y2 + 74 + i * 24, "•  " + s, 11, INK))

    y += 14
    b.append(rect(45, y, 590, 58, HEAD, LINE, 1.2, 8))
    b.append(text(65, y + 23, "Good labs do both: identify first, then measure. 先鉴定、后定量。",
                  12, INK, "700"))
    b.append(text(65, y + 43, "Gravimetric: dissolve → precipitate → filter → dry to constant mass → weigh.",
                  10.5, MUTED))
    return svg(W, y + 80, "".join(b))


# --------------------------------------------------------------------------
def build_ion_tree():
    """Ion identification flow."""
    W = 680
    b = [arrow_defs()]
    y = 32
    b.append(text(340, y, "Identifying an Unknown Solution｜未知溶液鉴定流程", 17, INK, "700", "middle"))
    y += 20

    b.append(rect(240, y, 200, 40, HEAD, LINE, 1.3, 8))
    b.append(text(340, y + 25, "unknown solution 未知液", 11.5, INK, "700", "middle"))
    y += 40

    y1 = y + 20
    b.append(arrow1(300, y, 170, y1))
    b.append(arrow1(380, y, 510, y1))
    b.append(text(200, y + 14, "clean wire loop", 9.5, MUTED))
    b.append(text(430, y + 14, "add a few drops of test reagent", 9.5, MUTED))

    # left: flame tests
    b.append(rect(60, y1, 220, 46, AMBER_F, AMBER, 1.3, 8))
    b.append(text(170, y1 + 20, "Flame test 焰色试验", 12, AMBER, "700", "middle"))
    b.append(text(170, y1 + 37, "(Ch.5 electron jumps)", 9.5, MUTED, "400", "middle"))
    flames = [("Na⁺", "yellow 黄"), ("K⁺", "lilac 紫"), ("Ca²⁺", "orange-red 橙红"), ("Cu²⁺", "green 绿")]
    fy = y1 + 56
    for ion, c in flames:
        b.append(text(110, fy + 4, ion, 11, INK, "700"))
        b.append(text(170, fy + 4, c, 10.5, AMBER))
        fy += 22

    # right: precipitation
    b.append(rect(400, y1, 220, 46, BLUE_F, BLUE, 1.3, 8))
    b.append(text(510, y1 + 20, "Precipitation tests 沉淀检验", 12, BLUE, "700", "middle"))
    b.append(text(510, y1 + 37, "(Ch.12 solubility rules)", 9.5, MUTED, "400", "middle"))
    tests = [("add Cl⁻(aq)", "ppt → Ag⁺ or Pb²⁺"), ("add SO₄²⁻(aq)", "ppt → Ba²⁺ or Pb²⁺"),
             ("add OH⁻(aq)", "ppt → many metal ions")]
    ty = y1 + 56
    for a, r in tests:
        b.append(text(415, ty + 4, a, 10.5, INK, "700"))
        b.append(text(520, ty + 4, r, 10, MUTED))
        ty += 22

    y = max(fy, ty) + 12
    b.append(rect(60, y, 560, 56, GREEN_F, GREEN, 1.2, 8))
    b.append(text(80, y + 23, "Combine with titration (Ch.13) for amounts → full analysis 完成定量",
                  11.5, GREEN, "700"))
    b.append(text(80, y + 43, "操作规范就是数据可信度：铂丝先洗净、火焰颜色对比钴玻璃看钾。", 10.5, INK))
    return svg(W, y + 78, "".join(b))


# --------------------------------------------------------------------------
def build_course_map():
    """The whole course in one flow map organized by the five Big Ideas."""
    W = 680
    b = [arrow_defs()]
    y = 32
    b.append(text(340, y, "The Whole Course in One Map｜全课程一张图", 17, INK, "700", "middle"))
    y += 24

    groups = [
        ("B1  Building blocks 构件", "Ch.5–7  atoms → periodic table → bonds & IMF", BLUE, BLUE_F),
        ("B3  Measuring 量度", "Ch.1 + Ch.8  sig figs · dimensional analysis · the mole", GREEN, GREEN_F),
        ("B4  Conservation 守恒", "Ch.9–11  reactions → stoichiometry → energy", AMBER, AMBER_F),
        ("B5  Solutions 溶解", "Ch.12–14  solubility → concentration → analysis", PURPLE, PURPLE_F),
        ("B2  Applications 应用", "Ch.2–4  organic chemistry → health · society · environment", RED, RED_F),
    ]
    for t, s, col, fl in groups:
        b.append(rect(60, y, 560, 54, fl, col, 1.3, 8))
        b.append(text(80, y + 22, t, 12.5, col, "700"))
        b.append(text(80, y + 42, s, 11, INK))
        y += 54 + 10

    y += 2
    b.append(arrow1(340, y, 340, y + 18))
    y += 22
    b.append(rect(140, y, 400, 48, HEAD, LINE, 1.3, 8))
    b.append(text(340, y + 21, "Atoms rearrange; matter & energy are conserved;", 11, INK, "700", "middle"))
    b.append(text(340, y + 37, "what dissolves depends on the nature of solute & solvent.", 11, INK, "700", "middle"))
    y += 48 + 18
    b.append(text(340, y + 4, "One storyline, five Big Ideas — nothing in the course is orphaned.",
                  10.5, MUTED, "400", "middle"))
    return svg(W, y + 26, "".join(b))


# --------------------------------------------------------------------------
def build_technique_match():
    """Scenario cards -> which technique?"""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Match the Technique to the Question｜给问题配技术", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "Exam favourite: given a scenario, choose the method and justify it.",
                  11, MUTED, "400", "middle"))
    y += 20

    rows = [
        ("Is this salt NaCl or KCl?", "flame test — K⁺ lilac vs Na⁺ yellow", BLUE, BLUE_F),
        ("Is this HCl 0.10 M or 0.12 M?", "titration against a standard base", GREEN, GREEN_F),
        ("How much Ag is in this alloy?", "gravimetric: dissolve, precipitate AgCl, weigh", AMBER, AMBER_F),
        ("Does this water contain Pb²⁺?", "precipitation test with Cl⁻, confirm with SO₄²⁻", PURPLE, PURPLE_F),
        ("Which painkiller dissolves faster?", "controlled dissolution + timed sampling", RED, RED_F),
        ("Is this fertilizer N-rich?", "quantitative test for NH₄⁺ content (titration)", "#C05621", "#FFFAF0"),
    ]
    rh = 52
    for q, a, col, fl in rows:
        b.append(rect(45, y, 590, rh - 6, fl, col, 1.3, 8))
        b.append(text(65, y + 21, q, 11.5, INK, "700"))
        b.append(text(65, y + 39, "→  " + a, 10.5, col, "700"))
        y += rh
    y += 6
    b.append(text(340, y + 4, "Justify with BOTH the property used and the evidence read. 性质+证据双说理。",
                  10.5, MUTED, "400", "middle"))
    return svg(W, y + 26, "".join(b))


# --------------------------------------------------------------------------
def main():
    figs = {
        "ch14-qual-vs-quant.svg": build_qual_quant,
        "ch14-ion-id-tree.svg": build_ion_tree,
        "ch14-course-map.svg": build_course_map,
        "ch14-technique-match.svg": build_technique_match,
    }
    for name, fn in figs.items():
        s = fn()
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)


if __name__ == "__main__":
    main()
