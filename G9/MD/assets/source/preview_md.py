# -*- coding: utf-8 -*-
"""
preview_md.py —— 把一份 md 渲染成 GitHub 风格的 HTML，用来**预览 mdview 里的实际观感**

为什么需要它：beautify_md.py 改的是 md 源码，效果要在渲染器里才看得见。
而本机没有装 mdview，所以这里用一份最小的 GitHub 风格 CSS（github-markdown-css 的
核心规则）离线渲染，尽可能接近 mdview / GitHub 的显示结果。

⚠️ 与 build_chapter_pdf.py 的区别（别混用）：
   - 那个是 A4 排版（分页、页眉页脚、SVG 内联、宽表横页），为打印服务；
   - 这个是**连续长页 + 图片走 <img src>** ，为屏幕阅读服务。

用法：
    python preview_md.py                     # 渲染 MD/ 下全部 → G9/preview/
    python preview_md.py Ch02                # 只渲染某一章（关键字匹配）
    python preview_md.py Ch02 AppendixC      # 多个
    python preview_md.py --open              # 渲染完用默认浏览器打开第一个
"""
import os
import re
import sys
import html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(os.path.dirname(HERE))               # assets/source -> G9/MD
G9 = os.path.dirname(MD)
PREVIEW = os.path.join(G9, "preview")

CSS = """
:root{--fg:#1f2328;--sub:#59636e;--line:#d1d9e0;--bg:#fff;--quote:#59636e;
--accent:#0969da;--code-bg:#f6f8fa;}
*{box-sizing:border-box}
body{margin:0 auto;padding:32px;max-width:900px;font:16px/1.7 -apple-system,
"Segoe UI","Microsoft YaHei",Helvetica,Arial,sans-serif;color:var(--fg);
background:var(--bg);-webkit-text-size-adjust:100%}
h1,h2,h3,h4{padding-bottom:.3em;border-bottom:1px solid var(--line);
margin-top:24px;margin-bottom:16px;font-weight:600;line-height:1.3}
h1{font-size:2em;margin-top:0}
h2{font-size:1.5em}
h3{font-size:1.25em}
h4{font-size:1em;border:0}
p{margin:0 0 16px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
ul,ol{padding-left:2em;margin:0 0 16px}
li{margin:.25em 0}
blockquote{margin:0 0 16px;padding:0 1em;color:var(--quote);
border-left:.25em solid var(--line)}
blockquote>*:last-child{margin-bottom:0}
hr{height:1px;border:0;background:var(--line);margin:24px 0}
table{border-collapse:collapse;display:block;width:max-content;max-width:100%;
overflow:auto;margin:0 0 16px}
th,td{padding:6px 13px;border:1px solid var(--line)}
th{background:var(--code-bg);font-weight:600}
tr:nth-child(2n){background:var(--code-bg)}
code{padding:.2em .4em;margin:0;font-size:85%;background:var(--code-bg);
border-radius:6px;font-family:ui-monospace,"Cascadia Code",Consolas,monospace}
pre{padding:16px;overflow:auto;font-size:85%;line-height:1.45;
background:var(--code-bg);border-radius:6px;margin:0 0 16px;
font-family:ui-monospace,"Cascadia Code",Consolas,monospace}
pre code{padding:0;background:none}
img{max-width:100%;border:1px solid var(--line);border-radius:6px;
margin:8px 0;background:#fff}
del{color:var(--sub)}
.task{-list-style:none;padding-left:0}
@media (prefers-color-scheme:dark){
:root{--fg:#e6edf3;--sub:#8b949e;--line:#30363d;--bg:#0d1117;
--quote:#8b949e;--accent:#58a6ff;--code-bg:#161b22}}
"""


def esc(s):
    return _html.escape(s, quote=False)


def inline(s):
    """行内 Markdown：代码 / 粗体 / 斜体 / 删除线 / 链接 / 图片"""
    out, i = [], 0
    pat = re.compile(
        r"(`[^`]+`)|(\*\*[^*]+\*\*)|(\*[^*]+\*)|(~~[^~]+~~)"
        r"|(!\[[^\]]*\]\([^)]*\))|(\[[^\]]*\]\([^)]*\))")
    for m in pat.finditer(s):
        if m.start() > i:
            out.append(esc(s[i:m.start()]))
        t = m.group(0)
        if t.startswith("`"):
            out.append("<code>%s</code>" % esc(t[1:-1]))
        elif t.startswith("**"):
            out.append("<strong>%s</strong>" % inline(t[2:-2]))
        elif t.startswith("~~"):
            out.append("<del>%s</del>" % inline(t[2:-2]))
        elif t.startswith("!["):
            mm = re.match(r"!\[([^\]]*)\]\(([^)]*)\)", t)
            out.append('<img src="%s" alt="%s">'
                       % (esc(mm.group(2)), esc(mm.group(1))))
        elif t.startswith("["):
            mm = re.match(r"\[([^\]]*)\]\(([^)]*)\)", t)
            out.append('<a href="%s">%s</a>'
                       % (esc(mm.group(2)), inline(mm.group(1))))
        else:
            out.append("<em>%s</em>" % inline(t[1:-1]))
        i = m.end()
    out.append(esc(s[i:]))
    return "".join(out)


def render(text):
    """极简 Markdown 渲染：够用就好（标题/段落/列表/引用/表格/代码块/hr）。"""
    lines = text.split("\n")
    out, i = [], 0
    para = []

    def flush():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para).strip()))
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()

        if s.startswith("```"):
            flush()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>%s</code></pre>" % esc("\n".join(buf)))
            continue

        if not s:
            flush()
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush()
            lv = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lv, inline(m.group(2)), lv))
            i += 1
            continue

        if re.match(r"^(---+|\*\*\*+)$", s):
            flush()
            out.append("<hr>")
            i += 1
            continue

        if s.startswith(">"):
            flush()
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>%s</blockquote>"
                       % render("\n".join(buf)))
            continue

        # 表格
        if s.startswith("|") and i + 1 < len(lines) \
                and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            flush()
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(s)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % inline(c) for c in head]
            t += ["</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join("<td>%s</td>" % inline(c)
                                          for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        if re.match(r"^[-*+]\s+", s) or re.match(r"^\d+\.\s+", s):
            flush()
            ordered = bool(re.match(r"^\d+\.\s+", s))
            items = []
            while i < len(lines):
                cur = lines[i].strip()
                mo = re.match(r"^(\d+\.)\s+(.*)$", cur) if ordered \
                    else re.match(r"^[-*+]\s+(.*)$", cur)
                if not mo:
                    break
                items.append(mo.group(2) if ordered else mo.group(1))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (
                tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            continue

        para.append(s)
        i += 1

    flush()
    return "\n".join(out)


def build(md_path, out_path):
    src = open(md_path, encoding="utf-8").read()
    body = render(src)
    name = os.path.basename(md_path)
    doc = ("<!DOCTYPE html>\n<html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
           "<title>%s</title><style>%s</style></head>\n<body>\n%s\n"
           "<hr><p style=\"color:#59636e;font-size:13px\">"
           "预览由 assets/source/preview_md.py 生成 · 用于查看 mdview 中的观感"
           "</p>\n</body></html>\n" % (esc(name), CSS, body))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8", newline="\n").write(doc)
    return out_path


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    open_it = "--open" in sys.argv
    keys = args or [None]
    made = []
    for d in ("chapters-cn", "appendices-cn", "chapters-en"):
        p = os.path.join(MD, d)
        if not os.path.isdir(p):
            continue
        for name in sorted(os.listdir(p)):
            if not name.endswith(".md"):
                continue
            if keys != [None] and not any(k in name for k in keys):
                continue
            out = build(os.path.join(p, name),
                        os.path.join(PREVIEW, name[:-3] + ".html"))
            made.append(out)
            print("OK ", os.path.basename(out))
    print("\n共 %d 个预览 → %s" % (len(made), PREVIEW))
    if open_it and made:
        os.startfile(made[0])


if __name__ == "__main__":
    main()
