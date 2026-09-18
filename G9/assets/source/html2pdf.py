# -*- coding: utf-8 -*-
"""HTML → A4 PDF，用 Chrome headless 渲染。

用法：
    html2pdf.py <html文件或目录> [输出目录]

要点（踩过的坑，勿删）：
1. Git Bash 下必须 unset MSYS_NO_PATHCONV / MSYS2_ARG_CONV_EXCL（调用方负责）。
2. Chrome 用系统 ANSI 代码页解析命令行，**非 ASCII 的输出文件名会被静默丢弃**——
   它照样打印 "N bytes written"，但文件根本不存在。所以先输出到 ASCII 临时名，
   再用 Python 的 os.replace 改成目标名（Python 处理 UTF-8 路径没问题）。
3. 必须 ls 确认文件存在，不能信 Chrome 的 stdout。
"""
import os
import subprocess
import sys
import glob

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("未找到 Chrome / Edge")


def to_file_url(path):
    p = os.path.abspath(path).replace("\\", "/")
    return "file:///" + p


def render(chrome, src, dst):
    """渲染单个 HTML → PDF。dst 可以是中文路径，内部用 ASCII 临时名中转。"""
    dst_dir = os.path.dirname(os.path.abspath(dst))
    os.makedirs(dst_dir, exist_ok=True)
    tmp = os.path.join(dst_dir, "_tmp_print.pdf")
    if os.path.exists(tmp):
        os.remove(tmp)
    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=15000",
        "--print-to-pdf=" + tmp.replace("\\", "/"),
        to_file_url(src),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not os.path.exists(tmp):
        raise SystemExit("渲染失败（文件未生成）: %s\n%s" % (src, r.stdout[-400:]))
    os.replace(tmp, dst)
    return os.path.getsize(dst)


def main():
    src = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    chrome = find_chrome()
    print("renderer:", os.path.basename(chrome))

    if os.path.isdir(src):
        files = sorted(glob.glob(os.path.join(src, "*.html")))
    else:
        files = [src]
    if not files:
        raise SystemExit("没有 HTML 文件")

    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]
        dst = os.path.join(out_dir, base + ".pdf") if out_dir \
            else os.path.splitext(f)[0] + ".pdf"
        size = render(chrome, f, dst)
        ok = "OK " if os.path.exists(dst) else "缺失"
        print("%s %-52s %6.0f KB" % (ok, os.path.basename(dst), size / 1024))


if __name__ == "__main__":
    main()
