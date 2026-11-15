# -*- coding: utf-8 -*-
"""
Ch.6（化学反应中的能量变化）配图脚本，风格与 build_figure_svg_g10.py 完全一致。

用法：
    python ch06_figures.py            # 全部生成
    python ch06_figures.py ch06       # 只生成文件名含 ch06 的图
    python ch06_figures.py exo        # 只生成文件名含 exo 的图

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


# ================================================================ 图 6-1
def fig_ch06_exo_endo():
    """放热 vs 吸热：左右两个能量变化图，只差生成物台阶的高低。"""
    w, H = 900, 440
    s = head(w, H, "Fig. 6-1　Exothermic vs Endothermic｜放热与吸热能量图",
             "higher → lower = heat out｜高→低 = 放热")
    s += ARROW_DEF

    # ---- 两个面板头
    s += box(24, 52, 414, 30, ORANGE_BG, ORANGE, 1.1)
    s += txt(231, 67, "EXOTHERMIC｜放热反应", 13, ORANGE_D, "700")
    s += box(462, 52, 414, 30, BLUE_BG, BLUE, 1.1)
    s += txt(669, 67, "ENDOTHERMIC｜吸热反应", 13, BLUE_D, "700")

    # ---- 左坐标系
    s += path("M64 300 V126", LINE, 1.3, marker="ar")
    s += path("M64 300 H430", LINE, 1.3, marker="ar")
    s += txt(74, 140, "Energy｜能量", 9.5, SUB, "600", anchor="start")

    # 反应物台阶（左高）
    s += ln(96, 175, 215, 175, BLUE, 2.4)
    s += txt(155, 157, "reactants｜反应物", 9.5, BLUE_D, "600")
    # 下降箭头
    s += path("M215 176 V246", BLUE_D, 2.0, marker="ar")
    # 生成物台阶（右低）
    s += ln(215, 250, 340, 250, ORANGE, 2.4)
    s += txt(277, 268, "products｜生成物", 9.5, ORANGE_D, "600")
    # 台阶之间的注记
    s += txt(312, 202, "energy released｜放出能量", 9.5, ORANGE_D, "700")
    s += txt(312, 218, "→ surroundings warm｜环境变暖", 9, SUB)

    # ---- 右坐标系
    s += path("M502 300 V126", LINE, 1.3, marker="ar")
    s += path("M502 300 H868", LINE, 1.3, marker="ar")
    s += txt(512, 140, "Energy｜能量", 9.5, SUB, "600", anchor="start")

    # 反应物台阶（左低）
    s += ln(534, 250, 653, 250, BLUE, 2.4)
    s += txt(593, 268, "reactants｜反应物", 9.5, BLUE_D, "600")
    # 上升箭头
    s += path("M653 244 V178", BLUE_D, 2.0, marker="ar")
    # 生成物台阶（右高）
    s += ln(653, 175, 778, 175, ORANGE, 2.4)
    s += txt(715, 157, "products｜生成物", 9.5, ORANGE_D, "600")
    s += txt(750, 208, "energy absorbed｜吸收能量", 9.5, BLUE_D, "700")
    s += txt(750, 224, "← surroundings cool｜环境变冷", 9, SUB)

    # ---- 两个面板结论
    s += box(24, 330, 414, 54, "#FFFFFF", ORANGE, 1.1)
    s += txt(231, 348, "Surroundings get WARMER｜环境变暖", 11.5, ORANGE_D, "700")
    s += txt(231, 368, "products end LOWER than reactants｜生成物能量更低", 9.5, INK)
    s += box(462, 330, 414, 54, "#FFFFFF", BLUE, 1.1)
    s += txt(669, 348, "Surroundings get COOLER｜环境变冷", 11.5, BLUE_D, "700")
    s += txt(669, 368, "products end HIGHER than reactants｜生成物能量更高", 9.5, INK)

    # ---- 底部规则条
    s += box(24, 398, 852, 30, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 413,
             "Read the two plateaus, not the hill: the height of the products decides the sign"
             "｜只看两个台阶的高低，别看山丘", 10, INK, "600")
    return wrap(s)


# ================================================================ 图 6-2
def fig_ch06_activation_energy():
    """活化能与催化剂：同一座山，催化剂只是把山丘压低。"""
    w, H = 900, 400
    s = head(w, H, "Fig. 6-2　Activation Energy and Catalyst｜活化能与催化剂",
             "lower hill, same Δ｜降门槛，不改总差")
    s += ARROW_DEF

    # ---- 坐标系
    s += path("M90 300 V100", LINE, 1.3, marker="ar")
    s += path("M90 300 H832", LINE, 1.3, marker="ar")
    s += txt(100, 114, "Energy｜能量", 9.5, SUB, "600", anchor="start")
    s += txt(460, 316, "Reaction progress｜反应进程", 10, SUB, "600")

    # ---- 两条台阶
    s += ln(120, 240, 250, 240, BLUE, 2.4)
    s += txt(185, 224, "reactants｜反应物", 9.5, BLUE_D, "600")
    s += ln(640, 200, 800, 200, ORANGE, 2.4)
    s += txt(720, 184, "products｜生成物", 9.5, ORANGE_D, "600")

    # ---- 无催化剂曲线（实线）
    s += path("M250 240 C 320 240 350 145 460 145"
              " C 570 145 600 200 640 200", INK, 2.0)
    # ---- 加催化剂曲线（虚线，山丘更低）
    s += path("M250 240 C 320 240 350 192 460 192"
              " C 570 192 600 200 640 200", BLUE, 1.6, dash="6 4")

    # ---- 活化能箭头（从反应物台阶水平延伸到峰顶）
    s += ln(250, 240, 475, 240, EDGE, 1.0, dash="4 3")
    s += path("M460 236 V152", INK, 1.2, marker="ar", dash="4 3")
    s += txt(460, 128, "activation energy｜活化能", 9.5, INK, "700")
    s += txt(540, 214, "lower hill｜山丘更低", 9, BLUE_D, "600")

    # ---- 图例
    s += box(250, 246, 470, 48, NEUTRAL_BG, LINE, 1.0)
    s += ln(264, 262, 296, 262, INK, 2.0)
    s += txt(306, 262, "uncatalysed｜不加催化剂", 9, INK, anchor="start")
    s += ln(264, 280, 296, 280, BLUE, 1.6, dash="6 4")
    s += txt(306, 280, "catalysed: lower Ea, same Δ｜加催化剂：活化能更低，总能量差不变",
             9, BLUE_D, anchor="start")

    # ---- 底部结论
    s += box(24, 332, 852, 44, "#FFFFFF", BLUE, 1.1)
    s += txt(450, 350,
             "A catalyst lowers the activation energy — it never adds or removes energy"
             "｜催化剂只降低活化能，不增加也不减少能量", 10.5, INK, "700")
    s += txt(450, 368,
             "So the reaction runs faster at the same temperature, and the same total energy is released"
             "｜同温下更快，放出的总能量不变", 9.5, SUB)
    return wrap(s)


# ================================================================ 图 6-3
def fig_ch06_evidence_cards():
    """证据 → 判定：温度上升/下降 对应 放热/吸热，四张真实例子卡。"""
    w, H = 900, 396
    s = head(w, H, "Fig. 6-3　Evidence to Verdict｜由温度证据判定放热吸热",
             "4 real examples｜4 个真实例子")

    # ---- 两个判据条
    s += box(24, 52, 414, 30, ORANGE_BG, ORANGE, 1.1)
    s += txt(231, 67, "Thermometer UP → EXOTHERMIC｜温度上升 → 放热", 12.5, ORANGE_D, "700")
    s += box(462, 52, 414, 30, BLUE_BG, BLUE, 1.1)
    s += txt(669, 67, "Thermometer DOWN → ENDOTHERMIC｜温度下降 → 吸热", 12.5, BLUE_D, "700")

    cards = [
        (24, 90, "① COMBUSTION｜燃烧", "CH₄ + 2 O₂ → CO₂ + 2 H₂O",
         "burns with heat and light｜燃烧放热发光", "EXO 放热", ORANGE_BG, ORANGE, ORANGE_D),
        (24, 198, "② NEUTRALIZATION｜中和", "HCl + NaOH → NaCl + H₂O",
         "acid + base; the flask feels warm｜酸碱混合，瓶壁发热", "EXO 放热",
         ORANGE_BG, ORANGE, ORANGE_D),
        (462, 90, "③ PHOTOSYNTHESIS｜光合作用", "6 CO₂ + 6 H₂O → C₆H₁₂O₆ + 6 O₂",
         "light energy stored in glucose｜光能存进葡萄糖", "ENDO 吸热",
         BLUE_BG, BLUE, BLUE_D),
        (462, 198, "④ COLD PACK｜冰袋", "NH₄NO₃(s) → NH₄NO₃(aq)",
         "absorbs heat; a physical change｜溶解吸热，物理变化", "ENDO 吸热",
         BLUE_BG, BLUE, BLUE_D),
    ]
    for x, y, title, eq, note, chip, cbg, cedge, ccol in cards:
        s += box(x, y, 414, 100, "#FFFFFF", EDGE, 1.0)
        s += txt(x + 16, y + 20, title, 10.5, ccol, "700", anchor="start")
        s += box(x + 336, y + 9, 62, 20, cbg, cedge, 0.9, rx=6)
        s += txt(x + 367, y + 19, chip, 8.5, ccol, "700")
        s += txt(x + 207, y + 52, eq, 11, INK, "600")
        s += txt(x + 207, y + 78, note, 9, SUB)

    # ---- 底部判定规则
    s += box(24, 308, 852, 66, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 328,
             "The verdict comes from the thermometer, not from how the equation looks"
             "｜判据是温度计，不是方程式看起来的样子", 11, INK, "700")
    s += txt(450, 348,
             "exothermic: surroundings warmer · endothermic: surroundings cooler｜放热=环境变暖 · 吸热=环境变冷",
             9.5, INK)
    s += txt(450, 366,
             "Needing a match is NOT the same as endothermic — a spark only supplies activation energy"
             "｜「需要点燃」≠ 吸热", 9, SUB)
    return wrap(s)


# ================================================================ 注册表
FIGURES = {
    "ch06-exo-vs-endo": fig_ch06_exo_endo,
    "ch06-activation-energy": fig_ch06_activation_energy,
    "ch06-evidence-cards": fig_ch06_evidence_cards,
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
