# -*- coding: utf-8 -*-
"""
G11 Ch.1 figure builder — 4 SVG figures for the bridging / quantitative-tools chapter.
Canvas height is computed from content, never hard-coded (lesson from G9 check_svg_bounds.py).

Figures:
  ch01-sigfig-flow.svg      Significant-figure decision flow
  ch01-dimensional-chain.svg  Dimensional-analysis chain (unit cancellation)
  ch01-mole-bridges.svg      The three bridges: particles <-> moles <-> mass
  ch01-naming-order.svg      English vs Chinese naming order (inorganic vs organic)
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "figures"))

# ---- theme (dark-friendly is irrelevant: SVG is embedded on light PDF page) ----
BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#52606D"
LINE = "#9AA5B1"
BLUE = "#2B6CB0"
BLUE_F = "#EBF4FF"
GREEN = "#2F855A"
GREEN_F = "#F0FFF4"
AMBER = "#B7791F"
AMBER_F = "#FFFBEB"
RED = "#C53030"
RED_F = "#FFF5F5"
PURPLE = "#6B46C1"
PURPLE_F = "#F5F0FF"

FONT = "'Segoe UI','Helvetica Neue',Arial,'Microsoft YaHei',sans-serif"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, size=13, fill=INK, weight="400", anchor="start", italic=False):
    st = f' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{st}>{esc(s)}</text>')


def rect(x, y, w, h, fill=BG, stroke=LINE, sw=1.2, rx=8):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def arrow_defs(cid, color):
    return (f'<defs><marker id="{cid}" markerWidth="10" markerHeight="8" refX="9" refY="4" '
            f'orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="{color}"/></marker></defs>')


def line(x1, y1, x2, y2, color=LINE, sw=1.4, marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}"{m}{d}/>')


def wrap_text(x, y, s, max_chars, size=12, fill=INK, lh=17, weight="400", anchor="start"):
    """Naive width-wrap on character count (mixed CJK/latin aware enough for our strings)."""
    out, cur, n = [], "", 0
    for ch in s:
        w = 2 if ord(ch) > 0x2E80 else 1
        if n + w > max_chars and ch not in " ，、。／/":
            out.append(cur)
            cur, n = "", 0
        cur += ch
        n += w
    if cur:
        out.append(cur)
    return "".join(text(x, y + i * lh, ln, size, fill, weight, anchor) for i, ln in enumerate(out)), len(out) * lh


def build_sigfig_flow():
    W, H = 680, 0
    b = []
    y = 0
    title = "Significant Figures — Decision Flow｜有效数字判定流程"
    b.append(text(W / 2, 26, title, 15, INK, "600", "middle"))
    y = 46

    steps = [
        ("Step 1", "Is the number a MEASURED value or an EXACT count?",
         "这个数是测量值，还是精确计数／定义值？", BLUE, BLUE_F),
        ("Step 2", "Find each digit: all non-zero digits count.",
         "逐位判断：所有非零数字都算。", GREEN, GREEN_F),
        ("Step 3", "Zeros BETWEEN non-zero digits always count.",
         "夹在非零数字之间的零，一律算。", GREEN, GREEN_F),
        ("Step 4", "Leading zeros NEVER count (0.0025 → 2 s.f.).",
         "前导零不算（0.0025 是 2 位）。", AMBER, AMBER_F),
        ("Step 5", "Trailing zeros count ONLY if a decimal point is present.",
         "末尾零只有在有小数点时才算（800 → 1 位；800. → 3 位）。", AMBER, AMBER_F),
    ]
    for tag, en, cn, col, fl in steps:
        h = 62
        b.append(rect(40, y, W - 80, h, fl, col, 1.2, 8))
        b.append(text(58, y + 24, tag, 12, col, "700"))
        b.append(text(118, y + 24, en, 12.5, INK, "500"))
        b.append(text(118, y + 44, cn, 12, MUTED))
        y += h + 10
        if tag != "Step 5":
            b.append(line(W / 2, y - 10, W / 2, y, LINE, 1.4))

    # two operation rules
    b.append(rect(40, y + 8, (W - 90) / 2, 74, BLUE_F, BLUE, 1.2, 8))
    b.append(text(58, y + 32, "× and ÷ : least s.f.", 12.5, BLUE, "700"))
    b.append(text(58, y + 52, "乘除 → 取有效位数最少者", 12, MUTED))
    b.append(rect(40 + (W - 90) / 2 + 10, y + 8, (W - 90) / 2, 74, BLUE_F, BLUE, 1.2, 8))
    b.append(text(58 + (W - 90) / 2 + 10, y + 32, "+ and − : least decimal place", 12.5, BLUE, "700"))
    b.append(text(58 + (W - 90) / 2 + 10, y + 52, "加减 → 取小数位最少者", 12, MUTED))
    y += 82
    b.append(text(40, y + 20, "⛔ Never round in the middle of a multi-step calculation.", 12.5, RED, "600"))
    b.append(text(52, y + 38, "多步计算中途不要四舍五入，只在最后一步取整。", 12, MUTED))
    y += 54

    H = y
    return svg(W, H, "".join(b))


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


def build_mole_bridges():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "The Three Bridges｜摩尔三桥：粒子 ⇄ 摩尔 ⇄ 质量", 15, INK, "600", "middle"))
    y = 54

    box_w, box_h = 168, 76
    gap = (W - 80 - box_w * 3) / 2
    y0 = y
    labels = [
        ("PARTICLES｜粒子数", "N  (atoms, molecules, ions)", PURPLE, PURPLE_F),
        ("MOLES｜物质的量", "n  (mol)", BLUE, BLUE_F),
        ("MASS｜质量", "m  (g)", GREEN, GREEN_F),
    ]
    xs = []
    for i, (t, sub, col, fl) in enumerate(labels):
        x = 40 + i * (box_w + gap)
        xs.append(x)
        b.append(rect(x, y0, box_w, box_h, fl, col, 1.4, 10))
        b.append(text(x + box_w / 2, y0 + 30, t, 13, col, "700", "middle"))
        b.append(text(x + box_w / 2, y0 + 54, sub, 12, MUTED, "400", "middle"))

    ymid = y0 + box_h / 2

    # bridge 1
    x1a, x1b = xs[0] + box_w, xs[1]
    b.append(arrow_defs("ar1", BLUE))
    b.append(arrow_defs("ar1r", BLUE))
    b.append(line(x1a + 4, ymid - 12, x1b - 4, ymid - 12, BLUE, 1.6, "ar1"))
    b.append(line(x1b - 4, ymid + 12, x1a + 4, ymid + 12, BLUE, 1.6, "ar1r"))
    b.append(text((x1a + x1b) / 2, ymid - 26, "÷ 6.02×10²³", 11.5, BLUE, "600", "middle"))
    b.append(text((x1a + x1b) / 2, ymid + 32, "× 6.02×10²³", 11.5, BLUE, "600", "middle"))

    # bridge 2
    x2a, x2b = xs[1] + box_w, xs[2]
    b.append(arrow_defs("ar2", GREEN))
    b.append(arrow_defs("ar2r", GREEN))
    b.append(line(x2a + 4, ymid - 12, x2b - 4, ymid - 12, GREEN, 1.6, "ar2"))
    b.append(line(x2b - 4, ymid + 12, x2a + 4, ymid + 12, GREEN, 1.6, "ar2r"))
    b.append(text((x2a + x2b) / 2, ymid - 26, "× M  (g/mol)", 11.5, GREEN, "600", "middle"))
    b.append(text((x2a + x2b) / 2, ymid + 32, "÷ M  (g/mol)", 11.5, GREEN, "600", "middle"))

    y = y0 + box_h + 26
    b.append(text(40, y, "Avogadro's number｜阿伏伽德罗常数：N_A = 6.02 × 10²³  particles / mol", 12.5, PURPLE, "600"))
    y += 22
    b.append(text(40, y, "Molar mass｜摩尔质量：M = the average atomic mass from the periodic table, in g/mol", 12.5, GREEN, "600"))
    y += 30
    b.append(rect(40, y, W - 80, 62, AMBER_F, AMBER, 1.2, 8))
    b.append(text(58, y + 24, "⚠ You can never jump straight from particles to mass.", 12.5, RED, "600"))
    b.append(text(58, y + 44, "粒子数不能直接换算成质量——必须经过「摩尔」这一站，这是本章之后所有计算题的骨架。", 12, MUTED))
    y += 78

    return svg(W, y, "".join(b))


def build_dimensional_chain():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Dimensional Analysis｜量纲分析：单位连消", 15, INK, "600", "middle"))
    y = 52
    b.append(text(40, y, "Given｜已知：0.752 kg of water  kg → mol   (M(H₂O) = 18.02 g/mol)", 12.5, MUTED))
    y += 26

    cw, ch = 150, 72
    gapx = (W - 80 - cw * 3) / 2
    y0 = y
    items = [
        ("GIVEN｜已知", "0.752 kg", BLUE, BLUE_F),
        ("× factor ①", "1000 g\n————\n1 kg", AMBER, AMBER_F),
        ("× factor ②", "1 mol\n————\n18.02 g", GREEN, GREEN_F),
    ]
    xs = []
    for i, (t, s, col, fl) in enumerate(items):
        x = 40 + i * (cw + gapx)
        xs.append(x)
        b.append(rect(x, y0, cw, ch, fl, col, 1.3, 8))
        b.append(text(x + cw / 2, y0 + 20, t, 11.5, col, "700", "middle"))
        parts = s.split("\n")
        for j, p in enumerate(parts):
            b.append(text(x + cw / 2, y0 + 42 + j * 14, p, 12, INK, "500", "middle"))
        if i < 2:
            b.append(arrow_defs(f"dc{i}", LINE))
            b.append(line(x + cw + 6, y0 + ch / 2, x + cw + gapx - 6, y0 + ch / 2, LINE, 1.5, f"dc{i}"))

    y = y0 + ch + 22
    b.append(rect(40, y, W - 80, 92, PURPLE_F, PURPLE, 1.3, 8))
    b.append(text(58, y + 24, "Chain｜连式（单位像分数一样约掉）", 12.5, PURPLE, "700"))
    b.append(text(58, y + 48, "0.752 kg × 1000 g/1 kg × 1 mol/18.02 g = 41.7 mol", 13, INK, "600"))
    b.append(text(58, y + 74, "kg 约掉 → g 约掉 → 只剩 mol ✓　结果 41.7 mol（3 s.f.，与 0.752 一致）", 12, MUTED))
    y += 108
    b.append(text(40, y + 16, "📏 Rule｜规则：每一站都写单位；单位不消干净，答案一定是错的。", 12.5, BLUE, "600"))
    y += 40
    return svg(W, y, "".join(b))


def build_naming_order():
    W = 680
    b, y = [], 0
    b.append(text(W / 2, 26, "Naming Order: Inorganic vs Organic｜命名语序对照", 15, INK, "600", "middle"))
    y = 50

    # --- inorganic ---
    b.append(rect(40, y, W - 80, 128, RED_F, RED, 1.3, 10))
    b.append(text(58, y + 26, "INORGANIC｜无机：语序相反 (reversed)", 13, RED, "700"))
    b.append(text(58, y + 54, "NaCl →  English:  sodium chloride     (metal → non-metal-ide)", 12.5, INK, "500"))
    b.append(text(58, y + 76, "            中文：    氯化钠              (非金属 + 化 + 金属)", 12.5, INK, "500"))
    b.append(text(58, y + 104, "⛔ Wrong｜错误：钠化氯 / sodium monochloride", 12, RED, "600"))
    y += 144

    # --- organic ---
    b.append(rect(40, y, W - 80, 128, GREEN_F, GREEN, 1.3, 10))
    b.append(text(58, y + 26, "ORGANIC｜有机：语序基本对应 (same order)", 13, GREEN, "700"))
    b.append(text(58, y + 54, "CH₃CH₂CH₃ →  English:  propane", 12.5, INK, "500"))
    b.append(text(58, y + 76, "                     中文：    丙烷", 12.5, INK, "500"))
    b.append(text(58, y + 104, "2-methylbutane → 2-甲基丁烷　(prefix 位置与中文一致)", 12, GREEN, "600"))
    y += 146

    b.append(rect(40, y, W - 80, 58, BLUE_F, BLUE, 1.2, 8))
    b.append(text(58, y + 24, "📏 Why it differs｜为什么不同", 12.5, BLUE, "700"))
    b.append(text(58, y + 44, "无机看「二元组成」→ 中英习惯相反；有机看「碳链 + 编号」→ 中英都按位置读。", 12, MUTED))
    y += 74
    return svg(W, y, "".join(b))


def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "ch01-sigfig-flow.svg": build_sigfig_flow(),
        "ch01-mole-bridges.svg": build_mole_bridges(),
        "ch01-dimensional-chain.svg": build_dimensional_chain(),
        "ch01-naming-order.svg": build_naming_order(),
    }
    for name, data in figs.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"wrote {name}  ({len(data)} bytes)")


if __name__ == "__main__":
    main()
