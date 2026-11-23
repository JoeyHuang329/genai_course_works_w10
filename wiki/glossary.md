---
title: 名詞表（Glossary）
type: glossary
sources: []
difficulty: 1
updated: 2026-11-23
---

# 名詞表

中英對照，依英文字母排序。詳細說明請點連結。回到 [index](index.md)。

| 英文 | 中文 | 一句話 | 頁面 |
|---|---|---|---|
| Amplitude encoding | 振幅編碼 | $d$ 維向量放進 $\log_2 d$ 個 qubit 的振幅 | [data-encoding](concepts/data-encoding.md) |
| Ansatz | 擬設（電路結構） | 參數化量子電路的「架構設計」，相當於神經網路的 architecture | [QGNN 通用 ansatz](models/qgnn-general-ansatz.md) |
| Angle encoding | 角度編碼 | 一個特徵值 → 一個旋轉角 | [data-encoding](concepts/data-encoding.md) |
| Basis encoding | 基底編碼 | 二進位資料 → 計算基底態 | [data-encoding](concepts/data-encoding.md) |
| Barren plateau | 貧瘠高原 | 梯度隨 qubit 數變多而消失 | [barren-plateau](concepts/barren-plateau.md) |
| CNOT (CX) | 受控反閘 | 控制 qubit 為 1 時翻轉目標 qubit | [qubit-basics](concepts/qubit-basics.md) |
| EDU | 等變可對角化 unitary | $(V^\dagger\otimes V^\dagger)D(V\otimes V)$，交換兩節點不變的雙 qubit 閘 | [EDU-QGC](models/edu-qgc.md) |
| Equivariant QGNN | 等變量子圖神經網路 | 電路結構保證排列對稱的 QGNN | [qgnn-taxonomy](concepts/qgnn-taxonomy.md) |
| Expressibility | 表達能力 | 電路 fidelity 分布與 Haar 分布的 KL 散度，越小越有表達力 | [expressibility](concepts/expressibility.md) |
| Fidelity | 保真度／重疊 | 兩個量子態有多像，$\lvert\langle\psi\vert\phi\rangle\rvert^2$ | [expressibility](concepts/expressibility.md) |
| Fully Quantum / Hybrid / Quantum-Assisted GNN | 全量子／混合／量子輔助 GNN | 依量子電路角色分的三類 QGNN | [qgnn-taxonomy](concepts/qgnn-taxonomy.md) |
| GCN | 圖卷積網路 | 用正規化鄰接矩陣做鄰居平均的 GNN | [graph-and-gnn](concepts/graph-and-gnn.md) |
| GHZ state | GHZ 態 | 多個 qubit「全 0 或全 1」的糾纏態，可提升感測靈敏度 | [S1](sources/S1-verdon-2019-qgnn.md) |
| Givens rotation | Givens 旋轉 | 只在兩個座標軸平面上旋轉的矩陣；2×2 核心即 $R_Y$ | [QuGCN](models/qugcn-givens.md) |
| Haar random | Haar 隨機 | 在狀態空間上「完全均勻」的隨機態分布 | [expressibility](concepts/expressibility.md) |
| Hamiltonian encoding | Hamiltonian 編碼 | 把圖的邊放進交互作用項 | [data-encoding](concepts/data-encoding.md) |
| Graph isomorphism | 圖同構 | 兩張圖只差在節點編號（重新編號後邊完全相同） | [QSGCNN](models/qsgcnn.md) |
| HOMO-LUMO gap | 前沿軌域能隙 | 分子最高佔據與最低未佔據軌域的能量差 | [S3](sources/S3-ryu-2023-materials.md) |
| Graph Laplacian | 圖拉普拉斯矩陣 | 度數矩陣減鄰接矩陣，$L=D-A$ | [QSGCNN](models/qsgcnn.md) |
| Hamiltonian | 哈密頓量 | 描述能量與時間演化的 Hermitian 矩陣 | [hamiltonian-and-ising](concepts/hamiltonian-and-ising.md) |
| Ising model | Ising 模型 | 圖上每節點一個自旋、每條邊一個 $ZZ$ 交互作用 | [hamiltonian-and-ising](concepts/hamiltonian-and-ising.md) |
| Master node | 主節點 | 連到所有節點的虛擬節點，模擬長距離交互作用 | [S3](sources/S3-ryu-2023-materials.md) |
| Message passing | 訊息傳遞 | 節點收集鄰居資訊並更新自己 | [graph-and-gnn](concepts/graph-and-gnn.md) |
| MPNN | 訊息傳遞神經網路 | message passing 框架下的 GNN 總稱 | [graph-and-gnn](concepts/graph-and-gnn.md) |
| NISQ | 含雜訊中等規模量子 | 目前的量子硬體世代：qubit 少、有雜訊、無完整糾錯 | [pqc-and-vqa](concepts/pqc-and-vqa.md) |
| Over-smoothing | 過度平滑 | GNN 層數多時節點表示趨於相同 | [graph-and-gnn](concepts/graph-and-gnn.md) |
| Parameter-shift rule | 參數平移法則 | 在量子硬體上估計梯度的方法 | [qgnn-challenges](concepts/qgnn-challenges.md) |
| Permutation equivariance | 排列等變性 | 節點重新編號，輸出跟著重排 | [permutation-equivariance](concepts/permutation-equivariance.md) |
| QRAM | 量子隨機存取記憶體 | 假設能高效載入資料的量子記憶體，目前不存在實用版本 | [advantage-vs-utility](concepts/advantage-vs-utility.md) |
| QGCNN / QGRNN | 量子圖卷積/遞迴網路 | 跨節點／跨迭代綁定參數的 QGNN | [QGNN 通用 ansatz](models/qgnn-general-ansatz.md) |
| QSGCNN | 量子頻譜圖卷積網路 | 連續變數版 QGCNN | [QSGCNN](models/qsgcnn.md) |
| Quantum advantage / utility / inspired | 量子優勢／實用效益／量子啟發 | S5 定義的三級宣稱強度 | [advantage-vs-utility](concepts/advantage-vs-utility.md) | <!-- reviewed-claim -->
| Qubit | 量子位元 | 長度 2 的單位複數向量 | [qubit-basics](concepts/qubit-basics.md) |
| Readout function | 讀出函數 | 把量測結果組成模型輸出，需對節點排列不變 | [EDU-QGC](models/edu-qgc.md) |
| Shots | 取樣次數 | 為估計期望值而重複執行電路的次數 | [qubit-basics](concepts/qubit-basics.md) |
| QM9 | QM9 資料集 | 最多 9 個重原子的有機小分子資料集，性質由 DFT 計算 | [S3](sources/S3-ryu-2023-materials.md) |
| Spectral clustering | 譜聚類 | 用圖 Laplacian 的低頻特徵向量把節點分群 | [QSGCNN](models/qsgcnn.md) |
| T1 / T2 | 弛豫／退相干時間 | qubit 能保持狀態多久的硬體參數 | [circuits-as-graphs](concepts/circuits-as-graphs.md) |
| Trotterization | Trotter 分解 | 把 $e^{-it(A+B)}$ 近似成交替小步 | [hamiltonian-and-ising](concepts/hamiltonian-and-ising.md) |
| 1-WL test | 1 維 Weisfeiler–Lehman 測試 | 衡量圖模型區分能力的基準 | [permutation-equivariance](concepts/permutation-equivariance.md) |
| VQE / QAOA | 變分量子本徵求解器／量子近似最佳化 | 兩種代表性的 VQA | [pqc-and-vqa](concepts/pqc-and-vqa.md) |
| VQA / VQC / PQC | 變分量子演算法／電路 | 量子前向 + 古典最佳化的可訓練電路 | [pqc-and-vqa](concepts/pqc-and-vqa.md) |
