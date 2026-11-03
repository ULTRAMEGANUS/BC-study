# BC Chemistry 11 — Bilingual Lecture Framework
## 不列颠哥伦比亚省 十一年级化学 — 英中对照讲义章节框架

> **根目录 Root**: `canada chemical/G11/`
> **依据来源 Source**: [BC Ministry of Education — Chemistry 11 Curriculum](https://curriculum.gov.bc.ca/curriculum/science/11/chemistry)（官方现行大纲，2026-09-29 复核）
> **素材对齐 Alignment**: 学校课程大纲（Tsou Outline，单元结构与评估权重）与 `NEW Chem 11 Data Booklet`（数据册）已完整消化进正文与附录；实验安全与观察素材（LAB SAFTY · LAB1）已消化进 Ch.1 与附录 E。源文件于 2026-11-01 从工作区移除，原件存于 git 历史，可随时恢复。
> **版本 Version**: v1.0（框架骨架 / framework skeleton）
> **语言体例 Convention**: 每个词条先英文后中文，格式 `English（中文）`；专业术语首次出现时双标注。

---

## 0. 课程定位与大纲依据｜Curriculum Position & Official Standards

### 0.1 官方 Big Ideas（核心概念）— 全部 5 条（Chemistry 11 是整门化学课，无"无关单元"）

| # | English (official, verbatim) | 中文 | 主线归属 |
|---|---|---|---|
| B1 | **Atoms and molecules are building blocks of matter.** | 原子与分子是物质的构件。 | Part II（原子理论） |
| B2 | **Organic chemistry and its applications have significant implications for human health, society, and the environment.** | 有机化学及其应用对人类健康、社会与环境有重大影响。 | Part I（有机化学） |
| B3 | **The mole is a quantity used to make atoms and molecules measurable.** | 摩尔是使原子与分子可被量度的量。 | Part III（摩尔） |
| B4 | **Matter and energy are conserved in chemical reactions.** | 化学反应中物质与能量均守恒。 | Part III–IV（反应与计量、能量） |
| B5 | **Solubility within a solution is determined by the nature of the solute and the solvent.** | 溶液中的溶解度由溶质与溶剂的本性决定。 | Part V（溶液化学） |

> ⚠️ 与 G9/G10 不同：Chemistry 11 是**独立化学课（全年）**，5 条 Big Idea 全部适用。
> 每章结尾回扣其中**一条**（每章标明对应哪条），全册收尾时五条合一。

### 0.2 官方 Content（内容标准）— 全部 15 条原文

| # | English (official, verbatim) | 中文 | 对应章节 |
|---|---|---|---|
| C1 | **quantum mechanical model and electron configuration** | 量子力学模型与电子排布 | Ch.5 |
| C2 | **valence electrons and Lewis structures** | 价电子与路易斯结构 | Ch.7 |
| C3 | **chemical bonding based on electronegativity** | 基于电负性的化学键 | Ch.7 |
| C4 | **bonds/forces** | 化学键/分子间作用力 | Ch.7（含 Ch.3 官能团性质接口） |
| C5 | **organic compounds** | 有机化合物 | Ch.2 – Ch.3 |
| C6 | **applications of organic chemistry** | 有机化学的应用 | Ch.4 |
| C7 | **the mole** | 摩尔 | Ch.8 |
| C8 | **dimensional analysis** | 量纲分析 | Ch.1（入门）→ Ch.8（完整方法） |
| C9 | **reactions** | 化学反应 | Ch.9 |
| C10 | **stoichiometric calculations using significant figures** | 使用有效数字的化学计量计算 | Ch.10 |
| C11 | **local and other chemical processes** | 本地与其他化学过程 | Ch.4（主）· Ch.12/Ch.14（接口） |
| C12 | **green chemistry** | 绿色化学 | Ch.4（主）· Ch.14（收尾） |
| C13 | **solubility of molecular and ionic compounds** | 分子化合物与离子化合物的溶解度 | Ch.12 |
| C14 | **stoichiometric calculations in aqueous solutions** | 水溶液中的化学计量计算 | Ch.13 |
| C15 | **analysis techniques** | 分析技术 | Ch.14 |

### 0.3 官方 Curricular Competencies（课程能力）— 六类，Chemistry 11 专属要点

| 类别 | Chemistry 11 层级要求（相对 G9/G10 的新增量） |
|---|---|
| Questioning and predicting | 多重假设、多重结果预测；对抽象问题提问 |
| Planning and conducting | 定性 + 定量数据采集；**有效数字 significant figures、不确定度 uncertainty、科学记数法 scientific notation** 成为硬要求 |
| Processing and analyzing | 图表/模型/图式解读；变量关系描述与计算； inconsistencies 识别 |
| Evaluating | 误差与不确定度来源；模型与类比的局限性；一手/二手资料可信度 |
| Applying and innovating | 本地/全球关联的项目设计；真实与概念情境的多策略解题 |
| Communicating | 理论模型表述；证据化论证；科学语言与规范表示 |

> ⛔ **量化是本课程与 Science 10 的分水岭**：Sig figs / sci notation / uncertainty 从 Ch.1 起贯穿所有计算题与实验报告，评估量规必须单列这一项。

### 0.4 纵向衔接与超纲红线｜Vertical Articulation & Out-of-Scope Lines

| 年级 | 化学相关内容 | 本讲义的处理 |
|---|---|---|
| **Science 9/10**（先修） | 周期表电荷、玻尔图、离子/共价命名、化学式、配平、六类反应、酸碱盐定性、质量守恒 | **不重教**，压缩为 **Ch.1 衔接复习**，只补 Chemistry 11 直接要用的部分 |
| **Chemistry 11**（本册） | C1–C15（见 0.2） | 主体内容 |
| **Chemistry 12**（后接·超纲红线） | 化学平衡 equilibrium 与 Keq、溶解度积 Ksp、酸碱理论深化与 `pH = −log[H⁺]` 定量计算、有机反应类型（加成/取代/消除/酯化）与机理、量热法定量 `q = mcΔT` 与 ΔH 计算、Hess 定律、氧化还原与电化学 | ⛔ **一律不写**；仅在正文出现必要时标 `【Extension → Chemistry 12】`，且不做练习 |

> **判据（写正文时自检）**：
> ① 出现平衡常数、Ksp、pH 计算式 → 超纲；② 有机化学只做**命名、画结构、辨官能团、说性质与用途**，
> 出现反应方程式（除燃烧外）→ 超纲；③ 能量变化只做**定性描述 + 能量图**，出现 q=mcΔT 计算 → 超纲。

---

## 1. 讲义总体结构｜Overall Structure

```
G11/                                  根目录
├─ md/                                md 输出（本框架在此）
│  ├─ chapters-en/                    14 章正文（英文在前版）
│  ├─ appendices-en/                  附录 A–E
│  └─ assets/                         SVG 源、校验与构建脚本
├─ pdf/                               ⛔ 本年级全部 PDF 产物的唯一出口（生成物，不入库）
└─ preview/                           章节 HTML 预览页（过程产物，不入库）
```

> **单元顺序 = 学校顺序**（`Tsou Outline` 明确）：学校把 **Organic Chemistry 排在第一单元**，
> 本讲义章节顺序完全跟随，保证讲义能配合学校进度使用，不按"传统顺序"（先原子后有机）重排。

### 单元划分｜Unit Map（学校 5 单元 → 讲义 6 部分 14 章）

| 部分 Part | 学校 Unit | 主题 Theme | 章节 Chapters | 课时（建议） |
|---|---|---|---|---|
| **Part 0** | 开学周 | 衔接·量化工具·实验安全与观察 Bridge, Quantitative Tools, Lab Safety | Ch.1 | 4 |
| **Part I** | Unit 1 – Organic Chemistry | 有机化学（→ C5·C6·B2） | Ch.2 – Ch.4 | 19 |
| **Part II** | Unit 2 – Atomic Theory | 原子理论（→ C1–C4·B1） | Ch.5 – Ch.7 | 18 |
| **Part III** | Unit 3 – The Mole & Chemical Reactions | 摩尔与化学反应（→ C7·C8·C9·B3·B4） | Ch.8 – Ch.9 | 11 |
| **Part IV** | Unit 4 – Stoichiometry | 化学计量与能量（→ C10·B4） | Ch.10 – Ch.11 | 12 |
| **Part V** | Unit 5 – Solution Chemistry | 溶液化学（→ C13·C14·C15·B5） | Ch.12 – Ch.14 | 18 |
| **附录 Appendix** | — | 词汇表 / 数据与官能团速查 / 命名速查 / 计算速查 / 实验库 | A – E | — |

> 合计约 **82 课时**，对应 BC 学年制 Chemistry 11（约 110–130 periods，含单元测验、复习与学校活动缓冲）。
> 评估权重按学校大纲：**Labs/Assignments/Unit Reviews 30% + Quizzes/Tests 70%**，Final Assessment 15%。

---

## 2. 章节框架｜Chapter-by-Chapter Framework

每个章节条目统一包含 7 个字段，填充正文时保持此体例（与 G9/G10 一致）：

```
1. 大纲对应 Content alignment
2. 学习目标 Learning objectives（EN / 中）
3. 知识点要点 Key concepts（双语分级条目）
4. 核心词汇 Key vocabulary（EN ↔ 中）
5. 实验与活动 Lab / Activity
6. 常见易错点 Common misconceptions
7. 评估方式 Assessment（知识 + 能力）
```

**正文统一采用 10 节结构**（体例硬约束，与 G9/G10 保持一致）：

```
1 大纲对应｜Content Alignment        （表格：官方条目原文 + 是否超纲）
2 学习目标｜Learning Objectives      （EN 5 条 + 中 5 条）
3 概念解析｜Concept Explanations     （3.x 分节：英文定义 → 要点 → 例子；中文只点难点）
4 表格比对｜Comparison Tables        （≥3 张，中英双语表头）
5 图例说明｜Diagrams & Worked Examples（≥3 个 SVG 图 + 逐步解析例题）
6 核心词汇｜Key Vocabulary           （表格：English / 中文 / 备注）
7 实验与活动｜Lab / Activity         （含 Curricular Competency 标注 + 安全）
8 常见易错点｜Common Misconceptions  （≥8 条：错误认识 / 正确理解）
9 答题评估｜Assessment               （A 基础 10×2 + B 应用 4×5 + C 挑战 2×10 + 完整答案 + 评分量规）
10 回扣核心概念｜Connection to the Big Idea   （标注本章回扣 B1–B5 中哪一条）
```

---

## Part 0 · 衔接·量化工具·实验安全｜Bridge, Quantitative Tools, Lab Safety

### Ch.1 — From Science 10 to Chemistry 11: Tools, Safety and Observation
### 第 1 章　从 Science 10 到 Chemistry 11：工具、安全与观察

- **大纲对应 Content alignment**: C8 dimensional analysis（入门）；Curricular Competencies（safety / sig figs / uncertainty 引入）
- **课时 Periods**: 4
- **素材对齐**: 实验安全讲义 ×4 与观察实验（原 `LAB SAFTY/`·`LAB1/`，2026-11-01 起源文件已移除，内容已消化进本章与附录 E）
- **回扣 Big Idea**: 工具章（无固定条目，末尾预告 B3——量化的意义）

**学习目标 Learning objectives**
- EN: Review Science 9/10 chemistry core skills (naming, formulas, balancing, six reaction types); apply significant figures, scientific notation and unit conversions; use dimensional analysis as a general problem-solving tool; follow WHMIS and school lab rules; record qualitative and quantitative observations properly.
- 中: 复习 Science 9/10 化学核心技能（命名、化学式、配平、六类反应）；应用有效数字、科学记数法与单位换算；把量纲分析作为通用解题工具；遵守 WHMIS 与本校实验室规则；规范记录定性与定量观察。

**知识点要点 Key concepts**
1. Science 9/10 快速通关清单：周期表电荷图 · 双原子分子（H-7 + P₄/S₈）· 离子/共价命名（多变价 + 多原子离子）· 六类反应 · 配平四步法 · 酸碱盐定性
2. **Significant figures 有效数字**：计数规则；乘除看"位数最少"、加减看"小数位最少"；`801` 与 `800.` 的区别
3. **Scientific notation 科学记数法**：`a × 10ⁿ`（1 ≤ a < 10）；与 sig figs 联动
4. **Dimensional analysis 量纲分析**：conversion factor 转换因子 → 单位连消 → 目标单位；mL↔L、g↔kg、J↔kJ（Ch.8 起全面展开）
5. **Uncertainty 不确定度（概念引入）**：读数估读位；重复测量波动；误差来源（random/systematic 复习）
6. **Lab safety 实验安全（学校规则落地）**：WHMIS 符号复习 + 本校硬规矩——pre-lab 未完成**不得进实验室**；实验日禁穿凉鞋/短裤/隐形眼镜；实验室内禁饮食；事故立即报告；补做实验每月一次（周三早 8:30–9:30）
7. **Observation 观察**：qualitative vs quantitative；只写"看到的"，推断与分析分开（LAB1 的核心要求）

**核心词汇 Key vocabulary**
significant figures 有效数字 · scientific notation 科学记数法 · dimensional analysis 量纲分析 · conversion factor 转换因子 · uncertainty 不确定度 · qualitative observation 定性观察 · quantitative observation 定量观察 · WHMIS · pre-lab 实验预习 · evidence 证据

**实验与活动 Lab / Activity**
- LAB1「Making Observations」复演：酒精灯/蜡烛/化学样品多站观察，按学校报告格式记录（qualitative + quantitative 分栏）`[Observing and recording / Communicating]`
- 安全标识寻宝：LAB SAFTY 讲义 + 实验室实景对照，写出本室洗眼器/灭火器/应急出口位置 `[Planning and conducting]`
- 量纲分析接力：8 道单位换算接力题，每棒只做一步、必须写出转换因子 `[Processing and analyzing]`

**常见易错点 Common misconceptions**
- 有效数字"越多越准"（仪器精度决定上限，不是靠多写位）。
- 800 与 800. 有效位数相同（带小数点才是明确 4 位）。
- 单位换算只换数字不换单位。
- 把观察写成结论（"生成了 CO₂" ≠ "产生无色气体，使石灰水变浑浊"）。
- pre-lab 当成"读完讲义"（学校要求书面写全目的/步骤/安全/数据表）。
- 隐形眼镜 + 腐蚀性药品的风险被低估（学校明令实验日禁戴）。

**评估方式 Assessment**
- 知识：sig figs + sci notation + 单位换算 20 题；命名与配平诊断测 20 题（摸底，检 Science 10 缺口）。
- 能力：LAB1 观察报告（量规：观察/推断分离、定量数据带单位与不确定度、安全项）。

---

## Part I · 有机化学｜Organic Chemistry（学校 Unit 1 · B2 主线）
> 对应官方 Content C5·C6；Big Idea B2：*Organic chemistry and its applications have significant implications for human health, society, and the environment.*

### Ch.2 — Hydrocarbons: Structure, Naming and Isomers
### 第 2 章　烃：结构、命名与同分异构体

- **大纲对应 Content alignment**: C5（前半：hydrocarbons）
- **课时 Periods**: 7
- **回扣 Big Idea**: B2

**学习目标 Learning objectives**
- EN: Explain why carbon forms the backbone of so many compounds; name and draw alkanes, alkenes and alkynes including branched and cyclic structures; write molecular, condensed and skeletal formulas; identify structural isomers.
- 中: 解释碳为何能构成如此多化合物的骨架；命名并书写烷烃、烯烃、炔烃（含支链与环状结构）；写出分子式、凝聚结构式与骨架式；辨认结构异构体。

**知识点要点 Key concepts**
1. **Organic chemistry 有机化学** = 含碳化合物的化学（CO₂、碳酸盐等例外）；碳的 4 键 → 链/环/支链的多样性
2. 三大家族（通式必背）：

| 家族 | English | 通式 | 后缀 | 结构特征 |
|---|---|---|---|---|
| 烷烃 | alkanes | CₙH₂ₙ₊₂ | -ane | 全单键，saturated 饱和 |
| 烯烃 | alkenes | CₙH₂ₙ | -ene | 含 C=C，unsaturated 不饱和 |
| 炔烃 | alkynes | CₙH₂ₙ₋₂ | -yne | 含 C≡C |

3. **IUPAC 命名四步**：找最长主链 → 编号（取代基位次最小）→ 前缀定取代基（methyl 甲基 / ethyl 乙基…）→ 后缀定家族；多个取代基用 di-/tri-/tetra-
4. 前缀 1–10：meth·eth·prop·but·pent·hex·hept·oct·non·dec
5. **三种结构式**：molecular（C₄H₁₀）/ condensed（CH₃CH₂CH₂CH₃）/ skeletal（骨架式）
6. **Structural isomers 结构异构体**：同分子式、不同连接方式（C₄H₁₀ 两种起，C₅H₁₂ 三种）
7. **Cycloalkanes 环烷烃**（CₙH₂ₙ，与烯烃通式相同但无 C=C）；支链环烷命名
8. **英中命名对照（本册体例重点）**：IUPAC 名直译——propane 丙烷 · 2-methylbutane 2-甲基丁烷 · cyclohexane 环己烷；英文"前缀+后缀"与中文"数字+官能团字"顺序基本对应，与无机命名（sodium chloride 氯化钠，顺序相反）不同
9. 性质趋势：链越长沸点越高（London dispersion 增大，预埋 Ch.7）；非极性、疏水、可燃

**核心词汇 Key vocabulary**
hydrocarbon 烃 · alkane 烷烃 · alkene 烯烃 · alkyne 炔烃 · saturated 饱和的 · unsaturated 不饱和的 · parent chain 主链 · substituent 取代基 · alkyl group 烷基 · structural isomer 结构异构体 · condensed formula 凝聚结构式 · skeletal formula 骨架式 · cycloalkane 环烷烃

**实验与活动 Lab / Activity**
- 「分子搭建」：分子模型套件搭 C₄H₁₀/C₅H₁₂ 全部异构体，拍照编目 `[Communicating]`
- 「命名-结构双轨道」：A 组给名画结构、B 组给结构命名，交换互评 `[Communicating]`
- 演示：矿物油（烷烃混合物）与溴水的对照观察（饱和/不饱和的表观差异，定性）`[Questioning and predicting]`

**常见易错点 Common misconceptions**
- 主链不找最长（找"最直"）。
- 编号不使取代基位次最小（但-ane 2-methylbutane 写成 3-methylbutane）。
- 双键/三键位置漏标（pent-2-ene 的 "2" 不能省）。
- 认为异构体是"同一种物质的画法不同"（性质不同！如正丁烷/异丁烷沸点不同）。
- 环烷烃与烯烃通式相同 → 误判官能团（看结构不看通式）。
- 骨架式数碳数错（顶点=碳，氢按 4 键补齐）。

**评估方式 Assessment**
- 知识：20 个命名↔结构互译（含支链/环状/异构）；3 组异构体书写。
- 能力：用模型解释"为什么 C₄H₁₀ 恰有两种异构体"并画出证据 `[Communicating]`。

---

### Ch.3 — Functional Groups: The Organic Vocabulary
### 第 3 章　官能团：有机化学的"词汇"

- **大纲对应 Content alignment**: C5（后半：functional groups）；C4 接口（官能团性质与氢键）
- **课时 Periods**: 8
- **回扣 Big Idea**: B2

**学习目标 Learning objectives**
- EN: Recognise the major functional groups; name and draw compounds containing each group; relate functional groups to physical properties such as solubility and boiling point using intermolecular forces.
- 中: 识别主要官能团；命名并书写含各官能团的化合物；用分子间作用力把官能团与溶解度、沸点等物理性质联系起来。

**知识点要点 Key concepts**

| 官能团 | English | 结构 | 命名要点 | 中文词尾 |
|---|---|---|---|---|
| 卤代 | halogenated compound | R–X | fluoro/chloro/bromo/iodo 前缀 | 氯代·溴代… |
| 羟基 | alcohol 醇 | R–OH | -anol（hydroxyl 羟基） | 醇 |
| 醚 | ether | R–O–R′ | alkoxy 前缀（methoxyethane） | 醚 |
| 醛 | aldehyde | R–CHO | -anal（端基 C=O–H） | 醛 |
| 酮 | ketone | R–CO–R′ | -anone（链中 C=O） | 酮 |
| 羧酸 | carboxylic acid | R–COOH | -anoic acid | 酸 |
| 酯 | ester | R–COO–R′ | 双词：alkyl alkanoate | 酸酯 |
| 胺 | amine | R–NH₂ | -anamine（amino 氨基） | 胺 |
| 酰胺 | amide | R–CONH₂ | -anamide | 酰胺 |

1. 官能团 = 决定分子特征反应与性质的原子团；同碳数不同官能团 → 性质迥异（C₂H₆O：乙醇液体 vs 二甲醚气体）
2. 命名规则：选**含官能团**的最长链作主链；编号使官能团位次最小；醇/醛/酮/酸/胺/酰胺用后缀，卤代/醚用前缀
3. **ester 酯的英中双词命名**：`methyl ethanoate` 乙酸甲酯——注意中英文词序不同（英文"醇部分+酸部分"，中文"酸部分+醇部分"）
4. 性质与 C4 接口：–OH / –NH₂ / C=O 可参与**hydrogen bonding 氢键** → 小分子醇/酸与水互溶；长链烃基主导 → 疏水（"亲水头、疏水尾"预埋 Ch.12 的 like dissolves like）
5. 沸点对比链：烃 < 醚 < 醛/酮 < 醇/酸（同碳数，分子间力增强）
6. ⛔ 有机**反应**（加成/取代/酯化方程式）属 Chemistry 12，本章只做命名、结构、性质

**核心词汇 Key vocabulary**
functional group 官能团 · hydroxyl group 羟基 · carboxyl group 羧基 · amino group 氨基 · alcohol 醇 · ether 醚 · aldehyde 醛 · ketone 酮 · carboxylic acid 羧酸 · ester 酯 · amine 胺 · amide 酰胺 · hydrogen bonding 氢键（预埋） · hydrophilic 亲水的 · hydrophobic 疏水的

**实验与活动 Lab / Activity**
- 「闻香识酯」：提供几种安全酯类样品的气味卡（乙酸乙酯=菠萝味等），联系"酯=香料"的应用直觉 `[Applying and innovating]`
- 「官能团分诊台」：30 个结构式分诊到 9 个官能团窗口，限时赛 `[Processing and analyzing]`
- 溶解性快测：乙醇/食用油/食盐在水中溶解性对照，用"亲水头/疏水尾"解释 `[Questioning and predicting]`

**常见易错点 Common misconceptions**
- aldehyde 与 ketone 混淆（看 C=O 是否在链端）。
- ester 双词名顺序写反（methyl ethanoate ≠ ethyl methanoate，是两种不同酯）。
- 醇的编号未使 –OH 位次最小（propan-2-ol 不能写成 propan-1-ol 乱标）。
- 认为 –OH 就是碱（有机醇 ≠ 无机氢氧化物，不电离出 OH⁻）。
- 把氢键当共价键（氢键是**分子间**作用力，弱得多）。
- "有机物都溶于有机溶剂、都不溶于水"——短链含氧官能团分子例外。

**评估方式 Assessment**
- 知识：20 个官能团判定 + 15 个命名↔结构互译（含酯双词名）；5 个"预测沸点/溶解性高低并解释"。
- 能力：给一个常见药物/香料结构式（如 aspirin），圈出全部官能团并逐一说性质影响 `[Communicating]`。

---

### Ch.4 — Applications of Organic Chemistry: Health, Society and the Environment
### 第 4 章　有机化学的应用：健康、社会与环境

- **大纲对应 Content alignment**: C6（主）；C11 local and other chemical processes；C12 green chemistry
- **课时 Periods**: 4
- **回扣 Big Idea**: B2（正面+负面两面评价，官方要求 evaluate）

**学习目标 Learning objectives**
- EN: Give examples of organic chemistry in fuels, plastics, pharmaceuticals, food and personal care; evaluate benefits and risks for human health, society and the environment; describe local chemical processes in BC and principles of green chemistry.
- 中: 举例说明有机化学在燃料、塑料、制药、食品与个人护理中的应用；评价其对人类健康、社会与环境的收益与风险；描述 BC 本地化学过程与绿色化学原则。

**知识点要点 Key concepts**
1. **Fuels 燃料**：fossil fuels 化石燃料；complete vs incomplete combustion 完全/不完全燃烧（CO 的危险）；燃料选择的权衡（能量、排放、成本）
2. **Plastics & polymers 塑料与聚合物**：monomer 单体 → polymer 聚合物的概念图景；常见塑料（PET、PE、PVC）与回收标识；微塑料议题
3. **Pharmaceuticals 制药**：aspirin（含羧酸+酯双官能团）结构解读；"结构决定功能"的直觉建立
4. **Food & personal care 食品与个护**：esters 与香味、emulsifiers 乳化剂（亲水/疏水双端，回收 Ch.3）
5. **Local chemical processes BC 本地**（C11）：pulp & paper 制浆造纸 · forestry 林业产品 · mining 冶炼与尾矿 · LNG/天然气 · 渔业加工；选一例做"收益-代价-改进"分析
6. **Green chemistry 绿色化学**（C12）原则精选：prevent waste 预防废物 · atom economy 原子经济 · safer solvents 安全溶剂 · renewable feedstocks 可再生原料 · catalysis 催化 · design for degradation 可降解设计
7. **First Peoples perspectives**（Competency 要求）：传统植物利用与天然产物知识（如雪松制品、植物染料/药物），以"知识体系与可持续实践"视角呈现，具体案例以官方 elaborations 与 FNESC 资源为准
8. 评价框架：health 健康 / society 社会 / environment 环境 三维度 + trade-off 权衡表

**核心词汇 Key vocabulary**
monomer 单体 · polymer 聚合物 · complete combustion 完全燃烧 · incomplete combustion 不完全燃烧 · pharmaceutical 药物 · emission 排放 · sustainability 可持续性 · green chemistry 绿色化学 · atom economy 原子经济 · trade-off 权衡 · First Peoples knowledge 原住民知识

**实验与活动 Lab / Activity**
- 「塑料回收码侦探」：收集 6 种回收标识塑料制品，按编号分类并查性质/用途，写一张家庭塑料地图 `[Applying and innovating]`
- 案例研究：BC 本地一家造纸/冶炼/能源企业，三栏报告"收益-风险-绿色化学改进建议" `[Evaluating]`
- 燃烧对比演示：蜡烛（氧气充足/受限罩烧）观察烟尘 → 解释 incomplete combustion `[Questioning and predicting]`

**常见易错点 Common misconceptions**
- "化学=人工=有害，天然=安全"（天然 ≠ 无害，合成 ≠ 有毒；看物质与剂量）。
- 不完全燃烧只生成 CO₂（缺氧时生成 CO 甚至碳烟）。
- 可降解塑料"随便丢就降解"（多数需工业堆肥条件）。
- 只谈收益或只谈风险——官方动词是 evaluate，必须两面。
- 绿色化学只是"回收再利用"（核心是**源头预防**）。

**评估方式 Assessment**
- 知识：完全/不完全燃烧产物判断与方程式；聚合物-单体-用途匹配。
- 能力：就一个有机化学应用写证据化论述（健康/社会/环境三维度 + 权衡结论）`[Communicating / Evaluating]`。

---

## Part II · 原子理论｜Atomic Theory（学校 Unit 2 · B1 主线）
> 对应官方 Content C1–C4；Big Idea B1：*Atoms and molecules are building blocks of matter.*

### Ch.5 — From Bohr to the Quantum Mechanical Model
### 第 5 章　从玻尔模型到量子力学模型

- **大纲对应 Content alignment**: C1 quantum mechanical model and electron configuration
- **课时 Periods**: 6
- **回扣 Big Idea**: B1

**学习目标 Learning objectives**
- EN: Trace the evolution of atomic models; describe the quantum mechanical model and orbitals; write full and core electron configurations; draw orbital diagrams; connect electron configuration to periodic table blocks.
- 中: 梳理原子模型的演进；描述量子力学模型与轨道；书写完整电子排布与核心简写；画轨道图；把电子排布与周期表分区联系起来。

**知识点要点 Key concepts**
1. 模型演进线：Dalton（实心球）→ Thomson（葡萄干布丁）→ Rutherford（核式）→ **Bohr（玻尔，分层，Science 9 已学）** → **quantum mechanical model 量子力学模型**（电子云/概率）
2. **Orbitals 轨道**：s（1 球形）/ p（3 哑铃）/ d（5）/ f（7）；每轨道最多 **2 e⁻**
3. 三大规则：**Aufbau principle 构造原理**（低能级先填）、**Pauli exclusion principle 泡利不相容**（同轨自旋相反）、**Hund's rule 洪特规则**（等能轨道先 singly 单占）
4. **Electron configuration 电子排布**：完整式（1s² 2s² 2p⁶…）+ **core notation 核心简写**（[Ne] 3s² 3p⁵）
5. **Orbital diagram 轨道图**（box diagram，↑↓）
6. **4s 与 3d 的次序**：先 4s 后 3d 填充（4s¹–⁴ 在 3d 前）；阳离子先失最外层
7. 周期表分区：s 区/p 区/d 区（transition metals）/f 区——排布即"周期表的地图"
8. ⛔ 量子数、薛定谔方程数学形式、能级精细分裂 → 大学/Chemistry 12，不做

**核心词汇 Key vocabulary**
quantum mechanical model 量子力学模型 · electron cloud 电子云 · orbital 轨道 · aufbau principle 构造原理 · Pauli exclusion principle 泡利不相容原理 · Hund's rule 洪特规则 · electron configuration 电子排布 · core notation 核心简写 · orbital diagram 轨道图 · valence electron 价电子

**实验与活动 Lab / Activity**
- 「电子入住大厦」：把周期表当"公寓楼"，按能量楼层安排"电子住户"，楼层平面图=周期表分区 `[Formulate models]`
- 焰色试验：Li/Na/K/Cu/Sr 盐的火焰颜色，从"电子跃迁发光"角度定性解释（Bohr→量子模型的桥）`[Questioning and predicting]`
- 排布速配赛：抽元素卡 → 60 秒写完整排布 + 核心简写 + 轨道图三件套 `[Processing and analyzing]`

**常见易错点 Common misconceptions**
- 电子在固定"轨道"上跑圈（量子模型是概率云，无确定轨迹）。
- 3d 排在 4s 前面（填充次序 4s 先；但**书写**与失电子次序另行处理，避免死记结论不分场合）。
- 一个轨道画两个同向箭头（违反 Pauli）。
- d 轨道只画 4 个或漏空轨道（Hund 要求先单占）。
- 认为玻尔模型"错了所以没用"（对氢原子光谱仍成立，是过渡桥梁）。
- 核心简写用错内层（[Ar] 4s² 只含到 Ar，不能写成 [Ne]）。

**评估方式 Assessment**
- 知识：Z = 1–36 全部元素的完整排布 + 核心简写；10 个轨道图纠错题。
- 能力：解释"为什么周期表形状长这样"（s/p/d/f 分区证据化说明）`[Communicating]`。

---

### Ch.6 — The Periodic Table and Periodic Trends
### 第 6 章　周期表与周期性趋势

- **大纲对应 Content alignment**: C1 接口（排布→分区→趋势）；Competency：Seek and analyze patterns
- **课时 Periods**: 5
- **回扣 Big Idea**: B1

**学习目标 Learning objectives**
- EN: Describe periodic trends in atomic radius, ionic radius, first ionization energy, electronegativity and metallic character; explain trends using electron shells and effective nuclear charge; compare reactivity of key groups.
- 中: 描述原子半径、离子半径、第一电离能、电负性与金属性的变化趋势；用电子层数与有效核电荷解释趋势；比较重点族的反应性。

**知识点要点 Key concepts**
1. 复习定位：group 族（纵）= 外层电子数 → 化学性质；period 周期（横）= 电子层数
2. 五大趋势（方向 + 微观解释）：

| 趋势 Trend | 横向（左→右） | 纵向（上→下） | 解释要点 |
|---|---|---|---|
| atomic radius 原子半径 | 减小 | 增大 | 核电荷↑拉紧电子层 / 层数↑外层更远 |
| first ionization energy 第一电离能 | 增大 | 减小 | 核对最外层"抓得紧 / 抓得松" |
| electronegativity 电负性 | 增大 | 减小 | 同上（F 最大 4.0，用 Data Booklet） |
| metallic character 金属性 | 减小 | 增大 | 失电子能力变化 |
| ionic radius 离子半径 | — | 同主层逻辑 | 阳离子<原子；阴离子>原子 |

3. **有效核电荷 effective nuclear charge（概念级）**与 shielding 屏蔽效应——趋势的统一解释工具
4. 族反应性对比：alkali metals 碱金属（下强上弱，与水反应剧烈度）· halogens 卤素（上强下弱）· noble gases 稀有气体（惰性来源=满壳层）
5. 电离能的"台阶异常"（Be→B、N→O 小幅回落）——用排布解释，展示模型威力（不要求定量）
6. ⛔ 定量屏蔽常数、逐级电离能数据表分析 → Chemistry 12/大学

**核心词汇 Key vocabulary**
periodic trend 周期性趋势 · atomic radius 原子半径 · ionic radius 离子半径 · first ionization energy 第一电离能 · electronegativity 电负性 · shielding effect 屏蔽效应 · effective nuclear charge 有效核电荷 · alkali metal 碱金属 · halogen 卤素 · noble gas 稀有气体

**实验与活动 Lab / Activity**
- 「趋势拼图」：给空白周期表 + 20 个元素数据贴纸（半径/IE/EN），自己贴出趋势图并总结规律 `[Seek and analyze patterns]`
- 演示：Na/K 与水反应剧烈度对比（视频 + 安全说明），对应"向下金属性增强" `[Questioning and predicting]`
- Data Booklet 实战：用电负性数据预言 5 组元素成键类型（直通 Ch.7）`[Applying and innovating]`

**常见易错点 Common misconceptions**
- 半径方向记反（"越往下越大"对，"越往右越大"错）。
- 电离能与电负性混为一谈（IE=失电子难度；EN=吸共用电子对能力）。
- 认为稀有气体"没有电离能"（有，只是极高）。
- 用"想失/想得电子"的拟人化代替能量解释。
- 阳离子/阴离子与原子大小关系记反。

**评估方式 Assessment**
- 知识：画出五趋势全景箭头图；8 个"给两个元素比大小并解释"。
- 能力：用"层数 + 核电荷 + 屏蔽"三要素解释任一趋势，写出一段证据化解释 `[Communicating]`。

---

### Ch.7 — Lewis Structures, Electronegativity, Bonding and Intermolecular Forces
### 第 7 章　路易斯结构、电负性、化学键与分子间作用力

- **大纲对应 Content alignment**: C2 · C3 · C4（本 Part 核心）
- **课时 Periods**: 7
- **回扣 Big Idea**: B1

**学习目标 Learning objectives**
- EN: Draw Lewis structures for atoms, ions and molecules including polyatomic ions; use electronegativity difference to classify bonds; predict molecular polarity from shape; distinguish intramolecular bonds from intermolecular forces (London dispersion, dipole-dipole, hydrogen bonding).
- 中: 画原子、离子与分子（含多原子离子）的路易斯结构；用电负性差分类化学键；由分子形状预测极性；区分分子内化学键与分子间作用力（色散力、偶极-偶极、氢键）。

**知识点要点 Key concepts**
1. **Lewis structure 路易斯结构**：价电子计数 → 骨架 → 补八隅 → 余电子成重键；多原子离子加 [ ]ⁿ⁻
2. **ΔEN 判键型**（Data Booklet 电负性表）：ΔEN < 0.5 covalent non-polar 非极性共价 · 0.5–1.8（教材阈值略有差异，注明）covalent polar 极性共价 · > 1.8 ionic 离子键——**键型是连续谱不是非黑即白**
3. 分子形状（概念级 VSEPR）：linear / bent / trigonal planar / pyramidal / tetrahedral——形状决定**分子极性**（对称抵消 → 非极性，如 CO₂；不对称 → 极性，如 H₂O）
4. **分子内 vs 分子间**（本单元最重要的一刀）：
   - intramolecular bonds 分子内化学键：ionic / covalent / metallic——强（数百 kJ/mol 量级）
   - intermolecular forces 分子间作用力：**London dispersion 色散力**（所有分子，随电子数增大）→ **dipole-dipole 偶极-偶极**（极性分子）→ **hydrogen bonding 氢键**（H–N/O/F 体系，最强 IMF）
5. IMF 定性质：熔沸点、溶解性（**like dissolves like 相似相溶**——直通 B5 与 Ch.12）、表面张力
6. 金属键 metallic bonding：电子海模型，解释延展性与导电

**核心词汇 Key vocabulary**
Lewis structure 路易斯结构 · lone pair 孤对电子 · octet rule 八隅规则 · electronegativity difference 电负性差 · polar covalent bond 极性共价键 · molecular polarity 分子极性 · VSEPR · London dispersion force 色散力 · dipole-dipole force 偶极-偶极力 · hydrogen bond 氢键 · intramolecular 分子内的 · intermolecular 分子间的 · like dissolves like 相似相溶

**实验与活动 Lab / Activity**
- 「水上漂回形针」：表面张力挑战 + 加洗洁精对比，用分子间力解释 `[Questioning and predicting]`
- 「分子极性分诊」：给 12 个分子（CO₂/H₂O/NH₃/CH₄/CCl₄…），先判键极性再判分子极性，两栏分开 `[Processing and analyzing]`
- 溶解性矩阵：NaCl/蔗糖/碘/石蜡 × 水/己烷，结果表 → 归纳 like dissolves like `[Seek and analyze patterns]`

**常见易错点 Common misconceptions**
- 分子内有氢键（氢键在分子**之间**，极少数分子内情形不在此阶段讨论）。
- "极性键组成的分子一定极性"（CO₂ 全是极性键但整体非极性——对称抵消）。
- 水沸腾"断 O–H 键"（断的是分子间氢键，O–H 共价键完好）。
- ΔEN 阈值绝对化（1.8 是经验线，过渡区"既不是纯离子也不是纯共价"）。
- 色散力"只存在于非极性分子"（所有分子都有，极性分子也叠加色散）。
- 八隅规则对 B/Be 失灵的分子硬凑电子。

**评估方式 Assessment**
- 知识：10 个路易斯结构（含 3 个多原子离子）；ΔEN→键型→分子极性三级判断 8 组。
- 能力：用 IMF 解释"HF 沸点远高于 HCl"的现象并作图 `[Communicating]`。

---

## Part III · 摩尔与化学反应｜The Mole & Chemical Reactions（学校 Unit 3 · B3+B4 主线）

### Ch.8 — The Mole: Making Atoms and Molecules Measurable
### 第 8 章　摩尔：让原子与分子可被量度

- **大纲对应 Content alignment**: C7 the mole；C8 dimensional analysis（完整方法）
- **课时 Periods**: 6
- **回扣 Big Idea**: B3

**学习目标 Learning objectives**
- EN: Define the mole and Avogadro's number; interconvert among particles, moles and mass; calculate percent composition; determine empirical and molecular formulas from data; apply dimensional analysis and significant figures to all quantitative work.
- 中: 定义摩尔与阿伏伽德罗常数；在粒子数、摩尔、质量三者间换算；计算百分组成；由实验数据确定实验式与分子式；把量纲分析与有效数字应用于所有定量运算。

**知识点要点 Key concepts**
1. **Mole 摩尔** = 6.02×10²³ 个粒子（Avogadro's number 阿伏伽德罗常数）；基准：12 g of C-12 含 1 mol 碳原子
2. **Molar mass 摩尔质量**（g/mol）：数值=平均原子量/式量（Data Booklet 周期表取数）
3. **三桥转换图**（本课程最核心工具）：
   `particles ⇄ (÷/× 6.02×10²³) ⇄ mole ⇄ (×/÷ molar mass) ⇄ mass`
4. **Dimensional analysis 完整方法**：已知量 → 转换因子链 → 单位逐项消 → 目标量；每步带单位写
5. **Sig figs 贯穿**：摩尔质量取 4–5 位参与计算，最终答案按题给数据最少位数保留
6. **Percent composition 百分组成**：各元素质量占比
7. **Empirical formula 实验式 / molecular formula 分子式**：由质量（或 %）→ 假设 100 g → mol 比 → 最简整数比；分子式 = 实验式 × n（需给出式量）
8. ⛔ 气体摩尔体积 22.4 L/mol（STP）若学校课程不教则不做；出现时标注来源（传统 Chem 11 补充内容，非 2018 大纲明文）

**核心词汇 Key vocabulary**
mole 摩尔 · Avogadro's number 阿伏伽德罗常数 · molar mass 摩尔质量 · formula mass 式量 · percent composition 百分组成 · empirical formula 实验式 · molecular formula 分子式 · stoichiometry（预埋） · conversion factor 转换因子

**实验与活动 Lab / Activity**
- 「一摩尔的分量」：称量 1 mol 的 NaCl/S/Cu/水，实物建立"摩尔尺度感" `[Communicating]`
- 水合硫酸铜定组成（定性→定量过渡）：加热前后称重，算结晶水比例的简化版 `[Planning and conducting]`
- 实验式推理赛：给 5 组 % 组成数据，限时定实验式+分子式 `[Processing and analyzing]`

**常见易错点 Common misconceptions**
- "1 mol 任何物质质量相同"（摩尔数相同≠质量相同）。
- 阿伏伽德罗常数抄错位数（6.02×10²³ ≠ 6.02×10²²）。
- 单原子/双原子不分：1 mol O₂ 含 2 mol O 原子。
- 实验式当分子式（CH₂ 是实验式，C₆H₁₂ 才可能是分子式）。
- 换算不带单位硬套公式（量纲分析的意义全丢）。
- 百分组成加起来不等于 100% 还继续往下算（先自检）。

**评估方式 Assessment**
- 知识：粒子⇄摩尔⇄质量 15 题全套（带 sig figs）；实验式/分子式 5 题。
- 能力：设计"用称重测定样品摩尔质量"的方案并指出误差来源 `[Planning and conducting / Evaluating]`。

---

### Ch.9 — Chemical Reactions: From Science 10 to Quantitative Thinking
### 第 9 章　化学反应：从 Science 10 到定量思维

- **大纲对应 Content alignment**: C9 reactions
- **课时 Periods**: 5
- **回扣 Big Idea**: B4（物质守恒侧面）

**学习目标 Learning objectives**
- EN: Review and upgrade the six reaction types; balance equations including diatomic elements and polyatomic groups; predict products using activity series and solubility rules; write complete and incomplete combustion equations; interpret equations quantitatively (mole ratios preview).
- 中: 复习并升级六类反应；配平含双原子分子与多原子原子团的方程式；用活动性顺序与溶解性规则预测产物；书写完全与不完全燃烧方程式；定量解读方程式（摩尔比预告）。

**知识点要点 Key concepts**
1. 六类反应复习（synthesis / decomposition / single replacement / double replacement / neutralization / combustion）——一般式 + 判据树照 G10 体例
2. **升级点 1：状态符号与条件全面化**（s/l/g/aq；Δ、catalyst）——为 Ch.13 的 aq 王国铺路
3. **升级点 2：预测产物规范化**：single replacement 查 activity series 金属活动性顺序；double replacement 查 solubility rules 溶解性规则（速查版，详表在 Ch.12）
4. **升级点 3：燃烧二分**：complete 完全（O₂ 足）→ CO₂ + H₂O；incomplete 不完全（O₂ 不足）→ CO（或 C）+ H₂O——安全链接（热水器/车库 CO 中毒）
5. **方程式的定量读法（预埋 Ch.10）**：系数比 = 摩尔比（"2 H₂ + O₂ → 2 H₂O"读作"2 mol : 1 mol : 2 mol"，不是质量比）
6. 质量守恒定量视角：配平 = 每种元素原子数左右相等（B4 物质侧面，能量侧面在 Ch.11）

**核心词汇 Key vocabulary**
activity series 金属活动性顺序 · solubility rules 溶解性规则 · complete combustion 完全燃烧 · incomplete combustion 不完全燃烧 · carbon monoxide 一氧化碳 · mole ratio 摩尔比 · state symbol 状态符号 · aqueous 水溶液

**实验与活动 Lab / Activity**
- 「六类反应证据站」升级版：6 个反应现场，分类 + 写方程式 + 标状态符号 `[Planning and conducting]`
- 「能否反应」预测-验证：5 组金属/盐溶液组合，先预测（活动性顺序）再做 `[Evaluating]`
- CO 警示案例研讨：燃气不完全燃烧事故新闻报道分析 `[Applying and innovating]`

**常见易错点 Common misconceptions**
- 系数比读成质量比（预埋章的核心雷区）。
- 双原子元素写成单原子（H₂/H₂O 级错误复发）。
- 不完全燃烧写成"生成 CO₂ 和 C"混杂不指明条件。
- Cu + HCl 类不反应组合照样写方程式。
- 配平后系数未约至最简整数比。
- 状态符号漏标或错标（NaCl(l)）。

**评估方式 Assessment**
- 知识：15 个配平（含燃烧与多原子团）+ 10 个产物预测 + 5 个"能否反应"判断。
- 能力：把一个真实事故案例转写成"反应条件→方程式→安全建议"链条 `[Communicating / Applying]`。

---

## Part IV · 化学计量与能量｜Stoichiometry & Energy（学校 Unit 4 · B4 主线）

### Ch.10 — Stoichiometry: Amounts in Chemical Reactions
### 第 10 章　化学计量：反应中的数量关系

- **大纲对应 Content alignment**: C10 stoichiometric calculations using significant figures（本课程量化顶点）
- **课时 Periods**: 8
- **回扣 Big Idea**: B4

**学习目标 Learning objectives**
- EN: Use mole ratios from balanced equations to convert between reactants and products; solve mass-mass problems; identify limiting and excess reagents; calculate theoretical, actual and percent yield; express purity; keep significant figures throughout.
- 中: 用配平方程式的摩尔比在反应物与生成物间换算；求解质量-质量问题；判断限量试剂与过量试剂；计算理论产量、实际产量与百分产率；表达纯度；全程保持有效数字规范。

**知识点要点 Key concepts**
1. **Mole ratio 摩尔比**：系数即摩尔比；"桥"必须经摩尔（mass A → mol A → **mol B** → mass B，四步流程图）
2. **Mass-mass calculation 质量对质量计算**：标准四步 + sig figs 规则示范（逐步例题 ≥5 道，难度递进）
3. **Limiting reagent 限量试剂 / excess reagent 过量试剂**：两种判断法（除以系数比比较 / 算双假设取小值）；"谁先用完谁限量"
4. **Theoretical yield 理论产量**（由限量试剂算）· **actual yield 实际产量**（实验测得）· **percent yield 百分产率** = actual/theoretical × 100%
5. > 100% 产率的检讨：产品未干/含杂质/称量误差——对接 Evaluating competency
6. **Percent purity 百分纯度**：纯物质质量/样品总质量 × 100%
7. 解题规范（全课程硬要求）：配平 → 单位链 → sig figs → 合理位数 + 单位 + 有效数字三查

**核心词汇 Key vocabulary**
stoichiometry 化学计量 · mole ratio 摩尔比 · limiting reagent 限量试剂 · excess reagent 过量试剂 · theoretical yield 理论产量 · actual yield 实际产量 · percent yield 百分产率 · percent purity 百分纯度 · significant figures 有效数字

**实验与活动 Lab / Activity**
- 定量产率实验：NaHCO₃ 加热分解或 Al+CdSO₄ 类置换，测实际产率并写误差分析 `[Planning and conducting / Evaluating]`
- 「限量试剂·实际版」：两种配比做同一反应，比较气泡/沉淀量，验证限量概念 `[Processing and analyzing]`
- 计算流程图制作：把 mass-mass 四步画成自己的流程卡（考试随身规格）`[Communicating]`

**常见易错点 Common misconceptions**
- 直接用质量比当摩尔比搭桥（必须经 mol）。
- 忘配平就取系数（一切比从配平后开始）。
- 限量试剂判断后仍用过量的量算产量。
- 理论/实际/百分产率三者概念混装。
- 中途四舍五入过早，末位漂移（全程保位，最后一步舍入）。
- 答案有效数字与题给数据脱节。

**评估方式 Assessment**
- 知识：6 道完整 mass-mass（含 2 道限量试剂 + 2 道产率 + 1 道纯度）+ 10 道单步换算。
- 能力：给自己实验的产率写误差与改进报告（定量 + 定性证据）`[Evaluating]`。

---

### Ch.11 — Energy Changes in Physical and Chemical Processes
### 第 11 章　物理与化学过程中的能量变化

- **大纲对应 Content alignment**: B4（能量守恒侧面）；学校 Unit 4 描述 "Describe energy changes that occur during a physical or chemical change"
- **课时 Periods**: 4
- **回扣 Big Idea**: B4

**学习目标 Learning objectives**
- EN: Distinguish energy changes in physical vs chemical changes; classify processes as exothermic or endothermic using evidence; draw and interpret energy-level diagrams with activation energy; read thermochemical notation qualitatively.
- 中: 区分物理变化与化学变化中的能量变化；用证据把过程判定为放热或吸热；绘制并解读含活化能的能量变化图；定性解读热化学表示法。

**知识点要点 Key concepts**
1. 守恒双联：物质守恒（Ch.9/10 已覆盖）+ **能量守恒**——B4 的两个侧面合流
2. **Exothermic 放热 / endothermic 吸热**（证据：温度升降、发光、吸热致冷）；物理变化例（熔化/蒸发吸热、凝固放热）与化学变化例并列——学校要求的 physical/chemical 两侧
3. **Energy-level diagram 能量图**：reactant plateau → transition peak（**activation energy 活化能**）→ product plateau；Δ 为正/负的方向解读
4. 微观解释复习升级：断键吸能 / 成键放能；总差额定放热吸热
5. **Thermochemical notation 定性读法**：kJ 出现在方程式生成物侧（放热）或反应物侧（吸热）；`ΔH` 负=放热的符号约定（概念级，不做 q=mcΔT 计算）
6. 催化剂：降低活化能，不改变始末能量差（G10 复习 + 图上标注升级）
7. ⛔ calorimetry 定量 `q = mcΔT`、ΔH 精确计算、Hess 定律 → Chemistry 12

**核心词汇 Key vocabulary**
exothermic 放热的 · endothermic 吸热的 · activation energy 活化能 · energy-level diagram 能量变化图 · thermochemical equation 热化学方程式 · enthalpy change 焓变（概念级） · bond breaking/forming 断键/成键 · physical change 物理变化 · chemical change 化学变化

**实验与活动 Lab / Activity**
- 「温度曲线四连测」：4 个过程（NaOH 溶解放热 / NH₄NO₃ 溶解吸热 / 中和放热 / 小苏打+醋吸热）温度-时间图 + 能量图归类 `[Processing and analyzing]`
- 冷暖袋拆解：市售冷暖袋成分表 → 对应反应类型 → 设计"更安全的替代" `[Applying and innovating]`
- 「能量图拼装」：给 6 组过程卡，画能量图并互检标注 `[Communicating]`

**常见易错点 Common misconceptions**
- "需要点燃 = 吸热反应"（点燃是提供活化能；燃烧本身放热）。
- ΔH 负值当成"能量少了不守恒"（能量释放到环境，守恒不变）。
- 物理变化"没有能量变化"（熔化蒸发照样吸热）。
- 催化剂"减少放热总量"（只削活化能峰，不动始末差）。
- 能量图上活化能标注位置错（峰顶与反应物平台之差）。

**评估方式 Assessment**
- 知识：10 个过程放热/吸热判定；4 幅能量图绘制与解读。
- 能力：用温度-时间数据支撑判定结论，并指出数据缺陷 `[Processing and analyzing / Evaluating]`。

---

## Part V · 溶液化学｜Solution Chemistry（学校 Unit 5 · B5 主线）
> 对应官方 Content C13·C14·C15；Big Idea B5：*Solubility within a solution is determined by the nature of the solute and the solvent.*

### Ch.12 — Solutions and Solubility
### 第 12 章　溶液与溶解度

- **大纲对应 Content alignment**: C13 solubility of molecular and ionic compounds
- **课时 Periods**: 6
- **回扣 Big Idea**: B5（直接主语）

**学习目标 Learning objectives**
- EN: Describe solution formation and the roles of solute and solvent; explain solubility using polarity ("like dissolves like"); write dissociation equations; apply solubility rules to ionic compounds; interpret solubility curves; predict precipitate formation.
- 中: 描述溶液形成过程与溶质溶剂的角色；用极性解释溶解度（相似相溶）；书写电离方程式；对离子化合物应用溶解性规则；解读溶解度曲线；预测沉淀生成。

**知识点要点 Key concepts**
1. **Solution 溶液** = solute 溶质 + solvent 溶剂；常见的气/液/固组合（合金=固态溶液）
2. **溶解三步（能量视角，接 Ch.11）**：溶质粒子分离（吸）→ 溶剂粒子分离（吸）→ 两者结合（放）——总效应决定"热感"
3. **Like dissolves like 相似相溶**（B5 落点）：极性溶质→极性溶剂（水）；非极性溶质→非极性溶剂（己烷）；用 Ch.7 的 IMF 解释（油不吃进水里是因为……）
4. **Ionic compound 溶解 = dissociation 电离**：NaCl(s) → Na⁺(aq) + Cl⁻(aq)（写法规范：s/l/g/aq）
5. **Solubility rules 溶解性规则表**（Data Booklet 版为准）：NO₃⁻/NH₄⁺/Group 1 全溶；Cl⁻ 除 Ag/Pb；SO₄²⁻ 除 Ba/Pb/Ca（微溶）…
6. **Saturated 饱和 / unsaturated / supersaturated 过饱和**；**solubility curve 溶解度曲线**：读图、交点含义、温度影响（固体多数升温增溶；**气体降温增溶**——温水缺氧鱼浮头）
7. **Precipitate formation 沉淀预测**：双溶液混合 → 交换成分 → 查规则 → 定沉淀
8. ⛔ Ksp 溶度积 → Chemistry 12

**核心词汇 Key vocabulary**
solute 溶质 · solvent 溶剂 · dissolution 溶解 · dissociation 电离（解离） · soluble 可溶的 · insoluble 不溶的 · saturated 饱和的 · supersaturated 过饱和的 · solubility curve 溶解度曲线 · precipitate 沉淀 · miscible 互溶的 · like dissolves like 相似相溶

**实验与活动 Lab / Activity**
- 溶解度曲线实测：KNO₃/NaCl 多温度点饱和溶液法（或数据拟合），作曲线 `[Planning and conducting]`
- 「沉淀预测-验证」：8 组盐溶液两两混合，先查表预测再验证 `[Evaluating]`
- 相似相溶演示矩阵：碘/食盐/蜡 × 水/乙醇/己烷，结果表归因 `[Seek and analyze patterns]`

**常见易错点 Common misconceptions**
- "溶解度 = 浓度"（溶解度是饱和态的属性；浓度任意可调）。
- "所有硝酸盐微溶"（NO₃⁻ 全溶——规则表必须内化）。
- 气体溶解度随温度升高而增大（反向！溶氧问题）。
- 电离方程式写成 NaCl → Na⁺ + Cl⁻（漏状态符号 (s)/(aq)）。
- "饱和溶液=浓溶液"（AgCl 饱和溶液极稀）。
- 把"不溶"当"绝对为零"（微溶≠不溶，规则表用"低溶解度"理解）。

**评估方式 Assessment**
- 知识：溶解性规则 20 判 + 6 组沉淀预测 + 1 幅溶解度曲线读图题。
- 能力：用"极性 + IMF"解释给定的 4 组溶解现象（说理链完整）`[Communicating]`。

---

### Ch.13 — Concentration and Solution Stoichiometry
### 第 13 章　浓度与溶液中的化学计量

- **大纲对应 Content alignment**: C14 stoichiometric calculations in aqueous solutions
- **课时 Periods**: 7
- **回扣 Big Idea**: B5（向 B3/B4 回并——溶液里的定量）

**学习目标 Learning objectives**
- EN: Calculate molarity and convert among moles, volume and concentration; perform dilution calculations; solve solution stoichiometry problems; write net ionic equations identifying spectator ions; describe titration procedure and interpret results.
- 中: 计算摩尔浓度并在物质的量、体积、浓度间换算；进行稀释计算；求解溶液化学计量问题；书写净离子方程式并找出旁观离子；描述滴定流程并解读结果。

**知识点要点 Key concepts**
1. **Molarity 摩尔浓度** `M = mol solute / L solution`；制备特定浓度溶液的规范（容量瓶、溶质先溶后定容）
2. 换算桥升级：`mass ⇄ mol ⇄ M·V` ——把 Ch.8 三桥扩成"溶液版四桥"
3. **Dilution 稀释** `C₁V₁ = C₂V₂`（单位统一即可，不必是 L）；稀释即"加水不加分子"
4. **Solution stoichiometry 溶液化学计量**：`V·M → mol A → mol B → V·M`，与 Ch.10 四步完全同构——只换"上桥方式"
5. **Net ionic equation 净离子方程式**：强电解质拆成离子 → 消 spectator ions 旁观离子 → 检查原子与电荷双守恒（例：AgNO₃ + NaCl → AgCl↓ + NaNO₃ 的净式 Ag⁺ + Cl⁻ → AgCl↓）
6. **Titration 滴定（定量分析入门）**：标准液/待测液、burette 滴定管、indicator 指示剂、end point 终点 vs equivalence point 等当点（概念区分）；由 V·M 算未知浓度——C14 的典型应用
7. 安全：酸碱稀释规则（**酸入水**）；滴定管操作规范
8. ⛔ pH = −log[H⁺] 计算、Ka/Kb → Chemistry 12

**核心词汇 Key vocabulary**
molarity 摩尔浓度 · dilution 稀释 · stock solution 储备液 · net ionic equation 净离子方程式 · spectator ion 旁观离子 · titration 滴定 · burette 滴定管 · standard solution 标准溶液 · indicator 指示剂 · equivalence point 等当点 · end point 终点

**实验与活动 Lab / Activity**
- **定量滴定实验**（本课程标志实验）：NaOH 标准液滴定 HCl，三组平行取均值，算未知浓度 + 误差分析 `[Planning and conducting / Processing and analyzing]`
- 配液实操：用容量瓶配 250.0 mL 0.100 mol/L NaCl，全程 sig figs 记录 `[Planning and conducting]`
- 「找旁观离子」：8 个双置换反应写净离子方程式，互查出错 `[Communicating]`

**常见易错点 Common misconceptions**
- C₁V₁=C₂V₂ 两边单位不一致（mL 与 L 混用但各顾各）。
- 净离子方程式把固体/气体/水也拆成离子（只拆强电解质水溶液）。
- 电荷不守恒的"净式"（拆完忘了查电荷）。
- end point 当 equivalence point（指示剂变色点≈但≠等当点，误差来源之一）。
- 滴定管读数不估读、初终读数差算错。
- 容量瓶"定容前摇匀"（应定容后倒转混匀）。

**评估方式 Assessment**
- 知识：8 道浓度/稀释计算 + 4 道溶液化学计量（含净离子方程式）+ 1 道滴定计算全套。
- 能力：滴定报告（数据表、均值与偏差、误差来源分级）+ sig figs 专项扣分项 `[Evaluating]`。

---

### Ch.14 — Analysis Techniques and Course Synthesis
### 第 14 章　分析技术与全课程综合

- **大纲对应 Content alignment**: C15 analysis techniques；C11/C12 收尾；C1–C14 综合
- **课时 Periods**: 5
- **回扣 Big Idea**: B1–B5 五条合流（本章是全课程收束点）

**学习目标 Learning objectives**
- EN: Describe qualitative and quantitative analysis techniques (flame tests, precipitation tests, titration, gravimetric analysis); match techniques to real questions; integrate the whole course around the five Big Ideas; complete a summative assessment.
- 中: 描述定性与定量分析技术（焰色试验、沉淀检验、滴定、重量分析）；把技术匹配到真实问题；围绕五条 Big Idea 整合全课程；完成总结性测评。

**知识点要点 Key concepts**
1. **Qualitative analysis 定性分析**：flame tests 焰色试验（接 Ch.5 电子跃迁）；沉淀检验流程（离子鉴定树：加 Cl⁻ 查 Ag⁺/Pb²⁺…）；指示剂定性判酸碱
2. **Quantitative analysis 定量分析**：titration（Ch.13 实战复盘）；**gravimetric analysis 重量分析**（沉淀过滤干燥称重→算含量，sig figs 全程）；数据质量（uncertainty、平行样、偏差）
3. 仪器技术概念级扫盲：spectroscopy 光谱法、chromatography 色谱——知道"什么问题用什么技术"，原理深度 ⛔ Chemistry 12/大学
4. **全课程主线串联**（一句话串 14 章）：
   > 原子结构（Ch.5）→ 电子排布 → 周期律（Ch.6）→ 键与分子间力（Ch.7）→ 有机词汇（Ch.2–4）→ 摩尔量度（Ch.8）→ 反应（Ch.9）→ 计量（Ch.10）→ 能量（Ch.11）→ 溶解（Ch.12）→ 溶液定量与分析（Ch.13–14）
5. **五 Big Idea 合一图**：B1（构件）→ B3（量度）→ B4（守恒）→ B5（溶解）→ B2（应用与影响）——一张概念图收束全册
6. 高频题型清单（对齐学校 quiz/test 模式）：命名互译 / 配平 / 摩尔三桥 / mass-mass / 限量试剂 / 产率 / 浓度 / 稀释 / 净离子式 / 滴定计算 / 溶解度曲线 / 趋势解释
7. Careers：chemical technician · pharmacist · environmental analyst · food scientist · lab QA

**核心词汇 Key vocabulary**
qualitative analysis 定性分析 · quantitative analysis 定量分析 · flame test 焰色试验 · gravimetric analysis 重量分析 · spectroscopy 光谱法 · chromatography 色谱法 · uncertainty 不确定度 · parallel trials 平行试验 · synthesis（综合）

**实验与活动 Lab / Activity**
- **综合分析挑战**：4 瓶未知盐溶液，用焰色 + 沉淀检验 + 滴定三技术联合鉴定并定量 `[Planning and conducting / Evaluating]`
- 五 Big Idea 概念图海报：小组把 20 个核心概念连成有向网络，口头答辩 `[Communicating]`
- 「给技术找问题」：给 10 个真实情景（水厂/药检/土壤调查…），匹配最适分析技术并说理由 `[Applying and innovating]`

**常见易错点 Common misconceptions**
- "滴定只能测酸碱"（沉淀滴定/氧化还原滴定同样存在，本阶段概念级知晓）。
- 定性/定量分析分工不清（"有没有/有多少"）。
- 焰色试验不洗铂丝/不看钴玻璃干扰（操作规范即数据可信度）。
- 重量分析不恒重就称量（恒重是 gravimetric 的生命线）。
- 综合题里单位与 sig figs 全线松懈（考试扣分重灾区）。

**评估方式 Assessment**
- 总结性测评（Final 15% 权重对齐学校制度）：知识卷（概念 + 计算全套）+ 综合分析实验任务 + 五 Big Idea 概念图。
- 双语政策：术语可双语作答；**化学式、IUPAC 命名与计算单位必须用英文规范**。

---

## 3. 附录框架｜Appendices

### 附录 A — Glossary 词汇总表（EN ↔ 中）
> **生成物**：由脚本从 14 章第 6 节抽取、去重、字母序汇总；同时导出 `glossary.csv`（Anki/Quizlet 源）。
> 体例：`mole｜摩尔｜Ch.8｜ 6.02×10²³ particles; makes atoms measurable 使原子可量度的量`

### 附录 B — Data & Functional Groups Quick Reference 数据与官能团速查
> B-1 Data Booklet 使用指南（带电负性周期表 p1；p2 扫描件内容经 OCR 核对后补录）
> B-2 有机官能团总表：通式 / 结构 / 后缀 / 例名（英中）
> B-3 常见摩尔质量速查（常用 30 物质，4–5 位有效数字）
> B-4 常数与单位：N_A、常用前缀（mL/L、g/kg、kJ/J）

### 附录 C — Naming Cheat Sheet 命名速查
> C-1 有机命名四步法 + 9 官能团后缀/前缀总表 + ester 双词名英中对照
> C-2 无机命名复习（离子/共价/酸碱；多变价 + 多原子离子）——Science 10 内容压缩版
> C-3 **英中命名对照规则**：有机"顺序基本对应"vs 无机"顺序相反"，30 例对照 + 错误示范

### 附录 D — Calculation Cheat Sheet 计算速查
> D-1 Sig figs 三规则 + 判定流程图
> D-2 Dimensional analysis 万能五步
> D-3 摩尔三桥图 + 溶液版四桥图
> D-4 Mass-mass 四步流程图 + 限量试剂双判法
> D-5 浓度/稀释/滴定公式卡 + 检算清单（单位/位数/电荷三查）

### 附录 E — Lab & Worksheet Bank 实验与练习单库
> 逐章配套练习单（A4 可打印）+ 实验单（含 pre-lab 模板——**对齐学校 pre-lab 强制要求**）+ 单元测评卷与量规。
> ⭐ 三份学校素材全解：
> ① `LAB SAFTY 1–3 + LAB SAFTY` 安全讲义精读题单；
> ② `LAB1 MAKE OBSERVATION` 全解（对照已产出的中英对照版）；
> ③ Data Booklet p1 电负性周期表读表练习 + p2 内容（OCR 核对后）专项练习。
> 学校原件已于 2026-11-01 移除（存 git 历史）；全解以正确化学为准，单列"原件易错点对照"。

---

## 4. 编写体例约定｜Writing Conventions

1. **双语顺序（2026-11-03 更新）**：标题与术语一律 `English（中文）`；**正文以英文为主**——叙述、专有名词、推导用英文完整书写；**关键部分中英对照**（定义、核心概念/规则/公式首述、结论句、易错判据）；**解释性内容可用中文**（难点拆解、类比、口诀、坑、技巧），1–3 行。不再逐段翻译全文。例外：第 9 节 Assessment 的题干与答案保留英中对照。**化学式与 IUPAC 命名必须用英文书写**。适用范围：**G11 新写/大改章节**；已完成 14 章保持原样。
2. **术语一致性**：同一概念全册只用一个中文译名（见附录 A）。沿用项目既定译法：semi-metal/metalloid → "类金属"。
3. **Big Idea 回扣**：每章结尾固定 `## 10. 回扣核心概念｜Connection to the Big Idea`，**标明本章回扣 B1–B5 中哪一条**（B2/B5 分别由 Part I / Part V 全程回扣）。
4. **能力标注**：每个实验/活动后标注所训练的 Curricular Competency，如 `[Planning and conducting]`。
5. **中英命名分栏**：有机命名"顺序基本对应"、无机命名"顺序相反"——凡涉及命名的章节用两栏表格并列展示并给出错误示范。
6. **超纲标注**：超出 Chemistry 11 官方 Content 的内容一律标 `【🔭 Extension → Chemistry 12】`（或大学），**不作主内容、不出练习**。三道硬红线见 0.4。
7. **有效数字纪律**：所有计算题的答案必须符合 sig figs 规范；实验报告量规单列 uncertainty 项（官方 Competency 硬要求）。
8. **图例一律用 SVG**（脚本生成、数据驱动），不使用 ASCII 字符画；改图改脚本再重跑，不直接编辑 SVG。
9. **学校制度对齐**：pre-lab 模板按学校要求设计（未完成不得进实验室）；讲义定位为**课后自学对照材料**，学校明令作业须独立完成（Academic Integrity），讲义答案供核对不供照抄。
10. **拼写体系**：全册统一 **aluminium**；`sulf-` 与 `sulph-` 首次出现处并列说明，正文以 `sulf-` 为准。

---

## 5. 素材来源与对齐｜Source Material Alignment

### 5.1 官方来源
- BC 省教育厅 Chemistry 11 课程页（Big Ideas ×5 / Content ×15 / Curricular Competencies 六类原文），2026-09-29 复核。
- BC 省 Chemistry 12 课程页（用于确定**超纲红线**）。
- 官方配套教材参照：*BC Science Chemistry 11*（McGraw-Hill Ryerson，章节顺序与本框架不必一致，以本框架为准）。

### 5.2 学校素材（内容已消化进正文；源文件于 2026-11-01 从工作区移除，原件存 git 历史）
| 文件 | 内容 | 对应章节 |
|---|---|---|
| `Tsou - Chemistry 11 Outline 2026-2027.pdf` | 5 单元结构（有机第一）· 评估权重 30/70 + Final 15% · pre-lab 与实验室规矩 · 补做实验制度 | 全册结构 · Ch.1 · 各章 Assessment 权重 |
| `NEW Chem 11 Data Booklet.pdf` | p1 带电负性周期表（原子量取数源）；p2 扫描件（待 OCR：通常含公式/常数/溶解性表，核对后补录附录 B） | Ch.6 · Ch.7 · Ch.8 · Ch.12 · 附录 B |
| `LAB SAFTY/`（4 份） | 实验安全讲义与规则 | Ch.1 · 附录 E |
| `LAB1/MAKE OBSERVATION_merge.pdf`（+ 中英对照版已产出） | 观察方法与记录规范 | Ch.1 · 附录 E |

> ⚠️ 学校大纲把 **Organic Chemistry 放第一单元**，与"传统顺序"（先原子理论）不同——讲义章节顺序已照学校排。
> ⚠️ Data Booklet p2 为扫描件：用 `pdf2txt.py --ocr on` 提取核对后，再决定收录哪些公式表进附录 B。

### 5.3 英文在前版（现状）
`md/chapters-en/` 已建成为**唯一的正文版本**：14 章 + 附录 A–E 全部落在此处，体例见 `chapters-en/_STYLE.md`。
> ✅ **2026-11-03 语言政策**：英文承载正文（含定义、专有名词），中文只作难点/易错/技巧的点睛解释。中文在前版（`chapters-cn/`）暂不做。
> ⛔ 若将来出中文版：md 与英文版**同名**，导出 PDF 必须分目录（`pdf/EN/` vs `pdf/CN/`），否则互相覆盖。

---

## 6. 下一步｜Next Steps

- [x] 目录骨架（`md/`、`pdf/` 已建）+ 本框架（2026-09-29 完成）
- [ ] **Ch.1 样板章**：定死 10 节结构、SVG 风格、题量与答案详略
- [ ] Data Booklet p2 OCR 提取核对（`pdf2txt.py --ocr on`），补录附录 B
- [ ] 并行派子代理生成 Ch.2–Ch.14（每个代理 2–3 章，prompt 给样板章路径 + 本框架 + 该章知识点清单 + 质量红线）
- [ ] SVG 图库（`md/assets/figures/` 脚本生成 + 越界自检）
- [ ] 附录 A–E（A 由脚本抽取；B–D 手写；E 含学校素材全解）
- [ ] 练习单（A4 可打印，`md/assets/printables/`）
- [ ] **PDF（各章 / 合订本 / 英文版）** —— ⛔ 需用户明确点名后才生成

---

*本框架依据 BC 省教育厅官方 Chemistry 11 课程标准与学校课程大纲（Ms. Tsou, 2026–2027）编制；官方原文以 curriculum.gov.bc.ca 为准。*
