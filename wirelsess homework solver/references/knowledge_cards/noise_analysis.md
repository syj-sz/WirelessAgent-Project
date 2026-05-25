# 噪声分析 (Noise Analysis)

> 教材参考: Goldsmith Ch.4, Molish Ch.3

## 核心公式

### Q 函数

$$Q(x) = \frac{1}{\sqrt{2\pi}} \int_x^\infty e^{-t^2/2} dt = \frac{1}{2}\text{erfc}\left(\frac{x}{\sqrt{2}}\right)$$

### erfc 与 Q 函数关系

$$\text{erfc}(x) = \frac{2}{\sqrt{\pi}} \int_x^\infty e^{-t^2} dt$$
$$Q(x) = \frac{1}{2}\text{erfc}\left(\frac{x}{\sqrt{2}}\right)$$

### AWGN 噪声功率

$$P_N = k \cdot T \cdot B \cdot F$$

其中 $k = 1.38 \times 10^{-23}$ J/K, $T$ 为温度 (K), $B$ 为带宽, $F$ 为噪声系数。

### 噪声系数

$$F = \frac{\text{SNR}_{\text{in}}}{\text{SNR}_{\text{out}}}, \quad \text{NF} = 10\log_{10}(F)$$

### Eb/N0 与 SNR 关系

$$\frac{E_b}{N_0} = \text{SNR} \cdot \frac{B}{R_b}$$

### 噪声温度

$$T_e = T_0(F - 1), \quad T_0 = 290\text{K}$$

## 关键概念

- **AWGN 信道模型**: 加性高斯白噪声, $y = x + n$, $n \sim \mathcal{N}(0, N_0/2)$
- **Q 函数与 erfc**: Q 函数值可用 `telecom_calc.py Q-function` 精确计算
- **噪声系数**: 衡量器件/系统恶化 SNR 的程度
- **Eb/N0 vs SNR**: Eb/N0 归一化到每比特, 便于不同调制方式比较
- **匹配滤波器检测**: 最大 SNR 意义下的最优线性滤波器

## 典型考题

1. 计算 Q(3) 的值
2. 给定 SNR=10dB, B=1MHz, Rb=100kbps, 求 Eb/N0
3. 级联系统噪声系数计算 (Friis 噪声公式)

## 计算工具

```bash
python telecom_calc.py q-function --x 3
python telecom_calc.py erfc --x 2
```
