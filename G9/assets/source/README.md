# assets/source — 生成脚本与数据源

本目录存放**生成 `figures/` 与 `appendices/附录A` 的脚本及其数据**。
改了正文或元素数据后，重跑脚本即可同步，不需要手工改附录——
**附录 A 与图表都是"生成物"，不要直接编辑**。

## 文件清单

| 文件 | 作用 | 输出 |
|---|---|---|
| `build_glossary.py` | 从 11 章正文第 6 节「核心词汇」抽取、去重、字母序汇总 | `appendices/AppendixA_*.md` + `glossary.csv` |
| `build_figures.py` | 用内置元素数据生成周期表、玻尔图、路易斯点式、玻尔模板 | `figures/*.svg` × 5 + `elements_1_20.csv` |
| `check_figures.py` | 校验所有 SVG：XML 合法性、禁用标签、文字是否越出 viewBox | 控制台报告 |
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
```

## 参数说明

**`build_glossary.py`**
- 无参数：自动定位 `G9/chapters/`，并**覆盖** `appendices/` 下已有的 `AppendixA_*.md`（沿用原文件名与生成时间，不产生无意义 diff）。
- 两个参数：`python build_glossary.py <chapters目录> <输出md>`。

**`build_figures.py`**
- 一个参数：输出目录（通常 `../figures`）。元素数据在脚本内的 `ELEMENTS` 列表，改数据改这里。

**`check_figures.py`**
- 一个参数：待校验目录。会报告 XML 错误、`<image>`/`<foreignObject>` 等禁用标签、文字超出 viewBox 的情况。

## 修改正文后怎么同步

1. 编辑 `chapters/Ch*.md` 第 6 节的词汇表（`| English | 中文 | 说明 |`）。
2. 重跑 `build_glossary.py`。附录 A 的字母序总表、按章索引、自测表会全部刷新。
3. A-4「易混术语辨析」是脚本里手写的 15 组，不受正文影响，需要单独改脚本里的 `pairs` 列表。

## 已知坑

- **加粗标记**：正文词汇表里的 `**` 会在排序时把词条挤到错误位置。脚本已做剥离，但如果新增词条后字母序异常，先检查是不是带 `**`。
- **Ch.11 的第三列**：Ch.11 是「全册高频复习表」，第三列是章节引用而非注释。脚本会识别 `Ch.\d` 开头的第三列并清空——新增类似的复习表时留意这一点。
- **元素拼写**：全项目统一用 BC 拼写的 **aluminium**（不是 aluminum）。Ch02 里保留了一处并列是刻意的拼写说明，不要"修正"它。
