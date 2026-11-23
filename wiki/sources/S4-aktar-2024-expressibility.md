---
title: S4｜Aktar et al. 2024 — 用 GNN 估計參數化量子電路的 Expressibility
type: source
sources: [S4]
difficulty: 2
updated: 2026-11-23
---

## 書目

S. Aktar, A. Bärtschi, D. Oyen, S. Eidenbenz, A.-H. A. Badawy. *Graph Neural Networks for Parameterized Quantum Circuits Expressibility Estimation*. arXiv:[2405.08100](https://arxiv.org/abs/2405.08100), 2024。作者來自 New Mexico State University 與 Los Alamos National Laboratory。

## 一句話

把量子電路畫成一張圖（閘 = 節點、qubit 線上的先後 = 邊），用古典的圖神經網路直接預測這個電路的 [expressibility](../concepts/expressibility.md)，省掉每個電路數千次的抽樣計算。

## 這篇在做什麼

1. **問題**：選電路結構（ansatz）時，expressibility 是重要指標，但要對每個電路抽數千組參數、算 fidelity 分布，非常昂貴；而且在含雜訊的硬體上數值還會改變。
2. **方法**：[電路 → 圖](../concepts/circuits-as-graphs.md)，再用 graph transformer 迴歸 expressibility，見 [GNN expressibility 預測器](../models/gnn-expressibility-predictor.md)。
3. **資料**：隨機產生 1～10 qubit 的電路，真值以 5,000 次 fidelity 抽樣計算。
4. **評估**：隨機電路測試集、文獻中的 19 個參考電路、Qiskit 的 RealAmplitudes 電路、對更多 qubit 的外插、5 個電路在真實 IBM 硬體上的比較。

## 重點

- 和本 Wiki 其他文獻的方向相反：S1–S3 是「用量子電路處理圖」，S4 是「用圖神經網路分析量子電路」。兩者都屬於「圖 × 量子電路」的交集。
- 模型輸入不只電路結構，還包括**硬體雜訊資訊**（每個 qubit 的 T1/T2、閘錯誤率、讀出錯誤），讓同一個電路在不同裝置上可以有不同的預測。
- 除了節點特徵，還加入電路的**全域特徵**（深度、參數化閘數、單 qubit 閘數等），作者顯示它們能降低誤差。

## 文獻怎麼說

- [S4] 直接計算 expressibility 需要大量 fidelity 樣本，例如 Sim et al. 的實驗對 4 qubit 電路使用 5,000 個樣本；裝置雜訊也會影響數值。[引述]
- [S4] 資料集：1～8 qubit 各 3,000 個、9 與 10 qubit 各 500 個，共 25,000 個隨機電路在無雜訊 QASM 模擬器上計算；另在 3 個 IBM Fake 後端（FakeGuadalupe、FakeMumbai、FakeHanoi，以真實裝置雜訊模型模擬）各收集 4,000 個，共 12,000 個。[模擬實驗]
- [S4] 測試集 RMSE 約 0.05（無雜訊）與 0.06（含雜訊後端）；在 19 個參考電路與 Qiskit RealAmplitudes 電路上，無雜訊 RMSE 分別為 0.05 與 0.06、含雜訊平均約 0.07 與 0.08。[模擬實驗]
- [S4] 外插：只用 ≤3 qubit 電路訓練時，對 6 與 10 qubit 電路的 RMSE 升到 0.22 與 0.3；用 ≤8 qubit 訓練時，對 10 qubit 電路的 RMSE 為 0.05；從「≤5 qubit」的模型開始外插表現就良好。[模擬實驗]
- [S4] 在真實 IBM Hanoi 硬體上量測 5 個參考電路的 expressibility，用 3 個 Fake 後端資料一起訓練的模型 RMSE 約 0.1，只用 FakeHanoi 資料訓練的約 0.19；作者據此認為跨雜訊水準訓練有助於真實硬體上的預測。[硬體實驗]
- [S4] 電路深度、參數數量、單 qubit 閘數與 expressibility 值呈負相關（值越小代表越有表達力）；加入全域特徵可在所有後端降低 RMSE。[模擬實驗]
- [S4] 作者宣稱此方法可大幅降低 fidelity 分布估計的計算成本，提供在模擬器與硬體上有效評估各種 PQC 的方法。[作者宣稱]

## 限制與批判

- 「含雜訊」的大部分資料來自 **Fake 後端（模擬雜訊）**，真實硬體只有 5 個電路，且其中某些電路的預測誤差相當大（例如真機 0.280，Fake 訓練模型預測 0.497）。
- 訓練資料是**隨機產生**的電路；對實際應用中常見的結構化 ansatz，泛化能力只用兩組參考電路驗證。
- 真值本身是用 5,000 次抽樣、bin 數 75 的直方圖估計的 KL 散度，也有估計誤差。[推論]

## 相關頁面

- [Expressibility](../concepts/expressibility.md)
- [把量子電路看成圖](../concepts/circuits-as-graphs.md)
- [GNN expressibility 預測器](../models/gnn-expressibility-predictor.md)
- [參數化量子電路與 VQA](../concepts/pqc-and-vqa.md)
- 回到 [index](../index.md)
