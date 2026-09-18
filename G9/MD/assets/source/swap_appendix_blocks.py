# -*- coding: utf-8 -*-
"""
swap_appendix_blocks.py —— 把附录 md 里的 ASCII 字符画换成 SVG 图片引用

与 swap_ascii_blocks.py 同思路：按「第 N 个代码块」定位（行号会漂移），
每条替换带 expect= 内容校验，块序号**降序**处理。

⚠️ 附录 E 是实验练习单，里面大量 `NAME 姓名：____` 之类的**填空表单**
   绝不能换成 SVG（换了就没法填写）。换之前务必人工确认块内容。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(os.path.dirname(HERE))
AP = os.path.join(MD, "appendices-cn")


def split_blocks(lines):
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


def img(alt, name):
    return ["![%s](../assets/figures/%s)" % (alt, name), ""]


def swap(md_path, index, new_lines, expect=None, add_title=None):
    lines = open(md_path, encoding="utf-8").read().split("\n")
    bs = split_blocks(lines)
    if index < 1 or index > len(bs):
        raise SystemExit("%s 块序号 %d 越界（共 %d 块）"
                         % (os.path.basename(md_path), index, len(bs)))
    st, en = bs[index - 1]
    if expect:
        head_txt = "\n".join(lines[st + 1:min(en, st + 4)])
        if expect not in head_txt:
            raise SystemExit("块%d 内容校验失败：开头是 %r，不含 %r"
                             % (index, head_txt[:70], expect))
    if add_title:
        new_lines = ["### %s" % add_title, ""] + new_lines
    lines[st:en + 1] = new_lines
    open(md_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("  替换 %s 块%d（原 %d 行 → %d 行）"
          % (os.path.basename(md_path)[:20], index, en - st + 1,
             len(new_lines)))


# 块序号**降序**：替换后该块不再是代码块，后面的序号会全部前移
PLAN = {
    "AppendixE_Lab_Worksheet_Bank": [
        # ⚠️ 只换「0 下划线」的纯参考图。带 ______ /【____】的是给学生填的
        #    练习框与报告模板，换成 SVG 就没法填写了，一律保留原样。
        (28, "shell 1 : 2 e",
         img("钙-40 Bohr 图参考答案｜Ca-40 Answer", "appe-bohr-Ca40.svg")),
        (27, "shell 1 : 2 e",
         img("磷-31 Bohr 图参考答案｜P-31 Answer", "appe-bohr-P31.svg")),
        (5, "shell 1 (K)",
         img("Na 钠玻尔图参考图例｜Reference Diagram", "appe-bohr-Na.svg")),
        (4, "bulb",
         img("导电性检测电路｜Conductivity Circuit",
             "appe-conductivity-circuit.svg")),
        (3, "MATTER",
         img("物质分类树｜Matter Classification Tree", "appe-matter-tree.svg")),
        (2, "INDEPENDENT",
         img("变量与公平实验｜Variables & Fair Test",
             "appe-variables-fair-test.svg")),
    ],
    "AppendixC_Naming_Cheat_Sheet": [
        (3, "╔", img("附录 C 命名速查卡｜Naming Cheat Sheet",
                     "appc-cheat-sheet.svg")),
        (2, "sodium chloride",
         img("附录 C-7 中英命名顺序相反｜Opposite Word Order",
             "appc-cn-en-order.svg")),
        (1, "拿到化学式",
         img("附录 C-1 命名决策树｜Naming Decision Tree",
             "appc-naming-decision-tree.svg")),
    ],
}


def main():
    args = sys.argv[1:] or list(PLAN)
    for key in args:
        if key not in PLAN:
            print("未定义的计划:", key)
            continue
        md = None
        for name in os.listdir(AP):
            if name.startswith(key) and name.endswith(".md"):
                md = os.path.join(AP, name)
                break
        if not md:
            raise SystemExit("找不到附录文件: " + key)
        print("===== %s =====" % os.path.basename(md))
        for index, expect, new_lines in PLAN[key]:
            swap(md, index, new_lines, expect=expect)


if __name__ == "__main__":
    main()
