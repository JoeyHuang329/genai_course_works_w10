---
title: 參數化量子電路與變分量子演算法（PQC / VQC / VQA）
type: concept
sources: [S2, S4]
difficulty: 1
updated: 2026-11-23
---

## 一句話

參數化量子電路（PQC，也叫 VQC 或 QNN）是「可訓練的量子層」：量子電腦負責前向計算與量測，古典電腦負責根據 loss 更新參數，兩者交替迭代。

## 直觀解釋

```
 古典資料 x ──► [編碼 U(x)] ──► [可訓練 W(θ)] ──► [量測 M] ──► 輸出 ──► loss
                                     ▲                                │
                                     └──── 古典最佳化器更新 θ ◄────────┘
```

1. **編碼 $U(x)$**：把古典資料放進量子態（見 [資料編碼](data-encoding.md)）。
2. **計算單元 $W(\theta)$**：一排旋轉閘（如 $R_Y(\theta_i)$）+ 糾纏閘（如 CNOT），通常重複數次。這個結構稱為 **ansatz**。
3. **量測 $M$**：讀出結果，接上 activation 或直接算 loss。
4. **古典最佳化**：更新 $\theta$，回到步驟 1。

這個「量子前向、古典更新」的流程叫 **VQA（Variational Quantum Algorithm）**，被視為目前含雜訊的中等規模量子電腦（NISQ）最實際的用法。

## 稍微正式一點

輸出 $f(x,\theta)=\langle 0|U(x)^\dagger W(\theta)^\dagger\, M\, W(\theta)U(x)|0\rangle$，訓練目標為最小化 $C(f(x,\theta))$。

## 文獻怎麼說

- [S2] VQC 由編碼單元 $U(x)$、含可訓練參數的計算單元 $W(\theta)$、量測子電路 $M$ 組成；量測結果常接上類似古典神經網路的 activation 以完成分類等任務。[理論]
- [S4] VQA 包含產生試驗態的 PQC、問題相關的 cost function、評估 cost 的量測，以及依量測結果調整參數的古典最佳化器；代表應用有 VQE（求量子系統基態能量）、QAOA（近似組合最佳化，如 Max-Cut）與量子機器學習。[引述]
- [S4] PQC 由固定閘與可訓練的單 qubit 旋轉閘（$R_X, R_Y, R_Z$）組成；其可調部分類似古典神經網路的權重與偏置；常見 ansatz 有 problem-inspired、hardware-efficient 與 variable-structure 三類。[引述]
- [S4] VQA 的表現高度依賴所選 PQC 的探索能力，設計「深度淺、參數精簡、又能涵蓋解空間」的 PQC 仍是一大挑戰；[expressibility](expressibility.md) 是評估指標之一。[作者分析]

## 相關頁面

- [Expressibility](expressibility.md)

- [Qubit 基礎](qubit-basics.md)
- [資料編碼](data-encoding.md)
- [Barren plateau](barren-plateau.md)
- [QuGCN](../models/qugcn-givens.md)
- 回到 [index](../index.md)
