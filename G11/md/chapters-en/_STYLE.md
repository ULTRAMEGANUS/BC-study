# G11/md/chapters-en/ 体例（English-primary · Chinese-gloss）

读者：母语为中文、在 BC 省读 Chemistry 11 的学生。**英文承载正文（含定义、专有名词、推导）；中文只用来解释难点、易错点、坑、提示与技巧。**
本规范沿用 `G9/MD/chapters-en/_STYLE.md`，G11 新增项以 ➕ 标出。

> 🔄 **2026-11-03 政策变更**：由「逐段英中对照」改为「英文为主 + 关键处对照 + 解释可中文」。
> 适用范围：**G11 新写或大改的章节**。已完成的 14 章**保持原样不动**（2026-11-03 用户决定），不回溯改造。

## 1. 标题（决定 PDF 书签，务必严格照做）

```markdown
# Ch.1 — From Science 10 to Chemistry 11: Review and Quantitative Tools
## Chapter 1 · From Science 10 to Chemistry 11｜第 1 章　从 Science 10 到 Chemistry 11：复习与量化工具

## 1. Content Alignment｜大纲对应
### 3.1 Significant Figures｜有效数字
### Table 1-1　Ionic vs Covalent｜离子化合物与共价化合物
### Fig. 1-1　The Three Bridges of the Mole｜摩尔三桥
### Example 1-1　Mass → Moles｜质量 → 摩尔
### Activity 1-1　Ion Charge Sprint｜离子电荷速查赛
```

规则：
- **英文在前，中文在后**，中间用全角竖线 `｜`（U+FF5C）分隔，两边不加空格。
- 图/表/例题/活动的编号在英文版写 `Fig. 1-1`、`Table 1-1`、`Example 1-1`、`Activity 1-1`。
- 标题层级：H1 章英文名 / H2 章名双语 / H2 节 / H3 小节。

## 2. 正文：英文承载，关键处对照，解释可中文

**英文写正文；关键部分中英对照；解释性内容可用中文。** 不再逐段翻译全文。

```markdown
A **significant figure** is a digit in a measurement that carries meaning about its precision.
**中文**：**有效数字**是测量值中携带精度信息的数字。

> 💡 **Tip｜口诀**：非零必算，夹零算，前导零不算，末尾零看小数点。

> ⚠️ **Misconception｜易错**：1200 与 1200. 精度不同——后者末尾零有效（trailing zeros after a decimal point are significant）。
```

规则：
- **英文承载正文**：叙述、专有名词、推导步骤、例题讲解用英文完整书写，能独立读懂，不是逐字直译。
- **关键部分给中英对照**（英文 + 一句中文紧接）：
  1. **定义**（`**Definition｜定义**` 块）；
  2. **核心概念/规则/公式**的首次陈述（如 Le Chatelier、IUPAC 编号规则、sig figs 三规则）；
  3. **结论句**——每节末尾那句"所以……"的判断；
  4. **易错判据**（区分醛/酮、醇/酚这类一句话判据）。
- **解释性内容可用中文**：难点拆解、类比、机制直觉、记忆口诀、考场动作、为什么容易错——放 `💡 Tip｜口诀`、`⚠️ Misconception｜易错`、`👩‍🏫 Teacher｜教师` 块或短段落，1–3 行。
- **不再逐段翻译**：不允许每个英文段都配一整段中文译文（整章译文 = 违规）。
- 术语首次出现写 `English（中文）`，之后单独用英文即可。

➕ **第 9 节 Assessment 硬规则（Ch.1 教训）**——**本节的英中对照继续保留**，是 §2 新政策的唯一例外（练习与核对需要）：
1. **每道题、每条答案必须紧跟中文对照**——题目下方用 `- **中文**：…`（空一行后）；
   答案列表项下用两格缩进的 `**中文**：…` 子项。评分要点、量规里的英文行同样处理。
2. **题与题、答案与答案之间必须空一行**。相邻两行 `**A1.**…` / `**A2.**…` 连排不空行，
   markdown 渲染会合并成一段（G9/G10 的 goldmark 内核都会这样）。
3. 化学式、方程式、单位不翻译；题目里的数字与符号在中文行原样保留。

## 3. 表格

表头双语、英文在前：`| Item｜项目 | Content｜内容 |`。
单元格：英文为主，必要时括注中文 `cobalt（钴）`。

## 4. 保留不动的东西

- **SVG 引用必须原样保留文件名**，只改 alt 文字为 `Fig. X-Y　English｜中文`。
- **代码块**（计算流程、量纲分析链式写法）保留，只把中文注记改成 `English｜中文`。
- **超纲内容**一律标 `【🔭 Extension → Chemistry 12】`（英文在前）。
- **Curricular Competency** 保留方括号标记：`[Planning and conducting] …｜计划与实施…`
- 每章结尾固定 `## 10. Connection to the Big Idea｜回扣核心概念`。
- 章首元信息块保留，标签英文在前：`> 🗂️ **Content Alignment｜大纲对应**：…`

## 5. 提示块 emoji（沿用现有体系，标签英文在前）

⚠️ Misconception｜易错 · 💡 Tip｜口诀 · 📏 Rule｜规则 · 🎯 Big Idea｜核心概念 ·
👩‍🏫 Teacher｜教师 · 🔭 Extension｜超纲 · ⏱️ Periods｜课时 · 🗂️ Meta｜元信息 ·
🌐 Bilingual｜双语 · ✏️ Example｜例题 · 🔍 Self-check｜自检 · 🧪 Lab｜实验 ·
⏭️ Preview｜预告 · 🔗 Cross-ref｜参见 · 🔢 Sig Figs｜有效数字

## 6. 化学口径（BC 官方 + 本课程约定，不可改）

- 用 **aluminium**（不是 aluminum）；硫系正文用 **sulf-**（sulfide/sulfate/sulfuric）。
- 英文 `metal + non-metal-ide`（sodium chloride）；中文 `非金属 + 化 + 金属`（氯化钠）。
- Fe²⁺ iron(II) 亚铁离子 / Fe³⁺ iron(III) 铁离子；semi-metal（metalloid）= 类金属。
- ➕ **有机命名英中顺序基本对应**（propane 丙烷；2-methylbutane 2-甲基丁烷），与无机命名**顺序相反**不同——涉及命名时两栏对照。
- ➕ **Sig figs 全课程硬要求**：任何计算结果必须按有效数字规则保留位数；量纲分析必须带单位书写。

## 7. 不要做的事

- 不要把内容压缩成提纲——篇幅由内容决定，不靠双语膨胀（不再按"英文 × 1.5"折算）。
- 不要在正文里加"本节已改写为英文版"这类元叙述；不要出现整段中文译文（见 §2）。
- 不要改章节编号、题目编号、分值。
- ✅ **实验安全内容照框架全收**（2026-11-03 用户确认）：WHMIS 符号、本校硬规矩（pre-lab 未完成不得进实验室、禁凉鞋短裤隐形眼镜、室内禁饮食、事故立即报告、补做实验每月一次周三早 8:30–9:30）、实验室设施定位，写在 Ch.1 与附录 E；原 `LAB SAFTY/` 源文件已移除，内容以正文为准。
