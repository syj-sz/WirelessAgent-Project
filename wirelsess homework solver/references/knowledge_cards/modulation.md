# 调制技术 (Modulation)

> 教材参考: Goldsmith Ch.6, Molish Ch.5

## 核心公式

### BPSK 误码率 (相干检测)

$$\text{BER}_{\text{BPSK}} = \frac{1}{2}\text{erfc}\left(\sqrt{\frac{E_b}{N_0}}\right)$$

### BFSK 误码率 (相干检测)

$$\text{BER}_{\text{BFSK}} = \frac{1}{2}\text{erfc}\left(\sqrt{\frac{E_b}{2N_0}}\right)$$

### DPSK 误码率

$$\text{BER}_{\text{DPSK}} = \frac{1}{2}\exp\left(-\frac{E_b}{N_0}\right)$$

### M-QAM 符号错误概率

$$P_s \approx 4\left(1 - \frac{1}{\sqrt{M}}\right) Q\left(\sqrt{\frac{3E_s}{(M-1)N_0}}\right)$$

### Eb 与 Es 关系

$$E_s = E_b \cdot \log_2 M$$

## 关键概念

- **BPSK/QPSK/QAM 星座图**: 信号空间表示
- **相干/非相干检测**: 是否需要载波相位信息
- **调制指数**: FM/PM 中频偏与调制信号的关系
- **Carson 带宽**: $B = 2(\Delta f + f_m)$
- **匹配滤波器**: 最大 SNR 接收

## 典型考题

1. 给定 Eb/N0=10dB, 求 BPSK 误码率
2. 比较 BPSK 与 QPSK 的带宽效率
3. 16QAM 星座图欧氏距离计算

## 计算工具

```bash
python telecom_calc.py ber-bpsk --ebn0-db 10
python telecom_calc.py ber-bfsk --ebn0-db 10
python telecom_calc.py ber-dpsk --ebn0-db 10
```
