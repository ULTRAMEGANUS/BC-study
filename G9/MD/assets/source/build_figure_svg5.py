# -*- coding: utf-8 -*-
"""
build_figure_svg5.py —— 附录（Appendix B–E）配图

与 build_figure_svg2/3/4 同一套绘图原语（都从 build_figure_svg.py 导入），
画布高度一律**由内容算出**或算好后写在注释里，改完必跑 check_svg_bounds.py。

注册：
    appc-naming-decision-tree.svg   附录 C-1 命名决策树
    appc-cn-en-order.svg            附录 C-7 中英命名顺序相反对照
    appc-cheat-sheet.svg            附录 C 末尾「一页纸速查卡」
"""
import os

from build_figure_svg import (head, box, txt, path, wrap, ARROW_DEF,
                              FONT, INK, SUB, LINE, EDGE, BLUE, BLUE_D,
                              BLUE_BG, ORANGE, ORANGE_D, ORANGE_BG, GREEN,
                              GREEN_BG, RED, NEUTRAL_BG)
from build_figure_svg3 import badge, bohr_figure

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "figures")


# ==================================================== 附录 C-1 命名决策树
def fig_appc_decision_tree():
    s = head(900, 470, "附录 C-1　命名决策树｜The Naming Decision Tree",
             "拿到化学式先判类型，两套命名法完全不同")
    s += ARROW_DEF
    # 起点
    s += box(330, 62, 240, 38, NEUTRAL_BG, LINE, 1.2, rx=8)
    s += txt(450, 81, "拿到化学式 Chemical formula", 12.5, INK, "700")
    s += path("M450 100 L450 116", LINE, 1.5)

    # 三分支判定行
    s += txt(450, 132, "① 看组成元素：有金属？含 NH₄⁺？全是 非金属？",
             11.5, SUB, "600")
    ys = 150
    cols = [(140, "有金属元素？", "metal present", BLUE_BG, BLUE_D),
            (450, "含 NH₄⁺ 铵根？", "ammonium", ORANGE_BG, ORANGE_D),
            (760, "全是 非金属？", "all non-metals", GREEN_BG, GREEN)]
    for x, q, sub, bg, fg in cols:
        s += box(x - 125, ys, 250, 44, bg, fg, 1.1, rx=8)
        s += txt(x, ys + 16, q, 12, INK, "700")
        s += txt(x, ys + 33, sub, 10, SUB, "400")
    # 汇聚：金属 与 NH₄⁺ 都走 IONIC
    s += path("M140 194 L140 214 L450 214 L450 232", BLUE, 1.6, marker="ar")
    s += path("M450 194 L450 232", ORANGE, 1.6, marker="ar")
    s += path("M760 194 L760 232", GREEN, 1.6, marker="ar")

    # 两个结果框
    y2 = 240
    s += box(70, y2, 380, 96, BLUE_BG, BLUE, 1.4, rx=10)
    s += txt(260, y2 + 22, "IONIC 离子化合物", 14, BLUE_D, "700")
    s += txt(260, y2 + 44, "电子转移 transfer → 交叉法 criss-cross", 11,
             INK, "400")
    s += txt(260, y2 + 62, "词尾改 -ide，不加前缀", 11, INK, "400")
    s += txt(260, y2 + 82, "例 NaCl sodium chloride 氯化钠", 11, BLUE_D,
             "700")

    s += box(450, y2, 380, 96, GREEN_BG, GREEN, 1.4, rx=10)
    s += txt(640, y2 + 22, "MOLECULAR 分子化合物", 14, GREEN, "700")
    s += txt(640, y2 + 44, "电子共用 sharing → 希腊前缀法", 11, INK, "400")
    s += txt(640, y2 + 62, "第 1 元素 >1 才加前缀，永不用 mono-", 11, INK,
             "400")
    s += txt(640, y2 + 82, "例 CO₂ carbon dioxide 二氧化碳", 11, GREEN, "700")

    y3 = y2 + 116
    s += box(70, y3, 760, 62, "#FFF8E1", ORANGE, 1.2, rx=8)
    s += txt(90, y3 + 22, "⚠ 两个例外：", 12, ORANGE_D, "700", "start")
    s += txt(90, y3 + 44,
             "① NH₄⁺ 铵根全是非金属，但它是阳离子 → 按离子化合物处理（NH₄Cl 氯化铵）",
             11, INK, "400", "start")
    s += txt(90, y3 + 60,
             "② CO₂、H₂O 不能用交叉法（会得出 CO 或 C₂O₄）——交叉法只对离子化合物成立",
             11, INK, "400", "start")

    y4 = y3 + 78
    s += box(70, y4, 760, 34, NEUTRAL_BG, EDGE, 1.0, rx=7)
    s += txt(450, y4 + 17, "看图要点：先看元素种类定类型，再看性质只是验证",
             12, INK, "700")
    return wrap(s)


# ==================================================== 附录 C-7 中英顺序相反
def fig_appc_cn_en_order():
    # 顶部警示条 58–92，中间两层 132–208 / 296–372，底部正反例 400–460
    s = head(900, 486, "附录 C-7　中英命名顺序相反｜Opposite Word Order",
             "英文：正在前　中文：负在前")
    s += box(50, 58, 800, 34, RED, RED, 1.2, rx=8)
    s += txt(450, 75, "🚨 对中国学生的头号警示：照着英文顺手写中文，一定写反",
             12.5, "#FFFFFF", "700")

    # 上：英文
    s += txt(450, 116, "ENGLISH　英文：正离子在前 → 负离子在后", 12, BLUE_D,
             "700")
    s += box(70, 132, 760, 76, BLUE_BG, BLUE, 1.2, rx=8)
    s += txt(240, 158, "sodium", 17, BLUE_D, "700")
    s += txt(240, 182, "正离子 Na⁺", 10.5, SUB, "400")
    s += txt(450, 170, "＋", 15, LINE, "700")
    s += txt(660, 158, "chloride", 17, BLUE_D, "700")
    s += txt(660, 182, "负离子 Cl⁻", 10.5, SUB, "400")
    s += txt(450, 222, "→ sodium chloride（正在前，负在后）", 12, BLUE_D,
             "700")

    # 中间箭头
    s += path("M450 236 L450 262", INK, 1.8, marker="ar")
    s += txt(450, 250, "顺序完全相反！", 12, RED, "700")

    # 下：中文
    s += txt(450, 282, "中文　中文：负在前 → 正在后（「某化某」）", 12, GREEN,
             "700")
    s += box(70, 296, 760, 76, GREEN_BG, GREEN, 1.2, rx=8)
    s += txt(240, 322, "氯", 17, GREEN, "700")
    s += txt(240, 346, "负（非金属）", 10.5, SUB, "400")
    s += txt(450, 334, "化", 15, INK, "700")
    s += txt(660, 322, "钠", 17, GREEN, "700")
    s += txt(660, 346, "正（金属）", 10.5, SUB, "400")
    s += txt(450, 386, "→ 氯化钠（负在前，正在后）", 12, GREEN, "700")

    # 正反例
    s += box(70, 400, 760, 60, "#FFFFFF", EDGE, 1.0, rx=8)
    s += txt(90, 420, "✗ 钠化氯　✗ 镁化氧　✗ 铝化硫　✗ 碳化二氧　✗ 磷化三氯",
             11.5, RED, "600", "start")
    s += txt(90, 444,
             "✅ 氯化钠　✅ 氧化镁　✅ 硫化铝　✅ 二氧化碳　✅ 三氯化磷",
             11.5, GREEN, "600", "start")
    return wrap(s)


# ==================================================== 附录 C 一页纸速查卡
def fig_appc_cheat_sheet():
    s = head(900, 486, "附录 C　命名速查卡｜Naming Cheat Sheet",
             "一页纸：判类型 → 走流程 → 查例外")

    # STEP 1
    s += box(50, 62, 800, 46, NEUTRAL_BG, INK, 1.2, rx=8)
    s += badge(84, 85, 12, "1", INK, size=11)
    s += txt(104, 85, "STEP 1　有金属 或 NH₄⁺ ？", 13, INK, "700", "start")
    s += txt(560, 85, "YES → IONIC（交叉法 + -ide）　NO → MOLECULAR（前缀法）",
             11.5, INK, "600", "start")

    # IONIC
    s += box(50, 118, 800, 150, BLUE_BG, BLUE, 1.3, rx=10)
    s += txt(70, 140, "IONIC 离子化合物", 14, BLUE_D, "700", "start")
    steps = ["① 写离子（正离子在前）", "② 电荷交叉 → 下标", "③ 约成最简整数比",
             "④ 下标 1 不写", "⑤ 验算总电荷 = 0"]
    for i, t in enumerate(steps):
        c, r = divmod(i, 3)
        s += txt(90 + c * 250, 166 + r * 22, t, 11.5, INK, "400", "start")
    s += txt(70, 216, "命名：金属名 + 非金属词根 -ide", 12, BLUE_D, "700",
             "start")
    s += txt(70, 238, "多变价 → 金属名(罗马数字)　多原子离子 → 照抄离子名，不改词尾",
             11, INK, "400", "start")
    s += txt(70, 258, "例　MgF₂ magnesium fluoride 氟化镁", 11.5, BLUE_D,
             "700", "start")

    # MOLECULAR
    y2 = 280
    s += box(50, y2, 800, 150, GREEN_BG, GREEN, 1.3, rx=10)
    s += txt(70, y2 + 22, "MOLECULAR 分子化合物", 14, GREEN, "700", "start")
    s += txt(70, y2 + 48, "第 1 元素：> 1 才加前缀，永不用 mono-", 11.5, INK,
             "400", "start")
    s += txt(70, y2 + 70, "第 2 元素：必加前缀 + 词尾改 -ide", 11.5, INK,
             "400", "start")
    pref_en = "mono  di  tri  tetra  penta  hexa  hepta  octa  nona  deca"
    pref_cn = "一    二   三   四     五     六     七     八     九     十"
    s += txt(70, y2 + 96, pref_en, 11, GREEN, "700", "start")
    s += txt(70, y2 + 116, pref_cn, 11, GREEN, "700", "start")
    s += txt(70, y2 + 140, "例　N₂O₄ dinitrogen tetroxide 四氧化二氮", 11.5,
             GREEN, "700", "start")

    # 顺序警示
    y3 = 442
    s += box(50, y3, 800, 40, "#FFF8E1", ORANGE, 1.3, rx=8)
    s += txt(70, y3 + 15, "🚨 中英顺序相反", 12, ORANGE_D, "700", "start")
    s += txt(230, y3 + 15, "英文：正在前 → sodium chloride", 11.5, INK, "600",
             "start")
    s += txt(560, y3 + 15, "中文：负在前 → 氯化钠　✗钠化氯", 11.5, RED, "600",
             "start")
    return wrap(s)


# ==================================================== 附录 E 参考图（练习单用）
def fig_appe_variables():
    """变量三栏 + 公平实验（E 实验报告模板里的参考图）"""
    s = head(900, 330, "变量与公平实验｜Variables &amp; Fair Test",
             "附录 E · 一次只改一个变量")
    cols = [("INDEPENDENT 自变量", "I change it 我改的", BLUE_BG, BLUE_D),
            ("DEPENDENT 因变量", "I measure it 我测的", ORANGE_BG, ORANGE_D)]
    for i, (t, sub, bg, fg) in enumerate(cols):
        x = 70 + i * 470
        s += box(x, 66, 290, 62, bg, fg, 1.2, rx=8)
        s += txt(x + 145, 88, t, 12.5, fg, "700")
        s += txt(x + 145, 110, "（%s）" % sub, 10.5, SUB, "400")
    # 中间的公平实验框
    s += box(330, 150, 240, 62, GREEN_BG, GREEN, 1.4, rx=10)
    s += txt(450, 172, "FAIR TEST 公平实验", 13, GREEN, "700")
    s += txt(450, 194, "一次只改自变量，其余全部保持不变", 10.5, INK, "400")
    # 箭头
    s += path("M215 128 L330 172", BLUE, 1.6, marker="ar")
    s += path("M450 212 L450 240", GREEN, 1.6, marker="ar")
    s += path("M450 240 L215 250 L215 128", ORANGE, 1.6, dash="5 3")
    s += path("M685 128 L570 172", ORANGE, 1.6, marker="ar")
    # 控制变量
    s += box(70, 250, 760, 52, NEUTRAL_BG, EDGE, 1.0, rx=8)
    s += txt(450, 272, "CONTROLLED 控制变量（keep the same 保持不变）", 12,
             INK, "700")
    s += txt(450, 290, "须**逐条列出**清单，只写「保持不变」不给满分", 10.5,
             SUB, "400")
    return wrap(s)


def fig_appe_matter_tree():
    """物质分类树（E 卡片分类活动的参考树状图）"""
    s = head(900, 356, "物质分类树｜Matter Classification Tree",
             "附录 E · 先分两大支，再往下细分")
    s += box(370, 62, 160, 40, NEUTRAL_BG, INK, 1.3, rx=8)
    s += txt(450, 82, "MATTER 物质", 13, INK, "700")
    s += path("M450 102 L450 122", INK, 1.6)
    s += path("M250 122 L650 122", INK, 1.6)
    s += path("M250 122 L250 142", INK, 1.6)
    s += path("M650 122 L650 142", INK, 1.6)

    def node(x, y, w, t, sub, bg, fg):
        s = box(x - w / 2, y, w, 56, bg, fg, 1.2, rx=8)
        s += txt(x, y + 22, t, 12.5, fg, "700")
        s += txt(x, y + 42, sub, 10.5, SUB, "400")
        return s

    s += node(250, 142, 200, "纯净物", "pure substance", BLUE_BG, BLUE_D)
    s += node(650, 142, 200, "混合物", "mixture", ORANGE_BG, ORANGE_D)
    y2 = 216
    for x in (250, 650):
        s += path("M%d 198 L%d %d" % (x, x, y2 - 12), LINE, 1.4)
    s += path("M150 %d L350 %d" % (y2 - 12, y2 - 12), LINE, 1.4)
    s += path("M550 %d L750 %d" % (y2 - 12, y2 - 12), LINE, 1.4)
    for x in (150, 350, 550, 750):
        s += path("M%d %d L%d %d" % (x, y2 - 12, x, y2), LINE, 1.4)
    s += node(150, y2, 150, "单质 / 元素", "element", GREEN_BG, GREEN)
    s += node(350, y2, 150, "化合物", "compound", GREEN_BG, GREEN)
    s += node(550, y2, 160, "均一混合物", "homogeneous", "#FFF8E1", ORANGE_D)
    s += node(750, y2, 170, "非均一混合物", "heterogeneous", "#FFF8E1",
              ORANGE_D)
    s += box(70, 296, 760, 40, NEUTRAL_BG, EDGE, 1.0, rx=8)
    s += txt(450, 316, "关键词：纯净物 = fixed ratio 固定配比；"
                       "混合物 = variable composition 组成可变", 11.5, INK,
             "700")
    return wrap(s)


def fig_appe_circuit():
    """导电性检测电路（E 金属/非金属检测实验的示意图）"""
    s = head(900, 356, "导电性检测电路｜Conductivity Circuit",
             "附录 E · 灯泡亮度 = 导电能力")
    # 回路
    s += box(180, 78, 540, 150, "#FFFFFF", EDGE, 1.0, rx=8)
    # 上边：灯泡
    s += path("M300 78 L300 130", INK, 2.0)
    s += path("M300 130 L600 130", INK, 2.0)
    s += path("M600 130 L600 78", INK, 2.0)
    s += path("M180 78 L300 78", INK, 2.0)
    s += path("M600 78 L720 78 L720 228", INK, 2.0)
    s += path("M180 228 L180 78", INK, 2.0)
    # 灯泡符号 ( ◡ )
    s += path("M420 130 A 26 26 0 0 1 472 130", INK, 2.2)
    s += path("M396 130 L496 130", INK, 2.2)
    s += txt(560, 118, "( ◡ ) = bulb 小灯泡", 10.5, SUB, "400", "start")
    # 两个电极
    s += path("M300 130 L300 176", INK, 2.0)
    s += path("M600 130 L600 176", INK, 2.0)
    s += box(272, 176, 56, 26, NEUTRAL_BG, INK, 1.0, rx=3)
    s += txt(300, 189, "电极 1", 10.5, INK, "700")
    s += box(572, 176, 56, 26, NEUTRAL_BG, INK, 1.0, rx=3)
    s += txt(600, 189, "电极 2", 10.5, INK, "700")
    s += box(340, 202, 220, 30, BLUE_BG, BLUE, 1.2, rx=6)
    s += txt(450, 217, "sample 样品（两电极同时插入/接触）", 11, BLUE_D, "700")
    s += path("M180 228 L720 228", INK, 2.0)
    s += box(390, 228, 120, 26, "#FFFFFF", INK, 1.0, rx=3)
    s += txt(450, 241, "battery 电池", 10.5, INK, "700")

    # 亮度等级
    s += box(70, 254, 760, 82, "#FFF8E1", ORANGE, 1.2, rx=8)
    s += txt(450, 274, "Brightness scale 亮度等级", 12, ORANGE_D, "700")
    levels = [("0", "不亮 dark"), ("1", "微亮 dim"),
              ("2", "较亮 bright"), ("3", "最亮 very bright")]
    for i, (n, t) in enumerate(levels):
        x = 130 + i * 170
        s += box(x, 288, 130, 34, "#FFFFFF", EDGE, 0.9, rx=6)
        s += txt(x + 65, 300, n, 13, INK, "700")
        s += txt(x + 65, 315, t, 9.5, SUB, "400")
    return wrap(s)


FIGURES = {
    "appc-naming-decision-tree.svg": fig_appc_decision_tree,
    "appc-cn-en-order.svg": fig_appc_cn_en_order,
    "appc-cheat-sheet.svg": fig_appc_cheat_sheet,
    "appe-variables-fair-test.svg": fig_appe_variables,
    "appe-matter-tree.svg": fig_appe_matter_tree,
    "appe-conductivity-circuit.svg": fig_appe_circuit,
    "appe-bohr-Na.svg": lambda: bohr_figure(
        "Na 钠参考图例｜Reference Diagram",
        "附录 E · 2, 8, 8 规则，内层满才能进外层",
        {"sym": "Na", "cn": "钠", "z": 11, "shells": [2, 8, 1], "a": 23,
         "foot": "Z = 11　A = 23　中子数 n⁰ = 23 − 11 = 12"}),
    "appe-bohr-P31.svg": lambda: bohr_figure(
        "磷-31 P-31 Bohr 图（参考答案）",
        "附录 E · C1　三层 2, 8, 5　价电子 = 5",
        {"sym": "P", "cn": "磷", "z": 15, "shells": [2, 8, 5], "a": 31,
         "foot": "Group 族 15　Period 周期 3　价电子 5"}),
    "appe-bohr-Ca40.svg": lambda: bohr_figure(
        "钙-40 Ca-40 Bohr 图（参考答案）",
        "附录 E · C2　四层 2, 8, 8, 2　价电子 = 2",
        {"sym": "Ca", "cn": "钙", "z": 20, "shells": [2, 8, 8, 2], "a": 40,
         "foot": "Group 族 2　Period 周期 4　价电子 2"}),
}


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name, fn in FIGURES.items():
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(fn())
        print("OK ", name)


if __name__ == "__main__":
    main()
