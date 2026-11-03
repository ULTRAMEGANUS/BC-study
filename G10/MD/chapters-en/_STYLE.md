# G10/MD/chapters-en/ 体例（English-primary · Chinese-at-key-points）

读者：母语为中文、在 BC 省读 Science 10 的学生。**英文承载正文（叙述、专有名词、推导）；关键部分中英对照（定义、规则、结论、易错判据）；解释性内容可用中文（难点、类比、技巧）。**

> 📌 **本文件 2026-11-03 新建**，与 `G11/md/chapters-en/_STYLE.md` 同一套体例（全库统一口径，见仓库根 `00_输出规则_Output_Rules.md`）。
> 📌 **现状提示**：`chapters-en/` 目前为空；G10 已有的 2 章在 `chapters-cn/`（中文在前版）。本规约自 2026-11-03 起约束**新写的英文版章节**，不回溯改已有中文版。
> ⛔ 英文版与中文版 md **同名**，导出 PDF 必须分目录（`pdf/EN/` vs `pdf/CN/`），否则互相覆盖。

## 1. 标题（决定 PDF 书签，务必严格照做）

```markdown
# Ch.1 — From Science 9 to Science 10: Atoms, Ions and Formulas
## Chapter 1 · From Science 9 to Science 10: Atoms, Ions and Formulas｜第 1 章　从 Science 9 到 Science 10：原子、离子与化学式

## 1. Content Alignment｜大纲对应
### 3.1 Ionic Charge from the Periodic Table｜由周期表位置读离子电荷
### Table 1-1　Ionic vs Molecular Compounds｜离子化合物与分子化合物
### Fig. 1-1　Reading a Periodic Table Cell｜周期表方格怎么读
### Example 1-1　Formula → Name with a Multivalent Metal｜化学式 → 含变价金属的命名
### Activity 1-1　Ion Charge Sprint｜离子电荷速查赛
```

规则：
- **英文在前，中文在后**，中间用全角竖线 `｜`（U+FF5C）分隔，两边不加空格。
- 十节标题一律英文在前：`## 1. Content Alignment｜大纲对应` … `## 10. Connection to the Big Idea｜回扣核心概念`。
- 图/表/例题/活动编号统一英文：`Fig. 1-1`、`Table 1-1`、`Example 1-1`、`Activity 1-1`（与 G11 一致，不再用「表 1-1」）。
- 标题层级：H1 章英文名 / H2 章名双语 / H2 节 / H3 小节。

## 2. 正文：英文承载，关键处对照，解释可中文

**英文写正文；关键部分中英对照；解释性内容可用中文。** 不逐段翻译全文。

```markdown
An **ion** is an atom or group of atoms that has gained or lost electrons and therefore carries a net charge.
**中文**：**离子**是得到或失去电子、因而带净电荷的原子或原子团。

> 💡 **Tip｜口诀**：主族元素电荷 = 族序数（金属失电子）或 8 − 族序数（非金属得电子）。

> ⚠️ **Misconception｜易错**：FeCl₂ 与 FeCl₃ 不是"随便写"——铁有 +2/+3 两种价态，必须用 Roman numeral 区分（iron(II) / iron(III)）。
```

规则：
- **英文承载正文**：叙述、专有名词、推导步骤、例题讲解用英文完整书写，能独立读懂，不是逐字直译。
- **关键部分给中英对照**（英文 + 一句中文紧接）：
  1. **定义**（`**Definition｜定义**` 块）；
  2. **核心概念/规则/公式**的首次陈述（如命名规则、配平步骤、六类反应判据）；
  3. **结论句**——每节末尾那句"所以……"的判断；
  4. **易错判据**（区分离子/共价、单质/化合物这类一句话判据）。
- **解释性内容可用中文**：难点拆解、类比、记忆口诀、考场动作、为什么容易错——放 `💡 Tip｜口诀`、`⚠️ Misconception｜易错`、`👩‍🏫 Teacher｜教师` 块或短段落，1–3 行。
- **不逐段翻译**：不允许每个英文段都配一整段中文译文。
- 术语首次出现写 `English（中文）`，之后单独用英文即可。

➕ **第 9 节 Assessment 硬规则**——**逐题逐答全中文对照**（比 §2 更严，练习与核对需要）：
1. 题目下方用 `- **中文**：…`（空一行后）；答案列表项下用两格缩进的 `**中文**：…` 子项。
2. **题与题、答案与答案之间必须空一行**，连排会被渲染合并成一段。
3. 化学式、方程式、单位不翻译；题目里的数字与符号在中文行原样保留。

## 3. 表格

表头双语、英文在前：`| Item｜项目 | Content｜内容 |`。
单元格：英文为主，必要时括注中文 `cobalt（钴）`。

## 4. 保留不动的东西

- **SVG 引用必须原样保留文件名**，只改 alt 文字为 `Fig. X-Y　English｜中文`。
- **代码块**（配平流程、逐步解题）保留，只把中文注记改成 `English｜中文`。
- **超纲内容**一律标 `【🔭 Extension → Chemistry 11】`（或 `Physics 11`），英文在前，**不作主内容、不出练习**。
- **Curricular Competency** 保留方括号标记：`[Planning and conducting] …｜计划与实施…`
- 每章结尾固定 `## 10. Connection to the Big Idea｜回扣核心概念`，标明回扣 B1–B4 哪一条。
- 章首元信息块保留，标签英文在前：`> 🗂️ **Content Alignment｜大纲对应**：…`

## 5. 提示块 emoji（全库统一 14 个，标签英文在前）

⚠️ Misconception｜易错 · 💡 Tip｜口诀 · 📏 Rule｜规则 · 🎯 Big Idea｜核心概念 ·
👩‍🏫 Teacher｜教师 · 🔭 Extension｜超纲 · ⏱️ Periods｜课时 · 🗂️ Meta｜元信息 ·
🌐 Bilingual｜双语 · ✏️ Example｜例题 · 🔍 Self-check｜自检 · 🧪 Lab｜实验 ·
⏭️ Preview｜预告 · 🔗 Cross-ref｜参见 · 🔢 Sig Figs｜有效数字

## 6. 化学口径（BC 官方 + 本课程约定，不可改）

- 用 **aluminium**（不是 aluminum）；硫系正文用 **sulf-**（sulfide/sulfate/sulfuric），首次出现可并列 `sulph-`。
- 英文 `metal + non-metal-ide`（sodium chloride）；中文 `非金属 + 化 + 金属`（氯化钠）。这一对照必须讲清楚并给错误示范。
- Fe²⁺ iron(II) 亚铁离子 / Fe³⁺ iron(III) 铁离子；semi-metal（metalloid）= 类金属。
- **Science 10 只做定性判断 + 配平 + 类型识别 + 现象预测**，不做摩尔计算（摩尔、浓度、pH 计算一律标超纲）。
- 计算类内容（如稀溶液配制）带单位书写，按有效数字保留位数。

## 7. 不要做的事

- 不要把内容压缩成提纲——篇幅由内容决定，不靠双语膨胀。
- 不要在正文里加"本节已改写为英文版"这类元叙述；不要出现整段中文译文（见 §2）。
- 不要改章节编号、题目编号、分值。
- ✅ **实验安全内容照框架全收**：学校规则、WHMIS 符号、设施定位写进对应实验章节与附录 E。
- ⛔ 不要把 `G10/CHEM10 rev/` 的原卷答案直接照抄——原卷有手写笔误（如 `Ag₂C₂O₄` 写成 "silver dichromate"），全解以正确化学为准，并单列"原卷易错点对照"。
