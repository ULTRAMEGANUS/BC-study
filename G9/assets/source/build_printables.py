# -*- coding: utf-8 -*-
"""生成 A4 可打印空白练习单（HTML → PDF）。

数据源与附录同源：
  - elements_1_20.csv  （前 20 号元素，与附录 D / figures 同源）
  - glossary.csv       （234 条术语，与附录 A 同源）

输出 html/ 与 pdf/ 两个目录；PDF 由外部 Chrome headless 渲染（见 README）。
"""
import csv
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
G9 = os.path.dirname(os.path.dirname(HERE))

SUB = "₂₃₄₅₆₇₈₉"
SUP = {"+": "⁺", "-": "⁻"}


def esc(s):
    return html.escape(str(s), quote=False)


def sub(n):
    return "".join(SUB[int(c) - 2] for c in str(n))


def charge(n):
    """1 -> ⁺ ; 2 -> ²⁺ ; -1 -> ⁻ ; -2 -> ²⁻"""
    sign = "⁺" if n > 0 else "⁻"
    m = abs(n)
    return ("" if m == 1 else SUP_MAP[m]) + sign


SUP_MAP = {1: "", 2: "²", 3: "³", 4: "⁴"}


def formula_ion(sym, n):
    return sym + charge(n)


# ------------------------------------------------------------------ 数据读取
def read_csv(name):
    p = os.path.join(HERE, name)
    with open(p, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


ELEMENTS = read_csv("elements_1_20.csv")
GLOSSARY = read_csv("glossary.csv")

# 前 20 号之外的常见元素（讲义附录 B 中出现过）
EXTRA_ELEMENTS = [
    {"symbol": "Fe", "English": "iron", "中文": "铁", "拼音": "tiě"},
    {"symbol": "Cu", "English": "copper", "中文": "铜", "拼音": "tóng"},
    {"symbol": "Zn", "English": "zinc", "中文": "锌", "拼音": "xīn"},
    {"symbol": "Br", "English": "bromine", "中文": "溴", "拼音": "xiù"},
    {"symbol": "Ag", "English": "silver", "中文": "银", "拼音": "yín"},
    {"symbol": "Sn", "English": "tin", "中文": "锡", "拼音": "xī"},
    {"symbol": "I", "English": "iodine", "中文": "碘", "拼音": "diǎn"},
    {"symbol": "Au", "English": "gold", "中文": "金", "拼音": "jīn"},
    {"symbol": "Hg", "English": "mercury", "中文": "汞", "拼音": "gǒng"},
    {"symbol": "Pb", "English": "lead", "中文": "铅", "拼音": "qiān"},
]

FAMILY_CN = {"1": "碱金属", "2": "碱土金属", "13": "硼族", "14": "碳族",
             "15": "氮族", "16": "氧族", "17": "卤素", "18": "稀有气体"}

GROUPS = [1, 2, 13, 14, 15, 16, 17, 18]


def el_by_z(z):
    for e in ELEMENTS:
        if int(e["atomic_number"]) == z:
            return e
    return None


# ------------------------------------------------------------------ CSS
CSS = """
@page { size: A4; margin: 14mm 12mm 13mm; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI","Microsoft YaHei","PingFang SC",Arial,sans-serif;
       font-size: 10.4pt; line-height: 1.45; color: #1a202c; margin: 0; }
.zh-h { display:block; font-size:.72em; font-weight:500; color:#5a6675; }
.zh   { display:block; color:#4a5568; font-size:.9em; }

.hd { border-bottom:2.2pt solid #185FA5; padding-bottom:5px; margin-bottom:9px;
      display:flex; justify-content:space-between; align-items:flex-end; gap:10px; }
.hd .l { flex:1; }
.hd .code { display:inline-block; background:#185FA5; color:#fff; font-size:8.2pt;
            font-weight:700; padding:1px 6px; border-radius:3px; margin-bottom:2px; }
.hd h1 { font-size:14.5pt; margin:0 0 1px; line-height:1.2; }
.hd .sub { font-size:8.4pt; color:#5a6675; }
.hd .field { font-size:8.4pt; color:#3d4753; white-space:nowrap; }

h2.sec { font-size:11pt; margin:11px 0 5px; padding-left:6px;
         border-left:3.5pt solid #185FA5; }
h2.sec .zh-h { display:inline; font-size:.78em; margin-left:6px; }
.tip { font-size:8.3pt; color:#6b7280; margin:3px 0 7px; }

table { border-collapse:collapse; width:100%; font-size:9.3pt; }
th,td { border:0.8pt solid #9aa7b5; padding:3.5pt 5pt; vertical-align:middle; }
th { background:#eef2f7; font-weight:600; font-size:8.7pt; }
td.c, th.c { text-align:center; }
tr { page-break-inside:avoid; }
td.fill { height:7.2mm; }
td.fill.tall { height:11mm; }
.given { color:#185FA5; font-weight:600; }

table.pt td { height:13mm; text-align:center; position:relative; }
table.pt .z { position:absolute; top:1.5pt; left:3pt; font-size:7.2pt; color:#9aa7b5; }
table.pt .big { font-size:13pt; font-weight:700; }
table.pt .cn { font-size:9pt; }
table.pt .en { font-size:7.4pt; color:#5a6675; }
table.pt th { font-size:8pt; }

.grid3 { width:100%; border-collapse:collapse; }
.grid3 td { border:0.8pt solid #c3cfdd; padding:4pt; text-align:center; width:33.3%; }
.grid4 td { width:25%; }
.mini { font-size:7.8pt; color:#4a5568; }

.ans { page-break-before:always; }
.ans h2 { font-size:12.5pt; color:#A32D2D; margin:0 0 3px;
          border-bottom:1.6pt solid #A32D2D; padding-bottom:4px; }
.ans table { font-size:8.8pt; }
.ans td { background:#fbfcfd; }
.foot { margin-top:8px; font-size:7.6pt; color:#9aa7b5; border-top:0.6pt solid #dde3ea; padding-top:4px; }

.cat-metal { background:#E6F1FB; }
.cat-nonmetal { background:#FAEEDA; }
.cat-noble { background:#EEEDFE; }
.cat-metalloid { background:#EAF3DE; }
"""


def wrap(code, title_en, title_cn, sub, body, foot=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{esc(code)} {esc(title_en)} {esc(title_cn)}</title>
<style>{CSS}</style></head><body>
<div class="hd">
  <div class="l">
    <span class="code">{esc(code)}</span>
    <h1>{esc(title_en)}<span class="zh-h">{esc(title_cn)}</span></h1>
    <div class="sub">{esc(sub)}</div>
  </div>
  <div class="field">Name 姓名 __________　Date 日期 __________　Score 得分 ______</div>
</div>
{body}
<div class="foot">BC Science 9 · Chemistry Unit ｜ {esc(code)} {esc(title_cn)}　{esc(foot)}</div>
</body></html>
"""


def ans_block(inner):
    return f"""<div class="ans">
<h2>答案｜Answer Key</h2>
<p class="tip">建议整份做完后对照；教师/家长可打印后裁下本页单独保存。</p>
{inner}
</div>"""


def t(rows, header=None, cls="", center_cols=()):
    out = [f'<table class="{cls}">']
    if header:
        out.append("<thead><tr>" + "".join(
            f'<th class="c">{esc(h)}</th>' if i in center_cols else f"<th>{esc(h)}</th>"
            for i, h in enumerate(header)) + "</tr></thead>")
    out.append("<tbody>")
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            # 空单元格 = 待填写，给足书写高度
            extra = "fill" if c == "" else ""
            if i in center_cols:
                extra = (extra + " c").strip()
            cells.append(f'<td class="{extra}">{c}</td>' if extra else f"<td>{c}</td>")
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


# ------------------------------------------------------------------ SVG 零件
def bohr_blank():
    """空白玻尔图框架：3 层同心圆 + 中心核。"""
    return """<svg viewBox="0 0 118 118" width="112" height="112">
  <circle cx="59" cy="59" r="53" fill="none" stroke="#c3cfdd" stroke-width="0.9" stroke-dasharray="3 3"/>
  <circle cx="59" cy="59" r="41" fill="none" stroke="#c3cfdd" stroke-width="0.9" stroke-dasharray="3 3"/>
  <circle cx="59" cy="59" r="29" fill="none" stroke="#c3cfdd" stroke-width="0.9" stroke-dasharray="3 3"/>
  <circle cx="59" cy="59" r="13" fill="#ffffff" stroke="#9aa7b5" stroke-width="0.9"/>
  <text x="59" y="56" font-size="6.4" text-anchor="middle" fill="#9aa7b5" font-family="Segoe UI">__p⁺</text>
  <text x="59" y="66" font-size="6.4" text-anchor="middle" fill="#9aa7b5" font-family="Segoe UI">__n⁰</text>
  <text x="59" y="7"  font-size="6" text-anchor="middle" fill="#b8c2ce" font-family="Segoe UI">M 8</text>
  <text x="59" y="19" font-size="6" text-anchor="middle" fill="#b8c2ce" font-family="Segoe UI">L 8</text>
  <text x="59" y="31" font-size="6" text-anchor="middle" fill="#b8c2ce" font-family="Segoe UI">K 2</text>
</svg>"""


def lewis_blank(sym, slots=8):
    """路易斯点式练习位：符号居中，四周 slots 个空心圆待涂。"""
    pos = [(59, 16), (59, 26), (88, 50), (80, 59), (59, 92), (59, 82), (30, 50), (38, 59)]
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="3.1" fill="none" stroke="#b8c2ce" stroke-width="0.8"/>'
        for x, y in pos[:slots])
    return f"""<svg viewBox="0 0 118 108" width="104" height="95">
  {dots}
  <text x="59" y="64" font-size="20" font-weight="700" text-anchor="middle"
        fill="#185FA5" font-family="Segoe UI">{esc(sym)}</text>
</svg>"""


def lewis_ion_blank(sym):
    """离子点式练习位：方括号 + 8 个空心圆 + 右上电荷空。"""
    pos = [(30, 20), (30, 32), (44, 44), (56, 44), (30, 80), (30, 68), (16, 44), (4, 44)]
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="3" fill="none" stroke="#b8c2ce" stroke-width="0.8"/>'
        for x, y in pos)
    return f"""<svg viewBox="0 0 96 104" width="88" height="95">
  {dots}
  <text x="30" y="57" font-size="17" font-weight="700" text-anchor="middle"
        fill="#185FA5" font-family="Segoe UI">{esc(sym)}</text>
  <path d="M46 8 L40 8 L40 96 L46 96" fill="none" stroke="#5a6675" stroke-width="1.1"/>
  <path d="M50 8 L56 8 L56 96 L50 96" fill="none" stroke="#5a6675" stroke-width="1.1"/>
  <text x="62" y="26" font-size="13" fill="#A32D2D" font-family="Segoe UI">____</text>
</svg>"""


def cell_bohr(sym_cn):
    return (f'<div style="text-align:center">{bohr_blank()}'
            f'<div class="mini">元素 <b>{esc(sym_cn)}</b></div>'
            f'<div class="mini">排布 ______　价电子 ______</div></div>')


def cell_lewis(sym):
    return (f'<div style="text-align:center">{lewis_blank(sym)}'
            f'<div class="mini">价电子 ______</div></div>')


def cell_ion(sym):
    return (f'<div style="text-align:center">{lewis_ion_blank(sym)}'
            f'<div class="mini">离子符号 ______</div></div>')


def grid(items, per_row=3):
    rows = [items[i:i + per_row] for i in range(0, len(items), per_row)]
    out = ['<table class="grid3%s">' % ("" if per_row == 3 else " grid4")]
    for r in rows:
        cells = "".join(f"<td>{c}</td>" for c in r)
        while len(r) < per_row:
            cells += "<td></td>"
        out.append(f"<tr>{cells}</tr>")
    out.append("</table>")
    return "\n".join(out)


# ================================================================== P01
def p01():
    body = []
    body.append('<h2 class="sec">A　按原子序数填表<span class="zh-h">给序数，填符号与中英名称</span></h2>')
    body.append('<p class="tip">方格左上角小字为原子序数 atomic number。请填：元素符号 symbol、中文名、英文名。</p>')
    body.append(periodic_table(blank=True))
    body.append('<h2 class="sec">B　按元素符号填表<span class="zh-h">给符号，填序数、中文名、英文名</span></h2>')
    body.append(periodic_table(blank=True, show="symbol"))

    a = []
    a.append('<h2 class="sec">周期表完整答案<span class="zh-h">底色 = 元素类别</span></h2>')
    a.append(periodic_table(blank=False))
    body.append(ans_block("\n".join(a)))
    return body


def periodic_table(blank=True, show="z"):
    out = ['<table class="pt">']
    out.append("<thead><tr><th>周期<br>Period</th>" + "".join(
        f'<th>{g}<br><span style="font-weight:400;font-size:6.8pt">{FAMILY_CN[str(g)]}</span></th>'
        for g in GROUPS) + "</tr></thead><tbody>")
    for p in range(1, 5):
        out.append(f'<tr><th>{p}</th>')
        for g in GROUPS:
            e = next((x for x in ELEMENTS
                      if int(x["period"]) == p and int(x["group"]) == g), None)
            if not e:
                out.append('<td style="background:#f4f6f8"></td>')
                continue
            z, sym = e["atomic_number"], e["symbol"]
            if blank:
                if show == "z":
                    inner = f'<span class="z">{z}</span>'
                else:
                    inner = f'<span class="z">{z}</span><div class="big">{esc(sym)}</div>'
                out.append(f"<td>{inner}</td>")
            else:
                out.append(
                    f'<td class="cat-{e["category"]}"><span class="z">{z}</span>'
                    f'<div class="big">{esc(sym)}</div>'
                    f'<div class="cn">{esc(e["中文"])}</div>'
                    f'<div class="en">{esc(e["English"])}</div></td>')
        out.append("</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


# ================================================================== P02
def p02():
    rows = []
    order = list(ELEMENTS) + EXTRA_ELEMENTS
    for e in order:
        rows.append([
            f'<span class="given">{esc(e["中文"])}</span>',
            f'<span class="mini">{esc(e["拼音"])}</span>',
            "", "",
        ])
    body = ['<h2 class="sec">元素符号与英文名默写<span class="zh-h">给中文名与拼音，写符号与英文</span></h2>',
            '<p class="tip">共 30 个。符号书写规则：1–2 个字母，首字母大写、第二个字母小写（如 Na、Cl、Mg）。</p>',
            t(rows, ["中文 Chinese", "拼音 pinyin", "符号 Symbol", "英文 English"], center_cols=(1, 2, 3))]

    ar = [[f'<span class="given">{esc(e["中文"])}</span>', f'<b>{esc(e["symbol"])}</b>',
           esc(e["English"])] for e in order]
    body.append(ans_block(t(ar, ["中文", "符号", "英文"], center_cols=(1,))))
    return body


# ================================================================== P03
def p03():
    picks = ["Li", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "S",
             "Cl", "Ar", "Ca"]
    body = ['<h2 class="sec">画出玻尔模型图<span class="zh-h">Bohr diagram</span></h2>',
            '<p class="tip">在同心圆上点电子，并在中心圆内填质子数与中子数。'
            '前 20 号元素按 <b>2, 8, 8</b> 依次填充（第 3 层按 8 处理）。</p>',
            grid([cell_bohr(s) for s in picks], 3)]
    ar = []
    for s in picks:
        e = next(x for x in ELEMENTS if x["symbol"] == s)
        ar.append([f'<b>{s}</b>', esc(e["中文"]), e["atomic_number"],
                   e["neutrons"], esc(e["electron_arrangement"]),
                   e["valence_electrons"]])
    body.append(ans_block(
        '<p class="tip">答案格式：元素 / 质子数 / 中子数 / 电子排布 / 价电子数</p>' +
        t(ar, ["符号", "中文", "质子 p⁺", "中子 n⁰", "电子排布", "价电子"], center_cols=(0, 2, 3, 4, 5))))
    return body


# ================================================================== P04
ION_DRILL = [
    ("Na", 1, 1, 1, "钠离子"), ("Mg", 2, 2, 2, "镁离子"), ("Al", 13, 3, 3, "铝离子"),
    ("K", 1, 1, 1, "钾离子"), ("Ca", 2, 2, 2, "钙离子"), ("Li", 1, 1, 1, "锂离子"),
    ("O", 16, 6, -2, "氧离子"), ("F", 17, 7, -1, "氟离子"), ("Cl", 17, 7, -1, "氯离子"),
    ("S", 16, 6, -2, "硫离子"), ("N", 15, 5, -3, "氮离子"), ("Br", 17, 7, -1, "溴离子"),
]
Z_OF = {"Na": 11, "Mg": 12, "Al": 13, "K": 19, "Ca": 20, "Li": 3,
        "O": 8, "F": 9, "Cl": 17, "S": 16, "N": 7, "Br": 35}
CN_OF = {"Na": "钠", "Mg": "镁", "Al": "铝", "K": "钾", "Ca": "钙", "Li": "锂",
         "O": "氧", "F": "氟", "Cl": "氯", "S": "硫", "N": "氮", "Br": "溴"}


def p04():
    rows = []
    for sym, g, v, ch, _ in ION_DRILL:
        rows.append([f'<b>{sym}</b> {CN_OF[sym]}', str(g), str(v), "", "", "", ""])
    body = ['<h2 class="sec">由族号推离子<span class="zh-h">Predicting ions from the group number</span></h2>',
            '<p class="tip">金属失电子 → 阳离子 cation（正）；非金属得电子 → 阴离子 anion（负）。'
            '目标都是达到 <b>8 个价电子</b>（八隅体规则 octet rule）。</p>',
            t(rows, ["元素 Element", "族 Group", "价电子", "失/得电子数", "离子符号",
                     "离子名称（中）", "电子总数"], center_cols=(1, 2, 3, 4, 5, 6))]

    body.append('<h2 class="sec">多变价与多原子离子<span class="zh-h">Multivalent &amp; polyatomic</span></h2>')
    body.append(t([["Fe²⁺", "", "亚铁离子"], ["Fe³⁺", "", "铁离子"],
                   ["Cu⁺", "", "亚铜离子"], ["Cu²⁺", "", "铜离子"],
                   ["NH₄⁺", "", "铵根离子"], ["OH⁻", "", "氢氧根离子"],
                   ["NO₃⁻", "", "硝酸根离子"], ["CO₃²⁻", "", "碳酸根离子"],
                   ["SO₄²⁻", "", "硫酸根离子"], ["PO₄³⁻", "", "磷酸根离子"]],
                  ["离子符号", "名称（English）", "名称（中文）"], center_cols=(0,)))

    ar = []
    for sym, g, v, ch, _ in ION_DRILL:
        z = Z_OF[sym]
        gain = "失去 %d" % abs(ch) if ch > 0 else "得到 %d" % abs(ch)
        e_total = z - ch
        name_en = {"Na": "sodium", "Mg": "magnesium", "Al": "aluminium", "K": "potassium",
                   "Ca": "calcium", "Li": "lithium", "O": "oxide", "F": "fluoride",
                   "Cl": "chloride", "S": "sulfide", "N": "nitride", "Br": "bromide"}[sym]
        ar.append([f'<b>{sym}</b>', gain + f" {abs(ch)} e⁻",
                   f'<b>{formula_ion(sym, ch)}</b>', name_en + " ion",
                   CN_OF[sym] + "离子", str(e_total)])
    body.append(ans_block(t(ar, ["元素", "得失电子", "离子符号", "English", "中文", "电子总数"],
                            center_cols=(0, 1, 2, 5))))
    return body


# ================================================================== P05
def p05():
    atoms = ["H", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "S",
             "Cl", "Ar", "Ca"]
    ions = ["Na", "Mg", "Al", "Cl", "O", "N"]
    body = ['<h2 class="sec">A　原子路易斯点式<span class="zh-h">Lewis dot diagrams for atoms</span></h2>',
            '<p class="tip">把价电子画成小圆点：上、右、下、左顺时针放置，每个方向最多 2 个。'
            '价电子数 = 主族族号个位数（He 例外，为 2）。</p>',
            grid([cell_lewis(s) for s in atoms], 3)]
    body.append('<h2 class="sec">B　离子路易斯点式<span class="zh-h">Lewis dot diagrams for ions</span></h2>')
    body.append('<p class="tip">阴离子：方括号内画 <b>8 个点</b>，右上角标电荷；'
                '阳离子：<b>不画点</b>，只标右上角电荷。</p>')
    body.append(grid([cell_ion(s) for s in ions], 3))

    ar = []
    for s in atoms:
        e = next((x for x in ELEMENTS if x["symbol"] == s), None)
        v = e["valence_electrons"] if e else {"H": "1"}.get(s, "")
        ar.append([f'<b>{s}</b>', v])
    ion_ar = [[f'<b>{s}</b>',
               {"Na": "Na⁺ 0 点", "Mg": "Mg²⁺ 0 点", "Al": "Al³⁺ 0 点",
                "Cl": "[Cl]⁻ 8 点", "O": "[O]²⁻ 8 点", "N": "[N]³⁻ 8 点"}[s]]
              for s in ions]
    body.append(ans_block(
        '<h2 class="sec" style="font-size:10pt">A　价电子数</h2>' +
        t([ar[i:i + 5] and [c for row in ar[i:i + 5] for c in row] for i in range(0, len(ar), 5)],
          ["符号", "价电子", "符号", "价电子", "符号", "价电子", "符号", "价电子", "符号", "价电子"],
          center_cols=tuple(range(10))) +
        '<h2 class="sec" style="font-size:10pt">B　离子点式</h2>' +
        t(ion_ar, ["元素", "离子点式写法"], center_cols=(0, 1))))
    return body


# ================================================================== P06
IONIC_A = ["NaCl", "MgCl₂", "Al₂O₃", "K₂S", "CaO", "FeCl₂", "FeCl₃",
           "Cu₂O", "NaOH", "CaCO₃", "(NH₄)₂SO₄", "AgNO₃", "ZnS", "Mg(OH)₂"]
IONIC_B = ["potassium bromide", "iron(III) oxide", "copper(II) sulfate",
           "ammonium chloride", "aluminium nitrate", "sodium carbonate"]
# ⚠ A / B / C 三组必须使用完全不重叠的化合物：任何交叉都会让上一组的答案
# 出现在下一组的题干里，练习单就白出了。改动这三组时务必重新核对交集。
IONIC_C = ["氧化镁", "硫化铝", "氢氧化钙", "硝酸钾", "氧化铜", "氯化锌",
           "硫酸镁", "溴化银", "碳酸钾", "硝酸铵"]


def p06():
    def rowf(f):
        return [f'<span class="given">{esc(f)}</span>', "", ""]

    body = ['<h2 class="sec">A　给化学式，写中英名称<span class="zh-h">Formula → name</span></h2>',
            '<p class="tip">英文：金属名 + 非金属词根 -ide（多变价金属加罗马数字）；'
            '中文：<b>非金属在前 + 化 + 金属在后</b>。</p>',
            t([rowf(f) for f in IONIC_A],
              ["化学式 Formula", "英文 English name", "中文 Chinese name"], center_cols=(0,))]
    body.append('<h2 class="sec">B　给英文名，写化学式与中文<span class="zh-h">English name → formula</span></h2>')
    body.append(t([[f'<span class="given">{esc(n)}</span>', "", ""] for n in IONIC_B],
                  ["英文 English name", "化学式 Formula", "中文 Chinese name"], center_cols=(1,)))
    body.append('<h2 class="sec">C　给中文名，写化学式与英文<span class="zh-h">最容易写反顺序的一组</span></h2>')
    body.append('<p class="tip">⚠ 中文顺序与英文相反：氯化钠 → sodium <b>chloride</b>（正离子在后）。'
                '写成「钠化氯」是错的。</p>')
    body.append(t([[f'<span class="given">{esc(n)}</span>', "", ""] for n in IONIC_C],
                  ["中文 Chinese name", "化学式 Formula", "英文 English name"], center_cols=(1,)))

    ans_a = [
        ("NaCl", "sodium chloride", "氯化钠"), ("MgCl₂", "magnesium chloride", "氯化镁"),
        ("Al₂O₃", "aluminium oxide", "氧化铝"), ("K₂S", "potassium sulfide", "硫化钾"),
        ("CaO", "calcium oxide", "氧化钙"), ("FeCl₂", "iron(II) chloride", "氯化亚铁"),
        ("FeCl₃", "iron(III) chloride", "氯化铁"), ("Cu₂O", "copper(I) oxide", "氧化亚铜"),
        ("NaOH", "sodium hydroxide", "氢氧化钠"), ("CaCO₃", "calcium carbonate", "碳酸钙"),
        ("(NH₄)₂SO₄", "ammonium sulfate", "硫酸铵"), ("AgNO₃", "silver nitrate", "硝酸银"),
        ("ZnS", "zinc sulfide", "硫化锌"), ("Mg(OH)₂", "magnesium hydroxide", "氢氧化镁"),
    ]
    ans_b = [("potassium bromide", "KBr", "溴化钾"), ("iron(III) oxide", "Fe₂O₃", "氧化铁"),
             ("copper(II) sulfate", "CuSO₄", "硫酸铜"), ("ammonium chloride", "NH₄Cl", "氯化铵"),
             ("aluminium nitrate", "Al(NO₃)₃", "硝酸铝"), ("sodium carbonate", "Na₂CO₃", "碳酸钠")]
    ans_c = [("氧化镁", "MgO", "magnesium oxide"), ("硫化铝", "Al₂S₃", "aluminium sulfide"),
             ("氢氧化钙", "Ca(OH)₂", "calcium hydroxide"),
             ("硝酸钾", "KNO₃", "potassium nitrate"),
             ("氧化铜", "CuO", "copper(II) oxide"), ("氯化锌", "ZnCl₂", "zinc chloride"),
             ("硫酸镁", "MgSO₄", "magnesium sulfate"), ("溴化银", "AgBr", "silver bromide"),
             ("碳酸钾", "K₂CO₃", "potassium carbonate"),
             ("硝酸铵", "NH₄NO₃", "ammonium nitrate")]
    # 自检：三组答案必须互不相交，否则上一组的答案会印在下一组题干里
    fa = {a for a, _, _ in ans_a}
    fb = {b for _, b, _ in ans_b}
    fc = {c for _, c, _ in ans_c}
    for x, y, tag in ((fa, fb, "A/B"), (fa, fc, "A/C"), (fb, fc, "B/C")):
        inter = x & y
        if inter:
            raise SystemExit("P06 %s 组答案交叉，练习单会泄露答案：%s" % (tag, inter))
    inner = "".join(
        '<h2 class="sec" style="font-size:10pt">%s</h2>' % h +
        t([[f'<b>{esc(a)}</b>', esc(b), esc(c)] for a, b, c in rows],
          ["化学式", "English", "中文"], center_cols=(0,))
        for h, rows in [("A", ans_a), ("B", ans_b), ("C", ans_c)])
    body.append(ans_block(inner))
    return body


# ================================================================== P07
def p07():
    pre = [(1, "mono-"), (2, "di-"), (3, "tri-"), (4, "tetra-"), (5, "penta-"),
           (6, "hexa-"), (7, "hepta-"), (8, "octa-"), (9, "nona-"), (10, "deca-")]
    body = ['<h2 class="sec">A　希腊数字前缀<span class="zh-h">Greek prefixes</span></h2>',
            t([[f'<span class="given">{n}</span>', "", f'<span class="given">{esc(cn)}</span>']
               for n, cn in [(1, "一"), (2, "二"), (3, "三"), (4, "四"), (5, "五"),
                             (6, "六"), (7, "七"), (8, "八"), (9, "九"), (10, "十")]],
              ["数字", "英文前缀 prefix", "中文"], center_cols=(0, 1, 2))]
    body.append('<p class="tip">三条硬规则：① 第一个元素仅当数目 &gt; 1 时才加前缀；'
                '② 第一个元素<b>永不用 mono-</b>；③ 第二个元素必加前缀，词尾改为 -ide。</p>')
    body.append('<h2 class="sec">B　给化学式，写中英名称<span class="zh-h">Formula → name</span></h2>')
    body.append(t([[f'<span class="given">{esc(f)}</span>', "", ""] for f in
                   ["CO₂", "CO", "N₂O₄", "PCl₃", "SF₆", "CCl₄", "N₂O₅", "SO₂", "P₂O₃", "Cl₂O₇"]],
                  ["化学式", "英文 English name", "中文 Chinese name"], center_cols=(0,)))
    body.append('<h2 class="sec">C　俗名记忆<span class="zh-h">Common names</span></h2>')
    body.append(t([[f'<span class="given">{esc(f)}</span>', "", ""] for f in
                   ["H₂O", "NH₃", "CH₄", "O₃", "H₂O₂"]],
                  ["化学式", "英文俗名 common name", "中文"], center_cols=(0,)))

    inner = ('<h2 class="sec" style="font-size:10pt">A　前缀</h2>' +
             t([[str(n), f'<b>{esc(p)}</b>', esc(cn)] for (n, p), cn in
                zip(pre, ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"])],
               ["数字", "prefix", "中文"], center_cols=(0, 1, 2)) +
             '<h2 class="sec" style="font-size:10pt">B　命名</h2>' +
             t([["CO₂", "carbon dioxide", "二氧化碳"], ["CO", "carbon monoxide", "一氧化碳"],
                ["N₂O₄", "dinitrogen tetroxide", "四氧化二氮"],
                ["PCl₃", "phosphorus trichloride", "三氯化磷"],
                ["SF₆", "sulfur hexafluoride", "六氟化硫"],
                ["CCl₄", "carbon tetrachloride", "四氯化碳"],
                ["N₂O₅", "dinitrogen pentoxide", "五氧化二氮"],
                ["SO₂", "sulfur dioxide", "二氧化硫"],
                ["P₂O₃", "diphosphorus trioxide", "三氧化二磷"],
                ["Cl₂O₇", "dichlorine heptoxide", "七氧化二氯"]],
               ["化学式", "English", "中文"], center_cols=(0,)) +
             '<h2 class="sec" style="font-size:10pt">C　俗名</h2>' +
             t([["H₂O", "water", "水"], ["NH₃", "ammonia", "氨"],
                ["CH₄", "methane", "甲烷"], ["O₃", "ozone", "臭氧"],
                ["H₂O₂", "hydrogen peroxide", "过氧化氢"]],
               ["化学式", "English", "中文"], center_cols=(0,)))
    body.append(ans_block(inner))
    return body


# ================================================================== P08
P08_ITEMS = ["NaCl", "H₂O", "CO₂", "MgO", "CH₄", "CaCO₃", "SO₂", "KBr",
             "NH₃", "Fe₂O₃", "CCl₄", "NaOH"]


def p08():
    body = ['<h2 class="sec">先判断类型，再命名<span class="zh-h">Ionic or molecular?</span></h2>',
            '<p class="tip">金属 + 非金属 → 离子化合物 ionic；非金属 + 非金属 → 分子（共价）化合物 molecular。'
            '再预测：熔点高低、水溶液能否导电。</p>',
            t([[f'<span class="given">{esc(f)}</span>', "", "", "", "", ""]
               for f in P08_ITEMS],
              ["化学式", "类型 ionic / molecular", "英文 English name", "中文 Chinese name",
               "熔点高/低", "水溶液导电？"], center_cols=(0, 1, 4, 5))]

    ans = [("NaCl", "ionic", "sodium chloride", "氯化钠", "高", "导电"),
           ("H₂O", "molecular", "water", "水", "低", "不导电"),
           ("CO₂", "molecular", "carbon dioxide", "二氧化碳", "低", "不导电"),
           ("MgO", "ionic", "magnesium oxide", "氧化镁", "高", "导电（熔融/溶液）"),
           ("CH₄", "molecular", "methane", "甲烷", "低", "不导电"),
           ("CaCO₃", "ionic", "calcium carbonate", "碳酸钙", "高", "难溶，几乎不导电"),
           ("SO₂", "molecular", "sulfur dioxide", "二氧化硫", "低", "不导电"),
           ("KBr", "ionic", "potassium bromide", "溴化钾", "高", "导电"),
           ("NH₃", "molecular", "ammonia", "氨", "低", "不导电"),
           ("Fe₂O₃", "ionic", "iron(III) oxide", "氧化铁", "高", "不溶，不导电"),
           ("CCl₄", "molecular", "carbon tetrachloride", "四氯化碳", "低", "不导电"),
           ("NaOH", "ionic", "sodium hydroxide", "氢氧化钠", "高", "导电")]
    body.append(ans_block(t([[f'<b>{esc(a)}</b>', esc(b), esc(c), esc(d), esc(e), esc(f)]
                             for a, b, c, d, e, f in ans],
                            ["化学式", "类型", "English", "中文", "熔点", "导电性"],
                            center_cols=(0, 1, 4))))
    return body


# ================================================================== P09
# 每章核心词（手写，避免按字母序抽到边缘词）。中文以 glossary.csv 为准做校准，
# CSV 里没有的用这里提供的译名（已与正文 11 章体例核对）。
CORE_WORDS = [
    ("Ch.1", [("matter", "物质"), ("pure substance", "纯净物"), ("mixture", "混合物"),
              ("atom", "原子"), ("molecule", "分子"), ("element", "元素")]),
    ("Ch.2", [("element", "元素"), ("chemical symbol", "元素符号"),
              ("atomic number", "原子序数"), ("atomic mass", "原子质量"),
              ("isotope", "同位素"), ("periodic table", "元素周期表")]),
    ("Ch.3", [("group", "族"), ("period", "周期"), ("metal", "金属"),
              ("non-metal", "非金属"), ("metalloid", "类金属"),
              ("transition element", "过渡元素")]),
    ("Ch.4", [("alkali metal", "碱金属"), ("alkaline earth metal", "碱土金属"),
              ("halogen", "卤素"), ("noble gas", "稀有气体"),
              ("diatomic molecule", "双原子分子"), ("reactivity", "活性")]),
    ("Ch.5", [("nucleus", "原子核"), ("electron shell", "电子层"),
              ("valence electron", "价电子"), ("mass number", "质量数"),
              ("Bohr diagram", "玻尔模型图"), ("electron arrangement", "电子排布")]),
    ("Ch.6", [("ion", "离子"), ("cation", "阳离子"), ("anion", "阴离子"),
              ("octet rule", "八隅体规则"), ("polyatomic ion", "多原子离子"),
              ("multivalent element", "多变价元素")]),
    ("Ch.7", [("ionic compound", "离子化合物"), ("chemical formula", "化学式"),
              ("criss-cross method", "交叉法"), ("subscript", "下标"),
              ("roman numeral", "罗马数字"), ("crystal", "晶体")]),
    ("Ch.8", [("molecular compound", "分子（共价）化合物"), ("covalent bond", "共价键"),
              ("prefix", "前缀"), ("shared pair", "共用电子对"),
              ("intermolecular force", "分子间作用力"), ("common name", "俗名")]),
    ("Ch.9", [("chemical change", "化学变化"), ("word equation", "文字方程式"),
              ("coefficient", "系数"), ("law of conservation of mass", "质量守恒定律"),
              ("precipitate", "沉淀"), ("reactant", "反应物")]),
    ("Ch.10", [("independent variable", "自变量"), ("dependent variable", "因变量"),
               ("controlled variable", "控制变量"), ("fair test", "公平实验"),
               ("hypothesis", "假设"), ("qualitative data", "定性数据")]),
    ("Ch.11", [("conductivity", "导电性"), ("melting point", "熔点"),
               ("chemical property", "化学性质"), ("periodic trend", "周期性趋势"),
               ("semiconductor", "半导体"), ("alloy", "合金")]),
]


def p09():
    # 用 CSV 校准中文，保证与附录 A 完全一致
    zh_of = {}
    for row in GLOSSARY:
        zh_of[row["English"].strip().lower()] = row["中文"].strip()
    words = []
    seen = set()
    for ch, ws in CORE_WORDS:
        for en, cn in ws:
            k = en.lower()
            if k in seen:          # element 在 Ch.1/Ch.2 都出现，只保留一次
                continue
            seen.add(k)
            words.append((ch, en, zh_of.get(en.lower(), cn)))

    # ⚠ 关键：A 组（英→中）与 B 组（中→英）必须用不重叠的词，
    # 否则同一行左右两栏互为答案，练习单直接失效。
    half = (len(words) + 1) // 2
    grp_a, grp_b = words[:half], words[half:]
    assert not ({w[1] for w in grp_a} & {w[1] for w in grp_b}), "P09 A/B 组词重复"

    body = ['<h2 class="sec">A　给英文写中文<span class="zh-h">English → 中文</span></h2>',
            '<p class="tip">按章分组的核心术语。写完再做 B 组，最后对照末页答案。</p>',
            t([[f'<span class="given">{esc(en)}</span>', "", esc(ch)]
               for ch, en, _ in grp_a],
              ["English", "中文 Chinese", "章"], center_cols=(2,))]
    body.append('<h2 class="sec">B　给中文写英文<span class="zh-h">中文 → English</span></h2>')
    body.append(t([[f'<span class="given">{esc(cn)}</span>', "", esc(ch)]
                   for ch, _, cn in grp_b],
                  ["中文 Chinese", "English", "章"], center_cols=(2,)))

    ar = [[esc(ch), f'<b>{esc(en)}</b>', esc(cn)] for ch, en, cn in words]
    body.append(ans_block(t(ar, ["章", "English", "中文"], center_cols=(0,))))
    return body


# ================================================================== P10
def p10():
    body = ['<h2 class="sec">A　错题整理单<span class="zh-h">Error log</span></h2>',
            '<p class="tip">写清「错在哪一步」比抄正确答案有用。重做日期建议间隔 2–3 天。</p>',
            t([["", "", "", "", ""] for _ in range(10)],
              ["日期 Date", "题目来源 Source", "我的错误答案", "正确答案 + 原因", "重做日期 / 结果"],
              center_cols=(0, 4))]
    body.append('<h2 class="sec">B　单元自测打卡<span class="zh-h">Self-check tracker</span></h2>')
    chapters = [("Ch.1", "物质与原子论 Matter & atoms"),
                ("Ch.2", "元素与周期表 Elements & periodic table"),
                ("Ch.3", "族、周期、金属非金属 Groups, periods, metals"),
                ("Ch.4", "化学族与活性 Chemical families"),
                ("Ch.5", "玻尔模型 Bohr diagrams"),
                ("Ch.6", "离子与路易斯点式 Ions & Lewis dots"),
                ("Ch.7", "离子化合物命名 Ionic naming"),
                ("Ch.8", "分子化合物命名 Molecular naming"),
                ("Ch.9", "化学变化入门 Chemical change"),
                ("Ch.10", "探究与安全 Inquiry & safety"),
                ("Ch.11", "单元综合 Synthesis")]
    body.append(t([[f'<span class="given">{esc(a)}</span>', esc(b), "", "", "", ""]
                   for a, b in chapters],
                  ["章", "主题 Topic", "第 1 轮 日期/得分", "第 2 轮", "第 3 轮", "是否已订正 ✓"],
                  center_cols=(0, 2, 3, 4, 5)))
    body.append('<h2 class="sec">C　考前一页纸<span class="zh-h">One-page review</span></h2>')
    body.append('<p class="tip">把这一页写成你自己的话：只会抄讲义不算掌握。</p>')
    body.append('<table>' + "".join(
        f'<tr><td class="fill tall"></td></tr>' for _ in range(8)) + '</table>')
    return body


# ------------------------------------------------------------------ 主程序
SHEETS = [
    ("P01", "Blank Periodic Table", "空白周期表", "Chapter 2–4 · 前 20 号元素", p01,
     "元素数据取自 elements_1_20.csv（与附录 D 同源）"),
    ("P02", "Element Symbol Drill", "元素符号默写", "Chapter 2 · 30 个常见元素", p02,
     "符号书写：首字母大写，第二个字母小写"),
    ("P03", "Bohr Diagram Practice", "玻尔图练习", "Chapter 5 · 15 个元素", p03,
     "前 20 号元素按 2, 8, 8 填充"),
    ("P04", "Ion Formation Drill", "离子形成练习", "Chapter 6 · 族号推电荷", p04,
     "金属失电子、非金属得电子"),
    ("P05", "Lewis Dot Diagram Practice", "路易斯点式练习", "Chapter 6 · 原子与离子", p05,
     "阳离子 0 点、阴离子 8 点"),
    ("P06", "Ionic Compound Naming", "离子化合物命名", "Chapter 7 · 中英互译", p06,
     "中英命名顺序相反，最易错"),
    ("P07", "Molecular Compound Naming", "分子化合物命名", "Chapter 8 · 希腊前缀", p07,
     "第一个元素永不用 mono-"),
    ("P08", "Ionic or Molecular?", "化合物类型判断", "Chapter 7–8 · 类型 + 性质", p08,
     "金属+非金属 → ionic"),
    ("P09", "Vocabulary Drill", "词汇默写", "Chapter 1–11 · 按章分组", p09,
     "词条取自 glossary.csv（与附录 A 同源）"),
    ("P10", "Error Log & Self-check", "错题整理与自测打卡", "全册 · 通用模板", p10,
     "可反复复印使用"),
]


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(G9, "assets", "printables")
    html_dir = os.path.join(out_dir, "html")
    os.makedirs(html_dir, exist_ok=True)
    made = []
    for code, en, cn, sub, fn, foot in SHEETS:
        body = "\n".join(fn())
        doc = wrap(code, en, cn, sub, body, foot)
        safe = en.replace(" ", "_").replace("?", "").replace("&", "and").replace("/", "-")
        name = f"{code}_{safe}"
        p = os.path.join(html_dir, name + ".html")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(doc)
        made.append((code, en, cn, name))
        print("written:", p)
    # 索引页
    idx = ['<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">',
           "<title>Printables Index 练习单索引</title>",
           f"<style>{CSS}</style></head><body>",
           '<div class="hd"><div class="l"><span class="code">G9</span>',
           "<h1>Printable Worksheets 索引<span class=\"zh-h\">A4 空白练习单 · BC Science 9 化学单元</span></h1>",
           '<div class="sub">在浏览器中打开本页，Ctrl+P 逐份打印；或直接打印 pdf/ 目录下的 PDF。</div>',
           "</div></div>",
           '<table><thead><tr><th>编号</th><th>练习单 Worksheet</th><th>中文</th>'
           "<th>对应范围</th><th>HTML</th><th>PDF</th></tr></thead><tbody>"]
    for (code, en, cn, name), (_, _, _, sub, _, _) in zip(made, SHEETS):
        idx.append(f'<tr><td class="c"><b>{code}</b></td><td>{esc(en)}</td><td>{esc(cn)}</td>'
                   f'<td>{esc(sub)}</td>'
                   f'<td class="c"><a href="html/{name}.html">打开</a></td>'
                   f'<td class="c"><a href="pdf/{name}.pdf">打开</a></td></tr>')
    idx.append("</tbody></table>")
    idx.append('<p class="tip" style="margin-top:12px">PDF 由 Chrome headless 渲染生成；'
               "若缺失，见 assets/source/README.md 的「练习单」一节重跑。</p>")
    idx.append("</body></html>")
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(idx))
    print("written:", os.path.join(out_dir, "index.html"))
    print("sheets:", len(made))


if __name__ == "__main__":
    main()
