# -*- coding: utf-8 -*-
"""校验章节 PDF：溢出 / 中文渲染 / 内容完整性 / 字体嵌入。

用法：
    check_chapter_pdf.py            # 校验 G9/pdf/CN/ 下全部
    check_chapter_pdf.py Ch01       # 只校验第 1 章

本机没有 PDF 阅读器且内置 Read 看不了 PDF，所以只能靠 pymupdf 程序化断言。
校验项（每项都可能抓出人眼看不出的问题）：
1. 文字块是否越出页边距（左右下三边）
2. 中文是否正常渲染（不是 IIII / 空白 / 豆腐块）
3. md 里的各级标题是否都在 PDF 中出现（防内容被静默丢弃）
4. 中文字体是否嵌入
5. 页码是否补齐
"""
import os
import re
import sys
import glob

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(os.path.dirname(HERE))               # assets/source -> G9/MD
G9 = os.path.dirname(MD)
PDF_DIR = os.path.join(G9, "pdf", "CN")
CHAPTERS = os.path.join(MD, "chapters-cn")

A4_W, A4_H = 595.28, 841.89
TOL = 2.0
# 同一 PDF 里可能混有横向页（宽表专用），边界必须按页面实际尺寸算，
# 否则横向页会被误判成"右侧溢出"。
MM = 72.0 / 25.4


def page_bounds(page):
    """按页面尺寸返回 (左边界, 右边界, 下边界)。纵向 14/18mm，横向 10/14mm。"""
    r = page.rect
    if r.width > r.height:                 # A4 landscape
        mx, mb = 10 * MM, 14 * MM
    else:                                  # A4 portrait
        mx, mb = 14 * MM, 18 * MM
    return mx, r.width - mx, r.height - mb


def md_images(md_path):
    """md 里的图片引用，返回 [(alt, 相对路径), ...]。"""
    if not md_path or not os.path.exists(md_path):
        return []
    out = []
    for ln in open(md_path, encoding="utf-8"):
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", ln.strip())
        if m:
            out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def svg_texts(path):
    """取出 SVG 内所有 <text> 的文字内容。"""
    import xml.etree.ElementTree as ET
    try:
        root = ET.parse(path).getroot()
    except Exception:
        return []
    return ["".join(t.itertext()).strip()
            for t in root.iter("{http://www.w3.org/2000/svg}text")]


def md_fig_count(md_path):
    """md 里 ASCII 图（代码围栏）的数量。"""
    if not md_path or not os.path.exists(md_path):
        return 0
    n, inb = 0, False
    for ln in open(md_path, encoding="utf-8"):
        if ln.strip().startswith("```"):
            if inb:
                n += 1
            inb = not inb
    return n


def md_titles(md_path):
    ts = []
    for ln in open(md_path, encoding="utf-8"):
        m = re.match(r"^(#{1,3})\s+(.*)$", ln.strip())
        if m:
            ts.append(m.group(2).strip())
    return ts


def check(pdf_path, md_path):
    doc = pymupdf.open(pdf_path)
    problems = []
    cjk = 0
    total_pages = len(doc)

    for pno, page in enumerate(doc, 1):
        MARGIN_L, MARGIN_R, MARGIN_B = page_bounds(page)
        for blk in page.get_text("blocks"):
            x0, y0, x1, y1, txt = blk[0], blk[1], blk[2], blk[3], blk[4]
            t = txt.strip()
            if not t:
                continue
            # 页码由 pymupdf 后处理补在页脚，本就在页边距内，不算溢出
            if re.fullmatch(r"\d+\s*/\s*\d+", t):
                continue
            cjk += len(re.findall(r"[\u4e00-\u9fff]", txt))
            if x1 > MARGIN_R + TOL:
                problems.append("p%d 右侧溢出 x1=%.0f > %.0f :: %s"
                                % (pno, x1, MARGIN_R, txt.strip()[:40]))
            if x0 < MARGIN_L - TOL:
                problems.append("p%d 左侧溢出 x0=%.0f < %.0f :: %s"
                                % (pno, x0, MARGIN_L, txt.strip()[:40]))
            if y1 > MARGIN_B + 14:   # 页码在底部，留 14pt 余量
                problems.append("p%d 底部溢出 y1=%.0f > %.0f :: %s"
                                % (pno, y1, MARGIN_B, txt.strip()[:40]))

    full = "\n".join(page.get_text() for page in doc)

    # 中文渲染
    if cjk < 500:
        problems.append("中文字符仅 %d 个，疑似未渲染（字体缺失）" % cjk)

    # 字体嵌入
    fonts = set()
    for page in doc:
        for f in page.get_fonts(full=True):
            fonts.add(f[3])
    embedded = [f for f in fonts if "Noto" in f or "YaHei" in f
                or "Hei" in f or "Song" in f or "Ming" in f]
    if not embedded:
        problems.append("未检测到嵌入的中文字体，fonts=%s" % list(fonts)[:5])

    # 页码
    last = doc[total_pages - 1].get_text()
    if "%d / %d" % (total_pages, total_pages) not in last:
        problems.append("末页未找到页码 %d / %d" % (total_pages, total_pages))

    # 标题完整性：md 里的标题文本应能在 PDF 中找到。
    # 注意 PDF 里标题常因折行被切断，比较前必须抹掉所有空白。
    if md_path and os.path.exists(md_path):
        norm_full = re.sub(r"\s+", "", full)
        miss = []
        for t in md_titles(md_path):
            core = re.sub(r"[*`]", "", t).strip()
            probe = core.split("｜")[0].strip()
            if len(probe) > 3 and re.sub(r"\s+", "", probe) not in norm_full:
                miss.append(probe)
        if miss:
            problems.append("标题缺失 %d 个: %s" % (len(miss), miss[:6]))

    # 图：md 里的代码围栏应变成位图；图片引用若是 SVG 则内联（无位图，
    # 只能用「SVG 里的文字是否出现在 PDF 文本层」来验证确实渲染了）
    fig_expected = md_fig_count(md_path) if md_path else 0
    fig_actual = sum(len(page.get_images()) for page in doc)
    if fig_expected and fig_actual < fig_expected:
        problems.append("ASCII 图缺失：应有 %d 张，实际 %d 张"
                        % (fig_expected, fig_actual))

    norm_full = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", full)
    n_svg = 0
    for alt, rel in md_images(md_path):
        p = os.path.normpath(os.path.join(os.path.dirname(md_path), rel))
        if not p.lower().endswith(".svg"):
            continue
        if not os.path.exists(p):
            problems.append("SVG 文件不存在: %s" % rel)
            continue
        texts = [t for t in svg_texts(p) if len(t) >= 6]
        if not texts:
            problems.append("SVG 无文字内容: %s" % rel)
            continue
        probe = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", max(texts, key=len))
        if probe[:24] in norm_full:
            n_svg += 1
        else:
            problems.append("SVG 未渲染进 PDF: %s" % rel)
    fig_actual += n_svg

    doc.close()
    return total_pages, cjk, len(embedded), fig_actual, problems


def main():
    key = sys.argv[1].lower() if len(sys.argv) > 1 else None
    pdfs = sorted(glob.glob(os.path.join(PDF_DIR, "Ch*.pdf")))
    if key:
        pdfs = [p for p in pdfs if key in os.path.basename(p).lower()]
    if not pdfs:
        raise SystemExit("没有可校验的 PDF")

    bad = 0
    for p in pdfs:
        base = os.path.basename(p)
        m = re.match(r"^(Ch\d\d)_", base)
        md = None
        if m:
            cand = glob.glob(os.path.join(CHAPTERS, m.group(1) + "_*.md"))
            md = cand[0] if cand else None
        pages, cjk, nfont, nfig, probs = check(p, md)
        flag = "OK " if not probs else "!! "
        if probs:
            bad += 1
        print("%s%-52s %2d页 中文%5d字 图%2d张 字体%d"
              % (flag, base, pages, cjk, nfig, nfont))
        for x in probs:
            print("     - " + x)
    print("\n合计 %d 个文件，%d 个有问题" % (len(pdfs), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
