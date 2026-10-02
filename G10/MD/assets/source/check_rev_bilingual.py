# -*- coding: utf-8 -*-
"""校验 _EN-CN.pdf：页数/尺寸、中文文本层、对照页溢出、答案页是否原样。

原件在 G10/CHEM10 rev/（REV），产物在 G10/pdf/（OUT）。
"""
import os, re
import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
G10 = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REV = os.path.join(G10, "CHEM10 rev")   # 原件（只读）
OUT = os.path.join(G10, "pdf")          # 产物
CJK = re.compile(r"[\u4e00-\u9fff]")

PAIRS = [("SCI 10 REV WORKSHEET 0 _merge.pdf", 2),
         ("SCI 10 REV WORKSHEET 1 _merge.pdf", 2),
         ("SCI 10 REV WORKSHEET 2 _merge.pdf", 2),
         ("SCI 10 REV WORKSHEET 3 _merge.pdf", 1)]

allok = True
for name, nq in PAIRS:
    out_name = os.path.splitext(name)[0] + "_EN-CN.pdf"
    doc = pymupdf.open(os.path.join(OUT, out_name))
    orig = pymupdf.open(os.path.join(REV, name))
    nans = orig.page_count - nq
    nbi = doc.page_count - nans
    print("=" * 74)
    print(f"{out_name} | 对照页 {nbi}（原件题目 {nq}）| 答案页 {nans} | 总 {doc.page_count}")
    issues = []
    if nbi != nq:
        issues.append(f"对照页数 {nbi} ≠ 原件题目页数 {nq}（有溢出/压缩）")
    for i, page in enumerate(doc):
        r = page.rect
        t = page.get_text("text")
        ncjk = len(CJK.findall(t))
        over = ""
        for b in page.get_text("blocks"):
            x0, y0, x1, y1 = b[:4]
            if x1 > r.width - 32 or y1 > r.height - 22:
                over = f"  ⚠溢出 {b[4][:34]!r} x1={x1:.0f} y1={y1:.0f}"
        kind = "对照页" if i < nbi else "答案页(原样)"
        print(f"  p{i+1} {r.width:.0f}x{r.height:.0f} {kind:<11} 中文={ncjk:3d} "
              f"chars={len(t):4d}{over}")
        if i < nbi:
            if ncjk < 20:
                issues.append(f"p{i+1} 中文过少({ncjk})")
            if over:
                issues.append(f"p{i+1} 内容溢出")
        else:
            if t.strip() != orig[nq + (i - nbi)].get_text("text").strip():
                issues.append(f"p{i+1} 与原件对应页文本不一致")
    print("  ->", "✅ PASS（0 问题）" if not issues else "❌ " + "; ".join(issues))
    allok &= not issues
    doc.close(); orig.close()
print("=" * 74)
print("总判定:", "✅ 4 份全部通过" if allok else "❌ 见上方问题")
