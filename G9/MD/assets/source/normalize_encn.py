# -*- coding: utf-8 -*-
"""把 G9/MD/chapters-en/ 下 11 章英文版的编号前缀与标题语言顺序统一为「英文在前、中文在后」。

用法（在 assets/source 下）：
    env -u MSYS_NO_PATHCONV -u MSYS2_ARG_CONV_EXCL "$PY" normalize_encn.py [--dry]

规则
1. 编号前缀统一成英文：图 X-Y → Fig. X-Y、表 X-Y → Table X-Y、活动 X-Y → Activity X-Y
   （只改围栏代码块之外的行，避免破坏 ASCII 图对齐）
2. 测评分组标题统一成 `Group A: …｜A 组：…`（吸收 `A 组：` / `Part A:` 两种写法）
3. 标题里「中文｜English」的顺序倒置（去掉编号前缀后比较中文字数）
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENCN = os.path.join(os.path.dirname(os.path.dirname(HERE)), "chapters-en")

CJK = r'[\u4e00-\u9fff（）「」《》、，。：；！？]'


def _make_repl(word):
    """替换成英文编号，并按需要补中英之间的空格。

    「把表 5-5 的 20 行」若直接替换会变成「把Table 5-5 的 20 行」，
    中英贴在一起；故当左右邻居是中文/中文标点时补一个半角空格。
    """

    def f(m):
        s = m.string
        before = s[m.start() - 1] if m.start() > 0 else ''
        after = s[m.end()] if m.end() < len(s) else ''
        pre = ' ' if before and re.match(CJK, before) else ''
        suf = ' ' if after and re.match(CJK, after) else ''
        return '%s%s %s%s' % (pre, word, m.group(1), suf)

    return f


# 编号前缀：图/表/活动 → 英文
NUM_PREFIX = [
    (re.compile(r'(?<!Fig\.)(?<!Fig\.\s)图\s*(\d+[-–]\d+)'), _make_repl('Fig.')),
    (re.compile(r'(?<!Table\s)表\s*(\d+[-–]\d+)'), _make_repl('Table')),
    (re.compile(r'(?<!Activity\s)活动\s*(\d+[-–]\d+)'), _make_repl('Activity')),
]

# 分组标题：`### A 组：X｜Y` / `### Part A: X｜Y` → `### Group A: X｜A 组：Y`
GROUP_CN = re.compile(r'^(#{2,4}\s*)A\s*组[：:]\s*(.*)$')
GROUP_PART = re.compile(r'^(#{2,4}\s*)Part\s+([ABC])\s*:\s*(.*)$')
# 已经是 `Group A: X｜A 组：Y` 的不动
GROUP_OK = re.compile(r'^#{2,4}\s*Group\s+[ABC]\s*:')

# 标题里去掉编号前缀后，用于判断「哪边是中文」
PREFIX = re.compile(
    r'^(?:Table|Fig\.|Figure|Activity|Example|Worked\s+Example)?\s*\d+[-–]\d+[　\s]*')


def cn_count(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))


def fix_heading(line):
    """只处理以 # 开头的标题行；返回修正后的行"""
    m = GROUP_CN.match(line)
    if m and '｜' in line:
        en, zh = line.split('｜', 1)
        en = GROUP_CN.sub(lambda x: 'Group A: ' + x.group(2), en)
        if not zh.lstrip().startswith('A 组'):
            zh = 'A 组：' + zh.lstrip('：: ')
        return en + '｜' + zh
    m = GROUP_PART.match(line)
    if m and '｜' in line:
        g = m.group(2)
        en, zh = line.split('｜', 1)
        en = GROUP_PART.sub(lambda x: 'Group %s: ' % g + x.group(3), en)
        if not zh.lstrip().startswith(g + ' 组'):
            zh = '%s 组：%s' % (g, zh.lstrip('：: '))
        return en + '｜' + zh

    if not line.lstrip().startswith('#') or '｜' not in line:
        return line
    head, body = line.split('｜', 1)
    a = PREFIX.sub('', head.lstrip('# ').strip())
    b = body.strip()
    ca, cb = cn_count(a), cn_count(b)
    # 只有「英文侧的中文明显多于中文侧」才判定为顺序倒置。
    # 不能只看中文侧字数少：像 `Oxygen｜氧　Period 2, Group 16` 中文侧只有 1 个字，
    # 但它本来就是英文在前，误判会把它翻成 `氧…｜Oxygen`。
    if ca >= 2 and ca > cb:
        # 互换时保留编号前缀
        m2 = re.match(r'^(#+\s*)(.*?)(\s*(?:Table|Fig\.|Figure|Activity|Example)?\s*\d+[-–]\d+[　\s]*)(.*)$',
                      head)
        if m2:
            num = m2.group(3)
            rest = m2.group(4)
        else:
            num, rest = '', a
        new_head = '%s%s%s' % (re.match(r'^#+\s*', head).group(0), num, b)
        return new_head + '｜' + rest
    return line


def process(path):
    lines = io.open(path, encoding='utf-8').read().split('\n')
    out = []
    in_code = False
    n_num = n_grp = n_swap = 0
    for ln in lines:
        if ln.lstrip().startswith('```'):
            in_code = not in_code
            out.append(ln)
            continue
        if in_code:
            out.append(ln)
            continue
        orig = ln
        for pat, rep in NUM_PREFIX:
            new = pat.sub(rep, ln)
            if new != ln:
                n_num += 1
                ln = new
        after = fix_heading(ln)
        if after != ln:
            if GROUP_CN.match(orig) or GROUP_PART.match(orig):
                n_grp += 1
            else:
                n_swap += 1
            ln = after
        out.append(ln)
    return '\n'.join(out), n_num, n_grp, n_swap


def main():
    dry = '--dry' in sys.argv
    files = sorted(f for f in os.listdir(ENCN) if f.startswith('Ch') and f.endswith('.md'))
    tot = [0, 0, 0]
    for name in files:
        p = os.path.join(ENCN, name)
        text, a, b, c = process(p)
        tot[0] += a
        tot[1] += b
        tot[2] += c
        print('  %-14s 编号%2d  分组%2d  顺序%2d' % (name[:12], a, b, c))
        if not dry and (a or b or c):
            io.open(p, 'w', encoding='utf-8').write(text)
    print('合计：编号前缀 %d 处，分组标题 %d 处，语言顺序 %d 处%s'
          % (tot[0], tot[1], tot[2], '（dry run，未写入）' if dry else ''))


if __name__ == '__main__':
    main()
