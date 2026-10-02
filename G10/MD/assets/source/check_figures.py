# -*- coding: utf-8 -*-
"""校验 figures/ 下所有 SVG：XML 合法性、禁用标签、文字越界、空内容"""
import os
import re
import sys
import glob
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"


def char_width(ch, fs):
    """粗略估算字符宽度：CJK 按 1.0em，其余按 0.55em"""
    o = ord(ch)
    if 0x2E80 <= o <= 0xFFEF:
        return fs * 1.0
    return fs * 0.55


def check(path):
    issues = []
    try:
        tree = ET.parse(path)
    except Exception as e:
        return ["XML 解析失败: %s" % e]
    root = tree.getroot()
    vb = root.get("viewBox")
    if not vb:
        issues.append("缺少 viewBox")
        W = H = None
    else:
        parts = vb.replace(",", " ").split()
        W, H = float(parts[2]), float(parts[3])

    raw = open(path, encoding="utf-8").read()
    for bad in ("<image", "<foreignObject", "xlink:href", "TBD", "待补充", "TODO"):
        if bad in raw:
            issues.append("含禁用内容: %s" % bad)

    n_text = 0
    for el in root.iter():
        tag = el.tag.replace(NS, "")
        if tag != "text":
            continue
        n_text += 1
        txt = "".join(el.itertext())
        if not txt.strip():
            continue
        fs = float(el.get("font-size", 12) or 12)
        try:
            x = float(el.get("x", 0))
            y = float(el.get("y", 0))
        except ValueError:
            continue
        w = sum(char_width(c, fs) for c in txt)
        anchor = el.get("text-anchor", "start")
        if anchor == "middle":
            left, right = x - w / 2, x + w / 2
        elif anchor == "end":
            left, right = x - w, x
        else:
            left, right = x, x + w
        if W and (right > W - 2 or left < 2):
            issues.append("文字越界 x: [%.0f, %.0f] 超出 0–%.0f | %s" % (left, right, W, txt[:38]))
        if H and (y > H - 2 or y < 8):
            issues.append("文字越界 y=%.0f 超出 0–%.0f | %s" % (y, H, txt[:38]))

    if n_text < 5:
        issues.append("文本元素过少 (%d)，可能没画完" % n_text)
    return issues


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(d, "*.svg")))
    if not files:
        print("没有找到 SVG")
        return
    total_bad = 0
    for f in files:
        issues = check(f)
        name = os.path.basename(f)
        size = os.path.getsize(f)
        if issues:
            total_bad += 1
            print("\n[X] %s  (%d bytes)" % (name, size))
            for i in issues[:8]:
                print("    - " + i)
            if len(issues) > 8:
                print("    ... 另有 %d 条" % (len(issues) - 8))
        else:
            print("[OK] %-42s %7d bytes" % (name, size))
    print("\n合计 %d 个文件，%d 个有问题" % (len(files), total_bad))


if __name__ == "__main__":
    main()
