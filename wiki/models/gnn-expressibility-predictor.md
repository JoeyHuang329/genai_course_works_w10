---
title: GNN Expressibility 預測器（Graph Transformer for PQCs）
type: model
sources: [S4]
difficulty: 2
updated: 2026-11-23
---

## 一句話

一個在古典電腦上跑的 graph transformer：輸入「量子電路的圖 + 硬體雜訊資訊」，輸出這個電路的 expressibility 預測值。

## 直觀解釋

它就是一般的「圖迴歸」模型，和預測分子性質的 GNN 沒有本質差別，只是這次的「分子」是量子電路：

1. 電路 → 圖（見 [把量子電路看成圖](../concepts/circuits-as-graphs.md)）
2. 3 層 TransformerConv（帶注意力的訊息傳遞）讓每個閘節點吸收鄰近閘的資訊
3. 全域平均池化 → 得到整個電路的向量
4. 電路的全域特徵（深度、參數化閘數……）另外經過兩層全連接
5. 兩個向量串接，經過 3 層全連接迴歸頭 → 預測值
6. 以預測值和真值（5,000 次抽樣算出的 expressibility）的差距訓練

## 稍微正式一點

$$\hat y = \text{MLP}_{\text{reg}}\Big(\big[\,\text{MeanPool}(\text{TConv}^{(3)}(X, E))\;\Vert\;\text{MLP}_{\text{glob}}(g)\,\big]\Big)$$

$X$ 為節點特徵矩陣（每列 23 維），$E$ 為邊，$g$ 為全域特徵，$\Vert$ 為串接。（此式為 Wiki 維護者依 S4 架構圖整理的記法。）

## 文獻怎麼說

- [S4] 模型改編自 Wang et al. 的 graph transformer：節點特徵經 graph transformer 層捕捉鄰近節點的相關性，全域特徵經全連接層，兩者串接後送入全連接迴歸層。[引述]
- [S4] 模型在無雜訊與含雜訊後端的測試 RMSE 分別約 0.05 與 0.06，並能外插到訓練時未見過的更多 qubit 電路。[模擬實驗]
- [S4] 以 3 個 Fake 後端資料共同訓練的模型，在真實 IBM Hanoi 硬體 5 個電路上的 RMSE（約 0.1）優於只用 FakeHanoi 訓練的模型（約 0.19）。[硬體實驗]

## 相關頁面

- [S4 文獻頁](../sources/S4-aktar-2024-expressibility.md)
- [Expressibility](../concepts/expressibility.md)
- [圖與 GNN](../concepts/graph-and-gnn.md)
- 回到 [index](../index.md)
