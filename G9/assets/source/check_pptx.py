# -*- coding: utf-8 -*-
"""静态校验生成的 pptx：越界、文本溢出、空页、页数分布。

本机没有 PowerPoint / LibreOffice，无法真实渲染，只能按 python-pptx 的
形状几何 + 文本量估算来体检。估算沿用 build_pptx 的宽度模型。

    python check_pptx.py <file.pptx>
"""
import sys, math, os
from pptx import Presentation
from pptx.util import Emu

EMU = 914400.0
SW, SH = 13.333, 7.5
FOOT_Y = 7.02


def is_cjk(ch):
    return ch in "，。、；：？！「」『』（）《》—…·" or \
        (0x2E80 <= ord(ch) <= 0x9FFF) or (0x3000 <= ord(ch) <= 0x303F) \
        or (0xFF00 <= ord(ch) <= 0xFFEF)


def em_width(s):
    return sum(1.0 if is_cjk(c) else 0.55 for c in s)


def est_h(text, w_in, size, gap=1.30):
    cap = (w_in * 72.0) / max(size, 1.0)
    tot = 0.0
    for line in text.split("\n"):
        em = em_width(line)
        rows = max(1, math.ceil(em / cap - 1e-9)) if em > 0 else 1
        tot += rows * size * gap
    return tot / 72.0


def frame_text(tf):
    return "\n".join(p.text for p in tf.paragraphs)


def est_frame(tf, w_in):
    """逐段估算：每段用自己的字号，不能拿全框最大字号去算所有文字。"""
    total = 0.0
    for p in tf.paragraphs:
        txt = p.text
        if not txt.strip():
            total += 0.12
            continue
        sizes = [r.font.size.pt for r in p.runs if r.font.size]
        size = max(sizes) if sizes else 12
        total += est_h(txt, w_in, size)
    return total


def max_size(tf):
    sizes = [r.font.size.pt for p in tf.paragraphs for r in p.runs if r.font.size]
    return max(sizes) if sizes else 12


def main(path):
    prs = Presentation(path)
    print("文件：%s" % path)
    print("尺寸：%.3f x %.3f in" % (prs.slide_width / EMU, prs.slide_height / EMU))
    print("页数：%d" % len(prs.slides))
    print("=" * 72)

    problems = []
    for idx, slide in enumerate(prs.slides, 1):
        shapes = list(slide.shapes)
        texts = []
        for sh in shapes:
            try:
                top, left = sh.top / EMU, sh.left / EMU
                h, w = sh.height / EMU, sh.width / EMU
            except Exception:
                continue

            if top < -0.02 or left < -0.02:
                problems.append((idx, "超出页面左上", "top=%.2f left=%.2f" % (top, left)))
            if top + h > SH + 0.03:
                problems.append((idx, "超出页面底部", "bottom=%.2f > %.2f" % (top + h, SH)))
            if left + w > SW + 0.03:
                problems.append((idx, "超出页面右侧", "right=%.2f > %.2f" % (left + w, SW)))

            if sh.has_text_frame and frame_text(sh.text_frame).strip():
                txt = frame_text(sh.text_frame)
                need = est_frame(sh.text_frame, w)
                if need > h + 0.08:
                    problems.append((idx, "文本超出文本框",
                                     "需 %.2fin / 框 %.2fin（最大 %dpt, %.0f 字）"
                                     % (need, h, max_size(sh.text_frame), len(txt))))
                texts.append(txt)
            if sh.has_table:
                tb = sh.table
                th = sum(r.height for r in tb.rows) / EMU
                if top + th > SH + 0.03:
                    problems.append((idx, "表格超出页面", "bottom=%.2f" % (top + th)))
                if top + th > FOOT_Y + 0.02:
                    problems.append((idx, "表格压到页脚", "bottom=%.2f" % (top + th)))
                texts.append(" ".join(c.text for r in tb.rows for c in r.cells))

        joined = " ".join(texts).strip()
        head = joined[:46].replace("\n", " ")
        print("P%02d  %-46s  %4d字" % (idx, head, len(joined)))

    print("=" * 72)
    if problems:
        print("发现问题 %d 处：" % len(problems))
        for idx, kind, msg in problems:
            print("  P%02d  %-16s %s" % (idx, kind, msg))
    else:
        print("未发现越界/溢出问题。")
    return len(problems)


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1]) == 0 else 1)
