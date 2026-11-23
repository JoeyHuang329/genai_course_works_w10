---
title: 跨文獻比較：圖與量子電路的四種結合方式
type: synthesis
sources: [S1, S2, S3, S4, S5]
difficulty: 2
updated: 2026-11-23
---

## 一句話

五篇文獻展示了「圖」與「量子電路」的四種結合：圖決定 Hamiltonian（S1）、圖變成振幅間的旋轉（S2）、圖變成對稱的雙 qubit 閘（S3）、以及反過來把電路變成圖（S4）；S5 提供評價這些做法的框架。

## 直觀解釋

| | S1 Verdon | S2 QuGCN | S3 EDU-QGC | S4 GNN 預測器 |
|---|---|---|---|---|
| 方向 | 圖 → 量子電路 | 圖 → 量子電路 | 圖 → 量子電路 | 量子電路 → 圖 |
| 誰是模型 | 量子電路 | 量子電路 | 量子電路 | 古典 graph transformer |
| 節點怎麼表示 | 每節點 ≥1 qubit | $N$ 個節點壓進 $\log_2 N$ 個 qubit 的振幅 | 每原子 1 qubit | 每個閘 1 個圖節點 |
| 邊怎麼表示 | Hamiltonian 的交互作用項 | Givens rotation（受控 $R_Y$） | EDU 雙 qubit 閘 | qubit 線上的先後關係 |
| 對稱性 | QGCNN 參數全圖共享 | 未特別處理 | 構造上等變 + 強制順序 | 由 GNN 本身提供 |
| 實驗規模 | 6～15 節點的隨機圖等 | Cora 子集 128～1024 節點 | QM9 ≤9 重原子 | 1～10 qubit 電路 |
| 執行環境 | 模擬 | 模擬（Qiskit Aer） | 無雜訊模擬（PennyLane） | 模擬 + Fake 雜訊後端 + 5 個電路真機 |
| S5 分類 | Fully Quantum | Fully Quantum（卷積） | Fully Quantum（等變） | 不在 QGNN 範圍 |

## 觀察

1. **省 qubit vs. 保結構**：S2 走「省 qubit」路線，代價是電路深度與資料載入成本；S1、S3 走「一節點一 qubit」路線，qubit 數線性成長，但結構清楚、容易保持對稱性。這正是 S5 說的表達力與可擴展性的取捨。
2. **Barren plateau 是共同的背景**：S1 用參數綁定避開它；S2 把 hybrid 模型的準確率限制歸因於它；S3 的 local 讀出優於 global 讀出也與它一致；S5 列為主要挑戰。
3. **幾乎全部是模擬**：只有 S4 有少量真機數據。依 S5 的標準，這些結果都應視為 quantum utility 的初步證據。
4. **GNN 與量子電路的關係是雙向的**：S4 說明圖神經網路也能成為設計量子電路的工具（例如篩選 ansatz）。

## 文獻怎麼說

- [S5] 現有的架構全景顯示量子表達力與實際可擴展性之間存在取捨，需要硬體感知的 ansatz 設計、有效率的圖到電路映射，以及能區分真正量子優勢與參數效率提升的基準。[作者分析] <!-- reviewed-claim -->
- [S2] 以 amplitude encoding 用 $\log_2 N$ 個 qubit 表示 $N$ 個節點，邊以 Givens rotation 實作。[理論]
- [S1] 每個節點對應一個量子子系統，邊決定哪些子系統之間允許耦合。[理論]
- [S3] 每個重原子一個 qubit，每條鍵一個 EDU。[理論]
- [S4] 把 PQC 視為有向圖，以古典 graph transformer 迴歸其 expressibility。[理論]
- [S1][S2][S3][S4][S5] 本表的四欄比較與「省 qubit vs. 保結構」的歸納為 Wiki 維護者依 S1–S5 整理，原文未有此比較。[推論]

## 相關頁面

- [QGNN 分類法](../concepts/qgnn-taxonomy.md)
- [資料編碼](../concepts/data-encoding.md)
- [QGNN 通用 ansatz](../models/qgnn-general-ansatz.md)、[QuGCN](../models/qugcn-givens.md)、[EDU-QGC](../models/edu-qgc.md)、[GNN 預測器](../models/gnn-expressibility-predictor.md)
- 回到 [index](../index.md)
