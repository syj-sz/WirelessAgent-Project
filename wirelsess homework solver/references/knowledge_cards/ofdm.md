# OFDM 正交频分复用

> 教材参考: Goldsmith Ch.12, Molish Ch.7

## 核心公式

### OFDM 符号周期

$$T_{\text{OFDM}} = N \cdot T_s + T_{cp}$$

其中 $N$ 为子载波数, $T_s$ 为采样周期, $T_{cp}$ 为循环前缀时长。

### 子载波间隔

$$\Delta f = \frac{1}{N \cdot T_s} = \frac{1}{T_{\text{FFT}}}$$

### 子载波带宽

$$B_{\text{subcarrier}} = \frac{1}{T_{\text{OFDM}}}$$

### 总带宽

$$B_{\text{total}} = N \cdot \Delta f = \frac{N}{T_{\text{FFT}}}$$

### 循环前缀约束

$$T_{cp} \geq \tau_{\max}$$

其中 $\tau_{\max}$ 为最大多径时延扩展。

### OFDM 传输方程

$$x(t) = \frac{1}{\sqrt{N}}\sum_{k=0}^{N-1} X_k e^{j2\pi k \Delta f t}, \quad 0 \leq t < T_{\text{OFDM}}$$

## 关键概念

- **子载波正交性**: $\int_0^{T} e^{j2\pi k \Delta f t} \cdot e^{-j2\pi l \Delta f t} dt = 0$ for $k \neq l$
- **循环前缀作用**: 将线性卷积转为循环卷积, 消除 ISI 和 ICI
- **ICI (子载波间干扰)**: 多普勒或频偏破坏正交性
- **ISI (符号间干扰)**: CP 长度小于信道冲击响应时发生
- **峰均比 (PAPR)**: OFDM 的缺点, 峰值功率/平均功率可达 $N$
- **OFDM 系统结构**: 串并转换 → IFFT → +CP → 信道 → -CP → FFT → 并串转换 → 检测

## 典型考题

1. 给定 N=64, 子载波间隔 15kHz, 求总带宽
2. CP 长度设计 (τmax=2μs)
3. 频偏引起的 ICI 分析

## 计算工具

```bash
python formula_lookup.py --category 带宽
```
