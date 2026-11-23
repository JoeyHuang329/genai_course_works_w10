---
title: S2｜Hu et al. 2022 — QuGCN：NISQ 時代的量子圖卷積網路設計
type: source
sources: [S2]
difficulty: 2
updated: 2026-11-23
---

## 書目

Z. Hu, J. Li, Z. Pan, S. Zhou, L. Yang, C. Ding, O. Khan, T. Geng, W. Jiang. *On the Design of Quantum Graph Convolutional Neural Network in the NISQ-Era and Beyond*. 2022 IEEE 40th International Conference on Computer Design (ICCD), pp. 290–297. [doi:10.1109/ICCD56317.2022.00050](https://doi.org/10.1109/ICCD56317.2022.00050)。作者來自 George Mason、Rochester、UConn。

## 一句話

把 GCN 公式 $\sigma(\hat A H W)$ 的三個部件逐一翻成量子電路：節點特徵 → amplitude encoding、鄰接矩陣 $\hat A$ → Givens rotation、權重 $W$ → 變分量子電路（VQC）。

## 這篇在做什麼

1. 指出既有量子 GCN 的兩個問題：有的只實作了權重矩陣（電路裡沒有圖結構），有的把鄰接矩陣留在古典端算（變成效能瓶頸）；另外多數設計用 $O(N)$ 個 qubit 表示 $N$ 個節點，不可擴展。
2. 提出 **QuGCN**，細節見 [QuGCN 模型頁](../models/qugcn-givens.md)。
3. 在 Cora 引文網路的子集上做半監督節點二分類，並做操作數（gate 數）複雜度分析。

## 重點

- **核心觀察**：Givens rotation（數值線代中只在兩個座標軸平面上旋轉的矩陣）的 2×2 核心，和 [qubit](../concepts/qubit-basics.md) 上的 $R_Y$ 閘是同一種旋轉 → 可以用量子閘在兩個基底態之間「搬振幅」，模擬鄰居之間傳訊息。
- **設計原則 1**：量子版要包含古典 GCN 的所有運算。
- **設計原則 2**：$\hat A H W$ 的乘法順序可以調換；若特徵維度逐層遞減，先算 $HW$ 可減少電路成本。
- 用 [amplitude encoding](../concepts/data-encoding.md) 把 $N$ 個值放進 $\log_2 N$ 個 qubit。

## 文獻怎麼說

- [S2] 既有量子 GCN 不是只實作權重矩陣（無法抽取圖結構特徵），就是以古典計算處理鄰接矩陣（易成為效能瓶頸）。[作者分析]
- [S2] 在 128～1024 節點的 Cora 子集二分類上，QuGCN 準確率高於只有 VQC 的 QNN，作者據此認為 Givens rotation 成功把圖結構嵌入電路；整體準確率接近古典 GCN；以 Qiskit API 與 Torch-Quantum 實作，可在 IBM Qiskit Aer 模擬器上執行。[模擬實驗]
- [S2] 古典 GCN 層的準確率通常高於 hybrid QGNN，作者歸因於 barren plateau 限制了 VQC 可用的可訓練參數數量。[作者分析]
- [S2] 複雜度分析：特徵轉換部分古典為 $O(LND^2)$、QuGCN 為 $O(LN\log D)$；鄰接部分古典為 $O(L(E+N)D)$、QuGCN 為 $O(L\log^2 N\cdot ED)$。結論是在特徵維度上可得到指數級改善，但因多出的 $\log^2 N$ 而失去優勢。[作者分析] <!-- reviewed-claim -->
- [S2] 依作者的操作數比較，在 256 維特徵時，節點數少於 128 的圖 QuGCN 的操作數少於古典 GCN；作者也承認目前的 Givens rotation 實作「不是好的設計」。[作者分析]
- [S2] Givens rotation 的乘積與正規化鄰接矩陣的熱圖有相似的樣式（對角線、非零位置相同），差別在 Givens 乘積的非對角元素為反對稱。[模擬實驗]
- [S2] 對大型圖的可擴展性：qubit 需求隨節點數與特徵數以對數成長，因此在小規模 NISQ 裝置上也能表示較大的圖。[作者宣稱]

## 限制與批判

- 複雜度表中的量子成本**沒有計入 amplitude encoding 的態準備成本**；一般狀況下準備任意 amplitude-encoded 態本身就要約 $O(d)$ 個操作（見 [資料編碼](../concepts/data-encoding.md)）。[推論]
- 實驗是二分類、子集、模擬器，且沒有雜訊；與古典 GCN 的比較未說明調參公平性。
- Givens rotation 的旋轉角 $\theta$ 是**所有邊共用的超參數**，不是逐邊學習的權重。
- PDF 抽取（A1c）：雙欄排版使 Givens 矩陣與範例式 (5) 的正負號難以從文字判讀，本 Wiki 以標準 Givens 定義書寫，不照抄範例式。

## 相關頁面

- [QuGCN 模型頁](../models/qugcn-givens.md)
- [資料編碼](../concepts/data-encoding.md)
- [參數化量子電路與 VQA](../concepts/pqc-and-vqa.md)
- [圖與 GNN](../concepts/graph-and-gnn.md)
- 回到 [index](../index.md)
