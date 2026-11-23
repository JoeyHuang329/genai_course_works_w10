---
title: EDU-QGC（Equivariantly Diagonalizable Unitary Quantum Graph Circuit）
type: model
sources: [S3, S5]
difficulty: 3
updated: 2026-11-23
---

## 一句話

由「節點層」與「連結層」交替組成的量子圖電路；連結層的每個雙 qubit 閘（EDU）都特別設計成**交換兩個節點也不變**，所以整個電路天生具有排列等變性。

## 直觀解釋

- **一個節點 = 一個 qubit**（在 S3 中是一個重原子）。
- **節點層**：每個 qubit 各自做一次單 qubit 旋轉（所有節點用同一組參數）→ 像「節點更新」。
- **連結層**：每條邊上放一個 EDU 作用在兩端的 qubit → 像「訊息傳遞」。
- **EDU 的長相**：「先把兩個 qubit 各自轉到某個座標系（$V\otimes V$）→ 做一個只改相位的雙 qubit 閘（$D$）→ 再轉回來（$V^\dagger\otimes V^\dagger$）」。因為兩邊用的是**同一個** $V$，對調兩個 qubit 結果不變。
- **讀出**：把所有 qubit 的量測平均起來 → 與節點順序無關。

## 稍微正式一點

$$\text{EDU} = (V^\dagger \otimes V^\dagger)\; D\; (V \otimes V)$$

| 符號 | 意義 | 用途 |
|---|---|---|
| $V$ | 單 qubit unitary；S3 預設是 3 參數的任意單 qubit 閘，簡化版只用 $R_Y$ | 決定「在哪個基底下交互作用」；**依鍵的種類**有不同參數 |
| $V\otimes V$ | 兩個 qubit 用**同一個** $V$ | 對稱 → 交換兩節點不變 |
| $D$ | 對角的雙 qubit 閘，S3 使用 $R_{ZZ}(\phi)=e^{-i\phi Z\otimes Z/2}$ | 真正產生交互作用（糾纏）的部分；$\phi$ **依層數**而定 |
| $V^\dagger\otimes V^\dagger$ | 轉回原座標系 | 讓 EDU 可被「同時對角化」 |

**讀出函數**（$r_0,r_1,r_2$ 可訓練，因為期望值被限制在 $[-1,1]$ 需要縮放）：
- Local：$r_0 + \frac{r_1}{|V|}\sum_{v}\langle Z_v\rangle$
- Global：再加上 $r_2\langle\bigotimes_v Z_v\rangle$

**工程上的麻煩**：參數不同的 EDU 一般不可交換，套用順序不同結果就不同 → 破壞等變性。S3 的解法是**強制排序**：同一種鍵的 EDU 一起套用（先單鍵，再雙鍵……）。同一層內所有 EDU 共用 $D$ 的角度，但 $V$ 依鍵的種類而異。

## 文獻怎麼說

- [S3] EDU 與 SWAP 及其他 qubit 上的自身複本可交換，因此連結層對節點排列等變；EDU-QGC 也可以表示成 EHQGC（以圖拓撲 Hamiltonian 構成的等變電路）。[理論]
- [S3] EDU-QGC 可近似有界圖上的任意實值函數，並可通過 1-WL 測試，而決定性的古典 MPNN 無法通過（S3 引用 Mernyei et al. 的結果）。[引述]
- [S3] 為了處理離散的鍵種類，EDU 的單 qubit 部分以依鍵種類而定的可訓練變數參數化，對角部分以依層數而定的變數參數化，並強制 EDU 的套用順序以維持等變。[理論]
- [S3] 預設 EDU（3 參數單 qubit 閘）比簡化 EDU（只用 $R_Y$）的 test MSE 低（$5.88$ vs. $9.82$，單位 $10^{-4}$ Ha²），顯示 EDU 的表達力影響模型表現。[模擬實驗]
- [S3] 節點編碼與節點運算可在所有 qubit 上平行執行；連結層的時間成本與圖的邊著色數成正比，作者認為至多與節點數線性相關，依連接性可能優於 MPNN 的成本。[作者分析]
- [S5] Equivariant QGNN 中有兩種主要實作：以圖拓撲 Hamiltonian 構成的 EHQGC，與由 S3 提出、以局部與對角 unitary 組成雙節點 EDU 的 EDU-QGC；這類模型的電路規模大，多半只能處理小圖。[作者分析]
- [S5] S3 對量子模型只做一次訓練、初始權重全為 1，而古典模型做了 3 次不同初始化，此評估方式需要進一步說明。[作者分析]

## 常見誤解

- 「通過 1-WL 就代表一定比古典 GNN 準」：1-WL 測的是**區分不同圖的能力上限**，不是在特定資料集上的預測誤差。S3 的實驗中 SOTA 古典模型仍然準很多。[推論]

- 「通過 1-WL」在這裡的意思是：能區分某些 1-WL 測試（以及決定性 MPNN）分不出來的圖。[推論]

## 相關頁面

- [QGNN 分類法](../concepts/qgnn-taxonomy.md)
- [QGNN 的挑戰](../concepts/qgnn-challenges.md)

- [S3 文獻頁](../sources/S3-ryu-2023-materials.md)
- [排列不變性/等變性](../concepts/permutation-equivariance.md)
- [QGNN 通用 ansatz](qgnn-general-ansatz.md)（EHQGC 與其相似）
- 回到 [index](../index.md)
