# -*- coding: utf-8 -*-
"""
为章节正文生成矢量示意图（SVG），替代 md 里的 ASCII 字符画。

为什么用脚本生成而不是手写文件：图与讲义同源，改文案后重跑即可，
不会像手改文件那样与正文漂移。风格严格对齐 assets/figures/ 已有图库
（900 宽、白底、标题 19pt、右上小字注释、圆角 rx=8、蓝/橙/灰配色）。

用法：
    python build_figure_svg.py          # 生成全部已定义的图
    python build_figure_svg.py ch01     # 只生成文件名含 ch01 的图

输出目录：../figures/
后续要加新图：在 FIGURES 字典里加一项即可。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(HERE), "figures")

# ---------------------------------------------------------------- 样式常量
FONT = ("'Segoe UI','Microsoft YaHei','PingFang SC',"
        "'Noto Sans CJK SC',Arial,sans-serif")
INK = "#2C2C2A"      # 主文字
SUB = "#5F5E5A"      # 次要文字
LINE = "#888780"     # 连线/中性描边
EDGE = "#B4B2A9"     # 浅边框
BLUE, BLUE_D, BLUE_BG = "#185FA5", "#0C447C", "#E6F1FB"
ORANGE, ORANGE_D, ORANGE_BG = "#BA7517", "#854F0B", "#FAEEDA"
GREEN, GREEN_BG = "#3B6D11", "#EAF3DE"
RED = "#A32D2D"
NEUTRAL_BG = "#F1EFE8"


def head(w, h, title, note):
    """画布 + 标题栏。"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}"
     font-family="{FONT}">
  <title>{title}</title>
  <rect width="{w}" height="{h}" fill="#FFFFFF"/>
  <text x="30" y="32" font-size="19" font-weight="600" fill="{INK}">{title}</text>
  <text x="{w - 30}" y="32" font-size="10.5" fill="{SUB}"
        text-anchor="end">{note}</text>
"""


def box(x, y, w, h, fill, stroke, sw=0.9, rx=8):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n')


def txt(x, y, s, size=12, fill=INK, weight="400", anchor="middle",
        baseline="central", extra=""):
    w = f' font-weight="{weight}"' if weight != "400" else ""
    return (f'  <text x="{x}" y="{y}" font-size="{size}"{w} fill="{fill}" '
            f'text-anchor="{anchor}" dominant-baseline="{baseline}"'
            f'{extra}>{s}</text>\n')


def path(d, stroke=LINE, sw=1.5, marker=None, dash=None):
    m = f' marker-end="url(#{marker})"' if marker else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <path d="{d}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}"{da}{m}/>\n')


ARROW_DEF = """  <defs>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"
            markerHeight="7" orient="auto-start-reverse">
      <path d="M2 1L9 5L2 9" fill="none" stroke="context-stroke"
            stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
  </defs>
"""


def wrap(inner):
    return inner + "</svg>\n"


# ================================================================ 图 1-1
def fig_matter_tree():
    """物质分类树状图：根 → 2 支 → 4 叶。"""
    s = head(900, 402, "图 1-1　物质分类树状图｜Classification Tree",
             "BC Science 9 · 先分纯净物/混合物，再往下细分")
    s += ARROW_DEF

    # ---- 根节点
    s += box(300, 62, 300, 58, NEUTRAL_BG, LINE, 1.0)
    s += txt(450, 82, "MATTER 物质", 15, INK, "600")
    s += txt(450, 102, "(has mass &amp; takes up space) 有质量、占空间",
             10, SUB)

    # ---- 根 → 两支
    s += path("M450 120 L450 150")
    s += path("M230 150 L670 150")
    s += path("M230 150 L230 172", marker="ar")
    s += path("M670 150 L670 172", marker="ar")

    # ---- 两个分支
    s += box(80, 176, 300, 62, BLUE_BG, BLUE, 1.2)
    s += txt(230, 196, "PURE SUBSTANCE 纯净物", 14, BLUE_D, "600")
    s += txt(230, 216, "(fixed composition) 组成固定", 10, BLUE)

    s += box(520, 176, 300, 62, ORANGE_BG, ORANGE, 1.2)
    s += txt(670, 196, "MIXTURE 混合物", 14, ORANGE_D, "600")
    s += txt(670, 216, "(variable composition) 组成可变", 10, ORANGE)

    # ---- 分支 → 四个叶子
    s += path("M230 238 L230 262")
    s += path("M120 262 L340 262")
    s += path("M120 262 L120 286", marker="ar")
    s += path("M340 262 L340 286", marker="ar")
    s += path("M670 238 L670 262")
    s += path("M560 262 L780 262")
    s += path("M560 262 L560 286", marker="ar")
    s += path("M780 262 L780 286", marker="ar")

    # ---- 四个叶子：英文 / 中文 / 性质 / 例子
    leaves = [
        (20, "ELEMENT", "元素", "1 种原子 only 1 kind of atom",
         "O₂　Fe　Cu", BLUE_BG, BLUE, BLUE_D),
        (240, "COMPOUND", "化合物", "2 种以上元素 2+ elements",
         "H₂O　NaCl", BLUE_BG, BLUE, BLUE_D),
        (460, "HOMOGENEOUS", "均一混合物", "看不出界面，整体均匀 uniform",
         "盐水　空气　溶液", ORANGE_BG, ORANGE, ORANGE_D),
        (680, "HETEROGENEOUS", "非均一混合物", "看得出分层或界面 visible parts",
         "沙水　沙拉　泥浆水", ORANGE_BG, ORANGE, ORANGE_D),
    ]
    for x, en, cn, desc, eg, bg, st, fg in leaves:
        s += box(x, 290, 200, 84, bg, st, 1.0)
        s += txt(x + 100, 308, en, 12.5, fg, "600")
        s += txt(x + 100, 327, cn, 13, INK, "600")
        s += txt(x + 100, 345, desc, 8.8, SUB)
        s += txt(x + 100, 361, eg, 9.5, fg, "600")

    # ---- 底部提示
    s += txt(450, 392,
             "判断顺序：先问「组成固不固定」，再问「看不看得出界面」",
             9.5, SUB)
    return wrap(s)


# ================================================================ 图 1-2
def fig_atomic_timeline():
    """原子模型演化时间轴：四格示意 + 年份。"""
    s = head(900, 486, "图 1-2　原子模型演化时间轴｜Atomic Model Timeline",
             "BC Science 9 · 模型随新证据不断修正")
    s += ARROW_DEF

    cols = [25, 240, 455, 670]           # 每列左边界，宽 205
    cxs = [c + 102.5 for c in cols]
    years = ["1808", "1897", "1911", "1913"]
    names = ["Dalton 道尔顿", "Thomson 汤姆孙", "Rutherford 卢瑟福",
             "Bohr 玻尔"]
    ideas = ["不可分的实心球", "发现电子（葡萄干布丁）",
             "发现原子核（金箔实验）", "电子分层排布 → 本册 Ch.5"]

    # ---- 时间轴
    s += path("M60 62 L840 62", LINE, 1.2)
    for cx, yr in zip(cxs, years):
        s += txt(cx, 52, yr, 12, BLUE_D, "600")
        s += f'  <circle cx="{cx}" cy="62" r="3.5" fill="{BLUE}"/>\n'
        s += path(f"M{cx} 66 L{cx} 88", BLUE, 1.2, marker="ar")

    # ---- 四格
    for i, (x, cx) in enumerate(zip(cols, cxs)):
        bg = [NEUTRAL_BG, ORANGE_BG, BLUE_BG, GREEN_BG][i]
        st = [LINE, ORANGE, BLUE, GREEN][i]
        s += box(x, 92, 205, 152, bg, st, 1.0)

    # (1) Dalton：实心球
    cx = cxs[0]
    s += f'  <circle cx="{cx}" cy="168" r="46" fill="#5F5E5A"/>\n'
    s += f'  <circle cx="{cx - 14}" cy="154" r="13" fill="#7F7E78"/>\n'
    s += txt(cx, 228, "solid sphere 实心球", 9.5, SUB)

    # (2) Thomson：葡萄干布丁
    cx = cxs[1]
    s += (f'  <circle cx="{cx}" cy="168" r="50" fill="#FBEBD2" '
          f'stroke="{ORANGE}" stroke-width="1.4"/>\n')
    for dx, dy in [(-26, -18), (0, -26), (26, -12), (-30, 16), (-4, 20),
                   (28, 22), (12, 2), (-14, 34)]:
        s += (f'  <circle cx="{cx + dx}" cy="{168 + dy}" r="5.5" '
              f'fill="{INK}"/>\n')
    s += txt(cx, 228, "plum pudding 电子嵌在正电荷糊里", 9, SUB)

    # (3) Rutherford：核 + α 粒子穿透
    cx = cxs[2]
    s += (f'  <circle cx="{cx}" cy="168" r="54" fill="none" '
          f'stroke="{EDGE}" stroke-width="1" stroke-dasharray="4 4"/>\n')
    s += f'  <circle cx="{cx}" cy="168" r="12" fill="{RED}"/>\n'
    for dx, dy in [(-30, -26), (34, -14), (-24, 30), (30, 28)]:
        s += (f'  <circle cx="{cx + dx}" cy="{168 + dy}" r="4.5" '
              f'fill="{BLUE}"/>\n')
    # α 粒子：一条穿过的虚线箭头 + 一条被弹回的
    s += path(f"M{cx - 78} 130 L{cx + 60} 196", RED, 1.4, marker="ar",
              dash="5 3")
    s += txt(cx - 62, 120, "α", 10, RED, "600")
    s += txt(cx, 230, "大部分直穿 → 原子内几乎全空", 9, SUB)

    # (4) Bohr：核 + 同心轨道
    cx = cxs[3]
    for r in (28, 48):
        s += (f'  <circle cx="{cx}" cy="168" r="{r}" fill="none" '
              f'stroke="{GREEN}" stroke-width="1.2"/>\n')
    s += f'  <circle cx="{cx}" cy="168" r="12" fill="{GREEN}"/>\n'
    s += (f'  <circle cx="{cx + 28}" cy="168" r="5" fill="{INK}"/>\n')
    s += (f'  <circle cx="{cx - 48}" cy="168" r="5" fill="{INK}"/>\n')
    s += (f'  <circle cx="{cx + 34}" cy="140" r="5" fill="{INK}"/>\n')
    s += txt(cx, 228, "shells 电子在固定壳层上", 9.5, SUB)

    # ---- 每格下方：名字 + 主张
    for i, (x, cx) in enumerate(zip(cols, cxs)):
        fg = [INK, ORANGE_D, BLUE_D, GREEN][i]
        s += txt(cx, 262, names[i], 13, fg, "600")
        s += txt(cx, 282, ideas[i], 9.5, SUB)

    # ---- 底部：演进说明
    s += box(60, 306, 780, 58, "#FAFAF8", EDGE, 0.9)
    s += txt(450, 326, "模型的演进不是「推翻」，而是「扩展」：",
             11.5, INK, "600")
    s += txt(450, 345,
             "Thomson 加进了电子，Rutherford 找到了原子核，Bohr 给电子安排了壳层 —— "
             "旧模型能解释的部分一直保留着",
             10, SUB)

    # ---- 强调 Ch.5
    s += box(60, 378, 780, 62, BLUE_BG, BLUE, 1.0)
    s += txt(450, 398, "本册主线：玻尔模型的「电子分层排布」", 12.5, BLUE_D,
             "600")
    s += txt(450, 418,
             "决定了元素在周期表中的位置，也决定了它会形成什么化合物 —— 这就是 Ch.5 之后全部内容的核心",
             10, BLUE)
    s += txt(450, 448,
             "Science 8 先修：atomic theory / protons, neutrons, electrons　→　"
             "Science 10 后续：chemical reactions, conservation of mass",
             9.5, SUB)
    return wrap(s)


# ================================================================ 图 1-3
def fig_atomic_structure():
    """原子结构与尺度：电子云 + 原子核 + 体育场类比。"""
    s = head(900, 470, "图 1-3　原子结构与尺度｜Atomic Structure &amp; Scale",
             "BC Science 9 · 以钠原子 Na-23 为例（11 p⁺ / 12 n⁰）")
    s += ARROW_DEF

    # ---- 左侧：电子云（虚线大圆）
    cx, cy, R = 235, 250, 178
    s += (f'  <circle cx="{cx}" cy="{cy}" r="{R}" fill="#FBFAF7" '
          f'stroke="{BLUE}" stroke-width="1.4" stroke-dasharray="7 5"/>\n')
    s += txt(cx, cy - R + 20, "电子云区域 electron cloud", 10.5, BLUE,
             "600")
    s += txt(cx, cy - R + 36, "（电子在这里运动，位置不固定）", 9, SUB)

    # 电子：固定坐标的点阵，模拟概率分布（越靠内越密）
    pts = [(-120, -70), (-95, 20), (-70, -120), (-55, 75), (-30, -35),
           (-15, 130), (10, -150), (25, -60), (45, 40), (65, -95),
           (85, 15), (105, -45), (60, 115), (-105, 95), (120, 70),
           (-40, -160), (15, 90), (95, 130), (-130, 30), (35, 160)]
    for dx, dy in pts:
        s += (f'  <circle cx="{cx + dx}" cy="{cy + dy}" r="4.5" '
              f'fill="{BLUE}"/>\n')
    # 三个带标签的电子
    for dx, dy, lx, ly in [(-70, -120, -70, -140), (105, -45, 125, -60),
                           (95, 130, 110, 150)]:
        s += (f'  <circle cx="{cx + dx}" cy="{cy + dy}" r="6.5" '
              f'fill="{BLUE}"/>\n')
        s += txt(cx + lx, cy + ly, "e⁻", 11, BLUE_D, "600")

    # ---- 原子核（故意画得极小，体现尺度差）
    s += f'  <circle cx="{cx}" cy="{cy}" r="17" fill="{RED}"/>\n'
    s += (f'  <circle cx="{cx - 6}" cy="{cy - 6}" r="5" fill="#C9A0A0"/>\n')
    # 引线标注
    s += path(f"M{cx + 14} {cy - 12} L{cx + 96} {cy - 74}", RED, 1.1)
    s += txt(cx + 140, cy - 88, "原子核 nucleus", 11.5, RED, "600")
    s += txt(cx + 140, cy - 70, "11 p⁺ + 12 n⁰", 10.5, RED, "600")
    s += txt(cx + 140, cy - 52, "直径只有原子的 1/100 000", 9.5, SUB)

    # ---- 右侧说明
    x = 470
    s += box(x, 92, 400, 96, NEUTRAL_BG, EDGE, 0.9)
    s += txt(x + 16, 112, "尺度对比 Scale", 12.5, INK, "600",
             anchor="start")
    s += txt(x + 16, 134, "原子直径　　≈ 1 × 10⁻¹⁰ m", 10.5, INK,
             anchor="start")
    s += txt(x + 16, 154, "原子核直径　≈ 1 × 10⁻¹⁵ m", 10.5, RED,
             "600", anchor="start")
    s += txt(x + 16, 174, "两者相差约 10 万倍", 10, SUB, anchor="start")

    s += box(x, 200, 400, 96, "#FAFAF8", EDGE, 0.9)
    s += txt(x + 16, 220, "质量分布 Mass", 12.5, INK, "600",
             anchor="start")
    s += txt(x + 16, 242, "原子核占原子总质量的 99.9% 以上", 10.5, RED,
             "600", anchor="start")
    s += txt(x + 16, 262, "电子质量极小，计算相对原子质量时可忽略", 9.5,
             SUB, anchor="start")
    s += txt(x + 16, 282, "→ 相对原子质量 ≈ 质子数 + 中子数", 10, BLUE_D,
             "600", anchor="start")

    # ---- 类比框
    s += box(x, 312, 400, 118, ORANGE_BG, ORANGE, 1.2)
    s += txt(x + 200, 334, "类比 Analogy", 13, ORANGE_D, "600")
    s += txt(x + 200, 356, "如果原子是一座体育场，", 11, INK)
    s += txt(x + 200, 376, "原子核就是场中央的一颗弹珠，", 11, INK)
    s += txt(x + 200, 396, "电子则在整座体育场的看台上活动。", 11, INK)
    s += txt(x + 200, 418, "原子内部几乎全是空的 —— mostly empty space",
             9.5, SUB)

    # ---- 底部提示（对应 Rutherford 的证据）
    s += txt(450, 452,
             "证据：卢瑟福金箔实验中大部分 α 粒子直穿而过，说明原子内部几乎全是空的",
             9.5, SUB)
    return wrap(s)


# ================================================================ 注册表
FIGURES = {
    "matter-classification-tree.svg": fig_matter_tree,
    "atomic-model-timeline.svg": fig_atomic_timeline,
    "atomic-structure-scale.svg": fig_atomic_structure,
}


def main():
    keys = FIGURES.keys()
    if len(sys.argv) > 1:
        k = sys.argv[1].lower()
        keys = [n for n in keys if k in n.lower()]
        if not keys:
            raise SystemExit("没有匹配的图：" + sys.argv[1])
    os.makedirs(FIG_DIR, exist_ok=True)
    for name in keys:
        svg = FIGURES[name]()
        out = os.path.join(FIG_DIR, name)
        open(out, "w", encoding="utf-8").write(svg)
        print("OK  %-36s %6.1f KB" % (name, len(svg.encode("utf-8")) / 1024))


if __name__ == "__main__":
    main()
