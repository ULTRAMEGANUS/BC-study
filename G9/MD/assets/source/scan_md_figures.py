# -*- coding: utf-8 -*-
"""
scan_md_figures.py —— 扫出 md 里残留的 ASCII 字符画代码块

用法：
    python scan_md_figures.py            # 扫 chapters/ + appendices/
    python scan_md_figures.py chapters   # 只扫某一目录

输出每个代码块的 序号 / 行号范围 / 是否为 ASCII 图 / 首行内容。
**替换前必须先跑这个**——块序号会随替换漂移，靠手数 fence 行必错
（有缩进的 ``` 会被 `grep -c '^\`\`\`'` 漏掉）。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(os.path.dirname(HERE))          # assets/source -> G9/MD

# ASCII 字符画用的制表符（全角/半角都算）
BOX_CHARS = "─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬►▼●○◆◇■□-_/\\|=+*·"
# 判定为"图"而非"公式/文字"：制表符达到一定密度
BOX_RE = re.compile("[─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬]")


def blocks(lines):
    """返回 [(start, end)]，闭区间，含首尾 ``` 行。兼容缩进的围栏。"""
    out, st, inb = [], 0, False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            if inb:
                out.append((st, i))
            else:
                st = i
            inb = not inb
    return out


def is_figure(body):
    n_box = len(BOX_RE.findall(body))
    if n_box >= 3:
        return True
    # 没有制表符但用了纯 ASCII 拼的框（+---+ / |   |）
    rows = [l for l in body.split("\n") if l.strip()]
    if len(rows) >= 3:
        boxy = sum(1 for l in rows
                   if re.match(r'^\s*[\+\|][-\+\|\s]*[\+\|]\s*$', l))
        if boxy >= 2:
            return True
    return False


def scan_dir(d):
    for name in sorted(os.listdir(d)):
        if not name.endswith(".md"):
            continue
        p = os.path.join(d, name)
        lines = open(p, encoding="utf-8").read().split("\n")
        bs = blocks(lines)
        n_fig = 0
        print("===== %s （代码块 %d 个）=====" % (name, len(bs)))
        for k, (st, en) in enumerate(bs, 1):
            body = "\n".join(lines[st + 1:en])
            if is_figure(body):
                n_fig += 1
                print("  [图] 块%-3d 行%-5d-%-5d %s"
                      % (k, st + 1, en + 1, lines[st + 1].strip()[:50]))
            else:
                print("       块%-3d 行%-5d-%-5d %s"
                      % (k, st + 1, en + 1,
                         (lines[st + 1].strip() or "（空）")[:50]))
        print("  → ASCII 图 %d 个\n" % n_fig)
        yield name, len(bs), n_fig


def main():
    args = sys.argv[1:] or ["chapters-cn", "appendices-cn", "chapters-en"]
    total = 0
    for a in args:
        d = os.path.join(MD, a)
        if not os.path.isdir(d):
            print("目录不存在:", d)
            continue
        for _, _, nf in scan_dir(d):
            total += nf
    print("合计待换 ASCII 图：%d 个" % total)


if __name__ == "__main__":
    main()
