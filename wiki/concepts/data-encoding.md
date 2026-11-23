---
title: 資料編碼（Quantum Data Encoding）
type: concept
sources: [S2, S3, S5]
difficulty: 2
updated: 2026-11-23
---

## 一句話

古典資料（節點特徵、圖結構）要先「載入」成量子態，量子電路才能處理；載入方式決定了要用多少 qubit、多深的電路。

## 直觀解釋

- **Angle encoding**：一個數字 → 一個旋轉角。直觀、便宜，但一個特徵大約佔一個 qubit。
- **Amplitude encoding**：整個向量 → 狀態向量的振幅。$d$ 維只需約 $\log_2 d$ 個 qubit，非常省 qubit。
- **Basis encoding**：二進位資料 → 對應的計算基底態（例如 101 → $|101\rangle$）。適合類別型特徵。
- **Hamiltonian encoding**：不把數字放進態，而是把**圖的邊**放進 Hamiltonian 的交互作用項，讓圖結構決定電路的形狀。這是 QGNN 最自然的做法（見 [QGNN 通用 ansatz](../models/qgnn-general-ansatz.md)）。

| 編碼 | qubit 數 | 準備成本 | 優點 | 缺點 | 本 Wiki 例子 |
|---|---|---|---|---|---|
| Angle | 約 $O(d)$（可用 re-uploading 換深度） | $O(d)$ 個旋轉閘 | 硬體友善、最常用 | qubit 多 | S3 |
| Basis | 依位元數 | 低 | 適合類別/二元特徵 | 連續值需離散化 | — |
| Amplitude | $O(\log d)$ | 一般為 $O(d)$ | 極省 qubit | 省下的 qubit 可能被準備成本吃掉 | S2 |
| Hamiltonian | 約 $O(\|V\|)$ | 每層約 $O(\|E\|)$ 個雙 qubit 操作 | 直接表示圖結構 | 稠密圖成本高 | S1、S3 |

> **最重要的批判觀念**：qubit 少 ≠ 整體快。把 $d$ 個數字放進振幅，一般就要做約 $d$ 次操作，除非假設有 QRAM 之類的特殊硬體。

## 稍微正式一點

Amplitude encoding：給 $x\in\mathbb{R}^N$，先正規化使 $\sum_i|x_i|^2=1$，若 $N<2^n$ 補 0，得到 $|\psi\rangle=\sum_i x_i|i\rangle$。

## 文獻怎麼說

- [S2] QuGCN 以 amplitude encoding 做節點與特徵的態準備：對第 $j$ 維特徵，把 $N$ 個節點的值以 L2 正規化後放進振幅，不足 $2^n$ 的位置補 0，共 $d$ 個量子電路。[理論]
- [S5] 編碼方式的選擇對 VQC 表現影響很大，且是取得量子優勢的必要前提；angle encoding 是編碼連續變數最常用且有效的方法。[作者分析] <!-- reviewed-claim -->
- [S5] amplitude encoding 只需 $O(\log d)$ 個 qubit，但一般任意態的準備需要 $O(d)$ 個操作，除非假設高效態準備、QRAM 或 oracle 存取；因此其 qubit 效率不自動代表端到端的量子優勢。[理論] <!-- reviewed-claim -->
- [S5] Hamiltonian encoding 對 QGNN 特別重要，因為圖拓撲可以直接編碼成 Hamiltonian 的交互作用項或依圖而定的 unitary 演化。[作者分析]
- [S3] EDU-QGC 以 angle encoding 為每個原子編碼一個 qubit：先 $R_Y$ 再 $R_Z$，旋轉角由原子序、鍵結氫數等特徵決定；例如只用原子序時，4 種原子被放在 Bloch 球內接正四面體的 4 個頂點，彼此盡量分開。[理論]
- [S3] 量子編碼方式常是經驗且任意的；以可訓練的古典小網路輸出旋轉角（neural-network-assisted encoding）可改善表現。[模擬實驗]
- [S3] data re-uploading（每層後重新編碼一次）理論上能提升表達力，但在 QM9 實驗中 test loss 反而略差。[模擬實驗]

## 相關頁面

- [QGNN 的挑戰](qgnn-challenges.md)
- [Advantage / Utility](advantage-vs-utility.md)

- [EDU-QGC](../models/edu-qgc.md)

- [Qubit 基礎](qubit-basics.md)
- [QuGCN](../models/qugcn-givens.md)
- 回到 [index](../index.md)
