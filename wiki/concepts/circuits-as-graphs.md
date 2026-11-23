---
title: 把量子電路看成圖（Quantum Circuits as Graphs）
type: concept
sources: [S4]
difficulty: 1
updated: 2026-11-23
---

## 一句話

量子電路本身就是一張有向無環圖（DAG）：閘是節點，同一條 qubit 線上「前一個閘 → 下一個閘」是邊，所以可以直接丟給圖神經網路處理。

## 直觀解釋

```
q0: ─[RY]──●──[RY]──
           │
q1: ─[RY]──⊕──[RY]──
```

轉成圖：
- **輸入節點** ×2（每條 qubit 線的起點）
- **閘節點** ×5（4 個 RY + 1 個 CNOT）
- **輸出節點** ×2（量測）
- **邊**：沿著每條 qubit 線連起來；CNOT 同時接在兩條線上，所以它有兩條入邊、兩條出邊。

每個節點再附上特徵向量：它是什麼閘、作用在哪個 qubit、那個 qubit 的硬體雜訊參數。

## 稍微正式一點

$G=(V,E)$，$V$ = 輸入節點 ∪ 閘節點 ∪ 輸出節點，$E$ = 資訊在電路中流動的方向。這和編譯器裡的「資料相依圖」是同一個概念：GNN 可以從中學到哪些結構（深度、糾纏閘的位置）會影響電路的性質。

## 文獻怎麼說

- [S4] 把 PQC 表示成有向圖：節點分為輸入、閘、輸出節點，邊表示電路中的資訊流；閘節點只使用裝置的原生閘（RZ、X、SX、CNOT）。[理論]
- [S4] 每個節點的特徵向量長 23：6 維節點類型 one-hot、10 維作用的 qubit、7 維硬體校正資訊（兩個 qubit 的 T1、T2、閘錯誤率、讀出錯誤 0→1 與 1→0）。[理論]
- [S4] 已有研究把量子電路視為圖、用 graph transformer 或 GNN 預測雜訊對電路 fidelity 的影響（S4 引用 Wang et al.、Saravanan et al.）。[引述]

## 相關頁面

- [圖與 GNN](graph-and-gnn.md)
- [GNN expressibility 預測器](../models/gnn-expressibility-predictor.md)
- [S4 文獻頁](../sources/S4-aktar-2024-expressibility.md)
- 回到 [index](../index.md)
