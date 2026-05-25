# 信道容量 (Channel Capacity)

> 教材参考: Goldsmith Ch.4, Molish Ch.3

## 核心公式

### Shannon 信道容量 (AWGN)

$$C = B \cdot \log_2(1 + \text{SNR}_{\text{linear}})$$

其中 $C$ 是信道容量 (bps), $B$ 是带宽 (Hz), $\text{SNR}_{\text{linear}}$ 是线性信噪比。

### dB 转线性

$$\text{SNR}_{\text{linear}} = 10^{\text{SNR}_{\text{dB}} / 10}$$

### 频谱效率

$$\eta = \frac{C}{B} = \log_2(1 + \text{SNR}_{\text{linear}}) \quad \text{(bps/Hz)}$$

### Nyquist 准则

$$R_s \leq 2B \quad \text{(无 ISI 传输)}$$

### 中断容量

$$P_{\text{out}} = P(\log_2(1 + |h|^2 \text{SNR}) < R)$$

## 关键概念

- **Shannon 定理**: AWGN 信道中可靠通信的最大速率
- **Nyquist 准则**: 无码间串扰的最大符号速率为 $2B$
- **注水定理 (Waterfilling)**: 频率选择性信道中的最优功率分配
- **频谱效率**: 单位带宽的传输速率
- **中断容量**: 衰落信道中以一定概率达到的速率

## 典型考题

1. 给定带宽 B=1MHz, SNR=30dB, 求信道容量
2. 求达到 10Mbps 速率所需的最小 SNR
3. 比较 AWGN 和 Rayleigh 衰落下的信道容量

## 计算工具

```bash
python telecom_calc.py shannon --bw 1e6 --snr-db 30
```
