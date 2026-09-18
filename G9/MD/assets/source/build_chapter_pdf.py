# -*- coding: utf-8 -*-
"""把 G9 章节 Markdown 转成 A4 讲义版 PDF（英中对照，学生阅读/打印用）。

用法：
    build_chapter_pdf.py                 # 全部章节
    build_chapter_pdf.py Ch01            # 只做第 1 章（模糊匹配文件名）

流程：md → 解析 → A4 HTML → Chrome headless 渲染 → pymupdf 补页码 → 静态校验

设计要点（别改坏）：
1. 用 HTML+CSS 而不是 ReportLab/元素式排版——浏览器自动处理分页，不存在
   手写坐标那种"内容重叠/被静默丢弃"的问题（PPT 方案就是栽在这上面）。
2. ASCII 图用等宽字体，字号按"最长行字符数"动态收缩，保证永远不溢出页宽。
   实测 Ch01 最长 65 字符，10pt Consolas 约 357pt < 可用宽 510pt。
3. 表格用 table-layout:fixed + word-break，6 列也不溢出。
4. Chrome 的 --no-pdf-header-footer 意味着页眉页脚得自己做，这里用 pymupdf
   后处理补页码（纯数字 "3 / 27"，避免中文字体坑）。
5. Git Bash 调用必须 unset MSYS_NO_PATHCONV / MSYS2_ARG_CONV_EXCL。
"""
import os
import re
import sys
import glob
import html as htmllib
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))      # .../G9/MD/assets/source
ASSETS = os.path.dirname(HERE)                          # .../G9/MD/assets
MD = os.path.dirname(ASSETS)                            # .../G9/MD
G9 = os.path.dirname(MD)                                # .../G9
CHAPTERS = os.path.join(MD, "chapters-cn")
APPENDICES = os.path.join(MD, "appendices-cn")
OUT_DIR = os.path.join(G9, "pdf", "CN")
HTML_DIR = os.path.join(OUT_DIR, "_html")
IMG_DIR = os.path.join(OUT_DIR, "_img")

CSS = """
@page { size: A4; margin: 18mm 14mm 18mm 14mm; }
* { box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "Segoe UI", "PingFang SC", sans-serif;
  font-size: 10.5pt; line-height: 1.62; color: #24242A; margin: 0;
}
h1.cover-en { font-size: 22pt; color: #185FA5; margin: 0 0 6pt; line-height:1.3; }
h2.cover-cn { font-size: 17pt; color: #24242A; margin: 0 0 10pt; font-weight:600;
              border:0; page-break-before: avoid; }
.cover-meta { font-size: 9pt; color:#5F5E5A; border-top:1px solid #B4B2A9;
              padding-top:8pt; margin-top:14pt; }
h2 { font-size: 14pt; color: #185FA5; margin: 0 0 8pt; padding-bottom: 4pt;
     border-bottom: 2px solid #185FA5; page-break-before: auto;
     page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #185FA5; margin: 14pt 0 5pt;
     page-break-after: avoid; }
h4 { font-size: 10.5pt; color: #24242A; margin: 10pt 0 4pt;
     page-break-after: avoid; }
/* 长英文串（如逐项列举的 sodium 钠 potassium 钾 …）在中文断行规则下可能不换行
   而溢出右边距，故允许任意处断行；正常中文行文不受影响 */
p { margin: 0 0 6pt; overflow-wrap: anywhere; line-break: anywhere; }
ul, ol { margin: 0 0 8pt; padding-left: 18pt; }
li { margin-bottom: 2pt; }
/* 表格：短表(<=14行)整表不跨页并用 10pt；长表允许跨页、表头自动重复 */
table { width: 100%; border-collapse: collapse; font-size: 9.5pt;
        margin: 6pt 0 10pt; table-layout: fixed; }
table.tk { page-break-inside: avoid; font-size: 10pt; }
table.tf { page-break-inside: auto; }
thead { display: table-header-group; }
th { background: #E6F1FB; color: #185FA5; font-weight: 600; }
td, th { border: 1px solid #B4B2A9; padding: 3.5pt 5pt; word-break: break-word;
         vertical-align: top; line-height: 1.45; }
tr:nth-child(even) td { background: #FAFAF8; }
.fig { text-align: center; margin: 6pt 0 10pt; padding: 6pt 4pt;
       background: #F7F6F3; border: 1px solid #DDDCD6; border-radius: 3pt;
       page-break-inside: avoid; }
.fig img { max-width: 100%; height: auto; }
.fig svg { display: block; width: 100%; height: auto; margin: 0 auto; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt;
       background: #F1F0EC; padding: 0 2pt; }
pre code { background: none; padding: 0; }
blockquote { margin: 6pt 0; padding: 5pt 10pt; background: #F7F6F3;
             border-left: 3px solid #185FA5; color: #3A3A38; }
hr { border: 0; border-top: 1px solid #DDDCD6; margin: 12pt 0; }
.fig-cap { font-size: 8.5pt; color: #5F5E5A; margin: -4pt 0 10pt; }
/* 宽表占位：1pt 白字，肉眼不可见但仍留在文本层，供 pymupdf 定位页码。
   break-before 用 auto（不强制另起页），让前页自然排满；break-after 用 always，
   保证标记是该页最后一项。渲染后在标记所在页之后插入/替换横向页。 */
.wt-ph { page-break-before: auto; page-break-after: always;
         font-size: 1pt; color: #FFFFFF; line-height: 1; }
"""
# 每个 ## 大节默认从新页开始；但会在渲染后按"空白是否超过半页"迭代撤销（见 main）
SEC_BREAK_CSS = ".sec-%d { page-break-before: always; }"

# 横向页：A4 landscape，宽表专用（纵向可用宽 505pt → 横向约 785pt）
CSS_LAND = CSS.replace(
    "@page { size: A4; margin: 18mm 14mm 18mm 14mm; }",
    "@page { size: A4 landscape; margin: 12mm 10mm 14mm 10mm; }"
) + "\ntable { font-size: 10.5pt; }\nbody { font-size: 10.5pt; }"


def esc(s):
    return htmllib.escape(s, quote=False)


def inline(s):
    """行内 Markdown：加粗、行内代码。先转义再替换，顺序不能反。"""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def parse_md(text, md_dir=""):
    """把 Markdown 解析成块列表。返回 [(kind, payload), ...]"""
    lines = text.split("\n")
    blocks = []
    i = 0
    para = []

    def flush_para():
        if para:
            blocks.append(("p", " ".join(para).strip()))
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        # 跳过 beautify_md.py 为 md 浏览器补的图题行（"**📊 图 2-1**　…"）：
        # SVG 内部已经画了图题，PDF 里再出现一次就重复了。
        if s.startswith("**\U0001F4CA"):
            i += 1
            continue

        # 代码围栏（ASCII 图）
        if s.startswith("```"):
            flush_para()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            blocks.append(("pre", "\n".join(buf)))
            continue

        if not s:
            flush_para()
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush_para()
            blocks.append(("h%d" % len(m.group(1)), m.group(2).strip()))
            i += 1
            continue

        # 表格
        if s.startswith("|"):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            # 去掉分隔行 |---|---|
            cells = []
            for r in rows:
                cs = [c.strip() for c in r.strip("|").split("|")]
                if all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cs if c):
                    continue
                cells.append(cs)
            if cells:
                blocks.append(("table", cells))
            continue

        # 引用
        if s.startswith(">"):
            flush_para()
            blocks.append(("quote", s.lstrip("> ").strip()))
            i += 1
            continue

        # 图片 ![alt](path) —— SVG 内联、位图引用
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", s)
        if m:
            flush_para()
            alt, rel = m.group(1).strip(), m.group(2).strip()
            p = rel if os.path.isabs(rel) else os.path.join(md_dir, rel)
            blocks.append(("image", (alt, os.path.normpath(p))))
            i += 1
            continue

        # 分割线
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            flush_para()
            blocks.append(("hr", ""))
            i += 1
            continue

        # 列表
        m = re.match(r"^([-*+])\s+(.*)$", s)
        m2 = re.match(r"^(\d+)[.)]\s+(.*)$", s)
        if m or m2:
            flush_para()
            ordered = bool(m2)
            items = []
            while i < len(lines):
                t = lines[i].strip()
                mm = re.match(r"^(\d+)[.)]\s+(.*)$", t) if ordered \
                    else re.match(r"^([-*+])\s+(.*)$", t)
                if not mm:
                    break
                items.append(mm.group(2))
                i += 1
            blocks.append(("ol" if ordered else "ul", items))
            continue

        para.append(s)
        i += 1

    flush_para()
    return blocks


# ------------------------------------------------------------------ ASCII 图
# ASCII 图不能直接丢给浏览器排版：图里混用制表符(─│┌)、中文、上下标(₂₃)、
# 甚至 emoji，没有任何单一等宽字体能覆盖全部字符（实测共 800 种非 ASCII 字符，
# 覆盖率最高的微软雅黑也只有 773/800）。浏览器按字符回退到不同字体，宽度
# 不一致 → 框线图散架（实测错位约 1 个字符宽，肉眼可见）。
# 解法：按"字符网格"逐格绘制成 PNG——位置由格数决定，与字体实际宽度无关，
# 因此混用字体也不会错位。
FONT_ASCII = r"C:/Windows/Fonts/consola.ttf"
FONT_CJK = r"C:/Windows/Fonts/msyh.ttc"       # 微软雅黑，覆盖 773/800
FONT_SYM = r"C:/Windows/Fonts/seguisym.ttf"   # Segoe UI Symbol，补箭头/勾叉
FONT_EMOJI = r"C:/Windows/Fonts/seguiemj.ttf"

_CACHE = {}


def _load(path, size, index=0):
    key = ("f", path, size, index)
    if key not in _CACHE:
        try:
            from PIL import ImageFont
            _CACHE[key] = ImageFont.truetype(path, size, index=index)
        except Exception:
            _CACHE[key] = None
    return _CACHE[key]


def _cmap(path, index=0):
    key = ("c", path, index)
    if key not in _CACHE:
        try:
            from fontTools.ttLib import TTFont
            _CACHE[key] = TTFont(path, fontNumber=index).getBestCmap()
        except Exception:
            _CACHE[key] = {}
    return _CACHE[key]


def _pick(ch, size):
    """为单个字符挑字体：ASCII→Consolas，其余→雅黑，缺失→Symbol/Emoji。"""
    if ord(ch) < 128:
        return _load(FONT_ASCII, size) or _load(FONT_CJK, size)
    for p in (FONT_CJK, FONT_SYM, FONT_EMOJI):
        if ord(ch) in _cmap(p):
            f = _load(p, size)
            if f:
                return f
    return _load(FONT_CJK, size) or _load(FONT_ASCII, size)


def _cells(ch):
    """字符占几个网格（全角/宽字符占 2 格，这是 ASCII 图的通用约定）。"""
    return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


FIG_BASE_PT = 12.5     # ASCII 图基准字号（等宽），越大图越大
FIG_MAX_W_PT = 495     # 图最宽不超过版心（A4 可用宽约 505pt，含 .fig 内边距）
FIG_MAX_H_PT = 680     # 图最高不超过正文区：A4 可用高约 740pt，再减去标题与 .fig 内外边距
FIG_SCALE = 4          # 超采样倍数，越大越清晰

_PNG_CACHE = {}


FIG_TITLE_RE = re.compile(r"(>)\s*(图|表|活动)\s*(\d+[-–]\d+)\s*([^<]*?)｜([^<]*?)(<)")
FIG_NUM_EN = {"图": "Fig.", "表": "Table", "活动": "Activity"}

EN_MODE = False      # 英文版（G9/MD/chapters-en）模式：正给 SVG 图题翻成「英文在前」


def _swap_fig_title(m):
    """`图 2-3　同位素…｜Isotopes` → `Fig. 2-3　Isotopes｜同位素…`

    只在英文版里做：中文版的 G9-combo.pdf 要保持中文在前。
    两侧文字只是互换位置，总宽度几乎不变，不会撑破标题栏。
    """
    return "%s%s %s　%s｜%s%s" % (m.group(1),
                                  FIG_NUM_EN.get(m.group(2), m.group(2)),
                                  m.group(3), m.group(5), m.group(4),
                                  m.group(6))


def inline_svg(path, key):
    """把 SVG 内联进 HTML。

    内联（而不是 <img src="*.svg">）是关键：Chrome 会把 <img> 里的 SVG
    整个栅格化，中文文本层丢失；内联后仍是可搜索、可复制的真实文本，
    且保持矢量清晰。已实测：12 个汉字全部可提取，连 ₂₃ 下标都正确。

    两处必要的改写：
    1. 内部 id 加前缀 —— 同页多张 SVG 若都定义 marker id="ar"，HTML 里
       id 全局冲突，url(#ar) 会全部指向第一个定义。
    2. 去掉根元素固定宽高，改由外层容器按版心缩放。
    """
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<\?xml[^>]*\?>", "", s).strip()
    for i in re.findall(r'\sid="([^"]+)"', s):
        s = s.replace('id="%s"' % i, 'id="%s-%s"' % (i, key))
        s = s.replace("url(#%s)" % i, "url(#%s-%s)" % (i, key))
    s = re.sub(r"(<svg\b[^>]*?)\s(?:width|height)=\"[^\"]*\"", r"\1", s,
               count=2)
    if EN_MODE:
        s = FIG_TITLE_RE.sub(_swap_fig_title, s)
    return s.replace("<svg", '<svg width="100%"', 1)


def _fit_page(wpt, hpt):
    """把 ASCII 图等比缩到版心内：先限宽，再限高。

    超高的图（如附录 E 整页的实验报告模板）会被 Chrome 拆到两页上，
    一张完整的表格被切成两半；限高后整图落在一页内，代价只是字略小。
    """
    if not wpt or not hpt:
        return wpt, hpt
    k = min(1.0, FIG_MAX_W_PT / wpt, FIG_MAX_H_PT / hpt)
    return wpt * k, hpt * k


def render_ascii_png(text, out_png,
                     max_w_pt=FIG_MAX_W_PT, base_pt=FIG_BASE_PT, scale=FIG_SCALE):
    """把 ASCII 图按字符网格绘成 PNG。返回 (显示宽pt, 显示高pt)。

    关键：图像分辨率定义为「1pt = scale px」，所以 PIL 字号 = pt*scale，
    字符步进 = 0.55*pt*scale px，显示宽度 = 像素宽 / scale（**不乘 0.75**）。
    早期版本在末尾多乘了 0.75，导致图上字号只有设定值的 75%，偏小。
    """
    from PIL import Image, ImageDraw

    key = (hash(text), max_w_pt, base_pt, scale)
    if key in _PNG_CACHE and os.path.exists(_PNG_CACHE[key][2]):
        c = _PNG_CACHE[key]
        return c[0], c[1]

    lines = text.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return 0, 0

    cols = max(sum(_cells(c) for c in l) for l in lines)
    rows = len(lines)

    # 自适应字号：pad 也按字号算，故用 (0.55*cols + 0.9) 反推，保证绝不超宽
    fs_pt = min(base_pt, max_w_pt / max(0.55 * cols + 0.9, 1))
    fs = fs_pt * scale
    cell_w, cell_h = fs * 0.55, fs * 1.28
    pad = int(fs * 0.45)

    W = int(cols * cell_w) + pad * 2
    H = int(rows * cell_h) + pad * 2
    img = Image.new("RGB", (W, H), "#F7F6F3")
    dr = ImageDraw.Draw(img)

    for r, line in enumerate(lines):
        col = 0
        for ch in line:
            n = _cells(ch)
            if ch != " ":
                f = _pick(ch, int(fs))
                if f:
                    try:
                        bb = dr.textbbox((0, 0), ch, font=f)
                        gw, gh = bb[2] - bb[0], bb[3] - bb[1]
                        x = pad + col * cell_w + (n * cell_w - gw) / 2 - bb[0]
                        y = pad + r * cell_h + (cell_h - gh) / 2 - bb[1]
                        dr.text((x, y), ch, font=f, fill="#24242A")
                    except Exception:
                        pass
            col += n

    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    img.save(out_png, optimize=True)
    wpt, hpt = W / scale, H / scale
    _PNG_CACHE[key] = (wpt, hpt, out_png)
    return wpt, hpt


def _col_widths(payload, ncol):
    """按各列内容显示宽度分配百分比（CJK 记 2 格），避免 6 列表格被挤成细条。"""
    w = []
    for c in range(ncol):
        m = 0
        for r in payload:
            if c < len(r):
                m = max(m, sum(2 if unicodedata.east_asian_width(x) in ("W", "F")
                               else 1 for x in str(r[c])))
        w.append(max(m, 3))
    lo, hi = 0.6 / ncol, 2.6 / ncol
    tot = sum(w)
    pct = [min(max(x / tot, lo), hi) for x in w]
    s = sum(pct)
    return [x / s * 100 for x in pct]


TABLE_KEEP_ROWS = 14   # 不超过这个行数的表整表不跨页（可上 10pt）

# 宽表判据（用户定）：列数 > 6 **且** 单元格文字较多 → 单独出 A4 横向页
WIDE_TABLE_COLS = 6
WIDE_TABLE_AVG_CELL = 5.0    # 平均每格显示宽度（CJK 记 2）低于此值不算"文字多"


def _is_wide_table(payload, ncol):
    """宽表判据：列数 > 6 且平均每格文字较多。"""
    if ncol <= WIDE_TABLE_COLS:
        return False
    tot = 0.0
    n = 0
    for r in payload:
        for c in r:
            tot += sum(2 if unicodedata.east_asian_width(x) in ("W", "F") else 1
                       for x in str(c))
            n += 1
    return n > 0 and (tot / n) >= WIDE_TABLE_AVG_CELL


def table_html(payload, ncol, land=False):
    """生成表格 HTML。land=True 时用于横向页（字号更大、更宽松）。"""
    tcls = "tk" if (land or len(payload) <= TABLE_KEEP_ROWS) else "tf"
    pct = _col_widths(payload, ncol)
    out = ['<table class="%s"><colgroup>%s</colgroup>'
           % (tcls, "".join('<col style="width:%.2f%%">' % p for p in pct))]
    for idx, row in enumerate(payload):
        row = row + [""] * (ncol - len(row))
        cells = "".join("<%s>%s</%s>" % ("th" if idx == 0 else "td",
                                         inline(c),
                                         "th" if idx == 0 else "td")
                        for c in row)
        if idx == 0:
            out.append("<thead><tr>%s</tr></thead><tbody>" % cells)
        else:
            out.append("<tr>%s</tr>" % cells)
    out.append("</tbody></table>")
    return "\n".join(out)


def blocks_to_html(blocks, title_en, title_cn, doc_id):
    out = []
    sec_titles = []        # 每个 ## 大节的标题文本，供分页优化定位
    wide_tables = []       # 需要单独出横向页的宽表
    # 封面
    out.append('<h1 class="cover-en">%s</h1>' % inline(title_en))
    if title_cn:
        out.append('<h2 class="cover-cn">%s</h2>' % inline(title_cn))
    out.append('<div class="cover-meta">BC Science 9 · Chemistry Unit · '
               '英中对照讲义 / Bilingual Handout</div>')

    fig_n = [0]
    for kind, payload in blocks:
        if kind == "p":
            out.append("<p>%s</p>" % inline(payload))
        elif kind.startswith("h") and kind[1:].isdigit():
            lvl = min(int(kind[1:]), 4)
            if kind == "h1" and payload == title_en:
                continue  # 封面已输出
            if kind == "h2" and payload == title_cn:
                continue  # 封面已输出
            cls = ""
            if lvl == 2:
                cls = ' class="sec-%d"' % len(sec_titles)
                sec_titles.append(re.sub(r"[*`]", "", payload).strip())
            out.append("<h%d%s>%s</h%d>" % (lvl, cls, inline(payload), lvl))
        elif kind == "image":
            alt, path = payload
            # 不输出 alt：正文里每张图都有 ### 图 X-X 小标题，alt 与之重复，
            # 会让同一行标题连着出现三次（h3 + alt + SVG 内标题栏）。
            ext = os.path.splitext(path)[1].lower()
            if ext == ".svg" and os.path.exists(path):
                fig_n[0] += 1
                out.append('<div class="fig">%s</div>'
                           % inline_svg(path, "%s_s%02d" % (doc_id,
                                                             fig_n[0])))
            elif os.path.exists(path):
                out.append('<div class="fig"><img src="file:///%s" '
                           'style="max-width:100%%"></div>'
                           % path.replace("\\", "/"))
            else:
                print("     ! 图片引用不存在: %s" % path, file=sys.stderr)
        elif kind == "pre":
            fig_n[0] += 1
            name = "%s_fig%02d.png" % (doc_id, fig_n[0])
            wpt, hpt = render_ascii_png(payload, os.path.join(IMG_DIR, name))
            wpt, hpt = _fit_page(wpt, hpt)
            out.append('<div class="fig"><img src="../_img/%s" '
                       'style="width:%.1fpt"></div>'
                       % (name, wpt))
        elif kind == "table":
            ncol = max(len(r) for r in payload)
            if _is_wide_table(payload, ncol):
                # 紧邻其上的小标题（如表 6-3 xxx）一并搬到横向页，
                # 否则纵页上只剩个标题就被迫断开，白丢半页。
                cap = None
                if out:
                    m = re.match(r"^<h([34])[^>]*>(.*)</h\1>$", out[-1], re.S)
                    if m:
                        cap = (int(m.group(1)), m.group(2))
                        out.pop()
                # 纵向页上只留一个不可见占位标记（独占一页），渲染后整页换成横向表
                idx = len(wide_tables)
                mark = "%sWT%02dMARK" % (doc_id, idx)
                wide_tables.append({"mark": mark, "payload": payload,
                                    "ncol": ncol, "cap": cap})
                out.append('<div class="wt-ph">%s</div>' % mark)
            else:
                out.append(table_html(payload, ncol))
        elif kind in ("ul", "ol"):
            items = "".join("<li>%s</li>" % inline(x) for x in payload)
            out.append("<%s>%s</%s>" % (kind, items, kind))
        elif kind == "quote":
            out.append("<blockquote>%s</blockquote>" % inline(payload))
        elif kind == "hr":
            out.append("<hr>")
    return "\n".join(out), sec_titles, wide_tables


def build_html(md_path, breaks=None):
    """breaks: 需要从新页开始的 ## 大节下标集合；None = 全部都另起一页。"""
    text = open(md_path, encoding="utf-8").read()
    blocks = parse_md(text, os.path.dirname(os.path.abspath(md_path)))

    # 取封面标题：第一个 h1（英）与紧随的 h2（中）
    title_en, title_cn = "", ""
    for idx, (kind, payload) in enumerate(blocks[:3]):
        if kind == "h1" and not title_en:
            title_en = payload
        elif kind == "h2" and title_en and not title_cn:
            title_cn = payload
            break
    if not title_en:
        title_en = os.path.splitext(os.path.basename(md_path))[0]

    m = re.match(r"(Ch\d\d|Appendix[A-E])", os.path.basename(md_path))
    doc_id = m.group(1) if m else "Doc"
    body, sec_titles, wide_tables = blocks_to_html(
        blocks, title_en, title_cn, doc_id)

    css = CSS
    idxs = range(len(sec_titles)) if breaks is None else sorted(breaks)
    if idxs:
        css += "\n" + "\n".join(SEC_BREAK_CSS % i for i in idxs)
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<title>%s</title><style>%s</style></head>"
            "<body>%s</body></html>" % (esc(title_en), css, body)), \
        sec_titles, wide_tables, title_en


def build_land_html(wt, title_en):
    """宽表专用横向页 HTML。"""
    cap = ""
    if wt.get("cap"):
        lvl, txt = wt["cap"]
        cap = "<h%d>%s</h%d>" % (lvl, txt, lvl)
    body = cap + \
        ('<div class="land-cap">%s　·　宽表横向页 / Wide table (landscape)</div>'
         % esc(title_en)) + table_html(wt["payload"], wt["ncol"], land=True)
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<title>wide</title><style>%s</style></head>"
            "<body>%s</body></html>"
            % (CSS_LAND + "\n.land-cap{font-size:8.5pt;color:#5F5E5A;"
                          "margin-bottom:6pt;}", body))


def add_page_numbers(pdf_path):
    """用 pymupdf 补页码（纯数字，规避中文字体坑）。"""
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    doc = pymupdf.open(pdf_path)
    total = len(doc)
    for i, page in enumerate(doc, 1):
        r = page.rect
        page.insert_text(
            (r.width / 2 - 14, r.height - 22),
            "%d / %d" % (i, total),
            fontsize=8.5, fontname="helv", color=(0.42, 0.42, 0.40),
        )
    doc.save(pdf_path.replace(".pdf", ".tmp.pdf"), garbage=4, deflate=True)
    doc.close()
    os.replace(pdf_path.replace(".pdf", ".tmp.pdf"), pdf_path)
    return total


def render_pdf(html_path, pdf_path):
    sys.path.insert(0, HERE)
    import html2pdf
    return html2pdf.render(html2pdf.find_chrome(), html_path, pdf_path)


# ------------------------------------------------------------ 分页优化
# 规则（用户要求）：某页底部空白超过半页就不要翻页。
# 大节(##)默认另起一页，但渲染后逐页量空白比例；若某页空白 > 50%，
# 说明它后面那次"强制分页"太浪费，就把那一节的分页撤销、让内容回流。
# 因为撤销后整体会重排，需要迭代收敛（实测 2~3 轮即稳定）。
PAGE_MARGIN_PT = 51.02    # 18mm
BLANK_LIMIT = 0.50


def _open_pdf():
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    return pymupdf


def page_blank_ratios(pdf_path):
    """返回每页底部空白占版心高度的比例（最后一页通常无意义，调用方自行忽略）。"""
    pymupdf = _open_pdf()
    doc = pymupdf.open(pdf_path)
    out = []
    for page in doc:
        r = page.rect
        top = PAGE_MARGIN_PT
        bot = r.height - PAGE_MARGIN_PT
        h = max(bot - top, 1)
        maxy = top
        for b in page.get_text("blocks"):
            if b[4].strip():
                maxy = max(maxy, b[3])
        try:
            for info in page.get_image_info():
                maxy = max(maxy, info["bbox"][3])
        except Exception:
            pass
        out.append(max(0.0, min(1.0, (bot - maxy) / h)))
    doc.close()
    return out


def page_landscape_flags(pdf_path):
    """每页是否为横向（宽表页）。"""
    doc = _open_pdf().open(pdf_path)
    flags = [p.rect.width > p.rect.height for p in doc]
    doc.close()
    return flags


def find_wasteful_breaks(pdf_path, sec_titles, limit=BLANK_LIMIT,
                         skip_marks=()):
    """找出「上一页空白超过 limit」因而该撤销分页的大节下标。

    skip_marks: 含这些标记的页是宽表占位页，空白是设计使然，跳过不分析。
    """
    ratios = page_blank_ratios(pdf_path)
    if len(ratios) < 2:
        return [], ratios, []
    pymupdf = _open_pdf()
    doc = pymupdf.open(pdf_path)
    texts = [" ".join(p.get_text().split()) for p in doc]
    doc.close()

    bad, unresolved = [], []
    for i, ratio in enumerate(ratios[:-1]):
        if ratio <= limit:
            continue
        if i == 0:
            continue          # 封面页：单独成页是排版惯例，空白不算浪费
        if any(m in texts[i] for m in skip_marks):
            continue          # 宽表占位页
        nxt = texts[i + 1] if i + 1 < len(texts) else ""
        hit = None
        for j, t in enumerate(sec_titles):
            probe = t.split("｜")[0].strip()
            probe = probe[:12] if len(probe) > 12 else probe
            if len(probe) >= 4 and probe in nxt:
                hit = j
                break
        if hit is None:
            unresolved.append(i + 1)
        else:
            bad.append(hit)
    return sorted(set(bad)), ratios, unresolved


# ------------------------------------------------------------ 宽表横向页
def _page_is_empty(page):
    try:
        if page.get_text().strip():
            return False
    except Exception:
        pass
    try:
        if page.get_image_info():
            return False
    except Exception:
        pass
    return True


def splice_wide_tables(portrait_path, land_map, out_path):
    """把宽表的 A4 横向页插进纵向稿。

    land_map: {纵向页下标(0-based): (横向 PDF 路径, [占位标记])}
    若标记所在页只有标记（说明它恰好落在新页开头）→ 整页替换为横向页；
    否则保留该页、把横向页插在它后面（前页因此能自然排满，不留半页空白）。
    PDF 允许同一文件内混用不同页面尺寸，所以横页可以直接插在纵页之间。
    """
    pymupdf = _open_pdf()
    src = pymupdf.open(portrait_path)
    new = pymupdf.open()
    n = len(src)
    i = 0
    used = 0
    while i < n:
        if i in land_map:
            path, marks = land_map[i]
            rest = src[i].get_text().strip()
            for m in marks:
                rest = rest.replace(m, "")
            if rest.strip():
                new.insert_pdf(src, from_page=i, to_page=i)   # 保留原页
            lp = pymupdf.open(path)
            new.insert_pdf(lp)
            used += len(lp)
            lp.close()
            i += 1
            while i < n and _page_is_empty(src[i]) and i not in land_map:
                i += 1          # 吃掉 break-after 造成的空白页
        else:
            if not _page_is_empty(src[i]):
                new.insert_pdf(src, from_page=i, to_page=i)
            i += 1
    new.save(out_path, garbage=4, deflate=True)
    n_land = len(new)
    new.close()
    src.close()
    return n_land, used


def strip_marks(pdf_path, marks):
    """把占位标记从文本层抹掉（红action），避免复制粘贴时带出 ChxxWTnnMARK。"""
    if not marks:
        return
    try:
        doc = _open_pdf().open(pdf_path)
        hit = False
        for page in doc:
            got = False
            for m in marks:
                for rect in page.search_for(m):
                    page.add_redact_annot(rect)
                    got = True
            if got:
                page.apply_redactions()
                hit = True
        if hit:
            tmp = pdf_path.replace(".pdf", ".cln.pdf")
            doc.save(tmp, garbage=4, deflate=True)
            doc.close()
            os.replace(tmp, pdf_path)
            return
        doc.close()
    except Exception as e:
        print("     (抹除占位标记失败，忽略) %s" % e, file=sys.stderr)


def main():
    global OUT_DIR, HTML_DIR, IMG_DIR, EN_MODE
    args = list(sys.argv[1:])

    # --src <MD 下的子目录名>  chapters-cn（默认）/ appendices-cn / chapters-en
    src_dir, pat = CHAPTERS, "Ch*.md"
    if "--src" in args:
        i = args.index("--src")
        a = args[i + 1]
        src_dir = a if os.path.isabs(a) else os.path.join(MD, a)
        pat = "*.md"
        del args[i:i + 2]

    # 英文版输出到 pdf/EN/ 子目录：md 文件名与中文版完全相同，
    # 直接输出到 pdf/CN/ 会把中文版各章 PDF 覆盖掉。
    _base = os.path.basename(src_dir.rstrip(os.sep)).lower()
    if _base in ("chapters-en", "appendices-en", "en") or _base.endswith("-en") \
            or "--en" in args:
        EN_MODE = True
        if "--en" in args:
            args.remove("--en")
        OUT_DIR = os.path.join(G9, "pdf", "EN")
        HTML_DIR = os.path.join(OUT_DIR, "_html")
        IMG_DIR = os.path.join(OUT_DIR, "_img")

    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(HTML_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)

    # 下划线开头的是说明性文档（如 chapters-en/_STYLE.md 体例规范），不参与排版
    files = [f for f in sorted(glob.glob(os.path.join(src_dir, pat)))
             if not os.path.basename(f).startswith("_")]
    if args:
        key = args[0].lower()
        files = [f for f in files if key in os.path.basename(f).lower()]
    if not files:
        raise SystemExit("没有匹配的章节文件")

    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]
        html_path = os.path.join(HTML_DIR, base + ".html")
        pdf_path = os.path.join(OUT_DIR, base + ".pdf")

        breaks = None            # None = 每个大节都另起一页
        ratios, unresolved = [], []
        for _ in range(5):
            html, sec_titles, wide_tables, title_en = build_html(f, breaks)
            open(html_path, "w", encoding="utf-8").write(html)
            render_pdf(html_path, pdf_path)
            bad, ratios, unresolved = find_wasteful_breaks(
                pdf_path, sec_titles,
                skip_marks=[w["mark"] for w in wide_tables])
            if not bad:
                break
            if breaks is None:
                breaks = set(range(len(sec_titles)))
            for j in bad:
                breaks.discard(j)

        # 宽表：单独渲染成 A4 横向页，再替换掉纵向稿里的占位页
        n_land = 0
        if wide_tables:
            land_map = {}
            doc = _open_pdf().open(pdf_path)
            for k, wt in enumerate(wide_tables):
                lname = "%s_wt%02d" % (base, k)
                lhtml = os.path.join(HTML_DIR, lname + ".html")
                lpdf = os.path.join(HTML_DIR, lname + ".pdf")
                open(lhtml, "w", encoding="utf-8").write(
                    build_land_html(wt, title_en))
                render_pdf(lhtml, lpdf)
                hit = None
                for i in range(len(doc)):
                    if wt["mark"] in doc[i].get_text():
                        hit = i
                        break
                if hit is None:
                    print("     ! 未定位到宽表占位页 %s，已改为纵向排版"
                          % wt["mark"], file=sys.stderr)
                    continue
                land_map[hit] = (lpdf, [wt["mark"]])
            doc.close()
            if land_map:
                tmp = os.path.join(HTML_DIR, base + "_spliced.pdf")
                n_land = splice_wide_tables(pdf_path, land_map, tmp)[1]
                os.replace(tmp, pdf_path)
        strip_marks(pdf_path, [w["mark"] for w in wide_tables])

        # 统计口径：占位页已被横页替换，必须在替换后重新量，否则会报假的高空白
        ratios = page_blank_ratios(pdf_path)
        land_flags = page_landscape_flags(pdf_path)
        # 横页天然底部空白大（表格矮、纸面宽），不参与"空白超半页"统计
        unresolved = [i + 1 for i in range(len(ratios) - 1)
                      if i > 0 and ratios[i] > BLANK_LIMIT
                      and not land_flags[i]]
        add_page_numbers(pdf_path)
        # 封面页与横页都不计入"最大空白"统计
        body_ratios = [r for i, r in enumerate(ratios)
                       if 0 < i < len(ratios) - 1 and not land_flags[i]]
        worst = max(body_ratios) if body_ratios else 0.0
        note = ""
        if worst > BLANK_LIMIT:
            note = "  (p%d 空白%.0f%%)" % (
                ratios.index(worst) + 1, worst * 100)
        wt_note = "  宽表横页%d个" % len(land_map) if wide_tables else ""
        print("OK  %-34s %2d页 撤销分页%d处 最大空白%.0f%%%s%s"
              % (os.path.basename(pdf_path), len(ratios),
                 0 if breaks is None else len(sec_titles) - len(breaks),
                 worst * 100, wt_note, note))
        if unresolved:
            print("     注：p%s 空白超半页但非大节分页造成（图/表被挤到下一页）"
                  % ",".join(str(x) for x in unresolved))


if __name__ == "__main__":
    main()
