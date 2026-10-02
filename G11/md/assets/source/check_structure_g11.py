# -*- coding: utf-8 -*-
"""G11 讲义结构校验（Ch.01–Ch.14 + 附录 A–E）
用法： python check_structure_g11.py
检查项：
  1. 每章 10 节编号齐（## 1. … ## 10.）
  2. 章标题与所有 ## 标题含全角竖线 ｜；不得出现半角 | 作标题分隔
  3. 图引用 ../assets/figures/*.svg 文件存在；全库无未引用图
  4. 第 9 节：题干 16 / 答案 16（A10·B4·C2）；题干与答案各有中文对照；相邻题干间必须空行
  5. 提示块（> ）的加粗标签必须英文在前（不得以中文字符开头）
退出码： 0 全通过 / 1 有问题
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.abspath(os.path.join(HERE, "..", ".."))
CH = os.path.join(MD, "chapters-en")
AP = os.path.join(MD, "appendices-en")
FIG = os.path.join(MD, "assets", "figures")

CJK = re.compile(r"[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]")
FIGREF = re.compile(r"\.\./assets/figures/([\w\-.]+\.svg)")


def md_files(d):
    out = []
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".md") and fn != "_STYLE.md":
                out.append(os.path.join(d, fn))
    return out


def chapter_section(lines):
    """切出第 9 节文本行。"""
    s, e = None, None
    for i, ln in enumerate(lines):
        if re.match(r"^## 9\.", ln):
            s = i
        elif s is not None and re.match(r"^## 10\.", ln):
            e = i
            break
    return lines[s:e] if s is not None else []


def main():
    problems = []
    chapters = md_files(CH)
    others = md_files(AP)
    used_figs = set()

    # ---- 逐章 ----
    for p in chapters:
        fn = os.path.basename(p)
        with io.open(p, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        tag = fn.split("_")[0]

        # 1. 十节
        secs = [int(m.group(1)) for m in
                (re.match(r"^## (\d+)\.", l) for l in lines) if m]
        if secs != list(range(1, 11)):
            problems.append(f"  [{tag}] 节编号异常：{secs}")

        # 2. 标题全角 ｜
        for l in lines:
            if l.startswith("## "):
                if "｜" not in l:
                    problems.append(f"  [{tag}] 标题缺全角｜：{l[:60]}")
                if re.search(r"[A-Za-z]\s\|\s", l):
                    problems.append(f"  [{tag}] 标题用了半角 |：{l[:60]}")

        # 3. 图引用
        refs = FIGREF.findall("\n".join(lines))
        if len(refs) != 4:
            problems.append(f"  [{tag}] 图引用 {len(refs)} 处（期望 4）")
        for r in refs:
            used_figs.add(r)
            if not os.path.isfile(os.path.join(FIG, r)):
                problems.append(f"  [{tag}] 图文件缺失：{r}")

        # 4. 第 9 节
        s9 = chapter_section(lines)
        stems = [(i, l) for i, l in enumerate(s9) if re.match(r"^\*\*[ABC]\d+\.\*\*", l)]
        answs = [(i, l) for i, l in enumerate(s9) if re.match(r"^- \*\*[ABC]\d+\.\*\*", l)]
        cnt = {"A": 0, "B": 0, "C": 0}
        for _, l in stems:
            cnt[l[2]] += 1
        if cnt != {"A": 10, "B": 4, "C": 2}:
            problems.append(f"  [{tag}] 题干分布 {cnt}（期望 A10·B4·C2）")
        if len(stems) != len(answs):
            problems.append(f"  [{tag}] 题干 {len(stems)} ≠ 答案 {len(answs)}")
        cn = [l for l in s9 if re.match(r"^\s*- \*\*中文\*\*：", l)]
        if len(cn) != 32:
            problems.append(f"  [{tag}] 第 9 节中文对照 {len(cn)} 条（期望 32）")
        # 每题干：向后扫到下一题干/小标题为止，须有（顶格）中文对照
        STEM = re.compile(r"^\*\*[ABC]\d+\.\*\*")
        for i, _ in stems:
            j = i + 1
            ok = False
            while j < len(s9):
                if STEM.match(s9[j]) or s9[j].startswith("### "):
                    break
                if re.match(r"^- \*\*中文\*\*：", s9[j]):
                    ok = True
                    break
                j += 1
            if not ok:
                problems.append(f"  [{tag}] 题干缺中文对照：L{i}")
        # 相邻题干间必须空行
        for k in range(1, len(stems)):
            if s9[stems[k][0] - 1].strip() != "":
                problems.append(f"  [{tag}] 题干之间未空行：{s9[stems[k][0]][:40]}")
        # 每答案：向后扫到下一答案为止，须有（缩进）中文对照
        ANS = re.compile(r"^- \*\*[ABC]\d+\.\*\*")
        for i, _ in answs:
            j, ok = i + 1, False
            while j < len(s9):
                if ANS.match(s9[j]):
                    break
                if re.match(r"^\s+- \*\*中文\*\*：", s9[j]):
                    ok = True
                    break
                j += 1
            if not ok:
                problems.append(f"  [{tag}] 答案缺中文对照：L{i}")

    # ---- 附录：仅查图引用与提示块 ----
    for p in others:
        fn = os.path.basename(p)
        with io.open(p, encoding="utf-8") as fh:
            txt = fh.read()
        for r in FIGREF.findall(txt):
            used_figs.add(r)
            if not os.path.isfile(os.path.join(FIG, r)):
                problems.append(f"  [{fn}] 图文件缺失：{r}")

    # 5. 提示块标签英文在前
    for p in chapters + others:
        fn = os.path.basename(p)
        with io.open(p, encoding="utf-8") as fh:
            for ln, l in enumerate(fh, 1):
                m = re.match(r"^> \S+ \*\*(.+?)\*\*", l)
                if m and CJK.match(m.group(1)[0]):
                    problems.append(f"  [{fn}:{ln}] 提示块标签非英文在前：{m.group(1)[:30]}")

    # 6. 图库未引用
    all_figs = {f for f in os.listdir(FIG) if f.endswith(".svg")}
    unused = sorted(all_figs - used_figs)
    if unused:
        problems.append(f"  未引用的图 {len(unused)} 张：{', '.join(unused[:6])}")

    print("=== G11 结构校验 ===")
    print(f"  章节 {len(chapters)} 份 · 附录 {len(others)} 份 · 图库 {len(all_figs)} 张"
          f"（已引用 {len(used_figs)}）")
    if problems:
        for x in problems:
            print(x)
        print(f"  合计 {len(problems)} 个问题 ❌")
        return 1
    print("  全部通过 ✅（10 节齐 · 标题全角｜· 图无孤立/无未引用 · 第9节16+16且中文齐 · 标签英文在前）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
