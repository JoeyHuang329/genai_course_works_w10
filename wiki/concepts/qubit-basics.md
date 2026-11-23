---
title: Qubit 基礎（給資工生的版本）
type: concept
sources: [S2]
difficulty: 1
updated: 2026-11-23
---

## 一句話

一個 qubit 是長度為 2 的單位複數向量；$n$ 個 qubit 是長度 $2^n$ 的單位向量；量子閘是乘在這個向量上的 unitary 矩陣；量測則是依振幅平方抽樣。

## 直觀解釋

| 量子概念 | 資工類比 | 注意 |
|---|---|---|
| 狀態 $a\|0\rangle+b\|1\rangle$ | 向量 $(a,b)$，$\|a\|^2+\|b\|^2=1$ | 「同時是 0 和 1」只是比喻 |
| $n$ 個 qubit | 長度 $2^n$ 的向量 | 指數大的狀態空間 |
| 量子閘 | 乘上 unitary 矩陣（保長度的「旋轉」） | 所以**量子計算是線性的** |
| 參數化閘 $R_Y(\theta)$ | 2×2 旋轉矩陣，$\theta$ 可訓練 | 相當於神經網路的權重 |
| 糾纏 | 向量無法寫成各 qubit 向量的張量積 | 由 CNOT 等雙 qubit 閘產生 |
| 量測 | 以 $\|振幅\|^2$ 機率得到某個基底態 | 要估期望值必須**重複執行很多次**（shots） |

## 稍微正式一點

$n$ 個 qubit 的狀態可寫成 $|\psi\rangle=\sum_{i=0}^{2^n-1} x_i|i\rangle$，其中 $\sum_i|x_i|^2=1$。量子計算就是 $|\psi\rangle=\cdots U_2(\theta_2)U_1(\theta_1)|\psi_0\rangle$，每個 $U$ 是一個量子閘。

常用閘：
- $X$（NOT）：交換 $|0\rangle,|1\rangle$
- CNOT（CX）：控制 qubit 為 1 時對目標做 $X$
- $R_Y(\theta)$：繞 Y 軸旋轉，矩陣為 $\begin{pmatrix}\cos\frac\theta2&-\sin\frac\theta2\\ \sin\frac\theta2&\cos\frac\theta2\end{pmatrix}$
- 受控 $R_Y$（CRY）：控制 qubit 為 1 時才轉

## 文獻怎麼說

- [S2] 一個 qubit 是兩個基底態的線性組合，振幅為複數且平方和為 1；$n$ 個 qubit 以 $2^n$ 個複數振幅表示；量子閘可表示為 unitary 矩陣，量子計算即 qubit 狀態的轉換。[理論]
- [S2] 量子電路最後以讀出子電路量測，例如 Z 量測得到 $|0\rangle$ 的機率。[理論]

## 相關頁面

- [參數化量子電路與 VQA](pqc-and-vqa.md)
- [資料編碼](data-encoding.md)
- [Hamiltonian 與 Ising 模型](hamiltonian-and-ising.md)
- 回到 [index](../index.md)
