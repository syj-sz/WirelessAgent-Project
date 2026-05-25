# 信号处理 (Signal Processing)

> 教材参考: Goldsmith Ch.5, Molish Ch.2

## 核心公式

### Nyquist 采样定理

$$f_s \geq 2f_{\max}$$

无失真重建连续信号所需的最小采样频率。

### 升余弦脉冲成形带宽

$$B = \frac{R_s(1 + \alpha)}{2}$$

其中 $R_s$ 为符号速率, $\alpha \in [0,1]$ 为滚降因子。

### PCM 量化信噪比

$$\text{SQNR}_{\text{dB}} = 6.02n + 1.76 \quad \text{(dB)}$$

其中 $n$ 为每样本量化比特数。

### Delta 调制约 SNR

$$\text{SNR} \approx \frac{3f_s^3}{8\pi^2 f_m^2 W}$$

### 升余弦脉冲时域波形

$$h(t) = \frac{\sin(\pi t/T_s)}{\pi t/T_s} \cdot \frac{\cos(\pi \alpha t/T_s)}{1 - (2\alpha t/T_s)^2}$$

## 关键概念

- **Nyquist 采样定理**: 避免频谱混叠的最低条件
- **升余弦脉冲成形**: 消除 ISI 的 Nyquist 脉冲
- **PCM 量化**: 每增加 1bit, SQNR 提高约 6dB
- **Delta 调制**: 1bit 量化 + 过采样
- **匹配滤波器**: 最大化输出 SNR, 频率响应 $H(f) = S^*(f)$

## 典型考题

1. 给定符号速率 Rs=1000baud, α=0.25, 求所需带宽
2. n=8bit 量化的 SQNR
3. 采样定理验证

## 计算工具

```bash
python telecom_calc.py raised-cosine --rs 1000 --alpha 0.25
```
