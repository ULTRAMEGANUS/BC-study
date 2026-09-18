# G9/MD/chapters-en/ 英文版讲义体例（English-primary · Chinese-gloss）

读者：母语为中文、在 BC 省读 Science 9 的学生。**英文是主体叙述语言，中文是紧随其后的对照解释。**

## 1. 标题（决定 PDF 书签，务必严格照做）

```markdown
# Ch.2 — Elements, Symbols and the Periodic Table
## Chapter 2 · Elements, Symbols and the Periodic Table｜第 2 章　元素、元素符号与元素周期表

## 1. Content Alignment｜大纲对应
### 3.1 Element｜元素
### 表 2-1　Atomic Number vs Atomic Mass｜原子序数与相对原子质量
### Fig. 2-1　Reading a Cell｜周期表方格怎么读
```

规则：
- **英文在前，中文在后**，中间用全角竖线 `｜`（U+FF5C）分隔，两边不加空格。
- 章节内小节编号保留（`3.1`、`表 2-1`、`图 X-Y`、`活动 X-Y`）。
- 图的编号在英文版里写 `Fig. 2-1`（不是「图 2-1」）。
- 标题层级：H1 章英文名 / H2 章名双语 / H2 节 / H3 小节。

## 2. 正文：英文段 + 中文段

**每一个英文段落后面紧跟一个中文段落**，中文段以 `**中文**：` 开头：

```markdown
An **element** is a pure substance made of only one kind of atom, which cannot be
broken down into simpler substances by chemical means.

**中文**：元素是由**同一种原子**组成的纯净物，**不能用化学方法**再分解成更简单的物质。
```

列表项同理，中文用**缩进的子项**：

```markdown
- An element cannot be separated into other substances by chemical reactions. 
  - **中文**：元素不能用化学反应分成别的物质。
```

定义块：

```markdown
**Definition｜定义**：A **chemical symbol** is a one- or two-letter shorthand…
**中文**：元素符号是全世界通用的 1–2 个字母缩写，表示一种元素。
```

要求：
- 英文段是**完整、可独立阅读的正式英文**，不是中式英语，也不是中文的逐字直译。
- 中文段是**完整译文**，不是摘要。长度与英文段相当。
- 术语首次出现写 `English（中文）`，之后单独用英文即可。

## 3. 表格

表头双语、英文在前：`| Rule｜规则 | Explanation｜说明 | Correct ✓ | Incorrect ✗ |`
单元格：英文为主，必要时括注中文 `cobalt（钴）`。

## 4. 保留不动的东西

- **SVG 引用必须原样保留文件名**，只改 alt 文字为 `Fig. X-Y　English｜中文`：
  `![Fig. 2-1　Reading a Cell｜周期表方格怎么读](../assets/figures/ch02-periodic-table-cell.svg)`
  不得新增、删除、改名的图片。
- **代码块**（公式、逐步解题）保留，只把里面的中文注记改成 `English｜中文`。
- **超纲内容**一律标 `【🔭 Extension → Science 10】`（英文在前）。
- **Curricular Competency** 保留方括号标记：`[Processing and analyzing] …｜处理与分析…`
- 每章结尾固定 `## 10. Connection to the Big Idea｜回扣核心概念`。
- 章首元信息块（大纲对应 / 课时 / 生成时间）保留，标签英文在前：
  `> 🗂️ **Content Alignment｜大纲对应**：…`

## 5. 提示块 emoji（沿用现有体系，标签英文在前）

⚠️ Misconception｜易错 · 💡 Tip｜口诀 · 📏 Rule｜规则 · 🎯 Big Idea｜核心概念 ·
👩‍🏫 Teacher｜教师 · 🔭 Extension｜超纲 · ⏱️ Periods｜课时 · 🗂️ Meta｜元信息 ·
🌐 Bilingual｜双语 · ✏️ Example｜例题 · 🔍 Self-check｜自检 · 🧪 Lab｜实验 ·
⏭️ Preview｜预告 · 🔗 Cross-ref｜参见

## 6. 化学命名（BC 官方口径，不可改）

- 用 **aluminium**（不是 aluminum）。
- 英文 `metal + non-metal-ide`（sodium chloride）；中文 `非金属 + 化 + 金属`（氯化钠）。这一对照必须讲清楚。
- Fe²⁺ iron(II) 亚铁离子 / Fe³⁺ iron(III) 铁离子。
- semi-metal（教材常用 metalloid）= 类金属。

## 7. 不要做的事

- 不要把内容压缩成提纲——篇幅应与原章相当或略长（英文 + 中文对照后约 1.3–1.5 倍）。
- 不要在正文里加"本节已改写为英文版"这类元叙述。
- 不要改章节编号、题目编号、分值。
