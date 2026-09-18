# -*- coding: utf-8 -*-
"""
生成 BC Science 9 化学单元讲义的 SVG 图表
数据源与前 20 号元素表（附录 D）保持一致

用法:
  python build_figures.py <输出目录>

生成:
  periodic-table-1-20-bilingual.svg   前 20 号元素中英双语周期表
  periodic-table-blank.svg            空白周期表（默测用）
  bohr-diagrams-1-20.svg              前 20 号元素玻尔模型图总表
"""
import sys
import os

# ---------------------------------------------------------------- 元素数据
# (Z, symbol, en, zh, pinyin, period, group, category, shells, mass_number)
# shells: 电子层排布（前 20 号按 2, 8, 8, n 填充）
# category: metal / metalloid / nonmetal / noble
ELEMENTS = [
    (1,  "H",  "hydrogen",  "氢", "qīng",  1, 1,  "nonmetal",  [1],          1),
    (2,  "He", "helium",    "氦", "hài",   1, 18, "noble",     [2],          4),
    (3,  "Li", "lithium",   "锂", "lǐ",    2, 1,  "metal",     [2, 1],       7),
    (4,  "Be", "beryllium", "铍", "pí",    2, 2,  "metal",     [2, 2],       9),
    (5,  "B",  "boron",     "硼", "péng",  2, 13, "metalloid", [2, 3],       11),
    (6,  "C",  "carbon",    "碳", "tàn",   2, 14, "nonmetal",  [2, 4],       12),
    (7,  "N",  "nitrogen",  "氮", "dàn",   2, 15, "nonmetal",  [2, 5],       14),
    (8,  "O",  "oxygen",    "氧", "yǎng",  2, 16, "nonmetal",  [2, 6],       16),
    (9,  "F",  "fluorine",  "氟", "fú",    2, 17, "nonmetal",  [2, 7],       19),
    (10, "Ne", "neon",      "氖", "nǎi",   2, 18, "noble",     [2, 8],       20),
    (11, "Na", "sodium",    "钠", "nà",    3, 1,  "metal",     [2, 8, 1],    23),
    (12, "Mg", "magnesium", "镁", "měi",   3, 2,  "metal",     [2, 8, 2],    24),
    (13, "Al", "aluminium", "铝", "lǚ",    3, 13, "metal",     [2, 8, 3],    27),
    (14, "Si", "silicon",   "硅", "guī",   3, 14, "metalloid", [2, 8, 4],    28),
    (15, "P",  "phosphorus","磷", "lín",   3, 15, "nonmetal",  [2, 8, 5],    31),
    (16, "S",  "sulfur",    "硫", "liú",   3, 16, "nonmetal",  [2, 8, 6],    32),
    (17, "Cl", "chlorine",  "氯", "lǜ",    3, 17, "nonmetal",  [2, 8, 7],    35),
    (18, "Ar", "argon",     "氩", "yà",    3, 18, "noble",     [2, 8, 8],    40),
    (19, "K",  "potassium", "钾", "jiǎ",   4, 1,  "metal",     [2, 8, 8, 1], 39),
    (20, "Ca", "calcium",   "钙", "gài",   4, 2,  "metal",     [2, 8, 8, 2], 40),
]

# ---------------------------------------------------------------- 样式
FONT = "'Segoe UI', 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', Arial, sans-serif"

CAT = {
    "metal":     {"fill": "#E6F1FB", "stroke": "#185FA5", "text": "#0C447C"},
    "metalloid": {"fill": "#EAF3DE", "stroke": "#639922", "text": "#3B6D11"},
    "nonmetal":  {"fill": "#FAEEDA", "stroke": "#BA7517", "text": "#854F0B"},
    "noble":     {"fill": "#EEEDFE", "stroke": "#7F77DD", "text": "#3C3489"},
}
NEUTRAL = {"fill": "#FFFFFF", "stroke": "#B4B2A9", "text": "#5F5E5A"}

INK = "#2C2C2A"
MUTED = "#5F5E5A"
HINT = "#888780"
GRID = "#B4B2A9"


def svg_open(w, h, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'font-family="{FONT}">\n'
        f'  <title>{title}</title>\n'
        f'  <rect width="{w}" height="{h}" fill="#FFFFFF"/>\n'
    )


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- 周期表
# 列位置：1, 2 族靠左，13–18 族靠右，中间为过渡元素预留空间
CELL_W, CELL_H, STEP = 52, 58, 54
COL_X = {1: 62, 2: 116, 13: 226, 14: 280, 15: 334, 16: 388, 17: 442, 18: 496}
ROW_Y = {1: 70, 2: 128, 3: 186, 4: 244}
PW, PH = 570, 420

GROUPS = [1, 2, 13, 14, 15, 16, 17, 18]
GROUP_CN = {1: "碱金属", 2: "碱土金属", 13: "硼族", 14: "碳族",
            15: "氮族", 16: "氧族", 17: "卤素", 18: "稀有气体"}


def grid(blank=False):
    """画出周期表格子；blank=True 时只保留原子序数"""
    out = []
    for (z, sym, en, zh, py, per, grp, cat, shells, mass) in ELEMENTS:
        x, y = COL_X[grp], ROW_Y[per]
        st = NEUTRAL if blank else CAT[cat]
        out.append(
            f'  <rect x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" rx="6" '
            f'fill="{st["fill"]}" stroke="{st["stroke"]}" stroke-width="{0.9 if not blank else 0.7}"/>'
        )
        out.append(
            f'  <text x="{x + 5}" y="{y + 12}" font-size="9" fill="{HINT}">{z}</text>'
        )
        if not blank:
            out.append(
                f'  <text x="{x + CELL_W / 2:.0f}" y="{y + 27}" font-size="16" font-weight="600" '
                f'fill="{st["text"]}" text-anchor="middle">{sym}</text>'
            )
            out.append(
                f'  <text x="{x + CELL_W / 2:.0f}" y="{y + 41}" font-size="11" '
                f'fill="{st["text"]}" text-anchor="middle">{zh}</text>'
            )
            out.append(
                f'  <text x="{x + CELL_W / 2:.0f}" y="{y + 52}" font-size="7.5" '
                f'fill="{MUTED}" text-anchor="middle">{en}</text>'
            )
    return "\n".join(out)


def table_frame():
    out = []
    # 族号表头
    for g in GROUPS:
        x = COL_X[g]
        out.append(
            f'  <text x="{x + CELL_W / 2:.0f}" y="52" font-size="12" font-weight="600" '
            f'fill="{INK}" text-anchor="middle">{g}</text>'
        )
        out.append(
            f'  <text x="{x + CELL_W / 2:.0f}" y="64" font-size="8.5" '
            f'fill="{HINT}" text-anchor="middle">{esc(GROUP_CN[g])}</text>'
        )
    # 周期号
    for p in (1, 2, 3, 4):
        y = ROW_Y[p]
        out.append(
            f'  <text x="44" y="{y + CELL_H / 2:.0f}" font-size="12" font-weight="600" '
            f'fill="{INK}" text-anchor="middle" dominant-baseline="central">{p}</text>'
        )
    out.append(
        f'  <text x="44" y="52" font-size="9" fill="{HINT}" text-anchor="middle">周期</text>'
    )
    out.append(
        f'  <text x="44" y="64" font-size="8.5" fill="{HINT}" text-anchor="middle">period</text>'
    )
    # 过渡元素占位
    out.append(
        f'  <rect x="172" y="70" width="50" height="232" rx="6" fill="#F7F6F2" '
        f'stroke="{GRID}" stroke-width="0.7" stroke-dasharray="3 3"/>'
    )
    out.append(
        f'  <text transform="rotate(-90 197 186)" x="197" y="186" font-size="9" '
        f'fill="{HINT}" text-anchor="middle" dominant-baseline="central">过渡元素 transition elements 3–12</text>'
    )
    return "\n".join(out)


def legend():
    """2 行 × 2 列图例，避免文字挤出画布"""
    items = [
        ("metal", "金属 metal", "左侧，导电导热、有延展性"),
        ("metalloid", "类金属 semi-metal", "锯齿线两侧，性质居中"),
        ("nonmetal", "非金属 non-metal", "右侧，多为气体或脆性固体"),
        ("noble", "稀有气体 noble gas", "第 18 族，价电子层已满"),
    ]
    out = []
    for idx, (key, name, desc) in enumerate(items):
        c, r = idx % 2, idx // 2
        x = 62 + c * 250
        y = 324 + r * 22
        st = CAT[key]
        out.append(
            f'  <rect x="{x}" y="{y}" width="15" height="15" rx="4" fill="{st["fill"]}" '
            f'stroke="{st["stroke"]}" stroke-width="0.9"/>'
        )
        out.append(f'  <text x="{x + 21}" y="{y + 11}" font-size="11" fill="{INK}">{esc(name)}</text>')
        out.append(f'  <text x="{x + 21 + 10 * len(name) * 0.62 + 12:.0f}" y="{y + 11}" '
                   f'font-size="9.5" fill="{HINT}">{esc(desc)}</text>')
    return "\n".join(out)


def build_periodic_table(path):
    s = [svg_open(PW, PH, "前 20 号元素中英双语周期表")]
    s.append(f'  <text x="30" y="28" font-size="19" font-weight="600" fill="{INK}">'
             f'前 20 号元素周期表｜Periodic Table, Elements 1–20</text>')
    s.append(f'  <text x="540" y="28" font-size="10.5" fill="{MUTED}" text-anchor="end">'
             f'BC Science 9 · 英中对照</text>')
    s.append(table_frame())
    s.append(grid(blank=False))
    s.append(legend())
    s.append(f'  <text x="30" y="384" font-size="10" fill="{HINT}">'
             f'格内自上而下：原子序数 atomic number ／ 元素符号 symbol ／ 中文名 ／ 英文名</text>')
    s.append(f'  <text x="30" y="400" font-size="10" fill="{HINT}">'
             f'方格颜色 = 元素类别；同一纵列为同一族 group，价电子数相同，化学性质相似。</text>')
    s.append('</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")


def build_blank_table(path):
    s = [svg_open(PW, PH, "空白周期表（前 20 号元素）")]
    s.append(f'  <text x="30" y="28" font-size="19" font-weight="600" fill="{INK}">'
             f'空白周期表｜Blank Periodic Table (1–20)</text>')
    s.append(f'  <text x="540" y="28" font-size="10.5" fill="{MUTED}" text-anchor="end">'
             f'默测用 · 填符号与中英文名称</text>')
    s.append(table_frame())
    s.append(grid(blank=True))
    s.append(f'  <text x="30" y="330" font-size="10.5" fill="{MUTED}">'
             f'填写：元素符号 symbol ／ 中文名 ／ 英文名　（格子左下角数字为原子序数）</text>')
    s.append(f'  <text x="30" y="352" font-size="10" fill="{HINT}">'
             f'自测方式：先默符号，再默中文名，最后默英文名；三遍全对才算过关。</text>')
    s.append(f'  <text x="30" y="370" font-size="10" fill="{HINT}">'
             f'提示：Na 钠 nà ／ Cl 氯 lǜ ／ Al 铝 lǚ —— 拼音读错，符号就容易写错。</text>')
    s.append('</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")


# ---------------------------------------------------------------- 玻尔图
import math

BW_COLS, BW_CELL = 5, 190
BW_W = 40 + BW_COLS * BW_CELL + 20
BW_ROWS = 4
BW_H = 70 + BW_ROWS * BW_CELL + 30

SHELL_R = {1: 30, 2: 50, 3: 70, 4: 88}
SHELL_NAME = {1: "K", 2: "L", 3: "M", 4: "N"}
SHELL_CAP = {1: 2, 2: 8, 3: 8, 4: 18}


def bohr_unit(cx, cy, el, show_inner=True):
    z, sym, en, zh, py, per, grp, cat, shells, mass = el
    neutrons = mass - z
    out = []
    # 电子层
    for i, n in enumerate(shells, start=1):
        r = SHELL_R[i]
        out.append(
            f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GRID}" stroke-width="0.8"/>'
        )
    # 电子
    for i, n in enumerate(shells, start=1):
        r = SHELL_R[i]
        for k in range(n):
            ang = -math.pi / 2 + k * 2 * math.pi / n
            ex = cx + r * math.cos(ang)
            ey = cy + r * math.sin(ang)
            out.append(f'  <circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.6" fill="#185FA5"/>')
    # 原子核
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="17" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.9"/>')
    out.append(f'  <text x="{cx}" y="{cy - 4}" font-size="8" fill="#854F0B" '
               f'text-anchor="middle">{z} p⁺</text>')
    out.append(f'  <text x="{cx}" y="{cy + 7}" font-size="8" fill="#854F0B" '
               f'text-anchor="middle">{neutrons} n⁰</text>')
    # 标签
    out.append(f'  <text x="{cx - 92}" y="{cy - 82}" font-size="13" font-weight="600" fill="{INK}">'
               f'{z} {sym} {zh}</text>')
    out.append(f'  <text x="{cx - 92}" y="{cy - 68}" font-size="9.5" fill="{MUTED}">{en}</text>')
    # 排布与价电子
    valence = shells[-1]
    out.append(f'  <text x="{cx + 92}" y="{cy - 82}" font-size="10" fill="{HINT}" text-anchor="end">'
               f'{", ".join(str(n) for n in shells)}</text>')
    out.append(f'  <text x="{cx + 92}" y="{cy - 68}" font-size="9.5" fill="#A32D2D" text-anchor="end">'
               f'价电子 {valence}</text>')
    return "\n".join(out)


def build_bohr(path):
    s = [svg_open(BW_W, BW_H, "前 20 号元素玻尔模型图")]
    s.append(f'  <text x="30" y="30" font-size="19" font-weight="600" fill="{INK}">'
             f'前 20 号元素玻尔模型图｜Bohr Diagrams, Elements 1–20</text>')
    s.append(f'  <text x="{BW_W - 30}" y="30" font-size="10.5" fill="{MUTED}" text-anchor="end">'
             f'BC Science 9 · 电子层容量 2, 8, 8</text>')
    for idx, el in enumerate(ELEMENTS):
        c, r = idx % BW_COLS, idx // BW_COLS
        cx = 40 + c * BW_CELL + BW_CELL / 2
        cy = 70 + r * BW_CELL + BW_CELL / 2
        s.append(bohr_unit(cx, cy, el))
    y = BW_H - 20
    s.append(f'  <text x="30" y="{y}" font-size="10" fill="{HINT}">'
             f'每个原子右侧小字为电子层排布（由内向外）与价电子数；原子核内标注质子数 p⁺ 与中子数 n⁰（以最常见同位素计）。</text>')
    s.append('</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")


# ---------------------------------------------------------------- 路易斯点式
LW_W, LW_H = 900, 580
LW_COL = [135 + i * 90 for i in range(8)]          # 8 个族列
LW_GRP = [1, 2, 13, 14, 15, 16, 17, 18]
LW_GRP_CN = {1: "碱金属", 2: "碱土金属", 13: "硼族", 14: "碳族",
             15: "氮族", 16: "氧族", 17: "卤素", 18: "稀有气体"}
LW_ROW = {"1": 125, "2": 210, "3": 296}

# (period, [(symbol, en, zh, group, valence)])
LW_ATOMS = [
    ("1", [("H", "hydrogen", "氢", 1, 1), ("He", "helium", "氦", 18, 2)]),
    ("2", [("Li", "lithium", "锂", 1, 1), ("Be", "beryllium", "铍", 2, 2),
           ("B", "boron", "硼", 13, 3), ("C", "carbon", "碳", 14, 4),
           ("N", "nitrogen", "氮", 15, 5), ("O", "oxygen", "氧", 16, 6),
           ("F", "fluorine", "氟", 17, 7), ("Ne", "neon", "氖", 18, 8)]),
    ("3", [("Na", "sodium", "钠", 1, 1), ("Mg", "magnesium", "镁", 2, 2),
           ("Al", "aluminium", "铝", 13, 3), ("Si", "silicon", "硅", 14, 4),
           ("P", "phosphorus", "磷", 15, 5), ("S", "sulfur", "硫", 16, 6),
           ("Cl", "chlorine", "氯", 17, 7), ("Ar", "argon", "氩", 18, 8)]),
]

# (symbol, zh, charge_label, group, kind)
LW_IONS = [
    ("Na", "钠", "⁺", 1, "cation"),
    ("Mg", "镁", "²⁺", 2, "cation"),
    ("Al", "铝", "³⁺", 13, "cation"),
    ("N", "氮", "³⁻", 15, "anion"),
    ("O", "氧", "²⁻", 16, "anion"),
    ("Cl", "氯", "⁻", 17, "anion"),
]


def dot_positions(cx, cy, n):
    """上 → 右 → 下 → 左 各放 1 个，超过 4 个再依次配对"""
    single = {0: (cx, cy - 15), 1: (cx + 17, cy - 4),
              2: (cx, cy + 16), 3: (cx - 17, cy - 4)}
    pair = {0: ((cx - 5.5, cy - 15), (cx + 5.5, cy - 15)),
            1: ((cx + 17, cy - 9.5), (cx + 17, cy + 1.5)),
            2: ((cx - 5.5, cy + 16), (cx + 5.5, cy + 16)),
            3: ((cx - 17, cy - 9.5), (cx - 17, cy + 1.5))}
    singles, pairs = min(n, 4), max(0, n - 4)
    pts = []
    for i in range(4):
        if i < pairs:
            pts.extend(pair[i])
        elif i < singles:
            pts.append(single[i])
    return pts


def lewis_atom(cx, cy, sym, zh, n, note=""):
    out = []
    for (px, py) in dot_positions(cx, cy, n):
        out.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="#185FA5"/>')
    out.append(f'  <text x="{cx}" y="{cy}" font-size="15" font-weight="600" fill="{INK}" '
               f'text-anchor="middle" dominant-baseline="central">{sym}</text>')
    out.append(f'  <text x="{cx}" y="{cy + 31}" font-size="9" fill="{HINT}" '
               f'text-anchor="middle">{n} e⁻</text>')
    return "\n".join(out)


def lewis_ion(cx, cy, sym, zh, charge, kind):
    out = []
    half = len(sym) * 4.6 + 3
    if kind == "anion":
        for (px, py) in dot_positions(cx, cy, 8):
            out.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="2.4" fill="#A32D2D"/>')
        out.append(f'  <text x="{cx - 21}" y="{cy}" font-size="26" fill="#A32D2D" '
                   f'text-anchor="middle" dominant-baseline="central">[</text>')
        out.append(f'  <text x="{cx + 21}" y="{cy}" font-size="26" fill="#A32D2D" '
                   f'text-anchor="middle" dominant-baseline="central">]</text>')
        col = "#A32D2D"
    else:
        col = "#185FA5"
    out.append(f'  <text x="{cx}" y="{cy}" font-size="15" font-weight="600" fill="{INK}" '
               f'text-anchor="middle" dominant-baseline="central">{sym}</text>')
    out.append(f'  <text x="{cx + half:.1f}" y="{cy - 11}" font-size="11" font-weight="600" '
               f'fill="{col}">{charge}</text>')
    out.append(f'  <text x="{cx}" y="{cy + 31}" font-size="9" fill="{HINT}" '
               f'text-anchor="middle">{zh}离子</text>')
    return "\n".join(out)


def build_lewis(path):
    s = [svg_open(LW_W, LW_H, "主族元素路易斯点式总表")]
    s.append(f'  <text x="30" y="30" font-size="19" font-weight="600" fill="{INK}">'
             f'主族元素路易斯点式｜Lewis Dot Diagrams</text>')
    s.append(f'  <text x="870" y="30" font-size="10.5" fill="{MUTED}" text-anchor="end">'
             f'BC Science 9 · 价电子 = 族号的个位数</text>')

    for i, g in enumerate(LW_GRP):
        cx = LW_COL[i]
        s.append(f'  <text x="{cx}" y="62" font-size="12.5" font-weight="600" fill="{INK}" '
                 f'text-anchor="middle">{g}</text>')
        s.append(f'  <text x="{cx}" y="78" font-size="8.5" fill="{HINT}" '
                 f'text-anchor="middle">{esc(LW_GRP_CN[g])}</text>')

    for per, atoms in LW_ATOMS:
        cy = LW_ROW[per]
        s.append(f'  <text x="78" y="{cy}" font-size="10" fill="{MUTED}" text-anchor="end" '
                 f'dominant-baseline="central">第 {per} 周期</text>')
        for (sym, en, zh, grp, n) in atoms:
            cx = LW_COL[LW_GRP.index(grp)]
            z = next(e[0] for e in ELEMENTS if e[1] == sym)
            s.append(f'  <text x="{cx}" y="{cy - 31}" font-size="9" fill="{MUTED}" '
                     f'text-anchor="middle">{z} {sym} {zh}</text>')
            s.append(lewis_atom(cx, cy, sym, zh, n))
            if sym == "He":
                s.append(f'  <text x="{cx}" y="{cy + 45}" font-size="8" fill="#A32D2D" '
                         f'text-anchor="middle">二重规则例外</text>')

    s.append(f'  <path d="M30 348 L870 348" stroke="{GRID}" stroke-width="0.8" stroke-dasharray="4 3" fill="none"/>')
    s.append(f'  <text x="30" y="372" font-size="12.5" font-weight="600" fill="{INK}">'
             f'常见离子的点式｜Lewis diagrams of ions</text>')

    icy = 436
    s.append(f'  <rect x="96" y="{icy - 34}" width="270" height="80" rx="9" fill="#E6F1FB" '
             f'stroke="#185FA5" stroke-width="0.7"/>')
    s.append(f'  <rect x="450" y="{icy - 34}" width="270" height="80" rx="9" fill="#FCEBEB" '
             f'stroke="#A32D2D" stroke-width="0.7"/>')
    s.append(f'  <text x="78" y="{icy}" font-size="10" fill="{MUTED}" text-anchor="end" '
             f'dominant-baseline="central">离子</text>')
    for (sym, zh, charge, grp, kind) in LW_IONS:
        cx = LW_COL[LW_GRP.index(grp)]
        s.append(lewis_ion(cx, icy, sym, zh, charge, kind))
    s.append(f'  <text x="231" y="{icy + 60}" font-size="10" fill="#185FA5" text-anchor="middle">'
             f'阳离子 cation：失去价电子，0 个点</text>')
    s.append(f'  <text x="585" y="{icy + 60}" font-size="10" fill="#A32D2D" text-anchor="middle">'
             f'阴离子 anion：得到电子至满 8 个，加方括号</text>')

    s.append(f'  <text x="30" y="508" font-size="10" fill="{HINT}">'
             f'点的放置顺序：上 → 右 → 下 → 左 各放 1 个；超过 4 个电子后再依次配对（第 5 个回到上方配对）。</text>')
    s.append(f'  <text x="30" y="526" font-size="10" fill="{HINT}">'
             f'价电子数 8（最外层满）= 稳定，这就是稀有气体几乎不反应的原因；H 与 He 例外，2 个即满（二重规则 duet rule）。</text>')
    s.append(f'  <text x="30" y="544" font-size="10" fill="{HINT}">'
             f'过渡元素（第 3–12 族）的点式在 9 年级不要求，故本表只列主族元素。</text>')
    s.append(f'  <text x="30" y="564" font-size="10" fill="{HINT}">'
             f'对应章节：Ch.6 离子与路易斯点式；离子点式是 Ch.7 写离子化合物化学式与命名的基础。</text>')
    s.append('</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")


# ---------------------------------------------------------------- 玻尔图模板
BT_W, BT_H = 880, 600
BT_R = [26, 42, 58, 74]
BT_CAP = ["2", "8", "8", "—"]
BT_NAME = ["K", "L", "M", "N"]


def bohr_shells(cx, cy):
    out = []
    for i, r in enumerate(BT_R):
        out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{GRID}" stroke-width="0.8"/>')
        out.append(f'  <text x="{cx + r + 4}" y="{cy - 2}" font-size="7.5" fill="{HINT}">'
                   f'{BT_NAME[i]} {BT_CAP[i]}</text>')
    return "\n".join(out)


def bohr_blank(cx, cy, idx):
    out = [bohr_shells(cx, cy)]
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="15" fill="#FFFFFF" stroke="#BA7517" stroke-width="0.8"/>')
    out.append(f'  <text x="{cx}" y="{cy - 4}" font-size="7.5" fill="#BA7517" text-anchor="middle">p⁺</text>')
    out.append(f'  <text x="{cx}" y="{cy + 6}" font-size="7.5" fill="#BA7517" text-anchor="middle">n⁰</text>')
    out.append(f'  <text x="{cx - 90}" y="{cy - 88}" font-size="11" font-weight="600" fill="{MUTED}">练习 {idx}</text>')
    y1, y2 = cy + 96, cy + 116
    out.append(f'  <line x1="{cx - 90}" y1="{y1}" x2="{cx + 90}" y2="{y1}" stroke="{GRID}" stroke-width="0.7"/>')
    out.append(f'  <text x="{cx - 88}" y="{y1 - 5}" font-size="9" fill="{HINT}">元素 element</text>')
    out.append(f'  <line x1="{cx - 90}" y1="{y2}" x2="{cx + 90}" y2="{y2}" stroke="{GRID}" stroke-width="0.7"/>')
    out.append(f'  <text x="{cx - 88}" y="{y2 - 5}" font-size="9" fill="{HINT}">电子排布 ____　价电子 ____</text>')
    return "\n".join(out)


def bohr_example(cx, cy):
    """已填好的范例：Na 钠"""
    out = [bohr_shells(cx, cy)]
    shells = [2, 8, 1]
    for i, n in enumerate(shells):
        r = BT_R[i]
        for k in range(n):
            ang = -math.pi / 2 + k * 2 * math.pi / n
            out.append(f'  <circle cx="{cx + r * math.cos(ang):.1f}" cy="{cy + r * math.sin(ang):.1f}" '
                       f'r="3.2" fill="#185FA5"/>')
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="15" fill="#FAEEDA" stroke="#BA7517" stroke-width="0.9"/>')
    out.append(f'  <text x="{cx}" y="{cy - 4}" font-size="7.5" fill="#854F0B" text-anchor="middle">11 p⁺</text>')
    out.append(f'  <text x="{cx}" y="{cy + 6}" font-size="7.5" fill="#854F0B" text-anchor="middle">12 n⁰</text>')
    out.append(f'  <text x="{cx - 90}" y="{cy - 88}" font-size="11" font-weight="600" fill="#0C447C">'
               f'范例 example：Na 钠</text>')
    out.append(f'  <text x="{cx - 88}" y="{cy + 92}" font-size="9.5" fill="{INK}">电子排布 2, 8, 1</text>')
    out.append(f'  <text x="{cx - 88}" y="{cy + 108}" font-size="9.5" fill="#A32D2D">价电子 1（第 1 族）</text>')
    return "\n".join(out)


def build_bohr_template(path):
    s = [svg_open(BT_W, BT_H, "玻尔模型图练习模板")]
    s.append(f'  <text x="30" y="30" font-size="19" font-weight="600" fill="{INK}">'
             f'玻尔模型图练习模板｜Bohr Diagram Practice Template</text>')
    s.append(f'  <text x="850" y="30" font-size="10.5" fill="{MUTED}" text-anchor="end">'
             f'BC Science 9 · 电子层容量 2, 8, 8</text>')

    cells = [("ex", 0, 0), (1, 1, 0), (2, 2, 0), (3, 3, 0),
             (4, 0, 1), (5, 1, 1), (6, 2, 1)]
    for kind, c, r in cells:
        cx = 140 + c * 200
        cy = 205 + r * 215
        if kind == "ex":
            s.append(bohr_example(cx, cy))
        else:
            s.append(bohr_blank(cx, cy, kind))

    hx, hy = 740, 205
    s.append(f'  <rect x="{hx - 90}" y="{hy - 100}" width="180" height="200" rx="9" fill="#F1EFE8" '
             f'stroke="{GRID}" stroke-width="0.8"/>')
    s.append(f'  <text x="{hx - 74}" y="{hy - 76}" font-size="11" font-weight="600" fill="{INK}">'
             f'怎么填 / How to</text>')
    tips = ["① 原子序数 = 质子数 = 电子数", "② 由内向外填电子：",
            "　 第 1 层最多 2 个", "　 第 2 层最多 8 个",
            "　 第 3 层按 8 个计算", "③ 最外层电子数 = 价电子",
            "④ 周期数 = 电子层数", "⑤ 族号决定价电子数"]
    for i, t in enumerate(tips):
        s.append(f'  <text x="{hx - 74}" y="{hy - 52 + i * 19}" font-size="9.5" fill="{MUTED}">{esc(t)}</text>')

    s.append(f'  <text x="30" y="530" font-size="11" font-weight="600" fill="#A32D2D">'
             f'注意｜前 20 号元素范围内，第 3 层一律按 8 个计算，不要写成 18。</text>')
    s.append(f'  <text x="30" y="552" font-size="10" fill="{HINT}">'
             f'（第 3 层实际可容纳 18 个电子，但那要到第 21 号元素之后才会用到，属于超出 BC Science 9 范围的内容。）</text>')
    s.append(f'  <text x="30" y="574" font-size="10" fill="{HINT}">'
             f'中子数 = 质量数 − 质子数；本册用最常见同位素的质量数（四舍五入取整数）。对应章节：Ch.5 原子结构与玻尔模型图。</text>')
    s.append('</svg>')
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(s) + "\n")


# ---------------------------------------------------------------- 主程序
if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out_dir, exist_ok=True)
    files = [
        ("periodic-table-1-20-bilingual.svg", build_periodic_table),
        ("periodic-table-blank.svg", build_blank_table),
        ("bohr-diagrams-1-20.svg", build_bohr),
        ("lewis-dot-elements.svg", build_lewis),
        ("bohr-diagram-template.svg", build_bohr_template),
    ]
    for name, fn in files:
        p = os.path.join(out_dir, name)
        fn(p)
        print("written:", p)

    # 附带导出元素数据 CSV（与附录 D 同源，可作为 Anki 卡片 / 表格数据源）
    import csv
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "elements_1_20.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["atomic_number", "symbol", "English", "中文", "拼音",
                    "period", "group", "category", "electron_arrangement",
                    "valence_electrons", "mass_number", "neutrons"])
        for Z, sym, en, zh, py, per, grp, cat, shells, A in ELEMENTS:
            w.writerow([Z, sym, en, zh, py, per, grp, cat,
                        ", ".join(str(x) for x in shells),
                        shells[-1], A, A - Z])
    print("written:", csv_path, "(%d rows)" % len(ELEMENTS))
