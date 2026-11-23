---
title: S1｜Verdon et al. 2019 — Quantum Graph Neural Networks
type: source
sources: [S1]
difficulty: 3
updated: 2026-11-23
---

## 書目

G. Verdon, T. McCourt, E. Luzhnica, V. Singh, S. Leichenauer, J. Hidary. *Quantum Graph Neural Networks*. arXiv:[1909.12264](https://arxiv.org/abs/1909.12264), 2019。作者來自 X（The Moonshot Factory）與 Google Research。PDF 版本標示為 under review 的預印本。

## 一句話

讓「圖的邊」決定「哪些量子子系統之間可以交互作用」，把圖神經網路的結構先驗直接寫進參數化量子電路，提出一整個家族的 ansatz：QGNN、QGRNN、QGCNN、QSGCNN。

## 這篇在做什麼

1. **動機**：沒有結構先驗的量子神經網路很難訓練（會遇到 [barren plateau](../concepts/barren-plateau.md)），需要更好的 ansatz（電路結構設計）。古典 GNN 在化學、生物物理上很成功，作者想把「利用資料的圖幾何」這個想法帶進量子電路。
2. **設定**：圖的每個節點對應一個量子子系統（一個或多個 qubit、qudit、qumode，甚至一整台量子電腦），邊決定哪些子系統可以耦合，這叫做「量子網路」（quantum network）。
3. **提出 4 種 ansatz**，見 [QGNN 通用 ansatz 與 QGRNN/QGCNN](../models/qgnn-general-ansatz.md) 與 [QSGCNN](../models/qsgcnn.md)。
4. **4 個數值實驗**（皆為模擬）：學習 Ising 模型動態、在感測網路上準備 GHZ 糾纏態、譜聚類、圖同構分類。

## 重點

- **通用 ansatz**：一連串由圖拓撲決定形狀的 [Hamiltonian](../concepts/hamiltonian-and-ising.md) 時間演化，重複 $P$ 次。
- **兩種參數綁定 → 兩種架構**：跨「重複次數」綁定參數 → QGRNN（像 RNN）；跨「節點」綁定參數 → QGCNN（像 CNN/GCN，帶來 [排列不變性](../concepts/permutation-equivariance.md)）。
- **QSGCNN**：用連續變數量子系統，在 Heisenberg picture 下推出含**圖 Laplacian** 的更新式，重現古典 GCN 的頻譜圖卷積。
- 應用都很「量子原生」：圖本身就定義了一個量子系統。

## 文獻怎麼說

- [S1] 沒有結構先驗的 QNN 會遇到量子版的「沒有免費午餐」問題，以梯度下降訓練會指數級困難，因此需要更好的 ansatz（S1 引用其參考文獻 [4] 的 barren plateau 結果）。[引述]
- [S1] 通用 QGNN ansatz 為 $P$ 次重複的 $Q$ 個 Hamiltonian 演化，Hamiltonian 的交互作用拓撲與問題圖相同；為了編譯方便，同一個 $\hat H_q$ 內的各項要求彼此可交換。[理論]
- [S1] QGRNN 等價於以 Trotter 方法模擬一個有效 Hamiltonian 的時間演化，因此適合學習圖上量子系統的動態。[理論]
- [S1] 學習帶橫場 Ising 模型動態的實驗中，初始猜測為隨機的密集連接圖，QGRNN 學回了真實的環狀結構與參數；損失為 15 個隨機時間點的平均 infidelity，fidelity 以 swap test 估計，梯度用步長 $10^{-4}$ 的有限差分。[模擬實驗]
- [S1] QGCNN 在不知道網路全域結構的情況下學會準備 GHZ 態；以相位回踢測試驗證時，7 節點網路觀察到約 7 倍的 Rabi 振盪頻率提升，作者解讀為達到感測的 Heisenberg 極限。[模擬實驗]
- [S1] QSGCNN 的耦合項與動能項演化在 Heisenberg picture 下，對每個節點的位置算符產生含圖 Laplacian $L_{jk}$ 的線性更新，與古典頻譜式圖卷積類比；再加上非二次的位能項提供非線性。[理論]
- [S1] 在單 qubit 精度的簡化下，QSGCNN 做譜聚類可得到合理結果，作者認為這對低 qubit 數的近期裝置是有前景的應用。[作者宣稱]
- [S1] 圖同構分類：比較兩張圖在同一組參數下量測到的「能量」分布，用 Kolmogorov–Smirnov 統計量判斷；在 Erdős–Rényi 隨機圖（6 節點與 15 節點、每組 100/50/50 對）上測試準確率多為 100%，以 Nelder–Mead 最佳化。[模擬實驗]

## 限制與批判

- 所有實驗都是小規模模擬；文中沒有在真實量子硬體上執行。
- 圖同構實驗的測試集只有 50 對圖，100% 準確率的統計意義有限。[推論]
- QSGCNN 需要連續變數（類比式）量子電腦，或用多個 qubit 模擬，硬體門檻高。

## 相關頁面

- [QGNN 分類法](../concepts/qgnn-taxonomy.md)（S5 將 S1 歸為 Fully Quantum）

- [QGNN 通用 ansatz、QGRNN、QGCNN](../models/qgnn-general-ansatz.md)
- [QSGCNN](../models/qsgcnn.md)
- [Hamiltonian 與 Ising 模型](../concepts/hamiltonian-and-ising.md)
- [圖與 GNN](../concepts/graph-and-gnn.md)
- 回到 [index](../index.md)
