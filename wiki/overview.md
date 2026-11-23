---
title: 總覽：圖神經網路 × 量子電路（Overview）
type: overview
sources: [S1, S2, S3, S4, S5]
difficulty: 1
updated: 2026-11-23
---

# 總覽

> 第一次來？照這個順序讀：本頁 → [圖與 GNN](concepts/graph-and-gnn.md) → [Qubit 基礎](concepts/qubit-basics.md) → [參數化量子電路](concepts/pqc-and-vqa.md) → [資料編碼](concepts/data-encoding.md) → 三個模型頁 → [Advantage vs. Utility](concepts/advantage-vs-utility.md)。

## 這個 Wiki 在講什麼

五篇文獻都落在「**量子計算**」、「**圖神經網路（GNN）**」與「**量子電路**」的交集上：

```
        圖神經網路（GNN）
             ╱    ╲
   用量子電路    用 GNN
   處理圖資料    分析量子電路
  (S1 S2 S3 S5)     (S4)
             ╲    ╱
          量子電路 / 量子計算
```

- **方向一：用量子電路處理圖**——也就是量子圖神經網路（QGNN）。核心問題是「圖的結構要怎麼放進量子電路」。S1 讓圖決定 Hamiltonian 的交互作用；S2 用 Givens rotation 模擬鄰接矩陣；S3 用對稱的雙 qubit 閘保證排列等變；S5 是這個方向的批判性回顧。
- **方向二：用 GNN 分析量子電路**——量子電路本身就是一張圖，S4 用古典 GNN 預測電路的 expressibility，幫忙挑選電路結構。

## 為什麼有人想把圖和量子放在一起

1. **古典 GNN 的瓶頸**：大圖上的 message passing 很貴，層數多會 over-smoothing。[S5]
2. **結構很像**：圖 = 節點 + 邊；量子系統 = qubit + 交互作用。Ising 模型就是「圖上的 Hamiltonian」。[S1][S5]
3. **量子電路難訓練**：沒有結構先驗的量子神經網路會遇到 barren plateau，用圖結構限制電路形狀是一種解法。[S1]
4. **量子原生的圖問題**：當圖本身描述的就是量子系統（量子感測網路、自旋系統），量子模型最自然。[S1][S5]

## 目前的現況（一句話版）

多數結果來自小規模**模擬**，展現的是 **quantum utility**（參數較少、收斂較快、準確率接近），而不是可證明的 **quantum advantage**；主要障礙是雜訊、qubit 數、資料載入成本與 barren plateau。[S5] 詳見 [QGNN 的挑戰](concepts/qgnn-challenges.md)。<!-- reviewed-claim -->

## 地圖

- 所有頁面：[index](index.md)
- 跨文獻比較表：[圖與量子電路的四種結合方式](syntheses/graph-to-circuit-mappings.md)
- 分類：[QGNN 分類法](concepts/qgnn-taxonomy.md)
