# -*- coding: utf-8 -*-
"""
把章节 md 里指定的 ASCII 代码块替换为图片引用。

按「第 N 个代码块」定位而不是行号，行号会因替换而漂移。
同一 md 内多个替换按序号降序执行。

用法：
    python swap_ascii_blocks.py            # 执行 PLAN 中登记的全部替换
    python swap_ascii_blocks.py Ch02       # 只处理文件名含 Ch02 的条目
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CH_DIR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "chapters-cn")


def split_blocks(lines):
    """返回 [(start, end)]，闭区间，含首尾 ``` 行。"""
    out, i, n = [], 0, len(lines)
    while i < n:
        if lines[i].lstrip().startswith("```"):
            st = i
            i += 1
            while i < n and not lines[i].lstrip().startswith("```"):
                i += 1
            out.append((st, i))
        i += 1
    return out


def swap(md_path, index, new_lines, add_title=None, expect=None):
    """把第 index 个代码块（1-based）整块替换为 new_lines（list）。

    expect 给出「块内首行应包含的片段」做保险校验：因为序号会随替换漂移，
    一旦数错就可能换掉相邻的块，校验能立刻中止而不是静默改错文件。
    """
    with open(md_path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    blocks = split_blocks(lines)
    if index < 1 or index > len(blocks):
        raise SystemExit(f"块序号越界：{md_path} 只有 {len(blocks)} 个块，要第 {index} 个")
    st, en = blocks[index - 1]
    if expect:
        head_txt = "\n".join(lines[st + 1:min(en, st + 4)])
        if expect not in head_txt:
            raise SystemExit(f"块{index} 内容校验失败：开头是 {head_txt[:60]!r}，"
                             f"不含 {expect!r}")
    body = new_lines[:]
    if add_title:
        body = ["", add_title, ""] + body
    lines[st:en + 1] = body
    with open(md_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print(f"  替换 {os.path.basename(md_path)} 块{index} "
          f"（原 {en - st + 1} 行 → {len(body)} 行）")


def img(alt, name):
    return [f"![{alt}](../assets/figures/{name})", ""]


# md 文件名关键字 → [(块序号, 替换内容, 可选的标题行)]
PLAN = {
    "Ch02": [
        (2, img("图 2-1　周期表方格怎么读｜Reading a Cell",
                "ch02-periodic-table-cell.svg")),
        (3, img("前 20 号元素简易周期表｜Simplified Periodic Table (1–20)",
                "periodic-table-1-20-simple.svg")),
        (4, img("图 2-3　同位素：质子同、中子不同｜Isotopes",
                "ch02-isotopes-carbon.svg")),
        (5, img("图 2-4　为什么改按原子序数排序｜Mass Order vs Number Order",
                "ch02-mass-vs-number-order.svg")),
    ],
    "Ch03": [
        (1, img("图 3-1　把周期表当「地图」读｜Reading the Map",
                "ch03-periodic-table-map.svg")),
        (2, img("前 20 号元素简易周期表｜Simplified Periodic Table (1–20)",
                "periodic-table-1-20-simple.svg")),
        (3, img("图 3-3　三大区与锯齿线｜Three Regions & the Zigzag Line",
                "ch03-zigzag-regions.svg")),
        (4, img("图 3-4　导电性检测电路｜Conductivity Test Circuit",
                "ch03-conductivity-test.svg")),
    ],
    "Ch09": [
        (3, img("图 9-1　化学变化证据盘｜Evidence of Chemical Change",
                "ch09-evidence-of-change.svg"), None, "IS IT A CHEMICAL CHANGE?"),
        (4, img("图 9-2　三级方程式阶梯｜From Words to a Balanced Equation",
                "ch09-three-levels.svg"), None, "第 1 级"),
        (5, img("图 9-3　磁贴配平示意｜Sticker Model for Balancing",
                "ch09-sticker-balancing.svg"), None, "每个方框 = 1 个原子"),
        (6, img("图 9-4　系数 vs 下标解剖图｜Anatomy of a Formula",
                "ch09-anatomy-formula.svg"), None, "coefficient 系数"),
    ],
    "Ch10": [
        (1, img("图 10-1　科学探究循环流程图｜The Inquiry Cycle",
                "ch10-inquiry-cycle.svg"), None, "1. QUESTION 提问"),
        (2, img("图 10-2　变量三栏对照｜Variables at a Glance",
                "ch10-variables.svg"), None, "INDEPENDENT 自变量"),
        (3, img("图 10-3　WHMIS 标识图形卡｜WHMIS Pictogram Cards",
                "ch10-whmis-pictograms.svg"), None, "① FLAMMABLE"),
        (4, img("图 10-4　数据记录表与作图规范｜Data Table & Graph Standards",
                "ch10-table-and-graph.svg"), None, "① 数据记录表"),
        (5, img("图 10-5　内插与外推｜Interpolation vs Extrapolation",
                "ch10-interpolation.svg"), None, "Time (s)"),
    ],
    "Ch11": [
        (2, img("图 11-1　全册主线流程图｜The Master Flowchart",
                "ch11-master-flowchart.svg"), None, "全册主线"),
        (3, img("图 11-2　「一条龙」解题路径｜The One-Stop Problem Route",
                "ch11-one-stop-route.svg"), None, "STEP 1  给元素"),
        (4, img("图 11-3　化合物类型决策树｜Compound Decision Tree",
                "ch11-decision-tree.svg"), None, "给定两种元素"),
        (5, img("图 11-4　一条龙示范 1：Ca 与 Cl｜Worked Example — Calcium + Chlorine",
                "ch11-example-ca-cl.svg"), None, "Ca 原子序数 20"),
        (6, img("图 11-5　一条龙示范 2：Al 与 O｜Worked Example — Aluminium + Oxygen",
                "ch11-example-al-o.svg"), None, "Al 原子序数 13"),
        (7, img("图 11-6　一条龙示范 3：C 与 O｜Worked Example — Carbon + Oxygen",
                "ch11-example-c-o.svg"), None, "C (2, 4)"),
    ],
    "Ch08": [
        (2, img("图 8-1　共价键的形成｜How a Covalent Bond Forms (H₂)",
                "ch08-covalent-bond.svg"), None, "两个 H 原子各有 1 个电子"),
        (3, img("图 8-2　三种常见分子的点式与结构式｜Lewis & Structural Formulas",
                "ch08-three-molecules.svg"), None, "H₂O"),
        (4, img("图 8-3　单键 / 双键 / 三键｜Single, Double and Triple Bonds",
                "ch08-bond-types.svg"), None, "单键 single bond"),
        (5, img("图 8-4　甲烷分子模型｜Methane Model (CH₄)",
                "ch08-methane-model.svg"), None, "路易斯点式"),
        (6, img("图 8-5　命名总流程图｜Complete Naming Flowchart",
                "ch08-naming-flowchart.svg"), None, "拿到一个化学式"),
        (7, img("图 8-6　共价键 vs 分子间作用力｜Bond Strength Clarified",
                "ch08-bond-strength.svg"), None, "INSIDE the molecule"),
        (9, img("例题 B　判断 ionic / molecular｜Judge the Type",
                "ch08-judge-table.svg"), None, "判据：有没有 metal"),
        # 注意：Ch08 共 12 个代码块，末尾主线图是第 12 块
        # （第 11 块是 A8 答案里 4 行的 N≡N 点式，保留原样）
        (12, img("全册主线：两条路 A vs 路 B｜The Two Routes",
                 "ch08-two-routes.svg"), None, "电子排布 electron arrangement"),
    ],
    "Ch07": [
        (1, img("图 7-1　交叉法图解｜Criss-cross Method (Mg + F)",
                "ch07-crisscross-method.svg")),
        (2, img("图 7-2　必须约成最简比｜Reduce to the Lowest Ratio",
                "ch07-reduce-ratio.svg")),
        (3, img("图 7-3　电子转移与路易斯图｜Electron Transfer & Lewis Diagram (MgF₂)",
                "ch07-electron-transfer-mgf2.svg")),
        (4, img("图 7-4　命名流程图｜Naming Decision Flowchart",
                "ch07-naming-flowchart.svg")),
        (5, img("图 7-5　离子晶格与导电性｜Crystal Lattice & Conductivity",
                "ch07-lattice-conductivity.svg")),
        (8, img("图 7-9　括号使用对照｜To Bracket or Not",
                "ch07-brackets.svg")),
        (9, img("全册主线：从原子序数到化合物性质｜The Main Chain",
                "ch07-main-chain.svg")),
    ],
    "Ch06": [
        (2, img("图 6-1　点的放置顺序｜Dot-Placement Order",
                "ch06-dot-placement-order.svg")),
        (3, img("图 6-2　第 1、2 族原子｜Groups 1 & 2 Atoms（金属 metals）",
                "ch06-groups-1-2-atoms.svg")),
        (4, img("图 6-3　H、He 与「二重规则」｜The Duet Rule Exception",
                "ch06-duet-rule.svg")),
        (5, img("图 6-4　第 17、18 族原子｜Groups 17 & 18 Atoms",
                "ch06-groups-17-18-atoms.svg")),
        (6, img("图 6-5　阳离子的点式｜Cations — Always 0 Dots",
                "ch06-cations-dots.svg")),
        (7, img("图 6-6　阴离子的点式｜Anions — Always 8 Dots",
                "ch06-anions-dots.svg")),
        (8, img("图 6-7　写离子符号、电子数与点式｜Worked Example — Writing Ions",
                "ch06-ion-examples.svg")),
        (9, img("图 6-8　诊断并改正错误写法｜Worked Example — Fix the Errors",
                "ch06-fix-the-errors.svg")),
        (10, img("图 6-9　八隅体规则的现场演示｜Na + Cl Electron Transfer",
                 "ch06-electron-transfer.svg")),
    ],
    "Ch05": [
        (1, img("标准核素记号｜Standard Nuclear Notation",
                "ch05-nuclear-notation.svg")),
        (2, img("图 5-1　电子层条形图的通用格式｜The Standard Layout",
                "ch05-bohr-layout.svg")),
        (3, img("图 5-2　H 氢 与 He 氦｜The Period 1 Pair",
                "ch05-bohr-H-He.svg")),
        (4, img("图 5-3　O 氧｜Period 2, Group 16", "ch05-bohr-O.svg")),
        (5, img("图 5-4　Na 钠｜Period 3, Group 1", "ch05-bohr-Na.svg")),
        (6, img("图 5-5　Cl 氯｜Period 3, Group 17", "ch05-bohr-Cl.svg")),
        (7, img("图 5-6　Ar 氩｜Period 3, Group 18 — The Stable One",
                "ch05-bohr-Ar.svg")),
        (8, img("图 5-7　Ca 钙｜Period 4, Group 2", "ch05-bohr-Ca.svg")),
        (9, img("图 5-8　画 Li 与 Al 的玻尔图｜Worked Example — Drawing",
                "ch05-bohr-Li-Al.svg")),
        (10, img("图 5-10　Period 3 全景｜为什么这一行叫「第三周期」",
                 "ch05-period3-panorama.svg")),
    ],
    "Ch04": [
        (1, img("图 4-1　四大族在周期表上的位置｜Where the Families Live",
                "ch04-family-locations.svg")),
        (2, img("图 4-2　两条活性趋势｜Reactivity Trends",
                "ch04-reactivity-trends.svg")),
        (3, img("图 4-3　七种双原子分子｜The Seven Diatomic Molecules",
                "ch04-diatomic-seven.svg")),
        (4, img("图 4-4　为什么稀有气体「什么都不做」｜Why Noble Gases Are Unreactive",
                "ch04-noble-gas-stability.svg")),
        (5, img("图 4-5　预测五步流程｜Prediction Flowchart",
                "ch04-prediction-flowchart.svg"),
         "### 图 4-5　预测五步流程｜Prediction Flowchart"),
    ],
}


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    for key, items in PLAN.items():
        if want and want not in key:
            continue
        md = [f for f in os.listdir(CH_DIR)
              if f.startswith(key + "_") and f.endswith(".md")]
        if not md:
            raise SystemExit(f"找不到 {key} 的 md 文件")
        path = os.path.join(CH_DIR, md[0])
        for item in sorted(items, key=lambda x: -x[0]):
            idx, body = item[0], item[1]
            title = item[2] if len(item) > 2 else None
            expect = item[3] if len(item) > 3 else None
            swap(path, idx, body, title, expect)


if __name__ == "__main__":
    main()
