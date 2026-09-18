# -*- coding: utf-8 -*-
"""
Ch02–Ch11 章节示意图生成器（第二批）。

与 build_figure_svg.py 完全同风格、同配色，只是把图量做大，故单独成文件，
避免单文件过长。复用前者的样式常量与 box/txt/path 助手。

用法：
    python build_figure_svg2.py            # 全部生成
    python build_figure_svg2.py ch04       # 只生成文件名含 ch04 的图

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
MONO = "'Consolas','Segoe UI','Microsoft YaHei',monospace"


def dot(x, y, r, fill, stroke=None, sw=1.2):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'  <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{st}/>\n')


def badge(x, y, r, label, fill, tcol="#FFFFFF", size=12):
    """编号圆形徽章。"""
    s = f'  <circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>\n'
    s += txt(x, y + 0.5, label, size, tcol, "600")
    return s


def note_line(x, y, s, size=11, fill=SUB, anchor="start"):
    """左侧小字说明行。"""
    return txt(x, y, s, size, fill, "400", anchor, "central")


# ============================================================ Ch02 图 2-1
def fig_ch02_cell():
    """周期表方格怎么读。"""
    s = head(900, 306, "图 2-1　周期表方格怎么读｜Reading a Cell",
             "BC Science 9 · 四个数字，只有一个是身份证号")
    s += ARROW_DEF

    # ---- 左侧：方格本体
    s += box(105, 78, 176, 176, "#FFFFFF", BLUE, 1.4, rx=6)
    s += txt(124, 100, "11", 16, BLUE_D, "700", "start")
    s += txt(193, 152, "Na", 42, INK, "700")
    s += txt(193, 186, "sodium", 13, SUB)
    s += txt(193, 232, "22.99", 12, INK)

    # ---- 右侧：四条注释 + 引线
    items = [
        ("1", "atomic number 原子序数", "= 质子数 = 11（整数）", 100, BLUE),
        ("2", "chemical symbol 元素符号", "首字母大写、第二个字母小写", 152, BLUE),
        ("3", "element name 元素名称", "英文全名，便于查词典", 186, LINE),
        ("4", "atomic mass 相对原子质量", "= 同位素加权平均 ⇒ 小数", 232, ORANGE),
    ]
    for num, t1, t2, y, col in items:
        s += path(f"M292 {y} L346 {y}", LINE, 1.0, dash="3 3")
        s += badge(360, y, 13, num, col)
        s += txt(382, y - 8, t1, 13, INK, "600", "start")
        s += txt(382, y + 11, t2, 11, SUB, "400", "start")

    # ---- 底部结论条
    s += box(105, 266, 690, 30, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(450, 281, "查表结果：sodium 钠（Na），第 11 号，22.99 amu",
             12, INK, "600")
    return wrap(s)


# ================================================ Ch02 图 2-2 / Ch03 图 3-2
def fig_periodic_simple():
    """前 20 号元素简易周期表（Ch02 图 2-2 与 Ch03 图 3-2 共用）。"""
    s = head(900, 372, "前 20 号元素简易周期表｜Simplified Periodic Table (1–20)",
             "BC Science 9 · 横着数序数，竖着看族")

    x0, rowlab_w = 42, 92
    cols = ["1", "2", "13", "14", "15", "16", "17", "18"]
    cw = (900 - 2 * x0 - rowlab_w) / 8.0
    gx = x0 + rowlab_w          # 数据区左边界
    y = 74
    hh = 30

    def cell(cx, cy, cwid, ch, fill, stroke, sw=0.8):
        return box(cx, cy, cwid, ch, fill, stroke, sw, rx=4)

    # ---- 表头：Group No.
    s += cell(x0, y, rowlab_w, hh, NEUTRAL_BG, EDGE)
    s += txt(x0 + rowlab_w / 2, y + hh / 2, "Group", 10.5, SUB, "600")
    for i, c in enumerate(cols):
        s += cell(gx + i * cw, y, cw, hh, NEUTRAL_BG, EDGE)
        s += txt(gx + i * cw + cw / 2, y + hh / 2, c, 12, INK, "700")

    data = [
        ("Period 1", [("H", "氢"), None, None, None, None, None, None,
                      ("He", "氦")]),
        ("Period 2", [("Li", "锂"), ("Be", "铍"), ("B", "硼"), ("C", "碳"),
                      ("N", "氮"), ("O", "氧"), ("F", "氟"), ("Ne", "氖")]),
        ("Period 3", [("Na", "钠"), ("Mg", "镁"), ("Al", "铝"), ("Si", "硅"),
                      ("P", "磷"), ("S", "硫"), ("Cl", "氯"), ("Ar", "氩")]),
        ("Period 4", [("K", "钾"), ("Ca", "钙"), None, None, None, None,
                      None, None]),
    ]
    rh = 46
    for ri, (rlab, row) in enumerate(data):
        cy = y + hh + ri * rh
        s += cell(x0, cy, rowlab_w, rh, "#FFFFFF", EDGE)
        s += txt(x0 + rowlab_w / 2, cy + rh / 2, rlab, 11.5, SUB, "600")
        for ci, it in enumerate(row):
            cx = gx + ci * cw
            if it is None:
                s += cell(cx, cy, cw, rh, "#FAFAF7", EDGE, 0.6)
                if ri == 0:
                    continue
                s += txt(cx + cw / 2, cy + rh / 2, "…", 14, EDGE)
                continue
            sym, cn = it
            noble = sym in ("He", "Ne", "Ar")
            fill = GREEN_BG if noble else "#FFFFFF"
            s += cell(cx, cy, cw, rh, fill, EDGE)
            s += txt(cx + cw / 2, cy + rh / 2 - 7, sym, 17, INK, "700")
            s += txt(cx + cw / 2, cy + rh / 2 + 12, cn, 10, SUB)

    # ---- 第 4 周期留空说明
    s += txt(gx + 3 * cw + 2.5 * cw, y + hh + 3 * rh + rh / 2,
             "31–36 号（Ga … Kr），超出前 20 号", 10, SUB)

    # ---- 底部说明
    base = y + hh + 4 * rh + 24
    s += txt(x0, base, "纵列 = group 族　　横行 = period 周期", 11.5, INK,
             "600", "start")
    s += note_line(x0, base + 20,
                   "第 1 周期只有 H（1 号）与 He（2 号）：H 在第 1 族，He 在第 18 族")
    s += note_line(x0, base + 40,
                   "第 4 周期的 13–18 族是 31–36 号（Ga … Kr），超出前 20 号范围，故留空")
    return wrap(s)


# ============================================================ Ch02 图 2-3
def fig_ch02_isotopes():
    """同位素：质子同、中子不同。"""
    s = head(900, 404, "图 2-3　同位素：质子同、中子不同｜Isotopes",
             "BC Science 9 · 黑点一样多 ⇒ 都是碳")
    s += ARROW_DEF

    s += box(40, 58, 820, 26, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(450, 71, "同一种元素 ⇒ 质子数必须相同 SAME　　同位素 ⇒ 中子数可以不同 DIFFERENT",
             12, INK, "600")

    specs = [("碳-12  C-12", 6, 6, "6p + 6n = 12", "约占 98.9%", "稳定 stable"),
             ("碳-13  C-13", 6, 7, "6p + 7n = 13", "约占 1.1%", "稳定 stable"),
             ("碳-14  C-14", 6, 8, "6p + 8n = 14", "痕量 trace", "放射性 radioactive")]
    bx, bw, gap = 62, 238, 33
    for i, (name, np_, nn, eq, pct, tag) in enumerate(specs):
        x = bx + i * (bw + gap)
        s += txt(x + bw / 2, 116, name, 14, INK, "700")
        s += box(x, 128, bw, 108, "#FFFFFF", LINE, 1.0, rx=6)
        # 质子行
        s += txt(x + 12, 152, "p⁺", 11, BLUE_D, "700", "start")
        for k in range(np_):
            s += dot(x + 42 + k * 22, 152, 7.5, BLUE_D)
        # 中子行
        s += txt(x + 12, 190, "n⁰", 11, SUB, "700", "start")
        for k in range(nn):
            s += dot(x + 42 + k * 22, 190, 7.5, "#FFFFFF", SUB, 1.4)
        s += txt(x + 12, 224, f'{np_} 个质子', 10, BLUE, "400", "start")
        s += txt(x + bw - 12, 224, f'{nn} 个中子', 10, SUB, "400", "end")
        # 下方标注
        s += txt(x + bw / 2, 254, eq, 13, INK, "600")
        s += txt(x + bw / 2, 274, pct, 11, SUB)
        s += txt(x + bw / 2, 292, tag, 10, GREEN if tag == "稳定 stable" else RED)

    # ---- 图例
    ly = 320
    s += dot(70, ly, 7.5, BLUE_D)
    s += txt(86, ly, "proton 质子", 11.5, INK, "400", "start")
    s += dot(210, ly, 7.5, "#FFFFFF", SUB, 1.4)
    s += txt(226, ly, "neutron 中子", 11.5, INK, "400", "start")
    s += txt(370, ly, "三者都是碳（都是 6 个质子），只是中子数不同", 11.5,
             INK, "600", "start")

    # ---- 氯的加权平均
    s += box(40, 340, 820, 52, ORANGE_BG, ORANGE, 1.0, rx=8)
    s += txt(60, 358, "氯的天然样品 ≈ 75% Cl-35 + 25% Cl-37", 12.5, ORANGE_D,
             "600", "start")
    s += txt(60, 378, "⇒ 平均值落在 35 与 37 之间、且偏向含量多的 35　⇒ 周期表上 Cl = 35.45（小数！）",
             11.5, ORANGE_D, "400", "start")
    return wrap(s)


# ============================================================ Ch02 图 2-4
def fig_ch02_mass_vs_number():
    """为什么改按原子序数排序。"""
    s = head(900, 392, "图 2-4　为什么改按原子序数排序｜Mass Order vs Number Order",
             "BC Science 9 · 位置由质子数决定，不由重量决定")
    s += ARROW_DEF

    s += box(60, 60, 360, 30, ORANGE_BG, ORANGE, 1.0, rx=6)
    s += txt(240, 75, "按 atomic mass 排（Mendeleev）", 12.5, ORANGE_D, "700")
    s += box(480, 60, 360, 30, BLUE_BG, BLUE, 1.0, rx=6)
    s += txt(660, 75, "按 atomic number 排（Moseley，现代）", 12.5, BLUE_D, "700")
    s += path("M450 96 L450 300", EDGE, 1.0, dash="4 4")

    groups = [
        (("Ar", "39.95", 18, "Ar", "惰性气体，与 Ne、Kr 同列"),
         ("K", "39.10", 19, "K", "活泼碱金属，与 Na 同列"), 106),
        (("Te", "127.60", 52, "Te", "与 O、S、Se 同列"),
         ("I", "126.90", 53, "I", "与 F、Cl、Br 同列"), 216),
    ]
    for top, bot, y0 in groups:
        # ---- 左：按质量
        s += box(90, y0, 140, 38, "#FFFFFF", ORANGE, 1.0, rx=6)
        s += txt(160, y0 + 19, f"{top[0]}  {top[1]}", 13, INK, "700")
        s += box(90, y0 + 50, 140, 38, "#FFFFFF", ORANGE, 1.0, rx=6)
        s += txt(160, y0 + 69, f"{bot[0]}  {bot[1]}", 13, INK, "700")
        s += path(f"M258 {y0 + 8} C280 {y0 + 18} 280 {y0 + 62} 258 {y0 + 80}",
                  RED, 1.4)
        s += txt(300, y0 + 19, "质量倒挂 ✗", 12, RED, "700", "start")
        s += note_line(300, y0 + 40, f"重的 {top[0]} 反而排在前面")
        s += note_line(300, y0 + 62, f"与 {bot[0]} 的性质完全对不上")

        # ---- 右：按原子序数
        for k, (sym, z, note) in enumerate([(top[2], top[3], top[4]),
                                            (bot[2], bot[3], bot[4])]):
            yy = y0 + k * 50
            s += box(510, yy, 150, 38, GREEN_BG, GREEN, 1.0, rx=6)
            s += txt(585, yy + 19, f"Z={z}  {sym}", 13, GREEN, "700")
            s += txt(700, yy + 19, f"✓ {note}", 11.5, INK, "400", "start")

    s += box(60, 328, 780, 46, BLUE_BG, BLUE, 1.0, rx=8)
    s += txt(450, 344, "X 射线光谱给出的是「核电荷数」＝ 质子数", 13, BLUE_D, "700")
    s += txt(450, 362, "⇒ 位置由质子数决定，不由重量决定　⇒ 周期表本质是一张按电子结构排列的表",
             11.5, BLUE_D)
    return wrap(s)


# ============================================================ Ch03 图 3-1
def fig_ch03_map():
    """把周期表当地图读。"""
    s = head(900, 366, "图 3-1　把周期表当「地图」读｜Reading the Map",
             "BC Science 9 · 位置 =（周期, 族）")
    s += ARROW_DEF

    s += txt(560, 66, "group 族（纵列 1 → 18）", 12.5, INK, "600")
    s += path("M700 76 L860 76", BLUE, 1.6, marker="ar")
    s += txt(870, 76, "向右：族号增大", 10.5, BLUE, "400", "start")

    gx, gw = 250, 550
    cols = ["1", "2", "13", "14", "15", "16", "17", "18"]
    cw = gw / 8.0
    s += box(gx - 8, 92, gw + 16, 30, NEUTRAL_BG, EDGE, 0.8, rx=4)
    for i, c in enumerate(cols):
        s += txt(gx + i * cw + cw / 2, 107, c, 11.5, SUB, "600")

    grid = [
        ("period 1", [("H", 0), ("He", 7)]),
        ("period 2", [("Li", 0), ("Be", 1), ("B", 2), ("C", 3), ("N", 4),
                      ("O", 5), ("F", 6), ("Ne", 7)]),
        ("period 3", [("Na", 0), ("Mg", 1), ("Al", 2), ("Si", 3), ("P", 4),
                      ("S", 5), ("Cl", 6), ("Ar", 7)]),
        ("period 4", [("K", 0), ("Ca", 1)]),
    ]
    rh = 34
    for ri, (lab, items) in enumerate(grid):
        cy = 122 + ri * rh
        if ri % 2 == 0:
            s += box(gx - 8, cy, gw + 16, rh, "#FBFAF6", "#F0EEE6", 0.6, rx=0)
        s += txt(200, cy + rh / 2, lab, 11.5, SUB, "600", "end")
        for sym, ci in items:
            s += txt(gx + ci * cw + cw / 2, cy + rh / 2, sym, 13, INK, "700")
        if ri == 3:
            s += txt(gx + 2.2 * cw, cy + rh / 2, "…（13–18 族为 31–36 号）",
                     10.5, SUB, "400", "start")
    s += box(gx - 8, 122, gw + 16, rh * 4, "none", LINE, 1.2, rx=6)

    s += path("M170 258 L170 292", BLUE, 1.6, marker="ar")
    s += txt(178, 300, "向下：周期数增大（电子层数增加）", 10.5, BLUE, "400",
             "start")

    s += box(40, 316, 820, 34, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(450, 333, "坐标读法 Position =（period, group）　　例：(3, 17) → Cl 氯　　(2, 14) → C 碳　　Na → (3, 1)",
             12, INK, "600")
    return wrap(s)


# ============================================================ Ch03 图 3-3
def fig_ch03_zigzag():
    """三大区与锯齿线。"""
    # 底部三行注记末尾在 base+40 = 466，留 26 下边距 → 492
    s = head(900, 492, "图 3-3　三大区与锯齿线｜Three Regions &amp; the Zigzag Line",
             "BC Science 9 · 线的左＝金属，右＝非金属，线上＝类金属")

    cols = ["1", "2", "13", "14", "15", "16", "17", "18"]
    x0, rl = 60, 74
    cw = (900 - x0 * 2 - rl) / 8.0
    gx = x0 + rl
    y0, hh, rh = 70, 30, 44
    s += box(x0, y0, rl, hh, NEUTRAL_BG, EDGE, 0.8, rx=4)
    for i, c in enumerate(cols):
        s += box(gx + i * cw, y0, cw, hh, NEUTRAL_BG, EDGE, 0.8, rx=4)
        s += txt(gx + i * cw + cw / 2, y0 + hh / 2, c, 12, INK, "700")

    # M 金属 / n 非金属 / N 稀有气体 / # 类金属
    grid = [
        "n------N",
        "MM#nnnnN",
        "MMM#nnnN",
        "MMM##nnN",
        "MMMM##nN",
    ]
    style = {"M": (BLUE_BG, BLUE_D, "M"), "n": (ORANGE_BG, ORANGE_D, "n"),
             "N": (GREEN_BG, GREEN, "N"), "#": ("#FFF8E1", ORANGE_D, "#")}
    for ri, row in enumerate(grid):
        cy = y0 + hh + ri * rh
        s += box(x0, cy, rl, rh, "#FFFFFF", EDGE, 0.8, rx=4)
        s += txt(x0 + rl / 2, cy + rh / 2, f"P{ri + 1}", 11.5, SUB, "700")
        for ci, ch in enumerate(row):
            if ch == "-":
                continue
            bg, fg, lab = style[ch]
            cx = gx + ci * cw
            s += box(cx + 2, cy + 2, cw - 4, rh - 4, bg, EDGE, 0.6, rx=4)
            s += txt(cx + cw / 2, cy + rh / 2, lab, 15, fg, "700")

    # ---- 锯齿线：沿 # 格的折线
    ytop = y0 + hh
    def cx(i):
        return gx + i * cw + cw / 2
    def cyy(r):
        return ytop + r * rh + rh / 2
    pts = [(2, 0), (3, 1), (3, 2), (4, 2), (4, 3), (5, 3)]
    d = "M" + " L".join(f"{cx(c):.1f} {cyy(r):.1f}" for c, r in pts)
    s += f'  <path d="{d}" fill="none" stroke="{RED}" stroke-width="2.4" ' \
         f'stroke-linejoin="round" stroke-dasharray="6 3"/>\n'
    for c, r in pts:
        s += dot(cx(c), cyy(r), 3.6, RED)

    # ---- 图例：类金属那条文字太长，单独占一行（否则 4 个盒子横排会超出 900 宽）
    ly = ytop + 5 * rh + 26
    s += box(x0, ly, 780, 26, "#FFF8E1", EDGE, 0.7, rx=5)
    s += txt(x0 + 10, ly + 13,
             "# = metalloid / semi-metal 类金属：B、Si、Ge、As、Sb、Te",
             10.5, ORANGE_D, "600", "start")
    ly2 = ly + 32
    others = [(BLUE_BG, BLUE_D, "M = metal 金属"),
              (ORANGE_BG, ORANGE_D, "n = non-metal 非金属"),
              (GREEN_BG, GREEN, "N = noble gas 稀有气体")]
    ow = (780 - 2 * 12) / 3.0
    for i, (bg, fg, t) in enumerate(others):
        s += box(x0 + i * (ow + 12), ly2, ow, 26, bg, EDGE, 0.7, rx=5)
        s += txt(x0 + i * (ow + 12) + 10, ly2 + 13, t, 10.5, fg, "600",
                 "start")

    base = ly2 + 48
    s += note_line(x0, base, "把各个 # 连起来，就是那条楼梯状的锯齿线 staircase / zigzag line")
    s += note_line(x0, base + 20, "线的左侧＝金属，线的右侧＝非金属，线上的元素＝类金属")
    s += note_line(x0, base + 40, "两个「不老实」的元素：H 在左上角却是非金属；Al 贴着线却是金属")
    return wrap(s)


# ============================================================ Ch03 图 3-4
def fig_ch03_circuit():
    """导电性检测电路。"""
    s = head(900, 372, "图 3-4　导电性检测电路｜Conductivity Test Circuit",
             "BC Science 9 · 灯泡亮度 = 导电能力")

    # ---- 回路
    lx, rx, ty, by = 250, 650, 84, 236
    s += path(f"M{(lx + rx) / 2 - 30} {ty} L{lx} {ty} L{lx} {by} "
              f"L{(lx + rx) / 2 - 26} {by}", LINE, 1.8)
    s += path(f"M{(lx + rx) / 2 + 30} {ty} L{rx} {ty} L{rx} {by} "
              f"L{(lx + rx) / 2 + 26} {by}", LINE, 1.8)

    # ---- 电池
    s += box(418, ty - 12, 64, 24, "#FFFFFF", LINE, 1.6, rx=3)
    s += path("M432 66 L432 90", INK, 3.0)
    s += path("M444 72 L444 84", INK, 1.4)
    s += path("M456 66 L456 90", INK, 3.0)
    s += path("M468 72 L468 84", INK, 1.4)
    s += txt(450, 52, "battery 电池", 11, SUB)

    # ---- 灯泡
    s += path(f"M450 {by} L450 176", LINE, 1.8)
    s += f'  <circle cx="450" cy="150" r="20" fill="#FFF8E1" ' \
         f'stroke="{ORANGE_D}" stroke-width="1.6"/>\n'
    s += path("M438 140 L462 160", ORANGE_D, 1.6)
    s += path("M462 140 L438 160", ORANGE_D, 1.6)
    s += txt(492, 150, "lamp 灯泡", 11.5, SUB, "400", "start")

    # ---- 样品
    s += path(f"M450 {by - 8} L450 272", LINE, 1.8)
    s += box(320, 272, 260, 44, NEUTRAL_BG, LINE, 1.2, rx=6)
    s += txt(450, 294, "待测样品 sample", 13, INK, "700")
    s += txt(600, 294, "← 把样品串接进电路", 10.5, SUB, "400", "start")

    # ---- 判据三栏
    rows = [("灯泡明亮", "good conductor 良导体", "多为金属 metal", GREEN_BG, GREEN),
            ("灯泡不亮", "poor conductor 不良导体", "多为非金属 non-metal", ORANGE_BG, ORANGE_D),
            ("灯泡暗 / 时亮时暗", "semiconductor 半导体", "多为类金属 metalloid（如 Si）", "#FFF8E1", ORANGE_D)]
    cw = 262
    for i, (a, b, c, bg, fg) in enumerate(rows):
        x = 42 + i * (cw + 27)
        s += box(x, 92, cw, 150, bg, EDGE, 0.9, rx=8)
        s += f'  <circle cx="{x + cw / 2}" cy="132" r="16" fill="#FFFFFF" ' \
             f'stroke="{fg}" stroke-width="1.4"/>\n'
        s += txt(x + cw / 2, 132, "", 10)
        if i == 0:
            s += path(f"M{x + cw / 2 - 9} 132 L{x + cw / 2 + 9} 132", ORANGE_D, 1.4)
            s += path(f"M{x + cw / 2} 123 L{x + cw / 2} 141", ORANGE_D, 1.4)
        elif i == 1:
            s += path(f"M{x + cw / 2 - 8} 132 L{x + cw / 2 + 8} 132", LINE, 1.4)
        else:
            s += path(f"M{x + cw / 2 - 8} 132 L{x + cw / 2 + 8} 132", ORANGE_D, 1.4)
            s += f'  <circle cx="{x + cw / 2}" cy="132" r="16" fill="#FFFFFF" ' \
                 f'stroke="{ORANGE_D}" stroke-width="1.4" stroke-dasharray="3 3"/>\n'
        s += txt(x + cw / 2, 168, a, 12.5, INK, "700")
        s += txt(x + cw / 2, 190, b, 11, fg, "600")
        s += txt(x + cw / 2, 210, c, 10.5, SUB)

    s += box(42, 330, 816, 30, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(450, 345, "对照实验 control：用一段已知铜线接入，确认电路本身完好",
             11.5, INK, "600")
    return wrap(s)


# ============================================================ Ch04 图 4-1
def fig_ch04_families():
    """四大族在周期表上的位置。"""
    s = head(900, 470, "图 4-1　四大族在周期表上的位置｜Where the Families Live",
             "BC Science 9 · 活泼的都在边缘")
    cols = [("1", BLUE_BG, BLUE_D), ("2", BLUE_BG, BLUE_D),
            ("3-12", NEUTRAL_BG, SUB), ("17", ORANGE_BG, ORANGE_D),
            ("18", GREEN_BG, GREEN)]
    x0, rl = 44, 96
    cw = (900 - x0 * 2 - rl) / 5.0
    gx, y0, hh, rh = x0 + rl, 70, 30, 38

    s += box(x0, y0, rl, hh, NEUTRAL_BG, EDGE, 0.8, rx=4)
    s += txt(x0 + rl / 2, y0 + hh / 2, "Group", 11, SUB, "700")
    for i, (c, bg, fg) in enumerate(cols):
        s += box(gx + i * cw, y0, cw, hh, bg, EDGE, 0.8, rx=4)
        s += txt(gx + i * cw + cw / 2, y0 + hh / 2, c, 13, fg, "700")

    rows = [
        ("Period 1", ["H*", "", "", "", "He"]),
        ("Period 2", ["Li", "Be", "", "F", "Ne"]),
        ("Period 3", ["Na", "Mg", "", "Cl", "Ar"]),
        ("Period 4", ["K", "Ca", "Sc … Zn", "Br", "Kr"]),
        ("Period 5", ["Rb", "Sr", "Y … Cd", "I", "Xe"]),
        ("Period 6", ["Cs", "Ba", "La … Hg", "At", "Rn"]),
        ("Period 7", ["Fr", "Ra", "Ac … Cn", "(Ts)", "(Og)"]),
    ]
    for ri, (lab, cells) in enumerate(rows):
        cy = y0 + hh + ri * rh
        s += box(x0, cy, rl, rh, "#FFFFFF", EDGE, 0.8, rx=4)
        s += txt(x0 + rl / 2, cy + rh / 2, lab, 11, SUB, "600")
        for ci, v in enumerate(cells):
            cx = gx + ci * cw
            s += box(cx + 2, cy + 2, cw - 4, rh - 4, "#FFFFFF", EDGE, 0.6, rx=4)
            if v:
                s += txt(cx + cw / 2, cy + rh / 2, v, 12.5, INK, "600")

    notes = [("第 1 列 = Group 1", "碱金属 alkali metals（H* 不是碱金属，它只是个非金属邻居）", BLUE_D),
             ("第 2 列 = Group 2", "碱土金属 alkaline earth metals", BLUE_D),
             ("中间 = Group 3–12", "过渡元素 transition elements（全是金属）", SUB),
             ("倒数第二 = Group 17", "卤素 halogens", ORANGE_D),
             ("最后一列 = Group 18", "稀有气体 noble gases", GREEN)]
    base = y0 + hh + 7 * rh + 26
    for i, (a, b, col) in enumerate(notes):
        cx = x0 if i % 2 == 0 else 470
        cy = base + (i // 2) * 24
        s += txt(cx, cy, a, 11.5, col, "700", "start")
        s += txt(cx + 150, cy, b, 11, SUB, "400", "start")
    return wrap(s)


# ============================================================ Ch04 图 4-2
def fig_ch04_trends():
    """两条活性趋势。"""
    s = head(900, 452, "图 4-2　两条活性趋势｜Reactivity Trends",
             "BC Science 9 · 金属往下更猛，非金属往下更懒")
    s += ARROW_DEF

    s += txt(190, 74, "Group 1 碱金属 alkali metals", 13, BLUE_D, "700")
    s += txt(710, 74, "Group 17 卤素 halogens", 13, ORANGE_D, "700")

    left = ["Li", "Na", "K", "Rb", "Cs"]
    right = ["F", "Cl", "Br", "I", "At"]
    bw, bh, y0 = 140, 40, 96
    for i, e in enumerate(left):
        s += box(120, y0 + i * 46, bw, bh, BLUE_BG, BLUE, 1.0, rx=6)
        s += txt(190, y0 + i * 46 + bh / 2, e, 16, BLUE_D, "700")
    for i, e in enumerate(right):
        s += box(640, y0 + i * 46, bw, bh, ORANGE_BG, ORANGE, 1.0, rx=6)
        s += txt(710, y0 + i * 46 + bh / 2, e, 16, ORANGE_D, "700")

    # 左：向上箭头 = 活泼性增强
    s += path("M300 306 L300 100", BLUE, 2.4, marker="ar")
    s += txt(316, 120, "reactivity", 11.5, BLUE_D, "700", "start")
    s += txt(316, 138, "INCREASES", 11.5, BLUE_D, "700", "start")
    s += txt(316, 156, "活泼性增强 ↑", 11.5, BLUE_D, "600", "start")
    s += txt(316, 182, "越往下越容易", 10.5, SUB, "400", "start")
    s += txt(316, 198, "丢掉最外层电子", 10.5, SUB, "400", "start")

    # 右：向下箭头 = 活泼性减弱
    s += path("M820 100 L820 306", ORANGE, 2.4, marker="ar")
    s += txt(836, 120, "reactivity", 11.5, ORANGE_D, "700", "start")
    s += txt(836, 138, "DECREASES", 11.5, ORANGE_D, "700", "start")
    s += txt(836, 156, "活泼性减弱 ↓", 11.5, ORANGE_D, "600", "start")
    s += txt(836, 182, "越往下越难", 10.5, SUB, "400", "start")
    s += txt(836, 198, "抢到 1 个电子", 10.5, SUB, "400", "start")

    s += box(60, 340, 780, 92, NEUTRAL_BG, EDGE, 0.9, rx=8)
    s += txt(450, 360, "共同原因 the same root cause：越往下原子越大、电子层越多", 12.5,
             INK, "700")
    s += txt(450, 384, "碱金属靠「丢掉」最外层电子　→　丢得越容易　⇒　越活泼　↑",
             11.5, BLUE_D)
    s += txt(450, 406, "卤素靠「抢来」一个电子　　→　抢得越困难　⇒　越不活泼　↓",
             11.5, ORANGE_D)
    return wrap(s)


# ============================================================ Ch04 图 4-3
def fig_ch04_diatomic():
    """七种双原子分子。"""
    s = head(900, 372, "图 4-3　七种双原子分子｜The Seven Diatomic Molecules",
             "BC Science 9 · 只有这七种，游离态必须写下标 2")

    items = [("H", "H₂", "氢气", "气体"), ("N", "N₂", "氮气", "气体"),
             ("O", "O₂", "氧气", "气体"), ("F", "F₂", "氟气", "气体"),
             ("Cl", "Cl₂", "氯气", "气体"), ("Br", "Br₂", "溴", "液体"),
             ("I", "I₂", "碘", "固体")]
    bw, gap, x0 = 108, 14, 23
    for i, (sym, formula, cn, state) in enumerate(items):
        x = x0 + i * (bw + gap)
        s += box(x, 82, bw, 150, "#FFFFFF", EDGE, 0.9, rx=8)
        s += dot(x + bw / 2 - 24, 122, 17, BLUE_BG, BLUE, 1.4)
        s += dot(x + bw / 2 + 24, 122, 17, BLUE_BG, BLUE, 1.4)
        s += path(f"M{x + bw / 2 - 8} 122 L{x + bw / 2 + 8} 122", BLUE, 2.2)
        s += txt(x + bw / 2 - 24, 122, sym, 12, BLUE_D, "700")
        s += txt(x + bw / 2 + 24, 122, sym, 12, BLUE_D, "700")
        s += txt(x + bw / 2, 168, formula, 17, INK, "700")
        s += txt(x + bw / 2, 192, cn, 12, INK, "600")
        bg = ORANGE_BG if state != "气体" else NEUTRAL_BG
        s += box(x + 10, 206, bw - 20, 20, bg, EDGE, 0.6, rx=4)
        s += txt(x + bw / 2, 216, state, 10.5, SUB)

    s += path("M40 254 L860 254", EDGE, 1.0)
    s += txt(450, 274, "共 7 种 diatomic molecules：H  N  O  F  Cl  Br  I　　英文记忆：BrINClHOF",
             12.5, INK, "600")
    s += box(40, 288, 820, 32, ORANGE_BG, ORANGE, 1.0, rx=6)
    s += txt(450, 304, "写法铁律：这七种元素的游离态必须加下标 2（写 O₂、N₂、H₂ 而不是 O、N、H）",
             12.5, ORANGE_D, "700")
    s += txt(450, 336, "反例对照（不要写 ₂！）　稀有气体：He  Ne  Ar  Kr  Xe  Rn ← 单原子 monatomic",
             11.5, SUB)
    s += txt(450, 356, "金属：Fe  Na  Cu  Ag  Au ← 直接用元素符号", 11.5, SUB)
    return wrap(s)


# ============================================================ Ch04 图 4-4
def fig_ch04_noble():
    """为什么稀有气体「什么都不做」。"""
    s = head(900, 392, "图 4-4　为什么稀有气体「什么都不做」｜Why Noble Gases Are Unreactive",
             "BC Science 9 · 满的价电子层 = 稳定 = 惰性")

    s += box(60, 62, 780, 176, GREEN_BG, GREEN, 1.2, rx=10)
    s += txt(450, 88, "Noble gases 稀有气体：最外层已经是「满」的状态", 14, GREEN, "700")
    rows = [("He", "氦", "只有第 1 层，2 个电子", "该层已满（2/2）"),
            ("Ne", "氖", "最外层 8 个电子", "已 满（8/8）"),
            ("Ar", "氩", "最外层 8 个电子", "已 满（8/8）")]
    for i, (sym, cn, a, b) in enumerate(rows):
        y = 122 + i * 36
        s += badge(110, y, 13, str(i + 1), GREEN)
        s += txt(140, y, sym, 14, GREEN, "700", "start")
        s += txt(176, y, cn, 12, INK, "400", "start")
        s += txt(300, y, a, 12, INK, "400", "start")
        s += txt(520, y, "→", 12, GREEN, "700", "start")
        s += txt(560, y, b, 12.5, GREEN, "700", "start")

    s += box(60, 252, 780, 96, ORANGE_BG, ORANGE, 1.2, rx=10)
    s += txt(450, 274, "对比 People who are NOT satisfied：", 13, ORANGE_D, "700")
    cmp_rows = [("第 1 族 Na", "最外层 1 个", "丢掉它最省事", "Na⁺  (+1)", BLUE_D),
                ("第 17 族 Cl", "最外层 7 个", "再补 1 个最省事", "Cl⁻  (−1)", ORANGE_D),
                ("第 18 族 Ar", "已满", "既不想丢也不想补", "不变化 (0)", GREEN)]
    for i, (a, b, c, d, col) in enumerate(cmp_rows):
        y = 300 + i * 0  # 单行横排
        x = 92 + i * 250
        s += txt(x, y, a, 12, INK, "700", "start")
        s += txt(x, y + 20, f"{b} → {c}", 11, SUB, "400", "start")
        s += txt(x + 190, y + 10, d, 13, col, "700", "end")

    s += box(60, 358, 780, 26, NEUTRAL_BG, EDGE, 0.8, rx=6)
    s += txt(450, 371, "⇒ full valence shell 满的价电子层 = stable 稳定 = inert 惰性",
             12.5, INK, "700")
    return wrap(s)


# ============================================================ Ch04 图 4-5
def fig_ch04_predict_flow():
    """预测五步流程。"""
    s = head(900, 214, "图 4-5　预测五步流程｜Prediction Flowchart",
             "BC Science 9 · 不做实验也能推出性质")
    s += ARROW_DEF
    steps = [("①", "position", "定位：周期 + 族"),
             ("②", "family", "归类：属于哪一族"),
             ("③", "analogue", "同族类比：共性"),
             ("④", "trend", "用趋势修正"),
             ("⑤", "prediction", "表述为可检验的预测")]
    bw, gap, x0 = 152, 24, 22
    for i, (num, en, cn) in enumerate(steps):
        x = x0 + i * (bw + gap)
        s += box(x, 96, bw, 74, BLUE_BG, BLUE, 1.2, rx=8)
        s += txt(x + bw / 2, 118, num + " " + en, 13.5, BLUE_D, "700")
        s += txt(x + bw / 2, 142, cn, 11.5, INK, "600")
        if i < 4:
            s += path(f"M{x + bw + 3} 133 L{x + bw + gap - 3} 133", BLUE, 1.8,
                      marker="ar")
    return wrap(s)


FIGURES = {
    "ch02-periodic-table-cell.svg": fig_ch02_cell,
    "periodic-table-1-20-simple.svg": fig_periodic_simple,
    "ch02-isotopes-carbon.svg": fig_ch02_isotopes,
    "ch02-mass-vs-number-order.svg": fig_ch02_mass_vs_number,
    "ch03-periodic-table-map.svg": fig_ch03_map,
    "ch03-zigzag-regions.svg": fig_ch03_zigzag,
    "ch03-conductivity-test.svg": fig_ch03_circuit,
    "ch04-family-locations.svg": fig_ch04_families,
    "ch04-reactivity-trends.svg": fig_ch04_trends,
    "ch04-diatomic-seven.svg": fig_ch04_diatomic,
    "ch04-noble-gas-stability.svg": fig_ch04_noble,
    "ch04-prediction-flowchart.svg": fig_ch04_predict_flow,
}


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    os.makedirs(FIG_DIR, exist_ok=True)
    for name, fn in FIGURES.items():
        if want and want not in name:
            continue
        p = os.path.join(FIG_DIR, name)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(fn())
        print("OK  " + name)


if __name__ == "__main__":
    main()
