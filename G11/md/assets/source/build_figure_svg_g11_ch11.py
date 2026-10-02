# -*- coding: utf-8 -*-
"""
G11 Ch.11 figure builder — energy changes.
Canvas height computed from content (never hard-coded).

Figures:
  ch11-exo-endo-diagrams.svg  Energy-level diagrams for exo and endo
  ch11-bond-accounting.svg    Bond breaking (in) vs bond forming (out) ledger
  ch11-sign-table.svg         Physical & chemical processes: exo or endo
  ch11-catalyst-effect.svg    Catalyst lowers the peak, not the gap
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


def path(pts, color=INK, sw=2.0):
    d = f'M {pts[0][0]},{pts[0][1]} ' + " ".join(f"L {x},{y}" for x, y in pts[1:])
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')


# --------------------------------------------------------------------------
def energy_diagram(b, x0, y_top, w, h, exo=True, title="", col=RED, fl=RED_F):
    """Draw one energy-level diagram panel. y grows downward.
    Peak (py) is always the highest point; plateaus move below it."""
    py = y_top + 6           # transition peak (highest)
    ry = y_top + 50 if exo else y_top + 106   # reactant plateau
    qy = ry + 56 if exo else ry - 56   # product plateau
    # axes
    b.append(line(x0, y_top - 6, x0, y_top + h - 14, MUTED, 1.4))
    b.append(line(x0, y_top + h - 14, x0 + w, y_top + h - 14, MUTED, 1.4))
    b.append(text(x0 - 8, y_top + 6, "E", 11, MUTED, "700", "end"))
    b.append(text(x0 + w - 4, y_top + h - 2, "reaction progress 反应进程", 9.5, MUTED, "400", "end"))
    # curve: reactant plateau -> peak -> product plateau
    p1x = x0 + w * 0.28
    p2x = x0 + w * 0.44
    p3x = x0 + w * 0.62
    pts = [(x0, ry), (p1x, ry), (x0 + w / 2, py), (p3x, qy), (x0 + w, qy)]
    b.append(path(pts, col, 2.2))
    # plateau labels
    b.append(line(x0, ry, x0 + w * 0.2, ry, LINE, 1.0, "3 3"))
    b.append(text(x0 + 6, ry - 6, "reactants 反应物", 10, INK, "700"))
    b.append(text(x0 + w - 6, qy + (14 if exo else -6), "products 生成物", 10, INK, "700", "end"))
    # delta H bracket
    if exo:
        b.append(line(x0 + w * 0.80, ry, x0 + w * 0.80, qy, GREEN, 1.6))
        b.append(text(x0 + w * 0.80 + 6, (ry + qy) / 2 + 4, "ΔH < 0", 11, GREEN, "700"))
    else:
        b.append(line(x0 + w * 0.80, qy, x0 + w * 0.80, ry, BLUE, 1.6))
        b.append(text(x0 + w * 0.80 + 6, (ry + qy) / 2 + 4, "ΔH > 0", 11, BLUE, "700"))
    # activation energy
    b.append(line(x0 + w * 0.5 - 30, py - 4, x0 + w * 0.5 - 30, ry, AMBER, 1.4, "4 3"))
    b.append(text(x0 + w * 0.5 - 36, (py + ry) / 2 - 2, "E_a", 10.5, AMBER, "700", "end"))
    # title
    b.append(text(x0 + w / 2, y_top + h + 6, title, 12.5, col, "700", "middle"))


def build_exo_endo():
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Energy-Level Diagrams｜能量变化图", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "The peak is the activation energy; the gap between plateaus is ΔH.",
                  11, MUTED, "400", "middle"))
    y += 14
    energy_diagram(b, 60, y + 8, 250, 190, exo=True,
                   title="Exothermic 放热 — heat OUT", col=RED)
    energy_diagram(b, 370, y + 8, 250, 190, exo=False,
                   title="Endothermic 吸热 — heat IN", col=BLUE)
    y += 190 + 30
    rows = [
        ("Exothermic 放热", "ΔH negative (e.g. −890 kJ)", "combustion, neutralization, freezing", RED),
        ("Endothermic 吸热", "ΔH positive (e.g. +66 kJ)", "melting, evaporation, photosynthesis", BLUE),
    ]
    for t1, t2, t3, col in rows:
        b.append(rect(55, y, 570, 56, BG, col, 1.3, 8))
        b.append(text(75, y + 22, t1, 12, col, "700"))
        b.append(text(230, y + 22, t2, 11.5, INK, "700"))
        b.append(text(75, y + 42, t3, 10.5, MUTED))
        y += 56 + 12
    b.append(text(340, y + 4, "kJ on the product side = exothermic ; on the reactant side = endothermic.",
                  11, MUTED, "400", "middle"))
    return svg(W, y + 28, "".join(b))


# --------------------------------------------------------------------------
def build_bond_accounting():
    """Energy ledger: breaking costs, forming pays."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "The Energy Ledger｜能量收支账本", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "Every reaction breaks bonds then forms bonds. The balance decides exo/endo.",
                  11, MUTED, "400", "middle"))
    y += 20

    # left: breaking
    b.append(rect(45, y, 285, 150, AMBER_F, AMBER, 1.4, 8))
    b.append(text(187, y + 26, "Breaking bonds 断键", 13, AMBER, "700", "middle"))
    b.append(text(187, y + 52, "absorbs energy 吸收能量", 12, INK, "700", "middle"))
    b.append(text(187, y + 76, "always IN from surroundings", 10.5, MUTED, "400", "middle"))
    b.append(text(187, y + 104, "spending money", 12, AMBER, "700", "middle", italic=True))
    b.append(text(187, y + 124, "（花钱）", 11, AMBER, "400", "middle"))

    # right: forming
    b.append(rect(350, y, 285, 150, GREEN_F, GREEN, 1.4, 8))
    b.append(text(492, y + 26, "Forming bonds 成键", 13, GREEN, "700", "middle"))
    b.append(text(492, y + 52, "releases energy 释放能量", 12, INK, "700", "middle"))
    b.append(text(492, y + 76, "always OUT to surroundings", 10.5, MUTED, "400", "middle"))
    b.append(text(492, y + 104, "earning money", 12, GREEN, "700", "middle", italic=True))
    b.append(text(492, y + 124, "（赚钱）", 11, GREEN, "400", "middle"))
    y += 150 + 18

    # verdict rows
    verdicts = [
        ("form MORE than you break → net OUT → exothermic 放热", GREEN, GREEN_F),
        ("break MORE than you form → net IN → endothermic 吸热", AMBER, AMBER_F),
    ]
    for s, col, fl in verdicts:
        b.append(rect(45, y, 590, 40, fl, col, 1.3, 8))
        b.append(text(340, y + 25, s, 12, col, "700", "middle"))
        y += 40 + 12
    b.append(text(340, y + 4, "Combustion pays well: the new C=O and O–H bonds are much stronger than the old ones.",
                  10.5, MUTED, "400", "middle"))
    return svg(W, y + 28, "".join(b))


# --------------------------------------------------------------------------
def build_sign_table():
    """Physical and chemical processes: exo or endo?"""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "Exo or Endo? Evidence Table｜放热还是吸热？", 17, INK, "700", "middle"))
    y += 22
    b.append(text(340, y, "Physical and chemical changes both carry energy bills — the thermometer tells you which.",
                  10.5, MUTED, "400", "middle"))
    y += 20

    hdr_y = y
    b.append(rect(45, hdr_y, 590, 32, HEAD, LINE, 1.2, 0))
    b.append(text(65, hdr_y + 21, "Process 过程", 12, INK, "700"))
    b.append(text(300, hdr_y + 21, "Type 类型", 12, INK, "700"))
    b.append(text(420, hdr_y + 21, "Direction", 12, INK, "700"))
    b.append(text(530, hdr_y + 21, "Thermometer 温度计", 12, INK, "700"))
    y += 32

    rows = [
        ("melting (ice → water) 熔化", "physical 物理", "IN", "drops 下降", BLUE),
        ("evaporation 蒸发", "physical 物理", "IN", "drops 下降", BLUE),
        ("freezing 凝固", "physical 物理", "OUT", "rises 上升", RED),
        ("dissolving NaOH 氢氧化钠溶解", "physical 物理", "OUT", "rises 上升", RED),
        ("dissolving NH₄NO₃ 硝铵溶解", "physical 物理", "IN", "drops 下降", BLUE),
        ("combustion 燃烧", "chemical 化学", "OUT", "rises 上升", RED),
        ("neutralization 中和", "chemical 化学", "OUT", "rises 上升", RED),
        ("baking soda + vinegar 小苏打+醋", "chemical 化学", "IN", "drops 下降", BLUE),
    ]
    rh = 30
    for i, (p, t, d, th, col) in enumerate(rows):
        if i % 2 == 0:
            b.append(rect(45, y, 590, rh, "#FAFBFC", "none", 0, 0))
        b.append(text(65, y + 20, p, 11, INK))
        b.append(text(300, y + 20, t, 10.5, MUTED))
        b.append(text(420, y + 20, d, 11, col, "700"))
        b.append(text(530, y + 20, th, 10.5, col))
        y += rh
    y += 12
    b.append(rect(45, y, 590, 44, HEAD, LINE, 1.2, 8))
    b.append(text(65, y + 19, "IN = endothermic 吸热 (surroundings cool) ; OUT = exothermic 放热 (surroundings warm)",
                  11.5, INK, "700"))
    b.append(text(65, y + 37, "ΔH 正负号只看方向：向环境吸 = 正，向环境放 = 负。", 10.5, MUTED))
    return svg(W, y + 64, "".join(b))


# --------------------------------------------------------------------------
def build_catalyst():
    """Catalyst lowers the peak, not the gap."""
    W = 680
    b = []
    y = 32
    b.append(text(340, y, "What a Catalyst Changes｜催化剂改变了什么", 17, INK, "700", "middle"))
    y += 16

    # one combined diagram
    x0, w = 70, 540
    y_top = y + 10
    ry = y_top + 60
    py = y_top + 12
    qy = ry + 50
    b.append(line(x0, y_top - 4, x0, y_top + 180, MUTED, 1.4))
    b.append(line(x0, y_top + 180, x0 + w, y_top + 180, MUTED, 1.4))
    b.append(text(x0 - 8, y_top + 8, "E", 11, MUTED, "700", "end"))
    b.append(text(x0 + w - 4, y_top + 196, "reaction progress 反应进程", 9.5, MUTED, "400", "end"))

    # without catalyst (higher peak)
    pts1 = [(x0, ry), (x0 + 140, ry), (x0 + 250, py), (x0 + 360, qy), (x0 + w, qy)]
    b.append(path(pts1, RED, 2.2))
    # with catalyst (lower peak)
    cy = py + 40
    pts2 = [(x0, ry), (x0 + 140, ry), (x0 + 250, cy), (x0 + 360, qy), (x0 + w, qy)]
    b.append(path(pts2, GREEN, 2.2, ))
    b.append(text(x0 + 250, py - 6, "no catalyst", 10.5, RED, "700", "middle"))
    b.append(text(x0 + 320, cy + 14, "with catalyst", 10.5, GREEN, "700"))

    b.append(text(x0 + 6, ry - 6, "reactants", 10, INK, "700"))
    b.append(text(x0 + w - 6, qy + 16, "products", 10, INK, "700", "end"))
    # gap markers
    b.append(line(x0 + w - 40, ry, x0 + w - 40, qy, INK, 1.6))
    b.append(text(x0 + w - 46, (ry + qy) / 2 + 4, "ΔH same｜ΔH 不变", 10.5, INK, "700", "end"))
    y = y_top + 216

    cards = [
        ("Lowers activation energy｜降低活化能", GREEN, GREEN_F),
        ("Does NOT change ΔH｜不改变始末能量差", BLUE, BLUE_F),
        ("Speeds the reaction, not the yield｜只加速，不加产", AMBER, AMBER_F),
    ]
    cw = 186
    for i, (s, col, fl) in enumerate(cards):
        cx = 45 + i * (cw + 12)
        b.append(rect(cx, y, cw, 58, fl, col, 1.3, 8))
        b.append(text(cx + cw / 2, y + 24, s.split("｜")[0], 10.5, col, "700", "middle"))
        b.append(text(cx + cw / 2, y + 42, s.split("｜")[1], 10.5, INK, "400", "middle"))
    y += 58 + 18
    b.append(text(340, y + 4, "A tunnel through the mountain is still the same mountain — start and end are identical.",
                  10.5, MUTED, "400", "middle"))
    return svg(W, y + 28, "".join(b))


# --------------------------------------------------------------------------
def main():
    figs = {
        "ch11-exo-endo-diagrams.svg": build_exo_endo,
        "ch11-bond-accounting.svg": build_bond_accounting,
        "ch11-sign-table.svg": build_sign_table,
        "ch11-catalyst-effect.svg": build_catalyst,
    }
    for name, fn in figs.items():
        s = fn()
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(s)
        print("wrote", name)


if __name__ == "__main__":
    main()
