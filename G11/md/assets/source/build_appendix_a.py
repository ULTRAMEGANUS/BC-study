# -*- coding: utf-8 -*-
"""
G11 Appendix A builder — glossary extracted from all chapters' Section 6
vocab tables. Outputs:
  md/appendices-en/Appendix_A_Glossary.md
  md/appendices-en/glossary.csv
Idempotent: safe to re-run after any chapter edit.
"""
import os
import re
import csv

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.abspath(os.path.join(HERE, "..", ".."))
CHAPTERS = os.path.join(MD, "chapters-en")
OUT_DIR = os.path.join(MD, "appendices-en")

HEADER = """# Appendix A — Glossary｜附录 A　词汇总表（EN ↔ 中）

> 🗂️ **Scope note｜范围说明**：Generated automatically from the Key Vocabulary tables of Chapters 1–14; run `build_appendix_a.py` again after any chapter edit.｜由第 1–14 章第 6 节词汇表自动汇总生成；章节修改后重跑 `build_appendix_a.py` 即可同步。
> Companions: `glossary.csv`（Anki / Quizlet import source）.

| Term 英文 | 中文 | Chapter 章 | Note 备注 |
|---|---|---|---|
"""


def chapter_sort_key(name):
    m = re.search(r"Ch(\d+)", name)
    return int(m.group(1)) if m else 999


def collect():
    rows = []
    seen = {}
    for f in sorted(os.listdir(CHAPTERS)):
        if not (f.startswith("Ch") and f.endswith(".md")):
            continue
        ch = int(re.search(r"Ch(\d+)", f).group(1))
        t = open(os.path.join(CHAPTERS, f), encoding="utf-8").read()
        m6 = re.search(r"^## 6\. Key Vocabulary.*?$", t, re.M)
        if not m6:
            continue
        rest = t[m6.end():]
        m7 = re.search(r"^## 7\.", rest, re.M)
        sec6 = rest[:m7.start()] if m7 else rest
        for line in sec6.split("\n"):
            line = line.strip()
            if not line.startswith("|") or line.startswith("|---") or line.startswith("| Term"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 2:
                continue
            # 有两种表头（Ch.5–7 与其余章不同）：
            #   3 列  | English | 中文 | Note｜备注 |
            #   2 列  | Term｜术语 | Meaning in one line｜一句话释义 |
            if "｜" in cells[0]:
                parts = cells[0].split("｜")
                en, zh = parts[0].strip(), parts[1].strip()
                note = cells[1]
            else:
                en, zh = cells[0], cells[1]
                note = cells[2] if len(cells) > 2 else ""
            if not en or not zh:
                continue
            if en.lower() in ("english", "term", "english term", "term 英文"):
                continue          # 表头行（两种表头：English / Term｜术语）
            key = en.lower()
            if key in seen:
                seen[key]["chs"].append(ch)
                continue
            seen[key] = {"en": en, "zh": zh, "note": note, "chs": [ch]}
            rows.append(seen[key])
    rows.sort(key=lambda r: re.sub(r"[^a-z]", "", r["en"].lower()))
    return rows


def main():
    rows = collect()
    os.makedirs(OUT_DIR, exist_ok=True)

    # 自检：术语/中文列不得残留全角竖线（说明表头变体没被正确拆分）
    badrows = [r for r in rows if "｜" in r["en"] or "｜" in r["zh"]]
    if badrows:
        raise SystemExit("ERROR: %d 行术语/中文列残留全角｜，表头变体未处理：%s"
                         % (len(badrows), badrows[0]["en"][:60]))
    misszh = [r for r in rows if not r["zh"]]
    if misszh:
        print("WARN: %d 条缺中文：%s" % (len(misszh), [r["en"] for r in misszh[:5]]))
    junk = [r for r in rows if r["en"].lower() in ("english", "term")]
    if junk:
        raise SystemExit("ERROR: 表头行被当成条目（%s）" % junk[0]["en"])

    lines = [HEADER]
    for r in rows:
        ch = "Ch." + ", ".join(f"{c}" for c in sorted(set(r["chs"])))
        note = r["note"].replace("|", "/")
        lines.append(f"| {r['en']} | {r['zh']} | {ch} | {note} |\n")
    lines.append(f"\n**{len(rows)} terms｜共 {len(rows)} 条。**\n")
    with open(os.path.join(OUT_DIR, "Appendix_A_Glossary.md"), "w", encoding="utf-8") as f:
        f.write("".join(lines))

    with open(os.path.join(OUT_DIR, "glossary.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Term", "Chinese", "Chapters", "Note"])
        for r in rows:
            w.writerow([r["en"], r["zh"], ", ".join(str(c) for c in sorted(set(r["chs"]))), r["note"]])

    print(f"Appendix A: {len(rows)} terms -> Appendix_A_Glossary.md + glossary.csv")


if __name__ == "__main__":
    main()
