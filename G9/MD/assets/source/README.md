# assets/source — 生成脚本与数据源

> 本目录位于 `G9/MD/assets/source/`。脚本按「上三级 = G9 根、上两级 = G9/MD」自动定位目录，
> 所以在任意工作目录下运行都能找到 md 与 PDF 输出位置。

本目录存放**生成 `figures/`、`MD/appendices-cn/附录A` 与 `printables/` 的脚本及其数据**。
改了正文或元素数据后，重跑脚本即可同步，不需要手工改附录和练习单——
**附录 A、图表、练习单 PDF 都是"生成物"，不要直接编辑**（要改就改脚本，再重跑）。

## 文件清单

| 文件 | 作用 | 输出 |
|---|---|---|
| `build_glossary.py` | 从 11 章正文第 6 节「核心词汇」抽取、去重、字母序汇总 | `MD/appendices-cn/AppendixA_*.md` + `glossary.csv` |
| `build_figures.py` | ⚠️ **已停用**（2026-11-15）：其 5 张产物图属无引用的一代旧图，已清理；勿再运行 | — |
| `build_figure_svg.py` | **讲义配图底座**：调色板、`head/box/txt/path/dot` 等绘图原语、箭头 marker | 被 svg2/3/4 复用，自身也出图 |
| `build_figure_svg2.py` | Ch02–Ch04 配图（周期表、同位素、族位置、反应性、双原子分子…） | `figures/ch02-*.svg` `ch03-*.svg` `ch04-*.svg`（12 张） |
| `build_figure_svg3.py` | Ch05–Ch06 配图。含两个参数化函数的**老巢**：`bohr_panel()` 画玻尔图、`lewis()` 画路易斯点式 | `figures/ch05-*.svg` `ch06-*.svg`（19 张） |
| `build_figure_svg4.py` | Ch07–Ch11 配图（交叉法、共价键、WHMIS、探究循环、总决策树…） | `figures/ch07-*.svg` … `ch11-*.svg`（30 张） |
| `build_figure_svg5.py` | 附录配图：C-1 决策树、C-7 中英顺序、C 速查卡；E 的变量/分类树/电路/玻尔参考答案 | `figures/appc-*.svg` `appe-*.svg`（9 张） |
| `beautify_md.py` | **给 md 做排版美化**（md 浏览器友好）：补图题、去冗余分隔线、提示块加 emoji、行内【】加 emoji。**幂等**，可重复跑 | 就地改写 `MD/chapters-cn/*.md` + `MD/appendices-cn/*.md` |
| `check_svg_bounds.py` | **越界自检**：扫所有 SVG，报出被画布裁掉的图元（见"已知坑"） | 控制台报告 |
| `check_figures.py` | 校验 SVG：XML 合法性、禁用标签、文字是否越出 viewBox | 控制台报告 |
| `build_figure_index.py` | 扫章节 md 的 `![]()` 引用，重建 `figures/index.html` 图库页（index.html 已随 2026-11-15 清理移除；需要时再跑） | `figures/index.html` |
| `build_chapter_pdf.py` | md → HTML → Chrome headless A4 PDF；SVG **内联**（不用 `<img>`）以保住中文文本层。默认 `--src chapters-cn` → `G9/pdf/CN/`；`--src chapters-en` → `G9/pdf/EN/` | `G9/pdf/CN/Ch*_*.pdf`、`G9/pdf/EN/Ch*_*.pdf` |
| `build_combo_pdf.py` | 合订本：合并多篇 PDF 并从 md 标题重建三级书签（Chrome 不打书签）；页标签按篇重置以对齐页脚。`--src appendices-cn --pattern 'Appendix*.pdf'` 出附录册 | `G9/pdf/CN/G9-combo.pdf`、`G9/pdf/CN/appendix-combo-cn.pdf`、`G9/pdf/EN/G9-combo-en.pdf` |
| `check_chapter_pdf.py` | 校验章节 PDF：页数、中文字数、溢出、页码、SVG 是否真渲染进文本层 | 控制台报告 |
| `build_printables.py` | 生成 A4 空白练习单 HTML（数据取自两个 CSV） | `../printables/html/*.html` + 索引页（中间产物，已 gitignore） |
| `html2pdf.py` | HTML → A4 PDF（Chrome headless 渲染，通用） | `printables/pdf/*.pdf` |
| `glossary.csv` | 234 条术语（English / 中文 / 说明 / 出现章节），Anki·Quizlet 导入源 | — |
| `elements_1_20.csv` | 前 20 号元素（序数/符号/中英/拼音/周期/族/类别/电子排布/价电子/质量数/中子数） | — |

`figures/` 现有 **73 张 SVG，全部由脚本生成**（`build_figure_svg*.py`），
不再有任何手写 SVG——要改图就改脚本再重跑，别直接编辑 `figures/*.svg`（下次重跑会被覆盖）。
> 2026-11-15 清理：删除 13 张无引用的一代旧图（`periodic-table-1-20-bilingual`、`periodic-table-blank`、
> `bohr-diagrams-1-20`、`bohr-diagram-template`、`lewis-dot-elements`、`ion-formation-Na-Cl`、
> `naming-decision-tree`、`criss-cross-method`、`greek-prefixes-chart`、`main-thread-flowchart`、
> `scientific-method-cycle`、`whmis-symbols`、`conductivity-circuit`）与 `index.html` 图库页；
> 其产出者 `build_figures.py` 保留作历史参考，但重跑会复活这 13 张图，勿再运行。
> 一次性文本工具 `scan_md_figures.py`、`swap_ascii_blocks.py`、`swap_appendix_blocks.py`、
> `normalize_encn.py` 已随清理移除（git 历史可恢复）。

## md 的两种消费方式，以及为什么要跑 beautify_md.py

同一份 md 有两种读法：**排成 PDF**（`build_chapter_pdf.py`，有 CSS 和配色）和
**直接在 Markdown 浏览器里翻**（mdview 一类工具）。后者只有标准 Markdown 的渲染结果，
会显得平、碎、找不着重点。`beautify_md.py` 就是补上这一层。

⚠️ **mdview 会省略原始 HTML**。goldmark / GitHub 风格内核明文写着 `Raw HTML is omitted`
（或转义）。所以 `<div style>`、`<span>`、`<img width=...>`、Mermaid **全部不可用**，
想做彩色提示块只能靠 **emoji + 引用块 + 粗体**（emoji 由浏览器渲染成彩色，
视觉上等价于 PDF 的配色分区）。改动 md 前先确认目标渲染器能吃哪套语法。

`beautify_md.py` 做的事（**幂等**，可放心重复跑）：
1. 补图题——SVG 的 alt 在 mdview 里不显示。但**只给前面没有 `### 图 X-Y` 标题的图补**
   （74 张图里多数已有标题，补了就重复）。
2. 删冗余分隔线——`---` + 紧随的 `## ` 在 GitHub CSS 下是双线，很吵。
3. 提示块加 emoji——按标签语义分类（⚠️ 易错 / 💡 记忆 / 📏 规则 / 🎯 Big Idea /
   👩‍🏫 教师 / 🔭 超纲 / ⏱️ 课时…），已有 emoji 的跳过。
4. 行内【】加 emoji——`【Extension → Science 10】` → `【🔭 Extension …】`；
   **填空 `【____】` 一律不动**。

⚠️ **配套改动**：`build_chapter_pdf.py` 会跳过 `**📊` 开头的图题行——
SVG 内部已经画了图题，PDF 里再出现一次就重复了。

⚠️ **附录 A 是生成物**：`beautify_md.py` 改完 `AppendixA_*.md` 后，
若重跑 `build_glossary.py` 会被还原。正确顺序是**先生成、后美化**。

⚠️ **附录 E 的 ASCII 块不能全换**：那是实验练习单，里面大量
`NAME 姓名：____`、`【____ 物质】` 是**给学生填的**，换成 SVG 就没法填写了。
判定办法：看代码块里有没有 `_{3,}` 连续下划线——有就是表单，保留。

## 运行方法

在本机使用 WorkBuddy 自带的 Python（避免污染系统环境）。

```bash
# 进入脚本目录
cd "G9/MD/assets/source"

PY="C:/Users/outma/.workbuddy/binaries/python/versions/3.13.12/python.exe"

# ⚠️ Git Bash 下必须 unset 这两个变量，否则绝对路径会被拼成 C:\c\Users\...
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_glossary.py
# build_figures.py 已停用（其 5 张产物图 2026-11-15 清理移除，见上方说明）

# 讲义配图（改图后跑这三步）
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_figure_svg.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_figure_svg2.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_figure_svg3.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_figure_svg4.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_figure_svg5.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" check_svg_bounds.py   # 越界自检，必须为 0

# md 排版美化（md 浏览器友好；附录 A 要在 build_glossary.py 之后跑）
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" beautify_md.py

# 章节 PDF
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_chapter_pdf.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" check_chapter_pdf.py

# 附录 PDF（同一套管线，只换 --src）
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_chapter_pdf.py --src appendices-cn

# 合订本（书签 + 页标签）
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_combo_pdf.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_combo_pdf.py --src appendices-cn --pattern 'Appendix*.pdf'

env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY"
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_chapter_pdf.py --src chapters-en
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_combo_pdf.py --src chapters-en

env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" check_figures.py ../figures

# 生成练习单 HTML，再渲染成 A4 PDF
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_printables.py ../printables
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" html2pdf.py ../printables/html ../printables/pdf
```

## 练习单（printables/）

10 份 A4 空白练习单，每份**末页附答案**（教师可打印后裁下）。数据源与附录同源：
元素取自 `elements_1_20.csv`，词汇取自 `glossary.csv`。

| 编号 | 内容 | 页数 |
|---|---|---|
| P01 | 空白周期表（按序数填 / 按符号填两版） | 2 |
| P02 | 元素符号与英文名默写（30 个） | 3 |
| P03 | 玻尔图练习（15 个元素，含 SVG 空圆） | 2 |
| P04 | 离子形成练习（族号推电荷 + 多变价/多原子离子） | 2 |
| P05 | 路易斯点式练习（原子 15 + 离子 6） | 3 |
| P06 | 离子化合物命名（化学式 ↔ 英文 ↔ 中文） | 4 |
| P07 | 分子化合物命名（前缀 + 俗名） | 2 |
| P08 | ionic / molecular 判断 + 性质预测 | 2 |
| P09 | 核心词汇默写（按章，65 词） | 5 |
| P10 | 错题整理单 + 自测打卡 + 考前一页纸 | 2 |

### 练习单的两个设计红线（改动时务必守住）

1. **同一份练习单内，各 Part 的题目不能交叉。** 否则上一 Part 的答案会印在下一 Part 的
   题干里，单子直接失效（例如 P06 的 B 组给了 `iron(III) oxide`，C 组就不能再出「氧化铁」）。
   `build_printables.py` 里 P06 有 `assert` 自检，交叉会直接报错退出。
2. **「英→中」与「中→英」必须是互不重叠的两批词。** 若同一行左右并排，等于把答案写在旁边。
   P09 按 `CORE_WORDS` 均分成 A/B 两组，也有 assert 把关。

## 参数说明

**`build_glossary.py`**
- 无参数：自动定位 `G9/MD/chapters-cn/`，并**覆盖** `MD/appendices-cn/` 下已有的 `AppendixA_*.md`（沿用原文件名与生成时间，不产生无意义 diff）。
- 两个参数：`python build_glossary.py <chapters目录> <输出md>`。

**`build_figures.py`**
- 一个参数：输出目录（通常 `../figures`）。元素数据在脚本内的 `ELEMENTS` 列表，改数据改这里。

**`check_figures.py`**
- 一个参数：待校验目录。会报告 XML 错误、`<image>`/`<foreignObject>` 等禁用标签、文字超出 viewBox 的情况。

**`build_printables.py`**
- 一个参数：输出目录（通常 `../printables`）。生成 `html/` 与 `index.html`；PDF 由 `html2pdf.py` 渲染。
- 改题目改脚本里的常量（`IONIC_A/B/C`、`CORE_WORDS`、`P08_ITEMS` 等），别改生成的 HTML。

**`html2pdf.py`**
- 参数：`html2pdf.py <html文件或目录> [输出目录]`。自动探测 Chrome / Edge。
- ⚠️ **Chrome 用系统 ANSI 代码页解析命令行，非 ASCII 的输出文件名会被静默丢弃**——
  它照样打印 "bytes written"，但文件根本不存在。脚本已用 ASCII 临时名中转再 `os.replace`，
  **不要绕过这层保护**。
- 无 PDF 阅读器时的校验：`pymupdf` 提取文本做断言（页数、中文字符数、`/FontFile2` 字体嵌入数）。

## 修改正文后怎么同步

1. 编辑 `MD/chapters-cn/Ch*.md` 第 6 节的词汇表（`| English | 中文 | 说明 |`）。
2. 重跑 `build_glossary.py`。附录 A 的字母序总表、按章索引、自测表会全部刷新。
3. A-4「易混术语辨析」是脚本里手写的 15 组，不受正文影响，需要单独改脚本里的 `pairs` 列表。

## 已知坑

- **SVG 画布高度是手写的，画超了会被静默裁掉。** `head(900, 486, …)` 里的高度是硬编码数字，
  后面再往里加内容却忘了同步改，超出的部分浏览器/PDF 直接裁掉——**既不报错也不警告**。
  实例：`ch10-whmis` 的整条底部注记（y=494–526，画布只有 486）就这样丢了。
  对策：改完图必跑 `check_svg_bounds.py`（目标：**越界 0 张**）；
  新写函数尽量让高度由内容算出（见 `fig_ch11_master` / `fig_ch11_route` 的 `H = …` 写法）。
- **长英文串在中文断行规则下不换行。** 如 `(a) sodium 钠　(b) potassium 钾 …` 用全角空格分隔时
  会溢出右边距。只加 `overflow-wrap: anywhere` 无效，必须同时加 **`line-break: anywhere`**
  （已写在 `build_chapter_pdf.py` 的 `p {}` 里）。
- **SVG 里的 `&` 必须写成 `&amp;`。** 标题里写 `Three Regions & the Zigzag` 会让 XML 解析失败，
  而失败时 `build_figure_svg*.py` 未必报错——靠 `check_svg_bounds.py` 之前的 XML 校验兜底。
- **加粗标记**：正文词汇表里的 `**` 会在排序时把词条挤到错误位置。脚本已做剥离，但如果新增词条后字母序异常，先检查是不是带 `**`。
- **Ch.11 的第三列**：Ch.11 是「全册高频复习表」，第三列是章节引用而非注释。脚本会识别 `Ch.\d` 开头的第三列并清空——新增类似的复习表时留意这一点。
- **ASCII 图太高会被 Chrome 拆到两页。** `.fig` 是 `page-break-inside: avoid`，
  但超过一页的图（如附录 E 整页的实验报告模板，845pt > A4 可用 740pt）仍会被拆断，
  一张完整的表格变成两半。对策：`_fit_page()` 把图等比缩到
  `FIG_MAX_H_PT = 720` 以内（代价只是字略小）。章节里最高的图 386pt，不受影响。
- **元素拼写**：全项目统一用 BC 拼写的 **aluminium**（不是 aluminum）。Ch02 里保留了一处并列是刻意的拼写说明，不要"修正"它。
