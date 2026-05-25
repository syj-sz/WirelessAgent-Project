# 无线传播 (Wireless Propagation)

> 教材参考: Goldsmith Ch.2-3, Molish Ch.4

## 核心公式

### 自由空间路径损耗 (Friis)

$$P_r = P_t \cdot G_t \cdot G_r \cdot \left(\frac{\lambda}{4\pi d}\right)^2$$

### dB 形式路径损耗

$$P_{r,\text{dBm}} = P_{t,\text{dBm}} + G_{t,\text{dBi}} + G_{r,\text{dBi}} - 20\log_{10}\left(\frac{4\pi d}{\lambda}\right)$$

### Rayleigh 分布 PDF

$$f(r) = \frac{r}{\sigma^2} \exp\left(-\frac{r^2}{2\sigma^2}\right), \quad r \geq 0$$

### Rician 分布 PDF

$$f(r) = \frac{r}{\sigma^2} \exp\left(-\frac{r^2 + s^2}{2\sigma^2}\right) I_0\left(\frac{rs}{\sigma^2}\right)$$

其中 $K = s^2/(2\sigma^2)$ 为 Rician K 因子。

### 电平穿越率 (LCR)

$$N_R = \sqrt{2\pi} \cdot f_D \cdot \rho \cdot e^{-\rho^2}$$

其中 $\rho = R/R_{\text{rms}}$, $f_D$ 为最大多普勒频移。

### 平均衰落时长 (AFD)

$$\bar{t}_f = \frac{e^{\rho^2} - 1}{\rho \cdot f_D \cdot \sqrt{2\pi}}$$

## 关键概念

- **大尺度衰落**: 路径损耗 + 阴影效应 (对数正态分布)
- **小尺度衰落**: 多径引起的快速幅度变化
- **Rayleigh 分布**: 无 LOS 路径, 多散射环境
- **Rician K 因子**: LOS 功率/散射功率比, $K \to 0$ 退化为 Rayleigh
- **电平穿越率 (LCR)**: 信号包络每秒正向穿越门限的次数
- **平均衰落时长 (AFD)**: 信号持续低于门限的平均时间
- **多普勒频移**: $f_D = v f_c / c$

## 典型考题

1. 给定 fD=50Hz, ρ=0.1, 求 LCR 和 AFD
2. 自由空间损耗计算 (d=1km, fc=2.4GHz)
3. Rician K=6dB 下的中断概率

## 计算工具

```bash
python telecom_calc.py rayleigh-lcr --fd 50 --rho 0.1
python telecom_calc.py rayleigh-afd --fd 50 --rho 0.1
```
