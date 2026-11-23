---
title: 排列不變性與等變性（Permutation Invariance / Equivariance）
type: concept
sources: [S1, S3]
difficulty: 2
updated: 2026-11-23
---

## 一句話

節點的編號是人為的；好的圖模型不應該因為「把 3 號節點改叫 7 號」就給出不同答案。

## 直觀解釋

- **不變（invariant）**：重新編號後，**整張圖的輸出**完全一樣。用在圖分類（例如「這個分子的能隙是多少」）。
- **等變（equivariant）**：重新編號後，**每個節點的輸出跟著一起換位置**，內容不變。用在節點分類。
- 類比：CNN 的**平移等變性**——貓在圖片左邊或右邊，偵測到的特徵只是跟著移動。

## 稍微正式一點

令 $\pi$ 為節點的一個排列、$P_\pi$ 為對應的置換矩陣。
- 不變：$f(P_\pi A P_\pi^\top, P_\pi X) = f(A, X)$
- 等變：$f(P_\pi A P_\pi^\top, P_\pi X) = P_\pi f(A, X)$

GCN 能做到等變，是因為 $W$ 被所有節點共用、鄰接矩陣又跟著節點一起被置換。量子版本要做到同樣的事，就得讓電路裡「每個節點、每條邊」用相同的參數。

**1-WL 測試（Weisfeiler–Lehman）**：一種反覆把「自己的標籤 + 鄰居標籤的多重集合」雜湊成新標籤的演算法，用來判斷兩張圖是否可能同構。標準 message passing GNN 的區分能力最多與 1-WL 相同，所以「能否超越 1-WL」常被用來衡量圖模型的表達力。

## 文獻怎麼說

- [S1] 古典圖卷積網路的關鍵特性是排列不變性，類比於一般卷積的平移不變性；在 QGCNN 中這表現為 Hamiltonian 只能有全域、而不能有局部的可訓練參數。[理論]
- [S3] EDU-QGC 以「兩端用同一個單 qubit 閘夾住對角閘」的雙 qubit 閘構成連結層，使電路對節點排列等變，並以對所有 qubit 取平均的讀出函數達成排列不變。[理論]
- [S3] 參數不同的 EDU 一般不可交換，若隨意排序會破壞等變性，因此需強制規定套用順序。[理論]
- [S3] EDU-QGC 可通過 1-WL 測試，而決定性的古典 MPNN 無法通過（S3 引用 Mernyei et al.）。[引述]

## 相關頁面

- [EDU-QGC](../models/edu-qgc.md)

- [圖與 GNN](graph-and-gnn.md)
- [QGNN 通用 ansatz、QGRNN、QGCNN](../models/qgnn-general-ansatz.md)
- 回到 [index](../index.md)
