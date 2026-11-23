---
title: Wiki 索引（Index）
type: index
sources: []
difficulty: 1
updated: 2026-11-23
---

# 圖神經網路 × 量子電路 LLM Wiki — 索引

LLM 回答問題前先讀這頁。規則見 [CLAUDE.md](../CLAUDE.md)，變更紀錄見 [log](log.md)，名詞見 [glossary](glossary.md)。
**第一次來請先讀 [總覽](overview.md)。**

## 文獻（sources）

| 代號 | 頁面 | 一句話 |
|---|---|---|
| S1 | [Verdon et al. 2019](sources/S1-verdon-2019-qgnn.md) | 讓圖決定量子子系統之間的交互作用；QGRNN / QGCNN / QSGCNN |
| S2 | [Hu et al. 2022](sources/S2-hu-2022-qugcn.md) | 把 GCN 公式逐項搬上量子電路：amplitude encoding + Givens rotation + VQC |
| S3 | [Ryu et al. 2023](sources/S3-ryu-2023-materials.md) | 一原子一 qubit、一鍵一 EDU，預測分子 HOMO-LUMO gap |
| S4 | [Aktar et al. 2024](sources/S4-aktar-2024-expressibility.md) | 把量子電路當成圖，用古典 GNN 預測電路的 expressibility |
| S5 | [Ceschini et al. 2026](sources/S5-ceschini-2026-review.md) | QGNN 批判性回顧：分類法、utility vs. advantage、五大挑戰 |

## 概念（concepts）

**先備知識**

| 頁面 | 難度 | 一句話 | 主要來源 |
|---|---|---|---|
| [圖與 GNN](concepts/graph-and-gnn.md) | 1 | 節點反覆聚合鄰居資訊；GCN 公式 | S1 S2 S5 |
| [Qubit 基礎](concepts/qubit-basics.md) | 1 | 單位向量、unitary 閘、量測抽樣 | S2 |
| [參數化量子電路與 VQA](concepts/pqc-and-vqa.md) | 1 | 量子前向、古典更新的訓練迴圈 | S2 S4 |
| [Hamiltonian 與 Ising 模型](concepts/hamiltonian-and-ising.md) | 2 | 圖 → Hamiltonian → 電路 | S1 S5 |

**核心概念**

| 頁面 | 難度 | 一句話 | 主要來源 |
|---|---|---|---|
| [資料編碼](concepts/data-encoding.md) | 2 | 四種編碼與「qubit 少 ≠ 整體快」 | S2 S3 S5 |
| [排列不變性/等變性](concepts/permutation-equivariance.md) | 2 | 節點編號不該影響答案；1-WL | S1 S3 |
| [Expressibility](concepts/expressibility.md) | 2 | 電路能多均勻地鋪滿狀態空間（KL 散度） | S4 |
| [Barren plateau](concepts/barren-plateau.md) | 2 | 梯度隨 qubit 數指數消失 | S1 S2 S3 S5 |
| [把量子電路看成圖](concepts/circuits-as-graphs.md) | 1 | 閘 = 節點、qubit 線 = 邊 | S4 |

**評價與統整**

| 頁面 | 難度 | 一句話 | 主要來源 |
|---|---|---|---|
| [QGNN 分類法](concepts/qgnn-taxonomy.md) | 2 | Fully / Hybrid / Quantum-assisted | S5 |
| [Advantage / Utility / Quantum-inspired](concepts/advantage-vs-utility.md) | 1 | 三種強度不同的「量子比較好」 | S5 |
| [QGNN 的五大挑戰](concepts/qgnn-challenges.md) | 2 | 雜訊、擴展、保證、高原、初始化 | S5 |

## 模型（models）

| 頁面 | 來源 | 難度 | 一句話 |
|---|---|---|---|
| [QGNN 通用 ansatz、QGRNN、QGCNN](models/qgnn-general-ansatz.md) | S1 | 2 | 由圖決定形狀的 Hamiltonian 演化 + 兩種參數綁定 |
| [QSGCNN](models/qsgcnn.md) | S1 | 3 | 連續變數版本，演化中出現圖 Laplacian |
| [QuGCN](models/qugcn-givens.md) | S2 | 2 | 一條邊 = 一次 Givens rotation（$R_Y$） |
| [EDU-QGC](models/edu-qgc.md) | S3 | 3 | 對稱的雙 qubit 閘構成天生等變的量子圖電路 |
| [GNN expressibility 預測器](models/gnn-expressibility-predictor.md) | S4 | 2 | 古典 graph transformer 讀電路圖、預測 expressibility |

## 綜合（syntheses）

| 頁面 | 一句話 |
|---|---|
| [圖與量子電路的四種結合方式](syntheses/graph-to-circuit-mappings.md) | S1–S4 的並排比較表 |

## 輔助頁

- [總覽](overview.md)・[名詞表](glossary.md)・[維護紀錄](log.md)
