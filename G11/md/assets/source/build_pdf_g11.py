# -*- coding: utf-8 -*-
"""build_pdf_g11.py —— G11 章节 md → A4 PDF（打印用）

与 preview_md.py 的分工：
  - preview_md.py  连续长页 + <img src>，给屏幕上 mdview 观感用；
  - 本脚本          A4 分页 + SVG 内联 + 页码 + 书签，给打印/发给学生用。

关键点（踩过的坑，勿删）：
1. SVG 必须**内联**，不能用 <img src>。Chrome 会把 <img> 里的 SVG 栅格化，
   SVG 内的中文文字层就没了，复制/搜索全失效。
2. 内联时要给每个图内部的 id 加前缀（marker/gradient 的 id 是文档级全局的，
   多图同页会互相顶掉），并去掉根节点 width/height 交给 CSS 缩放。
3. 二级列表在 md 里是「两格缩进」（  - **中文**：…），Python-Markdown 默认
   tab_length=4 会把它们并进上一条，必须先补成四格。
4. Chrome 用系统 ANSI 代码页解析命令行，非 ASCII 输出路径会被静默丢弃
   （照样打印 "bytes written"，文件却不存在）。先写 ASCII 临时名再 os.replace。

用法：
    python build_pdf_g11.py 1 2 3        # 只做 Ch.1–Ch.3
    python build_pdf_g11.py all          # 全部章节
    python build_pdf_g11.py 1 --keep-html
"""
import os
import re
import sys
import glob
import ctypes
import shutil
import subprocess
import tempfile

import markdown


def _import_pymupdf():
    """导入 pymupdf。

    2026-11-15 起本机 System32 缺 msvcp140.dll（只剩 CLR 变体），pymupdf 的
    mupdfcpp64.dll 一加载就报 "DLL load failed"。系统里其它程序（Edge/Chrome）
    自带一份，先把它 ctypes 预加载进来即可，不用装 VC 运行库、不用改系统。
    """
    try:
        import pymupdf
        return pymupdf
    except ImportError:
        pass
    pats = [r"C:/Program Files (x86)/Microsoft/Edge/Application/*/msvcp140.dll",
            r"C:/Program Files/Microsoft/Edge/Application/*/msvcp140.dll",
            r"C:/Program Files/Google/Chrome/Application/*/msvcp140.dll",
            r"C:/Program Files/Java/*/bin/msvcp140.dll"]
    for pat in pats:
        for dll in glob.glob(pat):
            try:
                ctypes.CDLL(dll)
                import pymupdf
                return pymupdf
            except OSError:
                continue
    raise SystemExit("pymupdf 无法加载，且未找到可用的 msvcp140.dll")


pymupdf = _import_pymupdf()

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(os.path.dirname(HERE))          # assets/source -> G11/md
G11 = os.path.dirname(MD)
SRC = os.path.join(MD, "chapters-en")
OUT = os.path.join(G11, "pdf", "EN")

CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { size: A4; margin: 16mm 14mm 14mm 14mm; }
* { box-sizing: border-box; }
body {
  font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
  font-size: 9.9pt; line-height: 1.55; color: #1A202C; margin: 0;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
h1 {
  font-size: 18pt; line-height: 1.25; margin: 0 0 2pt; color: #0B3D66;
  font-weight: 700; letter-spacing: -.2pt;
}
p.subtitle {
  font-size: 10.5pt; color: #5A6675; margin: 0 0 8pt; padding-bottom: 6pt;
  border-bottom: 1.6pt solid #0B3D66; font-weight: 500;
}
h2 {
  font-size: 13pt; margin: 15pt 0 6pt; color: #0B3D66; font-weight: 700;
  padding-left: 7pt; border-left: 3.5pt solid #2B6CB0;
  page-break-after: avoid;
}
h3 { font-size: 10.6pt; margin: 11pt 0 4pt; color: #234E70;
     font-weight: 700; page-break-after: avoid; }
h4 { font-size: 9.9pt; margin: 9pt 0 3pt; font-weight: 700; color: #2D3748;
     page-break-after: avoid; }
p { margin: 0 0 5pt; }
ul, ol { margin: 0 0 6pt; padding-left: 15pt; }
li { margin: 1pt 0; }
li > ul, li > ol { margin: 1.5pt 0 1.5pt; }
strong { color: #0F2540; }
code {
  font-family: Consolas, "Cascadia Mono", monospace; font-size: 8.7pt;
  background: #EEF2F6; padding: .5pt 2.5pt; border-radius: 2pt; color: #1A365D;
}
blockquote {
  margin: 6pt 0 8pt; padding: 5pt 8pt; background: #F7FAFC;
  border-left: 3pt solid #A0AEC0; font-size: 9.1pt; color: #2D3748;
  page-break-inside: avoid;
}
blockquote p { margin: 0 0 2.5pt; }
blockquote p:last-child { margin-bottom: 0; }
hr { border: 0; border-top: .8pt solid #CBD5E0; margin: 10pt 0; }
table {
  border-collapse: collapse; width: 100%; font-size: 8.5pt; line-height: 1.42;
  margin: 5pt 0 9pt; table-layout: auto;
}
thead { display: table-header-group; }
th, td {
  border: .6pt solid #B9C6D4; padding: 3pt 5pt; vertical-align: top;
  word-wrap: break-word; overflow-wrap: anywhere;
}
th { background: #E8EEF5; font-weight: 700; color: #0B3D66; }
tr { page-break-inside: avoid; }
tbody tr:nth-child(even) { background: #FAFCFE; }
figure {
  margin: 7pt 0 9pt; text-align: center; page-break-inside: avoid;
}
figure svg {
  width: 100%; height: auto;
  border: .6pt solid #CBD5E0; border-radius: 3pt; background: #fff;
}
figcaption { font-size: 8.2pt; color: #5A6675; margin-top: 3pt; }
.section-break { page-break-before: always; }
"""


# ---------------------------------------------------------------- 预处理

def find_chrome():
    for p in CHROME:
        if os.path.exists(p):
            return p
    raise SystemExit("未找到 Chrome / Edge")


def preprocess(text):
    """规范化 md，避免渲染器错判。"""
    lines = text.split("\n")
    out = []
    for ln in lines:
        # 1) 二级列表两格 → 四格（Python-Markdown tab_length=4）
        if re.match(r"^ {2}- ", ln) and not ln.startswith("    "):
            ln = "    " + ln[2:]
        # 2) 章副标题降级为段落，避免与 h2 视觉冲突
        m = re.match(r"^## (Chapter \d+ · .*)$", ln)
        if m:
            ln = '<p class="subtitle" markdown="1">%s</p>' % m.group(1)
        out.append(ln)
    return "\n".join(out)


def extract_figures(text):
    """把 ![](path) 换成占位符，返回 (新文本, [(占位符, 路径, alt)])。"""
    figs = []

    def rep(m):
        alt, path = m.group(1), m.group(2)
        key = "@@FIG%d@@" % len(figs)
        figs.append((key, path, alt))
        return key
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", rep, text), figs


MAX_FIG_H = 360          # pt；高图限高，防止整块被 avoid 顶到下页留半页空白
CONTENT_W = 516          # pt；A4 内容栏宽（210mm - 28mm 边距）


def inline_svg(path, key):
    """读 SVG、去根尺寸、给内部 id 加前缀，按 viewBox 限高，返回 figure HTML。"""
    with open(path, encoding="utf-8") as fh:
        svg = fh.read()
    svg = re.sub(r"^<\?xml[^>]*\?>\s*", "", svg)
    # 每个图的 id 加前缀（marker/gradient 是文档级全局）
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = svg.replace('id="%s"' % i, 'id="%s-%s"' % (key, i))
        svg = svg.replace("url(#%s)" % i, "url(#%s-%s)" % (key, i))
    # 去掉根节点写死的宽高，交给 CSS
    svg = re.sub(r"(<svg\b[^>]*?)\swidth=\"[^\"]*\"", r"\1", svg, count=1)
    svg = re.sub(r"(<svg\b[^>]*?)\sheight=\"[^\"]*\"", r"\1", svg, count=1)
    # 按 viewBox 算限高宽度（确定性写进 style，不指望 CSS max-height 对 SVG 生效）
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    style = ""
    if m:
        w, h = float(m.group(1)), float(m.group(2))
        full_h = CONTENT_W * h / w
        if full_h > MAX_FIG_H:
            style = ' style="width:%dpt;max-width:100%%"' % (MAX_FIG_H * w / h)
    return '<figure>%s</figure>' % (svg.replace("<svg ", "<svg%s " % style, 1))


def slug(t):
    t = re.sub(r"<[^>]+>", "", t).strip().lower()
    t = re.sub(r"[^\w\u4e00-\u9fff\s-]", "", t)
    return re.sub(r"\s+", "-", t).strip("-") or "s"


# ---------------------------------------------------------------- 渲染

def convert(md_path, keep_html=False):
    with open(md_path, encoding="utf-8") as fh:
        src = fh.read()

    heads = [(len(m.group(1)), m.group(2).strip())
             for m in re.finditer(r"^(#{1,2}) (.+)$", src, re.M)]

    body_src, figs = extract_figures(src)
    body_src = preprocess(body_src)

    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list",
                                       "sane_lists", "nl2br"],
                           output_format="html5")
    body = md.convert(body_src)

    # 图片占位符 → 内联 SVG
    # ⚠ id 前缀不能用占位符本身：占位符（@@FIG1@@）替换后再扫一遍正文时，
    #   会把已插入 SVG 内部的同名字符串又替换成整张 SVG，无限膨胀。
    base = os.path.dirname(os.path.abspath(md_path))
    for idx, (key, path, alt) in enumerate(figs):
        ab = os.path.normpath(os.path.join(base, path))
        if os.path.exists(ab):
            svg = inline_svg(ab, "f%d" % idx)
        else:
            svg = '<p style="color:#C53030">[缺图 %s]</p>' % path
        body = body.replace("<p>%s</p>" % key, svg)
        if key in body:
            body = body.replace(key, svg)   # 占位符不在独立段落里的兜底
        assert key not in body, "占位符未消干净：%s" % key

    # 给 h1/h2 加 id，供 PDF 书签与页内跳转
    body = re.sub(r"<h([12])>(.*?)</h\1>",
                  lambda m: '<h%s id="%s">%s</h%s>'
                  % (m.group(1), slug(m.group(2)), m.group(2), m.group(1)),
                  body, flags=re.S)

    title = heads[0][1] if heads else os.path.basename(md_path)
    doc = ("<!DOCTYPE html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
           "<title>%s</title><style>%s</style></head>\n<body>\n%s\n</body></html>\n"
           % (title, CSS, body))
    return doc, heads


def print_pdf(html_path, pdf_path, chrome):
    dst_dir = os.path.dirname(os.path.abspath(pdf_path))
    os.makedirs(dst_dir, exist_ok=True)
    tmp = os.path.join(dst_dir, "_tmp_g11.pdf")
    if os.path.exists(tmp):
        os.remove(tmp)
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
           "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
           "--virtual-time-budget=20000",
           "--print-to-pdf=" + tmp.replace("\\", "/"),
           "file:///" + os.path.abspath(html_path).replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if not os.path.exists(tmp):
        raise SystemExit("渲染失败：%s\n%s" % (html_path, r.stdout[-500:] + r.stderr[-500:]))
    os.replace(tmp, pdf_path)
    return os.path.getsize(pdf_path)


def finish(pdf_path, heads):
    """加页码 + 书签。"""
    doc = pymupdf.open(pdf_path)
    n = doc.page_count
    for i, page in enumerate(doc):
        w, h = page.rect.width, page.rect.height
        page.insert_text((w / 2 - 14, h - 22), "%d / %d" % (i + 1, n),
                         fontsize=8, fontname="helv", color=(0.42, 0.46, 0.5))
    norm = [re.sub(r"\s+", "", p.get_text()) for p in doc]
    toc, cur, miss = [], 0, []
    for lvl, text in heads:
        key = re.sub(r"\s+", "", text)
        page = next((i for i in range(cur, n) if key in norm[i]), None)
        if page is None:
            page = next((i for i in range(n) if key in norm[i]), None)
        if page is None:
            miss.append(text)
            continue
        cur = page
        toc.append([lvl, text, page + 1])
    doc.set_toc(toc)
    tmp = pdf_path + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, pdf_path)
    return n, len(toc), miss


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keep = "--keep-html" in sys.argv
    files = sorted(glob.glob(os.path.join(SRC, "Ch*.md")))
    if args and args[0] != "all":
        # 用 "Ch%02d_" 精确前缀，否则 "1" 会连带命中 Ch10–Ch14
        keys = ["Ch%02d_" % int(k) for k in args]
        files = [f for f in files
                 if any(os.path.basename(f).startswith(k) for k in keys)]
    if not files:
        raise SystemExit("没有匹配的章节")
    chrome = find_chrome()
    print("renderer:", os.path.basename(chrome), "| 输出:", OUT)
    tmpdir = tempfile.mkdtemp(prefix="g11pdf_")
    try:
        for f in files:
            name = os.path.splitext(os.path.basename(f))[0]
            doc, heads = convert(f)
            html_path = os.path.join(tmpdir, name + ".html")
            with open(html_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(doc)
            pdf = os.path.join(OUT, name + ".pdf")
            size = print_pdf(html_path, pdf, chrome)
            pages, ntoc, miss = finish(pdf, heads)
            flag = "" if not miss else "  ⚠ 缺书签 %d: %s" % (len(miss), miss[:3])
            print("OK  %-52s %3d 页 %6.0f KB  书签 %d/%d%s"
                  % (name[:52], pages, size / 1024, ntoc, len(heads), flag))
            if keep:
                keepdir = os.path.join(G11, "pdf", "_html")
                os.makedirs(keepdir, exist_ok=True)
                shutil.copy(html_path, os.path.join(keepdir, name + ".html"))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
