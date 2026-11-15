# -*- coding: utf-8 -*-
"""
Ch.7（酸、碱、盐与 pH）配图脚本，风格与 build_figure_svg_g10.py 完全一致。

用法：
    python ch07_figures.py            # 全部生成
    python ch07_figures.py ch07       # 只生成文件名含 ch07 的图
    python ch07_figures.py ph         # 只生成文件名含 ph 的图

输出目录：../figures/（与主脚本同目录，FIG_DIR 复用）
"""
import os
import sys

from build_figure_svg_g10 import (
    head, box, txt, path, ln, circ, wrap, ARROW_DEF,
    FIG_DIR, INK, SUB, LINE, EDGE,
    BLUE, BLUE_D, BLUE_BG, ORANGE, ORANGE_D, ORANGE_BG,
    GREEN, GREEN_BG, RED, NEUTRAL_BG,
)


def tw(s, fs):
    """与 check_figures.py 同口径的宽度估算：CJK 1.0em，其余 0.55em。"""
    w = 0.0
    for ch in s:
        w += fs * (1.0 if 0x2E80 <= ord(ch) <= 0xFFEF else 0.55)
    return w


def tw_eq(s, fs):
    """方程式排版用的更精细估算：空格 0.28em、箭头 0.75em。"""
    w = 0.0
    for ch in s:
        o = ord(ch)
        if ch == " ":
            w += fs * 0.28
        elif o == 0x2192:
            w += fs * 0.75
        else:
            w += fs * (1.0 if 0x2E80 <= o <= 0xFFEF else 0.55)
    return w


# ================================================================ 图 7-1
def fig_ch07_ph_scale():
    """pH 标度 0–14：色带 + 家用物质定位 + 每格 10 倍。"""
    w, H = 900, 436
    s = head(w, H, "Fig. 7-1　The pH Scale 0–14｜pH 标度 0–14",
             "each step = 10×｜每差 1 等于 10 倍")

    x0, cw = 40.0, 54.6667
    ax1 = x0 + 7 * cw          # 0–6 结束
    ax2 = ax1 + cw             # pH 7 结束

    # ---- 分区条
    s += box(x0, 50, ax1 - x0, 26, "#F7E3E3", RED, 1.1)
    s += txt(x0 + (ax1 - x0) / 2, 63, "ACID — pH 0 to 6｜酸", 10.5, RED, "700")
    s += box(ax1, 50, cw, 26, GREEN_BG, GREEN, 1.1)
    s += txt(ax1 + cw / 2, 59, "NEUTRAL", 7.5, GREEN, "700")
    s += txt(ax1 + cw / 2, 71, "中性 7", 7.5, GREEN, "700")
    s += box(ax2, 50, x0 + 15 * cw - ax2, 26, BLUE_BG, BLUE, 1.1)
    s += txt(ax2 + (x0 + 15 * cw - ax2) / 2, 63, "BASE — pH 8 to 14｜碱",
             10.5, BLUE_D, "700")

    # ---- 15 个 pH 格
    fills = ["#8C2020", "#A32D2D", "#B84A3A", "#C96B4A", "#D98E55",
             "#E0A868", "#E7C083", "#8FB86A", "#8FC0D8", "#6FA8C8",
             "#4F8FBA", "#2F76A8", "#185FA5", "#0C447C", "#08325C"]
    for i in range(15):
        x = x0 + i * cw
        s += box(x, 100, cw, 58, fills[i], fills[i], 0.8, rx=0)
        s += txt(x + cw / 2, 86, str(i), 12, INK, "700")
    s += box(x0, 100, 15 * cw, 58, "none", LINE, 1.0, rx=0)

    # ---- 家用物质标注
    items = [(1, "battery acid", "电池酸液", 0),
             (2, "lemon juice", "柠檬汁", 1),
             (3, "vinegar", "食醋", 0),
             (7, "pure water", "纯水", 0),
             (9, "baking soda", "小苏打溶液", 0),
             (10, "soap", "肥皂水", 1),
             (13, "drain cleaner", "管道清洁剂", 0)]
    for ph, en, cn, lvl in items:
        cx = x0 + (ph + 0.5) * cw
        cy = 176 if lvl == 0 else 224
        s += ln(cx, 158, cx, cy, LINE, 1.0)
        s += circ(cx, 158, 2.4, INK, INK, 0)
        s += box(cx - 50, cy, 100, 40, "#FFFFFF", EDGE, 1.0, rx=6)
        s += txt(cx, cy + 14, en, 9.5, INK, "700")
        s += txt(cx, cy + 29, "pH %d｜%s" % (ph, cn), 9, SUB)

    # ---- 10 倍规则
    s += box(24, 280, 852, 64, BLUE_BG, BLUE, 1.1)
    s += txt(450, 298,
             "Every step of 1 on the scale = a 10-fold change in acidity"
             "｜标度上每差 1 格，酸性相差 10 倍", 12, BLUE_D, "700")
    s += txt(450, 318,
             "pH 3 is 10× more acidic than pH 4, and 100× more acidic than pH 5"
             "｜pH 3 比 pH 4 酸 10 倍，比 pH 5 酸 100 倍", 10, INK)
    s += txt(450, 334,
             "So pH 2 is not a little more acidic than pH 5 — it is 1000 times"
             "｜pH 2 不是「稍酸」，它是 pH 5 的 1000 倍", 10, SUB)

    # ---- 适用边界
    s += box(24, 356, 852, 68, "#FFFFFF", RED, 1.1)
    s += txt(450, 376,
             "pH describes aqueous solutions only — a dry acid powder has no pH"
             "｜pH 只描述水溶液，干燥的酸粉没有 pH", 11, RED, "700")
    s += txt(450, 396,
             "Never taste a chemical: 'sour' and 'bitter' are descriptions, not tests"
             "｜味道是描述，不是检验方法", 10, INK)
    s += txt(450, 414,
             "In the lab the tests are litmus, universal indicator or a pH meter"
             "｜实验室只用石蕊、通用指示剂或 pH 计", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 7-2
def fig_ch07_acid_vs_base():
    """酸 vs 碱：六项检验并列对照。"""
    w, H = 900, 452
    s = head(w, H, "Fig. 7-2　Acid vs Base: Six Tests｜酸与碱的六项对照",
             "same tests, opposite results｜结果相反")

    lx, lw = 40, 200
    ax, aw = 252, 296
    bx, bw = 560, 300

    s += box(lx, 52, lw, 34, NEUTRAL_BG, LINE, 1.0)
    s += txt(lx + lw / 2, 69, "Test｜检验项目", 10.5, INK, "700")
    s += box(ax, 52, aw, 34, BLUE_BG, BLUE, 1.1)
    s += txt(ax + aw / 2, 69, "ACID｜酸", 13, BLUE_D, "700")
    s += box(bx, 52, bw, 34, ORANGE_BG, ORANGE, 1.1)
    s += txt(bx + bw / 2, 69, "BASE｜碱", 13, ORANGE_D, "700")

    rows = [
        ("Taste", "味道", "sour — lemon, vinegar｜酸", "bitter — soap, tonic water｜苦"),
        ("Litmus paper", "石蕊试纸",
         "turns BLUE litmus RED｜蓝石蕊变红", "turns RED litmus BLUE｜红石蕊变蓝"),
        ("pH value", "pH 值", "less than 7（0–6）｜小于 7", "more than 7（8–14）｜大于 7"),
        ("With active metal", "与活泼金属",
         "gives H₂ — bubbles form｜放出 H₂ 冒泡", "no reaction for most metals｜多数不反应"),
        ("With carbonate", "与碳酸盐",
         "gives CO₂ — fizzes｜放出 CO₂ 冒泡", "no reaction for most carbonates｜多数不反应"),
        ("Corrosive?", "腐蚀性",
         "yes — strong acids burn skin｜会", "yes — NaOH burns skin too｜也会"),
    ]
    y0, rh = 92, 46
    for i, (en, cn, atxt, btxt) in enumerate(rows):
        y = y0 + i * rh
        s += box(lx, y, lw, rh, NEUTRAL_BG, EDGE, 1.0)
        s += txt(lx + lw / 2, y + 17, en, 10.5, INK, "700")
        s += txt(lx + lw / 2, y + 32, cn, 9, SUB)
        s += box(ax, y, aw, rh, "#FFFFFF", EDGE, 1.0)
        s += txt(ax + aw / 2, y + rh / 2, atxt, 10.5, BLUE_D)
        s += box(bx, y, bw, rh, "#FFFFFF", EDGE, 1.0)
        s += txt(bx + bw / 2, y + rh / 2, btxt, 10.5, ORANGE_D)

    s += box(24, 382, 852, 58, "#FFFFFF", RED, 1.1)
    s += txt(450, 400,
             "Both columns are corrosive — 'base' does not mean 'safe'"
             "｜两栏都有腐蚀性：碱 ≠ 安全", 11, RED, "700")
    s += txt(450, 420,
             "Two different fizzes: acid + metal gives H₂, acid + carbonate gives CO₂"
             "｜两种气泡别混：金属放 H₂、碳酸盐放 CO₂", 10, INK)
    return wrap(s)


# ================================================================ 图 7-3
def fig_ch07_indicators():
    """指示剂颜色卡：四种指示剂 × 酸性 / 中性 / 碱性。"""
    w, H = 900, 428
    s = head(w, H, "Fig. 7-3　Indicator Colours｜指示剂颜色卡",
             "colour is the signal｜看颜色下结论")

    lx, lw = 40, 260
    cols = [(300, "Acid｜酸性", BLUE_BG, BLUE, BLUE_D),
            (486, "Neutral｜中性", GREEN_BG, GREEN, GREEN),
            (672, "Base｜碱性", ORANGE_BG, ORANGE, ORANGE_D)]
    s += box(lx, 52, lw, 32, NEUTRAL_BG, LINE, 1.0)
    s += txt(lx + lw / 2, 68, "Indicator｜指示剂", 10.5, INK, "700")
    for x, label, bg, eg, col in cols:
        s += box(x, 52, 180, 32, bg, eg, 1.1)
        s += txt(x + 90, 68, label, 11.5, col, "700")

    rows = [
        ("Litmus", "石蕊", "red / blue paper｜红蓝试纸", [
            ("#B23A3A", "red 红", "#B23A3A"),
            ("#7B5EA7", "purple 紫", "#7B5EA7"),
            ("#1F5FA5", "blue 蓝", "#1F5FA5")]),
        ("Phenolphthalein", "酚酞", "colourless solution｜无色溶液", [
            ("#FFFFFF", "colourless 无色", EDGE),
            ("#FFFFFF", "colourless 无色", EDGE),
            ("#E06A9B", "pink 粉红", "#E06A9B")]),
        ("Bromothymol blue", "溴百里酚蓝", "BTB solution｜BTB 溶液", [
            ("#D4B23C", "yellow 黄", "#D4B23C"),
            ("#4E9A51", "green 绿", "#4E9A51"),
            ("#1F5FA5", "blue 蓝", "#1F5FA5")]),
        ("Universal indicator", "通用指示剂", "paper or solution｜试纸 / 溶液", [
            ("#C0504D", "red to orange 红至橙", "#C0504D"),
            ("#4E9A51", "green 绿", "#4E9A51"),
            ("#4B3F8F", "blue to purple 蓝紫", "#4B3F8F")]),
        ("pH meter", "pH 计", "electronic reading｜电子读数", [
            ("#F1EFE8", "reads 2 to 6 读数 2–6", LINE),
            ("#F1EFE8", "reads 7 读数 7", LINE),
            ("#F1EFE8", "reads 8 to 13 读数 8–13", LINE)]),
    ]

    y0, rh = 88, 54
    for i, (en, cn, sub, cells) in enumerate(rows):
        y = y0 + i * rh
        s += box(lx, y, lw, rh, NEUTRAL_BG, EDGE, 1.0)
        s += txt(lx + 14, y + 18, en, 10.5, INK, "700", anchor="start")
        s += txt(lx + 14, y + 34, sub, 8.5, SUB, anchor="start")
        for j, (x, _, _, _, _) in enumerate(cols):
            fill, label, edge = cells[j]
            s += box(x, y, 180, rh, "#FFFFFF", EDGE, 1.0)
            s += box(x + 12, y + 14, 26, 26, fill, edge, 1.0, rx=4)
            s += txt(x + 46, y + rh / 2, label, 9.5, INK, anchor="start")

    s += box(24, 370, 852, 46, "#FFFFFF", RED, 1.1)
    s += txt(450, 385,
             "Phenolphthalein stays colourless in acid AND in neutral solution —"
             " pink means base only｜酚酞在酸性和中性都无色，粉红只代表碱", 10.5, RED, "700")
    s += txt(450, 404,
             "Universal indicator covers the whole scale; a pH meter gives a number, not a colour"
             "｜通用指示剂覆盖全程，pH 计给数字不给颜色", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 7-4
def fig_ch07_neutralization():
    """中和反应解剖：分子方程式 + 离子层面 H⁺ + OH⁻ → H₂O + 旁观离子。"""
    w, H = 900, 458
    s = head(w, H, "Fig. 7-4　Neutralization Anatomy｜中和反应解剖",
             "H⁺ + OH⁻ → H₂O｜本质就这一步")

    # ---- 分子方程式：单一 text + 字母基线（避免符号用 central 基线时 + / → 飘高、与相邻词重叠）
    s += box(24, 50, 852, 56, "#FFFFFF", EDGE, 1.0)
    eq = "HCl + NaOH → NaCl + H₂O"
    fs = 21
    total = tw_eq(eq, fs)
    x0 = 450 - total / 2
    s += txt(450, 84, eq, fs, INK, "700", baseline="alphabetic")
    marks = {"HCl": ("acid｜酸", BLUE_D), "NaOH": ("base｜碱", ORANGE_D),
             "NaCl": ("salt｜盐", GREEN), "H₂O": ("water｜水", BLUE_D)}
    for word, (label, col) in marks.items():
        pre = eq.split(word)[0]
        wx = x0 + tw_eq(pre, fs)
        s += txt(wx + tw_eq(word, fs) / 2, 98, label, 9, col, "700")

    # ---- 左：反应物离子
    s += box(24, 120, 320, 180, "#FFFFFF", EDGE, 1.0)
    s += txt(184, 138, "Reactant ions｜反应物离子", 10.5, BLUE_D, "700")
    s += circ(86, 182, 20, BLUE_BG, BLUE)
    s += txt(86, 182, "H⁺", 12, BLUE_D, "700")
    s += circ(150, 182, 20, BLUE_BG, BLUE)
    s += txt(150, 182, "Cl⁻", 12, BLUE_D, "700")
    s += txt(236, 182, "from HCl｜来自盐酸", 8.5, SUB, anchor="start")
    s += circ(86, 244, 20, ORANGE_BG, ORANGE)
    s += txt(86, 244, "Na⁺", 11, ORANGE_D, "700")
    s += circ(150, 244, 20, ORANGE_BG, ORANGE)
    s += txt(150, 244, "OH⁻", 11, ORANGE_D, "700")
    s += txt(236, 244, "from NaOH｜来自氢氧化钠", 8.5, SUB, anchor="start")
    s += txt(184, 286, "four ions floating in water｜四种离子都在水里", 8.5, SUB)

    # ---- 中：净变化
    s += box(356, 120, 170, 180, BLUE_BG, BLUE, 1.1)
    s += txt(441, 138, "Net change｜净变化", 10, BLUE_D, "700")
    s += txt(441, 178, "H⁺ + OH⁻", 12, BLUE_D, "700")
    s += txt(441, 206, "→", 16, LINE, "700")
    s += txt(441, 234, "H₂O", 14, GREEN, "700")
    s += txt(441, 268, "the only real step｜唯一真正发生的一步", 8, INK)
    s += txt(441, 284, "the rest just watch｜其余只是旁观", 8, SUB)

    # ---- 右：生成物离子
    s += box(538, 120, 322, 180, "#FFFFFF", EDGE, 1.0)
    s += txt(699, 138, "Product ions｜生成物离子", 10.5, GREEN, "700")
    s += circ(624, 182, 20, ORANGE_BG, ORANGE)
    s += txt(624, 182, "Na⁺", 11, ORANGE_D, "700")
    s += circ(688, 182, 20, BLUE_BG, BLUE)
    s += txt(688, 182, "Cl⁻", 12, BLUE_D, "700")
    s += txt(774, 182, "spectators｜旁观", 8.5, SUB, anchor="start")
    s += circ(624, 250, 24, GREEN_BG, GREEN)
    s += txt(624, 250, "H₂O", 11, GREEN, "700")
    s += txt(699, 250, "water｜水", 9, GREEN, anchor="start")
    s += txt(699, 286, "Na⁺ and Cl⁻ become the salt｜Na⁺ 与 Cl⁻ 就是盐", 8.5, SUB)

    # ---- 结论
    s += box(24, 316, 852, 56, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 336,
             "acid + base → salt + water; the water comes only from H⁺ + OH⁻"
             "｜酸 + 碱 → 盐 + 水，水只来自 H⁺ + OH⁻", 11, INK, "700")
    s += txt(450, 356,
             "The salt is whatever ions are left over: Na⁺ + Cl⁻ → NaCl"
             "｜盐就是剩下的那对离子：Na⁺ + Cl⁻ → NaCl", 10, SUB)

    # ---- 第二个例子 + 配平验算
    s += box(24, 384, 852, 62, "#FFFFFF", ORANGE, 1.1)
    s += txt(450, 403,
             "A base with two OH⁻ needs two acids:  2 HCl + Ca(OH)₂ → CaCl₂ + 2 H₂O",
             11, ORANGE_D, "700")
    s += txt(450, 424,
             "Check: H 4 = 4 · Cl 2 = 2 · Ca 1 = 1 · O 2 = 2 ✓ — two hydroxides, two waters"
             "｜两个 OH⁻ 就生成两个水", 9.5, INK)
    return wrap(s)


# ================================================================ 注册表
FIGURES = {
    "ch07-ph-scale": fig_ch07_ph_scale,
    "ch07-acid-vs-base": fig_ch07_acid_vs_base,
    "ch07-indicator-colours": fig_ch07_indicators,
    "ch07-neutralization": fig_ch07_neutralization,
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
