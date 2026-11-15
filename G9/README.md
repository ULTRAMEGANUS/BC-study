# G9 — BC Science 9 化学讲义项目｜BC Grade 9 Chemistry Lecture Notes

> 根目录 Root：`canada chemical/G9/`

## 项目目标｜Purpose

按**不列颠哥伦比亚省（BC）9 年级科学课程化学部分**官方大纲，编写一套**英中对照**的讲义，
服务在 BC 读 9 年级、母语为中文的学生——既能跟上英文课堂与考试，又能用中文建立概念底层理解。

## 大纲依据｜Source of Truth

- 官方大纲：[BC Ministry of Education — Science 9](https://curriculum.gov.bc.ca/curriculum/science/9/core)
- 官方配套教材：*BC Science Connections 9*, Unit 2 — "The electron arrangement of atoms impacts their chemical nature"
- 先修/后接：Science 8（原子论、分子运动论）→ Science 9（本册）→ Science 10（化学反应、酸碱、质量守恒）

### 化学部分官方范围（仅两条 Content）

| 官方原文 | 中文 |
|---|---|
| The electron arrangement of atoms impacts their chemical nature.（Big Idea） | 原子的电子排布决定其化学性质 |
| element properties as organized in the periodic table | 元素性质在元素周期表中的组织方式 |
| The arrangement of electrons determines the compounds formed by elements | 电子排布决定元素所形成的化合物 |

> 注意：化学方程式配平、酸碱、浓度属于 **Science 10**，本册仅以 `【Extension】` 形式做桥梁。

## 目录结构｜Structure

```
G9/
├─ 00_讲义章节框架_Course_Framework.md    ← 章节框架与总纲（先读这个）
├─ README.md                           ← 本文件
├─ MD/                                 ← 全部可编辑的 md 源与素材
│  ├─ chapters-cn/                     ← 11 章正文·中文在前（时间戳 20260918_005305）
│  ├─ chapters-en/                     ← 11 章正文·英文在前 + _STYLE.md 体例规范
│  ├─ appendices-cn/                   ← 附录 A–E（时间戳 20260918_124038）
│  └─ assets/
│     ├─ figures/                      ← SVG 矢量图（73 张）
│     ├─ printables/pdf/               ← A4 空白练习单 10 份（共 27 页）
│     ├─ cards/                        ← Anki 导入包（待做）
│     └─ source/                       ← 生成脚本与数据（改完重跑即同步）
└─ pdf/                                ← 生成物，勿手改
   ├─ CN/                              ← 中文版：11 章 + 附录 5 份 + 2 份合订本
   └─ EN/                              ← 英文在前版：11 章 + 全册合订本
```

## 图库｜Figures

`MD/assets/figures/` 下为独立 SVG 矢量图，白底、A4 友好，可直接打印或嵌入网页。
图由 `MD/assets/source/` 下的脚本生成，改脚本重跑即可同步，详见该目录 `README.md`。

## PDF 成品｜Built PDFs

| 文件 | 内容 |
|---|---|
| `pdf/CN/G9-combo.pdf` | 11 章合订本（205 页 / 书签 430 条） |
| `pdf/CN/appendix-combo-cn.pdf` | 附录 A–E 合订本（133 页 / 书签 119 条） |
| `pdf/EN/G9-combo-en.pdf` | 英文在前版全册合订本（335 页 / 书签 423 条） |

各章单篇 PDF 与合订本同源，位于 `pdf/CN/`、`pdf/EN/` 下，文件名与对应 md 一致。
注意：两份章节合订本（`G9-combo.pdf`、`G9-combo-en.pdf`）构建于 Ch01 末次重建**之前**，
合订本内的 Ch01 为旧版——以单章 PDF 为准，或重跑 `build_combo_pdf.py` 刷新。

> 图内配色与分类术语与正文、附录完全一致；所有图由 `MD/assets/source/build_figure_svg*.py`
> 生成，改脚本重跑即可全局同步，不会与附录 D 漂移。

## 生成脚本｜MD/assets/source

图库、附录 A、练习单 PDF 都是**生成物，不要直接编辑**。改完正文或元素数据后重跑脚本即同步。
详见 [`MD/assets/source/README.md`](MD/assets/source/README.md)。

| 脚本 | 输出 |
|---|---|
| `build_glossary.py` | `MD/appendices-cn/AppendixA_*.md`（234 条术语）+ `glossary.csv` |
| `build_figures.py` | `figures/*.svg` × 5（周期表 / 玻尔图 / 点式 / 模板）+ `elements_1_20.csv` |
| `check_figures.py` | 校验 SVG：XML 合法性、禁用标签、文字越界 |
| `build_printables.py` | A4 空白练习单 HTML（数据取自两个 CSV，与附录同源） |
| `html2pdf.py` | HTML → A4 PDF（Chrome headless，通用；含中文文件名保护） |

> ⚠️ Git Bash 下运行必须加 `env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL`，
> 否则绝对路径会被拼成 `C:\c\Users\...` 而静默失败。

## 附录｜Appendices

文件名含时间戳 `20260918_124038`，位于 `MD/appendices-cn/`：

| 文件 | 内容 |
|---|---|
| `AppendixA_Glossary_EN_CN_20260918_124038.md` | **词汇总表**：234 条术语，字母序总表 + 按章索引 + 15 组易混辨析 + 自测表（自动抽取自 11 章正文，术语严格一致） |
| `AppendixB_Common_Ions_Table_20260918_124038.md` | **常见离子表**：阳离子 / 阴离子 / 多原子离子 / 多变价金属 + 族号推电荷 + 离子电子数计算 + 20 项自测 |
| `AppendixC_Naming_Cheat_Sheet_20260918_124038.md` | **命名速查表**：决策树 + 离子/分子两套规则 + `-ide` 对照 + 罗马数字 + 俗名 + 20 组英中互译 + 一页纸速查卡 |
| `AppendixD_Elements_1_20_Bilingual_20260918_124038.md` | **元素中英对照表**：前 20 号元素（序数/符号/英文/中文/**拼音**/周期/族/价电子/离子/电子排布/中子数）+ 拼音索引 + 符号拉丁源 + 常考扩展元素 |
| `AppendixE_Lab_Worksheet_Bank_20260918_124038.md` | **实验与练习单**：21 份实验单 + 11 份练习单 + 100 分单元测评卷 + 3 张量规 + 4 个概念图模板 + 完整答案 |

## 章节一览｜Chapters at a Glance

| 章 | English | 中文 | 大纲对应 |
|---|---|---|---|
| Ch.1 | Matter, Atoms and Atomic Theory Review | 物质、原子与原子论回顾 | Sci 8 衔接 |
| Ch.2 | Elements, Symbols and the Periodic Table | 元素、符号与周期表 | C1 |
| Ch.3 | Groups, Periods, Metals & Non-metals | 族、周期、金属与非金属 | C1 |
| Ch.4 | Chemical Families and Reactivity Trends | 化学族与反应性趋势 | C1 |
| Ch.5 | Atomic Structure and Bohr Diagrams | 原子结构与玻尔模型图 | C1→C2 |
| Ch.6 | Ions and Lewis Dot Diagrams | 离子与路易斯点式 | C2 |
| Ch.7 | Ionic Compounds: Formulas and Naming | 离子化合物：化学式与命名 | C2 |
| Ch.8 | Molecular Compounds: Formulas and Naming | 分子化合物：化学式与命名 | C2 |
| Ch.9 | Chemical Change & Intro to Equations | 化学变化与方程式入门 | Extension→Sci 10 |
| Ch.10 | Scientific Inquiry, Lab Skills and Safety | 科学探究、实验技能与安全 | Competencies |
| Ch.11 | Unit Synthesis, Review and Assessment | 单元综合复习与测评 | C1+C2 |

建议授课顺序：Ch.2 → Ch.5 → Ch.6 → Ch.7 → Ch.8（主线），再补 Ch.1 / Ch.3 / Ch.4 / Ch.9–11。

## 体例约定｜Conventions

1. 标题与术语一律 `English（中文）`，术语首次出现双标注。
2. 每章结尾固定一段 **"How does this connect to the Big Idea?"（如何回扣核心概念）**。
3. 每个实验/活动后标注所训练的 Curricular Competency（如 `[Planning and conducting]`）。
4. 超纲内容加 `【Extension → Science 10】` 标记。
5. 命名章节用**两栏表格**并列展示英文命名规则与中文命名规则（两者顺序相反，需特别提示）。

## 正文讲义｜Chapter Files

文件名含时间戳 `20260918_005305`，位于 `MD/chapters-cn/`（英文在前版同名，位于 `MD/chapters-en/`）：

| 文件 | 章节 |
|---|---|
| `Ch01_Matter_Atoms_AtomicTheory_20260918_005305.md` | 物质、原子与原子论回顾（**样板章**） |
| `Ch02_Elements_Symbols_PeriodicTable_20260918_005305.md` | 元素、符号与周期表 |
| `Ch03_Groups_Periods_Metals_Nonmetals_20260918_005305.md` | 族、周期、金属与非金属 |
| `Ch04_Chemical_Families_Reactivity_20260918_005305.md` | 化学族与反应性趋势 |
| `Ch05_Atomic_Structure_Bohr_Diagrams_20260918_005305.md` | 原子结构与玻尔模型图 |
| `Ch06_Ions_Lewis_Dot_Diagrams_20260918_005305.md` | 离子与路易斯点式 |
| `Ch07_Ionic_Compounds_Formulas_Naming_20260918_005305.md` | 离子化合物：化学式与命名 |
| `Ch08_Molecular_Compounds_Formulas_Naming_20260918_005305.md` | 分子化合物：化学式与命名 |
| `Ch09_Chemical_Change_Intro_Equations_20260918_005305.md` | 化学变化与方程式入门（Extension） |
| `Ch10_Scientific_Inquiry_Lab_Safety_20260918_005305.md` | 科学探究、实验技能与安全 |
| `Ch11_Unit_Synthesis_Review_Assessment_20260918_005305.md` | 单元综合复习与测评 |

**统一体例（每章 10 节）**：大纲对应 → 学习目标 → **概念解析** → **表格比对** → **图例说明**
→ 核心词汇 → 实验与活动 → 常见易错点 → **答题评估** → 回扣 Big Idea。

- 图例为 `MD/assets/figures/` 下的独立 SVG（内联进 PDF 以保住中文文本层）；附录 E 的填空表单仍保留可手写的代码块。
- 答题评估统一为 A 基础题 10×2 分 + B 应用题 4×5 分 + C 挑战题 2×10 分，附完整参考答案与评分量规。

## 状态｜Status

- [x] 建立根目录与结构
- [x] 完成英中对照章节框架（`00_讲义章节框架_Course_Framework.md`）
- [x] 完成 11 章正文讲义（`MD/chapters-cn/`，共 6445 行）
- [x] 完成附录 A–E（`MD/appendices-cn/`，共 4137 行）
- [x] 完成图库 `MD/assets/figures/`（86 张 SVG）
- [x] 完成 A4 空白练习单 `MD/assets/printables/pdf/`（10 份 PDF，27 页，每份末页附答案）
- [ ] Anki 词汇卡 `MD/assets/cards/`
- [x] 可打印版讲义：`pdf/CN/G9-combo.pdf`、`pdf/CN/appendix-combo-cn.pdf`、`pdf/EN/G9-combo-en.pdf`
- [ ] 附录英文版 `MD/appendices-en/`

### 建议学习路径

1. 通读 `00_讲义章节框架_Course_Framework.md` 建立全局观。
2. 按 Ch.1 → Ch.11 顺序学正文，每章做完第 9 节「答题评估」。
3. **随时查**：附录 A 词汇 / 附录 B 离子 / 附录 C 命名 / 附录 D 元素。
4. **动手写**：`MD/assets/printables/pdf/` 的 10 份 A4 空白练习单，学完一章做一份。
5. **考前**：附录 E 的 11 份练习单 + 单元测评卷 + 附录 A-4 易混辨析。
