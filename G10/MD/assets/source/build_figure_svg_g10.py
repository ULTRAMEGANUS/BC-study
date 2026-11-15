# -*- coding: utf-8 -*-
"""
G10（BC Science 10 化学）章节示意图生成器。

风格与 G9 的 build_figure_svg*.py 完全一致：900 宽、白底、标题 19pt、
右上角小字注释、圆角 rx=8、蓝 / 橙 / 灰配色 —— 两册讲义视觉统一。

用法：
    python build_figure_svg_g10.py            # 全部生成
    python build_figure_svg_g10.py ch01       # 只生成文件名含 ch01 的图

输出目录：../figures/
改完必跑 check_svg_bounds.py：SVG 画布高度是脚本里手写的数字，
内容画超了会被浏览器 / PDF **静默裁掉**，不报错也看不见。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(HERE), "figures")

# ---------------------------------------------------------------- 样式常量
FONT = ("'Segoe UI','Microsoft YaHei','PingFang SC',"
        "'Noto Sans CJK SC',Arial,sans-serif")
INK = "#2C2C2A"      # 主文字
SUB = "#5F5E5A"      # 次要文字
LINE = "#888780"     # 连线 / 中性描边
EDGE = "#B4B2A9"     # 浅边框
BLUE, BLUE_D, BLUE_BG = "#185FA5", "#0C447C", "#E6F1FB"
ORANGE, ORANGE_D, ORANGE_BG = "#BA7517", "#854F0B", "#FAEEDA"
GREEN, GREEN_BG = "#3B6D11", "#EAF3DE"
RED = "#A32D2D"
NEUTRAL_BG = "#F1EFE8"


def head(w, h, title, note):
    """画布 + 标题栏。"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}"
     height="{h}" font-family="{FONT}">
  <title>{title}</title>
  <rect width="{w}" height="{h}" fill="#FFFFFF"/>
  <text x="30" y="32" font-size="19" font-weight="600" fill="{INK}">{title}</text>
  <text x="{w - 30}" y="32" font-size="10.5" fill="{SUB}"
        text-anchor="end">{note}</text>
"""


def box(x, y, w, h, fill, stroke, sw=0.9, rx=8):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def txt(x, y, s, size=12, fill=INK, weight="400", anchor="middle",
        baseline="central"):
    w = f' font-weight="{weight}"' if weight != "400" else ""
    return (f'  <text x="{x}" y="{y}" font-size="{size}"{w} fill="{fill}" '
            f'text-anchor="{anchor}" dominant-baseline="{baseline}">'
            f'{s}</text>\n')


def path(d, stroke=LINE, sw=1.5, marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <path d="{d}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}"{da}{m}/>\n')


ARROW_DEF = """  <defs>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"
            markerHeight="7" orient="auto-start-reverse">
      <path d="M2 1L9 5L2 9" fill="none" stroke="#888780"
            stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
"""


def circ(cx, cy, r, fill, stroke, sw=1.2):
    return (f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>\n')


def ln(x1, y1, x2, y2, stroke=EDGE, sw=1.0, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{sw}"{da}/>\n')


def wrap(inner):
    return inner + "</svg>\n"


# ================================================================ 图 1-1
def fig_ch01_periodic_charge_map():
    """周期表电荷图：8 个主族 + 过渡金属条带。"""
    w, H = 900, 314
    s = head(w, H, "Fig. 1-1　Periodic Table Charge Map｜周期表电荷图",
             "main groups: charge from group no.｜主族看族号定电荷")

    groups = [
        ("Group 1", "Na", "+1", "Alkali 碱金属", BLUE_D, BLUE, BLUE_BG),
        ("Group 2", "Mg", "+2", "Alkaline earth 碱土金属",
         BLUE_D, BLUE, BLUE_BG),
        ("Group 13", "Al", "+3", "Boron 硼族", BLUE_D, BLUE, BLUE_BG),
        ("Group 14", "C", "±4", "Carbon 碳族", SUB, EDGE, NEUTRAL_BG),
        ("Group 15", "N", "−3", "Nitrogen 氮族",
         ORANGE_D, ORANGE, ORANGE_BG),
        ("Group 16", "O", "−2", "Oxygen 氧族",
         ORANGE_D, ORANGE, ORANGE_BG),
        ("Group 17", "Cl", "−1", "Halogen 卤素",
         ORANGE_D, ORANGE, ORANGE_BG),
        ("Group 18", "Ne", "0", "Noble gas 稀有气体", SUB, EDGE, NEUTRAL_BG),
    ]

    y0, bh, pitch, bw, x0 = 62, 110, 109, 101, 18
    for i, (g, sym, chg, label, col, edge, bg) in enumerate(groups):
        x = x0 + i * pitch
        s += box(x, y0, bw, bh, bg, edge, 1.1)
        s += txt(x + bw / 2, y0 + 16, g, 9.5, SUB, "600")
        s += txt(x + bw / 2, y0 + 41, sym, 21, INK, "700")
        s += txt(x + bw / 2, y0 + 68, chg, 18, col, "700")
        s += txt(x + bw / 2, y0 + 97, label, 9.5, SUB)

    sy, sh = 186, 62
    s += box(18, sy, 864, sh, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, sy + 21, "Groups 3–12 · Transition Metals｜过渡金属",
             13, ORANGE_D, "700")
    s += txt(450, sy + 43,
             "Multivalent 多变价 — charge from Roman numerals or the name / formula of the compound"
             "（Fe²⁺ / Fe³⁺、Cu⁺ / Cu²⁺）", 10.5, SUB)

    ny, nh = 262, 42
    s += box(18, ny, 864, nh, "#FFFFFF", EDGE, 0.9)
    s += txt(450, ny + 15, "Same group → same charge ⇐ same number of valence electrons｜同族电荷相同 ⇐ 最外层电子数相同", 11.5, INK, "700")
    s += txt(450, ny + 32,
             "Where the whole unit starts: electron arrangement → ion charge → formula → equation｜全册起点", 10, SUB)
    return wrap(s)


# ================================================================ 图 1-2
def fig_ch01_diatomic_h7():
    """双原子分子 H-7 法则：7 个双原子 + P₄ / S₈ 特殊情形。"""
    w, H = 900, 312
    s = head(w, H, "Fig. 1-2　Diatomic Molecules: Rule of 7｜双原子分子 H-7 法则",
             "these 7 are always diatomic｜这 7 种必须双原子")

    items = [("H₂", "Hydrogen 氢", 1), ("N₂", "Nitrogen 氮", 7),
             ("O₂", "Oxygen 氧", 8), ("F₂", "Fluorine 氟", 9),
             ("Cl₂", "Chlorine 氯", 17), ("Br₂", "Bromine 溴", 35),
             ("I₂", "Iodine 碘", 53)]

    y0, bh, pitch, bw, x0 = 62, 84, 112, 104, 62
    for i, (sym, name, z) in enumerate(items):
        x = x0 + i * pitch
        s += box(x, y0, bw, bh, BLUE_BG, BLUE, 1.1)
        s += txt(x + bw / 2, y0 + 28, sym, 22, BLUE_D, "700")
        s += txt(x + bw / 2, y0 + 56, name, 9.5, SUB)
        s += txt(x + bw / 2, y0 + 71, f"Z = {z}", 8.5, SUB)

    y1 = y0 + bh + 20
    s += box(24, y1, 852, 56, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, y1 + 20,
             "Mnemonic: Have No Fear Of Ice Cold Beer　(H-N-O-F-Cl-Br-I)",
             11.5, INK, "600")
    s += txt(450, y1 + 40,
             "氢 氮 氧 氟 氯 溴 碘 — every other element appears as single atoms｜除这 7 种外，其余单质写单原子",
             10.5, SUB)

    y2 = y1 + 56 + 16
    s += box(24, y2, 852, 56, ORANGE_BG, ORANGE, 1.1)
    s += txt(450, y2 + 20, "Two polyatomic elements: P₄ · S₈｜还有两个多原子单质",
             12, ORANGE_D, "700")
    s += txt(450, y2 + 40,
             "Phosphorus is P₄ and sulfur is S₈ — writing single P / S in equations is a classic lost mark"
             "｜磷写 P₄、硫写 S₈，配平写成单原子是最常见丢分点", 10.5, SUB)
    return wrap(s)


# ================================================================ 图 1-3
def fig_ch01_naming_order():
    """英中命名顺序相反：先金属 vs 先非金属。"""
    w, H = 900, 380
    s = head(w, H, "Fig. 1-3　English vs Chinese Naming Order｜英中命名顺序相反",
             "metal first vs non-metal first｜顺序相反")

    # 两栏面板头
    s += box(24, 58, 414, 32, BLUE_BG, BLUE, 1.1)
    s += txt(231, 74, "ENGLISH — metal first｜金属在前", 12, BLUE_D, "700")
    s += box(462, 58, 414, 32, ORANGE_BG, ORANGE, 1.1)
    s += txt(669, 74, "中文 CHINESE — non-metal first｜非金属在前（顺序相反）", 12, ORANGE_D, "700")

    # 例 1：NaCl 拆词
    y, ch = 104, 52
    s += box(54, y, 152, ch, "#FFFFFF", BLUE, 1.1)
    s += txt(130, y + 20, "sodium", 14, BLUE_D, "700")
    s += txt(130, y + 38, "metal｜金属", 9, SUB)
    s += txt(219, y + 26, "→", 16, LINE)
    s += box(232, y, 176, ch, "#FFFFFF", ORANGE, 1.1)
    s += txt(320, y + 20, "chloride", 14, ORANGE_D, "700")
    s += txt(320, y + 38, "non-metal + -ide", 9, SUB)

    s += box(507, y, 120, ch, "#FFFFFF", ORANGE, 1.1)
    s += txt(567, y + 20, "氯", 14, ORANGE_D, "700")
    s += txt(567, y + 38, "non-metal｜非金属", 9, SUB)
    s += box(637, y, 64, ch, NEUTRAL_BG, EDGE, 1.1)
    s += txt(669, y + 26, "化", 14, INK, "700")
    s += box(711, y, 120, ch, "#FFFFFF", BLUE, 1.1)
    s += txt(771, y + 20, "钠", 14, BLUE_D, "700")
    s += txt(771, y + 38, "metal｜金属", 9, SUB)

    # 例 2 / 例 3
    def row(yy, formula, en, en_note, cn, cn_note, cn_col=BLUE_D):
        t = box(40, yy, 390, 58, "#FFFFFF", EDGE, 1.0)
        t += txt(235, yy + 22, f"{formula}　→　{en}", 13, INK, "700")
        t += txt(235, yy + 42, en_note, 10, SUB)
        t += box(470, yy, 390, 58, "#FFFFFF", EDGE, 1.0)
        t += txt(665, yy + 22, f"{formula}　→　{cn}", 13, cn_col, "700")
        t += txt(665, yy + 42, cn_note, 10, SUB)
        return t

    s += row(y + ch + 18, "MgF₂", "magnesium fluoride", "metal name + non-metal-ide",
             "氟化镁", "非金属 + 化 + 金属")
    s += row(y + ch + 18 + 62, "Fe₂S₃", "iron(III) sulfide",
             "multivalent metal needs a Roman numeral",
             "硫化铁（Ⅲ）", "中文可写「(Ⅲ)」或沿用旧称「高铁/亚铁」")

    y4 = y + ch + 18 + 62 + 58 + 18
    s += box(24, y4, 852, 52, "#FFFFFF", RED, 1.1)
    s += txt(450, y4 + 17, "常见错误 Common errors", 11.5, RED, "700")
    s += txt(450, y4 + 37,
             "sodium monochloride (no Greek prefixes) · 钠化氯 (wrong order) ·"
             " copper chloride (missing Roman numeral)｜离子化合物不加前缀 · 中文顺序勿反 · 变价须标数字", 10.5, INK)
    return wrap(s)


# ================================================================ 图 1-4
def fig_ch01_acid_base_salt():
    """酸 / 碱 / 盐 的化学式特征：三栏对照。"""
    w, H = 900, 316
    s = head(w, H, "Fig. 1-4　Acids, Bases and Salts｜酸碱盐的化学式特征",
             "look at the start and end of the formula｜看化学式首尾")

    panels = [
        (24, "ACID 酸", BLUE_BG, BLUE, BLUE_D, "starts with H｜以 H 开头",
         [("HCl", "hydrochloric acid"), ("H₂SO₄", "sulfuric acid"),
          ("HNO₃", "nitric acid"), ("H₃PO₄", "phosphoric acid"),
          ("CH₃COOH", "acetic acid")],
         "donates H⁺ in water｜水溶液给出 H⁺（Ch.7 展开）"),
        (314, "BASE 碱", ORANGE_BG, ORANGE, ORANGE_D, "ends with OH｜以 OH 结尾",
         [("NaOH", "sodium hydroxide"), ("KOH", "potassium hydroxide"),
          ("Ca(OH)₂", "calcium hydroxide"), ("Mg(OH)₂", "magnesium hydroxide"),
          ("NH₃", "ammonia — the common exception, no OH｜唯一常见例外")],
         "gives OH⁻ in water; slippery, bitter｜水溶液给出 OH⁻；滑腻、味苦"),
        (604, "SALT 盐", GREEN_BG, GREEN, GREEN,
         "ionic: metal + non-metal｜金属 + 非金属",
         [("NaCl", "sodium chloride"), ("KNO₃", "potassium nitrate"),
          ("CaCO₃", "calcium carbonate"),
          ("(NH₄)₂SO₄", "ammonium sulfate"),
          ("KMnO₄", "potassium permanganate")],
         "from acid + base neutralization (Ch.7)｜多由酸碱中和"),
    ]

    for x, title, bg, edge, col, lead, rows, note in panels:
        s += box(x, 58, 272, 32, bg, edge, 1.1)
        s += txt(x + 136, 74, title, 13, col, "700")
        s += box(x, 90, 272, 152, "#FFFFFF", EDGE, 1.0)
        s += txt(x + 136, 110, lead, 11.5, col, "700")
        yy = 132
        for formula, name in rows:
            s += txt(x + 136, yy, f"{formula}　{name}", 10.5, INK)
            yy += 18
        s += txt(x + 136, 214, note, 9.5, SUB)

    by = 258
    s += box(24, by, 852, 44, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, by + 16, "How to tell｜判定顺序", 11.5, INK, "700")
    s += txt(450, by + 32,
             "no metal + starts with H → acid　|　metal + ends with OH → base　|　"
             "metal + non-metal → salt｜无金属+H头=酸 · 金属+OH尾=碱 · 金属+非金属=盐", 10.5, SUB)
    return wrap(s)


# ================================================================ 图 2-1
def fig_ch02_atom_rearrange():
    """化学反应 = 原子重排：反应前后原子种类与数目不变。"""
    w, H = 900, 344
    s = head(w, H, "Fig. 2-1　A Chemical Reaction Rearranges Atoms｜化学反应 = 原子重排",
             "atoms are conserved｜原子不增减")
    s += ARROW_DEF

    # ---- 左：反应物
    s += box(24, 58, 340, 176, "#FFFFFF", EDGE, 1.0)
    s += txt(194, 78, "BEFORE — reactants｜反应前（反应物）", 11.5, BLUE_D, "700")
    for cx in (82, 122):
        s += circ(cx, 132, 21, BLUE_BG, BLUE)
        s += txt(cx, 132, "H", 15, BLUE_D, "700")
    s += txt(102, 166, "H₂ hydrogen", 10.5, SUB)
    s += txt(176, 132, "+", 18, LINE, "700")
    for cx in (228, 268):
        s += circ(cx, 132, 21, ORANGE_BG, ORANGE)
        s += txt(cx, 132, "O", 15, ORANGE_D, "700")
    s += txt(248, 166, "O₂ oxygen", 10.5, SUB)
    s += txt(194, 206, "4 H atoms · 2 O atoms｜共 4 个 H、2 个 O", 10.5, INK, "600")

    # ---- 中间箭头
    s += ln(386, 132, 508, 132, LINE, 2.0)
    s += '  <path d="M508 125 L522 132 L508 139 Z" fill="#888780"/>\n'
    s += txt(450, 108, "atoms rearrange", 11.5, INK, "700")
    s += txt(450, 156, "原子重排", 10, SUB)

    # ---- 右：生成物
    s += box(536, 58, 340, 176, "#FFFFFF", EDGE, 1.0)
    s += txt(706, 78, "AFTER — products｜反应后（生成物）", 11.5, ORANGE_D, "700")
    for base in (600, 746):
        s += circ(base, 132, 20, BLUE_BG, BLUE)
        s += txt(base, 132, "H", 14, BLUE_D, "700")
        s += circ(base + 38, 132, 24, ORANGE_BG, ORANGE)
        s += txt(base + 38, 132, "O", 16, ORANGE_D, "700")
        s += circ(base + 76, 132, 20, BLUE_BG, BLUE)
        s += txt(base + 76, 132, "H", 14, BLUE_D, "700")
        s += txt(base + 38, 168, "H₂O water", 10.5, SUB)

    # ---- 底部：原子计数
    s += box(24, 252, 852, 74, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 272, "Atom count｜原子计数", 11.5, INK, "700")
    s += txt(450, 294,
             "H: 4 → 4　O: 2 → 2 — same kinds, same numbers; only partners change"
             "｜种类数目不变，只有「搭档」换了", 11, INK)
    s += txt(450, 314,
             "The literal meaning of the Big Idea — and the microscopic basis of Ch.4 conservation of mass"
             "｜Big Idea 的字面含义，也是 Ch.4 质量守恒的微观依据", 10, SUB)
    return wrap(s)


# ================================================================ 图 2-2
def fig_ch02_evidence():
    """化学变化的六大证据。"""
    w, H = 900, 322
    s = head(w, H, "Fig. 2-2　Evidence of Chemical Change｜化学变化的六大证据",
             "several cues together｜多证据同现")
    cards = [
        ("① Colour change 变色",
         ["iron rusts; a cut apple browns", "石蕊遇酸变红"], BLUE_BG, BLUE, BLUE_D),
        ("② Gas produced 产气",
         ["bubbles: Zn + HCl,", "NaHCO₃ + CH₃COOH"], BLUE_BG, BLUE, BLUE_D),
        ("③ Precipitate 沉淀",
         ["two clear solutions turn cloudy:", "Pb(NO₃)₂ + KI → PbI₂↓"], ORANGE_BG, ORANGE, ORANGE_D),
        ("④ Temperature change 温度变化",
         ["rises: burning, CaO + H₂O", "or drops: cold pack 吸热降温"], ORANGE_BG, ORANGE, ORANGE_D),
        ("⑤ Light given off 发光",
         ["burning Mg gives a dazzling", "white light 耀眼白光"], GREEN_BG, GREEN, GREEN),
        ("⑥ New odour 新气味",
         ["rotten-egg smell (H₂S);", "fruity ester smell 水果香"], GREEN_BG, GREEN, GREEN),
    ]
    for i, (title, lines, bg, edge, col) in enumerate(cards):
        x = 20 + (i % 3) * 288
        y = 58 + (i // 3) * 94
        s += box(x, y, 272, 82, bg, edge, 1.1)
        s += txt(x + 136, y + 20, title, 11, col, "700")
        s += txt(x + 136, y + 46, lines[0], 9.5, INK)
        s += txt(x + 136, y + 64, lines[1], 9.5, INK)

    s += box(20, 250, 860, 58, "#FFFFFF", RED, 1.1)
    s += txt(450, 268, "⚠️ One piece of evidence ≠ chemical change｜单一证据 ≠ 化学变化", 11, RED, "700")
    s += txt(450, 286,
             "Melting ice and dissolving sugar are physical changes — the test is whether a NEW substance forms"
             "｜判据是有没有新物质生成，", 10, INK)
    s += txt(450, 301,
             "i.e. whether atoms have rearranged (Ch.4 explains why)｜本质是原子有没有重排（Ch.4）", 10, SUB)
    return wrap(s)


# ================================================================ 图 2-3
def fig_ch02_equation_ladder():
    """三级台阶：文字方程式 → 骨架方程式 → 配平方程式。"""
    w, H = 900, 372
    s = head(w, H, "Fig. 2-3　Word → Skeleton → Balanced｜方程式的三级台阶",
             "climb one step at a time｜逐级走，不跳级")

    panels = [
        (24, 118, "① Word equation 文字方程式", BLUE_BG, BLUE, BLUE_D,
         ["methane + oxygen", "→ carbon dioxide + water",
          "甲烷 + 氧气 → 二氧化碳 + 水"],
         ["names only, no formulas｜只写名称不写化学式", "word problems start here｜题目的原始形态"]),
        (314, 88, "② Skeleton equation 骨架方程式", ORANGE_BG, ORANGE, ORANGE_D,
         ["CH₄ + O₂", "→ CO₂ + H₂O",
          "formulas right, coefficients blank｜化学式对系数空着"],
         ["all formulas correct (Ch.1)｜化学式全写对", "NOT balanced yet｜此时尚未配平"]),
        (604, 58, "③ Balanced equation 配平方程式", GREEN_BG, GREEN, GREEN,
         ["CH₄ + 2 O₂", "→ CO₂ + 2 H₂O",
          "coefficients in place｜系数齐全"],
         ["验算：C 1=1、H 4=4、", "O 4=4 ✓（Ch.3）"]),
    ]
    for x, y0, chip, bg, edge, col, body, notes in panels:
        s += box(x, y0, 272, 180, "#FFFFFF", EDGE, 1.0)
        s += box(x, y0, 272, 30, bg, edge, 1.1)
        s += txt(x + 136, y0 + 15, chip, 10.5, col, "700")
        s += txt(x + 136, y0 + 52, body[0], 12.5, INK, "700")
        s += txt(x + 136, y0 + 72, body[1], 12.5, INK, "700")
        s += txt(x + 136, y0 + 90, body[2], 9, SUB)
        s += ln(x + 20, y0 + 102, x + 252, y0 + 102, EDGE, 0.9)
        s += txt(x + 136, y0 + 122, notes[0].replace("**", ""), 9.5, INK)
        s += txt(x + 136, y0 + 142, notes[1].replace("**", ""), 9.5, INK)

    s += box(20, 310, 860, 52, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 328,
             "Never skip a step: identify → write formulas → balance; only coefficients change, never subscripts"
             "｜不能跳级；配平只改系数，不改下标", 10.5, INK, "600")
    s += txt(450, 346,
             "Worksheets give either names (you write formulas) or formulas (you just balance)｜学校卷两种给法", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 2-4
def fig_ch02_equation_anatomy():
    """方程式的六个零件：系数 / 化学式 / 状态符号 / 箭头 / 条件 / 下标。"""
    w, H = 900, 460
    s = head(w, H, "Fig. 2-4　Anatomy of a Chemical Equation｜化学方程式六个零件",
             "every position has a rule｜每一处都有规矩")

    # ---- 大方程式
    s += box(24, 54, 852, 88, "#FFFFFF", EDGE, 1.0)
    s += txt(258, 98, "2", 24, ORANGE_D, "700")
    s += txt(292, 98, "H₂", 24, INK, "700")
    s += txt(332, 98, "(g)", 17, BLUE, "600")
    s += txt(366, 98, "+", 20, LINE, "700")
    s += txt(400, 98, "O₂", 24, INK, "700")
    s += txt(440, 98, "(g)", 17, BLUE, "600")
    s += txt(482, 98, "→", 24, LINE, "700")
    s += txt(528, 98, "2", 24, ORANGE_D, "700")
    s += txt(568, 98, "H₂O", 24, INK, "700")
    s += txt(620, 98, "(l)", 17, BLUE, "600")

    # ---- 中文读法
    s += box(24, 152, 852, 52, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 170,
             "Read: 2 hydrogen molecules + 1 oxygen molecule → 2 water molecules｜2 个氢分子 + 1 个氧分子 → 2 个水分子", 11, INK, "700")
    s += txt(450, 190,
             "Coefficients count molecules; subscripts count atoms within one molecule"
             "｜系数数分子、下标数原子，位置与含义完全不同", 10, SUB)

    # ---- 六个零件
    cards = [
        ("① Coefficient 系数", ORANGE_D,
         "the number IN FRONT of a formula｜写在化学式前面", "the only thing you may change: 2 H₂O = 2 molecules"),
        ("② Subscript 下标", BLUE_D,
         "bottom-right of a symbol｜元素符号右下角", "H₂O has 2 H — never change it｜配平绝不能改"),
        ("③ Formula 化学式", INK,
         "every formula must be correct (Ch.1)｜每种物质写对", "diatomic: H₂ / O₂ / N₂ / Cl₂"),
        ("④ State symbol 状态符号", BLUE,
         "(s) solid (l) liquid (g) gas (aq) aqueous｜固液气水溶液", "salt water is NaCl(aq), not NaCl(l)｜不是 NaCl(l)"),
        ("⑤ Arrow 箭头", INK,
         "means yields — never an equals sign｜读作生成，不写等号", "reversible reactions use ⇌ (extension)｜可逆用 ⇌"),
        ("⑥ Condition 反应条件", GREEN,
         "written above / below the arrow｜写在箭头上或下", "Δ heat · catalyst 催化剂 · light 光照"),
    ]
    for i, (title, col, l1, l2) in enumerate(cards):
        x = 20 + (i % 3) * 288
        y = 216 + (i // 3) * 88
        s += box(x, y, 272, 78, "#FFFFFF", EDGE, 1.0)
        s += txt(x + 136, y + 20, title, 11, col, "700")
        s += txt(x + 136, y + 44, l1.replace("**", ""), 9.5, INK)
        s += txt(x + 136, y + 62, l2.replace("**", ""), 9.5, INK)

    s += box(20, 398, 860, 50, "#FFFFFF", RED, 1.1)
    s += txt(450, 415,
             "⛔ Balance by coefficients only, never subscripts — changing a subscript changes the substance"
             "（CO₂ → CO 不再是二氧化碳）", 10.5, RED, "600")
    s += txt(450, 433,
             "Verification (Ch.3): count atoms on both sides — all equal = balanced｜验算见 Ch.3", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 2-5
def fig_ch02_words_to_equation():
    """从文字描述到配平方程式：四步法。"""
    w, H = 900, 430
    s = head(w, H, "Fig. 2-5　Words → Balanced Equation: 4 Steps｜文字描述到配平四步法",
             "school review sheets｜学校复习卷题型")

    steps = [
        ("1", "Underline reactants and products｜划出反应物与生成物",
         "Potassium metal reacts with water to produce potassium hydroxide and hydrogen gas.",
         "K + H₂O → KOH + H₂", BLUE_BG, BLUE, BLUE_D),
        ("2", "Turn every name into a formula (Ch.1)｜名称 → 化学式",
         "K (metal, single atom); water H₂O; KOH; hydrogen H₂ (diatomic!)｜氢气是双原子！",
         "K + H₂O → KOH + H₂", ORANGE_BG, ORANGE, ORANGE_D),
        ("3", "Add state symbols and conditions｜补状态符号与条件",
         "solid / liquid / aqueous / gas → (s)(l)(aq)(g); heat goes above the arrow｜加热写箭头上",
         "K(s)+H₂O(l)→KOH(aq)+H₂(g)", GREEN_BG, GREEN, GREEN),
        ("4", "Balance and verify (coefficients only)｜配平验算，只改系数",
         "after balancing: K 2=2, H 4=4, O 2=2 ✓ (counting table in Ch.3)｜验算全等",
         "2 K + 2 H₂O → 2 KOH + H₂", NEUTRAL_BG, LINE, INK),
    ]
    y = 58
    for num, title, desc, result, bg, edge, col in steps:
        s += box(24, y, 64, 64, bg, edge, 1.1)
        s += txt(56, y + 22, num, 22, col, "700")
        s += txt(56, y + 48, "STEP", 7.5, SUB, "600")
        s += txt(104, y + 20, title, 10.5, col, "700", anchor="start")
        s += txt(104, y + 42, desc, 9, INK, anchor="start")
        s += box(700, y, 176, 64, "#FFFFFF", edge, 1.0)
        s += txt(788, y + 32, result, 10, col, "600")
        if num != "4":
            s += ln(56, y + 64, 56, y + 70, EDGE, 1.2)
        y += 70

    s += box(24, 346, 852, 72, "#FFFFFF", EDGE, 1.0)
    s += txt(450, 364,
             "📌 Key words in word problems｜文字描述里的关键词", 11, INK, "700")
    s += txt(450, 384,
             "solid (s)　liquid (l)　gas (g)　aqueous / solution / dissolved 水溶液 (aq)", 9.5, INK)
    s += txt(450, 402,
             "heat / Δ 加热　catalyst 催化剂　light 光照　burns in air 燃烧　"
             "decomposes 分解　reacts with 与…反应", 9.5, SUB)
    return wrap(s)


# ================================================================ 注册表
FIGURES = {
    "ch01-periodic-charge-map": fig_ch01_periodic_charge_map,
    "ch01-diatomic-h7": fig_ch01_diatomic_h7,
    "ch01-naming-order-en-cn": fig_ch01_naming_order,
    "ch01-acid-base-salt": fig_ch01_acid_base_salt,
    "ch02-atom-rearrange": fig_ch02_atom_rearrange,
    "ch02-evidence": fig_ch02_evidence,
    "ch02-equation-ladder": fig_ch02_equation_ladder,
    "ch02-equation-anatomy": fig_ch02_equation_anatomy,
    "ch02-words-to-equation": fig_ch02_words_to_equation,
}


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    key = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for name, fn in FIGURES.items():
        if key and key not in name:
            continue
        p = os.path.join(FIG_DIR, name + ".svg")
        with open(p, "w", encoding="utf-8") as f:
            f.write(fn())
        n += 1
        print("OK  %-34s %7.1f KB" % (name + ".svg",
                                      os.path.getsize(p) / 1024))
    print("共生成 %d 张 → %s" % (n, FIG_DIR))


if __name__ == "__main__":
    main()
