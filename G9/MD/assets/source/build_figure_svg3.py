# -*- coding: utf-8 -*-
"""
Ch05–Ch07 章节示意图生成器（第三批）。

风格与 build_figure_svg.py / build_figure_svg2.py 完全一致。
本批以「参数化」为主：玻尔图、路易斯点式都由数据驱动生成，
改一个数字就能重出，不会与正文漂移。

用法：
    python build_figure_svg3.py            # 全部生成
    python build_figure_svg3.py ch05       # 只生成文件名含 ch05 的图

输出目录：../figures/
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_figure_svg import (head, box, txt, path, ARROW_DEF, wrap,  # noqa
                              FONT, INK, SUB, LINE, EDGE, BLUE, BLUE_D,
                              BLUE_BG, ORANGE, ORANGE_D, ORANGE_BG,
                              GREEN, GREEN_BG, RED, NEUTRAL_BG)

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(HERE), "figures")

SHELL_NAME = ["第1层 (K)", "第2层 (L)", "第3层 (M)", "第4层 (N)"]


def dot(x, y, r, fill, stroke=None, sw=1.2):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'  <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{st}/>\n')


def badge(x, y, r, label, fill, tcol="#FFFFFF", size=12):
    s = f'  <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>\n'
    s += txt(x, y + 0.5, label, size, tcol, "600")
    return s


def note_line(x, y, s, size=11, fill=SUB, anchor="start"):
    return txt(x, y, s, size, fill, "400", anchor, "central")


# ==================================================== 玻尔图面板（参数化）
def bohr_panel(px, py, pw, spec, right_pad=92):
    """
    画一个玻尔图面板。spec 字段：
      sym / cn / z / shells（由内向外，如 [2, 8, 1]）/ a / nuc_note / shell_note
    返回 (svg, panel_height)
    """
    sym, cn, z = spec["sym"], spec["cn"], spec["z"]
    shells, a = spec["shells"], spec["a"]
    n = len(shells)

    s = txt(px + pw / 2, py, f"{sym}  {cn}  Z = {z}", 14, INK, "700")
    arr = ", ".join(str(x) for x in shells)
    s += txt(px + pw / 2, py + 19, f"电子排布 = {arr}　　(A = {a})", 11, SUB)

    lh = 34
    bx = px + 92
    bw = pw - 92 - right_pad
    top = py + 40
    for i, cnt in enumerate(reversed(shells)):
        li = n - 1 - i
        y = top + i * lh
        outer = (li == n - 1)
        s += box(bx, y, bw, lh, "#FFFFFF", BLUE if outer else EDGE,
                 1.1 if outer else 0.8, rx=4)
        s += txt(bx - 8, y + lh / 2, SHELL_NAME[li], 10.5, SUB, "600", "end")
        step = 22 if cnt <= 9 else 18
        for k in range(cnt):
            s += dot(bx + 18 + k * step, y + lh / 2, 6.5, BLUE_D)
        s += txt(bx + bw - 10, y + lh / 2, str(cnt), 13.5,
                 BLUE_D if outer else INK, "700", "end")
        if outer:
            s += txt(bx + bw + 8, y + lh / 2, "← 价电子", 9.5, BLUE, "600",
                     "start")
        if spec.get("shell_note", {}).get(li):
            s += txt(bx + 18 + max(cnt, 1) * step + 6, y + lh / 2,
                     spec["shell_note"][li], 9.5, SUB, "400", "start")

    # 原子核
    ny = top + n * lh + 18
    cx = bx + bw / 2
    s += box(cx - 62, ny, 124, 46, NEUTRAL_BG, LINE, 1.1, rx=6)
    s += txt(cx, ny + 15, f"{z} p⁺", 12.5, INK, "700")
    s += txt(cx, ny + 32, f"{a - z} n⁰", 12.5, SUB, "700")
    s += txt(cx + 74, ny + 23, "原子核 nucleus", 10.5, SUB, "400", "start")
    if spec.get("nuc_note"):
        s += txt(cx - 74, ny + 23, spec["nuc_note"], 9.5, SUB, "400", "end")
    return s, (ny + 46 - py)


def panel_h(n):
    """玻尔图面板高度：标题 40 + 每层 34 + 核框 18 + 46。"""
    return 40 + n * 34 + 18 + 46


def bohr_figure(title, note, spec, w=900):
    """单元素玻尔图：面板居中。"""
    pw = 560
    h = panel_h(len(spec["shells"]))
    total = int(70 + h + (48 if spec.get("foot") else 34))
    s = head(w, total, title, note)
    s += bohr_panel((w - pw) / 2, 70, pw, spec)[0]
    if spec.get("foot"):
        s += box(60, 70 + h + 6, w - 120, 32, NEUTRAL_BG, EDGE, 0.8, rx=6)
        s += txt(w / 2, 70 + h + 22, spec["foot"], 11.5, INK, "600")
    return wrap(s)


def bohr_pair_figure(title, note, left, right, foot=None, w=900):
    """双元素玻尔图并排。"""
    pw = 430
    h = max(panel_h(len(left["shells"])), panel_h(len(right["shells"])))
    total = int(70 + h + (48 if foot else 34))
    s = head(w, total, title, note)
    s += bohr_panel(14, 70, pw, left, right_pad=84)[0]
    s += bohr_panel(w / 2 + 6, 70, pw, right, right_pad=84)[0]
    if foot:
        s += box(40, 70 + h + 6, w - 80, 32, NEUTRAL_BG, EDGE, 0.8, rx=6)
        s += txt(w / 2, 70 + h + 22, foot, 11.5, INK, "600")
    return wrap(s)


# ==================================================== Ch05 核素记号
def fig_ch05_notation():
    """标准核素记号。"""
    s = head(900, 348, "标准核素记号｜Standard Nuclear Notation",
             "BC Science 9 · 左上 A、左下 Z、中间符号")
    halves = [("标准写法 Standard notation", "X", "ᴬ", "Z",
               ["质量数 A", "元素符号 symbol", "原子序数 Z"], INK),
              ("实例 Example（钠）", "Na", "²³", "₁₁",
               ["A = 23", "sodium 钠", "Z = 11"], BLUE_D)]
    for i, (title, sym, a, z, labels, col) in enumerate(halves):
        cx = 240 if i == 0 else 660
        s += box(cx - 175, 62, 350, 30, NEUTRAL_BG, EDGE, 0.8, rx=6)
        s += txt(cx, 77, title, 12.5, INK, "700")
        s += txt(cx, 176, sym, 44, col, "700")
        s += txt(cx - 40, 138, a, 20, col, "700", "end")
        s += txt(cx - 40, 214, z, 20, col, "700", "end")
        for k, (lab, ly) in enumerate(zip(labels, [138, 176, 214])):
            s += path(f"M{cx + 24} {ly} L{cx + 52} {ly}", EDGE, 1.0)
            s += txt(cx + 60, ly, lab, 12, INK, "600", "start")
    s += path("M450 100 L450 236", EDGE, 1.0, dash="4 4")

    s += box(60, 250, 780, 30, BLUE_BG, BLUE, 0.9, rx=6)
    s += txt(450, 265, "横排写法 In-line：²³₁₁Na　　读作「Na-23」/「sodium-23」/ 中文「钠-23」",
             12.5, BLUE_D, "700")
    s += txt(450, 296, "三量求解 Three quantities：", 11.5, INK, "700")
    s += txt(450, 316, "protons 质子数 = Z = 11　　electrons 电子数 = Z（中性原子）= 11",
             11.5, SUB)
    s += txt(450, 334, "neutrons 中子数 = A − Z = 23 − 11 = 12", 11.5, SUB)
    return wrap(s)


# ==================================================== Ch05 图 5-1
def fig_ch05_layout():
    """电子层条形图通用格式（模板）。"""
    s = head(900, 372, "图 5-1　电子层条形图的通用格式｜The Standard Layout",
             "BC Science 9 · 只有三件东西：核、层、电子")
    s += ARROW_DEF
    s += path("M620 70 L620 96", BLUE, 1.6, marker="ar")
    s += txt(632, 74, "离核最远 outermost", 11, BLUE, "700", "start")
    s += txt(632, 90, "这一层就是 valence shell 价电子层", 10.5, BLUE,
             "600", "start")

    caps = ["容量 2，最先填满", "容量 8", "容量 8（范围内不要写 18！）",
            "前 20 号仅 K、Ca 用到（最多 2 个）"]
    lh, bx, bw = 34, 250, 330
    for i in range(4):
        y = 112 + i * lh
        s += box(bx, y, bw, lh, "#FFFFFF", EDGE, 0.8, rx=4)
        s += txt(bx - 8, y + lh / 2, SHELL_NAME[3 - i], 10.5, SUB, "600",
                 "end")
        for k in range(8):
            s += dot(bx + 20 + k * 24, y + lh / 2, 3.2, EDGE)
        s += txt(bx + bw + 10, y + lh / 2, caps[3 - i], 10, SUB, "400",
                 "start")

    ny = 112 + 4 * lh + 18
    s += box(355, ny, 124, 46, NEUTRAL_BG, LINE, 1.1, rx=6)
    s += txt(417, ny + 15, "Z p⁺", 12.5, INK, "700")
    s += txt(417, ny + 32, "A−Z n⁰", 12.5, SUB, "700")
    s += txt(492, ny + 23, "原子核 nucleus（永远在正中央）", 10.5, SUB,
             "400", "start")

    s += box(60, ny + 62, 780, 32, ORANGE_BG, ORANGE, 1.0, rx=6)
    s += txt(450, ny + 78, "填层铁律 Golden rule：由内向外 inner → outer，内层没满不许填外层",
             12.5, ORANGE_D, "700")
    return wrap(s)


# ==================================================== Ch05 图 5-2
def fig_ch05_H_He():
    h = {"sym": "H", "cn": "氢", "z": 1, "shells": [1], "a": 1,
         "nuc_note": "← 普通氢（氕）没有中子"}
    he = {"sym": "He", "cn": "氦", "z": 2, "shells": [2], "a": 4}
    return bohr_pair_figure(
        "图 5-2　H 氢 与 He 氦｜The Period 1 Pair",
        "BC Science 9 · 第 1 层满 2 就稳定", h, he,
        "H 第 1 层未满 → 活泼　　He 第 1 层已满 → 惰性")


def fig_ch05_O():
    return bohr_figure("图 5-3　O 氧｜Period 2, Group 16",
        "BC Science 9 · 2, 6：两层、最外层 6 个",
        {"sym": "O", "cn": "氧", "z": 8, "shells": [2, 6], "a": 16})


def fig_ch05_Na():
    return bohr_figure("图 5-4　Na 钠｜Period 3, Group 1",
        "BC Science 9 · 2, 8, 1：多余的一个最容易被丢掉",
        {"sym": "Na", "cn": "钠", "z": 11, "shells": [2, 8, 1], "a": 23})


def fig_ch05_Cl():
    return bohr_figure("图 5-5　Cl 氯｜Period 3, Group 17",
        "BC Science 9 · 2, 8, 7：差 1 个就满，所以抢得凶",
        {"sym": "Cl", "cn": "氯", "z": 17, "shells": [2, 8, 7], "a": 35})


def fig_ch05_Ar():
    return bohr_figure("图 5-6　Ar 氩｜Period 3, Group 18 — The Stable One",
        "BC Science 9 · 2, 8, 8：最外层正好满 8",
        {"sym": "Ar", "cn": "氩", "z": 18, "shells": [2, 8, 8], "a": 40,
         "foot": "full valence shell 满的价电子层 = stable 稳定 = inert 惰性"})


def fig_ch05_Ca():
    return bohr_figure("图 5-7　Ca 钙｜Period 4, Group 2",
        "BC Science 9 · 2, 8, 8, 2：前 20 号里唯一的 4 层元素之一",
        {"sym": "Ca", "cn": "钙", "z": 20, "shells": [2, 8, 8, 2], "a": 40})


def fig_ch05_Li_Al():
    li = {"sym": "Li", "cn": "锂", "z": 3, "shells": [2, 1], "a": 7}
    al = {"sym": "Al", "cn": "铝", "z": 13, "shells": [2, 8, 3], "a": 27}
    return bohr_pair_figure(
        "图 5-8　画 Li 与 Al 的玻尔图｜Worked Example — Drawing",
        "BC Science 9 · 层数 → 周期，最外层数 → 族", li, al,
        "自检：各层电子数之和必须等于 Z（中性原子）　Al 不能画成 2, 8, 8, 3")


# ==================================================== Ch05 图 5-10
def fig_ch05_period3():
    """Period 3 全景。"""
    s = head(900, 424, "图 5-10　Period 3 全景｜为什么这一行叫「第三周期」",
             "BC Science 9 · 层数相同 = 同一周期")
    els = ["Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar"]
    groups = ["第1族", "第2族", "第13族", "第14族", "第15族", "第16族",
              "第17族", "第18族"]
    rows = [("第3层", ["1", "2", "3", "4", "5", "6", "7", "8"], BLUE_D),
            ("第2层", ["8"] * 8, INK), ("第1层", ["2"] * 8, INK),
            ("层数", ["3"] * 8, INK),
            ("倾向", ["失1", "失2", "失3", "（±4）", "得3", "得2", "得1",
                      "0"], ORANGE_D)]
    x0, rl = 44, 78
    cw = (900 - x0 * 2 - rl) / 8.0
    gx = x0 + rl
    y, hh, rh = 74, 40, 34

    s += box(x0, y, rl, hh, NEUTRAL_BG, EDGE, 0.8, rx=4)
    for i, e in enumerate(els):
        s += box(gx + i * cw, y, cw, hh, "#FFFFFF", EDGE, 0.8, rx=4)
        s += txt(gx + i * cw + cw / 2, y + hh / 2, e, 16, INK, "700")
    s += box(x0, y + hh, rl, rh, NEUTRAL_BG, EDGE, 0.8, rx=4)
    for i, g in enumerate(groups):
        s += box(gx + i * cw, y + hh, cw, rh, NEUTRAL_BG, EDGE, 0.8, rx=4)
        s += txt(gx + i * cw + cw / 2, y + hh + rh / 2, g, 10.5, SUB, "600")

    for ri, (lab, vals, col) in enumerate(rows):
        cy = y + hh + rh + ri * rh
        s += box(x0, cy, rl, rh, "#FFFFFF", EDGE, 0.8, rx=4)
        s += txt(x0 + rl / 2, cy + rh / 2, lab, 11.5, SUB, "700")
        for ci, v in enumerate(vals):
            cx = gx + ci * cw
            bg = BLUE_BG if (ri == 0) else "#FFFFFF"
            s += box(cx, cy, cw, rh, bg, EDGE, 0.8, rx=4)
            s += txt(cx + cw / 2, cy + rh / 2, v, 12.5, col, "700")

    by = y + hh + rh + 5 * rh + 16
    s += box(60, by, 780, 44, GREEN_BG, GREEN, 1.1, rx=8)
    s += txt(450, by + 17, "终点　→→→→　大家都想变成 Ar 的「2, 8, 8」那个满层结构",
             13, GREEN, "700")
    s += txt(450, by + 34, "横着看：层数都是 3，但最外层从 1 递增到 8 —— 由活泼金属一路变为活泼非金属，停在惰性的 Ar",
             10.5, INK)
    return wrap(s)


# ==================================================== 路易斯点式（参数化）
def _dir_counts(n):
    """按放点规则把 n 个价电子分到 右/左/上/下 四个方向。

    规则：① 四方向各放 1 个，顺序 右→左→上→下
          ② 剩余按 上→下→左→右 补成对
    """
    c = {"R": 0, "L": 0, "T": 0, "B": 0}
    for d in ["R", "L", "T", "B"][:min(n, 4)]:
        c[d] += 1
    for d in ["T", "B", "L", "R"][:max(0, n - 4)]:
        c[d] += 1
    return c


def lewis(cx, cy, sym, n, charge=None, bracket=False, size=17, dr=3.4,
          col=INK):
    """画一个路易斯点式。左右方向的成对点竖排（对应 ASCII 的 `:`），
    上下方向的成对点横排。"""
    c = _dir_counts(n)
    half = len(sym) * size * 0.33 + 5
    dx, dy = half + 9, size * 0.66 + 8
    off = 5.2
    s = ""
    for d in ["T", "B", "L", "R"]:
        for k in range(c[d]):
            if d in ("R", "L"):
                x = cx + (dx if d == "R" else -dx)
                y = cy + (0 if c[d] == 1 else (-off if k == 0 else off))
            else:
                y = cy + (dy if d == "B" else -dy)
                x = cx + (0 if c[d] == 1 else (-off if k == 0 else off))
            s += dot(x, y, dr, col)

    if bracket:
        x1, x2 = cx - dx - 4, cx + dx + 4
        y1, y2 = cy - dy - 3, cy + dy + 3
        s += path(f"M{x1} {y1} L{x1 - 5} {y1} L{x1 - 5} {y2} L{x1} {y2}",
                  col, 1.4)
        s += path(f"M{x2} {y1} L{x2 + 5} {y1} L{x2 + 5} {y2} L{x2} {y2}",
                  col, 1.4)
    s += txt(cx, cy, sym, size, col, "700")
    if charge:
        s += txt(cx + dx + (18 if bracket else 11), cy - dy + 1, charge,
                 11.5, RED, "700", "start")
    return s


# ==================================================== Ch06 图 6-1
def fig_ch06_dot_order():
    s = head(900, 452, "图 6-1　点的放置顺序｜Dot-Placement Order",
             "BC Science 9 · 右→左→上→下，再回头补成对")
    s += box(40, 58, 820, 48, NEUTRAL_BG, EDGE, 0.9, rx=6)
    s += txt(56, 72, "放点规则 Rule：① 先给四个方向各放 1 个单点，顺序 右 → 左 → 上 → 下",
             12, INK, "600", "start")
    s += txt(56, 92, "　　　　　　　② 还有剩余电子时，按「上 → 下 → 左 → 右」把单点补成对",
             12, INK, "600", "start")

    groups = [(1, "钠 Na", "Na", 1), (2, "镁 Mg", "Mg", 2),
              (13, "铝 Al", "Al", 3), (14, "碳 C", "C", 4),
              (15, "氮 N", "N", 5), (16, "氧 O", "O", 6),
              (17, "氯 Cl", "Cl", 7), (18, "氩 Ar", "Ar", 8)]
    xs = [152, 348, 544, 740]
    for i, (g, cn, sym, n) in enumerate(groups):
        r, c = divmod(i, 4)
        x, y = xs[c], 168 + r * 106
        s += txt(x, y - 34, f"Group {g}", 11, SUB, "600")
        s += txt(x, y - 16, f"({n})　{cn}", 12, INK, "700")
        s += lewis(x, y, sym, n)

    s += path("M40 396 L860 396", EDGE, 1.0)
    s += txt(450, 412, "点数核对 dot count", 11.5, INK, "700")
    checks = ["3 = 上1 + 左1 + 右1", "4 = 上1 + 下1 + 左1 + 右1",
              "5 = 上2 + 下1 + 左1 + 右1", "6 = 上2 + 下2 + 左1 + 右1",
              "7 = 上2 + 下2 + 左2 + 右1", "8 = 四面全部成对"]
    for i, t in enumerate(checks):
        x = 60 + (i % 3) * 290
        y = 430 + (i // 3) * 18
        s += txt(x, y, t, 10.5, SUB, "400", "start")
    return wrap(s)


# ==================================================== Ch06 图 6-2
def fig_ch06_g1_g2():
    s = head(900, 280, "图 6-2　第 1、2 族原子｜Groups 1 &amp; 2 Atoms（金属 metals）",
             "BC Science 9 · 这些点很快就交出去")
    s += box(40, 58, 820, 26, BLUE_BG, BLUE, 0.9, rx=6)
    s += txt(450, 71, "金属 metals：点数少 = 容易失去 = 形成阳离子 cation",
             12, BLUE_D, "700")
    row1 = [("Li", "锂", 1), ("Na", "钠", 1), ("K", "钾", 1)]
    row2 = [("Be", "铍", 2), ("Mg", "镁", 2), ("Ca", "钙", 2)]
    xs = [170, 450, 730]
    for r, row in enumerate([row1, row2]):
        y = 146 + r * 86
        for i, (sym, cn, n) in enumerate(row):
            s += txt(xs[i], y - 20, f"({n})", 11, SUB, "600")
            s += lewis(xs[i], y, sym, n, size=18, col=BLUE_D)
            s += txt(xs[i], y + 30, cn, 12, INK, "600")
    return wrap(s)


# ==================================================== Ch06 图 6-3
def fig_ch06_duet():
    s = head(900, 356, "图 6-3　H、He 与「二重规则」｜The Duet Rule Exception",
             "BC Science 9 · 第 1 层的目标是 2 个点")
    s += txt(450, 62, "不只是 8 —— 第 1 层的目标是 2 个点！", 13, ORANGE_D, "700")
    cells = [("H", 1, None, False, "H ·", "氢原子", "1 个价电子", "想再要 1 个"),
             ("He", 2, None, False, "He :", "氦原子", "第 1 层已满",
              "不需要第 2 层"),
             ("Li", 0, "⁺", True, "[Li]⁺", "锂离子", "失去那 1 个", "追 He 结构"),
             ("H", 2, "⁻", True, "[H :]⁻", "氢负离子", "又得来 1 个",
              "追 He 结构")]
    xs = [128, 350, 572, 794]
    for i, (sym, n, ch, br, show, name, a, b) in enumerate(cells):
        x = xs[i]
        s += lewis(x, 120, sym, n, charge=ch, bracket=br, size=18)
        s += txt(x, 164, show, 12, SUB, "600")
        s += txt(x, 186, name, 12.5, INK, "700")
        s += txt(x, 208, a, 11, SUB)
        s += txt(x, 226, b, 11, SUB)
    s += box(40, 248, 820, 96, ORANGE_BG, ORANGE, 1.1, rx=8)
    s += txt(56, 268, "⚠ duet rule 二重规则：H、He（以及变成离子后只有第 1 层的 Li⁺、Be²⁺、H⁻）以 2 个电子为满，不是 8 个",
             12, ORANGE_D, "700", "start")
    s += txt(56, 292, "　　因为第 1 层只有 2 个位置。", 11.5, ORANGE_D, "400",
             "start")
    s += txt(56, 318, "【Extension → Science 10】H⁻ 氢负离子（hydride）在金属氢化物中出现，超出 Science 9 要求，",
             11, SUB, "400", "start")
    s += txt(56, 336, "此处只作「二重规则」的例子。", 11, SUB, "400", "start")
    return wrap(s)


# ==================================================== Ch06 图 6-4
def fig_ch06_g17_g18():
    s = head(900, 320,
             "图 6-4　第 17、18 族原子｜Groups 17 &amp; 18 Atoms",
             "BC Science 9 · 就差 1 个 vs 已经满了")
    s += box(40, 58, 400, 26, ORANGE_BG, ORANGE, 0.9, rx=6)
    s += txt(240, 71, "第 17 族 halogens（就差 1 个）", 12, ORANGE_D, "700")
    s += box(460, 58, 400, 26, GREEN_BG, GREEN, 0.9, rx=6)
    s += txt(660, 71, "第 18 族 noble gases（已满）", 12, GREEN, "700")
    cells = [("F", 7, "氟", ORANGE_D, 240), ("Cl", 7, "氯", ORANGE_D, 400),
             ("Ne", 8, "氖", GREEN, 660), ("Ar", 8, "氩", GREEN, 820)]
    for sym, n, cn, col, x in cells:
        s += lewis(x, 150, sym, n, size=18, col=col)
        s += txt(x, 196, f"({n})", 11.5, SUB, "600")
        s += txt(x, 216, cn, 12.5, INK, "700")
    s += box(40, 240, 820, 68, NEUTRAL_BG, EDGE, 0.9, rx=8)
    s += txt(56, 262, "⚠ 唯一例外 the one exception：He 氦", 12, INK, "700",
             "start")
    s += lewis(150, 292, "He", 2, size=16, col=GREEN)
    s += txt(220, 292, "(2)　氦　← 只有第 1 层，2 个点即满，绝不写成 8 个点",
             11.5, SUB, "400", "start")
    return wrap(s)


# ==================================================== Ch06 图 6-5
def fig_ch06_cations():
    s = head(900, 400, "图 6-5　阳离子的点式｜Cations — Always 0 Dots",
             "BC Science 9 · 方括号外一个点都没有")
    cells = [("Na", "Na⁺ 钠离子", "⁺", "11 p⁺ / 10 e⁻", "排布 2, 8",
              "追 Ne 结构"),
             ("Mg", "Mg²⁺ 镁离子", "²⁺", "12 p⁺ / 10 e⁻", "排布 2, 8",
              "追 Ne 结构"),
             ("Ca", "Ca²⁺ 钙离子", "²⁺", "20 p⁺ / 18 e⁻", "排布 2, 8, 8",
              "追 Ar 结构"),
             ("Al", "Al³⁺ 铝离子", "³⁺", "13 p⁺ / 10 e⁻", "排布 2, 8",
              "追 Ne 结构")]
    xs = [128, 350, 572, 794]
    for i, (sym, name, ch, pe, arr, tgt) in enumerate(cells):
        x = xs[i]
        s += txt(x, 78, name, 12.5, INK, "700")
        s += lewis(x, 124, sym, 0, charge=ch, bracket=True, size=18,
                   col=BLUE_D)
        s += txt(x, 174, pe, 10.5, SUB)
        s += txt(x, 192, arr, 10.5, SUB)
        s += txt(x, 210, tgt, 11, BLUE_D, "600")
    s += box(40, 232, 820, 30, BLUE_BG, BLUE, 1.0, rx=6)
    s += txt(450, 247, "方括号外面一个点都没有 —— 价电子已全部交出去了！", 12.5,
             BLUE_D, "700")
    s += txt(450, 288, "同电子数对照 compare（都是 10 个电子、排布都是 2, 8）：",
             11.5, INK, "700")
    for i, (sym, z) in enumerate([("Na", 11), ("Mg", 12), ("Al", 13)]):
        x = 220 + i * 230
        s += lewis(x, 330, sym, 0,
                   charge="⁺" if i == 0 else ("²⁺" if i == 1 else "³⁺"),
                   bracket=True, size=15, col=BLUE_D)
        s += txt(x, 366, f"{z} p⁺", 11.5, BLUE_D, "700")
    s += txt(450, 388, "└──────── 质子数不同 ⇒ 核电荷不同 ⇒ 不是同一种微粒",
             11, SUB, "600")
    return wrap(s)


# ==================================================== Ch06 图 6-6
def fig_ch06_anions():
    s = head(900, 330, "图 6-6　阴离子的点式｜Anions — Always 8 Dots",
             "BC Science 9 · 方括号 + 8 个点 + 电荷")
    cells = [("F", "F⁻ 氟离子", "⁻", "fluoride", "9 p⁺ / 10 e⁻", "排布 2, 8",
              "追 Ne 结构"),
             ("Cl", "Cl⁻ 氯离子", "⁻", "chloride", "17 p⁺ / 18 e⁻",
              "排布 2, 8, 8", "追 Ar 结构"),
             ("O", "O²⁻ 氧离子", "²⁻", "oxide", "8 p⁺ / 10 e⁻", "排布 2, 8",
              "追 Ne 结构"),
             ("N", "N³⁻ 氮离子", "³⁻", "nitride", "7 p⁺ / 10 e⁻",
              "排布 2, 8", "追 Ne 结构")]
    xs = [128, 350, 572, 794]
    for i, (sym, name, ch, en, pe, arr, tgt) in enumerate(cells):
        x = xs[i]
        s += txt(x, 76, name, 12.5, INK, "700")
        s += lewis(x, 126, sym, 8, charge=ch, bracket=True, size=18,
                   col=ORANGE_D)
        s += txt(x, 180, en, 11.5, SUB, "600")
        s += txt(x, 202, pe, 10.5, SUB)
        s += txt(x, 220, arr, 10.5, SUB)
        s += txt(x, 238, tgt, 11, ORANGE_D, "600")
    s += box(40, 262, 820, 28, ORANGE_BG, ORANGE, 1.0, rx=6)
    s += txt(450, 276, "阴离子 = 方括号 + 8 个点 + 右上角电荷，三样缺一不可",
             12.5, ORANGE_D, "700")
    s += txt(450, 306, "电荷数 = 「还差几个电子才满 8」，不是背出来的", 11.5,
             INK, "600")
    return wrap(s)


# ==================================================== Ch06 图 6-7
def fig_ch06_ion_examples():
    s = head(900, 236,
             "图 6-7　写离子符号、电子数与点式｜Worked Example — Writing Ions",
             "BC Science 9 · 阳离子 0 点、阴离子 8 点")
    cells = [("Na", 0, "⁺", True, "Na⁺ 钠离子", "0 个点", BLUE_D),
             ("N", 8, "³⁻", True, "N³⁻ 氮离子", "8 个点", ORANGE_D),
             ("Ca", 0, "²⁺", True, "Ca²⁺ 钙离子", "0 个点", BLUE_D),
             ("F", 8, "⁻", True, "F⁻ 氟离子", "8 个点", ORANGE_D)]
    xs = [128, 350, 572, 794]
    for i, (sym, n, ch, br, name, cnt, col) in enumerate(cells):
        x = xs[i]
        s += lewis(x, 116, sym, n, charge=ch, bracket=br, size=19, col=col)
        s += txt(x, 168, name, 12, INK, "700")
        s += txt(x, 190, cnt, 11.5, col, "700")
    s += box(40, 210, 820, 20, NEUTRAL_BG, EDGE, 0.8, rx=5)
    s += txt(450, 220, "判断口诀：是金属 ⇒ 阳离子 ⇒ 0 个点；是非金属 ⇒ 阴离子 ⇒ 8 个点",
             11, INK, "600")
    return wrap(s)


# ==================================================== Ch06 图 6-8
def fig_ch06_fix_errors():
    s = head(900, 262,
             "图 6-8　诊断并改正错误写法｜Worked Example — Fix the Errors",
             "BC Science 9 · 阳离子 0 点、阴离子 8 点")
    s += box(40, 58, 430, 26, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(255, 71, "① 与 ② 的改正 corrections", 12, INK, "700")
    s += lewis(150, 140, "Mg", 0, charge="²⁺", bracket=True, size=18,
               col=BLUE_D)
    s += txt(150, 190, "① 正确 [Mg]²⁺", 11.5, BLUE_D, "700")
    s += txt(150, 210, "0 个点（不是 2 个）", 10.5, SUB)
    s += lewis(370, 140, "O", 8, charge="²⁻", bracket=True, size=18,
               col=ORANGE_D)
    s += txt(370, 190, "② 正确 [:O:]²⁻", 11.5, ORANGE_D, "700")
    s += txt(370, 210, "8 个点（不是 6 个）", 10.5, SUB)

    s += box(490, 58, 370, 26, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(675, 71, "⑤ 中文命名对照 naming", 12, INK, "700")
    s += box(490, 92, 370, 150, "#FFFFFF", EDGE, 0.9, rx=8)
    s += txt(510, 118, "Fe²⁺ = 亚铁离子 = iron(II) ion", 12, INK, "600",
             "start")
    s += txt(510, 144, "Fe³⁺ = 铁离子　 = iron(III) ion", 12, INK, "600",
             "start")
    s += txt(510, 176, "中文规则：低价加「亚」，高价不加", 11.5, ORANGE_D,
             "700", "start")
    s += txt(510, 200, "罗马数字：iron(II) / iron(III)", 11.5, SUB, "400",
             "start")
    s += txt(510, 224, "⚠ 不要把 Fe²⁺ 写成「铁离子」", 11, RED, "600", "start")
    return wrap(s)


# ==================================================== Ch06 图 6-9
def fig_ch06_transfer():
    s = head(900, 392,
             "图 6-9　八隅体规则的现场演示｜Na + Cl Electron Transfer",
             "BC Science 9 · 电子守恒：1 + 7 = 0 + 8 = 8")
    s += ARROW_DEF
    s += box(40, 58, 380, 26, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(230, 71, "起点 Start（中性原子 atoms）", 12, INK, "700")
    s += box(480, 58, 380, 26, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(670, 71, "终点 Result（离子 ions）", 12, INK, "700")

    s += lewis(150, 140, "Na", 1, size=19, col=BLUE_D)
    s += txt(150, 186, "价电子 1", 11.5, BLUE_D, "700")
    s += lewis(330, 140, "Cl", 7, size=19, col=ORANGE_D)
    s += txt(330, 186, "价电子 7", 11.5, ORANGE_D, "700")
    s += lewis(590, 140, "Na", 0, charge="⁺", bracket=True, size=19,
               col=BLUE_D)
    s += txt(590, 186, "点数 0", 11.5, BLUE_D, "700")
    s += lewis(790, 140, "Cl", 8, charge="⁻", bracket=True, size=19,
               col=ORANGE_D)
    s += txt(790, 186, "点数 8", 11.5, ORANGE_D, "700")

    s += path("M450 140 L470 140", BLUE, 2.0, marker="ar")
    s += path("M250 112 C300 78 320 78 300 104", ORANGE, 1.8, marker="ar")
    s += txt(276, 66, "Na 把那 1 个点交给 Cl", 10.5, ORANGE_D, "600")

    s += box(40, 214, 820, 168, "#FFFFFF", EDGE, 0.9, rx=8)
    lines = ["· Na 把那 1 个点「交」给了 Cl　　(Na loses 1 e⁻ → Na⁺)",
             "· Cl 用它把自己补成 8 个　　　　(Cl gains 1 e⁻ → Cl⁻)",
             "· 质子数全程不变：Na 始终 11 p⁺，Cl 始终 17 p⁺",
             "· 电子守恒 electrons are conserved：1 + 7 = 0 + 8 = 8　✔",
             "· 双方都拿到满层结构 → 都变稳定 → 正负相吸 → NaCl 离子化合物（Ch.7）"]
    for i, t in enumerate(lines):
        s += txt(60, 240 + i * 28, t, 12, INK if i < 4 else BLUE_D,
                 "600", "start")
    return wrap(s)


FIGURES = {
    "ch05-nuclear-notation.svg": fig_ch05_notation,
    "ch05-bohr-layout.svg": fig_ch05_layout,
    "ch05-bohr-H-He.svg": fig_ch05_H_He,
    "ch05-bohr-O.svg": fig_ch05_O,
    "ch05-bohr-Na.svg": fig_ch05_Na,
    "ch05-bohr-Cl.svg": fig_ch05_Cl,
    "ch05-bohr-Ar.svg": fig_ch05_Ar,
    "ch05-bohr-Ca.svg": fig_ch05_Ca,
    "ch05-bohr-Li-Al.svg": fig_ch05_Li_Al,
    "ch05-period3-panorama.svg": fig_ch05_period3,
    "ch06-dot-placement-order.svg": fig_ch06_dot_order,
    "ch06-groups-1-2-atoms.svg": fig_ch06_g1_g2,
    "ch06-duet-rule.svg": fig_ch06_duet,
    "ch06-groups-17-18-atoms.svg": fig_ch06_g17_g18,
    "ch06-cations-dots.svg": fig_ch06_cations,
    "ch06-anions-dots.svg": fig_ch06_anions,
    "ch06-ion-examples.svg": fig_ch06_ion_examples,
    "ch06-fix-the-errors.svg": fig_ch06_fix_errors,
    "ch06-electron-transfer.svg": fig_ch06_transfer,
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
