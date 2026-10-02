# -*- coding: utf-8 -*-
"""
G11 Ch.5 figure builder — from Bohr to the quantum mechanical model.
Canvas height computed from content (never hard-coded).

Figures:
  ch05-model-evolution.svg   Five atomic models and what each one fixed
  ch05-orbital-shapes.svg    s / p / d / f — shape and capacity
  ch05-aufbau-order.svg      Filling order plus the three rules
  ch05-config-to-block.svg   Configuration mapped onto s / p / d / f blocks
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "figures"))

BG = "#FFFFFF"
INK = "#1F2933"
MUTED = "#52606D"
LINE = "#9AA5B1"
HEAD = "#F0F4F8"
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
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=13, fill=INK, weight="400", anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{st}>{esc(s)}</text>')


def rect(x, y, w, h, fill=BG, stroke=LINE, sw=1.2, rx=8):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, color=LINE, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{sw}"{d}/>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def build_model_evolution():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Five Atomic Models｜原子模型的五次升级", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Each upgrade kept what the old model explained and repaired the one thing it could not.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "每一次升级都保留旧模型能解释的部分，只修补它解释不了的那一处。", 11.5, MUTED))
    y += 24

    cards = [
        ("1803", "Dalton — solid sphere｜道尔顿 · 实心球",
         "原子不可再分，同种元素原子完全相同。解释不了阴极射线与放射性。", BLUE, BLUE_F),
        ("1897", "Thomson — plum pudding｜汤姆孙 · 葡萄干布丁",
         "电子嵌在正电球内。阴极射线实验发现了第一个亚原子粒子。", BLUE, BLUE_F),
        ("1911", "Rutherford — nuclear model｜卢瑟福 · 核式模型",
         "正电核极小、电子在核外。金箔 α 散射：多数穿透，少数大角度偏折。", GREEN, GREEN_F),
        ("1913", "Bohr — fixed shells｜玻尔 · 分层轨道",
         "电子只能待在固定能级上，跃迁时发光。成功解释氢原子光谱线。", AMBER, AMBER_F),
        ("1926", "Quantum mechanical — electron cloud｜量子力学 · 电子云",
         "电子位置只能用概率描述，轨道就是概率密度。海森堡与薛定谔建立。", PURPLE, PURPLE_F),
    ]
    ch = 52
    step = ch + 12
    for i, (yr, name, note, col, fl) in enumerate(cards):
        cy = y + i * step
        b.append(rect(40, cy, W - 80, ch, fl, "#E1E7EC", 0.9, 6))
        b.append(rect(40, cy, 6, ch, col))
        b.append(text(58, cy + 21, yr + " · " + name, 12.5, col, "700"))
        b.append(text(58, cy + 40, note, 11.5, MUTED))
    y2 = y + 5 * step + 4
    b.append(text(40, y2, "Bohr 不是「错」的——它对氢光谱至今成立，是从「确定轨道」通向「概率云」的桥。",
                  11.5, INK, "600"))
    return svg(W, y2 + 22, "".join(b))


# --------------------------------------------------------------------------
def build_orbital_shapes():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Orbitals: Shape and Capacity｜轨道的形状与容量", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "An orbital is a region where an electron is likely to be found — not a path it travels.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "轨道是「电子大概会出现在这里」的区域，不是电子跑的路线。", 11.5, MUTED))
    y += 26

    CX = [55, 185, 400, 570]
    b.append(rect(40, y, W - 80, 26, HEAD, "#CBD2D9", 1.0, 6))
    for t, x in zip(("Orbital｜轨道", "Shape｜形状", "Orbitals｜轨道数",
                     "Max e⁻｜最多电子"), CX):
        b.append(text(x, y + 18, t, 11.5, MUTED, "700"))
    y += 26

    rows = [
        ("s", "sphere｜球形", "1", "2", BLUE, BLUE_F),
        ("p", "dumbbell ×3｜哑铃形 ×3", "3", "6", GREEN, GREEN_F),
        ("d", "cloverleaf ×5｜四叶形 ×5", "5", "10", AMBER, AMBER_F),
        ("f", "complex ×7｜复杂形 ×7", "7", "14", PURPLE, PURPLE_F),
    ]
    rh = 30
    for i, (o, sh, n, e, col, fl) in enumerate(rows):
        b.append(rect(40, y, W - 80, rh, fl if i % 2 == 0 else BG, "#E1E7EC", 0.8, 4))
        b.append(text(CX[0], y + 20, o, 12.5, col, "700"))
        b.append(text(CX[1], y + 20, sh, 11.5, INK))
        b.append(text(CX[2], y + 20, n, 11.5, INK))
        b.append(text(CX[3], y + 20, e, 11.5, INK))
        y += rh
    y += 14
    b.append(text(40, y, "Each orbital holds at most 2 electrons (Pauli); orbitals in one subshell share one energy.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "每个轨道最多容纳 2 个电子（泡利）；同一亚层内各轨道能量相同。", 11.5, MUTED))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def build_aufbau_order():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Filling Order and the Three Rules｜填充顺序与三大规则", 15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "Fill from the lowest energy upward. The small numbers give the order of filling.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "从低能级往高能级填；格子右上角的小数字就是填充顺序。", 11.5, MUTED))
    y += 22

    cw, chh, gx0, gy0 = 80, 34, 60, y
    order = {
        (0, 0): ("1s", 1), (1, 0): ("2s", 2), (1, 1): ("2p", 3),
        (2, 0): ("3s", 4), (2, 1): ("3p", 5), (2, 2): ("3d", 7),
        (3, 0): ("4s", 6), (3, 1): ("4p", 8), (3, 2): ("4d", 10), (3, 3): ("4f", 13),
        (4, 0): ("5s", 9), (4, 1): ("5p", 11), (4, 2): ("5d", 14), (4, 3): ("5f", 17),
        (5, 0): ("6s", 12), (5, 1): ("6p", 15), (5, 2): ("6d", 18),
        (6, 0): ("7s", 16), (6, 1): ("7p", 19),
    }
    fills = [BLUE_F, GREEN_F, AMBER_F, PURPLE_F]
    for (r, c), (nm, k) in order.items():
        x = gx0 + c * (cw + 8)
        yy = gy0 + r * (chh + 10)
        b.append(rect(x, yy, cw, chh, fills[c], "#CBD2D9", 0.9, 5))
        b.append(text(x + 10, yy + 23, nm, 13, INK, "700"))
        b.append(text(x + cw - 8, yy + 13, str(k), 9.5, MUTED, "700", "end"))

    y2 = gy0 + 7 * (chh + 10) + 8
    rules = [
        ("Aufbau｜构造原理", ["低能级先填。",
                             "电子按能量从低到高入住。"], BLUE, BLUE_F),
        ("Pauli｜泡利不相容", ["一个轨道最多 2 个电子，",
                              "且两个电子自旋相反。"], GREEN, GREEN_F),
        ("Hund｜洪特规则", ["等能轨道先各占一个，",
                            "再逐一配对。"], AMBER, AMBER_F),
    ]
    bx, bw, bh, gap = 40, 186, 60, 11
    for i, (ttl, lines, col, fl) in enumerate(rules):
        x = bx + i * (bw + gap)
        b.append(rect(x, y2, bw, bh, fl, col, 1.0, 6))
        b.append(text(x + 10, y2 + 20, ttl, 11.5, col, "700"))
        for j, ln in enumerate(lines):
            b.append(text(x + 10, y2 + 38 + j * 15, ln, 10.5, MUTED))
    return svg(W, y2 + bh + 20, "".join(b))


# --------------------------------------------------------------------------
def build_config_to_block():
    W = 680
    b = []
    b.append(text(W / 2, 26, "Configuration Maps onto the Periodic Table｜排布就是周期表的地图",
                  15, INK, "600", "middle"))
    y = 48
    b.append(text(40, y, "The block of an element is simply the subshell that receives its last electron.",
                  11.5, MUTED))
    y += 16
    b.append(text(40, y, "元素的区块，就是「最后填入的电子」所在的那个亚层。", 11.5, MUTED))
    y += 24

    CX = [55, 165, 350, 550]
    b.append(rect(40, y, W - 80, 26, HEAD, "#CBD2D9", 1.0, 6))
    for t, x in zip(("Block｜区", "General form｜通式", "Where it sits｜所在族", "Example｜例"), CX):
        b.append(text(x, y + 18, t, 11.5, MUTED, "700"))
    y += 26

    rows = [
        ("s 区", "ns¹⁻²", "Groups 1–2｜第 1–2 族", "Na: [Ne]3s¹", BLUE, BLUE_F),
        ("p 区", "ns²np¹⁻⁶", "Groups 13–18｜第 13–18 族", "Cl: [Ne]3s²3p⁵", GREEN, GREEN_F),
        ("d 区·过渡金属", "(n−1)d¹⁻¹⁰ns¹⁻²", "Groups 3–12｜第 3–12 族", "Fe: [Ar]3d⁶4s²", AMBER, AMBER_F),
        ("f 区·镧系锕系", "(n−2)f¹⁻¹⁴ns²", "Below the table｜排在表外", "U: [Rn]5f³6d¹7s²", PURPLE, PURPLE_F),
    ]
    rh = 34
    for i, (blk, form, where, ex, col, fl) in enumerate(rows):
        b.append(rect(40, y, W - 80, rh, fl if i % 2 == 0 else BG, "#E1E7EC", 0.8, 4))
        b.append(text(CX[0], y + 22, blk, 11.5, col, "700"))
        b.append(text(CX[1], y + 22, form, 11.5, INK, "600"))
        b.append(text(CX[2], y + 22, where, 11, MUTED))
        b.append(text(CX[3], y + 22, ex, 11, INK))
        y += rh
    y += 16
    b.append(text(40, y, "Read the block from the last electrons added —", 11.5, MUTED))
    y += 15
    b.append(text(40, y, "it tells you which subshell is being filled.", 11.5, MUTED))
    y += 16
    b.append(text(40, y, "看最后填入的电子落在哪个亚层——那个亚层就决定了区块。", 11.5, MUTED))
    return svg(W, y + 18, "".join(b))


# --------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    figs = {
        "ch05-model-evolution.svg": build_model_evolution(),
        "ch05-orbital-shapes.svg": build_orbital_shapes(),
        "ch05-aufbau-order.svg": build_aufbau_order(),
        "ch05-config-to-block.svg": build_config_to_block(),
    }
    for name, data in figs.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(data)
        print("wrote", name, len(data), "bytes")


if __name__ == "__main__":
    main()
