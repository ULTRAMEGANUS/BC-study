# -*- coding: utf-8 -*-
"""
Ch.4（质量守恒定律）配图脚本，风格与 build_figure_svg_g10.py 完全一致。

用法：
    python ch04_figures.py            # 全部生成
    python ch04_figures.py ch04       # 只生成文件名含 ch04 的图

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


# ================================================================ 图 4-1
def fig_ch04_atom_ledger():
    """质量守恒的原子层面解释：2 H₂ + O₂ → 2 H₂O 原子台账。"""
    w, H = 900, 372
    s = head(w, H, "Fig. 4-1　Atom Ledger Before vs After｜反应前后原子台账",
             "count atoms, not grams｜数原子不数克")

    # ---- 方程式条
    s += box(24, 56, 852, 60, BLUE_BG, BLUE, 1.1)
    s += txt(450, 94, "2 H₂ + O₂  →  2 H₂O", 20, BLUE_D, "700")

    # ---- 台账表头
    cols = [(80, 240, "Element｜元素"), (320, 150, "Before｜反应前"),
            (470, 150, "After｜反应后"), (620, 200, "Same?｜是否相同")]
    hy, hh = 132, 28
    for x, cw, label in cols:
        s += box(x, hy, cw, hh, NEUTRAL_BG, LINE, 1.0)
        s += txt(x + cw / 2, hy + 14, label, 11.5, INK, "700")

    # ---- 台账两行
    rows = [("H｜氢", "4", "4", "✓ unchanged 不变"),
            ("O｜氧", "2", "2", "✓ unchanged 不变")]
    ry, rh = 160, 40
    for i, (el, b, a, same) in enumerate(rows):
        y = ry + i * rh
        s += box(80, y, 240, rh, "#FFFFFF", EDGE, 1.0)
        s += txt(200, y + rh / 2, el, 13, INK, "700")
        s += box(320, y, 150, rh, "#FFFFFF", EDGE, 1.0)
        s += txt(395, y + rh / 2, b, 15, BLUE_D, "700")
        s += box(470, y, 150, rh, "#FFFFFF", EDGE, 1.0)
        s += txt(545, y + rh / 2, a, 15, ORANGE_D, "700")
        s += box(620, y, 200, rh, "#FFFFFF", EDGE, 1.0)
        s += txt(720, y + rh / 2, same, 11.5, GREEN, "600")

    # ---- 质量结论
    ty = 252
    s += box(80, ty, 740, 36, GREEN_BG, GREEN, 1.1)
    s += txt(450, ty + 18,
             "Total mass before = Total mass after｜反应前总质量 = 反应后总质量",
             12.5, GREEN, "700")

    # ---- 底部注记
    s += box(24, 300, 852, 62, "#FFFFFF", EDGE, 1.0)
    s += txt(450, 320,
             "Atoms are only rearranged — kind, number and mass of atoms never change"
             "｜原子只是重排：种类、数目、单个原子质量三不变", 11, INK, "600")
    s += txt(450, 340,
             "Balancing an equation (Ch.3) is exactly this ledger check in symbols"
             "｜Ch.3 的配平验算就是用符号核对这本台账", 10, SUB)
    s += txt(450, 356,
             "So mass cannot change in a chemical reaction｜所以化学反应中质量必然不变", 10, SUB)
    return wrap(s)


# ================================================================ 图 4-2
def fig_ch04_open_closed():
    """开放 vs 封闭体系：镁条燃烧质量逸散 vs 密闭锥形瓶 + 气球。"""
    w, H = 900, 400
    s = head(w, H, "Fig. 4-2　Open vs Closed Systems｜敞开与封闭体系",
             "the balance sees the boundary｜天平只认边界")
    s += ARROW_DEF

    # ---- 左面板：开放体系
    s += box(24, 56, 414, 32, ORANGE_BG, ORANGE, 1.1)
    s += txt(231, 72, "OPEN SYSTEM｜敞开体系", 12, ORANGE_D, "700")
    # 开放边界（顶部开口，虚线）
    s += ln(64, 200, 64, 108, ORANGE, 1.4, dash="5 4")
    s += ln(64, 108, 160, 108, ORANGE, 1.4, dash="5 4")
    s += ln(302, 108, 398, 108, ORANGE, 1.4, dash="5 4")
    s += ln(398, 108, 398, 200, ORANGE, 1.4, dash="5 4")
    s += ln(64, 200, 398, 200, ORANGE, 1.4, dash="5 4")
    # 白烟（缺口上方的小圈）
    for dx, dy, r in ((180, 100, 6), (231, 96, 8), (282, 100, 6)):
        s += circ(dx, dy, r, "#FFFFFF", LINE, 1.0)
    s += txt(231, 125, "gap — smoke escapes｜顶部开口，烟逸出", 9.5, SUB)
    # 镁条 + 火焰
    s += box(200, 200, 62, 10, NEUTRAL_BG, INK, 1.0, rx=4)
    s += txt(322, 207, "Mg ribbon｜镁条", 9, SUB)
    s += path("M231 192 L223 178 L231 184 L239 170 L243 182 L247 174 L243 192 Z",
              ORANGE_D, 1.2)
    # 天平托盘
    s += ln(140, 214, 322, 214, LINE, 2.0)
    s += box(216, 214, 30, 26, "#FFFFFF", LINE, 1.2)
    s += box(186, 240, 90, 12, LINE, LINE, 1.2, rx=4)
    s += txt(231, 258, "reading changes｜读数会变", 10.5, RED, "700")
    # 面板结论
    s += box(24, 276, 414, 76, "#FFFFFF", ORANGE, 1.0)
    s += txt(231, 296, "Mg ribbon burns: white smoke (MgO) escapes｜镁条燃烧白烟逸出",
             10, INK)
    s += txt(231, 316, "escaped mass = lost mass on the balance｜逸散质量 = 读数减少量",
             10, INK)
    s += txt(231, 336, "law still holds — matter just left｜守恒仍成立，物质只是离开了",
             10, SUB)

    # ---- 右面板：封闭体系
    s += box(462, 56, 414, 32, BLUE_BG, BLUE, 1.1)
    s += txt(669, 72, "CLOSED SYSTEM｜封闭体系", 12, BLUE_D, "700")
    # 封闭边界（完整虚线框）
    s += box(502, 92, 334, 148, "#FFFFFF", BLUE, 1.1, rx=10)
    # 锥形瓶：瓶身三角 + 瓶颈
    s += path("M657 150 L657 172 L625 216 L713 216 L681 172 L681 150 Z",
              BLUE_D, 1.6)
    s += ln(657, 150, 681, 150, BLUE_D, 1.6)
    s += txt(669, 205, "solution｜反应液", 8.5, SUB)
    # 气球（密封在瓶口上方）
    s += circ(669, 118, 20, BLUE_BG, BLUE_D, 1.4)
    s += ln(663, 138, 663, 150, BLUE_D, 1.2)
    s += ln(675, 138, 675, 150, BLUE_D, 1.2)
    s += txt(560, 130, "balloon inflates", 9.5, BLUE_D, "600")
    s += txt(560, 146, "inside the seal｜气球在密封内鼓起", 9, SUB)
    # 天平托盘
    s += ln(580, 252, 758, 252, LINE, 2.0)
    s += box(654, 240, 30, 12, "#FFFFFF", LINE, 1.2)
    s += box(624, 264, 90, 12, LINE, LINE, 1.2, rx=4)
    s += txt(669, 288, "reading unchanged｜读数不变", 10.5, GREEN, "700")
    # 面板结论
    s += box(462, 276, 414, 76, "#FFFFFF", BLUE, 1.0)
    s += txt(669, 296, "NaHCO₃ + CH₃COOH in a sealed flask｜密闭锥形瓶内反应产气",
             10, INK)
    s += txt(669, 316, "gas stays inside — boundary crossed by nothing｜气体留在边界内",
             10, INK)
    s += txt(669, 336, "before reading = after reading｜反应前后读数相等", 10, SUB)

    # ---- 底部规则条
    s += box(24, 366, 852, 24, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 383,
             "Conservation never fails — only what the balance can see changes｜守恒从不失效，变的只是天平能看见的部分",
             10.5, INK, "600")
    return wrap(s)


# ================================================================ 图 4-3
def fig_ch04_apparent_mass():
    """表观质量变化三卡：生锈变重 / 燃烧变轻 / 密闭不变。"""
    w, H = 900, 400
    s = head(w, H, "Fig. 4-3　Why the Balance Seems to Lie｜表观质量变化三卡",
             "law intact, boundary differs｜定律没破，边界不同")

    cards = [
        (24, "① Rusting — heavier｜生锈变重", ORANGE_BG, ORANGE, ORANGE_D,
         [("steel wool 5.00 g → 6.35 g", INK),
          ("gain = 6.35 − 5.00 = 1.35 g", ORANGE_D),
          ("O₂ from the air joins the iron", INK),
          ("氧气从空气进入固体", SUB)]),
        (314, "② Burning — lighter｜燃烧变轻", "#F7E3E3", RED, RED,
         [("wood 250.0 g → ash 12.0 g", INK),
          ("lost = 250.0 − 12.0 = 238.0 g", RED),
          ("CO₂ and smoke escape upward", INK),
          ("气体与烟逸出，天平看不见", SUB)]),
        (604, "③ Sealed — unchanged｜密闭不变", GREEN_BG, GREEN, GREEN,
         [("flask before = after = 189.55 g", INK),
          ("difference = 189.55 − 189.55 = 0 g", GREEN),
          ("gas made but stays inside", INK),
          ("气体留在边界内，谁也出不去", SUB)]),
    ]
    for x, title, bg, edge, col, lines in cards:
        s += box(x, 58, 272, 32, bg, edge, 1.1)
        s += txt(x + 136, 74, title, 11.5, col, "700")
        s += box(x, 90, 272, 130, "#FFFFFF", EDGE, 1.0)
        yy = 114
        for text, color in lines:
            s += txt(x + 136, yy, text, 10, color)
            yy += 22

    # ---- 决策条
    s += box(24, 240, 852, 62, BLUE_BG, BLUE, 1.1)
    s += txt(450, 262, "First question: is the system open or closed?｜先问一句：体系是敞开还是封闭？",
             12, BLUE_D, "700")
    s += txt(450, 288,
             "Open → track escaped and entered matter, then the account balances　|　"
             "Closed → the reading must not change｜敞开→追算逸散与进入的质量；封闭→读数必然不变",
             10, INK)

    # ---- 底部警示条
    s += box(24, 318, 852, 70, "#FFFFFF", RED, 1.1)
    s += txt(450, 344,
             "The law of conservation of mass is never the thing that fails｜从不失效的是质量守恒定律",
             11, RED, "700")
    s += txt(450, 366,
             "What fails is assuming the balance saw everything — count the gases｜"
             "失效的是「天平看见了全部」这个假设——把气体算回来", 10, INK)
    return wrap(s)


# ================================================================ 注册表
FIGURES = {
    "ch04-atom-ledger": fig_ch04_atom_ledger,
    "ch04-open-vs-closed": fig_ch04_open_closed,
    "ch04-apparent-mass": fig_ch04_apparent_mass,
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
