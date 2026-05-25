# 无线通信公式库

> 30+ 常用无线通信公式, 附带参数说明和计算工具入口。

## 目录

- [带宽与速率](#带宽与速率)
- [误码率 (BER)](#误码率-ber)
- [调制](#调制)
- [信号处理](#信号处理)
- [传播与衰落](#传播与衰落)
- [信道容量](#信道容量)
- [编码](#编码)
- [工具函数](#工具函数)

---

## 带宽与速率

### 奈奎斯特带宽

$$B_{\min} = \frac{R_s}{2} \quad \text{(理想奈奎斯特)}$$

### 升余弦带宽

$$B = \frac{R_s(1 + \alpha)}{2}$$

**参数**: `Rs` 符号速率 (baud), `alpha` 滚降因子 [0,1]

**计算**: `python telecom_calc.py raised-cosine --rs <Rs> --alpha <α>`

---

### 符号速率与比特率

$$R_b = R_s \cdot \log_2 M$$

**参数**: `Rs` 符号速率, `M` 调制阶数

---

### OFDM 子载波间隔

$$\Delta f = \frac{1}{T_{\text{FFT}}}$$

---

### OFDM 总带宽

$$B_{\text{total}} = N \cdot \Delta f$$

**参数**: `N` 子载波数

---

### Carson 带宽 (FM)

$$B = 2(\Delta f + f_m)$$

---

## 误码率 (BER)

### BPSK 误码率 (相干)

$$\text{BER} = \frac{1}{2}\text{erfc}\left(\sqrt{\frac{E_b}{N_0}}\right)$$

**计算**: `python telecom_calc.py ber-bpsk --ebn0-db <Eb/N0_dB>`

---

### BFSK 误码率 (相干)

$$\text{BER} = \frac{1}{2}\text{erfc}\left(\sqrt{\frac{E_b}{2N_0}}\right)$$

**计算**: `python telecom_calc.py ber-bfsk --ebn0-db <Eb/N0_dB>`

---

### DPSK 误码率

$$\text{BER} = \frac{1}{2}\exp\left(-\frac{E_b}{N_0}\right)$$

**计算**: `python telecom_calc.py ber-dpsk --ebn0-db <Eb/N0_dB>`

---

### M-QAM 符号错误概率

$$P_s \approx 4\left(1 - \frac{1}{\sqrt{M}}\right) Q\left(\sqrt{\frac{3}{M-1} \cdot \frac{E_s}{N_0}}\right)$$

---

## 调制

### Eb 与 Es 关系

$$E_s = E_b \cdot \log_2 M$$

### QPSK → BPSK 等效

QPSK 的 BER 与 BPSK 相同 (每比特 Eb/N0 相同条件下)

---

## 信号处理

### 奈奎斯特采样定理

$$f_s \geq 2f_{\max}$$

---

### PCM SQNR

$$\text{SQNR}_{\text{dB}} = 6.02n + 1.76$$

**参数**: `n` 每样本量化比特数

---

## 传播与衰落

### 自由空间路径损耗 (Friis)

$$P_r = P_t G_t G_r \left(\frac{\lambda}{4\pi d}\right)^2$$

---

### Rayleigh 电平穿越率 (LCR)

$$N_R = \sqrt{2\pi} \cdot f_D \cdot \rho \cdot e^{-\rho^2}$$

**参数**: `fD` 最大多普勒频移 (Hz), `rho` 归一化门限电平

**计算**: `python telecom_calc.py rayleigh-lcr --fd <fD> --rho <ρ>`

---

### Rayleigh 平均衰落时长 (AFD)

$$\bar{t}_f = \frac{e^{\rho^2} - 1}{\rho \cdot f_D \cdot \sqrt{2\pi}}$$

**计算**: `python telecom_calc.py rayleigh-afd --fd <fD> --rho <ρ>`

---

### Rayleigh 中断概率

$$P_{\text{out}} = 1 - \exp\left(-\frac{P_{\text{th}}^2}{2\sigma^2}\right)$$

---

### Rician 中断概率

$$P_{\text{out}} = 1 - Q_1\left(\frac{s}{\sigma}, \frac{P_{\text{th}}}{\sigma}\right)$$

其中 $Q_1$ 为 Marcum Q 函数。

---

## 信道容量

### Shannon 容量 (AWGN)

$$C = B \cdot \log_2(1 + \text{SNR}_{\text{linear}})$$

**计算**: `python telecom_calc.py shannon --bw <B_Hz> --snr-db <SNR_dB>`

---

### MIMO 容量

$$C = \log_2 \det\left(I + \frac{\text{SNR}}{N_t}HH^H\right)$$

---

### 中断容量

$$P_{\text{out}} = P(\log_2(1 + |h|^2\text{SNR}) < R)$$

---

## 编码

### 检错能力

$$e_{\text{detect}} = d_{\min} - 1$$

### 纠错能力

$$e_{\text{correct}} = \left\lfloor\frac{d_{\min} - 1}{2}\right\rfloor$$

### 编码率

$$R = \frac{k}{n}$$

---

### 汉明界

$$2^{n-k} \geq \sum_{i=0}^{t} \binom{n}{i}$$

---

## 工具函数

### Q 函数

$$Q(x) = \frac{1}{2}\text{erfc}\left(\frac{x}{\sqrt{2}}\right)$$

**计算**: `python telecom_calc.py q-function --x <x>`

---

### erfc

$$\text{erfc}(x) = \frac{2}{\sqrt{\pi}} \int_x^\infty e^{-t^2} dt$$

**计算**: `python telecom_calc.py erfc --x <x>`

---

### dB ↔ 线性转换

$$\text{dB} = 10\log_{10}(x_{\text{linear}})$$

$$x_{\text{linear}} = 10^{\text{dB}/10}$$

**计算**: `python unit_convert.py --value <v> --from <dB|linear> --to <linear|dB>`

---

### Marcum Q 函数

$$Q_M(a, b) = \frac{1}{a^{M-1}} \int_b^\infty x^M \exp\left(-\frac{x^2 + a^2}{2}\right) I_{M-1}(ax) dx$$

**计算**: `python telecom_calc.py marcum-q --m <M> --a <a> --b <b>`

---

## 快速查找

列出所有公式: `python formula_lookup.py --list`
按类别搜索: `python formula_lookup.py --category <category>`
按关键字搜索: `python formula_lookup.py --search <keyword>`
