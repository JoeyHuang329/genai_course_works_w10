---
title: Hamiltonian 與 Ising 模型（Hamiltonian & Ising Model）
type: concept
sources: [S1, S5]
difficulty: 2
updated: 2026-11-23
---

## 一句話

Hamiltonian 是描述「一個量子系統的能量、以及它怎麼隨時間演化」的矩陣；Ising 模型是最簡單的「圖上的 Hamiltonian」：每個節點一個自旋（qubit），每條邊一個交互作用項。

## 直觀解釋

- 對資工生來說，可以先把 **Hamiltonian $\hat H$** 想成一個 Hermitian 矩陣（$\hat H = \hat H^\dagger$）。
- 讓系統「跑時間 $t$」，就是對狀態乘上 $e^{-i t \hat H}$。這個矩陣指數一定是 unitary，所以可以當成量子電路的一部分。
- 如果 $\hat H$ 是由「邊上的兩兩交互作用」加總而成，那 $e^{-it\hat H}$ 就是一個**形狀由圖決定**的運算。這是 QGNN 的核心直覺：**圖 → Hamiltonian → 電路**。
- **Ising 模型**：每個節點 $v$ 一個 qubit；邊 $(j,k)$ 上的項 $J_{jk} Z_j Z_k$ 代表「兩個自旋想要同向或反向」；節點上的項代表外加磁場。

## 稍微正式一點

S1 實驗中的目標 Hamiltonian（帶橫場的 Ising 模型）：

$\hat H = \sum_{\{j,k\}\in E} J_{jk}\, \hat Z_j \hat Z_k + \sum_{v\in V} Q_v\, \hat Z_v + \sum_{v\in V} \hat X_v$

- $\hat Z_j$、$\hat X_v$：作用在單一 qubit 上的 Pauli 矩陣（2×2）。
- $J_{jk}$：邊的耦合強度（相當於圖的邊權重）；$Q_v$：節點偏置。
- 當各項不可交換時，$e^{-it(\hat H_1+\hat H_2)}$ 不能直接拆開，常用 **Trotter 分解** 近似：$\big(e^{-i\Delta \hat H_1}e^{-i\Delta \hat H_2}\big)^{t/\Delta}$，也就是「小步交替跑」。QGRNN 就是這樣的結構。

## 文獻怎麼說

- [S1] 以帶橫場 Ising Hamiltonian 為目標，QGRNN 從量測到的時間演化資料學回 $J_{jk}$ 與 $Q_v$。[模擬實驗]
- [S1] QGRNN 的參數綁定方式使其可視為有效 Hamiltonian $\hat H_{\text{eff}}$ 的 Trotter 化模擬，時間步長 $\Delta=\sum_q|\eta_q|$。[理論]
- [S5] Ising 模型的交互作用項可對應圖的邊，因此 Ising Hamiltonian 可用來表示圖的鄰接結構，是 QGNN 處理圖資料的自然框架；QAOA 與 VQE 等求解 Ising 型問題的演算法也可改用於 QGNN 訓練。[作者分析]

## 相關頁面

- [資料編碼](data-encoding.md)（Hamiltonian encoding）

- [QGNN 通用 ansatz、QGRNN、QGCNN](../models/qgnn-general-ansatz.md)
- [Qubit 基礎](qubit-basics.md)
- 回到 [index](../index.md)
