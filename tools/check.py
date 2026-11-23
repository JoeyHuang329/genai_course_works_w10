#!/usr/bin/env python3
"""LLM Wiki / 簡報 檢查腳本（流程圖中的 L 節點與 C2 節點的自動化部分）。

用法：
    python3 tools/check.py wiki     [--report]
    python3 tools/check.py slides   [--report]
    python3 tools/check.py all      [--report]

--report 會把結果另存成 docs/check-reports/<時間>-<模式>.md，作為執行紀錄。
結束碼：有 ERROR 時為 1，否則為 0（WARN 不影響結束碼，需人工判斷）。
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
SLIDES = ROOT / "slides" / "index.html"
REPORTS = ROOT / "docs" / "check-reports"

REQUIRED_FM = ["title", "type", "sources", "difficulty", "updated"]
VALID_TYPES = {"source", "concept", "model", "synthesis", "overview", "index", "glossary", "log"}
VALID_SOURCES = {f"S{i}" for i in range(1, 6)}
EVIDENCE_TAGS = ["[理論]", "[模擬實驗]", "[硬體實驗]", "[作者分析]", "[作者宣稱]", "[引述]", "[推論]"]
# 誇大用詞：出現就列為 WARN，人工確認後可在該行加上 <!-- reviewed-claim --> 消音
OVERCLAIM = re.compile(r"指數級?(加速|改善|降低|優勢|提升|減少)|打敗|擊敗|全面勝過|超越古典|quantum advantage|量子優勢|exponential(ly)? (speedup|reduc)")
REVIEWED = "<!-- reviewed-claim -->"
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
SRC_TAG = re.compile(r"\[(S\d)\]")
EXPECTED_SLIDES = 20
MAX_DISPLAY_FORMULAS = 6


class Result:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warns: list[str] = []
        self.infos: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)

    def info(self, msg: str) -> None:
        self.infos.append(msg)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    fm: dict = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[end + 4 :]


def parse_list(v: str) -> list[str]:
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip() for x in v[1:-1].split(",") if x.strip()]
    return [v] if v else []


def section(body: str, heading: str) -> list[tuple[int, str]]:
    """回傳某個 ## 區塊內的 (行號, 行內容)。"""
    out, inside = [], False
    for i, line in enumerate(body.splitlines(), 1):
        if line.startswith("## "):
            inside = line[3:].strip() == heading
            continue
        if inside:
            out.append((i, line))
    return out


def check_wiki(r: Result) -> None:
    pages = sorted(WIKI.rglob("*.md"))
    r.info(f"Wiki 頁數：{len(pages)}")
    inbound: dict[Path, int] = {p.resolve(): 0 for p in pages}
    counts: dict[str, int] = {}

    for p in pages:
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        name = rel(p)

        # 1. frontmatter
        for k in REQUIRED_FM:
            if k not in fm:
                r.err(f"{name}: frontmatter 缺少 `{k}`")
        ptype = fm.get("type", "")
        counts[ptype] = counts.get(ptype, 0) + 1
        if ptype and ptype not in VALID_TYPES:
            r.err(f"{name}: type `{ptype}` 不在允許清單")
        fm_sources = set(parse_list(fm.get("sources", "[]")))
        bad = fm_sources - VALID_SOURCES
        if bad:
            r.err(f"{name}: sources 含未知代號 {sorted(bad)}")

        # 2. 連結
        outlinks = 0
        for m in LINK.finditer(body):
            target = m.group(2)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            dest = (p.parent / path).resolve()
            outlinks += 1
            if not dest.exists():
                r.err(f"{name}: 斷鏈 → `{target}`")
            elif dest in inbound and dest != p.resolve():
                inbound[dest] += 1
        if outlinks == 0 and ptype != "log":
            r.warn(f"{name}: 沒有任何連出的內部連結")

        # 3. 證據等級（只檢查 concept / model / source / synthesis）
        if ptype in {"concept", "model", "source", "synthesis"}:
            lines = section(body, "文獻怎麼說")
            if not lines:
                r.err(f"{name}: 缺少「## 文獻怎麼說」區塊")
            for ln, line in lines:
                s = line.strip()
                if not s.startswith("- "):
                    continue
                tags = SRC_TAG.findall(s)
                if not tags:
                    r.err(f"{name}:{ln} 文獻陳述沒有 [Sx] 來源標記")
                n_ev = sum(s.count(t) for t in EVIDENCE_TAGS)
                if n_ev != 1:
                    r.err(f"{name}:{ln} 證據等級標籤應恰好 1 個，實際 {n_ev} 個")
            # 本文用到的 [Sx] 應出現在 frontmatter sources
            used = set(SRC_TAG.findall(body))
            missing = used - fm_sources
            if missing:
                r.err(f"{name}: 本文引用 {sorted(missing)} 但 frontmatter sources 沒列")

        # 4. 誇大用詞（log 是後設紀錄，會引用被檢查的字串本身，故跳過）
        for i, line in enumerate(body.splitlines() if ptype != "log" else [], 1):
            if OVERCLAIM.search(line) and REVIEWED not in line:
                r.warn(f"{name}:{i} 可能誇大的用詞，需人工確認：{line.strip()[:80]}")

    # 5. 孤兒頁
    for p in pages:
        if p.name == "index.md":
            continue
        if inbound[p.resolve()] == 0:
            r.err(f"{rel(p)}: 孤兒頁（沒有任何頁面連到它）")
    r.info("頁面類型統計：" + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


class SlideParser(HTMLParser):
    """抓出 .slides 底下第一層 <section>，以及每張的文字與 data-wiki。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0          # 目前 <section> 巢狀深度
        self.in_slides = False
        self.slides: list[dict] = []
        self.div_stack: list[bool] = []
        self.skip = 0           # <script>/<style> 內文不算

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div":
            is_slides = "slides" in (a.get("class") or "").split()
            self.div_stack.append(is_slides)
            if is_slides:
                self.in_slides = True
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "section" and self.in_slides:
            self.depth += 1
            if self.depth == 1:
                self.slides.append({"wiki": a.get("data-wiki"), "id": a.get("id"), "text": "", "line": self.getpos()[0]})

    def handle_endtag(self, tag):
        if tag == "div" and self.div_stack:
            if self.div_stack.pop():
                self.in_slides = False
        if tag in ("script", "style"):
            self.skip -= 1
        if tag == "section" and self.in_slides:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth >= 1 and not self.skip and self.slides:
            # 以換行分隔各文字片段，避免相鄰儲存格的行內公式 "…$" + "$…" 被誤判成 "$$"
            self.slides[-1]["text"] += data + "\n"


def check_slides(r: Result) -> None:
    if not SLIDES.exists():
        r.err(f"找不到 {rel(SLIDES)}")
        return
    html = SLIDES.read_text(encoding="utf-8")
    sp = SlideParser()
    sp.feed(html)
    n = len(sp.slides)
    r.info(f"投影片張數：{n}（目標 {EXPECTED_SLIDES}）")
    if n != EXPECTED_SLIDES:
        r.err(f"投影片張數 {n} ≠ {EXPECTED_SLIDES}")

    total_formulas = 0
    for idx, s in enumerate(sp.slides, 1):
        label = f"slide {idx}（第 {s['line']} 行）"
        if not s["wiki"]:
            r.err(f"{label}: 缺少 data-wiki")
        else:
            for page in [x.strip() for x in s["wiki"].split(",") if x.strip()]:
                if not (WIKI / page).exists():
                    r.err(f"{label}: data-wiki 指到不存在的頁面 `{page}`")
        text = s["text"]
        f = text.count("$$") // 2
        total_formulas += f
        for line in text.splitlines():
            if OVERCLAIM.search(line):
                r.warn(f"{label}: 可能誇大的用詞，需人工確認：{line.strip()[:80]}")
    r.info(f"展示型公式（$$…$$）總數：{total_formulas}（上限 {MAX_DISPLAY_FORMULAS}）")
    if total_formulas > MAX_DISPLAY_FORMULAS:
        r.err(f"展示型公式 {total_formulas} 個，超過裁決 B2 的上限 {MAX_DISPLAY_FORMULAS}")

    # 來源標籤：每張投影片都要在畫面上顯示來源
    shown = len(re.findall(r'class="src"', html))
    if shown < n:
        r.warn(f"畫面上的來源標籤只有 {shown} 個，少於投影片數 {n}（可能由 JS 產生，需看截圖確認）")


def render(r: Result, mode: str) -> str:
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    out = [f"# 檢查報告：{mode}（{now} UTC+8）", ""]
    out.append(f"- 結果：{'❌ 未通過' if r.errors else '✅ 通過'}；ERROR {len(r.errors)}、WARN {len(r.warns)}")
    out += [f"- {x}" for x in r.infos]
    for title, items in (("ERROR", r.errors), ("WARN", r.warns)):
        out += ["", f"## {title}（{len(items)}）"]
        out += [f"- {x}" for x in items] or ["- （無）"]
    return "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "all"
    r = Result()
    if mode in ("wiki", "all"):
        check_wiki(r)
    if mode in ("slides", "all"):
        check_slides(r)
    if mode not in ("wiki", "slides", "all"):
        print(__doc__)
        return 2
    report = render(r, mode)
    print(report)
    if "--report" in argv:
        REPORTS.mkdir(parents=True, exist_ok=True)
        stamp = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%Y%m%d-%H%M%S")
        (REPORTS / f"{stamp}-{mode}.md").write_text(report, encoding="utf-8")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
