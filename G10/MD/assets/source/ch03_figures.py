# -*- coding: utf-8 -*-
"""
Ch.3（Balancing Chemical Equations）配图生成器。

风格完全沿用 build_figure_svg_g10.py：900 宽、白底、标题 19pt、右上角小字注释、
圆角 rx=8、蓝 / 橙 / 绿 / 灰配色。

用法：
    python ch03_figures.py            # 全部生成
    python ch03_figures.py ch03-count # 只生成文件名含该关键字的图

输出目录：../figures/
改完必跑 check_svg_bounds.py 与 check_figures.py。
"""
import os
import sys

from build_figure_svg_g10 import (
    head, box, txt, path, ln, circ, wrap, ARROW_DEF, FIG_DIR,
    INK, SUB, LINE, EDGE,
    BLUE, BLUE_D, BLUE_BG,
    ORANGE, ORANGE_D, ORANGE_BG,
    GREEN, GREEN_BG, RED, NEUTRAL_BG,
)


# ================================================================ 图 3-1
def fig_ch03_four_steps():
    """配平四步法：四步横排 + 一个完整示范。"""
    w, H = 900, 340
    s = head(w, H, "Fig. 3-1　Four Steps to Balance｜配平四步法",
             "coefficients only｜只改系数")
    s += ARROW_DEF

    steps = [
        ("① Formulas｜化学式", BLUE_BG, BLUE, BLUE_D,
         "Write each formula correctly",
         "先写对全部化学式",
         "a wrong formula cannot be saved"),
        ("② Order｜顺序", ORANGE_BG, ORANGE, ORANGE_D,
         "metal → non-metal → H → O",
         "顺序：金属→非金属→H→O",
         "leave O and H for the end"),
        ("③ Groups｜原子团", GREEN_BG, GREEN, GREEN,
         "Keep SO₄ NO₃ PO₄ whole",
         "原子团当一个整体配",
         "never split them into atoms"),
        ("④ Finish｜收尾", NEUTRAL_BG, LINE, INK,
         "Fractions are allowed midway",
         "分数过渡，最后乘整数",
         "then multiply by the LCM"),
    ]

    bw, y0, bh = 196, 56, 120
    for i, (chip, bg, edge, col, l1, l2, l3) in enumerate(steps):
        x = 22 + i * 220
        s += box(x, y0, bw, bh, "#FFFFFF", EDGE, 1.0)
        s += box(x, y0, bw, 28, bg, edge, 1.1)
        s += txt(x + bw / 2, y0 + 14, chip, 10.5, col, "700")
        s += txt(x + bw / 2, y0 + 48, l1, 9.6, INK, "600")
        s += txt(x + bw / 2, y0 + 72, l2, 9.4, SUB)
        s += txt(x + bw / 2, y0 + 100, l3, 8.8, SUB)
        if i < 3:
            s += path(f"M{x + bw + 2} {y0 + 74} L{x + bw + 18} {y0 + 74}",
                      LINE, 1.4, "ar")

    ey = 192
    s += box(22, ey, 856, 70, "#FFFFFF", EDGE, 1.0)
    s += txt(40, ey + 20, "start｜起点", 9.5, SUB, "600", "start")
    s += txt(150, ey + 20, "CH₄ + O₂ → CO₂ + H₂O", 11, INK, "600", "start")
    s += txt(430, ey + 20, "not balanced yet｜尚未配平", 9.5, SUB, "400", "start")
    s += txt(40, ey + 50, "end｜终点", 9.5, GREEN, "600", "start")
    s += txt(150, ey + 50, "CH₄ + 2 O₂ → CO₂ + 2 H₂O", 12.5, GREEN, "700", "start")
    s += txt(470, ey + 50, "C 1=1 · H 4=4 · O 4=4 ✓", 10, SUB, "400", "start")

    ry = 278
    s += box(22, ry, 856, 46, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, ry + 16,
             "Only coefficients change — never subscripts｜只改系数，不改下标",
             11, RED, "700")
    s += txt(450, ry + 34,
             "every Science 10 balancing item can be pushed through these four steps"
             "｜所有题都能用这四步推出来", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 3-2
def fig_ch03_count_table():
    """原子计数验算表：CH₄ + 2 O₂ → CO₂ + 2 H₂O。"""
    w, H = 900, 404
    s = head(w, H, "Fig. 3-2　Atom Count Check｜原子计数验算表",
             "count both sides｜左右各数一遍")

    s += box(24, 54, 852, 64, BLUE_BG, BLUE, 1.1)
    s += txt(450, 82, "CH₄ + 2 O₂ → CO₂ + 2 H₂O", 20, INK, "700")
    s += txt(450, 105, "methane burns in oxygen｜甲烷在氧气中燃烧", 9.5, SUB)

    # 表头
    cols = [(24, 160, "Element｜元素"), (184, 280, "Left — reactants｜左（反应物）"),
            (464, 280, "Right — products｜右（生成物）"), (744, 132, "Equal?｜相等？")]
    s += box(24, 134, 852, 28, NEUTRAL_BG, LINE, 1.0)
    for x, cw, label in cols:
        s += ln(x, 134, x, 270, EDGE, 0.9)
        s += txt(x + cw / 2, 148, label, 9.8, SUB, "600")
    s += ln(876, 134, 876, 270, EDGE, 0.9)

    rows = [
        ("C", "1 CH₄ → 1 C", "1 CO₂ → 1 C", "✓ 1 = 1"),
        ("H", "1 CH₄ → 4 H", "2 H₂O → 4 H", "✓ 4 = 4"),
        ("O", "2 O₂ → 4 O", "CO₂ 2 + 2 H₂O 2 = 4 O", "✓ 4 = 4"),
    ]
    ry = 162
    for i, (el, left, right, eq) in enumerate(rows):
        bg = "#FFFFFF" if i % 2 == 0 else "#FBFAF5"
        s += box(24, ry, 852, 36, bg, EDGE, 0.8, 0)
        ln(876, ry, 876, ry + 36, EDGE, 0.9)
        s += txt(58, ry + 18, el, 13, BLUE_D, "700")
        s += txt(204, ry + 18, left, 10.5, INK, "400", "start")
        s += txt(484, ry + 18, right, 10.5, INK, "400", "start")
        s += txt(810, ry + 18, eq, 10.5, GREEN, "700")
        ry += 36

    s += box(24, 282, 852, 52, "#FFFFFF", GREEN, 1.1)
    s += txt(450, 300, "All three elements match → the equation is balanced｜三种元素左右全等 = 配平完成",
             11, GREEN, "700")
    s += txt(450, 320, "If one row differs, change one coefficient and count the whole table again"
                      "｜差一行就改系数、整表重数", 9.5, SUB)

    s += box(24, 346, 852, 44, "#FFFFFF", RED, 1.1)
    s += txt(450, 362, "⛔ Never fix a mismatch by editing a subscript — that creates a different substance",
             10.2, RED, "600")
    s += txt(450, 379, "下标是化学式的一部分，改了下标就不是原来的物质了", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 3-3
def fig_ch03_combustion_order():
    """燃烧配平口诀：C → H → O，用 C₃H₈ 走一遍。"""
    w, H = 900, 390
    s = head(w, H, "Fig. 3-3　Combustion Order: C → H → O｜燃烧配平口诀",
             "C → H → O, always｜口诀顺序")
    s += ARROW_DEF

    cards = [
        (24, "① Carbon 先配碳", BLUE_BG, BLUE, BLUE_D,
         "Balance C with CO₂", "先给 CO₂ 定数，把 C 配平", "C₃H₈ → 3 CO₂"),
        (314, "② Hydrogen 再配氢", ORANGE_BG, ORANGE, ORANGE_D,
         "Balance H with H₂O", "再用 H₂O 把 H 配平", "C₃H₈ → 4 H₂O"),
        (604, "③ Oxygen 最后氧", GREEN_BG, GREEN, GREEN,
         "Count O on the right", "右边的 O 总数 ÷ 2 就是 O₂", "3×2 + 4 = 10 → 5 O₂"),
    ]
    y0, bh = 56, 156
    for x, chip, bg, edge, col, l1, l2, ex in cards:
        s += box(x, y0, 272, bh, "#FFFFFF", EDGE, 1.0)
        s += box(x, y0, 272, 30, bg, edge, 1.1)
        s += txt(x + 136, y0 + 15, chip, 11, col, "700")
        s += txt(x + 136, y0 + 56, l1, 10.2, INK, "600")
        s += txt(x + 136, y0 + 78, l2, 9.4, SUB)
        s += ln(x + 24, y0 + 96, x + 248, y0 + 96, EDGE, 0.9)
        s += txt(x + 136, y0 + 122, ex, 12, col, "700")

    for x in (296, 586):
        s += path(f"M{x} {y0 + 78} L{x + 14} {y0 + 78}", LINE, 1.4, "ar")

    s += box(24, 228, 852, 76, "#FFFFFF", EDGE, 1.0)
    s += txt(450, 250, "C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O", 19, INK, "700")
    s += txt(450, 274, "check｜验算   C 3 = 3　·　H 8 = 8　·　O 10 = 10 ✓", 10.2, GREEN, "600")
    s += txt(450, 293, "propane 丙烷 — a fuel with only C and H｜只含 C、H 的燃料", 9.3, SUB)

    s += box(24, 318, 852, 56, ORANGE_BG, ORANGE, 1.1)
    s += txt(450, 336, "If O is odd, double every coefficient at the end｜O 配成单数就整体 ×2",
             10.5, ORANGE_D, "700")
    s += txt(450, 356,
             "C₂H₂ + O₂ → 2 CO₂ + H₂O leaves 5 O on the right → multiply all by 2"
             "｜C₂H₂ 配平会剩下 5 个 O，整体乘 2 得 2 C₂H₂ + 5 O₂ → 4 CO₂ + 2 H₂O", 9.2, SUB)
    return wrap(s)


# ================================================================ 图 3-4
def fig_ch03_errors():
    """四类典型配平错误：改下标 / 漏双原子 / 未约简 / 拆原子团。"""
    w, H = 900, 366
    s = head(w, H, "Fig. 3-4　Four Classic Balancing Errors｜四类典型配平错误",
             "all cost marks｜都是丢分点")

    cards = [
        ("① Changing a subscript｜改下标", "✗  H₂ + O₂ → H₂O₂",
         "that is hydrogen peroxide, a different substance", "✓  2 H₂ + O₂ → 2 H₂O"),
        ("② Forgetting a diatomic element｜漏写双原子", "✗  H₂ + O → H₂O",
         "elemental oxygen is O₂, never O", "✓  2 H₂ + O₂ → 2 H₂O"),
        ("③ Not reducing to lowest terms｜未约简", "✗  4 H₂ + 2 O₂ → 4 H₂O",
         "divide every coefficient by 2", "✓  2 H₂ + O₂ → 2 H₂O"),
        ("④ Splitting a polyatomic group｜拆原子团", "✗  3 CaOH₂ + 2 H₃PO₄",
         "the brackets belong to the group: Ca(OH)₂", "✓  3 Ca(OH)₂ + 2 H₃PO₄ → Ca₃(PO₄)₂ + 6 H₂O"),
    ]

    for i, (title, wrong, why, right) in enumerate(cards):
        x = 24 if i % 2 == 0 else 456
        y = 54 if i < 2 else 176
        s += box(x, y, 420, 112, "#FFFFFF", EDGE, 1.0)
        s += txt(x + 16, y + 20, title, 10.8, INK, "700", "start")
        s += txt(x + 16, y + 46, wrong, 11.5, RED, "700", "start")
        s += txt(x + 16, y + 66, why, 9, SUB, "400", "start")
        s += txt(x + 16, y + 94, right, 11.2 if i == 3 else 12, GREEN, "700", "start")

    s += box(24, 300, 852, 46, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 317, "Every error above is checkable in 30 seconds with the count table (Fig. 3-2)",
             10.5, INK, "600")
    s += txt(450, 336, "上面四类错误，用 Fig. 3-2 的计数表 30 秒就能查出来", 9.5, SUB)
    return wrap(s)


# ================================================================ 注册表
FIGURES = {
    "ch03-four-steps": fig_ch03_four_steps,
    "ch03-count-table": fig_ch03_count_table,
    "ch03-combustion-order": fig_ch03_combustion_order,
    "ch03-balancing-errors": fig_ch03_errors,
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
