# G11/md/chapters-en/ 体例（English-primary · Chinese-gloss）

读者：母语为中文、在 BC 省读 Chemistry 11 的学生。**英文是主体叙述语言，中文是紧随其后的对照解释。**
本规范沿用 `G9/MD/chapters-en/_STYLE.md`，G11 新增项以 ➕ 标出。

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

## 2. 正文：英文段 + 中文段

**每一个英文段落后面紧跟一个中文段落**，中文段以 `**中文**：` 开头：

```markdown
A **significant figure** is a digit in a measurement that carries meaning about its precision.

**中文**：**有效数字**是测量值中携带精度信息的有意义数字。
```

列表项同理，中文用**缩进的子项**：

```markdown
- Only measured values count; exact counts and defined constants do not.
  - **中文**：只有**测量值**才计有效数字；精确计数与定义常数不计。
```

定义块：

```markdown
**Definition｜定义**：**Molar mass** is the mass of one mole of a substance, in g/mol.
**中文**：**摩尔质量**是 1 摩尔物质的质量，单位 g/mol。
```

要求：
- 英文段是**完整、可独立阅读的正式英文**，不是中式英语，也不是中文的逐字直译。
- 中文段是**完整译文**，不是摘要。长度与英文段相当。
- 术语首次出现写 `English（中文）`，之后单独用英文即可。

➕ **第 9 节 Assessment 硬规则（Ch.1 教训）**：
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

- 不要把内容压缩成提纲——篇幅应与中文版相当或略长（英文 + 中文对照后约 1.3–1.5 倍）。
- 不要在正文里加"本节已改写为英文版"这类元叙述。
- 不要改章节编号、题目编号、分值。
- ⛔ 不要写实验安全内容（LAB SAFTY 素材本课程不采用）。
