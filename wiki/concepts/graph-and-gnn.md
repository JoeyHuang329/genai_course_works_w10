---
title: 圖與圖神經網路（Graph & GNN）
type: concept
sources: [S1, S2, S3, S4, S5]
difficulty: 1
updated: 2026-11-23
---

## 一句話

圖神經網路（Graph Neural Network, GNN）讓每個節點反覆「收集鄰居的資訊、更新自己」，學出能反映圖結構的節點表示。

## 直觀解釋

- **圖（graph）** $G=(V,E)$：$V$ 是節點（例如論文、原子、qubit），$E$ 是邊（引用關係、化學鍵、可交互作用）。
- 每個節點有一個**特徵向量**（例如論文的關鍵字、原子的種類）。
- GNN 的一層就像一次「開會」：每個節點聽完鄰居的發言（**message passing，訊息傳遞**），整理成一個摘要（**aggregation，聚合**），再用摘要更新自己的看法（**update，更新**）。
- 疊 $k$ 層，節點就能「聽到」$k$ 步以外的資訊。

## 稍微正式一點

把 $n$ 個節點的特徵排成矩陣 $X \in \mathbb{R}^{n \times d}$（每列一個節點、$d$ 個特徵），鄰接矩陣 $A \in \mathbb{R}^{n\times n}$（$A_{jk}=1$ 表示 $j,k$ 相連）。一般的 message passing 寫成 $H^{(k)} = P(A, H^{(k-1)}, W^{(k)})$，$H^{(0)} = X$。最常見的實作是 **GCN（Graph Convolutional Network）**：

$$H^{(k)} = \sigma\!\left(\tilde D^{-1/2}\,\tilde A\,\tilde D^{-1/2}\; H^{(k-1)}\; W^{(k)}\right)$$

| 符號 | 意義 | 用途 |
|---|---|---|
| $H^{(k-1)}$ | 第 $k-1$ 層的節點表示（$n \times d$） | 本層的輸入 |
| $\tilde A = A + I$ | 鄰接矩陣加上自環 | 讓節點在聚合時也保留自己的資訊 |
| $\tilde D$ | $\tilde A$ 的度數矩陣（對角，$\tilde D_{jj}=\sum_k \tilde A_{jk}$） | 正規化用 |
| $\tilde D^{-1/2}\tilde A \tilde D^{-1/2}$ | 正規化鄰接矩陣 | 「鄰居平均」；避免鄰居多的節點數值爆大 |
| $W^{(k)}$ | 可訓練權重（$d \times d'$），**所有節點共用** | 特徵轉換，相當於一個全連接層 |
| $\sigma$ | 非線性函數（如 ReLU） | 讓模型能表示非線性關係 |

**讀法**：先用 $W$ 把每個節點的特徵轉換一下（$HW$），再用正規化鄰接矩陣對鄰居取加權平均（$\hat A \cdot$），最後過非線性。

兩個關鍵性質：
1. **權重共享**：$W$ 不依節點而變（像 CNN 的 kernel 在影像上滑動）。
2. **[排列等變性](permutation-equivariance.md)**：節點重新編號，輸出只會跟著重新排列。

## 文獻怎麼說

- [S1] GNN 的發展可整理在 message passing 框架下；GCN 以正規化的自環鄰接矩陣實作訊息傳遞，是最常見的實作之一。[引述]
- [S2] 未正規化的 $AHW$ 會讓鄰居多的節點數值在迭代中越變越大，因此改用 $\tilde D^{-1/2}\tilde A\tilde D^{-1/2}$ 正規化。[理論]
- [S2] 矩陣乘法 $(\hat A H)W=\hat A(HW)$ 的順序可交換，若特徵維度逐層遞減，先算 $HW$ 可降低成本；QuGCN 據此安排電路順序。[理論]
- [S3] 在分子性質預測中，常把分子轉成圖（原子為節點、鍵為邊）再用 MPNN 類模型；加入連到所有節點的 master node 可模擬長距離交互作用（S3 引用 Gilmer et al.）。[引述]
- [S5] 古典 GNN 的兩個痛點：大規模圖上 message passing 的計算與記憶體成本高；重複聚合導致 over-smoothing，節點表示變得無法區分。[引述]
- [S5] 圖 Laplacian $L=D-A$ 編碼了整張圖的結構；為避免權重不平衡影響頻譜，常用正規化形式 $L_{\text{norm}}=I-D^{-1/2}AD^{-1/2}$。[理論]
- [S4] GNN 也可以拿來處理「量子電路本身」：把電路轉成圖，用 graph transformer 做迴歸。[模擬實驗]

## 常見誤解

- 「GNN 越深越好」：層數多會 over-smoothing，所有節點的表示趨於相同。

- 「GNN 就是把 CNN 用在圖上」：只有一部分（spectral / convolutional 類）是這樣類比，GNN 還有 recurrent、attention 等家族。

## 相關頁面

- [排列等變性](permutation-equivariance.md)
- [QGNN 通用 ansatz](../models/qgnn-general-ansatz.md)：量子版本如何模仿權重共享
- [QuGCN](../models/qugcn-givens.md)：把 $\hat A$ 與 $W$ 逐項搬上量子電路
- [把量子電路看成圖](circuits-as-graphs.md)：反方向，用 GNN 分析電路
- 回到 [index](../index.md)
