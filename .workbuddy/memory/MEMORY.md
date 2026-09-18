# 项目长期记忆 — canada chemical（BC 省科学课程讲义）

## 项目背景
- 为用户（中文母语）编写 **BC 省（不列颠哥伦比亚省）中学科学课程**的英中对照讲义。
- 根目录结构：按年级分文件夹，如 `G9/`。（原同级的 `math/` 已由用户移出，与本项目无关）
- git 仓库建在**工作区根**（能覆盖未来新增的 G10 等），已排除无关 PDF。

## 已确认的大纲事实（来自 curriculum.gov.bc.ca 官网核实，勿凭记忆改写）
- **Science 9 化学部分**
  - Big Idea（仅 1 条）：The electron arrangement of atoms impacts their chemical nature.
  - Content（仅 2 条）：① element properties as organized in the periodic table；② The arrangement of electrons determines the compounds formed by elements
  - Curricular Competencies：Questioning and predicting / Planning and conducting / Processing and analyzing / Evaluating / Applying and innovating / Communicating
- **Science 8（先修）**：atomic theory and models、KMT、protons/neutrons/quarks、electrons/leptons、plate tectonics、EM radiation
- **Science 10（后接）**：rearrangement of atoms in chemical reactions、acid-base chemistry、law of conservation of mass、energy change during chemical reactions、nuclear energy
- **超纲红线**：方程式配平、酸碱、浓度、反应类型属 Science 10，9 年级讲义中只能标 `【Extension → Science 10】`。
- 官方配套教材：*BC Science Connections 9*，Unit 2 标题与 Big Idea 完全一致，Topic 2.1–2.4。

## 讲义编写体例（全项目统一）
1. 术语一律 `English（中文）`，首次出现双标注。
2. 每章结尾固定 "How does this connect to the Big Idea?"。
3. 每个实验/活动后标注所训练的 Curricular Competency。
4. 超纲内容必须加 `【Extension → Science XX】`。
5. **英中命名顺序相反**，必须两栏对照说明：
   - 英文：metal + non-metal-ide（sodium chloride）
   - 中文：非金属 + 化 + 金属（**氯化钠**）；`-ide` → "化"
6. 中文化学命名：Fe²⁺ 亚铁离子、Fe³⁺ 铁离子；多变价用罗马数字 iron(II)/iron(III)。
7. BC 官方用 semi-metal，教材常用 metalloid，统一译 "类金属"。

## 进度
- 2026-09-18 全部完成：`00_讲义章节框架` + **11 章正文**（6445 行）+ **附录 A–E**（4137 行）
  + **13 张 SVG** + 生成脚本与 CSV 数据源 + git 版本管理（提交 `c4f89f4`）。
- 待做：`assets/printables/`（A4 空白单）、`assets/cards/`（Anki 234 术语 + 元素卡）。

## 工程约定
- **图库与附录 A 是生成物，不要直接编辑**：改正文后重跑 `assets/source/` 下脚本同步。
  详见 `assets/source/README.md`（含 Git Bash 必须 unset MSYS 变量等已知坑）。
- 改完图必跑 `check_figures.py`：能自动抓出人眼看不出的文字越出 viewBox。
