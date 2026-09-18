# BC Science 9 · Chemistry — Bilingual Lecture Framework
## 不列颠哥伦比亚省 九年级科学 · 化学部分 — 英中对照讲义章节框架

> **根目录 Root**: `canada chemical/G9/`
> **依据来源 Source**: [BC Ministry of Education — Science 9 Curriculum](https://curriculum.gov.bc.ca/curriculum/science/9/core)（官方现行大纲）
> **配套官方资源 Alignment**: *BC Science Connections 9*, Unit 2 — "The electron arrangement of atoms impacts their chemical nature"
> **版本 Version**: v1.0（框架骨架 / framework skeleton）
> **语言体例 Convention**: 每个词条先英文后中文，格式 `English（中文）`；专业术语首次出现时双标注。

---

## 0. 课程定位与大纲依据｜Curriculum Position & Official Standards

### 0.1 官方 Big Idea（核心概念）— 化学部分

| # | English (official) | 中文 |
|---|---|---|
| B1 | **The electron arrangement of atoms impacts their chemical nature.** | 原子的电子排布决定其化学性质。 |

> 这是 BC Science 9 化学部分的**唯一**化学 Big Idea，整册讲义的一切内容都必须回扣这一句话。

### 0.2 官方 Content（内容标准）— 化学部分

| # | English (official, verbatim) | 中文 | 对应章节 |
|---|---|---|---|
| C1 | **element properties as organized in the periodic table** | 元素性质在元素周期表中的组织方式 | Ch.2 – Ch.4 |
| C2 | **The arrangement of electrons determines the compounds formed by elements** | 电子排布决定元素所形成的化合物 | Ch.5 – Ch.8 |

> 说明：BC 9 年级化学**不包含**化学方程式配平、酸碱中和、浓度计算——这些属于 **Science 10**（见 0.4）。
> 本讲义仅在 Ch.9 给出最低限度的"衔接桥梁"，并明确标注为 extension。

### 0.3 官方 Curricular Competencies（课程能力）— 全学科共用

| English | 中文 |
|---|---|
| Questioning and predicting | 提问与预测 |
| Planning and conducting | 计划与实施（含实验安全） |
| Processing and analyzing data and information | 数据处理与信息分析 |
| Evaluating | 评估（误差、模型局限、二手资料可信度） |
| Applying and innovating | 应用与创新 |
| Communicating | 交流（科学语言、图表、证据化论证） |

> 每一章的 "评估" 栏需同时覆盖 **Content**（知识）与 **Competency**（能力）两条线。

### 0.4 纵向衔接｜Vertical Articulation

| 年级 | 化学相关内容（官方原文） | 作用 |
|---|---|---|
| **Science 8**（先修） | atomic theory and models（原子论与原子模型）；kinetic molecular theory（分子运动论）；protons, neutrons, and quarks（质子、中子、夸克）；electrons and leptons（电子与轻子） | 预备知识 → Ch.1 复习 |
| **Science 9**（本册） | element properties as organized in the periodic table；The arrangement of electrons determines the compounds formed by elements | 主体内容 |
| **Science 10**（后接） | rearrangement of atoms in chemical reactions（化学反应中原子重排）；acid-base chemistry（酸碱）；law of conservation of mass（质量守恒）；energy change during chemical reactions（反应中的能量变化） | 延伸方向 → Ch.9 桥梁 |

---

## 1. 讲义总体结构｜Overall Structure

```
G9/                                  根目录
├─ 00_讲义章节框架_Course_Framework.md   ← 本文件（框架与总纲）
├─ README.md                          项目说明与使用指南
├─ chapters/                          各章正文讲义（待按框架逐章填充）
│   ├─ Ch01_...  Ch02_...  ... Ch11_...
└─ assets/                            图表、周期表、实验单、词汇卡等
```

### 单元划分｜Unit Map

| 部分 Part | 主题 Theme | 章节 Chapters | 课时（建议） |
|---|---|---|---|
| **Part 0** | 衔接与预备 Bridge & Prerequisite | Ch.1 | 2 |
| **Part I** | 元素与元素周期表 Elements & the Periodic Table（→ C1） | Ch.2 – Ch.4 | 7 |
| **Part II** | 电子排布与化合物 Electron Arrangement & Compounds（→ C2） | Ch.5 – Ch.8 | 11 |
| **Part III** | 桥梁与综合 Bridge, Inquiry & Synthesis | Ch.9 – Ch.11 | 6 |
| **附录 Appendix** | 词汇表 / 离子表 / 元素对照表 | A – D | — |

> 合计约 **26 课时（periods）**，对应 BC 学年中化学单元约 5–6 周的教学量；可按学校进度压缩至 18 节。

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

---

## Part 0 · 衔接与预备｜Bridge & Prerequisite

### Ch.1 — Matter, Atoms and Atomic Theory Review
### 第 1 章　物质、原子与原子论回顾

- **大纲对应 Content alignment**: 承接 Science 8「atomic theory and models / kinetic molecular theory」，为本册建立起点。
- **课时 Periods**: 2

**学习目标 Learning objectives**
- EN: Classify matter into pure substances and mixtures; recall the historical development of atomic models (Dalton → Thomson → Rutherford → Bohr); identify protons, neutrons and electrons with charge, mass and location.
- 中: 能将物质分类为纯净物与混合物；复述原子模型的发展（道尔顿 → 汤姆孙 → 卢瑟福 → 玻尔）；说出质子、中子、电子的电荷、质量与位置。

**知识点要点 Key concepts**
1. Matter（物质）→ pure substance（纯净物）／mixture（混合物）；element（单质/元素）／compound（化合物）
2. Homogeneous（均一）vs heterogeneous（非均一）mixture；solution（溶液）
3. Physical property（物理性质）vs chemical property（化学性质）；physical change（物理变化）vs chemical change（化学变化）
4. Atomic models timeline（原子模型发展史）：
   - Dalton 道尔顿 — solid sphere 实心球模型
   - Thomson 汤姆孙 — plum pudding 葡萄干布丁模型（发现 electron 电子）
   - Rutherford 卢瑟福 — nuclear model 核式模型（金箔实验 gold foil experiment，发现 nucleus 原子核）
   - Bohr 玻尔 — electron shells 电子层模型 → 本册 Ch.5 的主角
5. Subatomic particles（亚原子粒子）：proton 质子 (+1, 原子核)、neutron 中子 (0, 原子核)、electron 电子 (−1, 电子层)
6. Scale（尺度概念）：原子极小，原子核占体积比例极小

**核心词汇 Key vocabulary**
matter 物质 · pure substance 纯净物 · mixture 混合物 · element 元素 · compound 化合物 · atom 原子 · nucleus 原子核 · proton 质子 · neutron 中子 · electron 电子 · atomic theory 原子论 · model 模型

**实验与活动 Lab / Activity**
- 「分类墙」Classification wall：把教室物品图片分为 element / compound / mixture。
- 原子模型漫画时间轴：四人小组各画一个模型并互相讲评（Evaluate the validity and limitations of a model 模型局限评估）。

**常见易错点 Common misconceptions**
- 把化合物当混合物（化合物有固定组成 fixed ratio，混合物没有）。
- 认为电子"绕轨道运行"像行星——Model 只是类比，有局限。

**评估方式 Assessment**
- 知识：物质分类树状图 + 亚原子粒子表格填空。
- 能力：说明原子模型为何会随工具与技术的演进而改变（Consider the changes in knowledge over time as tools and technologies have developed）。

---

## Part I · 元素与元素周期表｜Elements & the Periodic Table
> 对应官方 Content C1：*element properties as organized in the periodic table*

### Ch.2 — Elements, Symbols and the Periodic Table
### 第 2 章　元素、元素符号与元素周期表

- **大纲对应 Content alignment**: C1
- **课时 Periods**: 2

**学习目标 Learning objectives**
- EN: Define an element; read and write chemical symbols; extract atomic number, symbol, name and atomic mass from a periodic table cell; describe how Mendeleev's table differs from the modern one.
- 中: 定义元素；读写元素符号；从周期表方格中读出原子序数、符号、名称与相对原子质量；说明门捷列夫周期表与现代周期表的差异。

**知识点要点 Key concepts**
1. Element（元素）：由同一种原子组成、不能用化学方法再分解的纯净物；自然界约 90 种，目前共 118 种
2. Chemical symbol（元素符号）：1–2 个字母，**首字母大写、次字母小写**（如 Na, Cl, Mg）；部分源自拉丁文（Na ← natrium 钠、Fe ← ferrum 铁、Au ← aurum 金、Pb ← plumbum 铅）
3. Periodic table cell（周期表方格）四要素：symbol 符号、name 名称、atomic number 原子序数、atomic mass 相对原子质量
4. Atomic number 原子序数 = 质子数（决定元素种类）；Atomic mass 相对原子质量 = 同位素加权平均值，单位 amu
5. Isotope 同位素：质子数相同、中子数不同的原子（解释为何原子质量是小数）
6. Mendeleev 门捷列夫（按 atomic mass 排序、留空位并预测新元素）→ Moseley 莫塞莱（改按 atomic number 排序，解决错位问题）

**核心词汇 Key vocabulary**
element 元素 · chemical symbol 元素符号 · atomic number 原子序数 · atomic mass 相对原子质量 · amu 原子质量单位 · isotope 同位素 · periodic table 元素周期表 · Mendeleev 门捷列夫

**实验与活动 Lab / Activity**
- 元素符号记忆赛：把 1–20 号元素的 English name / symbol / 中文名 / 拼音做成四联卡（见附录 D）。
- "Mendeleev's solitaire"：给一组乱序元素卡片，按性质重排并预测缺失元素性质。

**常见易错点 Common misconceptions**
- 符号大小写错误（CO 是一氧化碳分子，Co 是钴元素）。
- 混淆 atomic number 与 atomic mass（一个恒为整数，一个恒为小数）。

**评估方式 Assessment**
- 知识：给定空白周期表前 20 号，填符号与原子序数。
- 能力：解释 Mendeleev 留空位的预测价值（Connect scientific explorations to careers / 科学的预测力）。

---

### Ch.3 — Organization of the Periodic Table: Groups, Periods, Metals & Non-metals
### 第 3 章　周期表的组织：族、周期、金属与非金属

- **大纲对应 Content alignment**: C1
- **课时 Periods**: 2–3

**学习目标 Learning objectives**
- EN: Locate groups and periods; classify elements as metals, non-metals or metalloids by position and properties; compare properties of the three classes.
- 中: 能指出族与周期；按位置与性质把元素分为金属、非金属、类金属；比较三者的性质差异。

**知识点要点 Key concepts**
1. Group / family（族）：**纵列**，1–18 族；同族元素化学性质相似
2. Period（周期）：**横行**，1–7 周期
3. Three classes（三大类，以锯齿线 zigzag / staircase line 分界）：
   - Metals 金属（左侧）：shiny 有金属光泽、malleable 有延展性（可压成薄片）、ductile 可拉成丝、conduct heat & electricity 导热导电
   - Non-metals 非金属（右侧）：dull 无光泽、brittle 脆、poor conductor 不良导体，多为气体
   - Metalloids / semi-metals 类金属（锯齿线两侧）：兼有两者性质，如 Si 硅、B 硼、Ge 锗、As 砷、Sb 锑、Te 碲
4. Transition elements 过渡元素（3–12 族）vs main-group / representative elements 主族元素（1、2、13–18 族）
5. States of matter at room temperature：室温下唯一的两种液态元素是 Hg 汞（金属）和 Br 溴（非金属）
6. 磁性元素 magnetic elements：Fe 铁、Co 钴、Ni 镍

**核心词汇 Key vocabulary**
group 族 · family 族 · period 周期 · metal 金属 · non-metal 非金属 · metalloid 类金属 · semi-metal 半金属 · malleable 有延展性的 · ductile 可延展的 · conductor 导体 · brittle 脆的 · zigzag line 锯齿线 · transition element 过渡元素

**实验与活动 Lab / Activity**
- 金属 vs 非金属性质检验站：光泽、延展性、导电性（用电池+灯泡电路）、磁性四站轮转，记录 qualitative + quantitative 数据。
- 给空白周期表涂色：金属/非金属/类金属三色 + 标出 zigzag line。

**常见易错点 Common misconceptions**
- 周期表左上的 **Hydrogen 氢是非金属**，但因只有 1 个价电子被放在第 1 族——位置由电子排布决定，不是由金属性决定。
- 认为"所有金属都是固体"（Hg 是液体）。

**评估方式 Assessment**
- 知识：给出未知元素的性质描述，判断其属于哪一类并定位周期表区域。
- 能力：用表格系统整理三类元素的性质（Construct and analyze tables / 数据处理）。

---

### Ch.4 — Chemical Families and Reactivity Trends
### 第 4 章　化学族与反应性趋势

- **大纲对应 Content alignment**: C1（element properties）
- **课时 Periods**: 2

**学习目标 Learning objectives**
- EN: Name and locate the four key families; relate their ion charges and reactivity to position on the table; predict properties of an element from its group.
- 中: 说出并定位四个重要族；把各族的离子电荷与反应活性和周期表位置联系起来；由族预测元素性质。

**知识点要点 Key concepts**

| Group 族 | English name | 中文 | Ion charge 离子电荷 | Reactivity 活性 |
|---|---|---|---|---|
| 1 | Alkali metals | 碱金属 | +1 | 极活泼（遇水剧烈反应，需保存在油中） |
| 2 | Alkaline earth metals | 碱土金属 | +2 | 活泼（次于碱金属） |
| 17 | Halogens | 卤素 | −1 | 最活泼的非金属（"成盐者"） |
| 18 | Noble gases | 稀有气体（惰性气体） | 0 | 极不活泼 / inert 惰性 |

1. Halogens 卤素以 **diatomic molecules 双原子分子**存在：F₂、Cl₂、Br₂、I₂（及 H₂、N₂、O₂，共 7 种双原子分子）
2. Noble gases 稀有气体：**He 氦、Ne 氖、Ar 氩、Kr 氪、Xe 氙、Rn 氡**；因价电子层已满而稳定
3. Reactivity trend 活性趋势：第 1 族**向下增强**，第 17 族**向下减弱**
4. 周期表的预测力 predictive power：同族元素性质相似 → 可推断未学过的元素

**核心词汇 Key vocabulary**
alkali metal 碱金属 · alkaline earth metal 碱土金属 · halogen 卤素 · noble gas 稀有气体 · inert 惰性的 · reactive 活泼的 · diatomic molecule 双原子分子 · ion charge 离子电荷 · trend 趋势

**实验与活动 Lab / Activity**
- 碱金属与水反应（教师演示 video/demo，注意安全）：观察 Li/Na/K 反应速率差异，佐证趋势。
- 卤素家族图片卡排序 + 预测砹（At）性质。

**常见易错点 Common misconceptions**
- 把 "noble gas 稀有气体" 译成"贵族气体"——正确中文是**稀有气体 / 惰性气体**。
- 认为稀有气体"完全不能形成化合物"（He、Ne 基本不形成，其他可艰难形成）。

**评估方式 Assessment**
- 知识：给出族号，写出族名、典型离子电荷、活性描述。
- 能力：基于趋势对陌生元素做预测并说明证据（Seek and analyze patterns, trends, and connections）。

---

## Part II · 电子排布与化合物｜Electron Arrangement & Compounds
> 对应官方 Content C2：*The arrangement of electrons determines the compounds formed by elements*
> 这是全册的**核心**，直接回扣 Big Idea。

### Ch.5 — Atomic Structure and Bohr Diagrams
### 第 5 章　原子结构与玻尔模型图

- **大纲对应 Content alignment**: C1 → C2（承上启下：把周期表位置翻译成电子排布）
- **课时 Periods**: 3

**学习目标 Learning objectives**
- EN: Draw Bohr diagrams for the first 20 elements; determine protons, neutrons and electrons from atomic/mass number; use Bohr diagrams to find valence electrons and explain group/period patterns.
- 中: 绘制前 20 号元素的玻尔模型图；由原子序数与质量数求质子、中子、电子数；用玻尔图确定价电子数并解释族与周期的规律。

**知识点要点 Key concepts**
1. 数量关系（必背）：
   - Atomic number (Z) 原子序数 = 质子数 = 中性原子的电子数
   - Mass number (A) 质量数 = 质子数 + 中子数
   - Neutrons 中子数 = A − Z
2. Bohr diagram 玻尔模型图：原子核在中心（标 p⁺、n⁰），电子画在同心壳层上
3. Electron shell capacity 电子层容量（**前 20 号元素**）：第 1 层 2 个，第 2 层 8 个，第 3 层 8 个（2, 8, 8）
4. Valence shell 价电子层（最外层）／valence electrons 价电子（最外层电子）
5. **核心规律（回扣 Big Idea）**：
   - 同**族** → 价电子数相同 → 化学性质相似
   - 同**周期** → 电子层数相同（周期数 = 电子层数）
   - 主族价电子数：1 族→1，2 族→2，13→3，14→4，15→5，16→6，17→7，18→8（**He 例外，为 2**）
6. Noble gas stability 稀有气体稳定性（full valence shell 满层 = 稳定）；其他元素通过得失电子趋向满层 → 引出 Ch.6

**核心词汇 Key vocabulary**
Bohr diagram 玻尔模型图 · energy shell / electron shell 电子层 · valence shell 价电子层 · valence electron 价电子 · mass number 质量数 · atomic number 原子序数 · neutron 中子 · proton 质子 · stable 稳定的 · electron arrangement 电子排布

**实验与活动 Lab / Activity**
- Bohr diagram 制作工坊：用纸盘 + 豆子/贴纸做出 Na、Cl、Ar、Ca 的立体模型。
- "找出冒牌货"：给出 6 张玻尔图，其中 2 张违反 2-8-8 规则，找出并改正。

**常见易错点 Common misconceptions**
- 第 3 层容量记成 18（前 20 号元素范围内按 8 处理，钾钙之后才展开）。
- 用 atomic mass 而不是 mass number 去减中子数（原子质量是小数，应取四舍五入后的质量数）。

**评估方式 Assessment**
- 知识：给出元素，画完整玻尔图并标注 p⁺/n⁰/价电子数。
- 能力：Evaluate the validity and limitations of a model（玻尔模型是简化模型，真实原子并非如此——官方能力要求）。

---

### Ch.6 — Ions and Lewis Dot Diagrams
### 第 6 章　离子与路易斯点式

- **大纲对应 Content alignment**: C2
- **课时 Periods**: 2–3

**学习目标 Learning objectives**
- EN: Explain why atoms form ions; predict ion charge from group number; distinguish cations from anions; draw Lewis dot diagrams for atoms and ions.
- 中: 解释原子为何形成离子；由族号预测离子电荷；区分阳离子与阴离子；绘制原子与离子的路易斯点式。

**知识点要点 Key concepts**
1. Ion 离子：得失电子后带电的原子（质子数不变，**只有电子变**）
2. Cation 阳离子：金属**失去**电子 → 带正电 → 电子数变少
   Anion 阴离子：非金属**得到**电子 → 带负电 → 电子数变多
3. Octet rule 八隅体规则：原子趋向于拥有 8 个价电子（H、He 为 2）
4. 由族号推离子电荷（记忆表）：

| Group 族 | 1 | 2 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|
| Ion charge 电荷 | +1 | +2 | +3 | ±4 | −3 | −2 | −1 | 0 |

5. Multivalent elements 多变价元素：同一元素可形成多种离子，如 Fe²⁺/Fe³⁺、Cu⁺/Cu²⁺、Pb²⁺/Pb⁴⁺；命名用罗马数字（iron(II) / iron(III)）
6. Polyatomic ions 多原子离子：带电荷的原子团，如 NH₄⁺ 铵根、OH⁻ 氢氧根、NO₃⁻ 硝酸根、CO₃²⁻ 碳酸根、SO₄²⁻ 硫酸根、HCO₃⁻ 碳酸氢根、PO₄³⁻ 磷酸根
7. Lewis dot diagram 路易斯点式（点叉图）：
   - 原子：元素符号 + 周围点表示价电子（1 族 1 点 … 18 族 8 点）
   - 阳离子：**方括号 + 电荷，外面 0 个点**（电子已失去）
   - 阴离子：**方括号 + 8 个点 + 电荷**

**核心词汇 Key vocabulary**
ion 离子 · cation 阳离子 · anion 阴离子 · octet rule 八隅体规则 · multivalent 多变价的 · polyatomic ion 多原子离子 · Lewis dot diagram 路易斯点式 · roman numeral 罗马数字 · charge 电荷

**实验与活动 Lab / Activity**
- "离子角色扮演"：学生扮演原子，手持电子卡片互相"给/拿"，最后展示自己的电荷。
- Lewis 点式配对游戏：把原子卡与对应离子卡配对。

**常见易错点 Common misconceptions**
- 认为离子是"质子变了"——**质子数决定元素种类，绝不能变**。
- 阳离子路易斯图里还画点（应为 0 个点）。
- 中文命名混淆：Fe²⁺ 是**亚铁离子**，Fe³⁺ 是**铁离子**；英文为 iron(II) / iron(III)。

**评估方式 Assessment**
- 知识：给族号写离子电荷；给名称画离子路易斯图。
- 能力：用模型解释"为何金属失电子、非金属得电子"（Formulate physical or mental theoretical models）。

---

### Ch.7 — Ionic Compounds: Formulas and Naming
### 第 7 章　离子化合物：化学式与命名

- **大纲对应 Content alignment**: C2（核心）
- **课时 Periods**: 3–4

**学习目标 Learning objectives**
- EN: Write formulas for binary ionic compounds using the criss-cross method; name ionic compounds in English (including multivalent and polyatomic cases); map English names to Chinese names.
- 中: 用交叉法书写二元离子化合物的化学式；用英文命名离子化合物（含多变价与多原子离子）；建立英文命名与中文命名的对应关系。

**知识点要点 Key concepts**
1. Ionic compound 离子化合物 = **metal 金属 + non-metal 非金属**，通过**电子转移**成键（transfer of electrons）
2. 总电荷必须为零 The overall charge must be zero
3. Criss-cross method 交叉法：把离子电荷数交叉写成右下角下标，再约成最简比（1 不写）
   - 例：Mg²⁺ + F⁻ → MgF₂（氟化镁）
4. **英文命名规则**：
   - 金属名（不变）+ 非金属词根 **-ide**；如 NaCl = sodium chloride
   - 多变价金属 → 金属名 + **罗马数字**；如 FeCl₃ = iron(III) chloride
   - 含多原子离子 → 直接用离子名；如 CaCO₃ = calcium carbonate（碳酸钙）
5. **英中命名对照（关键差异）**：
   - 英文顺序：`metal + non-metal-ide`（正离子在前）
   - 中文顺序：`某化某` = **非金属在前 + "化" + 金属在后**（负离子在前）
   - 例：sodium chloride = **氯化钠**；magnesium oxide = **氧化镁**；aluminium sulfide = **硫化铝**
   - `-ide` 对应中文"**化**"：oxide 氧化物 / chloride 氯化物 / sulfide 硫化物 / nitride 氮化物 / fluoride 氟化物
6. Properties of ionic compounds 离子化合物性质：晶体 crystal、高熔沸点 high melting/boiling point、硬而脆 hard & brittle、**溶于水或熔融时导电** conduct when dissolved or molten

**核心词汇 Key vocabulary**
ionic compound 离子化合物 · chemical formula 化学式 · subscript 下标 · criss-cross method 交叉法 · binary 二元的 · -ide ……化物 · roman numeral 罗马数字 · crystal 晶体 · melting point 熔点 · electrolyte 电解质

**实验与活动 Lab / Activity**
- **导电性测试 Conductivity lab**：用电池-灯泡装置分别测固体盐、食盐水、糖水的导电性，对比离子化合物与分子化合物（直接呼应 Content C2 与 Ch.8）。
- 化学式配对卡牌：阳离子牌 × 阴离子牌 → 用交叉法拼出正确化学式。

**常见易错点 Common misconceptions**
- 忘记把比例约到最简（Mg₂O₂ → 应为 MgO）。
- 中文时把顺序写反（写成"钠化氯"）。
- 多变价金属漏写罗马数字。

**评估方式 Assessment**
- 知识：20 道"名称 ↔ 化学式"互译（含中英双向）。
- 能力：通过导电性实验数据归纳离子化合物的通性（Use knowledge of scientific concepts to draw conclusions consistent with evidence）。

---

### Ch.8 — Molecular (Covalent) Compounds: Formulas and Naming
### 第 8 章　分子（共价）化合物：化学式与命名

- **大纲对应 Content alignment**: C2（核心）
- **课时 Periods**: 3

**学习目标 Learning objectives**
- EN: Distinguish molecular from ionic compounds; use prefixes to name binary molecular compounds; know common/trivial names; compare properties of the two compound classes.
- 中: 区分分子化合物与离子化合物；用前缀命名二元分子化合物；掌握常见俗名；对比两类化合物的性质。

**知识点要点 Key concepts**
1. Molecular / covalent compound 分子（共价）化合物 = **non-metal + non-metal**，通过**共用电子对**成键（sharing of electrons）
2. Covalent bond 共价键：shared pair of electrons 共用电子对，用**短线**表示（H—H）
3. **英文命名**：用希腊数字前缀表示原子个数

| 数目 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Prefix 前缀 | mono- | di- | tri- | tetra- | penta- | hexa- | hepta- | octa- | nona- | deca- |
| 中文 | 一 | 二 | 三 | 四 | 五 | 六 | 七 | 八 | 九 | 十 |

4. 规则：**第一个元素**仅当数目 >1 时加前缀（**永不用 mono-**）；**第二个元素**必须加前缀并把词尾改为 **-ide**
   - CO₂ = carbon dioxide（二氧化碳）／CO = carbon monoxide（一氧化碳）
   - N₂O₄ = dinitrogen tetroxide（四氧化二氮）／PCl₃ = phosphorus trichloride（三氯化磷）
5. Common names 俗名（必须背）：
   - H₂O water 水（dihydrogen monoxide）
   - NH₃ ammonia 氨（nitrogen trihydride）
   - CH₄ methane 甲烷（carbon tetrahydride）
   - O₃ ozone 臭氧
   - H₂O₂ hydrogen peroxide 过氧化氢
6. **英中对照**：中文同样用数字前缀，但顺序为 `[第二个元素数目] + 化 + [第一个元素数目] + 第一个元素`
   - CO₂：二(氧) 化 (一)碳 → **二氧化碳**
7. Properties of molecular compounds 分子化合物性质：**低熔沸点** low melting/boiling point、**不导电** poor or no conductivity、多为气体/液体或软固体

**核心词汇 Key vocabulary**
molecular compound 分子化合物 · covalent bond 共价键 · shared pair 共用电子对 · prefix 前缀 · mono-/di-/tri- 一/二/三 · common name 俗名 · intermolecular force 分子间作用力 · conductivity 导电性

**实验与活动 Lab / Activity**
- 分子模型搭建：用球棍模型做 H₂O、CO₂、NH₃、CH₄，画出结构式（用短线表示共用电子对）。
- 性质对比实验：熔点/溶解性/导电性——石盐 NaCl vs 石蜡/蔗糖，填对比表。

**常见易错点 Common misconceptions**
- 第一个元素前也写 mono-（**错误**：CO 是 carbon monoxide，不是 monocarbon monoxide）。
- 对离子化合物误用前缀（NaCl **不能**叫 sodium monochloride）。
- 认为"共价键很弱"——弱的是**分子间作用力**，共价键本身很强。

**评估方式 Assessment**
- 知识：命名互译 + 前缀听写；给出 10 组物质判断 ionic / molecular 并解释依据。
- 能力：用证据表对比两类化合物并做论证（Communicate ... constructing evidence-based arguments）。

---

## Part III · 桥梁、探究与综合｜Bridge, Inquiry & Synthesis

### Ch.9 — Chemical Change and an Introduction to Chemical Equations
### 第 9 章　化学变化与化学方程式入门

- **大纲对应 Content alignment**: **衔接 Science 10**，标注为 **Extension（拓展）**；完整处理属 Science 10
- **课时 Periods**: 2

**学习目标 Learning objectives**
- EN: Identify evidence of chemical change; write word equations; count atoms to check a balanced equation; state the law of conservation of mass.
- 中: 识别化学变化的证据；书写文字方程式；通过数原子检验方程式是否配平；陈述质量守恒定律。

**知识点要点 Key concepts**
1. Evidence of chemical change 化学变化的证据：color change 变色、gas produced 生成气体、precipitate formed 生成沉淀、temperature change 温度变化、light 发光、odor 气味变化
2. Word equation 文字方程式 → Skeleton equation 骨架方程式 → Balanced equation 配平方程式
   - 例：hydrogen + oxygen → water；H₂ + O₂ → H₂O；**2**H₂ + O₂ → **2**H₂O
3. Law of conservation of mass 质量守恒定律：反应前后原子种类与数目不变
4. Coefficient 系数 vs subscript 下标：**只能改系数，不能改下标**
5. Science 10 预告 next up：反应类型（synthesis 化合、decomposition 分解、single replacement 置换、double replacement 复分解、combustion 燃烧）、acid-base 酸碱、concentration 浓度

**核心词汇 Key vocabulary**
chemical change 化学变化 · physical change 物理变化 · precipitate 沉淀 · word equation 文字方程式 · skeleton equation 骨架方程式 · balanced equation 配平方程式 · coefficient 系数 · subscript 下标 · law of conservation of mass 质量守恒定律

**实验与活动 Lab / Activity**
- 化学变化观察站：小苏打+醋（气体）、硝酸铅+碘化钾（沉淀）、钢丝绒燃烧（质量变化）——教师演示，学生填证据表。
- 用彩色磁贴模型配平方程式。

**常见易错点 Common misconceptions**
- 通过改下标来配平（会改变物质本身）。
- 把"溶解""熔化"误判为化学变化。

**评估方式 Assessment**
- 知识：判断变化类型 + 配平 5 个简单方程式。
- 能力：用原子模型解释质量守恒（Formulate models / evidence-based argument）。

---

### Ch.10 — Scientific Inquiry, Lab Skills and Safety
### 第 10 章　科学探究、实验技能与安全

- **大纲对应 Content alignment**: Curricular Competencies（Planning and conducting / Processing and analyzing / Evaluating）——**贯穿全册，非独立单元**
- **课时 Periods**: 2（+ 分散在各章实验中）

**学习目标 Learning objectives**
- EN: Design a fair test with independent, dependent and controlled variables; follow WHMIS safety guidelines; record qualitative and quantitative data; identify sources of error and suggest improvements.
- 中: 设计含自变量、因变量、控制变量的公平实验；遵守 WHMIS 安全规范；记录定性与定量数据；找出误差来源并提出改进。

**知识点要点 Key concepts**
1. Scientific method 科学方法：Question 提问 → Hypothesis 假设（If…then…）→ Prediction 预测 → Experiment 实验 → Analysis 分析 → Conclusion 结论 → Communication 交流
2. Variables 变量：independent variable 自变量（主动改变）、dependent variable 因变量（被测量）、controlled variable 控制变量（保持不变）
3. Qualitative data 定性数据 vs quantitative data 定量数据；SI units 国际单位制
4. WHMIS symbols 安全标识：flammable 易燃、corrosive 腐蚀性、toxic 有毒、oxidizing 氧化性、compressed gas 压缩气体、biohazard 生物危害、environmental hazard 环境危害
5. Error and uncertainty 误差与不确定度；confounding variable 干扰变量；alternative explanation 替代解释
6. Graphing 作图：标题、坐标轴标注（含单位）、刻度、最佳拟合线；interpolation 内插 / extrapolation 外推

**核心词汇 Key vocabulary**
fair test 公平实验 · independent variable 自变量 · dependent variable 因变量 · controlled variable 控制变量 · hypothesis 假设 · qualitative 定性的 · quantitative 定量的 · WHMIS 工作场所危险物质信息系统 · error 误差 · uncertainty 不确定度 · graph 图表 · interpolation 内插 · extrapolation 外推

**实验与活动 Lab / Activity**
- 学生自主微型探究：如"哪种常见液体导电性最好？"——完整走一遍流程并写实验报告。
- 安全标识配对与实验室逃生路线演练。

**常见易错点 Common misconceptions**
- 把"控制变量"说成"不变的量"时漏掉了数量词。
- 结论超出数据支持范围（过度外推）。

**评估方式 Assessment**
- 能力为主：实验报告量规（rubric）——假设、变量控制、数据质量、结论与证据一致性、改进建议。

---

### Ch.11 — Unit Synthesis, Review and Assessment
### 第 11 章　单元综合复习与测评

- **大纲对应 Content alignment**: C1 + C2 + Big Idea 综合
- **课时 Periods**: 2

**学习目标 Learning objectives**
- EN: Integrate the whole unit around the Big Idea; complete a summative assessment covering content and competencies.
- 中: 围绕核心概念整合全单元；完成覆盖知识与能力的总结性测评。

**知识点要点 Key concepts**
1. 主线回顾（一句话串全册）：
   > **电子排布 → 周期表位置 → 价电子数 → 得失电子倾向 → 离子电荷 → 化合物的化学式与命名 → 化合物的性质**
2. 易混概念总对比表：atom/ion、element/compound、metal/non-metal、ionic/molecular、cation/anion、group/period、atomic number/mass number
3. 综合题型：
   - 给元素 → 画玻尔图 → 判断离子 → 写与另一元素的化合物 → 命名 → 预测性质
4. 现实联系（Careers & Society）：材料科学 materials science、冶金 metallurgy、半导体 semiconductor（Si 硅）、环境 chemistry、药学 pharmaceuticals

**实验与活动 Lab / Activity**
- "神秘白色粉末"鉴别实验：综合运用导电性、溶解性、熔点等性质判断未知物是 ionic 还是 molecular。
- 单元概念图 Concept map 小组海报。

**评估方式 Assessment**
- 总结性测评 Summative：知识卷（60%）+ 实验/探究任务（25%）+ 概念图或科普写作（15%）
- 中文支持：允许学生用中英双语作答术语部分，但**化学式与英文命名必须用英文**。

---

## 3. 附录框架｜Appendices

### 附录 A — Glossary 词汇总表（EN ↔ 中）
> 全册术语按章汇总，每条含：English / 中文 / 所在章 / 备注。体例：
> `atom｜原子｜Ch.1｜ smallest unit of an element 元素的最小单位`

### 附录 B — Common Ions Table 常见离子表
> 分 cations 阳离子 / anions 阴离子 / polyatomic ions 多原子离子三张表，每行：符号 / English name / 中文名 / 电荷。
> 示例：
> `Na⁺｜sodium｜钠离子｜+1`　`SO₄²⁻｜sulfate｜硫酸根｜−2`　`NH₄⁺｜ammonium｜铵根｜+1`

### 附录 C — Naming Cheat Sheet 命名速查表
> C-1 Ionic（含 -ide 词尾、罗马数字、多原子离子）
> C-2 Molecular（前缀表 + 俗名）
> C-3 **英中命名互译规则对照**（含顺序相反的说明与 20 个例句）

### 附录 D — Elements 1–20 Bilingual Table 前 20 号元素中英对照表
> 每行：Atomic number 序数 / Symbol 符号 / English name / 中文名 / 拼音 / 常见离子电荷
> 示例：`11｜Na｜sodium｜钠｜nà｜+1`　`17｜Cl｜chlorine｜氯｜lǜ｜−1`

### 附录 E — Lab & Worksheet Bank 实验与练习单
> 逐章配套：实验单（含安全提示）、练习单、概念图模板、单元测评卷与量规。

---

## 4. 编写体例约定｜Writing Conventions

1. **双语顺序**：标题与术语一律 `English（中文）`；正文解释以英文为主、中文为辅，难句给中文整句。
2. **术语一致性**：同一概念全册只用同一个中文译名（见附录 A）；BC 官方用 semi-metal，教材也用 metalloid，统一译"类金属"，并在首次出现时注明两者等价。
3. **Big Idea 回扣**：每章结尾必须有一段 "How does this connect to the Big Idea?（如何回扣核心概念）"。
4. **能力标注**：每个实验/活动后标注所训练的 Curricular Competency 编号（如 [Planning and conducting]）。
5. **中英命名分栏**：凡涉及命名的章节，用两栏表格并列展示英文命名与中文命名规则。
6. **拓展标注**：超出 BC Science 9 官方 Content 的内容（如方程式配平、酸碱）一律加 `【Extension → Science 10】` 标记，避免超纲误导。

---

## 5. 下一步｜Next Steps

- [ ] 按本框架在 `chapters/` 下逐章生成正文讲义（建议顺序：Ch.2 → Ch.5 → Ch.6 → Ch.7 → Ch.8 先做主线，再补 Ch.1、Ch.3、Ch.4、Ch.9–11）
- [ ] 生成附录 A–D（词汇表、离子表、命名速查表、元素中英对照表）
- [ ] 为每章配套练习单与实验单，放入 `assets/`
- [ ] 制作可打印版（HTML/PDF）与 Anki 词汇卡

---

*本框架依据 BC 省教育厅官方 Science 9 课程标准编制；官方原文以 curriculum.gov.bc.ca 为准。*
