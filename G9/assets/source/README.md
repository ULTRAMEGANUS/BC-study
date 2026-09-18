# assets/source — 生成脚本与数据源

本目录存放**生成 `figures/`、`appendices/附录A` 与 `ppt/` 的脚本及其数据**。
改了正文或元素数据后，重跑脚本即可同步，不需要手工改附录和幻灯片——
**附录 A、图表、PPT 都是"生成物"，不要直接编辑**。

## 文件清单

| 文件 | 作用 | 输出 |
|---|---|---|
| `build_glossary.py` | 从 11 章正文第 6 节「核心词汇」抽取、去重、字母序汇总 | `appendices/AppendixA_*.md` + `glossary.csv` |
| `build_figures.py` | 用内置元素数据生成周期表、玻尔图、路易斯点式、玻尔模板 | `figures/*.svg` × 5 + `elements_1_20.csv` |
| `check_figures.py` | 校验所有 SVG：XML 合法性、禁用标签、文字是否越出 viewBox | 控制台报告 |
| `build_pptx.py` | 章节 md → 英中对照教学 PPT（16:9，自动分页/续页） | `ppt/ChXX_*.pptx` |
| `check_pptx.py` | 校验 pptx：形状越界、文本溢出框、表格压页脚 | 控制台报告 |
| `glossary.csv` | 234 条术语（English / 中文 / 说明 / 出现章节），Anki·Quizlet 导入源 | — |
| `elements_1_20.csv` | 前 20 号元素（序数/符号/中英/拼音/周期/族/类别/电子排布/价电子/质量数/中子数） | — |

`figures/` 里另外 8 张（命名决策树、全册主线、交叉法、电子转移、希腊前缀、科学方法、导电性电路、WHMIS）是手写的 SVG，没有脚本——它们的内容不随数据变化，直接编辑 SVG 即可。

## 运行方法

在本机使用 WorkBuddy 自带的 Python（避免污染系统环境）。
生成 PPT 需要 `python-pptx`，装在一个独立 venv 里，因此**用另一个解释器路径**。

```bash
# 进入脚本目录
cd "G9/assets/source"

PY="C:/Users/outma/.workbuddy/binaries/python/versions/3.13.12/python.exe"           # 基础
VENV="C:/Users/outma/.workbuddy/binaries/python/envs/default/Scripts/python.exe"      # 含 python-pptx

# ⚠️ Git Bash 下必须 unset 这两个变量，否则绝对路径会被拼成 C:\c\Users\...
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY"   build_glossary.py
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY"   build_figures.py ../figures
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY"   check_figures.py ../figures

# 生成章节 PPT（第 3 个参数起可追加要插入的 SVG 文件名）
env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$VENV" build_pptx.py \
    ../../chapters/Ch01_Matter_Atoms_AtomicTheory_20260918_005305.md \
    ../../ppt/Ch01_Matter_Atoms_AtomicTheory.pptx \
    main-thread-flowchart.svg

env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$VENV" check_pptx.py \
    ../../ppt/Ch01_Matter_Atoms_AtomicTheory.pptx
```

> 若 venv 里的 `python-pptx` 丢了：`pip install python-pptx -i https://mirrors.aliyun.com/pypi/simple/`
> （清华源在本机取不到该包。）

## 参数说明

**`build_glossary.py`**
- 无参数：自动定位 `G9/chapters/`，并**覆盖** `appendices/` 下已有的 `AppendixA_*.md`（沿用原文件名与生成时间，不产生无意义 diff）。
- 两个参数：`python build_glossary.py <chapters目录> <输出md>`。

**`build_figures.py`**
- 一个参数：输出目录（通常 `../figures`）。元素数据在脚本内的 `ELEMENTS` 列表，改数据改这里。

**`check_figures.py`**
- 一个参数：待校验目录。会报告 XML 错误、`<image>`/`<foreignObject>` 等禁用标签、文字超出 viewBox 的情况。

**`build_pptx.py`**
- 用法：`build_pptx.py <章节.md> <输出.pptx> [附加SVG ...]`
- 自动解析 md 的标题层级、Markdown 表格、代码围栏（ASCII 图）、列表、引用，
  生成封面 → 章节分隔页 → 内容页 → 表格页 → 图页，超长内容**自动续页，不丢弃**。
- 页码、章节标签、配色、双语字体全部由脚本统一处理，11 章版式天然一致。

**`check_pptx.py`**
- 一个参数：pptx 文件。检查形状越界、文本溢出文本框、表格压页脚。
- **本机没有 PowerPoint / LibreOffice，无法真实渲染**，只能靠几何 + 文本量估算体检，
  所以生成后仍建议在 PowerPoint 里目视确认一遍。

## 修改正文后怎么同步

1. 编辑 `chapters/Ch*.md` 第 6 节的词汇表（`| English | 中文 | 说明 |`）。
2. 重跑 `build_glossary.py`。附录 A 的字母序总表、按章索引、自测表会全部刷新。
3. A-4「易混术语辨析」是脚本里手写的 15 组，不受正文影响，需要单独改脚本里的 `pairs` 列表。
4. 改了正文内容后，重跑 `build_pptx.py` 即可刷新对应章节的 PPT。

## 已知坑

- **加粗标记**：正文词汇表里的 `**` 会在排序时把词条挤到错误位置。脚本已做剥离，但如果新增词条后字母序异常，先检查是不是带 `**`。
- **Ch.11 的第三列**：Ch.11 是「全册高频复习表」，第三列是章节引用而非注释。脚本会识别 `Ch.\d` 开头的第三列并清空——新增类似的复习表时留意这一点。
- **元素拼写**：全项目统一用 BC 拼写的 **aluminium**（不是 aluminum）。Ch02 里保留了一处并列是刻意的拼写说明，不要"修正"它。

### PPT 相关的坑

- **文本高度估算**：`est_height()` 里「每行容纳的 em 数 = 可用宽度(pt) / 字号」。
  早先版本误用「字符数」当分母（多乘了一个 0.55），把高度低估了近一倍，导致内容重叠。**别改回旧算法。**
- **文本框高度要按估算值设置**，不要写死 0.3in，否则 PowerPoint 里可能触发意外缩放。
- **表格行高必须按内容算**（`_row_heights`）：PowerPoint 表格行会自动增高，
  若给的行高小于内容需要，表格会被撑大并顶到页脚。
- **表格续页必须带表头**，否则第二页看不出列含义。
- **ASCII 字符画用 Consolas**：中文会回退到系统字体，宽度约为西文的 1.8 倍，
  因此含中文的图可能轻微错位。这是 Windows 无中英等宽字体的固有限制。
- **SVG 转 PNG 依赖 Edge headless**：脚本自动探测 `Program Files (x86)` 与
  `Program Files` 两个路径。若换机器没有 Edge/Chrome，SVG 页会被跳过。
