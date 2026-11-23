---
title: QGNN 通用 ansatz、QGRNN 與 QGCNN（Verdon 家族）
type: model
sources: [S1, S5]
difficulty: 2
updated: 2026-11-23
---

## 一句話

一個「由圖決定形狀」的參數化量子電路：一連串 Hamiltonian 演化，每個 Hamiltonian 只在**有邊相連的節點之間**放交互作用項；再透過不同的「參數綁定」方式，得到像 RNN 的 QGRNN 和像 GCN 的 QGCNN。

## 直觀解釋

把古典 GNN 的兩件事翻譯成量子語言：

| 古典 GNN | Verdon 的量子版本 |
|---|---|
| 鄰居之間傳訊息 | 只有相連節點的 qubit 之間有交互作用（雙 qubit 演化） |
| 一層的可訓練權重 | Hamiltonian 的係數 $W, B$ 與演化時間 $\eta$ |
| 疊很多層 | 把整串演化重複 $P$ 次 |
| RNN：每個時間步用同一組權重 | **QGRNN**：每次重複用同一組 $\eta$ |
| CNN/GCN：每個位置用同一組權重 | **QGCNN**：所有節點/邊用同一組係數 |

**為什麼要綁參數？** 完全自由的版本參數太多、太難訓練（[barren plateau](../concepts/barren-plateau.md)）；綁定參數等於加入結構先驗，就像 CNN 比全連接網路更好訓練。

## 稍微正式一點

**通用 ansatz：**

$$\hat U_{\text{QGNN}}(\boldsymbol\eta,\boldsymbol\theta) = \prod_{p=1}^{P}\;\prod_{q=1}^{Q} e^{-i\,\eta_{pq}\,\hat H_q(\boldsymbol\theta)}, \qquad \hat H_q(\boldsymbol\theta)=\sum_{\{j,k\}\in E}\sum_{r} W_{qrjk}\,\hat O_j^{(qr)}\!\otimes\hat P_k^{(qr)} + \sum_{v\in V}\sum_{r} B_{qrv}\,\hat R_v^{(qv)}$$

| 符號 | 意義 | 用途 |
|---|---|---|
| $P$ | 外層重複次數 | 相當於「層數」或「時間步數」 |
| $Q$ | 每次重複裡有幾個不同的 Hamiltonian | 例如一個管邊、一個管節點 |
| $\eta_{pq}$ | 第 $p$ 次重複、第 $q$ 個 Hamiltonian 的演化時間 | 可訓練，控制「這一步跑多久」 |
| $e^{-i\eta \hat H}$ | 讓系統在 $\hat H$ 下演化時間 $\eta$ | 一定是 unitary，可直接做成量子閘 |
| $\sum_{\{j,k\}\in E}$ | **只對圖上的邊加總** | 圖結構就是在這裡進入電路 |
| $\hat O_j\otimes \hat P_k$ | 作用在節點 $j$ 與 $k$ 上的一對算符（如 $Z_jZ_k$） | 「邊上的交互作用」= 訊息傳遞 |
| $W_{qrjk}$ | 邊項係數 | 可訓練，相當於邊上的權重 |
| $\hat R_v$、$B_{qrv}$ | 單一節點上的算符與係數 | 相當於節點自己的偏置/更新 |
| $\prod$ | 依序（time-ordered）相乘 | 電路是由右而左依序套用 |

**特化：**
- **QGRNN**：$\eta_{pq}\to\eta_q$（跨 $p$ 共用）。整串變成同一個小演化重複 $P$ 次 = Trotter 化的時間演化 → 適合學[量子系統的動態](../concepts/hamiltonian-and-ising.md)。
- **QGCNN**：$W_{qrjk}\to W_{qr}$、$B_{qrv}\to B_{qr}$（跨節點共用）。Hamiltonian 只剩全域參數 → 對節點重新編號不變，符合[排列不變性](../concepts/permutation-equivariance.md)。S1 把 QAOA（量子近似最佳化演算法）的一般化形式歸在這一類。
- **QSGCNN**：QGCNN 的連續變數版本，見 [QSGCNN](qsgcnn.md)。

**GHZ 實驗中的 QGCNN 具體長相**：$\hat H_1=\sum_{\{j,k\}\in E}\hat Z_j\hat Z_k$、$\hat H_2=\sum_{j\in V}\hat X_j$，可訓練的只有每層的 $\eta$。

## 文獻怎麼說

- [S1] 為使編譯容易，同一個 $\hat H_q$ 內的各項彼此可交換，但不同的 $\hat H_q$ 之間不需可交換。[理論]
- [S1] 為了讓 ansatz 更好訓練並避開 barren plateau，需要加入限制：在空間上綁定參數（卷積式）或在重複迭代間綁定參數（遞迴式）。[作者分析]
- [S1] 在量子網路上使用 QGNN 的好處之一：量子通訊回合數只與 $P$ 成正比，每個節點的局部動態與全域網路結構無關。[作者分析]
- [S1] QGCNN 在 GHZ 態準備任務中以穩定子期望值的負值為損失函數，成功學會在網路上準備近似 GHZ 態。[模擬實驗]
- [S5] Verdon 等人的模型是最早的 QGNN，受 QAOA 啟發，屬於 Fully Quantum；這類模型受雜訊、qubit 數與淺電路的限制，難以擴展。[作者分析]
- [S5] QGCNN 強制參數在全圖共享，能跨不同圖結構泛化，代價是在高度異質的圖上表達力可能下降。[作者分析]

## 常見誤解

- 「QGNN 就是把 GCN 公式抄到量子電路」：Verdon 家族並不模擬 $\hat A H W$ 的矩陣乘法，而是讓**圖決定交互作用的拓撲**。真正逐項模擬 GCN 公式的是另一條路線，見 [QuGCN](qugcn-givens.md)。

## 相關頁面

- [QGNN 分類法](../concepts/qgnn-taxonomy.md)

- [S1 文獻頁](../sources/S1-verdon-2019-qgnn.md)
- [QSGCNN](qsgcnn.md)
- [Hamiltonian 與 Ising 模型](../concepts/hamiltonian-and-ising.md)
- 回到 [index](../index.md)
