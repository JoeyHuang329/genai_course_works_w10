---
title: 表達能力（Expressibility）
type: concept
sources: [S4]
difficulty: 2
updated: 2026-11-23
---

## 一句話

一個參數化量子電路隨機取參數時，產生的量子態能多「均勻地」鋪滿整個狀態空間；越均勻，代表這個電路結構能表示的東西越多。

## 直觀解釋

- 想像狀態空間是一顆球的表面。好的電路隨便轉轉旋鈕，打出去的點應該**散佈在整顆球上**；差的電路打出去的點都**擠在一小塊**。
- 怎麼量「散佈得多均勻」？隨機抽兩組參數產生兩個態，看它們有多像（fidelity，重疊程度）。重複很多次，得到一個「相似度的分布」。
- 拿這個分布和**完全隨機的態**（Haar random）的相似度分布比較：越接近，電路越有表達力。
- 注意方向：**數值越小 = 越有表達力**（因為它是「差距」）。

## 稍微正式一點

$$\text{Expr} = D_{KL}\!\left(P_{\text{PQC}}(F;\boldsymbol\theta)\;\middle\|\;P_{\text{Haar}}(F)\right), \qquad P_{\text{Haar}}(F) = (N-1)(1-F)^{N-2}$$

| 符號 | 意義 | 用途 |
|---|---|---|
| $F = \lvert\langle\psi_{\boldsymbol\theta}\vert\psi_{\boldsymbol\phi}\rangle\rvert^2$ | 兩組隨機參數 $\boldsymbol\theta,\boldsymbol\phi$ 產生的兩個態的重疊（fidelity），介於 0～1 | 量「兩個態有多像」 |
| $P_{\text{PQC}}(F;\boldsymbol\theta)$ | 對這個電路反覆抽參數，得到的 $F$ 的經驗分布（直方圖） | 這個電路的「指紋」 |
| $P_{\text{Haar}}(F)$ | 完全隨機（Haar 分布）的態之間 $F$ 的分布，有解析解 | 「最有表達力」的參考標準 |
| $N$ | 狀態空間維度，$n$ 個 qubit 時 $N=2^n$ | qubit 越多，隨機態越不像彼此，分布越集中在 $F\approx 0$ |
| $D_{KL}(P\Vert Q)$ | KL 散度：兩個分布的差距 | 越小越接近 Haar → 越有表達力 |

**實際怎麼量 $F$？** 把電路 $U(\boldsymbol\theta)$ 接上 $U(\boldsymbol\phi)^\dagger$（反向電路），從 $|0\cdots0\rangle$ 出發，量到 $|0\cdots0\rangle$ 的機率就是 $F$。

## 文獻怎麼說

- [S4] Expressibility 定義為 PQC 的 fidelity 分布與 Haar 隨機態 fidelity 分布之間的 KL 散度，值越低代表越接近最大表達力的集合；此定義來自 Sim et al.（S4 引用）。[引述]
- [S4] 實作：將電路轉譯成目標裝置的原生閘，把第二組參數的反向電路接在第一個電路後，從 $|0\rangle^{\otimes n}$ 出發執行 5,000 次得到 fidelity 分布，Haar 分布以解析式計算，以 75 個 bin 的直方圖算 KL 散度。[模擬實驗]
- [S4] 裝置雜訊會改變同一個電路的 expressibility，影響變分演算法在不同後端上的表現。[模擬實驗]
- [S4] 增加電路重複層數一般會提升 expressibility（數值下降）。[模擬實驗]

## 常見誤解

- 「Expressibility 越高越好」：表達力太高的電路常常也更難訓練（梯度更平），兩者需要取捨；本 Wiki 的 S4 只處理「怎麼便宜地估計它」，沒有討論這個取捨。[推論]

## 相關頁面

- [參數化量子電路與 VQA](pqc-and-vqa.md)
- [Barren plateau](barren-plateau.md)
- [GNN expressibility 預測器](../models/gnn-expressibility-predictor.md)
- 回到 [index](../index.md)
