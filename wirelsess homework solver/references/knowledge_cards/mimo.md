# MIMO 多天线系统

> 教材参考: Goldsmith Ch.10, Molish Ch.8

## 核心公式

### MIMO 信道容量 (已知 CSI)

$$C = \log_2 \det\left(I + \frac{\text{SNR}}{N_t} HH^H\right)$$

其中 $H$ 为 $N_r \times N_t$ 信道矩阵。

### SVD 分解与并行信道

$$H = U\Sigma V^H$$

信道可分解为 $r = \text{rank}(H)$ 个并行独立信道:

$$C = \sum_{i=1}^{r} \log_2\left(1 + \frac{\text{SNR}}{N_t} \sigma_i^2\right)$$

### 注水功率分配

$$P_i = \max\left(\mu - \frac{N_t}{\text{SNR} \cdot \sigma_i^2}, 0\right)$$

### 分集增益

$$d = \lim_{\text{SNR} \to \infty} \frac{-\log P_e}{\log \text{SNR}}$$

### Alamouti 编码 (2×1)

$$\mathbf{S} = \begin{bmatrix} s_1 & -s_2^* \\ s_2 & s_1^* \end{bmatrix}$$

## 关键概念

- **空间复用增益**: 利用多天线传输多个独立数据流
- **分集增益**: 利用多路径降低误码率, 最大分集阶数 = $N_t \times N_r$
- **SVD 预编码**: 发端 $V$, 收端 $U^H$, 将 MIMO 转换为并行 SISO
- **Alamouti 空时编码**: 两发一收满分集方案
- **波束赋形 (Beamforming)**: 将能量集中到目标方向

## 典型考题

1. 2×2 MIMO 信道容量 (给定 H 矩阵)
2. 比较 Alamouti 与无分集 BER 性能
3. V-BLAST 与 D-BLAST 区别

## 计算工具

```bash
python formula_lookup.py --category 信道容量
```
