# -*- coding: utf-8 -*-
"""fix_table_delims.py —— 修复全库 md 表格「表头/分隔行列数不匹配」

背景：分隔行普遍比表头多 1 列（个别多 2 列）。python-markdown / GFM 要求
表头与分隔行列数一致，不一致时**整表拒渲染**，原样吐出竖线文本
（2026-11-01 Ch03 PDF 实测）。数据行经扫描全部与表头一致，
故修法 = 把分隔行按表头列数截断/补齐，保留原有对齐冒号。

用法：python fix_table_delims.py [--check]
"""
import re
import io
import os
import glob
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(os.path.dirname(HERE))
DIRS = [os.path.join(MD, "chapters-en"), os.path.join(MD, "appendices-en")]

DELIM = re.compile(r"^\|[\s:|-]+\|$")


def fix_delim(delim, n):
    """把分隔行调成 n 格，尽量保留每格的对齐冒号。"""
    cells = delim.strip().strip("|").split("|")
    keep = cells[:n]
    while len(keep) < n:
        keep.append("---")
    out = []
    for c in keep:
        c = c.strip()
        left = c.startswith(":")
        right = c.endswith(":") and len(c) > 1
        body = "-" * 3
        if left and right:
            out.append(":---:")
        elif left:
            out.append(":---")
        elif right:
            out.append("---:")
        else:
            out.append(body)
    return "|" + "|".join(out) + "|"


def main():
    check_only = "--check" in sys.argv
    total = 0
    for d in DIRS:
        for p in sorted(glob.glob(os.path.join(d, "*.md"))):
            lines = io.open(p, encoding="utf-8").read().split("\n")
            changed = 0
            for i in range(len(lines) - 1):
                s = lines[i].strip()
                dl = lines[i + 1].strip()
                if s.startswith("|") and DELIM.match(dl):
                    nh = len(s.strip("|").split("|"))
                    nd = len(dl.strip("|").split("|"))
                    if nh != nd:
                        changed += 1
                        if not check_only:
                            lines[i + 1] = fix_delim(dl, nh)
            if changed:
                total += changed
                print("%-58s %d 处" % (os.path.relpath(p, MD), changed))
                if not check_only:
                    io.open(p, "w", encoding="utf-8", newline="\n").write(
                        "\n".join(lines))
    print("\n%s %d 处" % ("发现" if check_only else "修复", total))


if __name__ == "__main__":
    main()
