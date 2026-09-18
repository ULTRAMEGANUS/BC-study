# -*- coding: utf-8 -*-
"""把章节 md 讲义转成英中对照教学 PPT。

用法：
    python build_pptx.py <chapter.md> <输出.pptx> [附加SVG名 ...]

例：
    python build_pptx.py ../../chapters/Ch01_xxx.md ../../ppt/Ch01_Matter.pptx main-thread-flowchart.svg

设计要点：
- 16:9；英文用 Segoe UI，中文用 Microsoft YaHei，ASCII 图用 Consolas（按字符切分 run 设字体）
- 文本高度按「中文 1.0 em / 西文 0.55 em」估算，超出自动缩字号或翻页
- SVG 通过 Edge headless 转 PNG 后插入（纯 Python 无可靠 SVG 光栅化方案）
"""
import os, re, sys, math, html, subprocess, tempfile

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

# ============================================================ 样式常量
EN_FONT = "Segoe UI"
CN_FONT = "Microsoft YaHei"
MONO_FONT = "Consolas"

INK      = RGBColor(0x2C, 0x2C, 0x2A)
MUTED    = RGBColor(0x5F, 0x5E, 0x5A)
HINT     = RGBColor(0x88, 0x87, 0x80)
GRID     = RGBColor(0xB4, 0xB2, 0xA9)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT   = RGBColor(0x18, 0x5F, 0xA5)   # 主蓝
ACCENT_L = RGBColor(0xE6, 0xF1, 0xFB)   # 浅蓝底
ACCENT_D = RGBColor(0x0C, 0x44, 0x7C)
RED      = RGBColor(0xA3, 0x2D, 0x2D)
ORANGE_L = RGBColor(0xFA, 0xEE, 0xDA)
GREEN_L  = RGBColor(0xEA, 0xF3, 0xDE)
GRAY_L   = RGBColor(0xF4, 0xF3, 0xF0)

SW, SH = 13.333, 7.5                    # 16:9 英寸
MARGIN = 0.62
BODY_W = SW - 2 * MARGIN                # 12.09
HEADER_Y = 0.30
TITLE_Y = 0.52
BODY_Y = 1.42
BODY_H = 5.62
FOOT_Y = 7.02

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
EDGE_ALT = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

CJK = r"\u2e80-\u9fff\u3000-\u303f\uff00-\uffef"


# ============================================================ 文本工具
def is_cjk(ch):
    return ch in "，。、；：？！「」『』（）《》—…·" or \
        (0x2E80 <= ord(ch) <= 0x9FFF) or (0x3000 <= ord(ch) <= 0x303F) \
        or (0xFF00 <= ord(ch) <= 0xFFEF)


def text_width_em(s):
    """以字号为 1em 估算字符串宽度（中文按 1.0，西文按 0.55）。"""
    w = 0.0
    for ch in s:
        w += 1.0 if is_cjk(ch) else 0.55
    return w


def strip_md(s):
    """去掉 markdown 标记，返回纯文本（保留 ** 由调用方处理）。"""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    return s.strip()


def split_bold(s):
    """把 'a **b** c' 拆成 [(text, is_bold), ...]。"""
    out, pos = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*", s):
        if m.start() > pos:
            out.append((s[pos:m.start()], False))
        out.append((m.group(1), True))
        pos = m.end()
    if pos < len(s):
        out.append((s[pos:], False))
    return out or [(s, False)]


def add_runs(tf, text, size, color, bold=False, font=None, first=False):
    """按中英文切分写入 run，中英分别用不同字体。"""
    para = tf.paragraphs[0] if first else tf.add_paragraph()
    para.alignment = PP_ALIGN.LEFT
    for seg, isb in split_bold(text):
        if not seg:
            continue
        buf, cur = "", None
        for ch in seg:
            k = "cn" if is_cjk(ch) else "en"
            if cur is None:
                cur = k
            if k != cur:
                r = para.add_run()
                r.text = buf
                r.font.size = Pt(size)
                r.font.bold = bold or isb
                r.font.color.rgb = color
                r.font.name = CN_FONT if cur == "cn" else (font or EN_FONT)
                _set_ea(r, CN_FONT if cur == "cn" else (font or EN_FONT))
                buf, cur = ch, k
            else:
                buf += ch
        if buf:
            r = para.add_run()
            r.text = buf
            r.font.size = Pt(size)
            r.font.bold = bold or isb
            r.font.color.rgb = color
            r.font.name = CN_FONT if cur == "cn" else (font or EN_FONT)
            _set_ea(r, CN_FONT if cur == "cn" else (font or EN_FONT))
    return para


def _set_ea(run, font_name):
    """设置东亚字体，避免中文在部分机器上回退到宋体。"""
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", font_name)


def fit_size(text, width_in, base_size, min_size=8, max_size=None):
    """按内容宽度估算合适的字号（用于表格与等宽图）。"""
    max_size = max_size or base_size
    tw = text_width_em(max(text.split("\n"), key=text_width_em)) if text else 0
    if tw <= 0:
        return base_size
    size = min(max_size, int(width_in * 72 / (tw * 1.02)))
    return max(min_size, min(max_size, size))


def est_height(text, width_in, size, line_gap=1.36):
    """估算一段文本渲染后的高度（英寸）。

    关键：把「em 数」和「字符数」统一。1em == size(pt)，所以每行能容纳的
    em 数 = 可用宽度(pt) / size。中文占 1.0em，西文占 0.55em。
    （早先版本用字符数当分母，把高度低估了近一倍，会造成内容重叠。）
    """
    cap = (width_in * 72.0) / max(size, 1.0)
    total = 0.0
    for line in text.split("\n"):
        em = text_width_em(line)
        rows = max(1, math.ceil(em / cap - 1e-9)) if em > 0 else 1
        total += rows * size * line_gap
    return total / 72.0 * 1.04          # 4% 安全余量


# ============================================================ SVG → PNG
def svg_to_png(svg_path, png_path, scale=2.0):
    with open(svg_path, encoding="utf-8") as f:
        svg = f.read()
    m = re.search(r'viewBox=["\']([\d.\-]+)\s+([\d.\-]+)\s+([\d.]+)\s+([\d.]+)', svg)
    if not m:
        return None
    w, h = float(m.group(3)), float(m.group(4))
    W, H = int(w * scale), int(h * scale)
    svg = re.sub(r"<svg([^>]*)>", lambda mm: "<svg" + re.sub(
        r'\s(width|height)="[^"]*"', "", mm.group(1)) + f' width="{W}" height="{H}">', svg, count=1)
    html_doc = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
                'html,body{margin:0;padding:0;background:#fff;overflow:hidden}'
                '</style></head><body>' + svg + '</body></html>')
    fd, tmp = tempfile.mkstemp(suffix=".html", text=True)
    os.close(fd)
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html_doc)
    exe = EDGE if os.path.exists(EDGE) else EDGE_ALT
    for headless in ("--headless=new", "--headless"):
        try:
            subprocess.run([exe, headless, "--disable-gpu", "--no-sandbox",
                            "--hide-scrollbars", f"--window-size={W},{H}",
                            f"--screenshot={png_path}", "file:///" + tmp.replace("\\", "/")],
                           timeout=60, capture_output=True)
        except Exception:
            pass
        if os.path.exists(png_path) and os.path.getsize(png_path) > 1000:
            break
    try:
        os.remove(tmp)
    except OSError:
        pass
    return png_path if os.path.exists(png_path) else None


# ============================================================ md 解析
def parse_md(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    meta, sections, cur = {}, [], None
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if ln.startswith("# "):
            meta["title_en"] = ln[2:].strip()
            i += 1
            continue
        if ln.startswith("## 第"):
            meta["title_cn"] = ln.replace("##", "").strip()
            i += 1
            continue
        if ln.startswith("> ") and cur is None and not sections:
            body = ln[2:].strip()
            m = re.match(r"\*\*(.+?)\*\*[：:](.+)", body)
            if m:
                meta[m.group(1)] = m.group(2).strip()
            i += 1
            continue
        if ln.startswith("## "):
            head = ln[3:].strip()
            mm = re.match(r"(\d+)\.\s*(.*)", head)
            cur = {"num": mm.group(1) if mm else "0",
                   "head": head, "blocks": []}
            if "｜" in head:
                a, b = head.split("｜", 1)
                cur["en"], cur["cn"] = b.strip(), a.strip()
            else:
                cur["en"] = cur["cn"] = head
            sections.append(cur)
            i += 1
            continue
        if cur is None:
            i += 1
            continue

        if ln.startswith("```"):                      # 代码块（ASCII 图）
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cur["blocks"].append({"type": "code", "text": "\n".join(buf)})
            continue
        if ln.startswith("### "):
            cur["blocks"].append({"type": "sub", "text": ln[4:].strip()})
            i += 1
            continue
        if ln.startswith("|") and i + 1 < n and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1].strip()):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not re.match(r"^[\s:\-]+$", "".join(cells)):
                    rows.append(cells)
                i += 1
            if rows:
                cur["blocks"].append({"type": "table", "rows": rows})
            continue
        if ln.strip() == "---":
            i += 1
            continue
        if ln.startswith("> "):
            cur["blocks"].append({"type": "quote", "text": ln[2:].strip()})
            i += 1
            continue
        if re.match(r"^\s*[-*]\s+", ln) or re.match(r"^\s*\d+\.\s+", ln):
            items = []
            while i < n and (re.match(r"^\s*[-*]\s+", lines[i]) or re.match(r"^\s*\d+\.\s+", lines[i])
                             or (items and re.match(r"^\s{2,}\S", lines[i]))):
                items.append(lines[i])
                i += 1
            cur["blocks"].append({"type": "list", "items": items})
            continue
        if ln.strip():
            cur["blocks"].append({"type": "para", "text": ln.strip()})
        i += 1
    return meta, sections


def fmt_list(items):
    out = []
    for it in items:
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", it)
        if not m:
            continue
        indent, _, text = m.groups()
        level = len(indent) // 2
        out.append((level, strip_md(text)))
    return out


# ============================================================ 幻灯片构建
class Deck:
    def __init__(self, meta, chapter_tag):
        self.prs = Presentation()
        self.prs.slide_width = Inches(SW)
        self.prs.slide_height = Inches(SH)
        self.blank = self.prs.slide_layouts[6]
        self.meta = meta
        self.tag = chapter_tag
        self.n = 0

    # ---------- 基础
    def new(self):
        s = self.prs.slides.add_slide(self.blank)
        self.n += 1
        return s

    def rect(self, s, x, y, w, h, fill=None, line=None, lw=0.75):
        from pptx.enum.shapes import MSO_SHAPE
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid()
            sh.fill.fore_color.rgb = fill
        if line is None:
            sh.line.fill.background()
        else:
            sh.line.color.rgb = line
            sh.line.width = Pt(lw)
        sh.shadow.inherit = False
        return sh

    def tb(self, s, x, y, w, h):
        t = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = t.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        return tf

    def footer(self, s, label=""):
        tf = self.tb(s, MARGIN, FOOT_Y, BODY_W, 0.28)
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = f"{self.tag}　|　{label}"
        r.font.size = Pt(9)
        r.font.color.rgb = HINT
        r.font.name = EN_FONT
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.RIGHT
        r2 = p2.add_run()
        r2.text = str(self.n)
        r2.font.size = Pt(9)
        r2.font.color.rgb = HINT
        r2.font.name = EN_FONT
        self.rect(s, MARGIN, FOOT_Y - 0.10, BODY_W, 0.01, fill=GRID)

    # ---------- 页面类型
    def cover(self, en, cn):
        s = self.new()
        self.rect(s, 0, 0, SW, SH, fill=RGBColor(0x0C, 0x44, 0x7C))
        self.rect(s, 0, 0, SW, 0.10, fill=RGBColor(0x9F, 0xD3, 0xF5))
        tf = self.tb(s, 1.0, 2.15, 11.3, 2.45)
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = self.tag.upper()
        r.font.size = Pt(20)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x9F, 0xD3, 0xF5)
        r.font.name = EN_FONT
        add_runs(tf, en, 40, WHITE, bold=True, first=False)
        add_runs(tf, cn, 24, RGBColor(0xB5, 0xD8, 0xF2), first=False)
        info = self.meta.get("课时 Periods", "")
        tf2 = self.tb(s, 1.0, 5.55, 11.3, 1.4)
        for t, sz, col in [
            ("BC Science 9 · Chemistry Unit　｜　不列颠哥伦比亚省 九年级科学 · 化学单元", 13, RGBColor(0x9F, 0xD3, 0xF5)),
            (f"课时 Periods：{info}" if info else "", 11, RGBColor(0x7E, 0xB8, 0xE0)),
            ("英中对照讲义　Bilingual Handout", 11, RGBColor(0x7E, 0xB8, 0xE0)),
        ]:
            if t:
                add_runs(tf2, t, sz, col, first=(t == t and tf2.paragraphs[0].runs == []))
        return s

    def section_divider(self, num, en, cn):
        s = self.new()
        self.rect(s, 0, 0, SW, SH, fill=ACCENT_L)
        self.rect(s, 0, 0, 0.22, SH, fill=ACCENT)
        tf = self.tb(s, 1.4, 2.45, 11, 2.55)
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = num
        r.font.size = Pt(72)
        r.font.bold = True
        r.font.color.rgb = ACCENT
        r.font.name = EN_FONT
        add_runs(tf, en, 30, INK, bold=True, first=False)
        add_runs(tf, cn, 20, MUTED, first=False)
        self.footer(s, "")
        return s

    def content_page(self, en, cn, blocks, label=""):
        """内容页：按估算高度自动续页，超出部分**绝不丢弃**。"""
        queue, page_no = list(blocks), 0
        while queue:
            page_no += 1
            s = self.new()
            self.rect(s, 0, 0, SW, 0.09, fill=ACCENT)
            title = en if page_no == 1 else f"{en}　（续 {page_no}）"
            self._title(s, title, cn)

            y, rest, started, i = BODY_Y, [], False, 0
            while i < len(queue):
                b = queue[i]
                if b[0] == "list":                     # 列表可跨页拆分
                    placed, remain, yy = [], [], y
                    for lvl, txt in b[1]:
                        w = BODY_W - 0.26 * (lvl + 1) - 0.16
                        h = est_height(txt, w, 14) + 0.11
                        if yy + h <= FOOT_Y - 0.35 and not remain:
                            placed.append((lvl, txt))
                            yy += h
                        else:
                            remain.append((lvl, txt))
                    if placed:
                        y = self._draw_block(s, ("list", placed), y)
                        started = True
                    if remain:
                        rest.append(("list", remain))
                    i += 1
                    continue
                h = self._block_height(b)
                if started and y + h > FOOT_Y - 0.35:
                    rest.extend(queue[i:])
                    break
                self._draw_block(s, b, y)
                y += h
                started = True
                i += 1
            self.footer(s, label)
            queue = rest
        return s

    def _block_height(self, b):
        k = b[0]
        if k == "p":
            return est_height(b[1], BODY_W, 15) + 0.16
        if k == "kv":
            return est_height(b[1] + b[2], BODY_W, 14) + 0.16
        if k == "quote":
            return est_height(b[1], BODY_W - 0.5, 13) + 0.26 + 0.20
        if k == "list":
            tot = 0.10
            for lvl, txt in b[1]:
                tot += est_height(txt, BODY_W - 0.26 * (lvl + 1) - 0.16, 14) + 0.11
            return tot
        return 0.2

    def _title(self, s, en, cn, max_h=0.88, base=25):
        """页标题：英文主标题 + 中文副标题，过长时自动降字号，避免压到正文。"""
        size = base
        while size > 16 and est_height(en, BODY_W, size) > max_h * 0.62:
            size -= 2
        csize = 15
        if cn and cn != en:
            while csize > 11 and est_height(cn, BODY_W, csize) > max_h * 0.34:
                csize -= 1
        tf = self.tb(s, MARGIN, TITLE_Y, BODY_W, max_h)
        add_runs(tf, en, size, INK, bold=True, first=True)
        if cn and cn != en:
            add_runs(tf, cn, csize, MUTED, first=False)
        return tf

    def _draw_block(self, s, b, y):
        kind = b[0]
        if kind == "p":
            h = est_height(b[1], BODY_W, 15)
            tf = self.tb(s, MARGIN, y, BODY_W, h)
            add_runs(tf, b[1], 15, INK, first=True)
            return y + h + 0.16
        if kind == "quote":
            txt = b[1]
            tw = BODY_W - 0.62
            th = est_height(txt, tw, 13)
            h = th + 0.26
            self.rect(s, MARGIN, y - 0.06, BODY_W, h, fill=GRAY_L)
            self.rect(s, MARGIN, y - 0.06, 0.055, h, fill=ACCENT)
            tf = self.tb(s, MARGIN + 0.24, y + 0.07, tw, th)
            add_runs(tf, txt, 13, INK, first=True)
            return y + h + 0.20
        if kind == "list":
            for lvl, txt in b[1]:
                indent = MARGIN + 0.26 * (lvl + 1)
                w = BODY_W - 0.26 * (lvl + 1) - 0.16
                h = est_height(txt, w, 14)
                tf = self.tb(s, indent, y, w, h)
                p = tf.paragraphs[0]
                bullet = "▸ " if lvl == 0 else "· "
                r = p.add_run()
                r.text = bullet
                r.font.size = Pt(14)
                r.font.color.rgb = ACCENT if lvl == 0 else HINT
                r.font.name = EN_FONT
                for seg, isb in split_bold(txt):
                    rr = p.add_run()
                    rr.text = seg
                    rr.font.size = Pt(14)
                    rr.font.bold = isb
                    rr.font.color.rgb = INK
                    rr.font.name = EN_FONT
                    _set_ea(rr, EN_FONT)
                y += h + 0.11
            return y + 0.10
        if kind == "kv":
            h = est_height(b[1] + b[2], BODY_W, 14)
            tf = self.tb(s, MARGIN, y, BODY_W, h)
            add_runs(tf, b[1] + "　" + b[2], 14, INK, first=True)
            return y + h + 0.16
        return y

    # ---------- 表格页
    def table_page(self, en, cn, rows, label="", max_rows=14, note=None):
        header, body = rows[0], rows[1:]
        # 每页都要带表头，否则续页看不出列含义
        chunks = [body[i:i + max_rows] for i in range(0, len(body), max_rows)] or [[]]
        total = len(chunks)
        for idx, chunk in enumerate(chunks):
            data = [header] + chunk
            s = self.new()
            self.rect(s, 0, 0, SW, 0.09, fill=ACCENT)
            title = en if total == 1 else f"{en}　（{idx + 1}/{total}）"
            self._title(s, title, cn, base=24)
            self._render_table(s, data, BODY_Y, BODY_H if not note else BODY_H - 0.5)
            if note:
                tf2 = self.tb(s, MARGIN, FOOT_Y - 0.58, BODY_W, 0.45)
                add_runs(tf2, note, 11.5, MUTED, first=True)
            self.footer(s, label)

    def _row_heights(self, rows, widths, size):
        """按单元格内容实际所需行数算行高（英寸）。

        PowerPoint 的表格行会自动增高，若我们给的行高小于内容需要，
        表格会被撑大、可能顶到页脚。所以这里按内容精确估算。
        """
        hs = []
        for r in rows:
            mx = 1
            for i, c in enumerate(r):
                w = max(0.30, widths[i] - 0.16)          # 扣掉左右单元格边距
                em = text_width_em(strip_md(c))
                cap = (w * 72.0) / max(size, 1.0)
                mx = max(mx, math.ceil(em / cap - 1e-9) if em > 0 else 1)
            hs.append(max(0.22, mx * size * 1.32 / 72.0 + 0.07))
        return hs

    def _render_table(self, s, rows, top, avail_h):
        if not rows:
            return
        cols = max(len(r) for r in rows)
        rows = [r + [""] * (cols - len(r)) for r in rows]
        longest = max((max((text_width_em(c) for c in r), default=0), r) for r in rows)[1]
        col_w_src = [max(text_width_em(r[i]) for r in rows) for i in range(cols)]
        tot = sum(col_w_src) or 1
        # 按内容宽度分配列宽，并给每列留出内边距
        widths = [max(0.55, BODY_W * w / tot) for w in col_w_src]
        scale = BODY_W / sum(widths)
        widths = [w * scale for w in widths]

        # 字号：先按「每列内容各占一行」取上限，再按总高度收敛；
        # 行高按每个单元格实际需要的行数算，避免 PowerPoint 自适应后撑出页面
        sample = max((" ".join(r) for r in rows), key=text_width_em)
        size = float(fit_size(sample, BODY_W * 1.6, 13, min_size=7.5, max_size=13))
        while size > 7.5:
            hs = self._row_heights(rows, widths, size)
            if sum(hs) <= avail_h:
                break
            size -= 0.5
        hs = self._row_heights(rows, widths, size)
        need = sum(hs)
        height = min(need, avail_h)

        shape = s.shapes.add_table(len(rows), cols, Inches(MARGIN), Inches(top),
                                   Inches(BODY_W), Inches(height))
        tbl = shape.table
        for i, w in enumerate(widths):
            tbl.columns[i].width = Emu(int(Inches(w)))
        for r in range(len(rows)):
            tbl.rows[r].height = Emu(int(Inches(hs[r])))

        for r, row in enumerate(rows):
            for c in range(cols):
                cell = tbl.cell(r, c)
                cell.margin_left = Inches(0.07)
                cell.margin_right = Inches(0.07)
                cell.margin_top = Inches(0.03)
                cell.margin_bottom = Inches(0.03)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                cell.fill.solid()
                if r == 0:
                    cell.fill.fore_color.rgb = ACCENT
                elif r % 2 == 0:
                    cell.fill.fore_color.rgb = GRAY_L
                else:
                    cell.fill.fore_color.rgb = WHITE
                tf = cell.text_frame
                tf.word_wrap = True
                for para in list(tf.paragraphs)[1:]:
                    p = para._p
                    p.getparent().remove(p)
                txt = strip_md(row[c])
                add_runs(tf, txt, size, WHITE if r == 0 else INK,
                         bold=(r == 0), first=True)
                self._cell_border(cell, GRID if r else ACCENT)

    def _cell_border(self, cell, color):
        tcPr = cell._tc.get_or_add_tcPr()
        for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
            el = tcPr.find(qn(tag))
            if el is None:
                el = tcPr.makeelement(qn(tag), {"w": "9525", "cap": "flat", "cmpd": "sng", "algn": "ctr"})
                tcPr.append(el)
            for sub in ("a:solidFill",):
                s = el.find(qn(sub))
                if s is None:
                    s = el.makeelement(qn("a:solidFill"), {})
                    el.append(s)
                for c in list(s):
                    s.remove(c)
                clr = s.makeelement(qn("a:srgbClr"), {"val": str(color)})
                s.append(clr)

    # ---------- 代码 / ASCII 图页
    def code_page(self, en, cn, code, label="", note=None):
        s = self.new()
        self.rect(s, 0, 0, SW, 0.09, fill=ACCENT)
        self._title(s, en, cn, base=23)

        lines = [l for l in code.split("\n")]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        body = "\n".join(lines)
        avail_h = BODY_H - (0.5 if note else 0)
        size = 13
        while size > 6:
            need = len(lines) * size * 1.24 / 72.0
            widest = max((text_width_em(l) for l in lines), default=1)
            # 等宽字体：西文 0.55em、中文回退约 1.0em，text_width_em 已折算过
            if need <= avail_h and widest * size * 1.02 / 72.0 <= BODY_W - 0.5:
                break
            size -= 0.5
        box_h = min(avail_h, len(lines) * size * 1.24 / 72.0 + 0.2)
        self.rect(s, MARGIN - 0.14, BODY_Y - 0.12, BODY_W + 0.28, box_h, fill=RGBColor(0xFA, 0xFA, 0xF8), line=GRID)
        tf2 = self.tb(s, MARGIN + 0.02, BODY_Y + 0.02, BODY_W, box_h)
        first = True
        for l in lines:
            p = tf2.paragraphs[0] if first else tf2.add_paragraph()
            first = False
            p.line_spacing = 1.0
            if not l:
                r = p.add_run()
                r.text = " "
                r.font.size = Pt(size)
            else:
                for seg, isb in split_bold(l):
                    if not seg:
                        continue
                    r = p.add_run()
                    r.text = seg
                    r.font.size = Pt(size)
                    r.font.name = MONO_FONT
                    _set_ea(r, MONO_FONT)
                    r.font.color.rgb = INK
        if note:
            tf3 = self.tb(s, MARGIN, BODY_Y + box_h + 0.10, BODY_W, 0.45)
            add_runs(tf3, note, 11.5, MUTED, first=True)
        self.footer(s, label)

    # ---------- 图片页（SVG 转 PNG）
    def image_page(self, en, cn, png, label="", note=None):
        s = self.new()
        self.rect(s, 0, 0, SW, 0.09, fill=ACCENT)
        self._title(s, en, cn, base=24)
        avail_h = BODY_H - (0.42 if note else 0)
        avail_w = BODY_W
        try:
            from PIL import Image
            with Image.open(png) as im:
                iw, ih = im.size
            ar = iw / ih
            if avail_w / ar <= avail_h:
                w, h = avail_w, avail_w / ar
            else:
                h, w = avail_h, avail_h * ar
        except Exception:
            w, h = avail_w, avail_h
        s.shapes.add_picture(png, Inches(MARGIN + (avail_w - w) / 2), Inches(BODY_Y), Inches(w), Inches(h))
        if note:
            tf3 = self.tb(s, MARGIN, BODY_Y + h + 0.10, BODY_W, 0.4)
            add_runs(tf3, note, 11.5, MUTED, first=True)
        self.footer(s, label)

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.prs.save(path)
        return path


# ============================================================ 章节 → 幻灯片
def build(md_path, out_path, extra_svgs=(), figures_dir=None, png_dir=None):
    meta, sections = parse_md(md_path)
    tag = "CH." + (re.search(r"Ch(\d+)", os.path.basename(md_path)).group(1)
                   if re.search(r"Ch(\d+)", os.path.basename(md_path)) else "?")
    deck = Deck(meta, tag)

    deck.cover(meta.get("title_en", ""), meta.get("title_cn", ""))

    # 附加 SVG（如全册主线图）放在导览位置
    if extra_svgs and figures_dir:
        for name in extra_svgs:
            src = os.path.join(figures_dir, name)
            if not os.path.exists(src):
                continue
            png = svg_to_png(src, os.path.join(png_dir, name.replace(".svg", ".png")))
            if png:
                deck.image_page("Where This Chapter Fits　本章位置",
                                "全册主线：电子排布 → 周期表 → 价电子 → 化合物",
                                png, note="先看路线图：本章是起点，终点是「电子排布决定化合物」。")

    for sec in sections:
        deck.section_divider(sec["num"], sec.get("en", ""), sec.get("cn", ""))
        pending, pend_title = [], None

        def flush():
            """把攒下的 block 输出成一页；没有子标题时回退用节标题。"""
            nonlocal pending
            if not pending:
                return
            t0 = pend_title[0] if pend_title else sec.get("en", "")
            t1 = pend_title[1] if pend_title else ""
            deck.content_page(t0, t1, pending, label=sec.get("cn", ""))
            pending = []

        for b in sec["blocks"]:
            if b["type"] == "sub":
                flush()
                t = b["text"]
                if "｜" in t:
                    a, c = t.split("｜", 1)
                    pend_title = (c.strip(), a.strip())
                else:
                    pend_title = (t, "")
                continue
            if b["type"] == "table":
                flush()
                deck.table_page(pend_title[0] if pend_title else sec.get("en", ""),
                                pend_title[1] if pend_title else "",
                                b["rows"], label=sec.get("cn", ""))
                continue
            if b["type"] == "code":
                flush()
                deck.code_page(pend_title[0] if pend_title else sec.get("en", ""),
                               pend_title[1] if pend_title else "",
                               b["text"], label=sec.get("cn", ""))
                continue
            if b["type"] == "list":
                pending.append(("list", fmt_list(b["items"])))
            elif b["type"] == "quote":
                pending.append(("quote", strip_md(b["text"])))
            elif b["type"] == "para":
                pending.append(("p", strip_md(b["text"])))
        flush()

    return deck.save(out_path), deck.n


if __name__ == "__main__":
    md = sys.argv[1]
    out = sys.argv[2]
    svgs = sys.argv[3:]
    here = os.path.dirname(os.path.abspath(__file__))
    figs = os.path.abspath(os.path.join(here, "..", "figures"))
    pngs = os.path.join(os.path.dirname(os.path.abspath(out)), "_png")
    os.makedirs(pngs, exist_ok=True)
    path, n = build(md, out, svgs, figs, pngs)
    print("written:", path, "(%d slides)" % n)
