# -*- coding: utf-8 -*-
"""把 G9/pdf/CN/ 下 11 章 PDF 合并成 G9-combo.pdf，并从 md 标题重建书签（outline）。

Chrome headless 打印出的 PDF **不带书签**，所以书签要从源头重建：
  1. 读每章 md，抽出 # / ## / ### 标题（跳过代码块内的 #）；
  2. 合并 PDF 后，在「该章页范围」内逐页搜标题文本，定位页码；
  3. 用 doc.set_toc() 写入三级书签。

用法（在 assets/source 下）：
    env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_combo_pdf.py
    env -u ... "$PY" build_combo_pdf.py --maxlevel 2        # 只做「章 / 节」两级
    env -u ... "$PY" build_combo_pdf.py --src appendices-cn \
        --pattern 'Appendix*.pdf'                         # 合并附录册 → pdf/CN/appendix-combo-cn.pdf
    env -u ... "$PY" build_combo_pdf.py --src chapters-en --out ../../pdf/EN/G9-combo-en.pdf

合并前要先有各篇的 PDF：章节由 build_chapter_pdf.py 生成，
附录用 `build_chapter_pdf.py --src appendices-cn` 生成。
"""
import os
import re
import sys
import glob
import datetime

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))       # .../G9/MD/assets/source
ASSETS = os.path.dirname(HERE)
MD = os.path.dirname(ASSETS)                            # .../G9/MD
G9 = os.path.dirname(MD)                                # .../G9
PDF_DIR = os.path.join(G9, "pdf")
MD_DIRS = [os.path.join(MD, "chapters-cn"), os.path.join(MD, "appendices-cn")]
OUT = os.path.join(PDF_DIR, "CN", "G9-combo.pdf")


# ---------------------------------------------------------------- 标题提取
def display_md(s):
    """书签里显示的文字：去 markdown 标记，但保留正常空格"""
    s = re.sub(r'^#+\s*', '', s).strip()
    s = s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    s = s.replace('**', '').replace('`', '')
    s = re.sub(r'\s+', ' ', s)
    return s


def strip_md(s):
    """用于匹配的文字：再去掉所有空白（PDF 文本层里标题可能被换行切断）"""
    s = display_md(s)
    s = re.sub(r'\s+', '', s)
    return s


def md_headings(md_path, maxlevel=3):
    """返回 [(level, 显示文字, 匹配文字)]，跳过围栏代码块内的 #。

    显示文字保留空格与 emoji（书签里要好看），匹配文字去掉所有空白
    （PDF 文本层里标题常被换行切断，逐字比对会漏）。
    """
    out = []
    in_fence = False
    for ln in open(md_path, encoding='utf-8').read().split('\n'):
        s = ln.strip()
        if s.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r'^(#{1,3})\s+(.*)$', s)
        if not m:
            continue
        lvl = len(m.group(1))
        if lvl > maxlevel:
            continue
        raw = m.group(2).strip()
        if not raw:
            continue
        out.append((lvl, display_md(raw), strip_md(raw)))
    return out


# ---------------------------------------------------------------- 页码定位
def page_text_norm(doc, pno):
    """页文本去掉所有空白（含页内换行），用于子串匹配"""
    return re.sub(r'\s+', '', doc[pno].get_text())


def split_across(t, nxt, norm):
    """标题是否被分页切断：前缀落在 t 末尾、后缀落在 nxt 开头。

    注意：不能简单地用 `norm in t + nxt` 判定——只要标题完整出现在下一页，
    拼上前一页文本后也必然「命中」，会把所有标题整体拉前一页（实测全错一页）。
    """
    if not nxt:
        return False
    for k in range(1, len(norm)):
        if t.endswith(norm[:k]) and nxt.startswith(norm[k:]):
            return True
    return False


def locate(doc, heads, start, end, cache):
    """在 [start, end] 页内按出现顺序定位每个标题的页码。

    cache: {pno: 归一化文本}。标题可能被分页切断，故用「本页 + 下一页」拼接匹配。
    """
    toc = []
    cursor = start
    hit = miss = 0
    for i, (lvl, raw, norm) in enumerate(heads):
        if not norm:
            continue
        found = None
        for p in range(cursor, end + 1):
            t = cache.get(p)
            if t is None:
                t = page_text_norm(doc, p)
                cache[p] = t
            if norm in t:
                found = p
                break
            if p < end:
                n2 = cache.get(p + 1)
                if n2 is None:
                    n2 = page_text_norm(doc, p + 1)
                    cache[p + 1] = n2
                if split_across(t, n2, norm):        # 真被切断才算命中本页
                    found = p
                    break
        if found is None:
            miss += 1
            print('    ⚠ 未定位：%-52s → 跳过' % raw[:52])
            continue
        hit += 1
        cursor = found
        toc.append((i, lvl, raw, found + 1))         # set_toc 用 1-based 页码
    return toc, hit, miss


# ---------------------------------------------------------------- 主流程
def doc_label(md_path):
    """顶层书签文字。

    章节 md 开头是「# Ch.2 — English」+「## 第 2 章　中文名」，两条指向同一页，
    合成一条「Ch.2 · 元素、元素符号与元素周期表」；
    附录 md 开头是「# 附录 A — Glossary 词汇总表｜…」+ 副标题，h1 本身就是中文标题，
    直接取 h1 截到「｜」之前即可。
    """
    heads = md_headings(md_path, maxlevel=2)
    h1 = next((raw for lvl, raw, _ in heads if lvl == 1), '')
    h2 = next((raw for lvl, raw, _ in heads if lvl == 2), '')
    if re.search(r'[一-鿿]', h1):                     # h1 已是中文标题
        return h1.split('｜')[0].strip() or h1
    m = re.search(r'Ch\.\s*\d+', h1)
    tag = m.group(0) if m else ''
    # 英文版 h2 形如「Chapter 2 · Elements…｜第 2 章　元素…」：拆成两段各清一次前缀
    if '｜' in h2:
        en, zh = h2.split('｜', 1)
        en = re.sub(r'^Chapter\s*\d+\s*[·\-–—]?\s*', '', en.strip())
        zh = re.sub(r'^第\s*[^章]*章[　\s]*', '', zh.strip())
        body = '%s｜%s' % (en, zh) if zh else en
    else:
        body = re.sub(r'^第\s*[^章]*章[　\s]*', '', h2)
    if tag and body:
        return '%s · %s' % (tag, body)
    return h1 or h2 or os.path.splitext(os.path.basename(md_path))[0]


def first_h2_index(heads):
    """返回第一个 ## 标题的下标（它就是中文章名，要和 level-1 去重）"""
    for i, (lvl, _, _) in enumerate(heads):
        if lvl == 2:
            return i
    return None


def main():
    argv = sys.argv[1:]
    maxlevel = 3
    out = None
    src = 'chapters-cn'              # md 所在目录（G9/MD 下的子目录名）
    pattern = 'Ch*.pdf'              # 参与合并的 PDF 文件名模式
    if '--maxlevel' in argv:
        maxlevel = int(argv[argv.index('--maxlevel') + 1])
    if '--out' in argv:
        out = argv[argv.index('--out') + 1]
    if '--src' in argv:
        src = argv[argv.index('--src') + 1]
    if '--pattern' in argv:
        pattern = argv[argv.index('--pattern') + 1]

    _s = src.lower()
    is_appx = 'append' in _s
    is_en = _s.endswith('-en') or _s in ('en', 'chapters-en', 'appendices-en')
    if out is None:
        sub = 'EN' if is_en else 'CN'
        out = os.path.join(PDF_DIR, sub,
                           'appendix-combo-%s.pdf' % sub.lower() if is_appx
                           else 'G9-combo-%s.pdf' % sub.lower())
    md_dir = src if os.path.isabs(src) else os.path.join(MD, src)
    # 中/英文版各章 PDF 同名，必须分开存放：pdf/CN/ 与 pdf/EN/
    pdf_dir = os.path.join(PDF_DIR, 'EN') if is_en else os.path.join(PDF_DIR, 'CN')
    if is_en:
        MD_DIRS.insert(0, md_dir)

    pdfs = sorted(glob.glob(os.path.join(pdf_dir, pattern)))
    # 排除上一轮的输出，避免自我合并
    pdfs = [p for p in pdfs if 'combo' not in os.path.basename(p).lower()]
    if not pdfs:
        raise SystemExit('没找到待合并的 PDF：%s / %s' % (PDF_DIR, pattern))

    print('待合并 %d 个文档：' % len(pdfs))
    for p in pdfs:
        print('   ', os.path.basename(p))

    combo = pymupdf.open()
    toc = []
    cache = {}
    total_hit = total_miss = 0
    chapter_starts = []                                        # 每章首页（0-based）

    for pdf_path in pdfs:
        base = os.path.basename(pdf_path)[:-4]                 # 去掉 .pdf
        md_path = os.path.join(md_dir, base + '.md')
        if not os.path.exists(md_path):      # 回退：在 chapters / appendices 里找同名 md
            for d in MD_DIRS:
                p = os.path.join(d, base + '.md')
                if os.path.exists(p):
                    md_path = p
                    break
        name = os.path.basename(pdf_path)

        doc = pymupdf.open(pdf_path)
        offset = combo.page_count                              # 本册首页在合并后的 0-based 序号
        combo.insert_pdf(doc)
        first, last = offset, combo.page_count - 1
        chapter_starts.append(first)

        if not os.path.exists(md_path):
            print('  ⚠ %s 没有对应 md，只有顶层书签' % name)
            toc.append([1, base, first + 1])
            doc.close()
            continue

        heads = md_headings(md_path, maxlevel=maxlevel)
        sub, hit, miss = locate(combo, heads, first, last, cache)
        total_hit += hit
        total_miss += miss

        # 顶层 level-1：把指向同一页的中英文标题并成一条
        skip = {i for i, (lvl, _, _) in enumerate(heads) if lvl == 1}
        fi = first_h2_index(heads)
        if fi is not None:
            skip.add(fi)

        toc.append([1, doc_label(md_path), first + 1])
        for i, lvl, raw, pno in sub:
            if i in skip:
                continue
            toc.append([lvl, raw, pno])

        print('   ✓ %-46s %2d页  标题%2d（命中%d 未定位%d）'
              % (name[:46], last - first + 1, len(heads), hit, miss))
        doc.close()

    combo.set_toc(toc)

    # 页标签：每章从 1 重新编号，让书签显示的页码与页脚「3 / 16」一致
    label_note = ''
    try:
        combo.set_page_labels([{'startpage': s, 'prefix': '', 'style': 'D',
                                'firstpagenum': 1} for s in chapter_starts])
        label_note = '（页标签已按文档重置，与页脚编号一致）'
    except Exception as e:                                     # 老版本 pymupdf 不支持则忽略
        label_note = '（页标签设置失败，已跳过：%s）' % e
    combo.set_metadata({
        'title': ('BC Science 9 · Chemistry Unit · 附录合订本（Appendices A–E）'
                  if is_appx else
                  'BC Science 9 · Chemistry Unit · English–Chinese Handout, '
                  'English-first Edition（全册合订本 · 英文在前）' if is_en else
                  'BC Science 9 · Chemistry Unit · 英中对照讲义（全册合订本）'),
        'author': 'BC Science 9 Bilingual Handout',
        'subject': ('G9 Chemistry Unit — appendices combined' if is_appx else
                    'G9 Chemistry Unit — 11 chapters, English-primary' if is_en
                    else 'G9 Chemistry Unit — 11 chapters combined'),
        'keywords': 'BC Science 9, chemistry, bilingual, 英中对照',
        'creator': 'build_combo_pdf.py',
        'creationDate': datetime.datetime.now().strftime('D:%Y%m%d%H%M%S'),
    })
    combo.save(out, garbage=4, deflate=True)
    combo.close()

    print('\n合并完成：%s' % out)
    print('  总页数 %d' % len(pymupdf.open(out)))
    print('  书签 %d 条（命中 %d / 未定位 %d）%s' % (len(toc), total_hit, total_miss, label_note))
    lv = {}
    for t in toc:
        lv[t[0]] = lv.get(t[0], 0) + 1
    print('  层级分布 %s' % dict(sorted(lv.items())))


if __name__ == '__main__':
    main()
