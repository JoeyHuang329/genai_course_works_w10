---
title: QGNN 分類法（Fully Quantum / Hybrid / Quantum-Assisted）
type: concept
sources: [S5, S1, S2, S3]
difficulty: 2
updated: 2026-11-23
---

## 一句話

判斷一個「量子圖神經網路」屬於哪一類，要看量子電路在模型裡做什麼，而不是看有沒有量子電路。

## 直觀解釋

把 GNN 想成一條生產線「讀圖 → 訊息傳遞/聚合 → 更新 → 輸出」：

| 類別 | 量子電路負責哪一段 | 比喻 |
|---|---|---|
| **Fully Quantum** | 整條線：圖的資訊直接在量子態上表示與處理 | 整間工廠都換成量子設備 |
| **Hybrid（HQGNN）** | 核心工序：訊息傳遞、聚合、卷積、依圖而定的 Hamiltonian 演化 | 關鍵機台換成量子的 |
| **Quantum-Assisted（QAGNN）** | 頭尾：前處理、特徵轉換、最後的分類器 | 工廠是古典的，只外包品管 |

Fully/Hybrid 再依架構細分：
- **Recurrent**（時間步間共享參數，例：[QGRNN](../models/qgnn-general-ansatz.md)）
- **Convolutional**（節點間共享參數，例：QGCNN、[QuGCN](../models/qugcn-givens.md)）
- **Time-series convolutional**（同時處理時間與空間相依）
- **Equivariant**（電路結構保證排列對稱，例：[EDU-QGC](../models/edu-qgc.md)）

## 本 Wiki 文獻的位置

```
                     量子整合程度 ↑（概念上離 S5 定義的 advantage 越近、但越難擴展）
Fully Quantum ─┬─ Recurrent ......... S1 QGRNN
               ├─ Convolutional ..... S1 QGCNN / QSGCNN、S2 QuGCN
               └─ Equivariant ....... S3 EDU-QGC
Hybrid ─────────  （本 Wiki 無代表文獻）
Quantum-Assisted  （本 Wiki 無代表文獻）
                     量子整合程度 ↓（近期較實用、理論支持較弱）
```

S4 是「用古典 GNN 分析量子電路」，不在這個分類的範圍內，見 [把量子電路看成圖](circuits-as-graphs.md)。

## 文獻怎麼說

- [S5] 分類依據是量子計算整合進圖學習流程的方式與深度，而不是是否出現量子電路；此分類反映整合深度，不是僵硬的切分。[作者分析]
- [S5] Quantum-Assisted GNN 的量子元件是輔助工具（上游前處理或下游分類），Hybrid 則把量子運算直接放進 GNN 層的 message passing 或聚合；QAGNN 可處理較大的圖，但缺乏穩固的理論基礎。[作者分析]
- [S5] 在文獻總表中，S1、S2、S3 皆被歸為 Fully Quantum。[作者分析]
- [S1] QGRNN 與 QGCNN 分別以「跨迭代」與「跨節點」綁定參數，對應古典的 RNN 與圖卷積網路。[理論]
- [S2] QuGCN 把節點特徵、鄰接矩陣、權重矩陣三者都放進量子電路，作者稱之為 full-quantum design。[作者宣稱]
- [S3] EDU-QGC 以構造方式保證排列等變。[理論]

## 常見誤解

- 「有用到量子電路就叫 QGNN」：S5 強調要看電路的**角色**；例如只在最後接一個量子分類器的模型，是 quantum-assisted。

## 相關頁面

- [S5 文獻頁](../sources/S5-ceschini-2026-review.md)
- [Advantage / Utility / Quantum-inspired](advantage-vs-utility.md)
- [跨文獻比較：圖結構怎麼進到電路](../syntheses/graph-to-circuit-mappings.md)
- 回到 [index](../index.md)
