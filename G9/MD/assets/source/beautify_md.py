# -*- coding: utf-8 -*-
"""
beautify_md.py —— 给 11 章正文 + 5 个附录做「Markdown 浏览器友好」的排版美化

## 为什么需要它
讲义同时有两种消费方式：① 用 build_chapter_pdf.py 排成 A4 PDF；② 直接在
Markdown 浏览器（mdview 等）里翻。PDF 有 CSS 和配色，而 md 浏览器只有
标准 Markdown 的渲染结果，所以同一个文件在 mdview 里会显得平、碎、找不着重点。

## 关键约束：mdview 会省略原始 HTML
mdview 一类工具用 goldmark / GitHub 风格内核，**`Raw HTML is omitted`**
（或转义）。所以：
  ❌ 不能用 <div style>、<span>、<img width=...>、Mermaid
  ✅ 只能用 标准 Markdown + GFM 表格 + 任务列表 + 引用块 + Unicode emoji

结论：想做"彩色提示块"，唯一可行的办法是 **emoji + 引用块 + 粗体**——
emoji 由浏览器渲染成彩色，视觉上就等价于 PDF 里的配色分区。

## 配色映射（对齐 PDF 的调色板）
  PDF 蓝 #185FA5 → 📘🔵 定义 / 知识 / 规则
  PDF 橙 #BA7517 → ⚠️🚨 易错 / 注意 / 例外 / 禁区
  PDF 绿 #3B6D11 → ✅🟢 正确示范 / 清单 / 结论
  PDF 红 #A32D2D → ⛔🚫 危险 / 绝对禁止
  PDF 灰 #F1EFE8 → 📋🗂️ 元信息 / 配套说明

## 做了什么（全部幂等，可重复运行）
  R1 图题单独成行：SVG 的 alt 在 mdview 里不显示，故在图片下补一行图题
     （编号加粗、标题常规）。⚠️ build_chapter_pdf.py 会跳过这些行，否则
     PDF 里会出现两个图题（SVG 内部已画了一个）。
  R2 删冗余分隔线：紧跟在 `## ` 之前的 `---` 删掉（GitHub CSS 的 h2 自带
     下边框，再加 --- 就是双线，很吵）。
  R3 提示块加 emoji 前缀：按标签语义分类，已有 emoji 的跳过。
  R4 行内【】标记加 emoji：Extension/预告/见 Ch.x 等；**填空【____】不动**。

用法：
    python beautify_md.py            # 处理 MD/chapters-cn + MD/appendices-cn + MD/chapters-en
    python beautify_md.py chapters-cn  # 只处理某一目录
    python beautify_md.py --dry      # 只打印会改什么，不写文件
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.dirname(os.path.dirname(HERE))               # assets/source -> G9/MD

# ---------------------------------------------------------------- emoji 分类表
# 顺序敏感：先匹配更具体的（警示 > 规则 > 记忆 > 通用）
BLOCK_RULES = [
    # (关键词, emoji)  —— 命中第一个就停
    (("课时", "时长", "Periods", "Time"), "⏱️"),
    (("教师专用", "教师提示", "给教师"), "👩‍🏫"),
    (("易错", "易混", "注意", "警示", "禁区", "例外", "澄清", "混淆",
      "提醒", "反例", "不要", "陷阱", "坑"), "⚠️"),
    (("危险", "严禁", "禁止", "不得", "绝对不能"), "⛔"),
    (("安全", "实验", "操作", "护目", "WHMIS"), "🧪"),
    (("Big Idea", "核心概念", "回扣"), "🎯"),
    (("一句话", "金句", "总结只有", "死记", "记住", "记忆", "口诀",
      "技巧", "联想", "好消息", "记忆点"), "💡"),
    (("铁律", "规则", "关键", "判据", "要点", "要求", "定律", "原则",
      "三步", "五步", "方法", "流程", "用法", "说明"), "📏"),
    (("Extension", "预告", "延伸", "回扣", "前瞻", "超纲"), "🔭"),
    (("双语", "中文", "英文", "命名", "译名", "词根"), "🌐"),
    (("例", "练一题", "同理"), "✏️"),
    (("大纲", "配套", "主课文", "生成时间", "文件", "数据来源", "术语总数",
      "统计", "页码", "来源", "类型"), "🗂️"),
    (("自检", "检查", "快速检查"), "🔍"),
]

# 已有 emoji 就不重复加
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]")

# 行内【】标记
INLINE_RULES = [
    (re.compile(r'【\s*Extension'), "【🔭 Extension"),
    (re.compile(r'【\s*预告'), "【⏭️ 预告"),
    (re.compile(r'【\s*复习'), "【🔙 复习"),
    (re.compile(r'【\s*(见\s*Ch|Ch\.?\s*\d)'), None),   # 动态加 🔗
]
# 填空类【____】必须原样保留
BLANK_RE = re.compile(r'【[_＿\s]*[_＿][_＿\s]*】|【[^】]{0,20}____')

# 图题：图 2-1　标题  /  Diagram / Table 等
FIG_ALT = re.compile(r'^(图\s*\d+[-–]\d+)[\s　]+(.+)$')


def pick_emoji(label):
    """按标签语义挑一个 emoji；返回 '' 表示不加。"""
    for keys, emo in BLOCK_RULES:
        for k in keys:
            if k in label:
                return emo
    return "📌"


# ---------------------------------------------------------------- R1 图题
def r1_figure_caption(lines):
    """SVG 的 alt 在 mdview 里不显示，故补一行图题。

    但**只有当前面没有 `### 图 X-Y …` 标题时才补**（全书 65 张图里有 56 张
    已经用 h3 写了图题，再补就是重复）。"""
    out, n = [], 0
    for i, ln in enumerate(lines):
        out.append(ln)
        m = re.match(r'^!\[(.*?)\]\((.*?)\)\s*$', ln)
        if not m:
            continue
        # 幂等：后面（跳过空行）已是图题
        k = i + 1
        while k < len(lines) and not lines[k].strip():
            k += 1
        if k < len(lines) and lines[k].strip().startswith("**📊"):
            continue
        # 前面已有标题图题 → 不补
        j = i - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        if j >= 0 and lines[j].lstrip().startswith("#"):
            continue
        alt = m.group(1)
        fm = FIG_ALT.match(alt)
        cap = ("**📊 %s**　%s" % (fm.group(1), fm.group(2))
               if fm else "**📊 %s**" % alt)
        out.append("")
        out.append(cap)
        n += 1
    return out, n


# ---------------------------------------------------------------- R2 分隔线
def r2_drop_rules(lines):
    """删掉「下一非空行是 ## 」的 ---，并顺手压掉因此多出来的空行。

    GitHub CSS 的 h2 自带下边框，`---` + h2 会形成双线，很吵。"""
    out, n = [], 0
    for i, ln in enumerate(lines):
        if ln.strip() == "---":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].lstrip().startswith("## "):
                n += 1
                # 前后都是空行的话删掉一个，避免留下连续两个空行
                if out and not out[-1].strip() and j > i + 1:
                    del out[-1]
                continue
        out.append(ln)
    return out, n


# ---------------------------------------------------------------- R3 提示块
def r3_block_emoji(lines):
    """> **标签**：...  →  > 🎯 **标签**：..."""
    pat = re.compile(r'^(>\s*)([*_]{0,2})([^*_：:]{1,40}?)([*_]{0,2})([：:])')
    out, n = [], 0
    for ln in lines:
        m = pat.match(ln)
        if m:
            lead, b1, label, b2, colon = m.groups()
            label_stripped = label.strip()
            # 已有 emoji / 纯英文元信息里带 - 列表项 → 跳过
            if (not EMOJI_RE.search(label_stripped)
                    and not label_stripped.startswith("-")
                    and len(label_stripped) >= 2):
                emo = pick_emoji(label_stripped)
                if emo:
                    ln = "%s%s %s%s%s%s" % (lead, emo, b1, label, b2, colon) \
                        + ln[m.end():]
                    n += 1
        out.append(ln)
    return out, n


# ---------------------------------------------------------------- R4 行内标记
def r4_inline_tags(lines):
    out, n = [], 0
    for ln in lines:
        if "【" in ln:
            new = ln
            # 先把填空占位保护起来
            holders = []

            def stash(mo):
                holders.append(mo.group(0))
                return "\x00%d\x00" % (len(holders) - 1)
            new = BLANK_RE.sub(stash, new)

            if "【Extension" in new:
                new = new.replace("【Extension", "【🔭 Extension")
                n += 1
            if "【预告" in new:
                new = new.replace("【预告", "【⏭️ 预告")
                n += 1
            if "【复习" in new:
                new = new.replace("【复习", "【🔙 复习")
                n += 1

            # 【见 Ch.x】/【Ch.x 详解】/【详因见 Ch.x】 → 🔗
            def link(mo):
                inner = mo.group(1)
                if inner.startswith("🔗") or "_" in inner:
                    return mo.group(0)
                return "【🔗 %s】" % inner
            before = new
            new = re.sub(r'【((?:见\s*|详因见\s*)?Ch[^】]{0,18})】', link, new)
            if new != before:
                n += 1

            new = re.sub(r'\x00(\d+)\x00',
                         lambda mo: holders[int(mo.group(1))], new)
            ln = new
        out.append(ln)
    return out, n


# ---------------------------------------------------------------- 主流程
def process(path, dry=False):
    src = open(path, encoding="utf-8").read()
    lines = src.split("\n")
    total = {}
    lines, c = r1_figure_caption(lines);   total["图题"] = c
    lines, c = r2_drop_rules(lines);       total["删分隔线"] = c
    lines, c = r3_block_emoji(lines);      total["提示块emoji"] = c
    lines, c = r4_inline_tags(lines);      total["行内标记"] = c
    new = "\n".join(lines)
    name = os.path.basename(path)
    changed = new != src
    if changed and not dry:
        open(path, "w", encoding="utf-8", newline="\n").write(new)
    print("%-56s %s" % (name[:56],
                        "  ".join("%s+%d" % (k, v) for k, v in total.items()
                                  if v) or "无变化"))
    return changed


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    dirs = args or ["chapters-cn", "appendices-cn", "chapters-en"]
    n = 0
    for d in dirs:
        p = os.path.join(MD, d)
        if not os.path.isdir(p):
            print("目录不存在:", p)
            continue
        print("===== %s =====" % d)
        for name in sorted(os.listdir(p)):
            if not name.endswith(".md"):
                continue
            if process(os.path.join(p, name), dry):
                n += 1
    print("\n%s %d 个文件" % ("（dry run，未写入）将修改" if dry else "已修改", n))


if __name__ == "__main__":
    main()
