# -*- coding: utf-8 -*-
"""
重建 assets/figures/index.html：把图库里所有 SVG 补进索引页。

已存在的卡片（含手写详细说明）保持原样，只为「新增且未收录」的图追加卡片，
描述取自章节 md 里的图片 alt（即图号 + 中英标题），因此与正文永远同步。

用法：python build_figure_index.py
"""
import os
import re
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(HERE), "figures")
MD = os.path.dirname(os.path.dirname(HERE))               # .../G9/MD
CH_DIR = os.path.join(MD, "chapters-cn")
INDEX = os.path.join(FIG_DIR, "index.html")

# md 里的引用 → alt 文本（含图号与中英标题）
ALT = {}
for f in sorted(glob.glob(os.path.join(CH_DIR, "Ch*.md"))):
    chap = os.path.basename(f)[:4]
    for alt, name in re.findall(r"!\[(.*?)\]\(\.\./assets/figures/(.*?)\)",
                                open(f, encoding="utf-8").read()):
        ALT.setdefault(name, (chap, alt))

html = open(INDEX, encoding="utf-8").read()
have = set(re.findall(r'<img src="([^"]+\.svg)"', html))
missing = sorted(f for f in os.listdir(FIG_DIR)
                 if f.endswith(".svg") and f not in have)

cards = []
for name in missing:
    chap, alt = ALT.get(name, ("", name.replace(".svg", "")))
    en = alt.split("｜")[-1] if "｜" in alt else alt
    zh = alt.split("｜")[0] if "｜" in alt else alt
    title = f"{zh}（{chap}）" if chap else zh
    cards.append(f"""
  <div class="card">
    <h2>{title}</h2>
    <div class="en">{en}</div>
    <img src="{name}" alt="{zh}">
    <p>{alt}</p>
  </div>
""")

if cards:
    html = html.replace("\n</div>\n\n<footer>",
                        "\n" + "".join(cards) + "\n</div>\n\n<footer>", 1)

total = len(glob.glob(os.path.join(FIG_DIR, "*.svg")))
html = re.sub(r"共 \d+ 张 SVG 矢量图", f"共 {total} 张 SVG 矢量图", html)
html = html.replace(
    "元素类图表由 <code>assets/source/build_figures.py</code> 生成，改脚本重跑即可全局同步；",
    "各章示意图由 <code>assets/source/build_figure_svg*.py</code> 生成，"
    "索引页由 <code>build_figure_index.py</code> 同步，改脚本重跑即可全局更新；")
open(INDEX, "w", encoding="utf-8", newline="\n").write(html)
print(f"index.html 已更新：新增 {len(cards)} 张卡片，图库共 {total} 张 SVG")
