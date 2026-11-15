# -*- coding: utf-8 -*-
"""
Ch.5（化学反应的类型）配图脚本，风格与 build_figure_svg_g10.py 一致。

用法：
    python ch05_figures.py            # 全部生成
    python ch05_figures.py ch05       # 只生成文件名含 ch05 的图

输出目录：../figures/（FIG_DIR 复用主脚本）
"""
import os
import sys

from build_figure_svg_g10 import (
    head, box, txt, path, ln, circ, wrap, ARROW_DEF,
    FIG_DIR, INK, SUB, LINE, EDGE,
    BLUE, BLUE_D, BLUE_BG, ORANGE, ORANGE_D, ORANGE_BG,
    GREEN, GREEN_BG, RED, NEUTRAL_BG,
)

LIGHT_RED = "#F7E3E3"


# ================================================================ 图 5-1
def fig_ch05_six_types():
    """六类反应总览：2×3 卡片，每类给一般式 + 一个实例方程式。"""
    w, H = 900, 384
    s = head(w, H, "Fig. 5-1　Six Types of Chemical Reactions｜六类反应总览",
             "each card = one pattern｜一张卡一条模具")

    cards = [
        ("1  Synthesis｜合成", "A + B → AB", "2 Mg + O₂ → 2 MgO",
         "many reactants → one product｜多变一", BLUE_BG, BLUE, BLUE_D),
        ("2  Decomposition｜分解", "AB → A + B", "CaCO₃ → CaO + CO₂",
         "one reactant → many products｜一变多（需加热）",
         ORANGE_BG, ORANGE, ORANGE_D),
        ("3  Single Replacement｜单置换", "A + BC → AC + B",
         "Zn + 2 HCl → ZnCl₂ + H₂",
         "check the activity series first｜先查活动性", BLUE_BG, BLUE, BLUE_D),
        ("4  Double Replacement｜双置换", "AB + CD → AD + CB",
         "AgNO₃ + NaCl → AgCl↓ + NaNO₃",
         "check solubility first｜先查溶解性", ORANGE_BG, ORANGE, ORANGE_D),
        ("5  Neutralization｜中和", "acid + base → salt + water",
         "HCl + NaOH → NaCl + H₂O",
         "a double replacement in disguise｜其实是双置换",
         GREEN_BG, GREEN, GREEN),
        ("6  Combustion｜燃烧", "fuel + O₂ → CO₂ + H₂O",
         "CH₄ + 2 O₂ → CO₂ + 2 H₂O",
         "O₂ is always a reactant｜必须有 O₂", LIGHT_RED, RED, RED),
    ]

    for i, (name, formula, example, note, bg, edge, col) in enumerate(cards):
        x = 20 + (i % 3) * 288
        y = 54 + (i // 3) * 140
        s += box(x, y, 272, 30, bg, edge, 1.1)
        s += txt(x + 136, y + 15, name, 11.5, col, "700")
        s += box(x, y + 30, 272, 102, "#FFFFFF", EDGE, 1.0)
        s += txt(x + 136, y + 56, formula, 12.5, col, "700")
        s += txt(x + 136, y + 84, example, 10.5, INK, "600")
        s += txt(x + 136, y + 110, note, 9, SUB)

    s += box(20, 336, 860, 36, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 354,
             "Six patterns every year: count the reactants, then check the two tables"
             "｜每年都考这六条：先数反应物，再查两张表", 10.5, INK, "600")
    return wrap(s)


# ================================================================ 图 5-2
def fig_ch05_activity_series():
    """金属活动性顺序阶梯：K→Au 逐级下降，H 作为酸线单独标出。"""
    w, H = 900, 440
    s = head(w, H, "Fig. 5-2　Activity Series of Metals｜金属活动性顺序",
             "higher displaces lower｜前换后")

    s += txt(40, 54,
             "Activity series（金属活动性顺序）— the stairs go down as reactivity falls"
             "｜阶梯向下 = 活泼性下降", 10.5, SUB, anchor="start")

    steps = [
        ("K", GREEN_BG, GREEN, GREEN), ("Na", GREEN_BG, GREEN, GREEN),
        ("Ca", GREEN_BG, GREEN, GREEN), ("Mg", BLUE_BG, BLUE, BLUE_D),
        ("Al", BLUE_BG, BLUE, BLUE_D), ("Zn", BLUE_BG, BLUE, BLUE_D),
        ("Fe", BLUE_BG, BLUE, BLUE_D), ("Pb", BLUE_BG, BLUE, BLUE_D),
        ("H", ORANGE_BG, ORANGE, ORANGE_D), ("Cu", LIGHT_RED, RED, RED),
        ("Ag", LIGHT_RED, RED, RED), ("Au", LIGHT_RED, RED, RED),
    ]
    for i, (sym, bg, edge, col) in enumerate(steps):
        x = 40 + i * 44
        y = 76 + i * 24
        s += box(x, y, 40, 22, bg, edge, 1.1, rx=4)
        s += txt(x + 20, y + 11, sym, 12, col, "700")

    # ---- 右侧三张用法卡
    cards = [
        ("RULE｜规则", "higher displaces lower",
         "排在前面的才能换掉后面的", 60),
        ("ABOVE H｜氢之前", "metal + acid → H₂",
         "Cu is below H → no reaction｜铜在氢后不反应", 158),
        ("EXAMPLE｜例", "Fe + CuSO₄ → FeSO₄ + Cu  ✓",
         "Cu + FeSO₄ → no reaction  ✗", 256),
    ]
    for title, l1, l2, y in cards:
        s += box(600, y, 276, 88, "#FFFFFF", EDGE, 1.0)
        s += txt(738, y + 18, title, 9.5, SUB, "700")
        s += txt(738, y + 44, l1, 11, INK, "700")
        s += txt(738, y + 66, l2, 9, SUB)

    s += box(24, 374, 852, 24, BLUE_BG, BLUE, 1.0)
    s += txt(450, 386,
             "K > Na > Ca > Mg > Al > Zn > Fe > Pb > (H) > Cu > Ag > Au", 11, BLUE_D, "700")

    s += box(24, 404, 852, 24, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 416,
             "H is not a metal — it is the acid line: only metals above it give H₂ with acid"
             "｜H 不是金属，是「酸线」", 9.5, INK, "600")
    return wrap(s)


# ================================================================ 图 5-3
def fig_ch05_solubility():
    """溶解性判据：可溶四行 + 五个必认沉淀 + 两个对照实例。"""
    w, H = 900, 450
    s = head(w, H, "Fig. 5-3　Solubility Rules｜溶解性规则",
             "precipitate, water or gas｜有沉淀才反应")

    # ---- 左：可溶
    s += box(24, 56, 400, 30, BLUE_BG, BLUE, 1.1)
    s += txt(224, 71, "SOLUBLE｜可溶（留在溶液里）", 11.5, BLUE_D, "700")
    left_rows = [
        ("NO₃⁻ nitrate｜硝酸根", "all soluble — no exception｜全溶，无例外"),
        ("Group 1⁺  and  NH₄⁺｜钾钠铵", "all soluble — no exception｜全溶，无例外"),
        ("Cl⁻  Br⁻  I⁻｜卤离子", "soluble except Ag⁺, Pb²⁺｜除银、铅"),
        ("SO₄²⁻ sulfate｜硫酸根", "soluble except Ba²⁺, Pb²⁺｜除钡、铅"),
    ]
    for i, (l1, l2) in enumerate(left_rows):
        y = 92 + i * 52
        s += box(24, y, 400, 44, "#FFFFFF", EDGE, 1.0)
        s += txt(224, y + 16, l1, 10.5, INK, "700")
        s += txt(224, y + 32, l2, 9, SUB)

    # ---- 右：不溶 → 沉淀
    s += box(448, 56, 428, 30, ORANGE_BG, ORANGE, 1.1)
    s += txt(662, 71, "INSOLUBLE → PRECIPITATE｜不溶 → 沉淀", 11.5, ORANGE_D, "700")
    salts = [
        ("AgCl", "white precipitate｜白色沉淀", ORANGE),
        ("PbI₂", "yellow precipitate｜黄色沉淀（唯一有颜色）", RED),
        ("PbCl₂", "white precipitate｜白色沉淀", ORANGE),
        ("BaSO₄", "white precipitate｜白色沉淀", ORANGE),
        ("CaCO₃", "white precipitate｜白色沉淀", ORANGE),
    ]
    for i, (f, note, col) in enumerate(salts):
        y = 92 + i * 42
        s += box(448, y, 428, 36, "#FFFFFF", EDGE, 1.0)
        s += txt(500, y + 18, f, 11, col, "700")
        s += txt(676, y + 18, note, 9.5, INK)

    # ---- 实例一：真的发生
    s += box(24, 318, 852, 54, "#FFFFFF", ORANGE, 1.1)
    s += txt(450, 336, "Pb(NO₃)₂ + 2 KI → PbI₂↓ + 2 KNO₃", 12, ORANGE_D, "700")
    s += txt(450, 357,
             "PbI₂ is insoluble → a yellow precipitate appears → the reaction happens"
             "｜生成不溶物，反应真正发生", 9.5, INK)

    # ---- 实例二：不反应
    s += box(24, 384, 852, 54, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 402, "NaNO₃ + KCl → no reaction", 12, INK, "700")
    s += txt(450, 423,
             "every ion stays dissolved → nothing to see → write no reaction"
             "｜四种离子全可溶，写 no reaction", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 5-4
def fig_ch05_decision_tree():
    """判类流程树：四问顺序，左问右答。"""
    w, H = 900, 512
    s = head(w, H, "Fig. 5-4　Which Type Is It? Decision Tree｜反应类型判定树",
             "ask in order, never at random｜按顺序问")

    rows = [
        ("Q1  One reactant formula?｜反应物只有一种？",
         "Decomposition｜分解", "AB → A + B", ORANGE_BG, ORANGE, ORANGE_D),
        ("Q2  Acid + base?｜是酸 + 碱？",
         "Neutralization｜中和", "acid + base → salt + water", GREEN_BG, GREEN, GREEN),
        ("Q3  Fuel (C, H) + O₂?｜燃料 + O₂？",
         "Combustion｜燃烧", "fuel + O₂ → CO₂ + H₂O", LIGHT_RED, RED, RED),
        ("Q4  Element + element?｜单质 + 单质？",
         "Synthesis｜合成", "A + B → AB", BLUE_BG, BLUE, BLUE_D),
        ("Q5  Element + compound?｜单质 + 化合物？",
         "Single replacement｜单置换", "A + BC → AC + B   (check activity)", BLUE_BG, BLUE, BLUE_D),
        ("Q6  Two compounds?｜两种化合物？",
         "Double replacement｜双置换", "AB + CD → AD + CB   (check solubility)",
         ORANGE_BG, ORANGE, ORANGE_D),
    ]

    for i, (q, name, formula, bg, edge, col) in enumerate(rows):
        y = 54 + i * 66
        s += box(24, y, 330, 58, "#FFFFFF", EDGE, 1.0)
        s += txt(189, y + 29, q, 10.5, INK, "600")
        s += ln(354, y + 29, 440, y + 29, LINE, 1.6)
        s += path("M440 %d L452 %d L440 %d Z" % (y + 23, y + 29, y + 35), LINE, 1.0)
        s += box(452, y, 424, 58, bg, edge, 1.1)
        s += txt(664, y + 20, name, 11, col, "700")
        s += txt(664, y + 40, formula, 9.5, INK)

    s += box(24, 454, 852, 46, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 469,
             "No match? Recount the reactants and run the six general formulas again"
             "｜套不进去就重新数反应物", 10, INK, "600")
    s += txt(450, 487,
             "One reaction may fit two labels — write the most specific one and add the other in brackets"
             "｜两个标签都对时，写更具体的那个", 9, SUB)
    return wrap(s)


# ================================================================ 注册表
FIGURES = {
    "ch05-six-types": fig_ch05_six_types,
    "ch05-activity-series": fig_ch05_activity_series,
    "ch05-solubility": fig_ch05_solubility,
    "ch05-decision-tree": fig_ch05_decision_tree,
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
