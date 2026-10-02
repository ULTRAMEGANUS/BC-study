# -*- coding: utf-8 -*-
"""
G11 Ch.4 figure builder — applications of organic chemistry.
Canvas height computed from content (never hard-coded).

Figures:
  ch04-combustion-two-paths.svg    Complete vs incomplete combustion
  ch04-monomer-polymer.svg         Monomer -> polymer, and the recycling codes
  ch04-evaluation-axes.svg         Health / society / environment trade-off frame
  ch04-green-chemistry.svg         Green chemistry: prevention first
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
def build_combustion():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Complete vs Incomplete Combustion｜完全燃烧与不完全燃烧", 14.5, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Same fuel, different oxygen supply — and very different products.",
                  12, MUTED))
    y += 17
    b.append(text(40, y, "同样的燃料，供氧不同，产物与危险程度完全不同。这是本章最重要的一条安全线。",
                  11.5, MUTED))
    y += 24

    colw = (W - 80 - 18) / 2

    # LEFT: complete
    b.append(rect(40, y, colw, 196, BLUE_F, BLUE, 1.3, 10))
    b.append(text(58, y + 26, "COMPLETE｜完全燃烧", 12.5, BLUE, "700"))
    b.append(text(58, y + 48, "Oxygen plentiful｜氧气充足", 11, INK, "600"))
    b.append(text(58, y + 74, "fuel + O₂  →  CO₂ + H₂O", 11.5, INK, "700"))
    b.append(text(58, y + 100, "Products｜产物：", 10.5, MUTED, "700"))
    b.append(text(58, y + 118, "CO₂  carbon dioxide｜二氧化碳", 10.5, MUTED))
    b.append(text(58, y + 134, "H₂O  water｜水", 10.5, MUTED))
    b.append(text(58, y + 156, "Flame｜火焰：blue, clean", 10.5, GREEN))
    b.append(text(58, y + 172, "蓝色、洁净、几乎无烟", 10.5, MUTED))
    b.append(text(58, y + 188, "Energy released is MAXIMUM｜放热最多", 10.5, GREEN, "600"))

    # RIGHT: incomplete
    x2 = 40 + colw + 18
    b.append(rect(x2, y, colw, 196, RED_F, RED, 1.3, 10))
    b.append(text(x2 + 18, y + 26, "INCOMPLETE｜不完全燃烧", 12.5, RED, "700"))
    b.append(text(x2 + 18, y + 48, "Oxygen limited｜氧气不足", 11, INK, "600"))
    b.append(text(x2 + 18, y + 74, "fuel + O₂  →  CO  or  C  +  H₂O", 10.5, INK, "700"))
    b.append(text(x2 + 18, y + 100, "Products｜产物：", 10.5, MUTED, "700"))
    b.append(text(x2 + 18, y + 118, "CO  carbon monoxide｜一氧化碳", 10.5, MUTED))
    b.append(text(x2 + 18, y + 134, "C  soot｜碳烟", 10.5, MUTED))
    b.append(text(x2 + 18, y + 156, "Flame｜火焰：yellow, sooty", 10.5, RED))
    b.append(text(x2 + 18, y + 172, "黄色、冒黑烟、有积碳", 10.5, MUTED))
    b.append(text(x2 + 18, y + 188, "Less energy AND toxic gas｜放热少且有毒气", 10.5, RED, "600"))
    y += 212

    b.append(rect(40, y, W - 80, 76, AMBER_F, AMBER, 1.2, 8))
    b.append(text(58, y + 24, "⚠ Carbon monoxide: colourless, odourless, binds haemoglobin ~200× stronger than O₂.",
                  11, AMBER, "600"))
    b.append(text(58, y + 44, "CO 无色无味，与血红蛋白结合能力约为氧的 200 倍——这就是车库/热水器/炭火取暖",
                  10.5, MUTED))
    b.append(text(58, y + 62, "事故的化学原因。通风不良 + 密闭空间 = 高危。", 10.5, MUTED))
    y += 92
    return svg(W, y, "".join(b))


# --------------------------------------------------------------------------
def build_monomer_polymer():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Monomer → Polymer｜单体 → 聚合物", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "A monomer is one small building unit; a polymer is many of them joined into a chain.",
                  12, MUTED))
    y += 17
    b.append(text(40, y, "单体是小单元，聚合物是成千上万个单体连成的长链——链越长，塑料越强韧。",
                  11.5, MUTED))
    y += 26

    # ethene -> polyethene schematic
    b.append(rect(40, y, W - 80, 128, BLUE_F, BLUE, 1.3, 10))
    b.append(text(58, y + 26, "ethene｜乙烯  →  polyethene (PE)｜聚乙烯", 12.5, BLUE, "700"))
    b.append(text(58, y + 50, "CH₂=CH₂", 12, INK, "700"))
    b.append(text(140, y + 50, "+", 13, MUTED, "700"))
    b.append(text(160, y + 50, "CH₂=CH₂", 12, INK, "700"))
    b.append(text(250, y + 50, "+", 13, MUTED, "700"))
    b.append(text(270, y + 50, "CH₂=CH₂", 12, INK, "700"))
    b.append(text(360, y + 50, "…", 13, MUTED, "700"))
    b.append(text(58, y + 76, "↓  the C=C opens, each carbon links to the next ｜C=C 打开，逐个相连", 10.5, MUTED))
    b.append(text(58, y + 100, "—CH₂—CH₂—CH₂—CH₂—CH₂—CH₂—CH₂—CH₂—   (a very long chain)", 10.5, INK, "600"))
    b.append(text(58, y + 120, "n 个单体重复 → 一条链；n 可以到几万。", 10.5, MUTED))
    y += 144

    # recycling codes table
    b.append(rect(40, y, W - 80, 26, HEAD, "#CBD2D9", 1.0, 6))
    for t, x in zip(("Code｜编号", "Polymer｜聚合物", "Made from｜单体", "Typical use｜常见用途"),
                    (50, 150, 300, 460)):
        b.append(text(x, y + 18, t, 11, MUTED, "700"))
    y += 26
    codes = [
        ("1 PET", "polyethene terephthalate", "饮料瓶、涤纶纤维"),
        ("2 HDPE", "high-density polyethene", "牛奶桶、洗涤剂瓶"),
        ("3 PVC", "polyvinyl chloride", "管道、电缆绝缘"),
        ("4 LDPE", "low-density polyethene", "保鲜膜、塑料袋"),
        ("5 PP", "polypropene", "餐盒、绳、汽车部件"),
        ("6 PS", "polystyrene", "泡沫塑料、杯"),
    ]
    for i, (code, poly, use) in enumerate(codes):
        b.append(rect(40, y, W - 80, 26, BLUE_F if i % 2 == 0 else BG, "#E1E7EC", 0.8, 4))
        b.append(text(50, y + 18, code, 11, BLUE, "700"))
        b.append(text(150, y + 18, poly, 10.5, INK))
        b.append(text(460, y + 18, use, 10.5, MUTED))
        y += 26
    y += 16

    b.append(rect(40, y, W - 80, 58, GREEN_F, GREEN, 1.2, 8))
    b.append(text(58, y + 24, "📏 A polymer's properties come from chain length, branching and the forces BETWEEN chains.",
                  11, GREEN, "600"))
    b.append(text(58, y + 44, "链间作用力（Ch.7 的分子间力）决定熔点、硬度与可回收性——不是靠分子内共价键。",
                  10.5, MUTED))
    y += 74
    return svg(W, y, "".join(b))


# --------------------------------------------------------------------------
def build_evaluation_axes():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Evaluating an Application｜应用的三维评价", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Big Idea B2 says \"evaluate\" — so you must look at BOTH benefits and risks.",
                  12, MUTED))
    y += 17
    b.append(text(40, y, "B2 的关键动词是 evaluate（评价）——只讲好处或只讲坏处都不及格。必须两面都讲。",
                  11.5, MUTED))
    y += 26

    cols = [
        ("HEALTH｜健康", "medicine, food, clean water", "toxicity, air quality, exposure",
         "药物、食品、净水", "毒性、空气质量、暴露", GREEN, GREEN_F),
        ("SOCIETY｜社会", "jobs, fuel, housing, transport", "cost, equity, dependence",
         "就业、燃料、住房、交通", "成本、公平、依赖", BLUE, BLUE_F),
        ("ENVIRONMENT｜环境", "renewable materials, green synthesis", "emissions, plastics, land use",
         "可再生材料、绿色合成", "排放、塑料、土地利用", AMBER, AMBER_F),
    ]
    cw = (W - 80 - 2 * 14) / 3
    for i, (t, ben, risk, cnb, cnr, col, fl) in enumerate(cols):
        x = 40 + i * (cw + 14)
        b.append(rect(x, y, cw, 168, fl, col, 1.3, 10))
        b.append(text(x + cw / 2, y + 26, t, 11.5, col, "700", "middle"))
        b.append(text(x + 14, y + 52, "＋ Benefit｜收益", 10.5, GREEN, "700"))
        b.append(text(x + 14, y + 70, ben, 10, INK))
        b.append(text(x + 14, y + 86, cnb, 10, MUTED))
        b.append(text(x + 14, y + 112, "− Risk｜风险", 10.5, RED, "700"))
        b.append(text(x + 14, y + 130, risk, 10, INK))
        b.append(text(x + 14, y + 146, cnr, 10, MUTED))
    y += 184

    b.append(rect(40, y, W - 80, 122, PURPLE_F, PURPLE, 1.2, 8))
    b.append(text(58, y + 24, "Trade-off table｜权衡表（评价题的答题骨架）", 12, PURPLE, "700"))
    hdr = [("Question｜问题", 58, 240), ("What to write｜写什么", 320, 340)]
    for t, x, _ in hdr:
        b.append(text(x, y + 46, t, 10.5, MUTED, "700"))
    rows = [
        "1  What is it used for?｜它用来做什么？",
        "2  Who benefits, and how?｜谁受益、怎么受益？",
        "3  What is the harm, and to whom?｜害处是什么、害谁？",
        "4  Is there a safer substitute?｜有没有更安全的替代？",
    ]
    for i, s in enumerate(rows):
        b.append(text(58, y + 66 + i * 14, s, 10, INK))
    b.append(text(320, y + 66, "state the use, then the mechanism", 10, MUTED))
    b.append(text(320, y + 80, "be specific: name the group", 10, MUTED))
    b.append(text(320, y + 94, "say whether it is short- or long-term", 10, MUTED))
    b.append(text(320, y + 108, "end with a reasoned verdict", 10, MUTED))
    y += 138
    return svg(W, y, "".join(b))


# --------------------------------------------------------------------------
def build_green_chemistry():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Green Chemistry: Prevention First｜绿色化学：源头预防优先", 14.5, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Green chemistry is a DESIGN approach — it starts long before the waste exists.",
                  12, MUTED))
    y += 17
    b.append(text(40, y, "绿色化学是一种「设计」思路：在废物产生之前就把它消灭掉，而不是产生后再处理。",
                  11.5, MUTED))
    y += 26

    # hierarchy arrow: prevent > reuse > treat > dispose
    b.append(text(40, y, "The waste hierarchy｜废物处理优先级（越靠上越好）", 12, INK, "700"))
    y += 18
    steps = [
        ("PREVENT｜预防", "design it out｜从设计上消除", GREEN, GREEN_F, 330),
        ("REUSE / RECYCLE｜回用", "loop the material back｜让材料回流", BLUE, BLUE_F, 270),
        ("TREAT｜处理", "neutralise before release｜排放前处理", AMBER, AMBER_F, 210),
        ("DISPOSE｜处置", "last resort｜最后手段", RED, RED_F, 150),
    ]
    for t, cn, col, fl, w in steps:
        b.append(rect(40, y, w, 34, fl, col, 1.2, 6))
        b.append(text(56, y + 15, t, 11, col, "700"))
        b.append(text(56, y + 29, cn, 10, MUTED))
        y += 42
    y += 6

    b.append(rect(40, y, W - 80, 26, HEAD, "#CBD2D9", 1.0, 6))
    for t, x in zip(("Principle｜原则", "What it means in practice｜实际含义"), (50, 300)):
        b.append(text(x, y + 18, t, 11, MUTED, "700"))
    y += 26
    prin = [
        ("Prevent waste｜预防废物", "design the process so no waste forms"),
        ("Atom economy｜原子经济", "most reactant atoms end up in the product"),
        ("Safer solvents｜安全溶剂", "avoid toxic or volatile solvents"),
        ("Renewable feedstocks｜可再生原料", "start from plants, not petroleum"),
        ("Catalysis｜催化", "lower energy demand per unit product"),
        ("Design for degradation｜可降解设计", "the product breaks down after use"),
    ]
    for i, (p, m) in enumerate(prin):
        b.append(rect(40, y, W - 80, 26, GREEN_F if i % 2 == 0 else BG, "#E1E7EC", 0.8, 4))
        b.append(text(50, y + 18, p, 10.5, GREEN, "700"))
        b.append(text(300, y + 18, m, 10.5, INK))
        y += 26
    y += 16

    b.append(rect(40, y, W - 80, 58, RED_F, RED, 1.2, 8))
    b.append(text(58, y + 24, "⚠ \"Green\" is not the same as \"recyclable\". Prevention beats recycling.",
                  11, RED, "600"))
    b.append(text(58, y + 44, "回收只是第二选择；能在源头不产生废物，才是绿色化学的第一原则。", 10.5, MUTED))
    y += 74
    return svg(W, y, "".join(b))


def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "ch04-combustion-two-paths.svg": build_combustion(),
        "ch04-monomer-polymer.svg": build_monomer_polymer(),
        "ch04-evaluation-axes.svg": build_evaluation_axes(),
        "ch04-green-chemistry.svg": build_green_chemistry(),
    }
    for name, data in figs.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(data)
        print(f"wrote {name}  ({len(data)} bytes)")


if __name__ == "__main__":
    main()
