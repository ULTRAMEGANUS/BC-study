# assets/source — 生成脚本与数据源

本目录存放**生成 `figures/`、`appendices/附录A` 与 `printables/` 的脚本及其数据**。
改了正文或元素数据后，重跑脚本即可同步，不需要手工改附录和练习单——
**附录 A、图表、练习单 PDF 都是"生成物"，不要直接编辑**（要改就改脚本，再重跑）。

## 文件清单

| 文件 | 作用 | 输出 |
|---|---|---|
| `build_glossary.py` | 从 11 章正文第 6 节「核心词汇」抽取、去重、字母序汇总 | `appendices/AppendixA_*.md` + `glossary.csv` |
| `build_figures.py` | 用内置元素数据生成周期表、玻尔图、路易斯点式、玻尔模板 | `figures/*.svg` × 5 + `elements_1_20.csv` |
| `check_figures.py` | 校验所有 SVG：XML 合法性、禁用标签、文字是否越出 viewBox | 控制台报告 |
| `build_printables.py` | 生成 A4 空白练习单 HTML（数据取自两个 CSV） | `printables/html/*.html` + 索引页 |
| `html2pdf.py` | HTML → A4 PDF（Chrome headless 渲染，通用） | `printables/pdf/*.pdf` |
| `glossary.csv` | 234 条术语（English / 中文 / 说明 / 出现章节），Anki·Quizlet 导入源 | — |
| `elements_1_20.csv` | 前 20 号元素（序数/符号/中英/拼音/周期/族/类别/电子排布/价电子/质量数/中子数） | — |

`figures/` 里另外 8 张（命名决策树、全册主线、交叉法、电子转移、希腊前缀、科学方法、导电性电路、WHMIS）是手写的 SVG，没有脚本——它们的内容不随数据变化，直接编辑 SVG 即可。

## 运行方法

在本机使用 WorkBuddy 自带的 Python（避免污染系统环境）。

```bash
# 进入脚本目录
cd "G9/assets/source"

PY="C:/Users/outma/.workbuddy/binaries/python/versions/3.13.12/python.exe"

# ⚠️ Git Bash 下必须 unset 这两个变量，否则绝对路径会被拼成 C:\c\Users\...
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_glossary.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" build_figures.py ../figures
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
- 无参数：自动定位 `G9/chapters/`，并**覆盖** `appendices/` 下已有的 `AppendixA_*.md`（沿用原文件名与生成时间，不产生无意义 diff）。
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

1. 编辑 `chapters/Ch*.md` 第 6 节的词汇表（`| English | 中文 | 说明 |`）。
2. 重跑 `build_glossary.py`。附录 A 的字母序总表、按章索引、自测表会全部刷新。
3. A-4「易混术语辨析」是脚本里手写的 15 组，不受正文影响，需要单独改脚本里的 `pairs` 列表。

## 已知坑

- **加粗标记**：正文词汇表里的 `**` 会在排序时把词条挤到错误位置。脚本已做剥离，但如果新增词条后字母序异常，先检查是不是带 `**`。
- **Ch.11 的第三列**：Ch.11 是「全册高频复习表」，第三列是章节引用而非注释。脚本会识别 `Ch.\d` 开头的第三列并清空——新增类似的复习表时留意这一点。
- **元素拼写**：全项目统一用 BC 拼写的 **aluminium**（不是 aluminum）。Ch02 里保留了一处并列是刻意的拼写说明，不要"修正"它。
