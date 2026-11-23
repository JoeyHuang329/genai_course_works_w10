# 繳交區文字草稿

> 這份是給課程作者貼到作業繳交區用的草稿，依作業要求的 6 項排列。標題（學校、學號、系級、姓名）與 AI 使用聲明由作者本人填寫（裁決 A1、A3），這裡只提供聲明的事實清單供參考。
> 連結假設 repo 已推到 `JoeyHuang329/genai_course_works_w10` 的 `main` 分支，並已開啟 GitHub Pages（設定方式見 [README](../README.md#部署)）。

---

## 1. LLM Wiki 主題與簡短介紹

**主題：圖神經網路 × 量子電路**

這個 Wiki 整理 5 篇與「量子計算」、「圖神經網路（GNN）」、「量子電路」相關的研究（2019–2026），共 27 頁，中文為主、術語附英文。內容涵蓋兩個方向：

- **用量子電路處理圖**（量子圖神經網路）：讓圖決定量子交互作用（Verdon 2019）、用 Givens 旋轉模擬鄰接矩陣（Hu 2022）、用對稱的雙 qubit 閘預測分子性質（Ryu 2023），以及一篇 2026 年的批判性回顧（Ceschini 2026）。
- **用 GNN 分析量子電路**：把電路當成圖，預測電路的表達能力（Aktar 2024）。

Wiki 依 Karpathy 的 LLM Wiki 模式分三層（raw／wiki／schema），由 `CLAUDE.md` 規範格式與流程。每條文獻陳述都標註來源與證據等級（理論、模擬實驗、硬體實驗、作者分析、作者宣稱、引述、推論），用詞依回顧論文區分 quantum advantage、quantum utility、quantum-inspired。

## 2. LLM Wiki 連結

- Wiki 首頁（索引）：https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/wiki/index.md
- 建議從總覽開始讀：https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/wiki/overview.md
- Schema：https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/CLAUDE.md
- 維護紀錄：https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/wiki/log.md

## 3. 教學 HTML 簡報連結

https://joeyhuang329.github.io/genai_course_works_w10/slides/

20 張，reveal.js。對象是會寫程式、但沒碰過 GNN 或量子計算的大學生。結構為：學習目標 → 地圖 → 兩個先備知識（GNN、qubit）→ 核心問題（編碼）→ 三種把圖放進電路的方法 → 反方向（電路是一張圖）→ 分類與評價 → 挑戰與三個重點 → 5 題互動測驗。

6 個關鍵公式都附符號表（意義、用途）。每張投影片左下角都有來源標籤，可點回對應的 Wiki 頁；完整對照表見 [traceability.md](traceability.md)。

## 4. Loop／Graph 設計

（流程圖與三個問題的完整回答：https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/docs/workflow.md）

**流程**：取得 PDF → 抽取檢查 → 討論底稿 → 人類確認 → 生成 Wiki 頁 → 自查 → Lint → 查詢 Wiki 規劃大綱 → 逐張產生投影片 → 數字可追溯檢查 → 內容檢查 → 組裝 HTML → 渲染檢查 → 紀錄

- **重複執行的步驟**：ingest 迴圈（每篇一次，共 5 次）、lint 修正迴圈、投影片重生迴圈（每張上限 2 次）、Wiki 缺口迴圈（簡報需要但 Wiki 沒有的知識，先補 Wiki 再改投影片）、渲染迴圈。
- **需要檢查或重新生成的地方**：PDF 抽取（公式、表格）、Wiki 格式與證據標記（`tools/check.py`）、投影片數字出處（`tools/traceability.py`）、內容與可讀性（人工）、渲染（`tools/render_check.py` 截圖＋人工看）。
- **為什麼這樣設計**：簡報階段只能讀 Wiki，讓每句話都能回答「出處是哪頁」；證據等級一開始就放，讓「該查證什麼」明確；Wiki 缺口回寫 Wiki，讓知識累積而不是只存在投影片裡；自動檢查負責「有沒有」，人工檢查負責「對不對」。

## 5. 一次實際執行的結果與檢查紀錄

（完整紀錄：https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/docs/run-log.md）

- 執行時間：2026-11-23 22:33–23:00，ingest 5 篇、產生 27 頁 Wiki 與 20 張簡報。
- 共記錄 37 筆問題，例如：
  - 討論底稿把 S2 歸為 Hybrid，ingest S5 時依原文改為 Fully Quantum。
  - 「含雜訊的後端」其實是模擬雜訊。
  - 第 13、20 張投影片出處漏列。
  - 「譜聚類」「圖同構」在 Wiki 沒有定義，觸發一次 Wiki 缺口迴圈。
  - 6 個版面問題。
  - 檢查工具本身的 7 個 bug 或誤報。
- 最終結果：lint ERROR 0、渲染 20 張無超出、找不到出處的數字 0。
- 每次 lint 的輸出存在 `docs/check-reports/`，最終截圖存在 `docs/render-check/`。

## 6. 反思

（完整版：https://github.com/JoeyHuang329/genai_course_works_w10/blob/main/docs/reflection.md）

- **最常出錯的節點**：「產生投影片」（9 筆，其中 6 筆是版面），其次是「生成 Wiki 頁」（7 筆）。版面錯誤多但便宜；內容錯誤少但代價高。例如術語沒定義的源頭在 Wiki 生成，卻到簡報階段才被發現，要繞一整圈補回 Wiki。
- **檢查往前移到哪裡**：
  - 數字出處檢查從「整份簡報完成後」移到「每張草稿完成後」（新寫 `traceability.py`，第一次執行就抓到第 20 張書目違反「只讀 Wiki」）。
  - 術語定義、單一證據、不錯連三項檢查移到「生成 Wiki 頁」的自查清單。
- **有沒有改 workflow**：有，`CLAUDE.md` 從 v1 改為 v2。
  - A3 後加自查節點、B2 後加數字檢查節點。
  - 渲染檢查明定要人工看截圖。
  - log 時間改由系統時鐘產生（因為有三筆是憑感覺手填）。
- **誠實的偏差**：
  - 「先討論、後生成」實際上是 5 篇批次確認，不是逐篇。
  - Verdon ansatz 與 QSGCNN 兩張對入門聽眾仍偏難。

---

## 附：AI 使用分工的事實清單（供作者撰寫聲明參考）

| 工作 | 誰做的 |
|---|---|
| 選主題、選 5 篇文獻、提供 PDF | 課程作者 |
| 讀 PDF、寫規劃文件與討論底稿（`docs/planning/01–03`） | Claude |
| 裁決 A1–F4 各項事項、確認討論底稿（`docs/planning/04`） | 課程作者 |
| `CLAUDE.md`、`tools/*.py`、27 頁 Wiki、20 張簡報、所有 `docs/` | Claude（在 Claude 對話中執行） |
| 執行流程、檢查、修正、撰寫 run-log 與 reflection | Claude |
| 審閱、推送到 GitHub、開啟 Pages、繳交 | 課程作者 |
| 5 篇論文的研究成果 | 各論文作者 |
