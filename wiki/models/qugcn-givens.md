---
title: QuGCN — 用 Givens rotation 實作鄰接矩陣
type: model
sources: [S2, S5]
difficulty: 2
updated: 2026-11-23
---

## 一句話

一條邊 $(p,q)$ ＝ 一個在第 $p$、$q$ 個基底態之間的旋轉：它把一部分振幅從節點 $p$「倒」給節點 $q$，這就是量子版的鄰居訊息傳遞。

## 直觀解釋

1. **把節點放進振幅**：對某一個特徵維度，把 $N$ 個節點的值排成向量、除以長度，當成 $\lceil\log_2 N\rceil$ 個 qubit 的狀態向量。第 $i$ 個基底態 $|i\rangle$ 的振幅 = 第 $i$ 個節點的值。
2. **一條邊 = 一次旋轉**：在 $|p\rangle$ 與 $|q\rangle$ 張成的平面上轉一個角度，兩個振幅就會互相混合，其他節點不受影響。
3. **所有邊依序轉一遍** → 整體效果近似「乘上鄰接矩陣」。
4. **權重 $W$** 交給一般的變分量子電路（一排 $R_Y$ + 糾纏閘，重複 7 次）。
5. 量測後分兩組加總，過 Softmax 得到分類結果。

## 稍微正式一點

**Givens rotation** $G_N(p,q,\theta)$ 是 $N\times N$ 的單位矩陣，只在第 $p,q$ 列/行換成：

$$\begin{pmatrix} \cos\frac{\theta}{2} & \sin\frac{\theta}{2} \\ -\sin\frac{\theta}{2} & \cos\frac{\theta}{2}\end{pmatrix}, \qquad
\begin{pmatrix} s_p' \\ s_q' \end{pmatrix} = \begin{pmatrix} \cos\frac{\theta}{2} & \sin\frac{\theta}{2} \\ -\sin\frac{\theta}{2} & \cos\frac{\theta}{2}\end{pmatrix}\begin{pmatrix} s_p \\ s_q \end{pmatrix}$$

| 符號 | 意義 | 用途 |
|---|---|---|
| $s_p, s_q$ | 狀態向量中第 $p$、$q$ 個振幅 = 節點 $p$、$q$ 的特徵值 | 被混合的兩個節點 |
| $\theta$ | 旋轉角；S2 中**所有 Givens rotation 共用同一個 $\theta$，是超參數** | 控制「傳多少訊息給鄰居」 |
| $\cos\frac{\theta}{2}$ | 保留自己的比例 | 類似自環 |
| $\sin\frac{\theta}{2}$ | 從鄰居拿來的比例 | 類似鄰接矩陣的非零項 |
| 2×2 核心 | 和 $R_Y$ 閘同一種旋轉（差一個角度正負號的慣例） | 所以可以用真正的量子閘實作 |

**多 qubit 時怎麼做？** 若 $p, q$ 的二進位表示差很多位（例如 $p=13=01101_2$、$q=18=10010_2$），要先用 X、CNOT 等**翻轉閘**把振幅一位一位搬到只差一位的位置，再用**多重受控** $R_Y$ 完成旋轉，最後對稱地把翻轉閘做回來，避免影響其他態。每個 Givens rotation 需要 $O(n^2)$ 個基本閘（$n=\log N$ 個 qubit）。

**複雜度比較**（$L$ 層、$N$ 節點、$D$ 特徵、$E$ 邊）：

| | 古典 GCN | QuGCN |
|---|---|---|
| $HW$（特徵轉換） | $O(LND^2)$ | $O(LN\log D)$ |
| $\hat AH$（鄰居聚合） | $O(L(E+N)D)$ | $O(L\log^2 N\cdot ED)$ |

## 文獻怎麼說

- [S2] Givens rotation 可直觀地把 $p$ 態的振幅傳給 $q$ 態，除了 $p,q$ 位置以外的狀態保持不變，因此可用來做圖結構嵌入；對 $N$ 節點的圖產生 $N$ 個 Givens rotation。[理論]
- [S2] Givens rotation 能表示有向圖；無向圖只考慮 $p\le q$ 的一半。[理論]
- [S2] 因為每個 Givens rotation 的超參數相同，未來可依特定樣式把多個 Givens rotation 合併（例如兩個互不重疊的 rotation 可用一個 $R_Y$ 實作），作者認為這是潛在的加速來源。[作者分析]
- [S2] QuGCN 在特徵維度上的成本以對數成長，但鄰居聚合多出 $\log^2 N$，在節點數主導複雜度時反而比古典 GCN 成長更快。[作者分析]
- [S2] 在 Cora 子集上 QuGCN 準確率高於只有 VQC 的 QNN，接近古典 GCN，部分情況下優於 hybrid QGNN。[模擬實驗]
- [S5] S2 被歸類為 Fully Quantum 的量子卷積 GNN：以 Givens rotation 把鄰接關係轉成作用在 qubit 對上的 unitary；其可擴展性同樣受限於大圖所需的 qubit 數。[作者分析]

## 常見誤解

- 「$\log_2 N$ 個 qubit 就能裝 $N$ 個節點，所以一定比較快」：qubit 數少不等於步驟少。把資料放進振幅（態準備）與量測（需要大量重複取樣）都有成本，見 [資料編碼](../concepts/data-encoding.md)。
- 「$\theta$ 是學出來的邊權重」：在 S2 裡 $\theta$ 是共用的超參數；可學習的部分在 VQC。

## 相關頁面

- [QGNN 分類法](../concepts/qgnn-taxonomy.md)

- [S2 文獻頁](../sources/S2-hu-2022-qugcn.md)
- [圖與 GNN](../concepts/graph-and-gnn.md)（GCN 公式）
- [QGNN 通用 ansatz](qgnn-general-ansatz.md)（另一條路線：圖決定交互作用拓撲）
- [資料編碼](../concepts/data-encoding.md)
- 回到 [index](../index.md)
