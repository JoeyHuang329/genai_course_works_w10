---
title: S3｜Ryu, Elala, Rhee 2023 — 以量子圖神經網路預測分子性質
type: source
sources: [S3]
difficulty: 2
updated: 2026-11-23
---

## 書目

J.-Y. Ryu, E. Elala, J.-K. K. Rhee. *Quantum Graph Neural Network Models for Materials Search*. Materials 16(12):4300, 2023. [doi:10.3390/ma16124300](https://doi.org/10.3390/ma16124300)。作者來自 KAIST 與 Qunova Computing。開放取用。

## 一句話

一個重原子 = 一個 qubit、一條化學鍵 = 一個保持排列對稱性的雙 qubit 閘（EDU），用這種量子電路預測小分子的 HOMO-LUMO 能隙，並和古典 GNN 在相近參數量下比較。

## 這篇在做什麼

1. 前半是回顧：古典 GNN 在材料研究的發展（MPNN、ALIGNN 等）、變分量子機器學習、各種 QGNN。
2. 後半是實驗：以 [EDU-QGC](../models/edu-qgc.md) 為核心，測試不同的編碼方式、層數、讀出函數、EDU 結構、master node、data re-uploading、以及用古典小網路學習編碼角度。
3. 資料：QM9（最多 9 個非氫原子的有機分子，性質由 DFT 計算），只預測 HOMO-LUMO gap。

**HOMO-LUMO gap 是什麼？** 分子中「最高被佔據的電子軌域」與「最低未被佔據的軌域」之間的能量差，和分子的穩定性、導電與光學性質有關，是材料篩選常用的目標。單位 Ha（Hartree，原子單位的能量）。

## 重點

- **圖的建法**：非氫原子 = 節點，鍵 = 邊；節點特徵有原子序、鍵結氫數、芳香性、混成軌域；邊特徵是鍵的種類（單/芳香/雙/參）。用 RDKit 從 SMILES 字串解析，**丟掉 3D 結構**。
- **編碼**：每個原子一個 qubit，用 $R_Y$ 再 $R_Z$ 把特徵轉成 Bloch 球上的一點（angle encoding）。
- **讀出**：對所有 qubit 的 $\langle Z\rangle$ 取平均（local），或再加上一個全部 qubit 的乘積項（global）；兩種都對 qubit 排列不變。
- **訓練**：PennyLane 無雜訊模擬，資料抽樣 10,000/1,000/1,000，Adam、lr 0.01、batch 128、MSE、150 epoch。

## 文獻怎麼說

- [S3] 在使用相近數量可訓練變數時，QGNN 可得到比古典模型更低的 test loss，且訓練收斂較快。[作者宣稱]
- [S3] 三種編碼中「原子序 + 鍵結氫數」最好（test MAE $1.88\times10^{-2}$ Ha）；把三個特徵塞進一個 qubit 反而較差，作者解釋為不同輸入在潛在空間中重疊過多。[模擬實驗]
- [S3] EDU-QGC 層數 1→2→3 時 test MSE 由 $7.38$ 降至 $5.88$（單位 $10^{-4}$ Ha²）。[模擬實驗]
- [S3] local 讀出優於 global 讀出，儘管 local 是 global 的特例；作者推測最佳化較容易被困在不佳區域。[模擬實驗]
- [S3] 加入 master node（連到所有原子的虛擬節點）使 test MSE 改善約 31%（MAE $1.51\times10^{-2}$ Ha），代價是多 1 個 qubit、約 2 倍可訓練變數與約 2 倍雙 qubit 閘；data re-uploading 理論上較強，實際卻略差。[模擬實驗]
- [S3] 以古典小網路（angle extraction network）學習編碼角度，使兩種特徵組合的 test loss 分別下降 9.6% 與 30.6%。[模擬實驗]
- [S3] 古典 GGNN 模型的最佳 test MAE 為 $1.77\times10^{-2}$ Ha（三層 GGNN、mean 聚合），量子 baseline 為 $1.88\times10^{-2}$、加 master node 後為 $1.51\times10^{-2}$。[模擬實驗]
- [S3] 與文獻中的 SOTA 古典模型 ALIGNN 相比，其回報的 test 誤差約比本文最佳 QGNN 低 10 倍（訓練與測試方法不同）。[作者分析]
- [S3] 學出來的編碼幾乎把所有原子映射到 $|1\rangle$ 附近；把所有原子固定編碼成 $|1\rangle$ 時，test loss 優於其中一種手工編碼、但劣於學習式編碼，作者認為細微差異仍有意義。[模擬實驗]
- [S3] QGNN 的 qubit 數正比於每張圖的節點數，且需要高連接性；作者認為全連接、高閘保真度的離子阱硬體最適合，並預期雜訊會比 qubit 數更早成為限制。[作者分析]
- [S3] EDU 的數量隨邊數線性成長，但作用在不同 qubit 上的 EDU 可同時執行，時間成本與圖的邊著色數（chromatic index）成正比，依 Vizing 定理至多為最大度數 + 1。[作者分析]

## 限制與批判

- **實驗公平性**：古典模型跑 3 次（不同初始化）取最佳，量子與 hybrid 模型只跑 1 次，且初始權重全設為 1。
- 只在**無雜訊模擬器**上執行；只有一個預測目標；資料為 QM9 的子集。
- 「比古典好」只在**本文自己的古典 baseline、相近參數量**的條件下成立；與 SOTA（ALIGNN）仍差約一個數量級 → 屬於 [quantum utility 而非 quantum advantage](../concepts/advantage-vs-utility.md) 的範疇；S5 也對分子化學領域下了相同結論。[推論] <!-- reviewed-claim -->
- 所有原子都被編碼到 $|1\rangle$ 附近，暗示模型可能主要依賴圖結構與鍵的種類，而非原子特徵。[推論]

## 相關頁面

- [EDU-QGC 模型頁](../models/edu-qgc.md)
- [排列不變性/等變性](../concepts/permutation-equivariance.md)
- [資料編碼](../concepts/data-encoding.md)
- 回到 [index](../index.md)
