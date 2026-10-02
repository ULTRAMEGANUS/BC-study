# -*- coding: utf-8 -*-
"""G11 讲义数值复核（Ch.01–Ch.14 + 附录）
用法： python check_numbers_g11.py
内容： (1) 文中声明的摩尔质量   (2) 关键计算链   (3) 全章节方程式元素配平自动扫描
       (4) 净离子/离子方程式电荷守恒自动扫描
输出： 逐条 OK/BAD；结尾汇总。任意 BAD → 退出码 1。
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.abspath(os.path.join(HERE, "..", ".."))          # G11/md
CH = os.path.join(MD, "chapters-en")
AP = os.path.join(MD, "appendices-en")

# ---- 原子量（与 Data Booklet 一致的常用取值） ----
MASS = {
    "H": 1.008, "He": 4.003, "Li": 6.94, "Be": 9.012, "B": 10.81, "C": 12.01,
    "N": 14.01, "O": 16.00, "F": 19.00, "Ne": 20.18, "Na": 22.99, "Mg": 24.31,
    "Al": 26.98, "Si": 28.09, "P": 30.97, "S": 32.06, "Cl": 35.45, "Ar": 39.95,
    "K": 39.10, "Ca": 40.08, "Sc": 44.96, "Ti": 47.87, "V": 50.94, "Cr": 52.00,
    "Mn": 54.94, "Fe": 55.85, "Co": 58.93, "Ni": 58.69, "Cu": 63.55, "Zn": 65.38,
    "Ga": 69.72, "Ge": 72.63, "As": 74.92, "Se": 78.97, "Br": 79.90, "Kr": 83.80,
    "Rb": 85.47, "Sr": 87.62, "Y": 88.91, "Zr": 91.22, "Nb": 92.91, "Mo": 95.95,
    "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71, "Sb": 121.76,
    "Te": 127.60, "I": 126.90, "Xe": 131.29, "Cs": 132.91, "Ba": 137.33,
    "W": 183.84, "Pt": 195.08, "Au": 196.97, "Hg": 200.59, "Pb": 207.2,
    "Bi": 208.98, "U": 238.03,
}
ELEMENTS = set(MASS)

# 下标、上标（含 Latin-1 上标 ¹²³ 与 Unicode 上标 ⁰⁴⁻⁹，两种写法都要收）
SUB = {chr(0x2080 + i): str(i) for i in range(10)}
SUP = {chr(0x2070 + i): str(i) for i in range(10)}
SUP.update({"\u00b9": "1", "\u00b2": "2", "\u00b3": "3"})
SUPSIGN = {"\u207a": 1, "\u207b": -1}          # ⁺ ⁻
SUPCH = "".join(SUP)                            # 全部上标数字
ALLOWED = set("0123456789()[]+-·. ") | set(SUB) | set(SUP) | set(SUPSIGN)


def show(s):
    return "".join(SUB.get(c, c) for c in s)


def near(a, b, tol):
    return abs(a - b) <= tol


# ============ 通用：化学式解析 ============
def count_atoms(formula):
    """返回 dict 元素->个数；未知元素抛 KeyError；括号不配平/占位符抛 ValueError。"""
    if not formula or any(ch in formula for ch in "·/≈?ₓᵧ…"):
        raise ValueError(formula)
    f = show(formula)
    f = re.sub("[" + SUPCH + "]*[⁺⁻]", "", f)          # 去电荷（含上标数字前缀）
    f = re.sub(r"[0-9]*[+-](?![A-Za-z0-9])$", "", f)
    i = 0
    depth = [0]

    def grp():
        nonlocal i
        acc = {}
        while i < len(f):
            c = f[i]
            if c == "(":
                depth[0] += 1
                i += 1
                sub = grp()
                n = ""
                while i < len(f) and f[i].isdigit():
                    n += f[i]; i += 1
                k = int(n) if n else 1
                for e, v in sub.items():
                    acc[e] = acc.get(e, 0) + v * k
            elif c == ")":
                if depth[0] == 0:
                    raise ValueError("unmatched ) in " + formula)
                depth[0] -= 1
                i += 1
                return acc
            elif c.isupper():
                el = c; i += 1
                while i < len(f) and f[i].islower():
                    el += f[i]; i += 1
                if el not in ELEMENTS:
                    raise KeyError(el)
                n = ""
                while i < len(f) and f[i].isdigit():
                    n += f[i]; i += 1
                acc[el] = acc.get(el, 0) + (int(n) if n else 1)
            else:
                i += 1
        if depth[0] != 0:
            raise ValueError("unclosed ( in " + formula)
        return acc
    out = grp()
    m = re.match(r"^(\d+(?:\.\d+)?)\s*", formula.strip())
    if m:
        k = float(m.group(1))
        out = {e: v * k for e, v in out.items()}
    return out


def _M(formula):
    """摩尔质量 = Σ 元素个数 × 原子量。"""
    tot = 0.0
    for e, v in count_atoms(formula).items():
        tot += MASS[e] * v
    return tot


# ============ 1. 摩尔质量 ============
MM_CASES = [
    ("H2O", 18.02, "Ch.8 §3"), ("NH3", 17.03, "Ch.8 §3"),
    ("Ca(OH)2", 74.10, "Ch.8 A2"), ("CO2", 44.01, "Ch.8 A3"),
    ("CH4", 16.04, "Ch.10 A10"), ("S8", 256.5, "Ch.8 §4"),
    ("NaCl", 58.44, "Ch.8 §4"), ("CaCO3", 100.09, "Ch.8 A6"),
    ("Fe2O3", 159.69, "Ch.8 C2 / Ch.10 B1"), ("C2H4O", 44.05, "Ch.8 C1"),
    ("C5H7N", 81.1, "Ch.8 B2"), ("NaHCO3", 84.01, "Ch.10 C1"),
    ("Na2CO3", 105.99, "Ch.10 C1"), ("MgO", 40.31, "Ch.10 A3"),
    ("Zn", 65.38, "Ch.10 B3"), ("N2", 28.02, "Ch.10 C2"),
    ("H2", 2.016, "Ch.10 C2"), ("CaCl2", 110.98, "Ch.13 B1"),
    ("CH3COOH", 60.05, "Ch.13 C1"), ("PbI2", 461.0, "Ch.12 §5"),
    ("BaSO4", 233.39, "Ch.13 §4"),
]


def sec1():
    print("=== 1. 摩尔质量 ===")
    bad = 0
    for f, stated, where in MM_CASES:
        try:
            calc = _M(f)
        except (KeyError, ValueError) as e:
            print(f"  ??   {f:12s} 解析失败 {e}（{where}）"); bad += 1; continue
        tol = 0.05 + 0.002 * stated
        if near(calc, stated, tol):
            print(f"  OK   {f:12s} {calc:7.2f} vs {stated:7.2f}  ({where})")
        else:
            print(f"  BAD  {f:12s} {calc:7.2f} vs {stated:7.2f}  ({where})"); bad += 1
    return bad


# ============ 2. 计算链 ============
CHAIN = [
    ("Ch.8 NH3 %N", 14.01 / 17.034 * 100, 82.3, 0.15),
    ("Ch.8 Ex chain n", 42.0 / 14.026, 3.0, 0.02),
    ("Ch.8 A2 Ca(OH)2", 40.08 + 2 * (16.00 + 1.008), 74.10, 0.02),
    ("Ch.8 A3 0.250*44.01", 0.250 * 44.01, 11.0, 0.05),
    ("Ch.8 A4 4.00/16.04", 4.00 / 16.04, 0.2494, 0.0002),
    ("Ch.8 A4 mol*NA", 4.00 / 16.04 * 6.02e23, 1.50e23, 0.02e23),
    ("Ch.8 A6 %Ca", 40.08 / 100.09 * 100, 40.0, 0.1),
    ("Ch.8 A6 %C", 12.01 / 100.09 * 100, 12.0, 0.1),
    ("Ch.8 A6 %O", 48.00 / 100.09 * 100, 48.0, 0.1),
    ("Ch.8 B2 C ratio", 74.0 / 12.01 / (17.3 / 14.01), 4.99, 0.02),
    ("Ch.8 B2 H ratio", 8.7 / 1.008 / (17.3 / 14.01), 6.99, 0.02),
    ("Ch.8 B2 n", 162 / 81.1, 2.0, 0.01),
    ("Ch.8 C1 C mass", 1.999 * 12.01 / 44.01, 0.5456, 0.001),
    ("Ch.8 C1 H mass", 0.818 * 2.016 / 18.02, 0.09154, 0.001),
    ("Ch.8 C1 O mass", 1.000 - 1.999 * 12.01 / 44.01 - 0.818 * 2.016 / 18.02, 0.3629, 0.001),
    ("Ch.8 C1 n", 88.0 / 44.05, 2.0, 0.01),
    ("Ch.8 C2 pure Fe2O3", 6.20 * 0.820, 5.084, 0.002),
    ("Ch.8 C2 mol", 6.20 * 0.820 / 159.69, 0.0318, 0.0002),
    ("Ch.8 C2 Fe mass", 5.084 * (2 * 55.85) / 159.69, 3.56, 0.01),
    ("Ch.10 §5 mol Mg", 6.0 / 24.3, 0.247, 0.001),
    ("Ch.10 §5 mass H2", 6.0 / 24.3 * 2.016, 0.50, 0.01),
    ("Ch.10 Ex10-3 pure Zn", 5.00 * 0.860, 4.30, 0.01),
    ("Ch.10 Ex10-3 theor H2", 5.00 * 0.860 / 65.38 * 2.016, 0.1326, 0.0002),
    ("Ch.10 Ex10-3 yield%", 0.112 / (5.00 * 0.860 / 65.38 * 2.016) * 100, 84.5, 0.15),
    ("Ch.10 A3 MgO", 4.86 / 24.3 * 40.31, 8.06, 0.02),
    ("Ch.10 A10 CO2", 16.0 / 16.04 * 44.01, 43.9, 0.15),
    ("Ch.10 A7 yield%", 9.6 / 12.0 * 100, 80.0, 0.1),
    ("Ch.10 B1 mol Fe2O3", 100.0 / 159.7, 0.6262, 0.0002),
    ("Ch.10 B1 Fe mass", 100.0 / 159.7 * 2 * 55.85, 69.9, 0.1),
    ("Ch.10 B3 pure Zn", 5.00 * 0.900, 4.50, 0.01),
    ("Ch.10 B3 theor H2", 5.00 * 0.900 / 65.38 * 2.016, 0.1388, 0.0002),
    ("Ch.10 B3 yield%", 0.135 / (5.00 * 0.900 / 65.38 * 2.016) * 100, 97.3, 0.15),
    ("Ch.10 C1 mol NaHCO3", 8.40 / 84.01, 0.1000, 0.0002),
    ("Ch.10 C1 theor Na2CO3", 8.40 / 84.01 / 2 * 105.99, 5.30, 0.02),
    ("Ch.10 C1 yield%", 4.90 / (8.40 / 84.01 / 2 * 105.99) * 100, 92.5, 0.15),
    ("Ch.10 C2 N2 kmol", 280 / 28.02, 9.99, 0.02),
    ("Ch.10 C2 N2->NH3", 280 / 28.02 * 2, 19.99, 0.02),
    ("Ch.10 C2 H2 kmol", 72 / 2.016, 35.7, 0.1),
    ("Ch.10 C2 H2->NH3", 72 / 2.016 * 2 / 3, 23.8, 0.1),
    ("Ch.10 C2 theor kg", 280 / 28.02 * 2 * 17.03, 340, 1.0),
    ("Ch.10 C2 yield%", 300 / (280 / 28.02 * 2 * 17.03) * 100, 88.2, 0.2),
    ("Ch.13 §2 M", 0.100 / 0.250, 0.400, 0.001),
    ("Ch.13 §2 V1", 0.25 * 400 / 1.0, 100, 0.5),
    ("Ch.13 A3 mass", 0.2500 * 0.100 * 58.44, 1.46, 0.01),
    ("Ch.13 B1 mol CaCO3", 1.50 / 100.1, 0.01499, 0.00002),
    ("Ch.13 B1 V", 1.50 / 100.1 * 2 / 0.250, 0.1199, 0.0002),
    ("Ch.13 B1 ppt mol", 0.100 * 0.0200, 0.00200, 1e-5),
    ("Ch.13 B1 ppt g", 0.100 * 0.0200 * 100.09, 0.200, 0.002),
    ("Ch.13 B3 avg", (23.10 + 22.90) / 2, 23.00, 0.01),
    ("Ch.13 B3 M", 0.002300 / 0.02500, 0.0920, 0.0002),
    ("Ch.13 C1 mol NaOH", 0.5000 * 0.03420, 0.01710, 0.00002),
    ("Ch.13 C1 M", 0.5000 * 0.03420 / 0.01000, 1.71, 0.01),
    ("Ch.13 C1 vinegar M", 50.0 / 60.05, 0.833, 0.002),
    ("Ch.14 A6 sum", 1.20 + 0.201 + 1.60, 3.00, 0.01),
    ("Ch.14 A6 C", 1.20 / 12.01, 0.09992, 0.0002),
    ("Ch.14 A6 H", 0.201 / 1.008, 0.19940, 0.0005),
    ("Ch.14 A6 O", 1.60 / 16.00, 0.10000, 0.00002),
]


def sec2():
    print("\n=== 2. 关键计算链 ===")
    bad = 0
    for desc, calc, stated, tol in CHAIN:
        if near(calc, stated, tol):
            print(f"  OK   {desc:24s} {calc:12.5f} vs {stated}")
        else:
            print(f"  BAD  {desc:24s} {calc:12.5f} vs {stated}"); bad += 1
    return bad


# ============ 3/4. 方程式扫描 ============
def expand(s, pos, step):
    """自 pos 起步按 step 方向扩展，遇非化学字符或跳出括号即止。返回 [lo,hi)。"""
    i = pos
    depth = 0
    while 0 <= i < len(s):
        c = s[i]
        if c in "()":
            if step < 0:                    # 向左：) 进组，( 出组
                if c == ")":
                    depth += 1
                else:
                    if depth == 0:
                        break
                    depth -= 1
            else:                           # 向右：( 进组，) 出组
                if c == "(":
                    depth += 1
                else:
                    if depth == 0:
                        break
                    depth -= 1
            i += step
        elif c.isupper() or c in ALLOWED:
            i += step
        elif c.islower():
            if 0 <= i - 1 < len(s) and s[i - 1].isupper():
                i += step
            else:
                break
        else:
            break
    return (i + 1, pos + 1) if step < 0 else (pos, i)


def trim_rhs(t):
    return re.split(r"\s{2,}|;\s|\.\s|=\s|\(\w\)\s|（|，|：|、|←|✔|✘|\|", t)[0]


def trim_edges(s):
    s = s.strip()
    s = re.sub(r"^[)\]]+\s*", "", s)
    s = re.sub(r"\s*[([]+$", "", s)
    return s.strip(" .·")


def coef_charge(t):
    m = re.match(r"^(\d+(?:\.\d+)?)", t.strip())
    return (float(m.group(1)) if m else 1) * charge_of(t)


def charge_of(formula):
    """物种净电荷：支持 ⁺/⁻ + 上标数字，以及 ASCII 的 + / - 结尾。"""
    q = 0
    for m in re.finditer("([" + SUPCH + "]*)([⁺⁻])", formula):
        digits = "".join(SUP.get(c, "") for c in m.group(1))
        q += (int(digits) if digits else 1) * SUPSIGN[m.group(2)]
    for m in re.finditer(r"(\d*)([+-])\s*$", formula.strip()):
        q += (int(m.group(1)) if m.group(1) else 1) * (1 if m.group(2) == "+" else -1)
    return q


BARE = re.compile(r"^\d*\.?\d*\s*[A-Z][a-z]?\d*$")
RATIO = re.compile(r"^[A-Z][a-z]?\s+[\d.]+$")
MARKER = re.compile(r"^[A-Za-z]{1,3}\d*\.\s+")
COEF = re.compile(r"^\d+(?:\.\d+)?")
# 裸的多原子原子团碎片（平衡推理过程里会出现「need 3 SO₄ → 3 H₂SO₄」这类）
FRAG = {"SO4", "OH", "NO3", "CO3", "PO4", "NH4", "CH3COO", "HSO4", "C2H3O2"}
QUOTED = '"\u201c\u201d\u2018\u2019'


def scan_files():
    print("\n=== 3/4. 方程式配平 + 电荷守恒自动扫描 ===")
    files = []
    for d in (CH, AP):
        if os.path.isdir(d):
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".md"):
                    files.append(os.path.join(d, fn))
    eq_ok = eq_bad = ch_ok = ch_bad = 0
    bad_lines, ok_lines = [], []
    seen = set()

    for path in files:
        with io.open(path, encoding="utf-8") as fh:
            for ln, line in enumerate(fh, 1):
                if "→" not in line or "Extension" in line:
                    continue
                if re.search(r"[Bb]alanc", line) or "配平" in line:
                    continue                                   # 刻意不配平的题干
                if re.search(r"写出|写净离子|预测|指出|判断", line):
                    continue                                   # 中文题干（要求产出方程式）
                s = line.strip()
                if re.match(r"^`[^`]*`\s*$", s):
                    continue                                   # 整行反引号包着的示例式
                raw = line.replace("↓", "").replace("↑", "")
                raw = re.sub(r"→[（(][^)）]*[)）]", "→", raw)   # 箭头上的条件注解
                for cell in raw.split("|"):
                    if "…" in cell or any(q in cell for q in QUOTED):
                        continue
                    for seg in cell.split(";"):
                        seg = re.sub(r"[（(](s|l|g|aq)[)）]", "", seg.replace("*", ""))
                        if "→" not in seg:
                            continue
                        idx = 0
                        while True:
                            a = seg.find("→", idx)
                            if a < 0:
                                break
                            idx = a + 1
                            lo, _ = expand(seg, a - 1, -1)
                            _, hi = expand(seg, a + 1, +1)
                            lhs = MARKER.sub("", trim_edges(seg[lo:a])).strip()
                            rhs = trim_edges(trim_rhs(seg[a + 1:hi]))
                            if not lhs or not rhs or lhs.startswith("+") or rhs.startswith("+"):
                                continue
                            lt = [t for t in (x.strip() for x in lhs.split("+")) if t]
                            rt = [t for t in (x.strip() for x in rhs.split("+")) if t]
                            if not lt or not rt:
                                continue
                            if any(RATIO.match(t) for t in lt + rt):
                                continue
                            if len(lt) == 1 and len(rt) == 1 and not any(COEF.match(t) for t in lt + rt):
                                continue            # 1→1 无系数＝文字箭头（"导致/转为"），非方程式
                            if len(lt) == 1 and BARE.match(lt[0]):
                                continue
                            if any(show(COEF.sub("", t).strip()).upper() in FRAG for t in lt + rt):
                                continue
                            key = (lhs, rhs)
                            if key in seen:
                                continue
                            try:
                                L, R = {}, {}
                                for t in lt:
                                    if not (t[0].isupper() or t[0] == "(" or t[0].isdigit()):
                                        raise ValueError(t)
                                    for e, v in count_atoms(t).items():
                                        L[e] = L.get(e, 0) + v
                                for t in rt:
                                    if not (t[0].isupper() or t[0] == "(" or t[0].isdigit()):
                                        raise ValueError(t)
                                    for e, v in count_atoms(t).items():
                                        R[e] = R.get(e, 0) + v
                            except (KeyError, ValueError, IndexError):
                                continue
                            seen.add(key)
                            if not L or not R:
                                continue                      # 纯数字/比例箭头，非方程式
                            ql = sum(coef_charge(t) for t in lt)
                            qr = sum(coef_charge(t) for t in rt)
                            charged = any(charge_of(t) for t in lt + rt)
                            if L == R:
                                eq_ok += 1
                                ok_lines.append(f"  OK  {lhs} → {rhs}")
                            else:
                                eq_bad += 1
                                bad_lines.append(
                                    f"  BAD[配平] {os.path.basename(path)}:{ln}  {lhs} → {rhs}\n"
                                    f"            L={dict(sorted(L.items()))}  R={dict(sorted(R.items()))}")
                            if charged:
                                if ql == qr:
                                    ch_ok += 1
                                else:
                                    ch_bad += 1
                                    bad_lines.append(
                                        f"  BAD[电荷] {os.path.basename(path)}:{ln}  {lhs} → {rhs}  qL={ql} qR={qr}")
    for b in bad_lines:
        print(b)
    for o in ok_lines:
        print(o)
    print(f"  配平：OK {eq_ok} · BAD {eq_bad}（去重后）")
    print(f"  电荷：OK {ch_ok} · BAD {ch_bad}")
    return eq_bad + ch_bad


if __name__ == "__main__":
    b1 = sec1()
    b2 = sec2()
    b3 = scan_files()
    total = b1 + b2 + b3
    print("\n================ 汇总 ================")
    print("  摩尔质量 BAD :", b1)
    print("  计算链   BAD :", b2)
    print("  方程式   BAD :", b3)
    print("  合计     BAD :", total, "→", "全部通过 ✅" if total == 0 else "需修 ❌")
    sys.exit(0 if total == 0 else 1)
