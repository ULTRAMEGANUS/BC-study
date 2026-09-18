# -*- coding: utf-8 -*-
"""从 11 章讲义正文抽取「核心词汇」表，去重汇总生成附录 A（英中对照词汇总表）。

用法（在任意目录运行均可，默认路径会自动定位到 G9/）：
    python build_glossary.py                          # 覆盖 appendices/ 下已有的 AppendixA_*.md
    python build_glossary.py <chapters目录> <输出md>

同时把术语表导出为同目录的 glossary.csv（Anki / Quizlet 导入源）。
"""
import os, re, sys, glob, csv, time

HERE = os.path.dirname(os.path.abspath(__file__))        # .../G9/assets/source
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))    # .../G9

chap_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "chapters")
if len(sys.argv) > 2:
    out_path = sys.argv[2]
else:
    # 已存在则原地覆盖（沿用原文件名与生成时间），不存在才新建带时间戳的文件
    _ex = sorted(glob.glob(os.path.join(ROOT, "appendices", "AppendixA_*.md")))
    out_path = _ex[-1] if _ex else os.path.join(
        ROOT, "appendices",
        "AppendixA_Glossary_EN_CN_%s.md" % time.strftime("%Y%m%d_%H%M%S"))

files = sorted(glob.glob(os.path.join(chap_dir, "Ch*.md")))
if not files:
    sys.exit("no chapter files found in %s" % chap_dir)


def chapter_of(fname):
    m = re.match(r"Ch(\d+)", os.path.basename(fname))
    return int(m.group(1)) if m else 0


entries = {}
for f in files:
    ch = chapter_of(f)
    with open(f, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    start, end = None, len(lines)
    for i, l in enumerate(lines):
        if l.startswith("## 6.") and "核心词汇" in l:
            start = i
        elif start is not None and l.startswith("## 7."):
            end = i
            break
    if start is None:
        print("  [warn] no vocab section:", os.path.basename(f))
        continue

    n = 0
    for l in lines[start:end]:
        l = l.strip()
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) < 2:
            continue
        en, zh = cells[0], cells[1]
        note = cells[2] if len(cells) > 2 else ""
        # 去掉加粗标记，保证全表排版与排序一致
        en = en.replace("**", "").strip()
        zh = zh.replace("**", "").strip()
        note = note.replace("**", "").strip()
        # Ch.11 是「全册高频复习表」，第三列是章节引用而非注释，遇到则清空
        if re.match(r"^Ch\.?\s*\d", note, re.I):
            note = ""
        # 跳过表头与分隔行
        if not en or en.lower() == "english" or re.match(r"^[-:\s]+$", en):
            continue
        if en.lower() == "英文" or zh.lower() == "中文":
            continue
        key = en.lower()
        if key not in entries:
            entries[key] = {"en": en, "zh": zh, "note": note, "chs": [ch]}
            n += 1
        else:
            if ch not in entries[key]["chs"]:
                entries[key]["chs"].append(ch)
            if not entries[key]["note"] and note:
                entries[key]["note"] = note
            if not entries[key]["zh"] and zh:
                entries[key]["zh"] = zh
    print("  Ch.%02d -> %d new rows" % (ch, n))

total = len(entries)
print("total unique terms:", total)


def chs_str(chs):
    return ", ".join("Ch.%d" % c for c in sorted(chs))


# ---------- A-2 字母序总表 ----------
alpha = sorted(entries.values(), key=lambda e: e["en"].lower())
rows_alpha = []
for e in alpha:
    note = e["note"] if e["note"] and e["note"] != "—" else "—"
    rows_alpha.append("| %s | %s | %s | %s |" % (e["en"], e["zh"], note, chs_str(e["chs"])))

# ---------- A-3 按章节索引 ----------
by_ch = {}
for e in alpha:
    for c in e["chs"]:
        by_ch.setdefault(c, []).append(e)
rows_ch = []
for c in sorted(by_ch):
    items = sorted(by_ch[c], key=lambda e: e["en"].lower())
    rows_ch.append("| **Ch.%d** | %d | %s |" % (c, len(items), " · ".join("%s（%s）" % (i["en"], i["zh"]) for i in items)))

# ---------- A-4 易混术语对 ----------
pairs = [
    ("element 元素 vs compound 化合物", "只有 1 种原子／2 种以上元素化学结合；前者不可再分解，后者有固定配比和化学式"),
    ("atom 原子 vs ion 离子", "电中性（质子数＝电子数）／带电（电子数变了，质子数永不变）"),
    ("atomic number 原子序数 vs mass number 质量数", "＝质子数，恒为整数／＝质子＋中子，本册范围内为整数；而 periodic table 上的 atomic mass 是小数（同位素加权平均）"),
    ("group 族 vs period 周期", "纵列，同族价电子数相同／横行，同周期电子层数相同"),
    ("metal 金属 vs non-metal 非金属 vs metalloid 类金属", "失电子、导电导热、有延展性／得电子、绝缘、脆／两者兼有，位于锯齿线两侧（metalloid = semi-metal）"),
    ("cation 阳离子 vs anion 阴离子", "金属失电子带正电，路易斯图 0 个点／非金属得电子带负电，路易斯图 8 个点"),
    ("ionic compound 离子化合物 vs molecular compound 分子化合物", "金属+非金属，电子转移，交叉法命名，高熔沸点、溶融/水溶液导电／非金属+非金属，电子共用，前缀法命名，低熔沸点、不导电"),
    ("physical change 物理变化 vs chemical change 化学变化", "无新物质、可逆／有新物质，看变色·气体·沉淀·温度·发光·新气味六证据"),
    ("homogeneous 均一的 vs heterogeneous 非均一的", "各处组成相同、看不出界面／能看出不同部分，会分层"),
    ("coefficient 系数 vs subscript 下标", "化学式前面的数字，**可以改**／元素右下角的小数字，**绝对不能改**（改了就换物质了）"),
    ("valence electron 价电子 vs valence shell 价电子层", "最外层上的**电子个数**／最外面那一**层**本身"),
    ("Bohr diagram 玻尔模型图 vs Lewis dot diagram 路易斯点式", "画出全部电子层与全部电子，看排布／只画最外层的价电子，看成键"),
    ("qualitative 定性的 vs quantitative 定量的", "描述性观察（颜色、状态）／可测量的数值（质量、温度、时间）"),
    ("independent 自变量 vs dependent 因变量 vs controlled variable 控制变量", "主动改变的量／因之变化、被测量的量／必须保持不变的量"),
    ("word equation 文字方程式 vs skeleton equation 骨架方程式 vs balanced equation 配平方程式", "只写名称／换成化学式但未配平／加系数后左右原子数相等"),
]
rows_pairs = ["| %s | %s |" % (a, b) for a, b in pairs]

# 沿用已有文件的生成时间，避免重跑产生无意义的时间戳 diff
stamp = time.strftime("%Y-%m-%d %H:%M")
if os.path.exists(out_path):
    with open(out_path, encoding="utf-8") as _fh:
        _m = re.search(r"\*\*生成时间\*\*：(.+)", _fh.read())
    if _m:
        stamp = _m.group(1).strip()

doc = """# 附录 A — Glossary 词汇总表｜英中对照 Master Glossary

## BC Science 9 · Chemistry Unit｜不列颠哥伦比亚省 九年级科学 · 化学单元

> **生成时间**：{stamp}
> **数据来源**：自动抽取自 `chapters/Ch01–Ch11` 各章第 6 节「核心词汇｜Key Vocabulary」，去重后按字母序汇总
> **术语总数**：{total} 条
> **配套文件**：附录 B 常见离子表 · 附录 C 命名速查表 · 附录 D 元素中英对照表 · 附录 E 实验与练习单

---

## A-1 使用说明｜How to Use This Glossary

1. **查词**：按 A-2 字母序总表查找，English 一列按 A→Z 排列（忽略大小写）。
2. **复习**：用 A-3 按章节索引做单元复习——遮住中文列自测，或遮住英文列自测。
3. **辨析**：A-4 收录了 {npairs} 组最易混淆的术语对，考前必看。
4. **导出**：A-2 表格可直接粘贴进 Anki / Quizlet 做单词卡（English 正面，中文+说明 反面）。
5. **体例**：术语一律 `English（中文）`；「说明」列为该术语在本册语境下的简要注解，不是完整定义，完整定义见对应章节第 3 节。

> **考试提示**：BC 省考试答题时，**化学式与英文命名必须用英文书写**；中文列是为了帮助你理解，不要写进英文答卷。

---

## A-2 字母序总表｜Alphabetical Master List（{total} 条）

| English | 中文 | 说明 | 出现章节 |
|---|---|---|---|
{alpha}

---

## A-3 按章节索引｜Index by Chapter

| 章节 | 条数 | 术语（English（中文）） |
|---|---|---|
{bych}

> 同一术语若在多个章节出现，会在各章索引中重复列出——这是**有意为之**，方便按章复习。

---

## A-4 易混术语辨析｜Confusable Pairs（考前必看）

| 术语对 | 辨析要点 |
|---|---|
{pairs}

---

## A-5 词汇自测表｜Self-Test Checklist

把下表打印出来，遮住右侧两列自测。**全部能默出即为达标。**

| ✓ | English | 中文 | 说明 |
|---|---|---|
{checklist}

---

*本附录由 `chapters/` 下 11 章正文自动抽取生成，术语与正文严格一致。如需增补，请回到对应章节第 6 节统一修改，再重新生成。*
""".format(
    stamp=stamp,
    total=total,
    npairs=len(pairs),
    alpha="\n".join(rows_alpha),
    bych="\n".join(rows_ch),
    pairs="\n".join(rows_pairs),
    checklist="\n".join("| ☐ | %s | %s | %s |" % (e["en"], e["zh"], (e["note"] if e["note"] and e["note"] != "—" else "—")) for e in alpha),
)

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as fh:
    fh.write(doc)

print("written:", out_path)

# ---------- 附带导出 CSV（Anki / Quizlet 导入源）----------
csv_path = os.path.join(HERE, "glossary.csv")
with open(csv_path, "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["English", "中文", "说明", "出现章节"])
    for e in alpha:
        w.writerow([
            e["en"], e["zh"],
            (e["note"] if e["note"] and e["note"] != "—" else ""),
            chs_str(e["chs"]),
        ])
print("written:", csv_path, "(%d rows)" % len(alpha))
