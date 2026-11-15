# -*- coding: utf-8 -*-
"""
Ch.8（实验技能、安全与科学探究）配图脚本，风格与 build_figure_svg_g10.py 完全一致。

用法：
    python ch08_figures.py            # 全部生成
    python ch08_figures.py ch08       # 只生成文件名含 ch08 的图

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


# ================================================================ 图 8-1
def fig_ch08_inquiry_cycle():
    """科学探究八步循环：八个节点围成一圈，首尾相接。"""
    w, H = 900, 546
    s = head(w, H, "Fig. 8-1　The Inquiry Cycle: 8 Steps｜科学探究八步循环",
             "one loop, eight steps｜八步一循环")
    s += ARROW_DEF

    cx0, cy0, rx, ry = 450, 295, 270, 152
    nodes = [
        ("1", "Question", "提出问题", 0.0),
        ("2", "Hypothesis", "假设 If…then…", 45.0),
        ("3", "Prediction", "预测测什么", 90.0),
        ("4", "Procedure", "步骤 · 控制变量", 135.0),
        ("5", "Data", "数据（含单位）", 180.0),
        ("6", "Analysis", "分析 · 作图", 225.0),
        ("7", "Conclusion", "结论", 270.0),
        ("8", "Communication", "交流 · 报告", 315.0),
    ]
    # 环上位置：从正上方开始顺时针
    import math
    pos = []
    for _, _, _, deg in nodes:
        a = math.radians(deg - 90)
        pos.append((cx0 + rx * math.cos(a), cy0 + ry * math.sin(a)))

    nw, nh = 130, 52
    hw, hh = nw / 2.0, nh / 2.0

    # ---- 箭头（先画，压在节点下面）
    for i in range(len(pos)):
        x1, y1 = pos[i]
        x2, y2 = pos[(i + 1) % len(pos)]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        t1 = min(hw / abs(ux) if ux else 1e6, hh / abs(uy) if uy else 1e6)
        t2 = min(hw / abs(ux) if ux else 1e6, hh / abs(uy) if uy else 1e6)
        sx, sy = x1 + ux * (t1 + 3), y1 + uy * (t1 + 3)
        ex, ey = x2 - ux * (t2 + 5), y2 - uy * (t2 + 5)
        s += path("M %.1f %.1f L %.1f %.1f" % (sx, sy, ex, ey),
                  LINE, 1.4, marker="ar")

    # ---- 八个节点
    for i, ((num, en, cn, _), (x, y)) in enumerate(zip(nodes, pos)):
        fill, edge, col = (BLUE_BG, BLUE, BLUE_D) if i % 2 == 0 else \
                          (ORANGE_BG, ORANGE, ORANGE_D)
        s += box(x - hw, y - hh, nw, nh, fill, edge, 1.1)
        s += txt(x, y - 9, num + "  " + en, 11, col, "700")
        s += txt(x, y + 12, cn, 9.5, SUB)

    # ---- 中心
    s += circ(cx0, cy0, 78, "#FFFFFF", EDGE, 1.2)
    s += txt(cx0, cy0 - 20, "Scientific Inquiry", 11.5, INK, "700")
    s += txt(cx0, cy0 + 2, "科学探究", 13, BLUE_D, "700")
    s += txt(cx0, cy0 + 24, "8 steps · 1 loop", 9.5, SUB)
    s += txt(cx0, cy0 + 40, "走完一圈再问下一个问题", 9, SUB)

    # ---- 底部说明
    s += box(24, 492, 852, 42, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 506,
             "Hypothesis（假设）: If … then … — a testable statement, not a guess｜是可检验的陈述，不是「我觉得」",
             10, INK, "600")
    s += txt(450, 524,
             "Prediction（预测）: the measured result you expect if the hypothesis is right｜预测 = 预期测到的具体数值或现象",
             10, SUB)
    return wrap(s)


# ================================================================ 图 8-2
def fig_ch08_variables():
    """公平实验的三类变量：温度对 NaHCO₃ + CH₃COOH 速率的影响。"""
    w, H = 900, 494
    s = head(w, H, "Fig. 8-2　A Fair Test: Three Variables｜公平实验的三类变量",
             "change one, measure one｜改一测一")

    # ---- 研究问题条
    s += box(24, 54, 852, 44, BLUE_BG, BLUE, 1.1)
    s += txt(450, 68, "Question｜研究问题", 10, BLUE_D, "700")
    s += txt(450, 86,
             "How does temperature affect the rate of NaHCO₃ + CH₃COOH?｜温度如何影响该反应的速率？",
             11, INK, "600")

    # ---- 左：装置
    s += box(30, 112, 340, 300, "#FFFFFF", EDGE, 1.0)
    s += txt(200, 130, "Set-up: change one thing only｜装置：只改一件事", 9.5, INK, "700")

    # 水浴烧杯
    s += path("M95 190 V350 H305 V190", LINE, 1.6)
    s += path("M97 216 H303 V348 H97 Z", BLUE_BG, 0)
    s += ln(95, 216, 305, 216, BLUE, 1.0)
    s += ln(88, 190, 95, 190, LINE, 1.4)
    s += ln(305, 190, 312, 190, LINE, 1.4)

    # 锥形瓶（浸在水浴里）
    s += ln(188, 170, 188, 208, BLUE_D, 1.6)
    s += ln(212, 170, 212, 208, BLUE_D, 1.6)
    s += path("M188 208 L165 320 L235 320 L212 208", BLUE_D, 1.6)
    s += path("M172 302 L228 302 L235 320 L165 320 Z", BLUE_BG, BLUE_D, 1.0)
    for bx, by, br in ((184, 288, 3.5), (200, 276, 4), (216, 292, 3)):
        s += circ(bx, by, br, "#FFFFFF", BLUE)
    s += txt(200, 338, "NaHCO₃ + CH₃COOH｜反应液", 8.5, SUB)

    # 气球
    s += circ(200, 148, 16, ORANGE_BG, ORANGE_D, 1.4)
    s += ln(196, 163, 200, 170, ORANGE_D, 1.2)
    s += ln(204, 163, 200, 170, ORANGE_D, 1.2)
    s += txt(248, 142, "balloon｜气球", 8.5, ORANGE_D, "600", anchor="start")

    # 温度计
    s += box(268, 222, 12, 100, "#FFFFFF", LINE, 1.0, rx=5)
    s += ln(274, 236, 274, 312, RED, 3.0)
    s += circ(274, 322, 8, "#FFFFFF", RED, 1.2)
    s += txt(338, 250, "20·30·40", 8.5, RED, "700")
    s += txt(338, 264, "°C", 8.5, RED, "700")
    s += ln(280, 244, 340, 244, RED, 0.8, dash="3 3")

    s += txt(200, 366, "water bath｜水浴（只改水温）", 9.5, BLUE_D, "600")
    s += txt(200, 390, "same flask · same solutions · same timer", 9, SUB)
    s += txt(200, 404, "同一锥形瓶、同样药量、同一计时", 9, SUB)

    # ---- 右：三张变量卡
    cards = [
        ("① Independent variable｜自变量", "what I change on purpose｜我故意改的",
         "Water-bath temperature: 20 °C → 30 °C → 40 °C",
         "chosen before the experiment, one value per trial｜实验前自己定的那一个",
         BLUE_D, BLUE_BG, BLUE, 112),
        ("② Dependent variable｜因变量", "what I measure｜我测量、记录的结果",
         "Time for the balloon to reach 10 cm (in seconds)",
         "depends on the temperature — it is the answer｜随自变量而变，就是结论要报的数值",
         ORANGE_D, ORANGE_BG, ORANGE, 216),
        ("③ Controlled variables｜控制变量", "what I keep identical｜我保持不变的那些",
         "1.0 g NaHCO₃ · 10 mL acid, same concentration",
         "same flask, same water volume, same timer｜其余条件全部相同",
         GREEN, GREEN_BG, GREEN, 320),
    ]
    for title, sub, l1, l2, col, bg, edge, y in cards:
        s += box(396, y, 476, 92, bg, edge, 1.1)
        s += box(396, y, 6, 92, edge, edge, 0)
        s += txt(414, y + 18, title, 11.5, col, "700", anchor="start")
        s += txt(414, y + 36, sub, 9, SUB, anchor="start")
        s += txt(414, y + 58, l1, 9.5, INK, anchor="start")
        s += txt(414, y + 76, l2, 9.5, INK, anchor="start")

    # ---- 底部：干扰变量
    s += box(24, 424, 852, 56, "#FFFFFF", RED, 1.1)
    s += txt(450, 440,
             "Confounding variable｜干扰变量 — the acid warms up as the bath heats, or two people time the runs",
             9.5, RED, "700")
    s += txt(450, 458,
             "Anything besides the independent variable that could change the result must be held constant or removed｜"
             "除自变量外还能影响结果的，要么控住要么排除", 9.5, INK)
    s += txt(450, 474,
             "Fair test = one variable changed, one variable measured, everything else identical｜公平实验三件事",
             9, SUB)
    return wrap(s)


# ================================================================ 图 8-3
def fig_ch08_whmis():
    """WHMIS 2015 八种象形图速览（简化几何示意，红色菱形边框）。"""
    w, H = 900, 506
    s = head(w, H, "Fig. 8-3　WHMIS Pictograms at a Glance｜WHMIS 安全标识速览",
             "know before you enter｜进实验室前先认全")

    s += box(24, 54, 852, 32, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 70,
             "WHMIS 2015 (GHS) — 8 pictograms on every chemical container｜八种标识，看到就要知道它警告什么",
             10.5, INK, "600")

    cards = [
        ("flame", "Flammable", "易燃", "catches fire easily｜易着火"),
        ("tube", "Corrosive", "腐蚀", "eats skin and metal｜伤皮肤、蚀金属"),
        ("skull", "Toxic", "有毒", "can kill at low dose｜少量即致命"),
        ("o_flame", "Oxidizing", "氧化性", "feeds fire, no flame needed｜助燃"),
        ("cylinder", "Compressed Gas", "压缩气体", "cylinder under pressure｜高压钢瓶"),
        ("bio", "Biohazard", "生物危害", "infectious material｜可致病生物材料"),
        ("tree", "Environmental Hazard", "环境危害", "harmful to water life｜危害水生生物"),
        ("bang", "Exclamation Mark", "刺激 / 警示", "irritant, low toxicity｜刺激、低毒"),
    ]

    cw, ch, gap = 200, 158, 18
    for i, (sym, en, cn, note) in enumerate(cards):
        x = 23 + (i % 4) * (cw + gap)
        y = 98 + (i // 4) * 178
        cx, cy = x + cw / 2.0, y + 50

        s += box(x, y, cw, ch, "#FFFFFF", EDGE, 1.0)
        # 红色菱形
        d = 38
        s += path("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z"
                  % (cx, cy - d, cx + d, cy, cx, cy + d, cx - d, cy),
                  RED, 3.2)
        s += _pictogram(sym, cx, cy)

        s += txt(cx, y + 108, en, 11.5, INK, "700")
        s += txt(cx, y + 126, cn, 10.5, RED, "700")
        s += txt(cx, y + 144, note, 8.5, SUB)

    s += box(24, 448, 852, 44, "#FFFFFF", RED, 1.1)
    s += txt(450, 462,
             "A pictogram tells you the hazard, not the procedure｜标识只告诉你「危险是什么」，不告诉你「怎么做」",
             10, RED, "700")
    s += txt(450, 480,
             "Read it before you pour: goggles on, tray under, waste in the labelled container｜"
             "倒之前先看标识：戴护目镜、放托盘、废液进指定桶", 9.5, INK)
    return wrap(s)


def _pictogram(kind, cx, cy):
    """简化几何符号，全部画在 38pt 菱形内。"""
    k = INK
    if kind == "flame":
        t = path("M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f "
                    "C%.1f %.1f %.1f %.1f %.1f %.1f "
                    "C%.1f %.1f %.1f %.1f %.1f %.1f "
                    "C%.1f %.1f %.1f %.1f %.1f %.1f Z"
                    % (cx, cy - 22,
                       cx + 6, cy - 11, cx + 12, cy - 5, cx + 12, cy + 3,
                       cx + 12, cy + 11, cx + 6, cy + 17, cx, cy + 17,
                       cx - 6, cy + 17, cx - 12, cy + 11, cx - 12, cy + 3,
                       cx - 12, cy - 3, cx - 5, cy - 9, cx, cy - 22), k, 1.8)
        t += path("M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f "
                 "C%.1f %.1f %.1f %.1f %.1f %.1f Z"
                 % (cx, cy + 13,
                    cx - 6, cy + 8, cx - 5, cy + 1, cx, cy - 6,
                    cx + 5, cy + 1, cx + 6, cy + 8, cx, cy + 13), k, 1.0)
        return t
    if kind == "tube":
        t = path("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z"
                 % (cx - 17, cy - 18, cx - 6, cy - 4, cx, cy - 9, cx - 11, cy - 23),
                 k, 1.6)
        t += circ(cx - 2, cy + 1, 2.6, k, k, 0.5)
        t += circ(cx + 1, cy + 7, 2.2, k, k, 0.5)
        t += ln(cx - 18, cy + 12, cx + 18, cy + 12, k, 1.8)
        t += path("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f"
                  % (cx - 3, cy + 12, cx - 1, cy + 17, cx + 2, cy + 13, cx + 4, cy + 17),
                  k, 1.2)
        return t
    if kind == "skull":
        t = ln(cx - 15, cy + 13, cx + 15, cy - 11, k, 2.0)
        t += ln(cx - 15, cy - 11, cx + 15, cy + 13, k, 2.0)
        t += circ(cx, cy - 3, 12, "#FFFFFF", k, 1.8)
        t += circ(cx - 5, cy - 5, 2.8, k, k, 0.3)
        t += circ(cx + 5, cy - 5, 2.8, k, k, 0.3)
        t += path("M%.1f %.1f V%.1f H%.1f V%.1f H%.1f V%.1f H%.1f V%.1f"
                  % (cx - 7, cy + 9, cy + 17, cx + 7, cy + 9, cx + 3, cy + 17, cx - 3, cy + 9),
                  k, 1.6)
        return t
    if kind == "o_flame":
        t = circ(cx, cy + 6, 13, "#FFFFFF", k, 2.0)
        t += path("M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f "
                  "C%.1f %.1f %.1f %.1f %.1f %.1f "
                  "C%.1f %.1f %.1f %.1f %.1f %.1f "
                  "C%.1f %.1f %.1f %.1f %.1f %.1f Z"
                  % (cx, cy - 24,
                     cx + 4, cy - 16, cx + 7, cy - 12, cx + 7, cy - 8,
                     cx + 7, cy - 4, cx + 4, cy - 2, cx, cy - 2,
                     cx - 4, cy - 2, cx - 7, cy - 4, cx - 7, cy - 8,
                     cx - 7, cy - 11, cx - 3, cy - 15, cx, cy - 24), k, 1.6)
        return t
    if kind == "cylinder":
        t = box(cx - 10, cy - 14, 20, 32, "#FFFFFF", k, 1.8, rx=7)
        t += box(cx - 4, cy - 21, 8, 7, k, k, 0.5, rx=2)
        t += ln(cx - 10, cy - 2, cx + 10, cy - 2, k, 1.0)
        return t
    if kind == "bio":
        t = ""
        for ax, ay in ((-10, -7), (10, -7), (0, 12)):
            t += circ(cx + ax, cy + ay, 7, "#FFFFFF", k, 1.6)
            t += circ(cx + ax, cy + ay, 2.4, k, k, 0.3)
        t += circ(cx, cy + 1, 5, "#FFFFFF", k, 1.4)
        return t
    if kind == "tree":
        t = ln(cx, cy + 16, cx, cy - 2, k, 2.0)
        t += path("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z"
                  % (cx, cy - 20, cx + 9, cy - 6, cx + 4, cy - 6, cx + 12, cy + 5,
                     cx - 12, cy + 5, cx - 4, cy - 6), k, 1.5)
        t += path("M%.1f %.1f Q%.1f %.1f %.1f %.1f T%.1f %.1f"
                  % (cx - 18, cy + 18, cx - 12, cy + 13, cx - 6, cy + 18,
                     cx + 6, cy + 18), k, 1.4)
        return t
    # bang
    t = ln(cx, cy - 18, cx, cy + 6, k, 4.2)
    t += circ(cx, cy + 14, 3.0, k, k, 0.3)
    return t


# ================================================================ 注册表
FIGURES = {
    "ch08-inquiry-cycle": fig_ch08_inquiry_cycle,
    "ch08-fair-test-variables": fig_ch08_variables,
    "ch08-whmis-pictograms": fig_ch08_whmis,
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
