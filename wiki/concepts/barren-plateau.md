---
title: 貧瘠高原（Barren Plateau）
type: concept
sources: [S1, S2, S3, S5]
difficulty: 2
updated: 2026-11-23
---

## 一句話

參數化量子電路的 loss 地形在 qubit 數變多時會變得幾乎「完全平坦」，梯度小到測不出來，訓練卡死。

## 直觀解釋

想像在一片濃霧中的廣大平原找最低點：腳下的坡度小到感覺不出來，往哪走都一樣，所以永遠走不到山谷。

## 稍微正式一點

對參數 $\theta_k$ 的偏微分 $\partial_k C$：
- 期望值 $\mathbb{E}[\partial_k C]=0$
- 變異數 $\mathrm{Var}[\partial_k C]$ 隨 qubit 數 $n$ **指數遞減**

由 Chebyshev 不等式，梯度偏離 0 超過 $\epsilon$ 的機率 $\le \mathrm{Var}/\epsilon^2$，也就是**幾乎所有隨機起點的梯度都接近 0**。要分辨這麼小的梯度，需要的量測次數（shots）也跟著指數增加。

**和古典梯度消失的差別**：古典是「層數」變多才消失；量子是「qubit 數」變多就會發生。雜訊、global cost function 會讓它更嚴重。

**對策**：local cost function、免梯度最佳化、逐層訓練、好的初始化、帶結構先驗的架構（例如 S1 的參數綁定、等變電路）。

## 文獻怎麼說

- [S1] 沒有結構先驗的量子神經網路，以梯度下降訓練會指數級困難；這是設計 QGRNN、QGCNN 等參數綁定架構的動機（S1 引用其參考文獻 [4]）。[引述]
- [S5] barren plateau 中 cost function 梯度的期望值為 0、變異數隨 qubit 數指數遞減，使梯度在數值精度下與 0 無法區分，最佳化停滯；這限制了 VQA 隨系統大小擴展。[理論]
- [S5] 與古典 NN 隨層數增加而梯度消失不同，QNN 隨 qubit 數增加更普遍地遇到此問題；雜訊與 cost function 設計會使其惡化，即使用免梯度最佳化也可能受影響。[作者分析]
- [S5] EQGC（等變量子圖電路）被觀察到較不易出現 barren plateau，但證據只來自 6～10 qubit 的電路，需要更多驗證（S5 引用 Mernyei et al.）。[引述]
- [S5] Ryu et al.（S3）比較了 local 與 global 讀出，local 較好的一個可能原因是 global 讀出更容易遇到 barren plateau，但差異很小、對理解 QGNN 的高原問題幫助有限。[作者分析]
- [S3] local 讀出（各 qubit $\langle Z\rangle$ 平均）的 test loss 優於 global 讀出，儘管 local 是 global 的特例。[模擬實驗]
- [S2] 在 Cora 子集實驗中，古典 GCN 層的準確率通常高於 hybrid QGNN，作者歸因於 barren plateau 限制了 VQC 中可訓練參數的數量。[作者分析]

## 相關頁面

- [QGNN 的挑戰](qgnn-challenges.md)
- [Expressibility](expressibility.md)
- [EDU-QGC](../models/edu-qgc.md)

- [參數化量子電路與 VQA](pqc-and-vqa.md)

- [QGNN 通用 ansatz、QGRNN、QGCNN](../models/qgnn-general-ansatz.md)
- 回到 [index](../index.md)
