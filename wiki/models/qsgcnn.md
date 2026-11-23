---
title: QSGCNN（Quantum Spectral Graph Convolutional Neural Network）
type: model
sources: [S1, S5]
difficulty: 3
updated: 2026-11-23
---

## 一句話

用「連續變數」量子系統（每個節點是一個量子振子，有位置 $\hat x$ 與動量 $\hat p$）設計的 QGCNN；把它的演化寫出來，會自然冒出古典頻譜式 GCN 裡的**圖 Laplacian**。

## 直觀解釋

想像每個節點是一顆掛在彈簧上的小球：
- **邊 = 彈簧**：相連的兩顆球位置差越大，能量越高 → 它們會互相拉近。這一步就是**訊息傳遞**（像鄰居平均）。
- **動能項**：讓球依照自己的動量移動 → 相當於**節點更新**。
- **非線性位能**（例如雙井形狀的四次方位能）：讓球偏好落在某些位置 → 提供**非線性**，類似 ReLU 的角色。
- 交替重複這四步 $P$ 次，就得到一個多層的圖卷積網路，只不過一切都在量子態上進行。

這裡的「Heisenberg picture」只是一種觀點：不追蹤量子態怎麼變，而是追蹤「位置算符 $\hat x_j$ 怎麼變」，這樣更新式就很像古典神經網路的一層。

## 稍微正式一點

四個 Hamiltonian（$Q=4$）：
- 耦合（訊息傳遞）：$\hat H_C=\tfrac12\sum_{\{j,k\}\in E}\Lambda_{jk}(\hat x_j-\hat x_k)^2$，$\Lambda_{jk}$ 是**固定的**邊權重（不可訓練）
- 動能（節點更新）：$\hat H_K=\tfrac12\sum_{j\in V}\hat p_j^2$
- 非線性：$\hat H_A=\sum_{j\in V} f(\hat x_j)$，例如 $f(x)=((x-\mu)^2-\omega^2)^2$

先做耦合、再做動能，位置算符的更新是：

$$e^{-i\gamma \hat H_K}\,e^{-i\alpha \hat H_C}:\quad \hat x_j \;\mapsto\; \hat x_j + \gamma\,\hat p_j - \alpha\gamma\sum_{k\in V} L_{jk}\,\hat x_k$$

| 符號 | 意義 | 用途 |
|---|---|---|
| $\hat x_j$、$\hat p_j$ | 節點 $j$ 的位置與動量算符 | 節點的「特徵」與它的「速度」 |
| $\alpha$、$\gamma$ | 耦合與動能演化的時間 | **可訓練參數**，像每層的學習權重 |
| $L_{jk}=\delta_{jk}\sum_v\Lambda_{jv}-\Lambda_{jk}$ | 加權圖 **Laplacian**（度數矩陣 − 鄰接矩陣） | 和頻譜式 GCN 用的是同一個矩陣 |
| $-\alpha\gamma\sum_k L_{jk}\hat x_k$ | 自己減去鄰居的加權差 | 把節點往鄰居拉近 = 圖卷積／平滑 |
| $\gamma\hat p_j$ | 動量帶來的位移 | 和古典 GCN 不同：動量會**跨層累積** |

再做 $\hat H_A$ 與 $\hat H_K$：$\hat x_j\mapsto \hat x_j+\beta\hat p_j-\delta\beta f'(\hat x_j)$，這一步是非線性映射。整體：
$\hat U_{\text{QSGCNN}}=\prod_{j=1}^{P}e^{-i\beta_j\hat H_K}e^{-i\delta_j\hat H_A}e^{-i\gamma_j\hat H_K}e^{-i\alpha_j\hat H_C}$，可訓練參數為 $\{\alpha,\beta,\gamma,\delta\}$。

## 兩個應用任務是什麼？

- **譜聚類（spectral clustering）**：利用圖 Laplacian 的低頻特徵向量（「最平滑」的幾種節點取值方式）把節點分群；連得緊密的節點會落在同一群。
- **圖同構（graph isomorphism）**：判斷兩張圖是否「只差在節點編號」——若能重新編號使兩者的邊完全一樣，就是同構。這是衡量圖模型區分能力的經典測試（參見 [1-WL](../concepts/permutation-equivariance.md)）。

## 文獻怎麼說

- [S1] 譜聚類是找出圖 Laplacian 的低頻特徵值、並對節點取值分群以辨識圖中的群集（S1 引用其參考文獻 [37]）。[引述]
- [S5] 在譜聚類中，目標是利用圖 Laplacian 的低頻特徵向量辨識群集；QSGCNN 類方法可把依圖而定的頻譜資訊編進量子動態並透過量測取出。[作者分析]
- [S1] 圖同構基準是用圖模型判斷兩張圖是否同構，用來衡量古典 GNN 的表示能力（S1 引用其參考文獻 [38]）。[引述]

- [S1] QSGCNN 在 Heisenberg picture 下重現了 Kipf & Welling GCN 的「訊息傳遞、節點更新、非線性」交替結構，是其量子相干的類比。[理論]
- [S1] 與古典 GCN 的一個差異：動量可以在層與層之間累積。[理論]
- [S1] 加入次數大於 2 的位能會產生非高斯態，一般而言無法以古典電腦有效模擬；交替組合高斯與非高斯變換可得到量子計算通用的 ansatz（S1 引用其參考文獻 [28]、[29]）。[引述]
- [S1] 實作上，連續變數可用類比式量子電腦，或在數位量子電腦上以多個 qubit 模擬；單 qubit 精度的簡化版把 $\hat p^2$ 換成 $\hat X$、$\hat x$ 換成 $|1\rangle\langle1|$，用於譜聚類與圖同構實驗。[理論]
- [S1] 圖同構分類中，對兩張圖以相同參數執行單 qubit 精度 QSGCNN，比較量測能量分布的 KS 統計量（大於 0.4 判為不同構），在 6 與 15 節點隨機圖上得到高準確率。[模擬實驗]

## 常見誤解

- 「Spectral 就要做特徵分解」：古典頻譜式 GCN 原本要對 Laplacian 做特徵分解，QSGCNN 則是讓 Laplacian 透過物理演化**隱式**作用，不需要顯式分解。[推論] 本條為 Wiki 維護者的歸納。

## 相關頁面

- [QGNN 通用 ansatz、QGRNN、QGCNN](qgnn-general-ansatz.md)
- [圖與 GNN](../concepts/graph-and-gnn.md)（GCN 公式）
- [S1 文獻頁](../sources/S1-verdon-2019-qgnn.md)
- 回到 [index](../index.md)
