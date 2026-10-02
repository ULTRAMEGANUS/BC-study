# -*- coding: utf-8 -*-
"""把第 9 节 Answer Key 里「内联式」中文对照改成体例规定的「两格缩进独立子项」。

规定见 chapters-en/_STYLE.md §9：
    每道题、每条答案必须紧跟中文对照——题目下方用 `- **中文**：…`（空一行后）；
    答案列表项下用两格缩进的 `**中文**：…` 子项。

改前： - **A1.** English text.｜**中文**：中文译文。
改后： - **A1.** English text.
       （空行）
         - **中文**：中文译文。

幂等：已符合体例的行不会被改动。
用法： python normalize_answer_cn.py [--check]
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.abspath(os.path.join(HERE, "..", "..", "chapters-en"))
PAT = re.compile(r"^(- \*\*[ABC]\d+\.\*\*)(.*?)｜\*\*中文\*\*：(.*)$")

def main(check):
    total = 0
    for fn in sorted(os.listdir(CH)):
        if not re.match(r"^Ch\d+.*\.md$", fn):
            continue
        p = os.path.join(CH, fn)
        with io.open(p, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
        out, n = [], 0
        for ln in lines:
            m = PAT.match(ln)
            if m:
                n += 1
                out.append(f"{m.group(1)}{m.group(2).rstrip()}")
                out.append("")
                out.append(f"  - **中文**：{m.group(3).strip()}")
            else:
                out.append(ln)
        if n:
            total += n
            if not check:
                with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write("\n".join(out))
            print(f"  {'待改' if check else '已改'} {n:3d} 条  {fn}")
    print(f"  合计 {total} 条")
    return 0

if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
