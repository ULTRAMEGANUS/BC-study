# -*- coding: utf-8 -*-
"""SCI 10 REV WORKSHEET 0–3 → 英中对照版 PDF（题目页对照，答案页原样保留）。

用法：
    env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL <python> build_rev_bilingual.py

产物：G10/pdf/（本年级统一 PDF 目录），文件名后缀 `_EN-CN.pdf`。
      原件仍从 G10/CHEM10 rev/ 读取，不动原件。
结构：
    对照页（题目页，逐行 中文 用 ｜ 跟在英文后）
  + 原答案页（从原件按页插入，不做任何改动）

要点：
- 原卷是 US Letter 612×792pt，CSS @page 必须一致，否则合并后页尺寸不齐。
- 中文列用灰色小字内联，保持"一原页 → 一对照页"的行数对应，学生仍可在空白处作答。
- 化学式用 <sub> 正常排下标（原卷是平排的纯文本）。
- Chrome 渲染走 html2pdf.py（非 ASCII 文件名会静默丢失，它已用 ASCII 临时名中转）。
"""
import os
import re
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
G10 = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # G10/
REV = os.path.join(G10, "CHEM10 rev")                                 # 原件目录（只读）
OUT = os.path.join(G10, "pdf")                                        # 产物目录
BUILD = os.path.join(HERE, "_build_rev")                              # 中间产物
sys.path.insert(0, HERE)
from html2pdf import find_chrome, render                             # noqa: E402

# --------------------------------------------------------------------------- #
# 排版小工具
# --------------------------------------------------------------------------- #
BL = lambda px=70: f'<span class="b" style="min-width:{px}px"></span>'   # 填空横线


def li(en, cn="", gap=0, bullet="", indent=0):
    """一行对照。en 可含 HTML；cn 为纯文本。gap=下方留白(mm)。"""
    pad = f"margin-left:{indent}mm;" if indent else ""
    g = f' style="{pad}margin-bottom:{gap}mm"' if (pad or gap) else ""
    c = f' <span class="cn">｜{cn}</span>' if cn else ""
    b = f'<span class="bul">{bullet}</span>' if bullet else ""
    return f'<div class="li"{g}>{b}<span class="en">{en}</span>{c}</div>'


def h1(en, cn):
    return f'<h1>{en} <span class="cn">｜{cn}</span></h1>'


def h2(en, cn):
    return f'<h2>{en} <span class="cn">｜{cn}</span></h2>'


CSS = """
@page { size: 612pt 792pt; margin: 34pt 38pt 28pt 38pt; }
* { box-sizing: border-box; }
body { font-family: Calibri, "Segoe UI", "Microsoft YaHei", sans-serif;
       font-size: 10pt; line-height: 1.28; color: #1b1b1b; margin: 0; }
h1 { font-size: 14pt; margin: 0 0 3pt; padding-bottom: 2pt;
     border-bottom: 2px solid #1b1b1b; }
h2 { font-size: 11.5pt; margin: 8pt 0 3pt; color: #0B4F6C;
     border-bottom: 1px solid #cbd5e1; padding-bottom: 1.5pt; }
.cn { color: #5a5a5a; font-size: 8.6pt; font-weight: normal; }
.cnb { color: #5a5a5a; font-size: 9pt; }
.li { margin: 1pt 0; }
.bul { display: inline-block; width: 3.6mm; color: #444; }
.b { display: inline-block; border-bottom: 1px solid #8b8b8b;
     height: 0.92em; vertical-align: -0.12em; min-width: 40px; }
.ans { display: inline-block; border-bottom: 1px solid #b9b9b9;
       height: 0.92em; min-width: 60px; }
.gap { height: 7mm; }
.gap6 { height: 6mm; }
.sub { font-size: 9pt; color: #8a8a8a; }
table { border-collapse: collapse; width: 100%; font-size: 9.5pt; margin-top: 3pt; }
th, td { border: 1px solid #94a3b8; padding: 3pt 4pt; vertical-align: top; }
th { background: #EAF2F8; font-weight: 600; }
td.tw { height: 17pt; }
.note { background: #F1F6FA; border-left: 3px solid #0B4F6C;
        padding: 3pt 5pt; font-size: 8.4pt; margin: 3pt 0 5pt; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.foot { margin-top: 8pt; font-size: 9pt; color: #666; font-style: italic; }
"""

NOTE = ('<div class="note">中英对照版｜<b>English–Chinese bilingual edition</b>：'
        '中文列仅供理解参考，<b>作答请用英文</b>（化学式与英文命名必须用英文书写）。'
        '答案页保留原件原样。Answer keys on the following pages are kept as the original.</div>')

# --------------------------------------------------------------------------- #
# WS0 · Science 10 Review Notes（2 页题目）
# --------------------------------------------------------------------------- #
ws0_p1 = [
    h1("Chemistry 11 — Science 10 Review Notes", "化学 11 · Science 10 复习讲义"),
    NOTE,
    li("Name: " + BL(120) + "　Date: " + BL(90) + "　Block: " + BL(60),
       "姓名 / 日期 / 班级"),
    h2("Warm Up", "热身题"),
    li("1. " + BL(430), "", gap=1.2),
    li("2. " + BL(430), "", gap=1.2),
    li("3. " + BL(430), "", gap=1.2),
    li("4. " + BL(430), "", gap=1.2),
    li("5. " + BL(430), "", gap=1.2),
    h2("Periodic Table Tips", "周期表要点"),
    li("Charges for…", "各族的常见电荷"),
    li("Group 1 (Alkali Metals): " + BL(90), "第 1 族（碱金属）：", bullet="•"),
    li("Group 2 (Alkaline Earth Metals): " + BL(90), "第 2 族（碱土金属）：", bullet="•"),
    li("Groups 3–12 (Transition Metals): Most of these are " + BL(130) + ". You can tell what "
       "the charge is by looking at the name or formula of the compound.",
       "第 3–12 族（过渡金属）：大多数是 ______；其电荷可从化合物的名称或化学式反推。",
       bullet="•"),
    li("Group 13: " + BL(90), "第 13 族：", bullet="•"),
    li("Group 14: " + BL(90), "第 14 族：", bullet="•"),
    li("Group 15: " + BL(90), "第 15 族：", bullet="•"),
    li("Group 16: " + BL(90), "第 16 族：", bullet="•"),
    li("Group 17 (Halogens): " + BL(90), "第 17 族（卤素）：", bullet="•"),
    li("Group 18 (Noble Gases): " + BL(90), "第 18 族（稀有气体）：", bullet="•"),
    h2("Diatomic Molecules", "双原子分子"),
    li("“H-7 Rule” or “Rule of 7” (" + BL(230) + ")",
       "“H-7 法则”，又叫“七兄弟法则”（______）", bullet="•"),
    li("Also: P<sub>4</sub>, S<sub>8</sub>", "另外还有：P₄、S₈", bullet="•"),
    h2("Naming…", "命名……"),
    li("1. Ionic Compounds (metal &amp; non-metal)", "1. 离子化合物（金属 + 非金属）", bullet="•"),
    li("Write the name of the " + BL(80) + " first", "先写 ______ 的名称", bullet="•", indent=4),
    li("Write the name of the " + BL(120) + " second and change the ending to " + BL(70),
       "第二个写 ______ 的名称，并把词尾改成 ______（中文则用「化」）", bullet="•", indent=4),
    li("If the metal has " + BL(140) + " (ie. transition metals), include a roman numeral "
       "to indicate which one it is",
       "如果金属有 ______（如过渡金属），须用罗马数字标明是哪一个", bullet="•", indent=4),
    li("When naming ionic compounds with polyatomic ions, pretend the polyatomic ion is just one "
       "atom and follow the same rules",
       "命名含多原子离子的离子化合物时，把多原子离子当作“一个原子”套用同样的规则",
       bullet="•", indent=4),
    li("Examples　MgF<sub>2</sub>　CuCl<sub>2</sub>　KPO<sub>4</sub>",
       "例：氟化镁、氯化铜(II)、磷酸钾", bullet="•", indent=4),
    li("2. Covalent Compounds (2 non-metals)", "2. 共价化合物（两种非金属）", bullet="•"),
    li("Write the name of the first non-metal", "先写第一种非金属的名称", bullet="•", indent=4),
    li("Write the name of the second non-metal and change the ending to " + BL(70),
       "第二种非金属名称的词尾改成 -ide", bullet="•", indent=4),
    li("Use " + BL(150) + " to express how many of each non-metal are present",
       "用 ______ 表示每种非金属的个数", bullet="•", indent=4),
    li("You do not use a prefix when there is only one of the first non-metal",
       "第一种非金属只有 1 个时不加前缀（永不用 mono-）", bullet="o", indent=8),
    li("Example　SO<sub>2</sub>　Si<sub>3</sub>N<sub>4</sub>",
       "例：二氧化硫、四氮化三硅", bullet="o", indent=8),
]

ws0_p2 = [
    li('<span class="sub">Chemistry 11 — Science 10 Review Notes（续）</span>'),
    h2("Formulas…", "化学式……"),
    li("1. Ionic Compounds", "1. 离子化合物", bullet="•"),
    li("Add " + BL(90) + " so that the positive charges balance the negative charges "
       "(“drop and swap” or “criss-cross”)",
       "添加 ______，使正电荷总数与负电荷总数相等（“drop and swap” / 交叉法）", bullet="•", indent=4),
    li("If the metal has more than one charge, the charge will be indicated by the " + BL(110),
       "若金属有多个电荷，其电荷由 ______ 标明", bullet="•", indent=4),
    li("When writing formulas of ionic compounds with polyatomic ions, pretend the polyatomic "
       "ion is just one atom and follow the same rules",
       "含多原子离子时同样把它当成“一个原子”，必要时加括号", bullet="•", indent=4),
    li("Examples　Magnesium phosphide　Iron (III) sulfide　Calcium carbonate",
       "例：磷化镁、硫化铁(III)、碳酸钙", bullet="•", indent=4),
    li("2. Covalent Compounds", "2. 共价化合物", bullet="•"),
    li("The prefixes indicate how many of each non-metal are present",
       "前缀表示每种非金属的个数", bullet="•", indent=4),
    li("Examples　Phosphorus trioxide　Dinitrogen pentacarbide",
       "例：三氧化磷、五碳化二氮", bullet="•", indent=4),
    h2("Acids, Bases &amp; Salts", "酸、碱、盐"),
    li("Acids:", "酸（acid）", bullet="•"),
    li("Formulas usually start with " + BL(70), "化学式通常以 ______ 开头", bullet="o", indent=4),
    li("Example: " + BL(140), "例：______", bullet="o", indent=4),
    li("Bases", "碱（base）", bullet="•"),
    li("Formulas usually end with " + BL(70), "化学式通常以 ______ 结尾", bullet="o", indent=4),
    li("Example: " + BL(140), "例：______", bullet="o", indent=4),
    li("Salts", "盐（salt）", bullet="•"),
    li("Salts are ionic compounds (metal and non-metal)",
       "盐是离子化合物（金属 + 非金属，或含多原子离子）", bullet="o", indent=4),
    li("Example: " + BL(140), "例：______", bullet="o", indent=4),
    h2("Types of Reactions", "反应类型"),
    """<table>
<tr><th style="width:30%">Type｜类型</th><th style="width:31%">General Formula｜一般式</th>
<th>Example｜例</th></tr>
<tr><td class="tw">1. Synthesis｜合成</td><td></td><td></td></tr>
<tr><td class="tw">2. Decomposition｜分解</td><td></td><td></td></tr>
<tr><td class="tw">3. Single Replacement｜单置换</td><td></td><td></td></tr>
<tr><td class="tw">4. Double Replacement｜双置换</td><td></td><td></td></tr>
<tr><td class="tw">5. Neutralization｜中和</td><td></td><td></td></tr>
<tr><td class="tw">6. Combustion｜燃烧</td><td></td><td></td></tr>
</table>""",
    '<div class="foot">Practice: Science 10 Chemistry Review ｜ 练习：Science 10 化学复习</div>',
]

# --------------------------------------------------------------------------- #
# WS1 · Science 10 Review（2 页题目）
# --------------------------------------------------------------------------- #
WS1_FORMULA = [
    ("Barium nitride", "氮化钡"), ("Lithium oxide", "氧化锂"),
    ("Aluminum sulphide", "硫化铝（sulphide = sulfide）"), ("Copper(II) oxide", "氧化铜(II)"),
    ("Zinc(II) fluoride", "氟化锌"), ("Chromium(III) nitride", "氮化铬(III)"),
    ("Silver oxalate", "草酸银"), ("Chromium(II) acetate", "乙酸铬(II)〔醋酸铬(II)〕"),
    ("Gold (III) chromate", "铬酸金(III)"),
]
WS1_NAME = [
    ("GaAs", "砷化镓"), ("KCl", "氯化钾"), ("Ni<sub>3</sub>P<sub>2</sub>", "磷化镍(II)"),
    ("TiO<sub>2</sub>", "二氧化钛"), ("Au<sub>2</sub>Se", "硒化金(I)"),
    ("Ag<sub>2</sub>C<sub>2</sub>O<sub>4</sub>", "草酸银"),
    ("Na<sub>2</sub>CrO<sub>4</sub>", "铬酸钠"),
    ("Cr(NO<sub>3</sub>)<sub>2</sub>", "硝酸铬(II)"),
]

ws1_p1 = [h1("Chemistry 11 — Science 10 Review", "化学 11 · Science 10 复习"), NOTE,
          li("Name: " + BL(120) + "　Date: " + BL(90) + "　Block: " + BL(60),
             "姓名 / 日期 / 班级"),
          h2("Write the formula for the following compounds",
             "写出下列化合物的化学式")]
for i, (en, cn) in enumerate(WS1_FORMULA, 1):
    ws1_p1.append(li(f"{i}. {en}" + BL(150), cn, gap=6))
ws1_p1.append(h2("Write the name for the following compounds", "写出下列化合物的名称"))
for i, (en, cn) in enumerate(WS1_NAME, 1):
    ws1_p1.append(li(f"{i}. {en}" + BL(150), cn, gap=6))

ws1_p2 = [
    li('<span class="sub">Chemistry 11 — Science 10 Review（续）</span>'),
    h2("Classify each of the following as an acid, base, or salt",
       "判断下列各物质是酸、碱还是盐"),
]
for i, (en, cn) in enumerate([
    ("Potassium hydroxide", "氢氧化钾"), ("Has a pH of 3", "pH 为 3"),
    ("NaCl", "氯化钠"), ("Magnesium carbonate", "碳酸镁"), ("HF", "氢氟酸"),
    ("LiOH", "氢氧化锂"), ("Tastes bitter", "尝起来是苦的"),
    ("Calcium nitrate", "硝酸钙"), ("H<sub>3</sub>PO<sub>4</sub>", "磷酸"),
    ("Sr(OH)<sub>2</sub>", "氢氧化锶"),
], 1):
    ws1_p2.append(li(f"{i}. {en}" + BL(70), cn, gap=1.2))
ws1_p2.append(h2("Balance the following reaction and classify the type of chemical reaction",
                 "配平下列反应并判断反应类型"))
ws1_p2.append(li("1. ___ CH<sub>4</sub> + ___ O<sub>2</sub> → ___ CO<sub>2</sub> + ___ H<sub>2</sub>O",
                 "甲烷燃烧", gap=3))
ws1_p2.append(li("2. ___ B + ___ Cl<sub>2</sub> → ___ BCl<sub>3</sub>", "硼 + 氯气", gap=3))
ws1_p2.append(li("3. ___ Ca + ___ HCl → ___ H<sub>2</sub> + ___ CaCl<sub>2</sub>",
                 "钙 + 盐酸", gap=3))
ws1_p2.append(li("4. ___ HClO + ___ O<sub>2</sub> → ___ HClO<sub>4</sub>",
                 "次氯酸 + 氧气", gap=3))
ws1_p2.append(li("5. ___ C<sub>25</sub>H<sub>52</sub> + ___ O<sub>2</sub> → ___ CO<sub>2</sub> "
                 "+ ___ H<sub>2</sub>O", "石蜡（C₂₅H₅₂）燃烧", gap=3))
ws1_p2.append(li("6. ___ Hg<sub>2</sub>SO<sub>3</sub> → ___ Hg + ___ S + ___ O<sub>2</sub>",
                 "亚硫酸汞(I) 分解", gap=3))
ws1_p2.append(li("7. ___ CH<sub>3</sub>COOH + ___ Ti(OH)<sub>3</sub> → "
                 "___ Ti(CH<sub>3</sub>COO)<sub>3</sub> + ___ H<sub>2</sub>O",
                 "乙酸 + 氢氧化钛(III)（中和反应）", gap=3))
ws1_p2.append(h2("Write the complete balanced chemical reactions for the following",
                 "根据下列描述写出完整并配平的化学方程式"))
ws1_p2.append(li("a) Potassium hydroxide and hydrogen are produced when potassium metal reacts "
                 "with water." + BL(120), "钾与水反应，生成氢氧化钾和氢气。", gap=6))
ws1_p2.append(li("b) The reaction between magnesium metal and copper(II) sulphate." + BL(120),
                 "镁与硫酸铜之间的反应。", gap=6))
ws1_p2.append(li("c) Decomposition of mercury(II) oxide to its elements." + BL(120),
                 "氧化汞分解为其组成元素。", gap=6))

# --------------------------------------------------------------------------- #
# WS2 · Science 10 Review 2（2 页题目）
# --------------------------------------------------------------------------- #
ws2_p1 = [h1("Chemistry 11 — Science 10 Review 2", "化学 11 · Science 10 复习（二）"), NOTE,
          li("Name: " + BL(120) + "　Date: " + BL(90) + "　Block: " + BL(60),
             "姓名 / 日期 / 班级")]
ws2_p1.append(h2("Write the names of the following", "写出下列物质的名称"))
ws2_p1.append('<table><tr>'
              + "".join(f'<td>{li(en + BL(80), cn)}</td>' for en, cn in [
                  ("NaCl", "氯化钠"), ("O<sub>2</sub>F<sub>5</sub>", "五氟化二氧"),
                  ("Mg(OH)<sub>2</sub>", "氢氧化镁"), ("CuCl", "氯化铜(I)"),
                  ("SO<sub>4</sub>", "四氧化硫"), ("Ag<sub>2</sub>HPO<sub>4</sub>", "磷酸氢银"),
              ]) + '</tr></table>')
ws2_p1.append(h2("Write the formulas for the following compounds", "写出下列化合物的化学式"))
ws2_p1.append('<table><tr>'
              + "".join(f'<td>{li(en + BL(80), cn)}</td>' for en, cn in [
                  ("Chromium (III) oxide", "氧化铬(III)"), ("Strontium sulphate", "硫酸锶"),
                  ("Iron (III) oxalate", "草酸铁(III)"), ("Potassium oxide", "氧化钾"),
              ]) + '</tr></table>')
ws2_p1.append(h2("Write the formulas and balance the word equations",
                 "写出化学式并配平下列文字方程式"))
for i, (en, cn) in enumerate([
    ("Sodium + Oxygen gas → Sodium oxide", "钠 + 氧气 → 氧化钠"),
    ("Rubidium + Nitrogen gas → Rubidium nitride", "铷 + 氮气 → 氮化铷"),
    ("Fluorine gas + Magnesium chloride → Magnesium fluoride + Chlorine gas",
     "氟气 + 氯化镁 → 氟化镁 + 氯气"),
    ("Aluminum chloride + Potassium → Potassium chloride + Aluminum",
     "氯化铝 + 钾 → 氯化钾 + 铝"),
    ("Iron (III) chlorate → Iron (III) chlorite + Oxygen gas",
     "氯酸铁(III) → 亚氯酸铁(III) + 氧气"),
    ("Aluminum + Phosphoric acid (H<sub>3</sub>PO<sub>4</sub>) → Aluminum phosphate + Hydrogen gas",
     "铝 + 磷酸 → 磷酸铝 + 氢气"),
    ("Potassium chlorate → Potassium chloride + Oxygen gas",
     "氯酸钾 → 氯化钾 + 氧气"),
    ("Copper + Silver acetate → Copper (II) acetate + Silver",
     "铜 + 乙酸银 → 乙酸铜(II) + 银"),
], 1):
    ws2_p1.append(li(f"{i}. {en}", cn, gap=6))

ws2_p2 = [
    li('<span class="sub">Chemistry 11 — Science 10 Review 2（续）</span>'),
    h2("Determine the reaction type, predict the products and balance the following equations",
       "判断反应类型、预测产物并配平下列方程式"),
]
for en, cn in [("Aluminum oxide + Zinc →", "氧化铝 + 锌"),
               ("Carbon + Oxygen gas →", "碳 + 氧气"),
               ("SrF<sub>2</sub> →", "氟化锶"),
               ("HCl + Ca(OH)<sub>2</sub> →", "盐酸 + 氢氧化钙"),
               ("CH<sub>4</sub> + O<sub>2</sub> →", "甲烷 + 氧气"),
               ("CaCl<sub>2</sub> + Al<sub>2</sub>O<sub>3</sub> →", "氯化钙 + 氧化铝")]:
    ws2_p2.append(li(en, cn, gap=7))
ws2_p2.append(h2("Balance the following equations", "配平下列方程式"))
for a, b in [("HgCl<sub>2</sub>", "H<sub>2</sub>S"), ("Hg<sub>3</sub>S<sub>2</sub>Cl<sub>2</sub>", "HCl"),
             ("Bi(NO<sub>3</sub>)<sub>3</sub>", "H<sub>2</sub>S"),
             ("Bi<sub>2</sub>S<sub>3</sub>", "HNO<sub>3</sub>"), ("Sb<sub>2</sub>O<sub>5</sub>", "HCl"),
             ("SbCl<sub>5</sub>", "H<sub>2</sub>O"),
             ("Na<sub>3</sub>AsO<sub>3</sub>+HCl", "H<sub>2</sub>S"),
             ("As<sub>2</sub>S<sub>3</sub>+NaCl", "H<sub>2</sub>O"),
             ("K<sub>2</sub>SnO<sub>3</sub>+K<sub>2</sub>SnS<sub>3</sub>", "HCl"),
             ("SnS<sub>2</sub>", "KCl+H<sub>2</sub>O"),
             ("FeCl<sub>3</sub>+NH<sub>4</sub>HS", "NH<sub>3</sub>"),
             ("Fe<sub>2</sub>S<sub>3</sub>", "NH<sub>4</sub>Cl"),
             ("C<sub>5</sub>H<sub>12</sub>NO<sub>2</sub>", "O<sub>2</sub>"),
             ("C<sub>3</sub>H<sub>5</sub>N<sub>3</sub>O<sub>6</sub>", "O<sub>2</sub>"),
             ("C<sub>10</sub>H<sub>19</sub>NO<sub>2</sub>", "O<sub>2</sub>"),
             ("As<sub>4</sub>+NaOCl+H<sub>2</sub>O", "H<sub>3</sub>AsO<sub>4</sub>+NaCl")]:
    ws2_p2.append(li(f"_____{a} + _____{b}", "", gap=0.4))

# --------------------------------------------------------------------------- #
# WS3 · Science 10 Review 2（1 页题目）
# --------------------------------------------------------------------------- #
ws3_p1 = [h1("Chemistry 11 — Science 10 Review 2", "化学 11 · Science 10 复习（二）"), NOTE,
          li("Name: " + BL(120) + "　Date: " + BL(90) + "　Block: " + BL(60),
             "姓名 / 日期 / 班级")]
ws3_p1.append(h2("Write the names of the following", "写出下列物质的名称"))
ws3_p1.append('<table><tr>' + "".join(f'<td>{li(en + BL(80), cn)}</td>' for en, cn in [
    ("Sr<sub>3</sub>P<sub>2</sub>", "磷化锶"), ("KMnO<sub>4</sub>", "高锰酸钾"),
    ("Na<sub>3</sub>N", "氮化钠"), ("NiCl<sub>2</sub>", "氯化镍(II)"),
]) + '</tr></table>')
ws3_p1.append(h2("Write the formulas for the following compounds", "写出下列化合物的化学式"))
ws3_p1.append('<table><tr>' + "".join(f'<td>{li(en + BL(80), cn)}</td>' for en, cn in [
    ("Silver (I) chloride", "氯化银(I)"), ("Calcium carbonate", "碳酸钙"),
    ("Chromium (III) oxide", "氧化铬(III)"), ("Strontium sulphate", "硫酸锶"),
]) + '</tr></table>')
ws3_p1.append(h2("Predict the products of the following", "预测下列反应的产物"))
for en, cn in [("Barium hydroxide + Hydrochloric acid →", "氢氧化钡 + 盐酸"),
               ("C<sub>2</sub>H<sub>6</sub> + O<sub>2</sub> →", "乙烷 + 氧气"),
               ("Magnesium hydroxide + Zinc →", "氢氧化镁 + 锌")]:
    ws3_p1.append(li(en, cn, gap=8))
ws3_p1.append(h2("Balance the following word equations", "配平下列文字方程式"))
for en, cn in [
    ("Barium carbonate + Magnesium → Barium + Magnesium carbonate", "碳酸钡 + 镁 → 钡 + 碳酸镁"),
    ("Potassium chlorate → Potassium chloride + oxygen gas", "氯酸钾 → 氯化钾 + 氧气"),
    ("Aluminum + phosphoric acid (H<sub>3</sub>PO<sub>4</sub>) → aluminum phosphate + hydrogen gas",
     "铝 + 磷酸 → 磷酸铝 + 氢气"),
]:
    ws3_p1.append(li(en, cn, gap=8))

# --------------------------------------------------------------------------- #
WORK = [
    ("SCI 10 REV WORKSHEET 0 _merge.pdf", [ws0_p1, ws0_p2], [3, 4]),
    ("SCI 10 REV WORKSHEET 1 _merge.pdf", [ws1_p1, ws1_p2], [3, 4]),
    ("SCI 10 REV WORKSHEET 2 _merge.pdf", [ws2_p1, ws2_p2], [3, 4]),
    ("SCI 10 REV WORKSHEET 3 _merge.pdf", [ws3_p1], [2]),
]


def build_html(pages, title):
    body = "".join(f'<div class="page">{"".join(p)}</div>' for p in pages)
    return ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            f"<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>")


def main():
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    chrome = find_chrome()
    print("renderer:", os.path.basename(chrome))
    for src_name, pages, ans_pages in WORK:
        stem = os.path.splitext(src_name)[0].replace(" ", "_")
        html_path = os.path.join(BUILD, stem + ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_html(pages, stem))

        mid_pdf = os.path.join(BUILD, stem + ".pdf")
        render(chrome, html_path, mid_pdf)

        out_path = os.path.join(OUT, os.path.splitext(src_name)[0] + "_EN-CN.pdf")
        src_doc = pymupdf.open(os.path.join(REV, src_name))
        out = pymupdf.open()
        out.insert_pdf(pymupdf.open(mid_pdf))
        for p in ans_pages:
            out.insert_pdf(src_doc, from_page=p - 1, to_page=p - 1)
        out.set_metadata({"title": os.path.basename(out_path),
                          "author": "bilingual study sheet"})
        out.save(out_path, garbage=3, deflate=True)
        out.close(), src_doc.close()
        print(f"OK  {os.path.basename(out_path):<48} "
              f"{os.path.getsize(out_path)/1024:7.1f} KB")


if __name__ == "__main__":
    main()
