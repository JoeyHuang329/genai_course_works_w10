---
title: Quantum Advantage、Quantum Utility 與 Quantum-inspired
type: concept
sources: [S5, S2, S3]
difficulty: 1
updated: 2026-11-23
---

## 一句話

「量子模型表現不錯」不等於「量子比古典好」：S5 把宣稱分成三級，本 Wiki 一律照這三級用詞（裁決 B5）。

## 直觀解釋

| 用詞 | 白話 | 要滿足什麼 | 例子 |
|---|---|---|---|
| **Quantum advantage**（量子優勢） | 「量子**確定**贏了」 | 對手是**最強的**古典方法；在明確計算模型下可證明（時間/樣本/記憶體的漸進改善，或實測端到端加速）；成本要算**整條管線** | 目前 QGNN 尚無；QRAM 假設下的理論結果屬於容錯量子電腦情境 <!-- reviewed-claim --> |
| **Quantum utility**（量子實用效益） | 「量子**有些好處**」 | 準確率相近或略好、參數較少、收斂較快、更穩、適合量子原生資料 | S3：相近參數量下 test loss 較低 |
| **Quantum-inspired**（量子啟發） | 「借量子的**點子**，在古典電腦上跑」 | 不需要量子硬體 | 用量子漫步、張量網路、Hamiltonian 動力學設計的古典模型 |

**檢查一個宣稱的四個問題**：
1. 比較對象是誰？是不是最強的古典方法？
2. 成本算了哪些？資料載入、量測次數、訓練迭代有沒有算進去？
3. 是模擬還是真機？有沒有雜訊？
4. 實驗是否公平？（調參次數、初始化、資料切分）

## 文獻怎麼說

- [S5] quantum advantage 只用於在明確計算模型下、可證明勝過最佳古典對手的情況，且須計入編碼、態準備、電路評估、shots、最佳化、前後處理與 QRAM 或硬體連接性假設。[作者分析] <!-- reviewed-claim -->
- [S5] 目前多數 QGNN 結果，尤其在 NISQ 裝置上的，屬於 quantum utility。[作者分析]
- [S2] 作者的複雜度分析顯示特徵維度上有指數級改善，但鄰接部分多出 $\log^2 N$ 而失去優勢。[作者分析] <!-- reviewed-claim -->
- [S2] 該複雜度表未計入 amplitude encoding 的態準備成本；依 S5 的三分法，這個結果不能稱為 quantum advantage。[推論] <!-- reviewed-claim -->
- [S3] 相近參數量下 QGNN 的 test loss 低於本文的古典 baseline、收斂較快；但文獻中 SOTA 古典模型 ALIGNN 的誤差約低 10 倍。[作者分析]
- [S5] 分子化學領域的 QGNN（包括 S3）展現了利用幾何與對稱性的實用效益，但沒有任何案例達成真正的量子優勢。[作者分析] <!-- reviewed-claim -->

## 常見誤解

- 「qubit 少 = 比較快」：見 [資料編碼](data-encoding.md) 的 amplitude encoding 成本。
- 「模擬器上贏 = 真機上也贏」：模擬器沒有雜訊；而且精確模擬的記憶體需求隨 qubit 數指數成長，只能測小圖。

## 相關頁面

- [S5 文獻頁](../sources/S5-ceschini-2026-review.md)
- [QGNN 分類法](qgnn-taxonomy.md)
- [QGNN 的挑戰](qgnn-challenges.md)
- [S3 文獻頁](../sources/S3-ryu-2023-materials.md)
- 回到 [index](../index.md)
