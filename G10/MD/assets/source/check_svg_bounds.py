# -*- coding: utf-8 -*-
"""
check_svg_bounds.py —— 图形越界自检（越界 = 被画布裁掉，肉眼看 md 发现不了）

为什么需要它：
    SVG 的画布高度是脚本里手写的数字（head(900, 486, ...)），
    如果后面又往里加了内容却没同步改高度，超出的部分浏览器/PDF 会直接裁掉，
    既没有报错也没有警告。ch10-whmis 的整条底部注记就是这样丢掉的。

做法：
    读 viewBox 得到画布 W×H，再扫所有图元算各自的最大下边界 / 右边界，
    超过 H（右边界超过 W）就报出来。path 取 d 里出现的数字做保守估计。
"""
import os
import re
import sys
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(HERE), "figures")

TOL = 2.0   # 允许的小误差（pt）


def bounds(svg_text):
    """返回 (max_bottom, max_right, 明细列表)"""
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
    if not m:
        return None
    W, H = float(m.group(1)), float(m.group(2))
    worst_b, worst_r = 0.0, 0.0
    detail = []

    def note(kind, val, limit, raw):
        nonlocal worst_b, worst_r
        if limit == "b":
            worst_b = max(worst_b, val)
        else:
            worst_r = max(worst_r, val)
        if val > (H if limit == "b" else W) + TOL:
            detail.append((kind, val, raw[:70]))

    # rect
    for tag in re.findall(r'<rect\b[^>]*/>', svg_text):
        g = lambda a, d=0.0: float(re.search(a + r'="([-\d.]+)"', tag).group(1)) \
            if re.search(a + r'="([-\d.]+)"', tag) else d
        note("rect", g("y") + g("height"), "b", tag)
        note("rect", g("x") + g("width"), "r", tag)
    # circle / ellipse
    for tag in re.findall(r'<(?:circle|ellipse)\b[^>]*/>', svg_text):
        g = lambda a, d=0.0: float(re.search(a + r'="([-\d.]+)"', tag).group(1)) \
            if re.search(a + r'="([-\d.]+)"', tag) else d
        r = g("r") or g("rx") or g("ry")
        note("circle", g("cy") + r, "b", tag)
        note("circle", g("cx") + r, "r", tag)
    # text（基线 y，加 0.45em 估计字底）
    for tag in re.findall(r'<text\b[^>]*>.*?</text>', svg_text, re.S):
        gm = re.search(r'\by="([-\d.]+)"', tag)
        fm = re.search(r'font-size="([-\d.]+)"', tag)
        if not gm:
            continue
        y = float(gm.group(1))
        fs = float(fm.group(1)) if fm else 12.0
        note("text", y + fs * 0.45, "b", tag)
        am = re.search(r'\btext-anchor="(\w+)"', tag)
        xm = re.search(r'\bx="([-\d.]+)"', tag)
        if xm and (am is None or am.group(1) in ("start",)):
            note("text", float(xm.group(1)), "r", tag)
    # path：按 SVG 指令规范解析（M/L/T 2 参，H/V 1 参，C 6 参，S/Q 4 参，A 7 参）
    for tag in re.findall(r'<path\b[^>]*/>', svg_text):
        dm = re.search(r'\sd="([^"]+)"', tag)
        if not dm:
            continue
        ys, xs = [], []
        cur = None
        for tok in re.finditer(r'([MLHVCQSTAZmlhvcqstaz])\s*([^MLHVCQSTAZmlhvcqstaz]*)',
                               dm.group(1)):
            cmd, argstr = tok.group(1), tok.group(2)
            nums = [float(v) for v in re.findall(r'-?\d*\.?\d+', argstr)]
            up = cmd.upper()
            n = {"M": 2, "L": 2, "T": 2, "H": 1, "V": 1,
                 "C": 6, "S": 4, "Q": 4, "A": 7, "Z": 0}[up]
            if n == 0 or not nums:
                cur = up
                continue
            for i in range(0, len(nums) - n + 1, n):
                grp = nums[i:i + n]
                if up == "H":
                    xs.append(grp[0])
                elif up == "V":
                    ys.append(grp[0])
                elif up == "A":
                    # rx ry rot large-arc sweep x y → 终点在最后两位
                    xs.append(grp[5])
                    ys.append(grp[6])
                else:
                    xs += grp[0::2]
                    ys += grp[1::2]
            cur = up
        if ys:
            note("path", max(ys), "b", tag)
        if xs:
            note("path", max(xs), "r", tag)
    return W, H, worst_b, worst_r, detail


def main():
    files = sorted(glob.glob(os.path.join(FIG_DIR, "*.svg")))
    bad = 0
    for f in files:
        s = open(f, encoding="utf-8").read()
        r = bounds(s)
        if not r:
            print("!! 无 viewBox:", os.path.basename(f))
            bad += 1
            continue
        W, H, wb, wr, detail = r
        if detail:
            bad += 1
            print("!! %-40s 画布 %.0fx%.0f  下边界%.0f 右边界%.0f"
                  % (os.path.basename(f), W, H, wb, wr))
            for kind, val, raw in detail[:4]:
                axis = "下" if val > H else "右"
                print("     %s向越界 %.0f  %s" % (axis, val, raw))
    print("\n共检查 %d 张，越界 %d 张" % (len(files), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
