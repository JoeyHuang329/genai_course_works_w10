#!/usr/bin/env python3
"""產生「投影片 ↔ Wiki 頁 ↔ 文獻」對照表，並檢查投影片上的數字是否都能在對應 Wiki 頁找到。

用法：python3 tools/traceability.py [--write]
    --write：輸出到 docs/traceability.md

數字是最容易出錯、也最容易自動比對的主張，所以這裡只自動檢查數字；
文字主張仍需人工（C1）比對。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402

ROOT = check.ROOT
REPO = "https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/wiki/"
# 抓「有意義的數字」：小數、含千分位、或 ≥2 位數的整數；排除 1 位數整數（太常見，如「第 1 層」）
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+\.\d+|\d{2,})(?![\w])")
IGNORE = {"2026", "2019", "2022", "2023", "2024", "101"}  # 年份另由書目處理；101 來自標題「Qubit 101」
SRC_TAG = re.compile(r"\[(S\d)\]")


def numbers(text: str) -> set[str]:
    # 去掉 LaTeX 指令與上下標中的數字干擾（如 10^{-2}、\frac{1}{2}）
    t = re.sub(r"\$[^$]*\$", " ", text)
    return {n for n in NUM.findall(t) if n not in IGNORE}


def main(argv: list[str]) -> int:
    sp = check.SlideParser()
    html = check.SLIDES.read_text(encoding="utf-8")
    sp.feed(html)
    titles = re.findall(r"<section[^>]*>\s*(?:<p[^>]*>.*?</p>\s*)?<h[12][^>]*>(.*?)</h[12]>", html, flags=re.S)
    titles = [re.sub(r"<[^>]+>", "", t).strip() for t in titles]

    rows, missing_total = [], 0
    for i, s in enumerate(sp.slides, 1):
        pages = [p.strip() for p in (s["wiki"] or "").split(",") if p.strip()]
        wiki_text = ""
        srcs: set[str] = set()
        for p in pages:
            f = check.WIKI / p
            if f.exists():
                t = f.read_text(encoding="utf-8")
                wiki_text += t
                fm, _ = check.parse_frontmatter(t)
                srcs |= set(check.parse_list(fm.get("sources", "[]")))
        nums = numbers(s["text"])
        # Wiki 中的數字可能寫成 5,000 或 5000；比對時兩種都試
        miss = sorted(n for n in nums if n not in wiki_text and n.replace(",", "") not in wiki_text)
        missing_total += len(miss)
        rows.append((i, titles[i - 1] if i - 1 < len(titles) else "", pages, sorted(srcs), sorted(nums), miss))

    out = ["# 投影片 ↔ Wiki ↔ 文獻 對照表（traceability）", "",
           "由 `tools/traceability.py` 自動產生。每張投影片的 `data-wiki` 屬性列出它依據的 Wiki 頁；",
           "「文獻」欄是這些 Wiki 頁 frontmatter 中的 `sources`。「數字檢查」欄列出投影片上出現的數字，",
           "以及在對應 Wiki 頁中**找不到**的數字（應為空）。", "",
           "| # | 投影片標題 | 依據的 Wiki 頁 | 文獻 | 投影片上的數字 | 找不到的數字 |",
           "|---|---|---|---|---|---|"]
    for i, title, pages, srcs, nums, miss in rows:
        links = "<br>".join(f"[{p.removesuffix('.md')}]({REPO}{p})" for p in pages)
        out.append(f"| {i} | {title.replace('|', '／')} | {links} | {' '.join(srcs) or '—'} | {', '.join(nums) or '—'} | {('**' + ', '.join(miss) + '**') if miss else '✅'} |")
    out += ["", f"找不到對應的數字共 **{missing_total}** 個。"]
    report = "\n".join(out) + "\n"
    if "--write" in argv:
        (ROOT / "docs" / "traceability.md").write_text(report, encoding="utf-8")
    print(report)
    return 1 if missing_total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
