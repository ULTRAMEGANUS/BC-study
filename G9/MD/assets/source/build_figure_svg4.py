# -*- coding: utf-8 -*-
"""
Ch07–Ch11 章节示意图生成器（第四批）。

风格与 build_figure_svg.py / 2 / 3 完全一致；本批多为流程图、对照图、
分子模型与图表规范。点式/玻尔图等元素直接复用第三批的 lewis()/bohr_*。

用法：
    python build_figure_svg4.py            # 全部生成
    python build_figure_svg4.py ch07       # 只生成文件名含 ch07 的图

输出目录：../figures/
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_figure_svg import (head, box, txt, path, ARROW_DEF, wrap,  # noqa
                              FONT, INK, SUB, LINE, EDGE, BLUE, BLUE_D,
                              BLUE_BG, ORANGE, ORANGE_D, ORANGE_BG,
                              GREEN, GREEN_BG, RED, NEUTRAL_BG)
from build_figure_svg3 import dot, lewis, badge, bohr_panel, panel_h  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(HERE), "figures")


def note_line(x, y, s, size=11, fill=SUB, anchor="start"):
    return txt(x, y, s, size, fill, "400", anchor, "central")


def ion(x, y, label, col, size=16, w=92, h=40):
    """离子小胶囊。"""
    s = box(x - w / 2, y - h / 2, w, h, "#FFFFFF", col, 1.3, rx=8)
    s += txt(x, y, label, size, col, "700")
    return s


# ==================================================== Ch07 图 7-1
def fig_ch07_crisscross():
    s = head(900, 400, "图 7-1　交叉法图解｜Criss-cross Method (Mg + F)",
             "BC Science 9 · 电荷数交叉 → 对方的下标")
    s += ARROW_DEF

    s += ion(230, 96, "Mg²⁺", BLUE_D)
    s += ion(670, 96, "F⁻", ORANGE_D)
    s += txt(230, 132, "电荷 +2", 12, BLUE_D, "700")
    s += txt(670, 132, "电荷 −1", 12, ORANGE_D, "700")

    # 两条交叉线：Mg 的 2 → F 的下标；F 的 1 → Mg 的下标
    s += path("M258 116 C420 150 520 220 636 238", BLUE, 1.8, marker="ar")
    s += path("M642 116 C480 150 380 220 264 238", ORANGE, 1.8, marker="ar")
    s += txt(450, 168, "把电荷数交叉写到对方右下角", 12, INK, "700")

    s += txt(230, 262, "Mg", 26, INK, "700")
    s += txt(262, 276, "1", 15, BLUE_D, "700", "start")
    s += txt(670, 262, "F", 26, INK, "700")
    s += txt(700, 276, "2", 15, ORANGE_D, "700", "start")
    s += txt(450, 262, "→", 20, LINE, "700")
    s += txt(450, 300, "MgF₂　（下标 1 省略）", 20, INK, "700")

    s += box(60, 330, 780, 56, GREEN_BG, GREEN, 1.1, rx=8)
    s += txt(450, 350, "验算 CHECK：(+2)×1 + (−1)×2 = 2 − 2 = 0　✓", 13, GREEN,
             "700")
    s += txt(450, 372, "英文：magnesium fluoride　　中文：氟化镁（非金属在前、金属在后）",
             11.5, INK)
    return wrap(s)


# ==================================================== Ch07 图 7-2
def fig_ch07_reduce():
    s = head(900, 436,
             "图 7-2　必须约成最简比｜Reduce to the Lowest Ratio",
             "BC Science 9 · Mg₂O₂ 是本章第一大陷阱")
    s += ARROW_DEF

    def col(cx, ion1, ion2, c1, c2, sym1, sym2, raw, ok, why, final_cn,
            final_en, raw_ok):
        s = ""
        s += box(cx - 190, 62, 380, 30, NEUTRAL_BG, EDGE, 0.8, rx=6)
        s += txt(cx, 77, f"情形：{ion1} + {ion2}", 12.5, INK, "700")
        s += ion(cx - 90, 126, ion1, BLUE_D, size=15, w=86, h=36)
        s += ion(cx + 90, 126, ion2, ORANGE_D, size=15, w=86, h=36)
        s += path(f"M{cx - 60} 146 L{cx + 34} 186", BLUE, 1.6)
        s += path(f"M{cx + 60} 146 L{cx - 34} 186", ORANGE, 1.6)
        s += txt(cx, 196, raw, 20, INK, "700")
        s += txt(cx + 62, 196, "← 交叉结果", 10.5, SUB, "400", "start")
        s += txt(cx, 226, ok, 16, GREEN if raw_ok else RED, "700")
        s += txt(cx, 252, why, 11.5, SUB)
        if not raw_ok:
            s += path(f"M{cx} 268 L{cx} 292", BLUE, 1.8, marker="ar")
            s += txt(cx + 70, 280, "约简 + 去下标 1", 11, BLUE_D, "700",
                     "start")
        s += txt(cx, 314, final_cn, 22, INK, "700")
        s += txt(cx, 342, final_en, 12, SUB)
        return s

    s += col(240, "Mg²⁺", "O²⁻", 2, 2, "Mg", "O", "Mg₂O₂", "✗ 错",
             "公因数 2 → 必须约简", "MgO　氧化镁", "magnesium oxide", False)
    s += col(660, "Al³⁺", "O²⁻", 3, 2, "Al", "O", "Al₂O₃", "✓ 对",
             "2 与 3 互质 → 不能约", "Al₂O₃　氧化铝", "aluminium oxide", True)
    s += path("M450 90 L450 350", EDGE, 1.0, dash="4 4")

    s += box(60, 376, 780, 48, ORANGE_BG, ORANGE, 1.0, rx=8)
    s += txt(450, 394, "再一个：Na⁺ + S²⁻ → Na₂S₁ → Na₂S　硫化钠 sodium sulfide",
             13, ORANGE_D, "700")
    s += txt(450, 414, "见电荷相同（2 与 2）立刻想到 1:1；互质的下标必须原样保留",
             11.5, ORANGE_D)
    return wrap(s)


# ==================================================== Ch07 图 7-3
def fig_ch07_transfer():
    s = head(900, 456,
             "图 7-3　电子转移与路易斯图｜Electron Transfer &amp; Lewis Diagram (MgF₂)",
             "BC Science 9 · 阳离子 0 点、阴离子 8 点")
    s += ARROW_DEF

    s += box(40, 62, 820, 106, BLUE_BG, BLUE, 1.1, rx=8)
    s += txt(56, 82, "STEP 1　起始：镁有 2 个价电子，氟各有 7 个价电子", 12.5,
             BLUE_D, "700", "start")
    s += lewis(220, 132, "Mg", 2, size=17, col=BLUE_D)
    s += txt(300, 132, "+", 18, INK)
    s += lewis(430, 132, "F", 7, size=17, col=ORANGE_D)
    s += txt(510, 132, "+", 18, INK)
    s += lewis(640, 132, "F", 7, size=17, col=ORANGE_D)
    s += txt(220, 158, "自己不稳（想丢 2 个）", 10, BLUE_D)
    s += txt(535, 158, "各缺 1 个（想拿 1 个）", 10, ORANGE_D)

    s += box(40, 182, 820, 130, ORANGE_BG, ORANGE, 1.1, rx=8)
    s += txt(56, 202, "STEP 2　电子转移：Mg 把 2 个电子分开送给 2 个 F", 12.5,
             ORANGE_D, "700", "start")
    s += path("M270 176 C290 214 300 214 340 216", ORANGE, 1.6, marker="ar")
    s += path("M270 176 C420 150 560 190 610 216", ORANGE, 1.6, marker="ar")
    s += txt(300, 168, "e⁻", 11, ORANGE_D, "700")
    s += txt(520, 168, "e⁻", 11, ORANGE_D, "700")
    s += lewis(220, 268, "Mg", 0, charge="²⁺", bracket=True, size=17,
               col=BLUE_D)
    s += lewis(430, 268, "F", 8, charge="⁻", bracket=True, size=17,
               col=ORANGE_D)
    s += lewis(640, 268, "F", 8, charge="⁻", bracket=True, size=17,
               col=ORANGE_D)
    s += txt(220, 300, "(0 个点)", 10.5, BLUE_D, "700")
    s += txt(535, 300, "(8 个点)", 10.5, ORANGE_D, "700")

    s += box(40, 326, 820, 118, GREEN_BG, GREEN, 1.1, rx=8)
    s += txt(56, 346, "STEP 3　静电吸引 → 组成 MgF₂（氟化镁 magnesium fluoride）",
             12.5, GREEN, "700", "start")
    s += lewis(220, 398, "Mg", 0, charge="²⁺", bracket=True, size=17,
               col=BLUE_D)
    s += lewis(430, 398, "F", 8, charge="⁻", bracket=True, size=17,
               col=ORANGE_D)
    s += lewis(640, 398, "F", 8, charge="⁻", bracket=True, size=17,
               col=ORANGE_D)
    s += path("M300 398 L360 398", GREEN, 1.4)
    s += path("M500 398 L560 398", GREEN, 1.4)
    s += txt(450, 430, "MgF₂　氟化镁", 18, INK, "700")
    return wrap(s)


# ==================================================== Ch07 图 7-4
def fig_ch07_naming_flow():
    s = head(900, 560, "图 7-4　命名流程图｜Naming Decision Flowchart",
             "BC Science 9 · 分水岭：有没有金属")
    s += ARROW_DEF

    s += box(340, 62, 220, 38, NEUTRAL_BG, LINE, 1.2, rx=8)
    s += txt(450, 81, "给定化学式 / 名称", 13, INK, "700")
    s += path("M450 100 L450 118", LINE, 1.6)
    s += path("M180 118 L720 118", LINE, 1.6)
    s += path("M180 118 L180 142", LINE, 1.6, marker="ar")
    s += path("M720 118 L720 142", LINE, 1.6, marker="ar")
    s += txt(126, 132, "是 metal + non-metal", 11, BLUE_D, "700", "end")
    s += txt(126, 146, "（或含 NH₄⁺ 铵根）？", 11, BLUE_D, "700", "end")
    s += txt(774, 132, "全是 non-metal", 11, ORANGE_D, "700", "start")
    s += txt(774, 146, "（见 Ch.8）", 11, ORANGE_D, "700", "start")

    # 左：IONIC
    s += box(50, 148, 260, 34, BLUE_BG, BLUE, 1.3, rx=8)
    s += txt(180, 165, "离子化合物 IONIC", 13.5, BLUE_D, "700")
    for i, t in enumerate(["① 写离子符号（含电荷）", "② 交叉法 → 下标",
                           "③ 约简 + 去 1"]):
        s += txt(70, 200 + i * 22, t, 11.5, INK, "400", "start")
    s += box(50, 274, 260, 34, "#FFFFFF", BLUE, 1.0, rx=6)
    s += txt(180, 291, "金属是多变价吗？", 12, BLUE_D, "700")
    s += path("M120 308 L120 326", LINE, 1.4, marker="ar")
    s += path("M240 308 L240 326", LINE, 1.4, marker="ar")
    s += txt(116, 320, "否", 10.5, SUB, "700", "end")
    s += txt(246, 320, "是", 10.5, SUB, "700", "start")
    s += box(46, 330, 128, 46, "#FFFFFF", EDGE, 0.9, rx=6)
    s += txt(110, 346, "直接写 metal 名", 10.5, INK, "600")
    s += txt(110, 362, "NaCl sodium chloride", 9.5, SUB)
    s += box(186, 330, 128, 46, "#FFFFFF", EDGE, 0.9, rx=6)
    s += txt(250, 346, "金属名 + (罗马数字)", 10.5, INK, "600")
    s += txt(250, 360, "FeCl₃ iron(III) chloride", 9, SUB)
    s += txt(250, 372, "FeCl₂ iron(II) chloride", 9, SUB)
    s += path("M180 380 L180 398", LINE, 1.4, marker="ar")
    s += box(50, 402, 260, 34, "#FFFFFF", ORANGE, 1.0, rx=6)
    s += txt(180, 419, "含多原子离子？直接照抄离子名", 11, ORANGE_D, "700")
    for i, t in enumerate(["CaCO₃ calcium carbonate",
                           "NaOH  sodium hydroxide",
                           "(NH₄)₂SO₄ ammonium sulfate"]):
        s += txt(70, 452 + i * 18, t, 10.5, SUB, "400", "start")

    # 右：MOLECULAR
    s += box(590, 148, 260, 34, ORANGE_BG, ORANGE, 1.3, rx=8)
    s += txt(720, 165, "分子化合物 MOLECULAR", 13.5, ORANGE_D, "700")
    for i, t in enumerate(["① 数各元素原子个数",
                           "② 第二元素加希腊前缀 + -ide",
                           "③ 第一元素仅在 >1 时加前缀（永不用 mono-）"]):
        s += txt(610, 200 + i * 22, t, 11.5, INK, "400", "start")
    s += box(590, 274, 260, 52, "#FFFFFF", EDGE, 0.9, rx=6)
    s += txt(720, 292, "CO₂ → carbon dioxide", 11.5, ORANGE_D, "600")
    s += txt(720, 310, "CO  → carbon monoxide", 11.5, ORANGE_D, "600")
    s += txt(720, 332, "中文：二氧化碳 / 一氧化碳", 11, INK, "600")

    # 底部：中文倒序
    s += box(50, 496, 800, 52, RED, RED, 1.4, rx=8)
    s += txt(60, 516, "★ 翻成中文时把顺序倒过来：", 12.5, "#FFFFFF", "700",
             "start")
    s += txt(60, 536, "sodium chloride → 氯化钠（不是「钠化氯」）　calcium carbonate → 碳酸钙　ammonium sulfate → 硫酸铵",
             11.5, "#FFFFFF", "400", "start")
    return wrap(s)


# ==================================================== Ch07 图 7-5
def fig_ch07_lattice():
    s = head(900, 344, "图 7-5　离子晶格与导电性｜Crystal Lattice &amp; Conductivity",
             "BC Science 9 · 变的只是能不能移动")
    # 左：固体晶格
    s += box(50, 62, 380, 30, ORANGE_BG, ORANGE, 1.0, rx=6)
    s += txt(240, 77, "固体 NaCl（不导电）", 12.5, ORANGE_D, "700")
    cells = [["Na⁺", "Cl⁻", "Na⁺", "Cl⁻"], ["Cl⁻", "Na⁺", "Cl⁻", "Na⁺"],
             ["Na⁺", "Cl⁻", "Na⁺", "Cl⁻"]]
    gx, gy, cw2 = 110, 104, 65
    for r, row in enumerate(cells):
        for c, v in enumerate(row):
            col = BLUE_D if v.startswith("Na") else ORANGE_D
            x, y = gx + c * cw2, gy + r * 52
            s += box(x, y, cw2, 52, "#FFFFFF", EDGE, 0.9, rx=3)
            s += txt(x + cw2 / 2, y + 26, v, 13, col, "700")
    s += txt(410, 180, "离子被锁死", 11.5, ORANGE_D, "700", "start")
    s += txt(410, 200, "在晶格上", 11.5, ORANGE_D, "700", "start")
    s += box(50, 268, 380, 32, "#FFFFFF", ORANGE, 1.0, rx=6)
    s += txt(240, 284, "灯泡不亮　✗", 13, ORANGE_D, "700")

    # 右：溶液/熔融
    s += box(470, 62, 380, 30, GREEN_BG, GREEN, 1.0, rx=6)
    s += txt(660, 77, "NaCl(aq) 或熔融 NaCl（导电）", 12.5, GREEN, "700")
    s += box(470, 100, 380, 156, "#FFFFFF", EDGE, 0.9, rx=8)
    free = [("Na⁺", 540, 140), ("Cl⁻", 660, 126), ("Na⁺", 780, 150),
            ("Cl⁻", 560, 196), ("Na⁺", 690, 208), ("Cl⁻", 800, 196)]
    for v, x, y in free:
        col = BLUE_D if v.startswith("Na") else ORANGE_D
        s += txt(x, y, v, 15, col, "700")
    s += txt(660, 176, "· 自由移动 ·", 11.5, GREEN, "700")
    s += txt(660, 240, "离子一直都在，只是现在能自由移动", 11, GREEN, "700")
    s += box(470, 268, 380, 32, "#FFFFFF", GREEN, 1.0, rx=6)
    s += txt(660, 284, "电流通过　灯泡亮　✓", 13, GREEN, "700")

    s += box(50, 312, 800, 22, NEUTRAL_BG, EDGE, 0.8, rx=5)
    s += txt(450, 323, "解释「固体不导电、溶液导电」的唯一正确答案：离子一直都在，变的只是能不能移动",
             11.5, INK, "600")
    return wrap(s)


# ==================================================== Ch07 图 7-9
def fig_ch07_brackets():
    s = head(900, 276, "图 7-9　括号使用对照｜To Bracket or Not",
             "BC Science 9 · 个数 > 1 才加括号")
    rows = [("MgOH₂", "Mg(OH)₂", "氢氧化镁 magnesium hydroxide"),
            ("AlSO₄₃", "Al₂(SO₄)₃", "硫酸铝　aluminium sulfate"),
            ("CaPO₄₂", "Ca₃(PO₄)₂", "磷酸钙　calcium phosphate"),
            ("NH₄₂SO₄", "(NH₄)₂SO₄", "硫酸铵　ammonium sulfate"),
            ("NaOH₂", "NaOH", "氢氧化钠（OH 只有 1 个 → 不要括号、不要下标）")]
    for i, (bad, good, cn) in enumerate(rows):
        y = 76 + i * 36
        s += box(60, y, 150, 30, "#FDECEC", RED, 0.9, rx=5)
        s += txt(135, y + 15, "✗  " + bad, 13, RED, "700")
        s += txt(232, y + 15, "→", 14, LINE, "700")
        s += box(252, y, 190, 30, "#EAF3DE", GREEN, 0.9, rx=5)
        s += txt(347, y + 15, "✓  " + good, 13.5, GREEN, "700")
        s += txt(460, y + 15, cn, 11.5, INK, "600", "start")
    s += box(60, 262, 780, 0, "none", "none", 0)
    return wrap(s)


# ==================================================== Ch07 主线因果链
def fig_ch07_main_chain():
    s = head(900, 470, "全册主线：从原子序数到化合物性质｜The Main Chain",
             "BC Science 9 · 顺着读能推性质，倒着读能认物质")
    s += ARROW_DEF
    steps = [("原子序数 atomic number", "= 质子数 = 电子数", BLUE_BG, BLUE_D),
             ("电子排布 electron arrangement", "例：Mg 2-8-2，F 2-7　（Ch.5 玻尔图分层）", BLUE_BG, BLUE_D),
             ("价电子数 valence electrons", "Mg → 2 个价电子；F → 7 个价电子", BLUE_BG, BLUE_D),
             ("得失电子数 gained / lost e⁻", "八隅体规则 Ch.6：趋向 8 电子稳定结构 → Mg²⁺、F⁻", ORANGE_BG, ORANGE_D),
             ("化合物中的原子个数比 ratio", "总电荷必须为零 → 用交叉法求最简整数比：Mg²⁺ : F⁻ = 1 : 2", ORANGE_BG, ORANGE_D),
             ("化学式 chemical formula", "MgF₂　（反过来也成立：由化学式可读出电子排布）", ORANGE_BG, ORANGE_D),
             ("命名 naming", "magnesium fluoride ／ 氟化镁（中文顺序相反）", GREEN_BG, GREEN),
             ("化合物的性质 properties", "结构决定性质：晶体、高熔点、硬脆、熔融或水溶液导电", GREEN_BG, GREEN)]
    y = 74
    for i, (t1, t2, bg, fg) in enumerate(steps):
        s += box(70, y, 760, 40, bg, fg, 1.0, rx=7)
        s += badge(104, y + 20, 13, str(i + 1), fg)
        s += txt(126, y + 13, t1, 12.5, fg, "700", "start")
        s += txt(126, y + 30, t2, 10.5, INK, "400", "start")
        if i < len(steps) - 1:
            s += path(f"M450 {y + 40} L450 {y + 48}", LINE, 1.5, marker="ar")
        y += 48
    return wrap(s)


# ==================================================== Ch08 图 8-1
def pair_dots(x, y, n, vertical=True, col=INK, r=3.2, gap=6, step=9):
    """画 n 对共用电子（每对 2 点）。vertical=True 时每对竖排。"""
    s = ""
    for k in range(n):
        ox = 0 if vertical else (k - (n - 1) / 2) * step
        oy = (k - (n - 1) / 2) * step if vertical else 0
        if vertical:
            s += dot(x + ox, y + oy - gap / 2, r, col)
            s += dot(x + ox, y + oy + gap / 2, r, col)
        else:
            s += dot(x + ox - gap / 2, y + oy, r, col)
            s += dot(x + ox + gap / 2, y + oy, r, col)
    return s


def fig_ch08_covalent():
    s = head(900, 344, "图 8-1　共价键的形成｜How a Covalent Bond Forms (H₂)",
             "BC Science 9 · 谁也没丢电子，只是共享")
    s += ARROW_DEF
    steps = [("STEP 1　两个 H 原子各有 1 个电子，都不肯把它交出去",
              [(0, 0)], "H ·", "· H", None),
             ("STEP 2　把电子推到中间，两个核共同吸引这一对电子",
              [(1, 0)], "H :", ": H", "中间这一对就是 shared pair 共用电子对"),
             ("STEP 3　用短线代替这一对电子（需要时再还原成点式）",
              [(2, 0)], "H —", "— H", "single covalent bond 单键")]
    y = 76
    for i, (t, _u, a, b, note) in enumerate(steps):
        s += box(50, y, 800, 60, NEUTRAL_BG if i == 0 else
                 (BLUE_BG if i == 1 else GREEN_BG), EDGE, 0.9, rx=8)
        s += txt(66, y + 16, t, 12, INK, "700", "start")
        s += txt(330, y + 40, a, 20, INK, "700")
        s += txt(450, y + 40, b, 20, INK, "700")
        if i == 0:
            s += txt(390, y + 40, "·", 20, INK, "700")
            s += txt(450, y + 40, "· H", 20, INK, "700")
        if i == 1:
            s += pair_dots(390, y + 40, 1)
            s += txt(660, y + 40, note, 11, BLUE_D, "600", "start")
        if i == 2:
            s += path("M366 124 L434 124", INK, 2.6)
            s += txt(660, y + 40, note, 11, GREEN, "600", "start")
        if i < 2:
            s += path(f"M450 {y + 60} L450 {y + 72}", LINE, 1.5,
                      marker="ar")
        y += 84
    s += box(50, 268, 800, 62, "#FFFFFF", ORANGE, 1.1, rx=8)
    s += txt(66, 288, "★ 两个 H 都因此拥有了 2 个价电子 → 达到 He 的稳定结构（duet rule）",
             12, ORANGE_D, "700", "start")
    s += txt(66, 312, "★ 没有任何电子被「转移走」，所以没有离子生成 → 这就是分子化合物不导电的根子",
             12, ORANGE_D, "700", "start")
    return wrap(s)


# ==================================================== Ch08 图 8-2
def fig_ch08_three_molecules():
    s = head(900, 436,
             "图 8-2　三种常见分子的点式与结构式｜Lewis &amp; Structural Formulas",
             "BC Science 9 · 每一对共用电子 = 一条短线")
    s += ARROW_DEF
    # ---- 点式
    cy = 148
    # H2O
    s += txt(112, cy, "H", 18, INK, "700")
    s += txt(180, cy, "O", 18, INK, "700")
    s += txt(248, cy, "H", 18, INK, "700")
    s += pair_dots(146, cy, 1)
    s += pair_dots(214, cy, 1)
    s += pair_dots(180, cy - 30, 1, vertical=False)
    s += pair_dots(180, cy + 30, 1, vertical=False)
    # CO2
    s += txt(372, cy, "O", 18, INK, "700")
    s += txt(450, cy, "C", 18, INK, "700")
    s += txt(528, cy, "O", 18, INK, "700")
    s += pair_dots(406, cy, 2)
    s += pair_dots(494, cy, 2)
    s += pair_dots(372, cy - 30, 1, vertical=False)
    s += pair_dots(372, cy + 30, 1, vertical=False)
    s += pair_dots(528, cy - 30, 1, vertical=False)
    s += pair_dots(528, cy + 30, 1, vertical=False)
    # NH3
    s += txt(650, cy, "H", 18, INK, "700")
    s += txt(720, cy, "N", 18, INK, "700")
    s += txt(790, cy, "H", 18, INK, "700")
    s += txt(720, cy + 54, "H", 18, INK, "700")
    s += pair_dots(685, cy, 1)
    s += pair_dots(755, cy, 1)
    s += pair_dots(720, cy + 28, 1, vertical=False)
    s += pair_dots(720, cy - 30, 1, vertical=False)

    s += txt(450, 214, "↓　把每一对共用电子改成短线　↓", 11.5, SUB, "600")

    # ---- 结构式
    sy = 262
    s += txt(112, sy, "H", 18, INK, "700")
    s += txt(180, sy, "O", 18, INK, "700")
    s += txt(248, sy, "H", 18, INK, "700")
    s += path("M130 262 L156 262", INK, 2.2)
    s += path("M204 262 L230 262", INK, 2.2)
    s += txt(372, sy, "O", 18, INK, "700")
    s += txt(450, sy, "C", 18, INK, "700")
    s += txt(528, sy, "O", 18, INK, "700")
    s += path("M390 254 L432 254", INK, 2.0)
    s += path("M390 268 L432 268", INK, 2.0)
    s += path("M468 254 L510 254", INK, 2.0)
    s += path("M468 268 L510 268", INK, 2.0)
    s += txt(650, sy, "H", 18, INK, "700")
    s += txt(720, sy, "N", 18, INK, "700")
    s += txt(790, sy, "H", 18, INK, "700")
    s += txt(720, sy + 54, "H", 18, INK, "700")
    s += path("M668 262 L702 262", INK, 2.2)
    s += path("M738 262 L772 262", INK, 2.2)
    s += path("M720 280 L720 306", INK, 2.2)

    for x, cn, en, shape in [(180, "水 water", "H₂O", "bent 折线形"),
                             (450, "二氧化碳", "CO₂", "linear 直线形"),
                             (720, "氨 ammonia", "NH₃", "pyramidal 三角锥")]:
        s += txt(x, 344, cn, 12.5, INK, "700")
        s += txt(x, 362, en, 12, SUB, "600")
        s += txt(x, 380, shape, 11, BLUE_D, "600")

    s += box(50, 396, 800, 30, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(450, 411, "数一数：H₂O 的 O 有 2 对共用 + 2 对孤对；CO₂ 每个 O 与 C 之间共用 2 对（= 双键）；NH₃ 的 N 上方还有 1 对孤对",
             11, INK, "600")
    return wrap(s)


# ==================================================== Ch08 图 8-3
def fig_ch08_bond_types():
    s = head(900, 320, "图 8-3　单键 / 双键 / 三键｜Single, Double and Triple Bonds",
             "BC Science 9 · 短线数量 = 共用电子对数量")
    cols = [("单键 single bond", "(1 对共用电子)", 1, "H", "H", "hydrogen 氢气 H₂"),
            ("双键 double bond", "(2 对共用电子)", 2, "O", "O", "oxygen 氧气 O₂"),
            ("三键 triple bond", "(3 对共用电子)", 3, "N", "N", "nitrogen 氮气 N₂")]
    xs = [170, 450, 730]
    for i, (t1, t2, n, a, b, name) in enumerate(cols):
        x = xs[i]
        s += box(x - 130, 62, 260, 34, NEUTRAL_BG, EDGE, 0.9, rx=6)
        s += txt(x, 74, t1, 12.5, INK, "700")
        s += txt(x, 90, t2, 11, SUB)
        s += txt(x - 46, 146, a, 22, INK, "700")
        s += txt(x + 46, 146, b, 22, INK, "700")
        for k in range(n):
            off = (k - (n - 1) / 2) * 8
            s += path(f"M{x - 22} {146 + off} L{x + 22} {146 + off}", INK, 2.2)
        s += txt(x, 186, name, 12, INK, "600")
        s += txt(x, 206, ["键长最长、键能最小", "键长居中，键更强",
                          "键长最短，键最强（N₂ 极稳定）"][i], 11,
                 ORANGE_D, "600")
    s += box(50, 234, 800, 30, ORANGE_BG, ORANGE, 1.0, rx=6)
    s += txt(450, 249, "为什么 N₂ 这么稳定、能占空气 78%？因为三键太难被拉断。",
             12.5, ORANGE_D, "700")
    s += txt(450, 284, "双键不是「画得粗一点」，而是实实在在 4 个电子参与", 11.5,
             INK, "600")
    return wrap(s)


# ==================================================== Ch08 图 8-4
def fig_ch08_methane():
    s = head(900, 356, "图 8-4　甲烷分子模型｜Methane Model (CH₄)",
             "BC Science 9 · 下标 4 是真实原子数，不许约简")
    heads = ["路易斯点式", "结构式 structural", "球棍模型 ball-and-stick"]
    for i, t in enumerate(heads):
        x = 160 + i * 290
        s += box(x - 130, 62, 260, 28, NEUTRAL_BG, EDGE, 0.8, rx=6)
        s += txt(x, 76, t, 12, INK, "700")

    # 点式
    cx, cy = 160, 168
    s += txt(cx, cy - 56, "H", 17, INK, "700")
    s += txt(cx - 62, cy, "H", 17, INK, "700")
    s += txt(cx, cy, "C", 17, INK, "700")
    s += txt(cx + 62, cy, "H", 17, INK, "700")
    s += txt(cx, cy + 56, "H", 17, INK, "700")
    s += pair_dots(cx, cy - 28, 1, vertical=False)
    s += pair_dots(cx - 32, cy, 1)
    s += pair_dots(cx + 32, cy, 1)
    s += pair_dots(cx, cy + 28, 1, vertical=False)

    # 结构式
    cx = 450
    s += txt(cx, cy - 56, "H", 17, INK, "700")
    s += txt(cx - 62, cy, "H", 17, INK, "700")
    s += txt(cx, cy, "C", 17, INK, "700")
    s += txt(cx + 62, cy, "H", 17, INK, "700")
    s += txt(cx, cy + 56, "H", 17, INK, "700")
    s += path(f"M{cx} 126 L{cx} 156", INK, 2.0)
    s += path(f"M404 168 L434 168", INK, 2.0)
    s += path(f"M466 168 L496 168", INK, 2.0)
    s += path(f"M{cx} 180 L{cx} 210", INK, 2.0)

    # 球棍模型
    cx, cy = 740, 168
    for dx, dy in [(0, -58), (-58, 0), (58, 0), (0, 58), (-42, 42),
                   (42, 42)][:4]:
        s += path(f"M{cx} {cy} L{cx + dx} {cy + dy}", LINE, 2.4)
    s += dot(cx, cy, 17, "#5F5E5A")
    s += txt(cx, cy, "C", 14, "#FFFFFF", "700")
    for dx, dy in [(0, -58), (-58, 0), (58, 0), (0, 58)]:
        s += dot(cx + dx, cy + dy, 11, "#FFFFFF", BLUE, 1.6)
        s += txt(cx + dx, cy + dy, "H", 10.5, BLUE_D, "700")

    s += box(50, 240, 800, 104, NEUTRAL_BG, EDGE, 0.9, rx=8)
    s += txt(66, 262, "★ C 有 4 个价电子 → 与 4 个 H 各共用 1 对 → 4 条单键",
             12, INK, "700", "start")
    s += txt(66, 284, "★ H 达到 2 电子稳定；C 达到 8 电子稳定（octet rule 八隅体规则）",
             12, INK, "700", "start")
    s += txt(66, 306, "★ 英文名 methane（俗名，必背）；系统名 carbon tetrahydride；中文名 甲烷",
             11.5, SUB, "400", "start")
    s += txt(66, 328, "　　「甲」= 1 个碳，属有机命名【Extension → Science 10】",
             11.5, SUB, "400", "start")
    return wrap(s)


# ==================================================== Ch08 图 8-5
def fig_ch08_naming_flow():
    s = head(900, 528, "图 8-5　命名总流程图｜Complete Naming Flowchart",
             "BC Science 9 · 只需一个分支：有没有金属")
    s += ARROW_DEF
    s += box(330, 62, 240, 36, NEUTRAL_BG, LINE, 1.2, rx=8)
    s += txt(450, 80, "拿到一个化学式 / 中文名", 13, INK, "700")
    s += path("M450 98 L450 114", LINE, 1.6)
    s += box(210, 118, 480, 38, ORANGE_BG, ORANGE, 1.2, rx=8)
    s += txt(450, 132, "含 metal（金属）或含 NH₄⁺ ？", 13.5, ORANGE_D, "700")
    s += txt(450, 148, "是 ↓　　　　　　　　　　　否（全是非金属）↓", 11, ORANGE_D)
    s += path("M240 156 L240 178", ORANGE, 1.6, marker="ar")
    s += path("M660 156 L660 178", ORANGE, 1.6, marker="ar")

    s += box(60, 182, 360, 38, BLUE_BG, BLUE, 1.3, rx=8)
    s += txt(240, 201, "IONIC 离子化合物（Ch.7）", 13.5, BLUE_D, "700")
    s += box(480, 182, 360, 38, GREEN_BG, GREEN, 1.3, rx=8)
    s += txt(660, 201, "MOLECULAR 分子（共价）化合物（Ch.8）", 13, GREEN, "700")

    left = ["① 写离子 + 电荷", "② 交叉 → 下标", "③ 约简到最简比 + 去 1",
            "④ 多变价 → 加罗马数字", "⑤ 多原子离子 → 抄离子名"]
    right = ["① 数各元素的原子个数", "② 第二元素：加希腊前缀 + 改 -ide",
             "③ 第一元素：仅当 >1 加前缀（永不用 mono-）",
             "④ 对照俗名单，命中则写俗名",
             "⑤ 检查拼写：monoxide / tetroxide"]
    for i, t in enumerate(left):
        s += txt(78, 244 + i * 24, t, 11.5, INK, "400", "start")
    for i, t in enumerate(right):
        s += txt(498, 244 + i * 24, t, 11.5, INK, "400", "start")
    s += path("M240 372 L240 396", BLUE, 1.6, marker="ar")
    s += path("M660 372 L660 396", GREEN, 1.6, marker="ar")

    s += box(120, 400, 660, 108, "#FFFFFF", RED, 1.4, rx=10)
    s += txt(450, 424, "★ 翻成中文时两侧都要把顺序「翻过来」：", 13, RED, "700")
    s += txt(450, 450, "sodium chloride → 氯化钠（不是「钠化氯」）", 12.5,
             INK, "600")
    s += txt(450, 476, "carbon dioxide　→ 二氧化碳（不是「碳化二氧」）", 12.5,
             INK, "600")
    s += txt(450, 498, "整章只需记住一个分支：有没有金属。这一句决定后面所有规则。",
             11, SUB)
    return wrap(s)


# ==================================================== Ch08 图 8-6
def fig_ch08_bond_strength():
    s = head(900, 340,
             "图 8-6　共价键 vs 分子间作用力｜Bond Strength Clarified",
             "BC Science 9 · 强的是分子内部，弱的是分子之间")
    s += box(50, 62, 360, 34, BLUE_BG, BLUE, 1.1, rx=6)
    s += txt(230, 79, "分子内部 INSIDE the molecule", 13, BLUE_D, "700")
    s += box(70, 106, 320, 130, "#FFFFFF", BLUE, 1.3, rx=10)
    s += txt(160, 152, "H", 19, INK, "700")
    s += txt(230, 152, "O", 19, INK, "700")
    s += txt(300, 152, "H", 19, INK, "700")
    s += path("M178 152 L204 152", INK, 2.6)
    s += path("M256 152 L282 152", INK, 2.6)
    s += txt(230, 186, "共用电子对　共价键 COVALENT", 11.5, BLUE_D, "700")
    s += txt(230, 208, "★ 非常强 ★　(~ 400 kJ/mol)", 12, BLUE_D, "700")

    s += box(490, 62, 360, 34, ORANGE_BG, ORANGE, 1.1, rx=6)
    s += txt(670, 79, "分子之间 BETWEEN molecules", 13, ORANGE_D, "700")
    s += box(500, 106, 150, 100, "#FFFFFF", EDGE, 1.0, rx=8)
    s += txt(575, 146, "H₂O", 15, INK, "700")
    s += txt(575, 168, "分子", 11, SUB)
    s += box(690, 106, 150, 100, "#FFFFFF", EDGE, 1.0, rx=8)
    s += txt(765, 146, "H₂O", 15, INK, "700")
    s += txt(765, 168, "分子", 11, SUB)
    for k in range(3):
        s += dot(660, 140 + k * 14, 2.6, ORANGE)
    s += txt(670, 226, "↑ intermolecular force 分子间作用力", 11.5, ORANGE_D,
             "700")
    s += txt(670, 246, "★ 非常弱 ★　(~ 40 kJ/mol，约 1/10)", 11.5, ORANGE_D)

    s += box(50, 262, 800, 62, GREEN_BG, GREEN, 1.1, rx=8)
    s += txt(66, 282, "加热沸腾时：破的是 ──→ 分子之间的「点线」，不是分子内部的「短线」",
             12.5, GREEN, "700", "start")
    s += txt(66, 306, "⇒ 所以 H₂O 到 100 ℃ 就沸腾，但 H₂O 分子本身并没有肢解成 H 和 O。",
             12, GREEN, "700", "start")
    return wrap(s)


# ==================================================== Ch08 例题 B 判定表
def fig_ch08_judge_table():
    s = head(900, 452, "例题 B　判断 ionic / molecular｜Judge the Type",
             "BC Science 9 · 判据只有一个：有没有 metal 或 NH₄⁺")
    s += box(50, 58, 800, 28, BLUE_BG, BLUE, 1.0, rx=6)
    s += txt(450, 72, "判据：有没有 metal 或 NH₄⁺？ 有 → ionic；全非金属 → molecular",
             12.5, BLUE_D, "700")
    rows = [("(a)", "Mg 金属 + O", "IONIC", "magnesium oxide 氧化镁", None),
            ("(b)", "S + O 全非金属", "MOLECULAR", "sulfur dioxide 二氧化硫",
             None),
            ("(c)", "N, H, Cl 全非金属", "IONIC ★",
             "ammonium chloride 氯化铵", "★ 含 NH₄⁺ 多原子阳离子——例外！"),
            ("(d)", "C + H 全非金属", "MOLECULAR",
             "methane 甲烷（俗名，必背）", None),
            ("(e)", "Si 类金属 + O", "MOLECULAR",
             "silicon dioxide 二氧化硅", "★ Si 是 metalloid，按非金属处理"),
            ("(f)", "H + F 全非金属", "MOLECULAR",
             "hydrogen monofluoride 氟化氢", None)]
    cols = [50, 112, 300, 510]
    widths = [62, 188, 210, 340]
    s += box(50, 92, 800, 26, NEUTRAL_BG, EDGE, 0.8, rx=4)
    for i, h in enumerate(["物质", "元素组成", "判定", "英文 / 中文名"]):
        s += txt(cols[i] + 10, 105, h, 11.5, INK, "700", "start")
    for r, (no, comp, kind, name, extra) in enumerate(rows):
        y = 118 + r * 40
        h = 52 if extra else 40
        vals = [no, comp, kind, name]
        for i, v in enumerate(vals):
            bg = "#FFFFFF"
            fg = INK
            if i == 2:
                bg = BLUE_BG if v.startswith("IONIC") else GREEN_BG
                fg = BLUE_D if v.startswith("IONIC") else GREEN
            s += box(cols[i], y, widths[i], h, bg, EDGE, 0.8, rx=4)
            s += txt(cols[i] + 10, y + h / 2 - (8 if extra else 0), v, 11.5,
                     fg, "700", "start")
        if extra:
            s += txt(cols[3] + 10, y + 36, extra, 10, RED, "600", "start")
    y = 118 + 6 * 40 + 12
    s += box(50, y, 800, 84, ORANGE_BG, ORANGE, 1.0, rx=8)
    s += txt(66, y + 20, "再验证一轮（性质反推）：", 12, ORANGE_D, "700", "start")
    s += txt(66, y + 42, "(a) MgO 熔点 2852 ℃、熔融导电 → IONIC ✓　　　(b) SO₂ 室温是气体、不导电 → MOLECULAR ✓",
             11.5, ORANGE_D, "400", "start")
    s += txt(66, y + 64, "(f) HF 溶于水会微弱导电【Extension → Science 10】；9 年级仍按「非金属+非金属 = molecular」判定。",
             11.5, ORANGE_D, "400", "start")
    return wrap(s)


# ==================================================== Ch08 主线（两条路）
def fig_ch08_main_chain():
    s = head(900, 560, "全册主线：两条路 A vs 路 B｜The Two Routes",
             "BC Science 9 · 一切差异源自「电子给不给」")
    s += ARROW_DEF
    s += box(70, 62, 760, 44, NEUTRAL_BG, LINE, 1.2, rx=8)
    s += txt(450, 78, "电子排布 electron arrangement", 13, INK, "700")
    s += txt(450, 96, "C 2-4、O 2-6、H 1、N 2-5　→　最外层不够满，都想达到 stable octet",
             11, SUB)
    s += path("M450 106 L450 122", LINE, 1.6)
    s += txt(450, 134, "两条路 A vs 路 B", 12.5, INK, "700")
    s += path("M180 146 L720 146", LINE, 1.6)
    s += path("M180 146 L180 168", BLUE, 1.6, marker="ar")
    s += path("M720 146 L720 168", GREEN, 1.6, marker="ar")

    left = [("金属 + 非金属", BLUE_BG, BLUE_D),
            ("一方愿「给」，一方愿「拿」", "#FFFFFF", INK),
            ("TRANSFER 电子转移", BLUE_BG, BLUE_D),
            ("cation + anion", "#FFFFFF", INK),
            ("个数比（必须最简）", BLUE_BG, BLUE_D),
            ("MgF₂ / MgO / CaCO₃", "#FFFFFF", INK),
            ("交叉法 · 罗马数字 · 多原子离子", BLUE_BG, BLUE_D),
            ("English: magnesium oxide", "#FFFFFF", INK),
            ("中文：氧化镁（倒序）", "#FFFFFF", INK),
            ("晶体 · 高熔点 · 熔融/溶液导电", BLUE_BG, BLUE_D)]
    right = [("非金属 + 非金属", GREEN_BG, GREEN),
             ("双方都「不肯给」", "#FFFFFF", INK),
             ("SHARING 电子共用", GREEN_BG, GREEN),
             ("共用电子对 → 分子", "#FFFFFF", INK),
             ("原子个数（不许约简）", GREEN_BG, GREEN),
             ("H₂O / CO₂ / CH₄", "#FFFFFF", INK),
             ("希腊前缀 · 俗名", GREEN_BG, GREEN),
             ("English: carbon dioxide", "#FFFFFF", INK),
             ("中文：二氧化碳（倒序）", "#FFFFFF", INK),
             ("气体液体 · 低熔点 · 不导电", GREEN_BG, GREEN)]
    for i, ((lt, lb, lf), (rt, rb, rf)) in enumerate(zip(left, right)):
        y = 172 + i * 32
        s += box(70, y, 340, 30, lb, EDGE if lb == "#FFFFFF" else lf, 0.9,
                 rx=5)
        s += txt(240, y + 15, lt, 11.5, lf, "600")
        s += box(490, y, 340, 30, rb, EDGE if rb == "#FFFFFF" else rf, 0.9,
                 rx=5)
        s += txt(660, y + 15, rt, 11.5, rf, "600")
        if i < len(left) - 1:
            s += path(f"M240 {y + 30} L240 {y + 32}", LINE, 1.2)
            s += path(f"M660 {y + 30} L660 {y + 32}", LINE, 1.2)

    y = 172 + 10 * 32 + 6
    s += path("M240 492 L240 506 L660 506 L660 492", LINE, 1.6)
    s += box(190, 510, 520, 42, "#FFF8E1", ORANGE_D, 1.3, rx=8)
    s += txt(450, 526, "★★★ 一切差异，都源自「电子给不给」★★★", 13, ORANGE_D,
             "700")
    s += txt(450, 544, "价电子数 → 得失电子数 → 共用电子数 → 化学式中原子个数 → 命名规则 → 性质",
             10.5, INK)
    return wrap(s)


# ==================================================== Ch09 图 9-1
def fig_ch09_evidence():
    s = head(900, 350, "图 9-1　化学变化证据盘｜Evidence of Chemical Change",
             "BC Science 9 · 六种证据都是线索，不是结论")
    s += ARROW_DEF
    s += box(310, 62, 280, 46, NEUTRAL_BG, LINE, 1.3, rx=8)
    s += txt(450, 78, "IS IT A CHEMICAL CHANGE?", 13.5, INK, "700")
    s += txt(450, 98, "是化学变化吗？", 12, SUB)
    s += path("M450 108 L450 132", LINE, 1.6)
    s += path("M130 132 L770 132", LINE, 1.6)
    ev = [("colour change", "变色", BLUE_BG, BLUE_D),
          ("gas / bubbles", "生成气体", ORANGE_BG, ORANGE_D),
          ("precipitate", "生成沉淀", GREEN_BG, GREEN),
          ("temperature", "温度变化", "#FDECEC", RED),
          ("light / odour", "发光 / 新气味", "#F3EEFA", "#5B4B8A")]
    for i, (en, cn, bg, fg) in enumerate(ev):
        x = 130 + i * 160
        s += path(f"M{x} 132 L{x} 152", LINE, 1.4, marker="ar")
        s += box(x - 70, 156, 140, 60, bg, fg, 1.1, rx=8)
        s += txt(x, 178, en, 12, fg, "700")
        s += txt(x, 200, cn, 12.5, fg, "600")
    s += path("M130 216 L770 216", LINE, 1.4)
    s += path("M450 216 L450 236", LINE, 1.6, marker="ar")
    s += box(120, 240, 660, 96, ORANGE_BG, ORANGE, 1.3, rx=10)
    s += txt(450, 264, "⚠ 单一证据不充分！必须问：有没有 NEW SUBSTANCE 新物质生成？",
             13, ORANGE_D, "700")
    s += txt(450, 292, "有新物质 → CHEMICAL CHANGE 化学变化", 12.5, INK, "700")
    s += txt(450, 316, "无新物质 → PHYSICAL CHANGE 物理变化", 12.5, INK, "700")
    return wrap(s)


# ==================================================== Ch09 图 9-2
def fig_ch09_three_levels():
    s = head(900, 420, "图 9-2　三级方程式阶梯｜From Words to a Balanced Equation",
             "BC Science 9 · 唯一能改的是系数")
    s += ARROW_DEF
    levels = [("第 1 级　WORD EQUATION 文字方程式",
               ["hydrogen  +  oxygen  ──▶  water",
                "氢气      +  氧气    ──▶   水"],
               "（只写名称，不涉及原子数）", BLUE_BG, BLUE_D,
               "把名称换成化学式（下标照抄，双原子分子别忘 ₂）"),
              ("第 2 级　SKELETON EQUATION 骨架方程式",
               ["H₂  +  O₂  ──▶  H₂O"],
               "⚠ 未配平：左 O = 2，右 O = 1　✘", ORANGE_BG, ORANGE_D,
               "只在化学式前面加系数（绝不改下标）"),
              ("第 3 级　BALANCED EQUATION 配平方程式",
               ["2H₂  +  O₂  ──▶  2H₂O"],
               "✔ 左：H = 4，O = 2　　右：H = 4，O = 2", GREEN_BG, GREEN,
               None)]
    y = 66
    for i, (t, eqs, note, bg, fg, trans) in enumerate(levels):
        h = 40 + len(eqs) * 22
        s += box(70, y, 760, h, bg, fg, 1.2, rx=8)
        s += txt(90, y + 18, t, 12.5, fg, "700", "start")
        for k, e in enumerate(eqs):
            s += txt(450, y + 42 + k * 22, e, 15, INK, "700")
        s += txt(450, y + h - 10, note, 11, fg, "600")
        if trans:
            s += path(f"M450 {y + h} L450 {y + h + 16}", LINE, 1.5,
                      marker="ar")
            s += txt(470, y + h + 8, trans, 11, INK, "600", "start")
            y += h + 44
        else:
            y += h + 10
    s += box(70, y + 4, 760, 30, NEUTRAL_BG, EDGE, 0.9, rx=6)
    s += txt(450, y + 19, "三级是递进关系：骨架式来自文字式，配平式来自骨架式",
             12, INK, "700")
    return wrap(s)


# ==================================================== Ch09 图 9-3
def tile_cluster(x, y, groups, sep=10):
    """groups = [[原子标签,...], ...]：一簇 = 一个分子。"""
    s = ""
    cx = x
    for g in groups:
        w = len(g) * 30 + 12
        s += box(cx, y, w, 34, "#FFFFFF", INK, 1.4, rx=5)
        for i, a in enumerate(g):
            s += txt(cx + 18 + i * 30, y + 17, a, 15, INK, "700")
        cx += w + sep
    return s, (cx - sep - x)


def fig_ch09_stickers():
    s = head(900, 500, "图 9-3　磁贴配平示意｜Sticker Model for Balancing",
             "BC Science 9 · 整簇整簇地复制，不能拆")
    s += ARROW_DEF
    s += txt(450, 62, "每个方框 = 1 个原子；一「簇」方框 = 1 个分子", 12,
             INK, "700")
    cases = [("① 骨架式（不配平）", [["H", "H"], ["O", "O"]], [["H", "O"]],
              "左：H = 2，O = 2　　右：H = 2，O = 1　← O 不平", "✘", RED,
              BLUE_BG),
             ("② 只改下标 = 犯罪！（把 H₂O 写成 H₂O₂）",
              [["H", "H"], ["O", "O"]], [["H", "O", "O"]],
              "H₂O₂ 是过氧化氢（双氧水），不是水！→ 你已经把反应偷偷换掉了",
              "✘✘", RED, "#FDECEC"),
             ("③ 正确做法：复制整簇磁贴（加系数 2）",
              [["H", "H"], ["O", "O"]], [["H", "O"], ["H", "O"]],
              "左：H = 2，O = 2　　右：H = 4，O = 2　← O 平了，H 又不平",
              "△", ORANGE_D, ORANGE_BG),
             ("④ 左边也复制一份 H₂（系数 2）",
              [["H", "H"], ["H", "H"], ["O", "O"]], [["H", "O"], ["H", "O"]],
              "左：H = 4，O = 2　　右：H = 4，O = 2　✔ 配平！", "✔", GREEN,
              GREEN_BG)]
    y = 84
    for title, left, right, note, mark, mcol, bg in cases:
        s += box(50, y, 800, 98, bg, EDGE, 0.9, rx=8)
        s += txt(66, y + 18, title, 12, INK, "700", "start")
        a, w1 = tile_cluster(80, y + 34, left)
        s += a
        ax = 80 + w1 + 22
        s += path(f"M{ax} {y + 51} L{ax + 34} {y + 51}", INK, 1.8,
                  marker="ar")
        b, w2 = tile_cluster(ax + 48, y + 34, right)
        s += b
        s += txt(ax + 60 + w2 + 20, y + 51, mark, 22, mcol, "700", "start")
        s += txt(66, y + 88, note, 11, mcol, "600", "start")
        y += 106
    return wrap(s)


# ==================================================== Ch09 图 9-4
def fig_ch09_anatomy():
    s = head(900, 336, "图 9-4　系数 vs 下标解剖图｜Anatomy of a Formula",
             "BC Science 9 · 系数可改，下标不可改")
    s += ARROW_DEF
    s += txt(300, 76, "coefficient 系数（可改）", 13, BLUE_D, "700")
    s += path("M300 90 L300 122", BLUE, 1.6, marker="ar")
    s += box(276, 126, 48, 40, BLUE_BG, BLUE, 1.4, rx=6)
    s += txt(300, 146, "2", 22, BLUE_D, "700")
    s += txt(360, 146, "H₂O", 30, INK, "700")
    s += path("M368 166 L368 196", ORANGE, 1.6)
    s += path("M400 166 L400 196", ORANGE, 1.6)
    s += path("M368 196 L400 196", ORANGE, 1.6)
    s += path("M384 196 L384 210", ORANGE, 1.6, marker="ar")
    s += txt(392, 224, "subscript 下标（不可改）", 12, ORANGE_D, "700",
             "start")
    s += txt(500, 146, "← 元素符号", 12, SUB, "400", "start")

    s += box(70, 244, 760, 76, NEUTRAL_BG, EDGE, 1.0, rx=8)
    s += txt(450, 266, "2 H₂O = 2 个水分子 = 4 个 H 原子（2×2）+ 2 个 O 原子（2×1）",
             13, INK, "700")
    s += txt(450, 292, "算原子总数公式：原子数 = 系数 × 下标", 12.5, BLUE_D,
             "700")
    s += txt(450, 312, "例：3Ca(OH)₂ → Ca = 3×1 = 3；O = 3×2 = 6；H = 3×2 = 6",
             11.5, SUB)
    return wrap(s)


# ==================================================== Ch10 图 10-1
def fig_ch10_cycle():
    s = head(900, 486, "图 10-1　科学探究循环流程图｜The Inquiry Cycle",
             "BC Science 9 · 是循环，不是直线")
    s += ARROW_DEF
    steps = [("1", "QUESTION 提问", "「水温会影响糖的溶解速度吗？」", NEUTRAL_BG, INK),
             ("2", "HYPOTHESIS 假设", "If 水温↑, then 溶解更快, because 粒子运动更快", BLUE_BG, BLUE_D),
             ("3", "PREDICTION 预测", "「60 ℃ 时应能在 30 s 内溶完」", BLUE_BG, BLUE_D),
             ("4", "EXPERIMENT 实验", "公平实验 fair test：一次只改 1 个变量", ORANGE_BG, ORANGE_D),
             ("5", "DATA 数据", "定性 + 定量 + 单位，重复 3 次", ORANGE_BG, ORANGE_D),
             ("6", "ANALYSIS 分析", "作图、算平均、找趋势 trend", GREEN_BG, GREEN),
             ("7", "CONCLUSION 结论", "数据支持假设吗？必须引用证据", GREEN_BG, GREEN),
             ("8", "COMMUNICATION 交流", "报告 / 海报 / 汇报 + 误差与改进", NEUTRAL_BG, INK)]
    y = 64
    for i, (n, t, d, bg, fg) in enumerate(steps):
        s += box(70, y, 760, 40, bg, EDGE if bg == NEUTRAL_BG else fg, 1.0,
                 rx=7)
        s += badge(104, y + 20, 13, n, fg)
        s += txt(126, y + 14, t, 12.5, fg, "700", "start")
        s += txt(126, y + 31, d, 11, INK, "400", "start")
        if i < len(steps) - 1:
            s += path(f"M450 {y + 40} L450 {y + 48}", LINE, 1.5, marker="ar")
        y += 48
    s += path("M450 448 L450 462 L800 462 L800 64", BLUE, 1.8, marker="ar")
    s += txt(700, 456, "结论常常引出新的问题 → 循环回到 1. QUESTION", 11.5,
             BLUE_D, "700")
    return wrap(s)


# ==================================================== Ch10 图 10-2
def fig_ch10_variables():
    s = head(900, 424, "图 10-2　变量三栏对照｜Variables at a Glance",
             "BC Science 9 · 控制变量要写成带数值的清单")
    cols = [("INDEPENDENT 自变量", "我主动改变 I CHANGE", BLUE_BG, BLUE_D,
             ["画在 x 轴", "每实验只能有 1 个", "例：水温 20/40/60 ℃"]),
            ("DEPENDENT 因变量", "我被动测量 I MEASURE", ORANGE_BG, ORANGE_D,
             ["画在 y 轴", "可以有多个", "例：溶解时间 (s)"]),
            ("CONTROLLED 控制变量", "我刻意固定 KEEP SAME", GREEN_BG, GREEN,
             ["不画，写成清单", "越多越好（越公平）",
              "例：糖 5 g、水 100 mL、不搅拌、同型号烧杯"])]
    x0, cw = 50, 266
    for i, (t1, t2, bg, fg, rows) in enumerate(cols):
        x = x0 + i * (cw + 16)
        s += box(x, 62, cw, 34, bg, fg, 1.2, rx=6)
        s += txt(x + cw / 2, 79, t1, 13, fg, "700")
        s += box(x, 96, cw, 30, "#FFFFFF", EDGE, 0.9, rx=6)
        s += txt(x + cw / 2, 111, t2, 11.5, INK, "600")
        for k, r in enumerate(rows):
            s += box(x, 126 + k * 46, cw, 46, "#FFFFFF", EDGE, 0.9, rx=6)
            s += txt(x + cw / 2, 149 + k * 46, r, 11.5, INK, "400")
    y = 126 + 3 * 46 + 12
    s += box(70, y, 760, 100, ORANGE_BG, ORANGE, 1.2, rx=8)
    s += txt(450, y + 24, "FAIR TEST 公平实验 = 一次只改 1 个自变量 + 其余全部列入控制变量清单",
             12.5, ORANGE_D, "700")
    s += txt(450, y + 50, "漏掉的那一个 → CONFOUNDING VARIABLE 干扰变量 → 结论不可信",
             12.5, ORANGE_D, "700")
    s += txt(450, y + 78, "只写「水量相同」不够，要写「每次都用 100 mL 蒸馏水」",
             11.5, INK)
    return wrap(s)


# ==================================================== Ch10 图 10-3
def diamond(cx, cy, r):
    return (f'  <path d="M{cx} {cy - r} L{cx + r} {cy} L{cx} {cy + r} '
            f'L{cx - r} {cy} Z" fill="#FFFFFF" stroke="{INK}" '
            f'stroke-width="1.8"/>\n')


def fig_ch10_whmis():
    # 3 行卡片 + 底部统一说明条（494→526），另留 24 下边距 → 画布高 550
    s = head(900, 550, "图 10-3　WHMIS 标识图形卡｜WHMIS Pictogram Cards",
             "BC Science 9 · 菱形边框 + 黑色符号")
    cards = [
        ("① FLAMMABLE", "易燃", "flame",
         "火焰 flame → 远离明火，改用热水浴加热"),
        ("② CORROSIVE", "腐蚀性", "corr",
         "试管滴液腐蚀手和桌面 → 戴手套、大量水冲洗 15 min"),
        ("③ TOXIC", "有毒", "skull", "骷髅 + 交叉骨 → 少量即可致命"),
        ("④ OXIDIZING", "氧化性", "oxid", "圆圈上托火焰 → 助燃，远离可燃物"),
        ("⑤ COMPRESSED GAS", "压缩气体", "gas", "钢气瓶 → 固定存放、防撞击受热"),
        ("⑥ BIOHAZARD", "生物危害", "bio", "三叶环 trefoil → 生物材料，严禁带离"),
        ("⑦ ENVIRONMENT", "环境危害", "env", "枯树 + 死鱼 → 对水生生物有毒"),
        ("⑧ EXPLOSIVE", "爆炸性", "boom", "炸弹 + 碎片 → 防震、防热、防摩擦"),
        ("⑨ IRRITANT", "刺激性", "irri", "感叹号 → 引起皮肤/呼吸道不适"),
    ]
    x0, y0, cw, ch = 60, 76, 260, 132
    for i, (en, cn, kind, desc) in enumerate(cards):
        r, c = divmod(i, 3)
        x = x0 + c * (cw + 10)
        y = y0 + r * (ch + 6)
        s += box(x, y, cw, ch, "#FFFFFF", EDGE, 0.9, rx=8)
        s += diamond(x + 52, y + 58, 34)
        gx, gy = x + 52, y + 58
        if kind == "flame":
            s += (f'  <path d="M{gx} {gy - 16} C{gx + 10} {gy - 4} '
                  f'{gx + 8} {gy + 12} {gx} {gy + 16} '
                  f'C{gx - 8} {gy + 12} {gx - 10} {gy - 4} {gx} {gy - 16} Z" '
                  f'fill="{INK}"/>\n')
        elif kind == "corr":
            s += (f'  <path d="M{gx - 12} {gy - 16} L{gx - 2} {gy - 16} '
                  f'L{gx - 6} {gy + 2} L{gx - 12} {gy + 2} Z" '
                  f'fill="{INK}"/>\n')
            s += dot(gx - 9, gy + 12, 3.4, INK)
            s += box(gx + 2, gy + 6, 16, 10, INK, INK, 0)
        elif kind == "skull":
            s += dot(gx, gy - 4, 10, INK)
            s += dot(gx - 4, gy - 6, 2.2, "#FFFFFF")
            s += dot(gx + 4, gy - 6, 2.2, "#FFFFFF")
            s += path(f"M{gx - 8} {gy + 6} L{gx + 8} {gy + 16}", INK, 2.6)
            s += path(f"M{gx + 8} {gy + 6} L{gx - 8} {gy + 16}", INK, 2.6)
        elif kind == "oxid":
            s += f'  <circle cx="{gx}" cy="{gy}" r="12" fill="none" ' \
                 f'stroke="{INK}" stroke-width="2"/>\n'
            s += (f'  <path d="M{gx} {gy - 18} C{gx + 8} {gy - 8} '
                  f'{gx + 6} {gy + 4} {gx} {gy + 8} '
                  f'C{gx - 6} {gy + 4} {gx - 8} {gy - 8} {gx} {gy - 18} Z" '
                  f'fill="{INK}"/>\n')
        elif kind == "gas":
            s += box(gx - 8, gy - 18, 16, 34, "none", INK, 2.0, rx=4)
            s += path(f"M{gx - 4} {gy - 22} L{gx + 4} {gy - 22}", INK, 2.0)
        elif kind == "bio":
            for k in range(3):
                a = -90 + k * 120
                import math
                px = gx + 11 * math.cos(math.radians(a))
                py = gy + 11 * math.sin(math.radians(a))
                s += f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="6.5" ' \
                     f'fill="none" stroke="{INK}" stroke-width="1.8"/>\n'
            s += dot(gx, gy, 3, INK)
        elif kind == "env":
            s += path(f"M{gx - 12} {gy + 14} L{gx - 12} {gy - 2}", INK, 2.0)
            s += (f'  <path d="M{gx - 20} {gy - 2} L{gx - 4} {gy - 2} '
                  f'L{gx - 12} {gy - 18} Z" fill="{INK}"/>\n')
            s += f'  <ellipse cx="{gx + 8}" cy="{gy + 6}" rx="9" ry="5" ' \
                 f'fill="{INK}"/>\n'
            s += (f'  <path d="M{gx + 17} {gy + 6} L{gx + 24} {gy} '
                  f'L{gx + 24} {gy + 12} Z" fill="{INK}"/>\n')
        elif kind == "boom":
            s += dot(gx - 4, gy, 11, INK)
            for k in range(6):
                import math
                a = math.radians(-60 + k * 24)
                s += path(f"M{gx - 4 + 13 * math.cos(a):.1f} "
                          f"{gy + 13 * math.sin(a):.1f} "
                          f"L{gx - 4 + 22 * math.cos(a):.1f} "
                          f"{gy + 22 * math.sin(a):.1f}", INK, 2.0)
        else:  # irri
            s += box(gx - 3, gy - 14, 6, 20, INK, INK, 0)
            s += dot(gx, gy + 12, 3.4, INK)
        s += txt(x + 108, y + 40, en, 12, INK, "700", "start")
        s += txt(x + 108, y + 60, cn, 13, BLUE_D, "700", "start")
        s += txt(x + 108, y + 84, desc, 9.5, SUB, "400", "start")
    y = y0 + 3 * (ch + 6) + 4
    s += box(50, y, 800, 32, NEUTRAL_BG, EDGE, 0.9, rx=6)
    s += txt(450, y + 16, "所有标识统一为：菱形边框（旋转 45° 的正方形）＋ 黑色符号；边框 ◇　底色白　符号黑",
             11.5, INK, "700")
    return wrap(s)


# ==================================================== Ch10 图 10-4
def fig_ch10_table_graph():
    s = head(900, 486, "图 10-4　数据记录表与作图规范｜Data Table &amp; Graph Standards",
             "BC Science 9 · 自变量永远在 x 轴")
    s += txt(450, 66, "① 数据记录表 Data Table（必须有表头 + 单位；自变量在左列）",
             12.5, INK, "700")
    heads = ["Temperature (℃)", "Trial 1 (s)", "Trial 2 (s)", "Average (s)"]
    subs = ["自变量 →", "因变量 →", "", ""]
    x0, cw = 70, 190
    for i, h in enumerate(heads):
        s += box(x0 + i * cw, 82, cw, 26, BLUE_BG, BLUE, 1.0, rx=4)
        s += txt(x0 + i * cw + cw / 2, 95, h, 11.5, BLUE_D, "700")
    for i, t in enumerate(subs):
        if t:
            s += txt(x0 + i * cw + cw / 2, 118, t, 9.5, SUB, "600")
    rows = [["20", "62", "58", "60"], ["40", "41", "39", "40"],
            ["60", "28", "26", "27"]]
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            s += box(x0 + c * cw, 108 + r * 26, cw, 26, "#FFFFFF", EDGE,
                     0.9, rx=4)
            s += txt(x0 + c * cw + cw / 2, 121 + r * 26, v, 11.5, INK, "700")
    s += txt(70, 208, "定性观察 Qualitative：60 ℃ 时杯底有对流扰动；溶液始终无色透明。",
             10.5, SUB, "400", "start")

    # ---- 作图
    s += txt(450, 232, "② 作图 Graph", 12.5, INK, "700")
    gx, gy, gw, gh = 120, 258, 640, 150
    s += box(gx, gy, gw, gh, "#FFFFFF", EDGE, 1.0, rx=4)
    s += path(f"M{gx + 46} {gy + 10} L{gx + 46} {gy + gh - 22}", INK, 1.6)
    s += path(f"M{gx + 46} {gy + gh - 22} L{gx + gw - 16} {gy + gh - 22}",
              INK, 1.6)
    for k in range(8):
        xx = gx + 46 + (k + 1) * (gw - 62) / 8.0
        s += path(f"M{xx:.1f} {gy + gh - 26} L{xx:.1f} {gy + gh - 22}",
                  INK, 1.0)
    for k in range(6):
        yy = gy + 14 + k * (gh - 42) / 6.0
        s += path(f"M{gx + 42} {yy:.1f} L{gx + 46} {yy:.1f}", INK, 1.0)
    pts = [(20, 60), (40, 40), (60, 27)]
    def px(t):
        return gx + 46 + (t / 80.0) * (gw - 62)
    def py(v):
        return gy + gh - 22 - (v / 70.0) * (gh - 40)
    for t, v in pts:
        s += dot(px(t), py(v), 4.2, BLUE_D)
        s += txt(px(t) + 26, py(v) - 8, f"({t},{v})", 9.5, SUB, "400",
                 "start")
    s += path(f"M{px(14):.1f} {py(66):.1f} L{px(70):.1f} {py(18):.1f}",
              ORANGE, 1.8)
    s += txt(px(48), py(52), "← 最佳拟合线 line of best fit", 9.5, ORANGE_D,
             "600", "start")
    s += txt(gx + 20, gy + gh / 2, "Time (s) 因变量 y", 11, INK, "700",
             "start")
    s += txt(gx + gw / 2, gy + gh + 12, "Temperature (℃)　自变量 x", 11,
             INK, "700")
    s += box(70, 428, 760, 44, GREEN_BG, GREEN, 1.0, rx=6)
    s += txt(450, 444, "Title：The Effect of Water Temperature on the Dissolving Time of Sugar",
             11, GREEN, "700")
    s += txt(450, 462, "✔ 轴名 + 单位　✔ 等距刻度　✔ 描点清晰　✔ 最佳拟合线（平滑线，不是折线）",
             11, INK)
    return wrap(s)


# ==================================================== Ch10 图 10-5
def fig_ch10_interpolation():
    s = head(900, 424, "图 10-5　内插与外推｜Interpolation vs Extrapolation",
             "BC Science 9 · 结论的取值范围 = 你的取值范围")
    gx, gy, gw, gh = 120, 74, 620, 190
    s += box(gx, gy, gw, gh, "#FFFFFF", EDGE, 1.0, rx=4)
    s += path(f"M{gx + 44} {gy + 12} L{gx + 44} {gy + gh - 26}", INK, 1.6)
    s += path(f"M{gx + 44} {gy + gh - 26} L{gx + gw - 14} {gy + gh - 26}",
              INK, 1.6)

    def px(t):
        return gx + 44 + (t / 110.0) * (gw - 58)
    def py(v):
        return gy + gh - 26 - (v / 75.0) * (gh - 46)
    pts = [(20, 62), (40, 41), (60, 27)]
    for t, v in pts:
        s += dot(px(t), py(v), 4.4, BLUE_D)
    # 实测范围
    s += box(px(20) - 6, gy + 12, px(60) - px(20) + 12, gh - 38, GREEN_BG,
             GREEN, 0.9, rx=4)
    s += path(f"M{px(14):.1f} {py(70):.1f} L{px(72):.1f} {py(18):.1f}",
              ORANGE, 1.8, dash="5 3")
    s += path(f"M{px(72):.1f} {py(18):.1f} L{px(104):.1f} {py(-14):.1f}",
              RED, 1.8, dash="5 3")
    s += txt(px(30), gy + 26, "实测范围 20–60 ℃", 10.5, GREEN, "700", "start")
    s += txt(gx + 18, gy + gh / 2, "Time (s)", 11, INK, "700", "start")
    s += txt(gx + gw / 2, gy + gh + 12, "Temperature (℃)", 11, INK, "700")

    s += box(70, 288, 380, 60, GREEN_BG, GREEN, 1.1, rx=8)
    s += txt(260, 308, "INTERPOLATION 内插（数据点之间）", 12, GREEN, "700")
    s += txt(260, 330, "✅ 可信：估计 30 ℃ 的值 → 约 50 s", 11.5, INK, "600")
    s += box(470, 288, 360, 60, "#FDECEC", RED, 1.1, rx=8)
    s += txt(650, 308, "EXTRAPOLATION 外推 ⚠ 危险", 12, RED, "700")
    s += txt(650, 330, "延长到 100 ℃ 会得到负的溶解时间（物理上荒谬）", 11,
             INK, "600")

    s += box(70, 358, 760, 56, NEUTRAL_BG, EDGE, 0.9, rx=6)
    s += txt(90, 376, "❌ 过度外推：「由此可知所有固体在所有温度下都溶解得更快」",
             11.5, RED, "600", "start")
    s += txt(90, 398, "✅ 正确结论：「在 20–60 ℃ 范围内，对 5 g 蔗糖 / 100 mL 水这一条件，水温越高，溶解所需时间越短。」",
             11, GREEN, "600", "start")
    return wrap(s)


# ==================================================== Ch11 图 11-1
def fig_ch11_master():
    # 画布高度由内容算出（手写数字会随步骤增删而失配，见 check_svg_bounds.py）
    steps = [
        ("① 电子排布 electron arrangement", "Ch.5",
         ["Bohr 图：核内 p⁺/n⁰，核外电子按 2-8-8 分层"]),
        ("② 周期表位置 position on the periodic table", "Ch.2 / Ch.3",
         ["周期数 = 电子层数　　主族族号 → 价电子数"]),
        ("③ 价电子数 number of valence electrons", "Ch.5",
         ["1族→1　2族→2　13→3　14→4　15→5　16→6　17→7　18→8 (He=2)"]),
        ("④ 得失电子倾向 tendency to lose or gain", "Ch.4 / Ch.6",
         ["金属（左侧）：价电子少 → 倾向失去 lose",
          "非金属（右侧）：价电子多 → 倾向得到 gain",
          "满层 8 个（He 2 个）→ 稳定 stable，不反应（稀有气体）"]),
        ("⑤ 离子电荷 ion charge", "Ch.6",
         ["cation 阳离子：金属失电子 → 正电（+1 +2 +3）",
          "anion 阴离子：非金属得电子 → 负电（−3 −2 −1）",
          "八隅体规则 octet rule：一切为了「满层」"]),
        ("⑥ 化合物的化学式与命名 formula &amp; naming", "Ch.7 / Ch.8",
         ["IONIC 金属+非金属：交叉法 criss-cross　MgCl₂ magnesium chloride 氯化镁",
          "MOLECULAR 非金属+非金属：前缀法 prefixes　CO₂ carbon dioxide 二氧化碳"]),
        ("⑦ 化合物的性质 properties of compounds", "Ch.7 / Ch.8",
         ["离子：晶体 · 高熔沸点 · 硬而脆 · 溶于水或熔融时导电",
          "分子：低熔沸点 · 不导电 · 多为气/液/软固"]),
        ("⑧ 证据与方法 evidence &amp; inquiry", "Ch.9 / Ch.10",
         ["化学变化证据：变色 / 气体 / 沉淀 / 温度 / 发光 / 新气味",
          "公平实验 fair test · 变量控制 · WHMIS 安全 · 误差与改进"]),
    ]
    y_end = 132 + sum(30 + len(ln) * 19 + 12 for _, _, ln in steps)
    H = y_end + 4 + 34 + 24          # 结尾绿框 + 下边距
    s = head(900, H, "图 11-1　全册主线流程图｜The Master Flowchart",
             "BC Science 9 · 顺读推性质，倒读认物质")
    s += ARROW_DEF
    s += box(50, 58, 800, 62, BLUE_BG, BLUE, 1.4, rx=10)
    s += txt(450, 78, "BC SCIENCE 9 · CHEMISTRY UNIT · 全册主线", 14,
             BLUE_D, "700")
    s += txt(450, 100, "BIG IDEA: The electron arrangement of atoms impacts their chemical nature.",
             11.5, INK)
    s += txt(450, 116, "—— 原子的电子排布决定其化学性质", 11.5, INK)

    y = 132
    for i, (t, ch, lines) in enumerate(steps):
        h = 30 + len(lines) * 19
        s += box(70, y, 760, h, "#FFFFFF", BLUE, 1.0, rx=7)
        s += badge(104, y + 16, 12, str(i + 1), BLUE_D, size=11)
        s += txt(124, y + 16, t, 12, BLUE_D, "700", "start")
        s += txt(830, y + 16, ch, 10.5, SUB, "600", "end")
        for k, ln in enumerate(lines):
            s += txt(124, y + 36 + k * 19, ln, 10.5, INK, "400", "start")
        if i < len(steps) - 1:
            s += path(f"M450 {y + h} L450 {y + h + 8}", LINE, 1.5,
                      marker="ar")
        y += h + 12
    s += box(70, y + 4, 760, 34, GREEN_BG, GREEN, 1.2, rx=7)
    s += txt(450, y + 21, "全部回扣 BIG IDEA：一切性质的根源 = 电子排布", 13,
             GREEN, "700")
    return wrap(s)


# ==================================================== Ch11 图 11-2
def fig_ch11_route():
    # 高度同样由内容算出：7 步 × 40 + 检查清单 160
    steps = ["给元素 → 查周期表 → 得 atomic number 原子序数",
             "原子序数 = 质子数 = 中性原子电子数",
             "按 2-8-8 画 Bohr 图 → 数最外层 → 得 价电子数",
             "价电子数 → 族 → 判断 失/得 电子 → 写 离子符号（含电荷）",
             "与另一元素的离子用 交叉法 配平总电荷 = 0 → 化学式",
             "判断类型（金属+非金属?）→ 选命名规则 → 英文名 + 中文名",
             "由类型预测 性质（熔沸点 / 导电性 / 状态）"]
    H = 64 + len(steps) * 40 + 8 + 160 + 24
    s = head(900, H, "图 11-2　「一条龙」解题路径｜The One-Stop Problem Route",
             "BC Science 9 · 七步固定顺序，跳步必错")
    s += ARROW_DEF
    y = 64
    for i, t in enumerate(steps):
        s += box(70, y, 760, 34, "#FFFFFF", BLUE if i in (2, 5) else EDGE,
                 1.0 if i in (2, 5) else 0.8, rx=6)
        s += badge(104, y + 17, 12, str(i + 1), BLUE_D, size=11)
        s += txt(126, y + 17, t, 12, INK, "600", "start")
        if i < len(steps) - 1:
            s += path(f"M450 {y + 34} L450 {y + 40}", LINE, 1.3)
        y += 40

    s += box(70, y + 8, 760, 160, NEUTRAL_BG, INK, 1.2, rx=8)
    s += txt(90, y + 30, "检查清单 Checklist（每题做完都过一遍）", 12.5, INK,
             "700", "start")
    checks = ["□ 符号大小写正确？（Co 钴 ≠ CO 一氧化碳）",
              "□ 化学式是否 最简比、总电荷为 0？",
              "□ 多变价金属有没有写 罗马数字？",
              "□ 英文命名：离子化合物没有前缀，分子化合物必须有？",
              "□ 中文命名顺序是不是「负在前、正在后」？",
              "□ 双原子分子（O₂ Cl₂ …）下标 2 写了没有？"]
    for k, c in enumerate(checks):
        s += txt(100, y + 52 + k * 19, c, 11, INK, "400", "start")
    return wrap(s)


# ==================================================== Ch11 图 11-3
def fig_ch11_decision_tree():
    s = head(900, 440, "图 11-3　化合物类型决策树｜Compound Decision Tree",
             "BC Science 9 · 先看元素种类，性质只是验证")
    s += ARROW_DEF
    s += box(340, 62, 220, 36, NEUTRAL_BG, LINE, 1.2, rx=8)
    s += txt(450, 80, "给定两种元素 / 一个化学式", 12.5, INK, "700")
    s += path("M450 98 L450 112", LINE, 1.5)
    s += box(280, 116, 340, 36, ORANGE_BG, ORANGE, 1.2, rx=8)
    s += txt(450, 134, "两种都是 NON-METAL 非金属吗？", 13, ORANGE_D, "700")
    s += path("M300 152 L300 178 L180 178 L180 196", GREEN, 1.6, marker="ar")
    s += path("M600 152 L600 178 L720 178 L720 196", BLUE, 1.6, marker="ar")
    s += txt(292, 172, "是", 11, GREEN, "700", "end")
    s += txt(608, 172, "否（至少一种是金属）", 11, BLUE_D, "700", "start")

    s += box(60, 200, 340, 40, GREEN_BG, GREEN, 1.3, rx=8)
    s += txt(230, 220, "MOLECULAR 分子化合物", 13.5, GREEN, "700")
    s += box(500, 200, 340, 40, BLUE_BG, BLUE, 1.3, rx=8)
    s += txt(670, 220, "IONIC 离子化合物", 13.5, BLUE_D, "700")
    for i, t in enumerate(["命名：前缀法", "CO₂ carbon dioxide 二氧化碳",
                           "低熔沸点 · 不导电", "例：H₂O　CH₄　NH₃　SO₂"]):
        s += txt(230, 254 + i * 20, t, 11.5, INK, "400")
    for i, t in enumerate(["命名：交叉法 + -ide",
                           "MgCl₂ magnesium chloride 氯化镁",
                           "高熔沸点 · 溶/熔导电",
                           "例：NaCl　CaCl₂　MgO　Al₂O₃"]):
        s += txt(670, 254 + i * 20, t, 11.5, INK, "400")

    s += box(60, 346, 780, 82, NEUTRAL_BG, EDGE, 1.0, rx=8)
    s += txt(80, 366, "反推题（给性质判类型）：", 12, INK, "700", "start")
    for i, t in enumerate(["熔点 801 ℃ + 水溶液导电 → IONIC",
                           "熔点 −78 ℃ + 不导电 → MOLECULAR",
                           "加热即分解 + 无导电性 → MOLECULAR（多为）"]):
        s += txt(100, 388 + i * 18, "· " + t, 11, INK, "400", "start")
    return wrap(s)


# ==================================================== Ch11 图 11-4 / 11-5
def _worked_example(title, note, sp_left, sp_right, steps, extra=None):
    """玻尔图并排 + 下方 STEP 文字，用于 Ch11 的「一条龙」示范题。"""
    pw = 430
    h = max(panel_h(len(sp_left["shells"])), panel_h(len(sp_right["shells"])))
    body_h = 30 + len(steps) * 20 + (30 + len(extra) * 19 if extra else 0)
    total = int(70 + h + 12 + body_h + 16)
    s = head(900, total, title, note)
    s += bohr_panel(14, 70, pw, sp_left, right_pad=84)[0]
    s += bohr_panel(456, 70, pw, sp_right, right_pad=84)[0]
    y = 70 + h + 22
    for t in steps:
        s += txt(70, y, t, 11.5, INK, "400", "start")
        y += 20
    if extra:
        y += 10
        s += box(60, y - 14, 780, 20 + len(extra) * 19, ORANGE_BG, ORANGE,
                 1.0, rx=7)
        for k, t in enumerate(extra):
            s += txt(78, y + k * 19, t, 11, ORANGE_D,
                     "700" if k == 0 else "400", "start")
    return wrap(s)


def fig_ch11_cacl2():
    ca = {"sym": "Ca", "cn": "钙", "z": 20, "shells": [2, 8, 8, 2], "a": 40}
    cl = {"sym": "Cl", "cn": "氯", "z": 17, "shells": [2, 8, 7], "a": 35}
    steps = [
        "STEP 1–2　Ca 原子序数 20 → 20 p⁺，20 e⁻；Cl 原子序数 17 → 17 p⁺，17 e⁻",
        "STEP 4　Ca 价电子少 → 失去 2 个 → Ca²⁺（cation）　Cl 价电子 7 → 得到 1 个 → Cl⁻（anion）",
        "STEP 5　交叉法：1 个 Ca²⁺(+2) 需 2 个 Cl⁻(−1×2 = −2)　→　化学式 = CaCl₂（下标 1 不写）",
        "STEP 6　金属 Ca + 非金属 Cl → IONIC　英文 calcium chloride（不加前缀）　中文 氯化钙",
        "STEP 7　白色晶体；熔点高（约 772 ℃）；硬而脆；易溶于水；固体不导电，溶于水或熔融时导电",
    ]
    return _worked_example(
        "图 11-4　一条龙示范 1：Ca 与 Cl｜Worked Example — Calcium + Chlorine",
        "BC Science 9 · 下标 2 不是猜的，是电荷逼出来的", ca, cl, steps)


def fig_ch11_al2o3():
    al = {"sym": "Al", "cn": "铝", "z": 13, "shells": [2, 8, 3], "a": 27}
    o = {"sym": "O", "cn": "氧", "z": 8, "shells": [2, 6], "a": 16}
    steps = [
        "STEP 1–2　Al 原子序数 13 → 13 p⁺，13 e⁻；O 原子序数 8 → 8 p⁺，8 e⁻",
        "STEP 4　Al → 失去 3 个 → Al³⁺（cation）　O → 得到 2 个 → O²⁻（anion）",
        "STEP 5　交叉法：Al³⁺ 与 O²⁻ 的最小公倍数是 6 → 2×(+3) = +6，3×(−2) = −6　→　Al₂O₃",
        "STEP 6　金属 + 非金属 → IONIC　英文 aluminium oxide（BC 拼写）　中文 氧化铝",
        "STEP 7　白色固体，熔点极高（约 2072 ℃），硬度大；不溶于水；固体不导电（熔融时可导电）",
        "　　　　天然形式为刚玉 corundum，含杂质时即红宝石 / 蓝宝石",
    ]
    extra = ["── 延伸：为什么铝制品耐腐蚀？────────────────────",
             "铝很活泼，表面立刻与 O₂ 反应生成一层致密且牢固的 Al₂O₃ 薄膜，隔绝内部铝与空气/水 → 不再继续被腐蚀。",
             "对比：铁生成的 Fe₂O₃·xH₂O 铁锈疏松多孔，会不断剥落，所以铁会一直锈穿，而铝不会。"]
    return _worked_example(
        "图 11-5　一条龙示范 2：Al 与 O｜Worked Example — Aluminium + Oxygen",
        "BC Science 9 · 电荷不整除 → 用最小公倍数", al, o, steps, extra)


def fig_ch11_co2():
    s = head(900, 452,
             "图 11-6　一条龙示范 3：C 与 O｜Worked Example — Carbon + Oxygen",
             "BC Science 9 · 都是非金属 → 只能共用，不能转移")
    s += box(50, 62, 800, 60, BLUE_BG, BLUE, 1.2, rx=8)
    s += txt(70, 82, "C (2, 4)　第 2 周期，第 14 族，价电子 = 4", 12, BLUE_D,
             "700", "start")
    s += txt(70, 102, "O (2, 6)　第 2 周期，第 16 族，价电子 = 6", 12, BLUE_D,
             "700", "start")
    s += txt(470, 92, "两者都是非金属 → 不转移电子，而是共用电子对（covalent bond 共价键）",
             11.5, INK, "600", "start")

    s += box(50, 134, 800, 62, GREEN_BG, GREEN, 1.2, rx=8)
    s += txt(70, 156, "CO  = carbon monoxide　中文：一氧化碳", 13, GREEN,
             "700", "start")
    s += txt(70, 178, "（第一个元素永不用 mono-；第二个元素必须加前缀 mono-）",
             11, INK, "400", "start")
    s += txt(560, 156, "CO₂ = carbon dioxide　中文：二氧化碳", 13, GREEN,
             "700", "start")

    s += txt(450, 218, "结构式（短线 = 共用电子对）", 12, INK, "700")
    s += txt(300, 254, "O", 20, INK, "700")
    s += txt(400, 254, "C", 20, INK, "700")
    s += txt(500, 254, "O", 20, INK, "700")
    s += path("M320 246 L372 246", INK, 2.2)
    s += path("M320 262 L372 262", INK, 2.2)
    s += path("M428 246 L480 246", INK, 2.2)
    s += path("M428 262 L480 262", INK, 2.2)
    s += txt(400, 286, "O＝C＝O", 13, SUB, "600")
    s += txt(700, 254, "C", 20, INK, "700")
    s += txt(790, 254, "O", 20, INK, "700")
    s += path("M720 248 L762 248", INK, 2.2)
    s += path("M720 254 L762 254", INK, 2.2)
    s += path("M720 260 L762 260", INK, 2.2)
    s += txt(745, 286, "C≡O", 13, SUB, "600")

    rows = [("常温状态", "气体", "固体晶体"),
            ("熔沸点", "极低（干冰 −78.5 ℃ 直接升华）", "极高（约 2072 ℃）"),
            ("导电性", "不导电", "熔融时导电"),
            ("作用力", "分子间作用力（弱）", "离子间静电作用（强）")]
    x0 = 70
    widths = [180, 290, 290]
    s += box(x0, 306, widths[0], 28, NEUTRAL_BG, EDGE, 0.8, rx=4)
    s += box(x0 + widths[0], 306, widths[1], 28, GREEN_BG, GREEN, 0.9, rx=4)
    s += box(x0 + widths[0] + widths[1], 306, widths[2], 28, BLUE_BG, BLUE,
             0.9, rx=4)
    s += txt(x0 + 10, 320, "", 11)
    s += txt(x0 + widths[0] / 2, 320, "", 11)
    s += txt(x0 + widths[0] + widths[1] / 2, 320, "CO₂（分子）", 11.5, GREEN,
             "700")
    s += txt(x0 + widths[0] + widths[1] + widths[2] / 2, 320, "Al₂O₃（离子）",
             11.5, BLUE_D, "700")
    for r, (a, b, c) in enumerate(rows):
        y = 334 + r * 28
        for i, v in enumerate([a, b, c]):
            cx = x0 + sum(widths[:i])
            s += box(cx, y, widths[i], 28, "#FFFFFF", EDGE, 0.8, rx=4)
            s += txt(cx + widths[i] / 2, y + 14, v, 11, INK, "400")

    s += box(50, 382, 800, 58, ORANGE_BG, ORANGE, 1.1, rx=8)
    s += txt(70, 400, "为什么差这么多？→ 根子仍在电子排布：", 12, ORANGE_D,
             "700", "start")
    s += txt(70, 420, "C 与 O 都不愿彻底交出电子 → 只能共用 → 独立小分子 → 分子间只有弱作用力 → 低沸点。",
             11, ORANGE_D, "400", "start")
    s += txt(70, 436, "Al 与 O 之间电子彻底转移 → 正负离子靠强静电作用堆成巨大晶体 → 极高熔点。",
             11, ORANGE_D, "400", "start")
    return wrap(s)


FIGURES = {
    "ch07-crisscross-method.svg": fig_ch07_crisscross,
    "ch07-reduce-ratio.svg": fig_ch07_reduce,
    "ch07-electron-transfer-mgf2.svg": fig_ch07_transfer,
    "ch07-naming-flowchart.svg": fig_ch07_naming_flow,
    "ch07-lattice-conductivity.svg": fig_ch07_lattice,
    "ch07-brackets.svg": fig_ch07_brackets,
    "ch07-main-chain.svg": fig_ch07_main_chain,
    "ch08-covalent-bond.svg": fig_ch08_covalent,
    "ch08-three-molecules.svg": fig_ch08_three_molecules,
    "ch08-bond-types.svg": fig_ch08_bond_types,
    "ch08-methane-model.svg": fig_ch08_methane,
    "ch08-naming-flowchart.svg": fig_ch08_naming_flow,
    "ch08-bond-strength.svg": fig_ch08_bond_strength,
    "ch08-judge-table.svg": fig_ch08_judge_table,
    "ch08-two-routes.svg": fig_ch08_main_chain,
    "ch09-evidence-of-change.svg": fig_ch09_evidence,
    "ch09-three-levels.svg": fig_ch09_three_levels,
    "ch09-sticker-balancing.svg": fig_ch09_stickers,
    "ch09-anatomy-formula.svg": fig_ch09_anatomy,
    "ch10-inquiry-cycle.svg": fig_ch10_cycle,
    "ch10-variables.svg": fig_ch10_variables,
    "ch10-whmis-pictograms.svg": fig_ch10_whmis,
    "ch10-table-and-graph.svg": fig_ch10_table_graph,
    "ch10-interpolation.svg": fig_ch10_interpolation,
    "ch11-master-flowchart.svg": fig_ch11_master,
    "ch11-one-stop-route.svg": fig_ch11_route,
    "ch11-decision-tree.svg": fig_ch11_decision_tree,
    "ch11-example-ca-cl.svg": fig_ch11_cacl2,
    "ch11-example-al-o.svg": fig_ch11_al2o3,
    "ch11-example-c-o.svg": fig_ch11_co2,
}


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    os.makedirs(FIG_DIR, exist_ok=True)
    for name, fn in FIGURES.items():
        if want and want not in name:
            continue
        with open(os.path.join(FIG_DIR, name), "w", encoding="utf-8") as fh:
            fh.write(fn())
        print("OK  " + name)


if __name__ == "__main__":
    main()
