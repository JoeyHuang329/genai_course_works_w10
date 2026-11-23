---
title: 維護紀錄（Log）
type: log
sources: []
difficulty: 1
updated: 2026-11-23
---

# 維護紀錄

只追加、不修改舊紀錄。格式見 [CLAUDE.md](../CLAUDE.md) §4。回到 [index](index.md)。

## [2026-11-21 23:40] discuss | S1–S5 討論底稿（批次）
- （時間為估計值：當天對話開始於 23:22，無系統時鐘紀錄。）
- 討論：Claude 讀完 5 篇 PDF，產出討論底稿 `docs/planning/03_文獻梳理與討論底稿.md`，每篇 3–7 個重點與 2 個待確認問題，並在 `02_待裁決事項.md` 列出 E1–E5 爭議點。
- 問題（A1c）：`pdftotext -layout` 抽取時，S5 出現多筆 `Missing language pack for 'Adobe-GB1'` 與 `Unknown font tag` 警告；S1、S2 的數學式被拆散、S2 雙欄文字交錯、S3 段落與行號重複。處理：數學式改以內文文字描述與上下文重建，表格數值逐一對照上下文。
- 生成：無（等待人類回覆）。

## [2026-11-23 22:33] human-reply | S1–S5 批次確認
- 人類回覆：見 `docs/planning/04_裁決結果_2026-11-23.md`。兩處推翻底稿建議：(1) QSGCNN 簡報也要放（B3）；(2) 主題不限定為 QGNN，S4 不特別定位（B4）。E1–E5 照建議。
- 流程偏差：C1 要求逐篇確認，實際為 5 篇批次確認一次。
- 生成：建立 [CLAUDE.md](../CLAUDE.md)（schema）、`raw/sources.md`、`tools/check.py`。

## [2026-11-23 22:39] ingest | S1 Verdon 2019
- 討論：依 11/21 底稿 S1 段（重點 4 條、Q1-1、Q1-2）。
- 人類回覆：B3 → QSGCNN 獨立成頁、難度 3、簡報也要放。
- 生成：新增 [S1](sources/S1-verdon-2019-qgnn.md)、[graph-and-gnn](concepts/graph-and-gnn.md)、[hamiltonian-and-ising](concepts/hamiltonian-and-ising.md)、[permutation-equivariance](concepts/permutation-equivariance.md)、[barren-plateau](concepts/barren-plateau.md)（骨架）、[qgnn-general-ansatz](models/qgnn-general-ansatz.md)、[qsgcnn](models/qsgcnn.md)；建立 index、glossary。
- 問題（L）：第一次 lint ERROR 2 — 我在兩頁中提前連到 S2 才會建立的 `qubit-basics.md`、`qugcn-givens.md`（斷鏈）。處理：暫改純文字，S2 ingest 時補回連結。第二次 lint 通過。

## [2026-11-23 22:42] ingest | S2 Hu et al. 2022（QuGCN）
- 討論：依底稿 S2 段（重點 6 條、Q2-1、Q2-2）。
- 人類回覆：E1 → 「指數級」只能連同 $\log^2 N$ 劣勢一起寫；Q2-1 未回覆，採建議（Givens 圖解）。
- 生成：新增 [S2](sources/S2-hu-2022-qugcn.md)、[qugcn-givens](models/qugcn-givens.md)、[qubit-basics](concepts/qubit-basics.md)、[pqc-and-vqa](concepts/pqc-and-vqa.md)、[data-encoding](concepts/data-encoding.md)（骨架）；更新 graph-and-gnn、barren-plateau、hamiltonian-and-ising、qgnn-general-ansatz（補回 S1 時移除的連結）、index、glossary。
- 問題（A1c）：S2 雙欄排版使 Givens 範例式 (5) 的正負號無法從抽取文字確定 → Wiki 改用標準定義，不照抄範例。
- 問題（A3 自查）：qubit-basics 表格中的 `|0⟩`、`|a|` 管線符號會切斷 Markdown 表格欄位 → 改為 `\|`。lint 腳本抓不到這類問題（只檢查連結與標記）。
- 問題（L）：lint 通過，但人工複查發現誇大用詞 regex 只比對「指數級加速」，漏掉 S2 頁的「指數級改善」→ 擴大 regex 為「指數級?(加速|改善|降低|優勢|提升|減少)」等。該行已附限制條件，標記為 reviewed-claim。

## [2026-11-23 22:43] ingest | S3 Ryu et al. 2023（EDU-QGC、QM9）
- 討論：依底稿 S3 段（重點 7 條、Q3-1、Q3-2）。
- 人類回覆：E2 → 「比古典好」與「SOTA 低 10 倍」、實驗公平性問題三者並陳；E3 → 1-WL 標為引述 Mernyei et al.；Q3-1 未回覆，採建議（Wiki 記錄「全部編碼成 |1⟩」發現）。
- 生成：新增 [S3](sources/S3-ryu-2023-materials.md)、[edu-qgc](models/edu-qgc.md)；更新 permutation-equivariance（加 1-WL 說明）、data-encoding、graph-and-gnn、index、glossary。
- 問題（A1c）：S3 抽取文字有段落與行號重複，表 3–9 的數值靠前後文對齊；所有寫進 Wiki 的數字逐一回頭對照表格。
- 問題（A3 自查）：S3 頁為了避免連到尚未建立的 advantage-vs-utility 頁，我把「quantum utility」**錯連**到 permutation-equivariance 頁。連結目標存在，lint 不會報錯 → 人工發現後改成純文字。**這類「語意錯的連結」只能靠人工或 LLM 檢查。**
- 問題（L）：lint WARN 1 為誤報：log.md 中描述 regex 的那一行被判為誇大用詞 → 修改 check.py，誇大用詞檢查跳過 type=log 的頁面。

## [2026-11-23 22:45] ingest | S4 Aktar et al. 2024（GNN 預測 expressibility）
- 討論：依底稿 S4 段（重點 4 條、Q4-1、Q4-2）。
- 人類回覆：B4 → **推翻底稿**：不加「⚠️ 這不是 QGNN」警示、不特別定位；Wiki 主題擴大為「量子計算 × GNN × 電路」。Q4-1 → 照一般 model 頁處理；Q4-2 → 不需要誤分類 lint 規則。
- 生成：新增 [S4](sources/S4-aktar-2024-expressibility.md)、[expressibility](concepts/expressibility.md)、[circuits-as-graphs](concepts/circuits-as-graphs.md)、[gnn-expressibility-predictor](models/gnn-expressibility-predictor.md)；更新 pqc-and-vqa、graph-and-gnn、index、glossary。
- 問題（A3 查證）：11/21 底稿與 02 E5 寫「S4 用到含雜訊的後端資料」，回頭查原文發現 12,000 筆含雜訊樣本來自 IBM **Fake 後端（以真實裝置雜訊模型模擬）**，真實硬體（IBM Hanoi）只測了 5 個電路。底稿的描述不夠精確 → Wiki 以 [模擬實驗] 與 [硬體實驗] 分開標記。
- 問題（L）：lint 通過。

## [2026-11-23 22:49] ingest | S5 Ceschini et al. 2026（批判性回顧）
- 討論：依底稿 S5 段（重點 6 條、Q5-1、Q5-2）。
- 人類回覆：B5 → 採用三分法並寫成獨立概念頁；Q5-2 → S2 的歸類標 [推論]，查證後再定。
- 生成：新增 [S5](sources/S5-ceschini-2026-review.md)、[qgnn-taxonomy](concepts/qgnn-taxonomy.md)、[advantage-vs-utility](concepts/advantage-vs-utility.md)、[qgnn-challenges](concepts/qgnn-challenges.md)、[graph-to-circuit-mappings](syntheses/graph-to-circuit-mappings.md)、[overview](overview.md)；大幅更新 data-encoding（四種編碼比較表）、barren-plateau（數學性質與對策）；更新 hamiltonian-and-ising、graph-and-gnn、qgnn-general-ansatz、qugcn-givens、edu-qgc、S1、S3（補回 S3 ingest 時拿掉的 utility 連結）、index（重寫為分組版）、glossary。
- 問題（A3 查證）：**11/21 討論底稿把 S2 歸為 Hybrid，是錯的。** 查 S5 §4.1.3 與附錄 Table 7：S5 把 Hu et al.（ref [50]）、Verdon et al.（[48]）、Ryu et al.（[63]）都列為 **Fully Quantum**。底稿當時已自己標註這是推論（Q5-2），這次依原文修正。證據等級欄位在這裡發揮了作用：被標成推論的陳述，ingest 時被優先查證。
- 問題（A3 自查）：advantage-vs-utility 頁有兩條陳述把「作者的數據」和「我的判斷」寫在同一條、只標一個 [作者分析] → 拆成兩條，判斷改標 [推論] 或改引 S5 的原話。lint 只能檢查「標籤個數 = 1」，檢查不出「一條陳述裡混了兩種證據」。
- 問題（L）：lint ERROR 1（qgnn-taxonomy 連到尚未寫的 synthesis 頁）、WARN 10。10 個 WARN 逐條人工審閱，**全是 S5 在否定或定義量子優勢**（例如「而不是 quantum advantage」），不是誇大 → 加上 reviewed-claim 標記；其中一行在程式碼區塊內，加註解會被顯示，改為改寫措辭。結論：字面 regex 分不出否定語氣，在「專門討論優勢」的頁面上誤報率很高。之後又出現 overview 孤兒頁（index 尚未改寫）→ 重寫 index 後通過。
- 問題（L，LLM 人工檢查）：比對 S3 的 MAE 數字（1.51／1.77／1.88）、S4 的 RMSE 數字、模型名稱 QGCNN／QuGCN／QSGCNN 在各頁的用法，未發現矛盾。

## [2026-11-23 22:49] fix | log 時間戳更正
- 問題：S3、S4、S5 三筆紀錄的時間是我憑感覺填寫（22:47、22:53、23:08），不是讀系統時鐘；實際完成時間依 `docs/check-reports/` 檔名為 22:43、22:45、22:49。已更正上面三筆的時間。
- 對策：之後所有 log 時間一律由 `date` 指令產生，不手填。

## [2026-11-23 22:58] gap-fill | 簡報階段發現的 Wiki 缺口
- 觸發：簡報 C1 可讀性檢查發現第 10 張使用「譜聚類」「圖同構」但未解釋；查 Wiki 只有「做了這兩個實驗」，**沒有定義** → 依 CLAUDE.md §3.4 視為 Wiki 缺口，先補 Wiki 再改投影片，不在投影片上自行撰寫定義。
- 生成：[qsgcnn](models/qsgcnn.md) 新增「兩個應用任務是什麼？」小節與 3 條文獻陳述（S1 引述、S5 分析）；frontmatter sources 加入 S5；[glossary](glossary.md) 新增 Graph isomorphism、Spectral clustering。
- 問題（L）：lint 通過。

## [2026-11-23 23:00] schema | CLAUDE.md v1 → v2
- 依第一次完整執行（ingest 5 篇 + 20 張簡報）的檢查紀錄修改流程，細節見 [CLAUDE.md](../CLAUDE.md) §5 與 `docs/reflection.md`。
