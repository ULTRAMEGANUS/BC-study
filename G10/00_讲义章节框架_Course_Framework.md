# BC Science 10 · Chemistry — Bilingual Lecture Framework
## 不列颠哥伦比亚省 十年级科学 · 化学部分 — 英中对照讲义章节框架

> **根目录 Root**: `canada chemical/G10/`
> **依据来源 Source**: [BC Ministry of Education — Science 10 Curriculum](https://curriculum.gov.bc.ca/curriculum/science/10/core)（官方现行大纲，2026-09-22 复核）
> **素材对齐 Alignment**: `G10/CHEM10 rev/SCI 10 REV WORKSHEET 0–3`（学校 Chem 11 课前发的 Science 10 复习练习，含答案页）
> **版本 Version**: v1.0（框架骨架 / framework skeleton）
> **语言体例 Convention**: 每个词条先英文后中文，格式 `English（中文）`；专业术语首次出现时双标注。

---

## 0. 课程定位与大纲依据｜Curriculum Position & Official Standards

### 0.1 官方 Big Idea（核心概念）— 化学相关

| # | English (official, verbatim) | 中文 | 作用 |
|---|---|---|---|
| B1 | **Energy change is required as atoms rearrange in chemical processes.** | 原子在化学过程中重排时，必然伴随能量变化。 | **化学单元的唯一 Big Idea**，全册一切内容回扣此句 |
| B2 | **Energy is conserved, and its transformation can affect living things and the environment.** | 能量守恒，其转化会影响生物与环境。 | 能量单元 Big Idea；Ch.6 与 Ch.10 需与它对接 |
| — | *DNA is the basis for the diversity of living things.* | 生物部分 Big Idea | 与本册化学部分无关，不涉及 |
| — | *The formation of the universe can be explained by the big bang theory.* | 天文部分 Big Idea | 与本册化学部分无关，不涉及 |

> ⚠️ **注意分工**：BC Science 10 是**综合科学**课，含生物（DNA/遗传）、化学、物理（能量）、天文（宇宙）四个单元。
> **本讲义只做化学单元**（B1 主线，B2 部分对接），文件名与目录均不承诺覆盖其余单元。

### 0.2 官方 Content（内容标准）— 化学部分原文

| # | English (official, verbatim) | 中文 | 对应章节 |
|---|---|---|---|
| C1 | **rearrangement of atoms in chemical reactions** | 化学反应中原子的重排 | Ch.2 – Ch.5 |
| C2 | **acid-base chemistry** | 酸碱化学 | Ch.7 |
| C3 | **law of conservation of mass** | 质量守恒定律 | Ch.4 |
| C4 | **energy change during chemical reactions** | 化学反应中的能量变化 | Ch.6 |
| C5 | **practical applications and implications of chemical processes, including First Peoples knowledge** | 化学过程的实际应用与影响（含原住民知识） | Ch.9 |
| C6 | **nuclear energy and radiation** | 核能与辐射 | Ch.10 |
| — | *(law of conservation of energy; potential and kinetic energy; transformation of energy; local and global impacts of energy transformations from technologies)* | 能量守恒 / 动能势能 / 能量转化 / 技术影响 | 属**能量单元**，仅 Ch.6·Ch.10 接口处引用 |

> 📌 化学单元在官方 Content 里就是 **C1–C5** 五条；**C6 核能与辐射** 与化学相邻（涉及原子核与同位素），本讲义收录并明确标注其归属。

### 0.3 官方 Curricular Competencies（课程能力）— 全学科共用

| English | 中文 |
|---|---|
| Questioning and predicting | 提问与预测 |
| Planning and conducting | 计划与实施（含实验安全） |
| Processing and analyzing data and information | 数据处理与信息分析 |
| Evaluating | 评估（误差、模型局限、二手资料可信度） |
| Applying and innovating | 应用与创新 |
| Communicating | 交流（科学语言、图表、证据化论证） |

> 每章的"评估"栏需同时覆盖 **Content**（知识）与 **Competency**（能力）两条线。

### 0.4 纵向衔接与超纲红线｜Vertical Articulation & Out-of-Scope Lines

| 年级 | 化学相关内容 | 本讲义的处理 |
|---|---|---|
| **Science 9**（先修） | 元素与周期表；电子排布（玻尔图）决定化学性质；离子与路易斯点式；离子/分子化合物命名与化学式 | **不重教**，压缩为 **Ch.1 衔接复习**（1 章），只补 Science 10 直接要用的部分 |
| **Science 10**（本册） | C1–C6（见 0.2） | 主体内容 |
| **Chemistry 11**（后接·超纲红线） | mole 摩尔、化学计量 stoichiometry（质量-质量计算）、溶液浓度 molarity、滴定 titration、pH 计算 `pH = −log[H⁺]`、理想气体定律、有机化学、氧化还原半反应、电子层精细结构与周期律定量描述 | ⛔ **一律不写**；仅在正文出现必要时标 `【Extension → Chemistry 11】`，且不做练习 |
| **Chemistry 12**（更远） | 化学平衡 equilibrium、溶解度积 Ksp、反应动力学定量、电化学 | ⛔ 同上 |

> **判据（写正文时自检）**：凡是需要"已知质量求物质的量"或"用浓度算 pH"的题，一律超纲。
> Science 10 只做**定性判断 + 配平 + 类型识别 + 现象预测**，不做摩尔计算。

---

## 1. 讲义总体结构｜Overall Structure

```
G10/                                  根目录
├─ 00_讲义章节框架_Course_Framework.md   ← 本文件（框架与总纲）
├─ README.md                          项目说明与使用指南
├─ CHEM10 rev/                        学校原始复习练习单（只读素材，不改动）
├─ MD/                                md 源与素材
│   ├─ chapters-cn/                   11 章正文·中文在前
│   ├─ chapters-en/                   11 章正文·英文在前（第二版，见 5.3）
│   ├─ appendices-cn/                 附录 A–E
│   └─ assets/                        图表、练习单、脚本与数据
│       ├─ figures/                   SVG 配图（脚本生成）
│       ├─ printables/                A4 练习单
│       └─ source/                    生成脚本 + CSV（必须建，否则产物不可再生）
└─ pdf/                               ⛔ 本年级**全部 PDF 产物的唯一出口**（未经点名不生成）
    ├─ CN/                            中文在前版各章 PDF + 合订本
    ├─ EN/                            英文在前版各章 PDF + 合订本（与 CN 同名，必须分目录）
    └─ *_EN-CN.pdf                    英中对照复习卷等单件产物直接放这一层
```

> **PDF 输出目录约定（2026-09-24 定，全项目适用）**：`<年级>/pdf/` 是该年级 PDF 的唯一输出位置。
> 不要与原件同目录、不要塞进 `MD/`。G9 → `G9/pdf/`、G10 → `G10/pdf/`、G11 → `G11/pdf/`。
> 即脚本里「读」与「写」必须是两个常量（`REV`/`SRC` 与 `OUT`），路径按脚本自身位置推导，不写死绝对路径。

### 单元划分｜Unit Map

| 部分 Part | 主题 Theme | 章节 Chapters | 课时（建议） |
|---|---|---|---|
| **Part 0** | 衔接与预备 Bridge & Prerequisite | Ch.1 | 2 |
| **Part I** | 原子重排与化学方程式（→ C1 · C3） | Ch.2 – Ch.4 | 8 |
| **Part II** | 反应类型与能量变化（→ C1 · C4） | Ch.5 – Ch.6 | 6 |
| **Part III** | 酸碱化学（→ C2） | Ch.7 | 4 |
| **Part IV** | 探究、应用与核能（→ C5 · C6 · Competencies） | Ch.8 – Ch.10 | 6 |
| **Part V** | 综合复习与测评 | Ch.11 | 2 |
| **附录 Appendix** | 词汇表 / 离子表 / 命名速查 / 配平与预测速查 | A – E | — |

> 合计约 **28 课时（periods）**，对应 BC 学年中科学课化学单元约 6 周的教学量；可按学校进度压缩至 20 节。

---

## 2. 章节框架｜Chapter-by-Chapter Framework

每个章节条目统一包含 7 个字段，填充正文时保持此体例：

```
1. 大纲对应 Content alignment
2. 学习目标 Learning objectives（EN / 中）
3. 知识点要点 Key concepts（双语分级条目）
4. 核心词汇 Key vocabulary（EN ↔ 中）
5. 实验与活动 Lab / Activity
6. 常见易错点 Common misconceptions
7. 评估方式 Assessment（知识 + 能力）
```

**正文统一采用 10 节结构**（体例硬约束，与 G9 保持一致）：

```
1 Content Alignment｜大纲对应        （表格：官方条目原文 + 是否超纲）
2 Learning Objectives｜学习目标      （EN 5 条 + 中 5 条）
3 Concept Explanations｜概念解析     （3.x 分节：英文定义 → 要点 → 例子；中文只点难点）
4 Comparison Tables｜表格比对        （≥3 张，中英双语表头）
5 Diagrams & Worked Examples｜图例说明（≥3 个 SVG 图 + 逐步解析例题）
6 Key Vocabulary｜核心词汇           （表格：English / 中文 / 备注）
7 Lab / Activity｜实验与活动         （含 Curricular Competency 标注 + 安全）
8 Common Misconceptions｜常见易错点  （≥8 条：错误认识 / 正确理解）
9 Assessment｜答题评估               （A 基础 10×2 + B 应用 4×5 + C 挑战 2×10 + 完整答案 + 评分量规）
10 Connection to the Big Idea｜回扣核心概念
```

---

## Part 0 · 衔接与预备｜Bridge & Prerequisite

### Ch.1 — From Science 9 to Science 10: Atoms, Ions and Formulas
### 第 1 章　从 Science 9 到 Science 10：原子、离子与化学式

- **大纲对应 Content alignment**: 承接 Science 9「element properties as organized in the periodic table / arrangement of electrons determines compounds」；直接服务于 C1 与 C2 的最低门槛
- **课时 Periods**: 2
- **素材对齐**: `SCI 10 REV WORKSHEET 0` p1–p2（Periodic Table Tips / Diatomic Molecules / Naming / Formulas / Acids, Bases & Salts）

**学习目标 Learning objectives**
- EN: Recall the subatomic structure of an atom and how to determine ion charge from periodic table position; write formulas and names for ionic and covalent compounds, including multivalent metals and polyatomic ions; recognize acids, bases and salts by their formulas.
- 中: 回顾原子内部结构与"由周期表位置推离子电荷"的方法；书写并命名离子化合物与共价化合物（含多变价金属与多原子离子）；由化学式辨认酸、碱、盐。

**知识点要点 Key concepts**
1. 粒子与电荷（复习）: proton 质子 / neutron 中子 / electron 电子；原子中性 ⇔ 质子数 = 电子数
2. **Periodic table charge map 周期表电荷图**（本册最常用工具）:
   - Group 1 → +1；Group 2 → +2；Group 13 → +3；Group 14 → 通常不形成离子（±4 极少）
   - Group 15 → −3；Group 16 → −2；Group 17（halogens 卤素）→ −1；Group 18 → 0（noble gases 稀有气体，不形成离子）
   - **Groups 3–12（transition metals 过渡金属）→ multivalent 多变价**，电荷看罗马数字或化合物名称/化学式反推
3. **Diatomic molecules 双原子分子**（"Rule of 7" / H-7 Rule）: H₂ · N₂ · O₂ · F₂ · Cl₂ · Br₂ · I₂（+ 特殊: P₄ · S₈）
4. **Ionic compound 离子化合物** = metal + non-metal（含多原子离子）
   - 命名: 金属名 + 非金属词根 **-ide**；多变价金属加**罗马数字**；多原子离子整体当"一个原子"处理
   - 化学式: criss-cross / drop-and-swap 交叉法，总电荷为零，比例约至最简
5. **Covalent compound 分子化合物** = non-metal + non-metal；用希腊数字前缀（mono-/di-/tri-…），第二个元素必加前缀并改 **-ide**；第一个元素**永不用 mono-**
6. **Acid / Base / Salt 酸碱盐的化学式特征**:
   - Acid 酸: 化学式**以 H 开头**（HCl、H₂SO₄、H₃PO₄、CH₃COOH）
   - Base 碱: 化学式**以 OH 结尾**（NaOH、Ca(OH)₂、Mg(OH)₂）
   - Salt 盐: 金属 + 非金属的**离子化合物**（NaCl、KNO₃、CaCO₃）
7. **英中命名顺序相反**（必须明写）: 英文 `metal + non-metal-ide`（sodium chloride）；中文 `非金属 + 化 + 金属`（**氯化钠**）
8. 拼写变体说明: **aluminium / aluminum**、**sulphide / sulfide**、**sulphate / sulfate** —— 学校材料与 BC 官方/教材不完全一致，本讲义统一用 **aluminium**，遇到 -ph- 拼写在首次出现处括注。

**核心词汇 Key vocabulary**
ion 离子 · cation 阳离子 · anion 阴离子 · ion charge 离子电荷 · multivalent 多变价的 · polyatomic ion 多原子离子 · roman numeral 罗马数字 · diatomic molecule 双原子分子 · ionic compound 离子化合物 · covalent/molecular compound 共价（分子）化合物 · prefix 前缀 · acid 酸 · base 碱 · salt 盐 · criss-cross method 交叉法

**实验与活动 Lab / Activity**
- 「离子电荷速查赛」：给出族号与元素符号，10 秒内写出电荷（覆盖 1/2/13–17 族 + 常见多变价金属）。
- 「化学式配对卡」：阳离子牌 × 阴离子牌（含 SO₄²⁻、NO₃⁻、CO₃²⁻、OH⁻、PO₄³⁻、C₂O₄²⁻、CH₃COO⁻、CrO₄²⁻、ClO₃⁻），交叉法拼化学式。
- 「酸碱盐三分类」：给 20 个化学式（含 pH 与味觉描述等间接线索），分类并说明依据。

**常见易错点 Common misconceptions**
- 以为过渡金属只有一个电荷（Cu⁺/Cu²⁺、Fe²⁺/Fe³⁺ 必须靠罗马数字区分）。
- 在离子化合物上套希腊前缀（**NaCl 不能叫 sodium monochloride**）。
- 共价化合物第一个元素加了 mono-（**CO 是 carbon monoxide**，不是 monocarbon monoxide）。
- 双原子分子按单原子写方程式（H₂ 不能写成 H）。
- 中文命名顺序写反（写成"钠化氯"；正确为**氯化钠**）。
- 把 `NH₄⁺` 当金属阳离子处理却又忘了它整体带电（ammonium 铵根）。
- `Ag₂HPO₄` 这类"酸式盐"漏看 H（silver monohydrogen phosphate 磷酸氢银）。

**评估方式 Assessment**
- 知识：20 组"名称 ↔ 化学式"双向互译（含多变价与多原子离子）+ 10 个化合物 ionic / covalent 判定。
- 能力：用一个表格系统整理各族离子电荷并解释"为什么同族电荷相同"（Seek and analyze patterns / Use knowledge of scientific concepts to draw conclusions）。

---

## Part I · 原子重排与化学方程式｜Atom Rearrangement & Equations
> 对应官方 Content C1：*rearrangement of atoms in chemical reactions*；C3：*law of conservation of mass*

### Ch.2 — Chemical Reactions and Chemical Equations
### 第 2 章　化学反应与化学方程式

- **大纲对应 Content alignment**: C1（核心）
- **课时 Periods**: 2–3
- **素材对齐**: `WS1` p2 / `WS2` p1（word equations → formulas）

**学习目标 Learning objectives**
- EN: Explain a chemical reaction as a rearrangement of atoms; identify evidence of chemical change; convert a word equation into a skeleton equation and then into a balanced equation; use state symbols and reaction conditions.
- 中: 把化学反应解释为原子的重排；识别化学变化的证据；把文字方程式转成骨架方程式再配平；正确使用状态符号与反应条件。

**知识点要点 Key concepts**
1. Chemical reaction 化学反应 = 原子**重新组合**（旧键断裂、新键形成），原子种类与数目不变，只是"搭档换了"
2. Evidence of chemical change 证据: color change 变色 / gas produced 产气 / precipitate 沉淀 / temperature change 温度变化 / light 发光 / new odour 新气味
3. 方程式三级台阶: word equation 文字方程式 → skeleton equation 骨架方程式（写对化学式，系数留空）→ balanced equation 配平方程式
4. Chemical formula 化学式书写（复习 Ch.1）+ **state symbols 状态符号**: (s) solid 固 · (l) liquid 液 · (g) gas 气 · (aq) aqueous 水溶液
5. Reaction conditions 反应条件（写在箭头上/下）: heat Δ / catalyst 催化剂 / light / spark
6. Coefficient 系数 vs subscript 下标: **只能改系数，绝不动下标**
7. 阅读方程式六问: 谁反应？生成谁？状态？条件？系数比？能量？

**核心词汇 Key vocabulary**
chemical reaction 化学反应 · reactant 反应物 · product 生成物 · word equation 文字方程式 · skeleton equation 骨架方程式 · balanced equation 配平方程式 · coefficient 系数 · subscript 下标 · state symbol 状态符号 · aqueous 水溶液 · precipitate 沉淀 · catalyst 催化剂

**实验与活动 Lab / Activity**
- 「原子搬家」实物演示：用两种颜色磁贴代表原子，动手"拆开再重组"，数出反应前后原子数。
- 方程式翻译工作坊：10 句英文文字描述 → 写出化学式 → 配平（含状态符号）。
- 化学变化观察站：NaHCO₃ + CH₃COOH、Pb(NO₃)₂ + KI、Mg 燃烧，记录证据并写方程式。

**常见易错点 Common misconceptions**
- 通过改下标来"配平"（改变了物质本身）。
- 忘记双原子分子（写 H + O → H₂O）。
- 状态符号乱标（把食盐水写成 NaCl(l)）。
- 系数写在下标位置（Fe₂O₃ 与 2Fe₂O₃ 混淆）。
- 把"溶解""熔化"当化学变化。

**评估方式 Assessment**
- 知识：10 个文字方程式 → 化学式 → 配平；判断题"这是化学变化吗，证据是什么"。
- 能力：用原子模型/磁贴图解释原子守恒（Formulate models / Communicate with scientific representations）。

---

### Ch.3 — Balancing Chemical Equations
### 第 3 章　化学方程式的配平

- **大纲对应 Content alignment**: C1（核心技能）
- **课时 Periods**: 3
- **素材对齐**: `WS1` p2 / `WS2` p2 / `WS3` p2（大量配平题，含"复杂配平"）

**学习目标 Learning objectives**
- EN: Balance chemical equations systematically; choose an element order that minimises rework; check the balance by counting atoms (and charge for ions); handle fractional coefficients and polyatomic groups.
- 中: 系统化地配平化学方程式；选择合理的元素顺序以减少返工；通过数原子（对离子还数电荷）验算；处理分数系数与多原子原子团。

**知识点要点 Key concepts**
1. 配平唯一依据: **Law of conservation of mass 质量守恒** —— 反应前后每种元素的原子数相等
2. 四步法（本讲义主推的稳定流程）：
   - ① 写对全部化学式（这一步错了后面全错）
   - ② 找**只出现在一个反应物与一个生成物**中的元素先配（通常金属 → 非金属 → 氢 → 氧）
   - ③ 成对出现的原子团（SO₄、NO₃、PO₄、C₂O₄、CH₃COO）**整体当一个单位**配
   - ④ 最后配 O 与 H；必要时用分数系数过渡再整体乘最小公倍数
3. 技巧:
   - 含 C/H/O 的燃烧反应口诀：**先配 C → 再配 H → 最后用 O 收尾**
   - 出现奇数/偶数原子（如 O₂）→ 先给奇数一侧乘 2
   - 有 H₂O 与 O₂ 同时出现的组合，最后统一配 O
4. 验算: 列一张各元素计数表（左/右对照），全等才算完；离子方程式还要验电荷守恒
5. ⛔ 红线: **不要背答案、不要试凑着改下标**；所有配平都可用上面四步推出来

**核心词汇 Key vocabulary**
balance 配平 · conserve 守恒 · coefficient 系数 · fractional coefficient 分数系数 · polyatomic group 多原子原子团 · combustion 燃烧 · reactant 反应物 · product 生成物 · verify 验算

**实验与活动 Lab / Activity**
- 「配平接力赛」：四人一组，每人负责一步（写化学式 → 先配金属 → 手配原子团 → 收尾验算），完成后互查。
- 「找出错在哪」：给 8 个"已配平"的方程式，找出错误类型（改了下标 / 系数未约简 / 漏了双原子分子）。
- 用彩色磁贴搭出 `C₂₅H₅₂ + 38 O₂ → 25 CO₂ + 26 H₂O`（WS1 原题）感受"大数配平"。

**常见易错点 Common misconceptions**
- 配平后忘记把系数约至**最简整数比**（4 Na + 2 O₂ → 4 Na₂O 应写成 2 Na₂O…注意 Na₂O 系数应约简）。
- 火焰/燃烧反应最后配 O 时反复改动前面已配好的 C、H。
- 把多原子团拆成单个原子去配，导致 SO₄ 被写坏。
- 认为"系数必须最小"而拒绝合法的分数系数过渡步骤（最终结果才要求整数）。
- 只数了原子忘了电荷（离子方程式）。

**评估方式 Assessment**
- 知识：15 道配平（含燃烧、含多原子团、含分数过渡）；`WS2` p2 的复杂配平题作为挑战题。
- 能力：写出并说明自己的配平顺序与理由（Communicating / evidence-based reasoning）。

---

### Ch.4 — The Law of Conservation of Mass
### 第 4 章　质量守恒定律

- **大纲对应 Content alignment**: C3（核心）
- **课时 Periods**: 1–2

**学习目标 Learning objectives**
- EN: State the law of conservation of mass and explain it in terms of atoms; use mass data to check whether a reaction is complete; explain apparent mass changes (open vs closed system, gas escape).
- 中: 陈述质量守恒定律并用原子观点解释；用质量数据判断反应是否完全；解释"看起来质量变了"的现象（敞开/封闭体系、气体逸出）。

**知识点要点 Key concepts**
1. Statement 表述: 在任何化学变化中，**物质总质量不变**（反应前后质量相等）
2. 微观解释: 原子种类不变、数目不变、每个原子质量不变 → 只是重新组合
3. 与配平的关系: 配平就是质量守恒在符号层面的表现
4. 开放体系 closed vs open system: 镁条燃烧质量"变轻"（白烟 MgO 逸出）/ 变重（结合空气中的 O₂）；钢铁生锈变重
5. 实验验证: 密闭容器内反应前后称重（Na₂CO₃ + HCl 密闭）；`WS` 无关，属课本经典实验
6. 应用: 由"消失的质量"推断逸出气体的质量（不做摩尔计算，只做简单加减）

**核心词汇 Key vocabulary**
law of conservation of mass 质量守恒定律 · closed system 封闭体系 · open system 敞开体系 · mass 质量 · reactant 反应物 · product 生成物 · atom count 原子计数

**实验与活动 Lab / Activity**
- 密闭体系称重：锥形瓶 + 气球（NaHCO₃ + CH₃COOH），反应前后称重，差值 ≈ 0；再打开气球放气后称重，解释差值。
- 钢丝绒生锈 48 小时质量变化记录（含变量控制）。
- 数据推理题：已知反应物与部分生成物质量，求某种气体质量。

**常见易错点 Common misconceptions**
- "燃烧后灰烬变轻 → 质量不守恒"（气体逸出未计入）。
- 把质量守恒当成"体积守恒"。
- 认为反应"消失"的物质真的没了（原子只是换了搭档）。
- 忽略体系开放性直接拿台秤数据下结论。

**评估方式 Assessment**
- 知识：给数据算未知质量；判断题分析质量变化原因。
- 能力：设计一个能证明质量守恒的密闭实验（变量、步骤、判据、误差来源）。

---

## Part II · 反应类型与能量变化｜Reaction Types & Energy Change

### Ch.5 — Types of Chemical Reactions
### 第 5 章　化学反应的类型

- **大纲对应 Content alignment**: C1（核心）
- **课时 Periods**: 3–4
- **素材对齐**: `WS0` p2 表格（6 类与一般式）/ `WS1` p2 / `WS2` p2 / `WS3` p2（分类 + 预测产物）

**学习目标 Learning objectives**
- EN: Classify reactions into the six types taught in BC Science 10; write the general formula of each; predict products and use the activity series and solubility rules to judge whether a single/double replacement will occur.
- 中: 把反应归入 BC Science 10 要求的六类；写出各自的一般式；预测生成物，并用**金属活动性顺序**与**溶解性规则**判断置换/复分解能否发生。

**知识点要点 Key concepts**

| # | Type 类型 | English | 一般式 General formula | 中文要点 |
|---|---|---|---|---|
| 1 | 合成 | Synthesis / Combination | A + B → AB | 多种→一种 |
| 2 | 分解 | Decomposition | AB → A + B | 一种→多种（常需加热/电） |
| 3 | 单置换 | Single Replacement | A + BC → AC + B | 金属换金属、金属换氢 |
| 4 | 双置换 | Double Replacement | AB + CD → AD + CB | 正负离子"换配偶"，常生成沉淀/水/气 |
| 5 | 中和 | Neutralization | acid + base → salt + water | 双置换的特例 |
| 6 | 燃烧 | Combustion | hydrocarbon + O₂ → CO₂ + H₂O | 只针对含 C/H（含 O）燃料 |

1. 判定顺序（本讲义推荐的判据树）：先看反应物种类数 → 再看是否是酸+碱 → 再看是否含 O₂ 与燃料 → 最后用一般式核对
2. **Activity series 金属活动性顺序**（用于单置换）: K > Na > Ca > Mg > Al > Zn > Fe > Pb > Cu > Ag > Au（越靠前的金属越"主动"，能把它后面的金属从化合物里换出来）
3. **Solubility rules 溶解性规则**（用于双置换/复分解是否能"明显发生"）: 生成 insoluble 沉淀 / water / gas 才算真正发生
4. 常见沉淀: AgCl、PbI₂、BaSO₄、CaCO₃、PbCl₂ 等
5. 燃烧产物: 只含 C/H → CO₂ + H₂O；含 C/H/O → CO₂ + H₂O；含 N 的燃料还要写 N₂（WS2 有此类题）
6. ⚠️ 分类**不唯一**时要能说理由（如中和也是双置换）

**核心词汇 Key vocabulary**
synthesis 合成 · decomposition 分解 · single replacement 单置换 · double replacement 双置换 · neutralization 中和 · combustion 燃烧 · general formula 一般式 · activity series 金属活动性顺序 · solubility 溶解性 · precipitate 沉淀 · hydrocarbon 烃/碳氢化合物 · reactant 反应物 · product 生成物

**实验与活动 Lab / Activity**
- 「六类反应证据站」：6 个反应现场（Mg + O₂、CaCO₃ 加热、Cu + AgNO₃、Pb(NO₃)₂ + KI、HCl + NaOH、CH₄ 燃烧），学生分类 + 写方程式。
- 「预测-验证」：先只用活动性顺序与溶解性规则预测"会不会反应"，再做实验验证，写预测准确率报告。
- 反应类型卡片分类赛（含干扰项：中和 vs 双置换）。

**常见易错点 Common misconceptions**
- 把中和反应漏掉（它同时是双置换）。
- 燃烧反应写成"燃料 + O₂ → 一种氧化物"（忽略了 CO₂ 与 H₂O 两种产物）。
- 单置换不检查活动性（Cu + HCl 不反应，很多学生照样写方程式）。
- 双置换不检查沉淀/水/气（以为写出方程式就算反应发生）。
- 分解反应当成单置换（AB → A + B 与 A + BC → AC + B 混淆）。
- 忘记助燃的 O₂ 来自空气，写成"燃料 → CO₂ + H₂O"。

**评估方式 Assessment**
- 知识：20 个方程式分类；10 个"预测产物 + 配平"；5 个"能否发生"判断。
- 能力：用活动性顺序与溶解性规则做预测并说明依据（Seek and analyze patterns / Evaluate predictions against evidence）。

---

### Ch.6 — Energy Change in Chemical Reactions
### 第 6 章　化学反应中的能量变化

- **大纲对应 Content alignment**: C4（核心）；对接 B2
- **课时 Periods**: 2–3

**学习目标 Learning objectives**
- EN: Distinguish exothermic from endothermic reactions using evidence; interpret energy-level diagrams; explain activation energy; relate bond breaking/forming to energy absorbed/released; connect to real applications.
- 中: 用证据区分放热与吸热反应；读懂能量变化图；解释活化能；把"断键吸能、成键放能"与总能量变化联系起来；联系真实应用。

**知识点要点 Key concepts**
1. Exothermic 放热: 释放能量，周围温度升高（燃烧、中和、生石灰加水、手暖袋）
2. Endothermic 吸热: 吸收能量，周围温度降低（光合作用、热分解 CaCO₃、冰袋、电解）
3. **Energy level diagram 能量变化图**: reactant plateau / product plateau；高→低 = 放热，低→高 = 吸热
4. **Activation energy 活化能**: 引发反应所需的最低能量（"起步的门槛"）；催化剂降低活化能，不改变总能量差
5. 微观解释（简版）: 断裂旧键需**吸能**，形成新键会**放能**；两者差值决定放热或吸热
   - 【🔭 Extension → Chemistry 11】键能 key energy 的**定量计算**（用键能表算 ΔH）
6. 能量守恒（对接 B2）: 能量不会消失，只是转移或转化；反应体系放出的热进入了周围环境
7. 现实应用: 燃料选择（能量密度、产物）、自热饭盒/暖宝宝、冷敷袋、工业放热控制

**核心词汇 Key vocabulary**
exothermic 放热的 · endothermic 吸热的 · activation energy 活化能 · energy level diagram 能量变化图 · bond breaking 断键 · bond forming 成键 · catalyst 催化剂 · enthalpy 焓【Ext.】 · temperature change 温度变化

**实验与活动 Lab / Activity**
- 「温度曲线」实验：用温度计/数据采集器记录 4 个反应的温度-时间曲线（NaOH + HCl、CaO + H₂O、NH₄NO₃ + H₂O、NaHCO₃ + CH₃COOH），判定放热/吸热并画能量图。
- 「催化剂只是让你更快」：H₂O₂ 分解（加/不加 MnO₂），测温度与气泡速率，讨论"催化剂是否改变放热量"。
- 生活案例辩论：暖宝宝 vs 冰袋，用什么反应、为什么安全。

**常见易错点 Common misconceptions**
- 把"需要点燃"当成吸热反应（点燃只是提供**活化能**，燃烧本身是放热）。
- 认为吸热反应"不需要能量"。
- 认为催化剂"增加放出的热量"。
- 把温度变化与"质量变化"混为一谈。
- 认为放热反应"温度一定上升很多"（取决于体系大小与散热）。

**评估方式 Assessment**
- 知识：判定 10 个反应放热/吸热；画 4 个能量图并标注活化能。
- 能力：用实验数据（温度曲线）支持结论并提出改进（Processing and analyzing / Evaluating）。

---

## Part III · 酸碱化学｜Acid-Base Chemistry

### Ch.7 — Acids, Bases, Salts and pH
### 第 7 章　酸、碱、盐与 pH

- **大纲对应 Content alignment**: C2（核心）
- **课时 Periods**: 4
- **素材对齐**: `WS0` p2（Acids, Bases & Salts）/ `WS1` p2（分类为酸/碱/盐）/ `WS3` p1（中和反应预测）

**学习目标 Learning objectives**
- EN: Describe the properties of acids and bases; classify substances as acid, base or salt from name, formula, pH or described properties; read the pH scale; write and balance neutralization reactions; name common acids and bases.
- 中: 描述酸碱的性质；由名称、化学式、pH 或描述性质判断某物质是酸、碱还是盐；读懂 pH 标度；书写并配平中和反应；命名常见酸碱。

**知识点要点 Key concepts**
1. Properties 性质:
   - Acid 酸: sour 酸味、使蓝色石蕊变红、与活泼金属放 H₂、与碳酸盐放 CO₂、pH < 7、导电（水溶液）
   - Base 碱: bitter 苦味、滑腻 slippery、使红色石蕊变蓝、pH > 7、腐蚀性 corrosive
   - Salt 盐: 由中和反应生成，多为中性（少数水解呈酸/碱性【🔭 Ext.】）
2. **pH 标度 pH scale**: 0–14；< 7 酸、= 7 中性、> 7 碱；**每差 1 代表 10 倍**（对数关系）
   - ⛔ `pH = −log[H⁺]` 的**计算**属 Chemistry 11，只做定性比较
3. Indicators 指示剂: litmus 石蕊、phenolphthalein 酚酞（碱性变粉）、bromothymol blue、universal indicator / pH 试纸、pH meter
4. 命名:
   - 酸：HCl hydrochloric acid；H₂SO₄ sulfuric acid；HNO₃ nitric acid；H₃PO₄ phosphoric acid；CH₃COOH acetic acid
   - 碱：metal + hydroxide（NaOH sodium hydroxide、Ca(OH)₂ calcium hydroxide）
   - 二元酸无氧 → hydro-…-ic acid（HCl 盐酸）
5. **Neutralization 中和反应**: acid + base → salt + water；本质是 H⁺ + OH⁻ → H₂O
   - 例：HCl + NaOH → NaCl + H₂O；2 HCl + Ca(OH)₂ → CaCl₂ + 2 H₂O
6. 生活与安全: 抗酸药 antacid（Mg(OH)₂、CaCO₃）、食醋/柠檬酸、肥皂、胃酸、酸雨、强酸强碱的实验室安全与稀释规则（**酸入水，不是水入酸**）

**核心词汇 Key vocabulary**
acid 酸 · base 碱 · alkali 碱（可溶碱）· salt 盐 · pH · indicator 指示剂 · litmus 石蕊 · phenolphthalein 酚酞 · neutralization 中和反应 · corrosive 腐蚀性的 · electrolyte 电解质 · antacid 抗酸药 · dilute 稀释

**实验与活动 Lab / Activity**
- 「pH 巡测」：测 12 种家用液体（醋、柠檬汁、牛奶、纯净水、小苏打水、肥皂水、洗手液…）pH，排序并预测指示剂颜色。
- 「指示剂三兄弟」：石蕊 / 酚酞 / 通用指示剂对酸碱的颜色反应对照表。
- 「中和滴定（定性版）」：向 NaOH 溶液滴加酚酞，再加 HCl 至刚好褪色，记录体积趋势、写方程式（⛔ 不做浓度计算）。
- 抗酸药有效性（定性）：模拟胃酸（稀 HCl）+ 不同抗酸药，观察 pH 变化（用指示剂判断）。

**常见易错点 Common misconceptions**
- 认为"酸都很危险、碱都很安全"（NaOH 同样强腐蚀）。
- 用 pH 判酸碱时忘记 pH 只是水溶液的属性（干燥固态酸不显酸性）。
- 把中和反应写成"酸 + 碱 → 盐 + 氢气"。
- 中和后一定中性（只有在**恰好完全反应**时才中性）。
- 酚酞在酸中"变蓝/变红"（正确：无色；碱中变粉红）。
- 混淆 strong 强 / concentrated 浓（强弱看电离程度，浓稀看水量【🔭 Ext. 定性提及】）。
- 稀释浓硫酸时把水倒入酸（**必须酸入水**）。

**评估方式 Assessment**
- 知识：20 个物质分为 acid / base / salt；写 8 个中和反应并配平；pH 排序与指示剂颜色预测。
- 能力：用指示剂与 pH 数据设计"未知溶液鉴别"方案（Planning and conducting / Evaluating）。

---

## Part IV · 探究、应用与核能｜Inquiry, Applications & Nuclear Energy

### Ch.8 — Lab Skills, Safety and Scientific Inquiry
### 第 8 章　实验技能、安全与科学探究

- **大纲对应 Content alignment**: Curricular Competencies（Planning and conducting / Processing and analyzing / Evaluating）—— 贯穿全册
- **课时 Periods**: 2（+ 分散在各章实验中）
- **素材对齐**: `G11/LAB SAFTY` 与 `G11/MAKE OBSERVATION` 的同类要求（学校对实验报告与观察记录的格式要求）

**学习目标 Learning objectives**
- EN: Plan a fair test with independent, dependent and controlled variables; follow WHMIS and lab safety rules; record qualitative and quantitative observations; identify sources of error and suggest improvements.
- 中: 设计含自变量、因变量、控制变量的公平实验；遵守 WHMIS 与实验室安全规范；记录定性与定量观察；找出误差来源并提出改进。

**知识点要点 Key concepts**
1. Inquiry 探究流程: Question → Hypothesis (If…then…) → Prediction → Procedure → Data → Analysis → Conclusion → Communication
2. Variables 变量: independent 自变量 / dependent 因变量 / controlled 控制变量 / confounding 干扰变量
3. Observation vs inference 观察与推断: 只写看到的，不写猜测；qualitative 定性 vs quantitative 定量
4. WHMIS 安全标识: flammable 易燃、corrosive 腐蚀、toxic 有毒、oxidizing 氧化性、compressed gas 压缩气体、biohazard 生物危害、environmental hazard 环境危害
5. 化学实验安全要点（本册高频）: 护目镜必戴；酸入水；不尝药品；闻气味用手扇；加热试管口不对人；废液分类回收
6. 数据与图像: 表格规范（含单位）、作图（标题/轴/刻度/最佳拟合线）、interpolation 内插 / extrapolation 外推
7. 误差评估: random 随机误差 / systematic 系统误差；准确度 accuracy vs 精密度 precision

**核心词汇 Key vocabulary**
fair test 公平实验 · independent variable 自变量 · dependent variable 因变量 · controlled variable 控制变量 · hypothesis 假设 · observation 观察 · inference 推断 · qualitative 定性的 · quantitative 定量的 · WHMIS · accuracy 准确度 · precision 精密度 · systematic error 系统误差 · random error 随机误差

**实验与活动 Lab / Activity**
- 完整微型探究：「温度如何影响 NaHCO₃ + CH₃COOH 的反应速率？」——写完整报告并自评。
- 安全标识配对 + 本实验室应急路线与灭火器位置演练。
- 数据质量评审：给两份"同一实验"的数据，判断哪份更可信、为什么。

**常见易错点 Common misconceptions**
- 把结论写成"猜的"而非"数据支持的"。
- 控制变量写"全部保持不变"却说不出具体是哪几个。
- 观察写成推断（"它产生了 CO₂"应为"有气泡产生，可使澄清石灰水变浊"）。
- 把 accuracy 与 precision 混用。
- 只报"成功"数据，剔除不合预期的点。

**评估方式 Assessment**
- 能力为主：实验报告量规（假设 / 变量 / 数据质量 / 结论与证据一致性 / 改进建议 / 安全）。

---

### Ch.9 — Chemical Processes in the Real World (and First Peoples Knowledge)
### 第 9 章　化学过程的实际应用与影响（含原住民知识）

- **大纲对应 Content alignment**: C5（含 `including First Peoples knowledge`）
- **课时 Periods**: 2

**学习目标 Learning objectives**
- EN: Give examples of chemical processes used in industry and daily life; evaluate their benefits and risks (environmental, social, economic); recognise First Peoples knowledge and practices involving chemical processes in BC.
- 中: 举例说明工业与日常中的化学过程；评价其收益与风险（环境、社会、经济）；认识 BC 原住民在化学过程方面的知识与实践。

**知识点要点 Key concepts**
1. 常见化工过程: 燃烧发电与燃料、金属冶炼 smelting、石灰石煅烧制水泥、肥料生产、电池、制药、水处理、食品加工（发酵/膨松）
2. 收益与代价（本单元最容易考"论述题"）:
   - 收益: 能源、材料、医药、清洁水
   - 代价: CO₂ 排放、酸雨、水体污染、尾矿、能耗
3. 绿色化学理念: 原子经济性、可再生原料、催化替代、减少废物、安全化学品【🔭 Ext. → Chemistry 11/12 深化】
4. **First Peoples knowledge（BC 官方明确要求）**: 例如
   - 传统植物知识与制药（如太平洋西北地区的雪松、北美肺草等植物用途）
   - 传统食品保存/加工中的化学过程（熏制、风干、发酵、鱼油提取）
   - 潮间带贝类与石灰来源、用火管理森林与草原生态（controlled burning）
   - 与土地、水域的可持续性观念
   > ⚠️ 写这一节时须谨慎：以"知识体系与可持续实践"的角度呈现，避免任何刻板化表达；具体案例以 BC 官方 elaborations 与 FNESC 资源为准。
5. 影响评价框架: 环境 environmental / 社会 social / 伦理 ethical / 经济 economic / 可持续 sustainability
6. 案例研究（择一深挖）：酸雨与石灰中和 / 铜冶炼与尾气 SO₂ / 城市水处理的加氯与加石灰

**核心词汇 Key vocabulary**
chemical process 化学过程 · industry 工业 · smelting 冶炼 · emission 排放 · acid rain 酸雨 · water treatment 水处理 · sustainability 可持续性 · First Peoples knowledge 原住民知识 · traditional ecological knowledge 传统生态知识 · trade-off 权衡 · ethics 伦理

**实验与活动 Lab / Activity**
- 「净化一杯浑水」：用沉淀 + 过滤 + 加石灰/明矾调 pH（定性）模拟水处理，写工艺流程图。
- 案例分析报告：选一个 BC 本地化工项目（如水泥厂 / 冶炼厂 / 造纸厂），写"收益-风险-改进建议"三栏报告。
- 原住民知识专题研究：小组查阅 FNESC / 官方资源，汇报一项传统化学相关实践及其科学解释。

**常见易错点 Common misconceptions**
- 只讲收益不讲风险（反之亦然）——官方要求是"evaluate"，必须两面。
- 把"化学"等同"有毒"（混淆 chemical 与 toxic）。
- 把原住民知识当成"民俗"而非知识体系（用词与视角都要注意）。
- 化学过程的"影响"只谈环境，漏掉社会与经济维度。

**评估方式 Assessment**
- 知识：把 10 个日常产品对应到其制造中的化学过程；写酸雨成因与中和处理的方程式。
- 能力：就一个化工项目写证据化论述（Communicate evidence-based arguments / Consider social, ethical and environmental implications）。

---

### Ch.10 — Nuclear Energy and Radiation
### 第 10 章　核能与辐射

- **大纲对应 Content alignment**: C6（官方 Content 条目；与化学相邻，涉及原子核与同位素）
- **课时 Periods**: 2

**学习目标 Learning objectives**
- EN: Distinguish nuclear reactions from chemical reactions; describe alpha, beta and gamma radiation and their penetrating power; explain fission and fusion; evaluate benefits and risks of nuclear energy and radiation uses.
- 中: 区分核反应与化学反应；描述 α、β、γ 三种辐射及其穿透力；解释裂变与聚变；评价核能与辐射应用的收益与风险。

**知识点要点 Key concepts**
1. 核反应 vs 化学反应（本单元最重要的对比）: 化学反应只动**核外电子**、原子核不变、能量变化小；核反应改变**原子核**（质子/中子数变化）、可把一种元素变成另一种元素、能量变化巨大
2. 三种辐射:

| 辐射 | 符号 | 本质 | 电荷 | 穿透力 | 屏蔽 |
|---|---|---|---|---|---|
| alpha α | ⁴₂He | 氦核（2p + 2n） | +2 | 最弱（一张纸/皮肤） | 纸、衣物 |
| beta β | ⁰₋₁e | 高速电子 | −1 | 中等（几毫米铝） | 铝板、有机玻璃 |
| gamma γ | γ | 高能电磁波 | 0 | 最强（需厚铅/混凝土） | 厚铅、混凝土 |

3. 半衰期 half-life（**定性理解 + 简单整数次减半**）：每经过一个半衰期，放射性原子数目减半；用于碳-14 测年、医学示踪
4. Fission 裂变: 重核（如 U-235）分裂 + 释放能量 + 中子链式反应；核电站原理
5. Fusion 聚变: 轻核（H 同位素）结合成氦 + 释放更多能量；太阳与恒星的能量来源
6. 应用与风险: 发电、医学诊断与治疗（放疗、示踪）、工业探伤、食品辐照；风险: 辐射损伤、废物处理、事故
7. ⛔ 超纲红线: 质能方程 `E = mc²` 的定量计算、核反应方程式的质量亏损计算属 **Physics 11/12**，只做概念提及

**核心词汇 Key vocabulary**
nuclear reaction 核反应 · radiation 辐射 · alpha particle α 粒子 · beta particle β 粒子 · gamma ray γ 射线 · half-life 半衰期 · fission 裂变 · fusion 聚变 · radioactive 放射性的 · isotope 同位素 · chain reaction 链式反应 · shielding 屏蔽

**实验与活动 Lab / Activity**
- 模拟半衰期：用 100 枚硬币/骰子，每轮"正面者移除"，画数量-轮次图并求半衰期，与真实数据对比。
- 辐射穿透力演示（视频/模拟）：纸 / 铝 / 铅 对三种辐射的遮挡。
- 辩论：本省是否应扩大核能？要求引用数据与风险分析。

**常见易错点 Common misconceptions**
- 认为"核电站会像原子弹一样爆炸"（燃料丰度与结构完全不同）。
- 把化学反应称为"核反应"（如认为燃烧改变了原子核）。
- 认为辐射"接触就致死"（剂量决定效应）。
- α 粒子"最危险"或"最无害"的绝对化说法（穿透弱但若进入体内危害大）。
- 认为半衰期"过两个半衰期就完全没有了"（永远剩下 1/2ⁿ）。
- 混淆 fission 与 fusion。

**评估方式 Assessment**
- 知识：α/β/γ 对比表；裂变与聚变对比；简单半衰期计算（整数轮）。
- 能力：就核能/辐射应用写一份风险评估短文（Consider social, ethical and environmental implications）。

---

## Part V · 综合｜Synthesis

### Ch.11 — Unit Synthesis, Review and Assessment
### 第 11 章　单元综合复习与测评

- **大纲对应 Content alignment**: C1–C6 + B1 综合
- **课时 Periods**: 2
- **素材对齐**: ⭐ `SCI 10 REV WORKSHEET 0–3` 全卷（本章评估部分须覆盖其全部题型）

**学习目标 Learning objectives**
- EN: Integrate the whole chemistry unit around the Big Idea; complete a summative assessment covering content and competencies.
- 中: 围绕核心概念整合全单元；完成覆盖知识与能力的总结性测评。

**知识点要点 Key concepts**
1. 主线回顾（一句话串全册）：
   > **周期表位置 → 离子电荷 → 化学式与命名 → 写出方程式 → 配平（原子守恒）→ 判类型 → 预测产物 → 能量变化 → 应用与影响**
2. 易混概念总对比表: chemical vs nuclear、exothermic vs endothermic、synthesis vs decomposition、single vs double replacement、acid vs base vs salt、strong vs concentrated、mass number vs atomic number
3. 十类高频题型（对应学校复习卷）:
   - ① 名称 ↔ 化学式（含多变价 + 多原子离子）② 离子/共价判定 ③ 酸碱盐分类 ④ 由文字描述写方程式 ⑤ 配平 ⑥ 反应类型分类 ⑦ 预测产物 ⑧ 活动性/溶解性判断能否反应 ⑨ 放热/吸热判定与能量图 ⑩ pH 与指示剂
4. 现实联系（Careers & Society）: 化学工程、环境监测、药学、冶金、核医学、实验室技术员

**实验与活动 Lab / Activity**
- 「神秘溶液鉴别」综合实验：4 瓶未知溶液（酸 / 碱 / 盐 / 水），用指示剂 + 反应特征鉴别并写全部方程式。
- 概念图 Concept map 小组海报（把全册 20 个核心概念连成网络）。

**评估方式 Assessment**
- 总结性测评 Summative：知识卷（60%）+ 实验/探究任务（25%）+ 概念图或科普写作（15%）
- 双语政策：术语可用中英双语作答；**化学式与英文命名必须用英文**。

---

## 3. 附录框架｜Appendices

### 附录 A — Glossary 词汇总表（EN ↔ 中）
> **生成物**：由 `build_glossary.py` 从 11 章第 6 节抽取、去重、字母序汇总；同时导出 `glossary.csv`（Anki/Quizlet 源）。
> 体例：`atom｜原子｜Ch.1｜ smallest unit of an element 元素的最小单位`

### 附录 B — Common Ions Table 常见离子表
> 三张表：cations 阳离子（含多变价 metal(I)/metal(II)）/ anions 阴离子 / **polyatomic ions 多原子离子**（含 oxalate、acetate、chromate、dichromate、permanganate、chlorate、chlorite、hydrogen carbonate、hydrogen phosphate）。
> 每行：符号 / English name / 中文名 / 电荷。

### 附录 C — Naming & Formula Cheat Sheet 命名与化学式速查
> C-1 离子化合物（-ide 词尾、罗马数字、多原子离子）
> C-2 共价化合物（前缀表 + 俗名）
> C-3 酸 / 碱 / 盐 的化学式特征与命名
> C-4 **英中命名互译规则对照**（顺序相反的说明 + 30 个例句 + 错误示范）
> C-5 拼写变体说明表（aluminium/aluminum、sulphide/sulfide、sulphate/sulfate）

### 附录 D — Reactions & Balancing Cheat Sheet 反应与配平速查
> D-1 六类反应一般式与识别判据
> D-2 配平四步法流程图 + 5 个由易到难的示范
> D-3 金属活动性顺序表（含"能否发生置换"的用法）
> D-4 溶解性规则表（含常见沉淀）
> D-5 燃烧反应配平口诀与 3 个示范

### 附录 E — Lab & Worksheet Bank 实验与练习单库
> 逐章配套练习单（A4 可打印）+ 实验单（含安全提示）+ 概念图模板 + 单元测评卷与量规。
> ⭐ 其中一份专门做 **`SCI 10 REV WORKSHEET 0–3` 全解**（学校原卷 + 逐步解答 + 常见错误对照），
> 原卷放在 `G10/CHEM10 rev/`（只读，不改动）。

---

## 4. 编写体例约定｜Writing Conventions

1. **双语顺序（2026-11-03 统一到 G11 口径）**：标题与术语一律 `English（中文）`；**正文以英文为主**——叙述、专有名词、推导用英文完整书写；**关键部分中英对照**（定义、核心概念/规则/公式首述、结论句、易错判据）；**解释性内容可用中文**（难点、类比、口诀、坑、技巧），1–3 行。不再逐段翻译全文。例外：第 9 节 Assessment 题干与答案保留逐题对照。**化学式与英文命名必须用英文书写**。
2. **术语一致性**：同一概念全册只用一个中文译名（见附录 A）。BC 官方用 semi-metal、教材常用 metalloid，统一译"类金属"。
3. **Big Idea 回扣**：每章结尾固定 `## 10. 回扣核心概念｜Connection to the Big Idea`，回扣 B1（Ch.10 并行回扣 B2）。
4. **能力标注**：每个实验/活动后标注所训练的 Curricular Competency，如 `[Planning and conducting]`。
5. **中英命名分栏**：凡涉及命名的章节，用两栏表格并列展示英文命名与中文命名规则，并给出错误示范。
6. **超纲标注**：超出 Science 10 官方 Content 的内容一律标 `【🔭 Extension → Chemistry 11】`（或 Physics 11/12），**不作主内容、不出练习**。
7. **图例一律用 SVG**（脚本生成，数据驱动），不再使用 ASCII 字符画；改图改脚本再重跑，不直接编辑 SVG。
8. **拼写体系**：全册统一 **aluminium**；`sulph-` 与 `sulf-` 两种拼写首次出现处并列说明，正文以 `sulf-` 为准（与附录 B 一致）。
9. **学校素材对齐**：正文知识点顺序与 `SCI 10 REV WORKSHEET 0–3` 的题型顺序保持可映射关系（见 5.2），便于直接用于课前复习。

---

## 5. 素材来源与对齐｜Source Material Alignment

### 5.1 官方来源
- BC 省教育厅 Science 10 课程页（Big Ideas / Content / Curricular Competencies 三类原文），2026-09-22 复核。
- BC 省 Chemistry 11 课程页（用于确定**超纲红线**）。
- 官方配套教材：*BC Science Connections 10*（化学相关章节做参照）。

### 5.2 学校素材（`G10/CHEM10 rev/`，只读）
| 文件 | 页数 | 覆盖内容 | 对应章节 |
|---|---|---|---|
| `SCI 10 REV WORKSHEET 0 _merge.pdf` | 4 | 周期表电荷、双原子分子、离子/共价命名、化学式、酸碱盐、六类反应表 | Ch.1 · Ch.5 · Ch.7 |
| `SCI 10 REV WORKSHEET 1 _merge.pdf` | 4 | 化学式互译（含多原子离子）、酸碱盐分类、配平 + 分类、由描述写方程式 | Ch.1 · Ch.3 · Ch.5 · Ch.7 |
| `SCI 10 REV WORKSHEET 2 _merge.pdf` | 4 | 命名、化学式、文字方程式配平、产物预测、复杂配平（含 C/H/N/O 燃料） | Ch.3 · Ch.5 |
| `SCI 10 REV WORKSHEET 3 _merge.pdf` | 2 | 命名（含 KMnO₄）、化学式、产物预测、中和与置换、配平 | Ch.3 · Ch.5 · Ch.7 |

> ⚠️ 原卷答案里有**手写笔误**（如把 `Ag₂C₂O₄` 写成 "silver dichromate"、`AlPO₄` 系数写错）。
> 附录 E 的"全解"以**正确化学**为准，并单列"原卷易错点对照"，不照抄原答案。

### 5.3 英文版（现行口径）
`MD/chapters-en/` 为英文版正文目录，体例见该目录 `_STYLE.md`（2026-11-03 新建，与 G11 同一套：英文为主 + 关键处中英对照 + 解释可中文）。
> 📌 **现状**：`chapters-en/` 目前为空，已有 Ch.1–Ch.2 在 `chapters-cn/`（中文在前版）。英文版自 2026-11-03 起按新口径新写，中文版不回溯改造。
> ⛔ 英文版 md 与中文版**同名**，导出 PDF 必须分目录（`pdf/EN/` vs `pdf/CN/`），否则互相覆盖。

---

## 6. 下一步｜Next Steps

- [ ] 目录骨架 + 本框架（已完成 2026-09-22）
- [x] **Ch.1 样板章**：定死 10 节结构、SVG 风格、题量与答案详略（2026-09-24 完成，
      `MD/chapters-cn/Ch01_Atoms_Ions_Formulas.md` + 图库 `build_figure_svg_g10.py` 4 张）
- [x] **Ch.2 化学反应与化学方程式**（2026-09-24 完成，`MD/chapters-cn/Ch02_Chemical_Reactions_Equations.md`
      + 图库新增 5 张 ch02-*；同时修复 preview_md.py 预览图片相对路径）
- [ ] 并行派子代理生成 Ch.2–Ch.11（每个代理 2–3 章，prompt 给样板章路径 + 本框架 + 该章知识点清单 + 质量红线）
- [ ] SVG 图库（`MD/assets/figures/`，脚本生成 + `check_svg_bounds.py` 越界自检）
- [ ] 附录 A–E（A 由脚本抽取；B–D 手写；E 含学校复习卷全解）
- [ ] 练习单（A4 可打印，`MD/assets/printables/`）
- [ ] **PDF（各章 / 合订本 / 英文版）** —— ⛔ 需用户明确点名后才生成

---

*本框架依据 BC 省教育厅官方 Science 10 课程标准编制；官方原文以 curriculum.gov.bc.ca 为准。*
