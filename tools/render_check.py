#!/usr/bin/env python3
"""C2 渲染檢查：用 headless Chrome 逐張開啟簡報、截圖，並量測內容是否超出投影片範圍。

用法：
    python3 tools/render_check.py [--local-npm DIR] [--out DIR]

--local-npm：若執行環境連不到 CDN，把 cdn.jsdelivr.net/npm/<套件>@<版本>/<路徑>
             的請求改由 DIR/node_modules/<套件>/<路徑> 回應（需先 npm i reveal.js@5.1.0 katex@0.16.11）。
--out：截圖輸出資料夾（預設 docs/render-check/）。

檢查項目：
1. 投影片數量
2. KaTeX 是否正確渲染（無 .katex-error；展示型公式數量）
3. 每張投影片內是否有元素超出 1280×720 範圍（overflow）
4. 瀏覽器 console 錯誤
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SLIDES = ROOT / "slides" / "index.html"
CDN = re.compile(r"https://cdn\.jsdelivr\.net/npm/(?P<pkg>[^@/]+)@[^/]+/(?P<path>.+)")
MIME = {".css": "text/css", ".js": "application/javascript", ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf"}

OVERFLOW_JS = """
() => {
  const box = document.querySelector('.reveal .slides').getBoundingClientRect();
  const cur = Reveal.getCurrentSlide();
  const bad = [];
  cur.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (el.closest('.katex-mathml')) return;  // KaTeX 的隱藏無障礙層，不會顯示
    if (el.closest('details:not([open])') && el.tagName !== 'SUMMARY' && el.tagName !== 'DETAILS') return;
    const over = Math.max(r.bottom - box.bottom, r.right - box.right, box.left - r.left, box.top - r.top);
    if (over > 2) bad.push({tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? el.className : '', over: Math.round(over / Reveal.getScale())});
  });
  bad.sort((a, b) => b.over - a.over);
  return bad.slice(0, 3);
}
"""


def main(argv: list[str]) -> int:
    local = None
    out = ROOT / "docs" / "render-check"
    if "--local-npm" in argv:
        local = Path(argv[argv.index("--local-npm") + 1]) / "node_modules"
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    out.mkdir(parents=True, exist_ok=True)

    problems: list[str] = []
    console_errors: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

        if local:
            def handle(route):
                m = CDN.match(route.request.url)
                f = local / m.group("pkg") / m.group("path") if m else None
                if f and f.exists():
                    route.fulfill(path=str(f), headers={"Content-Type": MIME.get(f.suffix, "application/octet-stream"), "Access-Control-Allow-Origin": "*"})
                else:
                    route.abort()
            page.route("https://cdn.jsdelivr.net/**", handle)
            page.route("https://fonts.googleapis.com/**", lambda r: r.abort())

        page.goto(SLIDES.as_uri())
        page.wait_for_function("window.Reveal && Reveal.isReady()")
        page.wait_for_function("document.querySelectorAll('.katex').length > 0", timeout=15000)
        # 關閉換頁動畫，否則截圖與量測會落在轉場途中
        page.evaluate("Reveal.configure({ transition: 'none', backgroundTransition: 'none' })")
        page.wait_for_timeout(800)

        n = page.evaluate("Reveal.getTotalSlides()")
        katex_err = page.evaluate("document.querySelectorAll('.katex-error').length")
        displays = page.evaluate("document.querySelectorAll('.katex-display').length")
        print(f"投影片：{n} 張；KaTeX 展示型公式：{displays} 個；KaTeX 錯誤：{katex_err} 個")
        if katex_err:
            problems.append(f"KaTeX 錯誤 {katex_err} 個")

        for i in range(n):
            page.evaluate(f"Reveal.slide({i})")
            page.wait_for_timeout(250)
            bad = page.evaluate(OVERFLOW_JS)
            sid = page.evaluate("Reveal.getCurrentSlide().id")
            page.screenshot(path=str(out / f"slide-{i + 1:02d}.png"))
            status = "OK" if not bad else f"超出範圍 {bad[0]['over']}px（{bad[0]['tag']} {bad[0]['cls']}）"
            print(f"slide {i + 1:02d} [{sid}]: {status}")
            if bad:
                problems.append(f"slide {i + 1}: {status}")
        browser.close()

    real_console = [e for e in console_errors if "net::ERR_FAILED" not in e and "Failed to load resource" not in e]
    if real_console:
        problems.append(f"console 錯誤 {len(real_console)} 個：{real_console[:3]}")
    print("\n結果：" + ("✅ 通過" if not problems else "❌ 未通過"))
    for x in problems:
        print(" -", x)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
