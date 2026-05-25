# 教材章节索引

## 主教材

### 1. Andrea Goldsmith — *Wireless Communications* (Cambridge, 2005)

| 章节 | 主题 | 知识卡片 | 核心公式 |
|------|------|---------|---------|
| Ch.2 | 路径损耗与阴影衰落 | propagation | Friis 方程, 对数正态阴影 |
| Ch.3 | 统计多径信道模型 | propagation | Rayleigh, Rician, Nakagami, LCR, AFD |
| Ch.4 | 信道容量 | channel_capacity, noise_analysis, info_theory | Shannon 公式, Q 函数, AWGN |
| Ch.5 | 数字调制与检测 | signal_processing | Nyquist, 升余弦, 匹配滤波器 |
| Ch.6 | 数字调制性能 | modulation | BPSK/QPSK/QAM BER, 星座图 |
| Ch.8 | 信道编码 | coding | 线性分组码, 汉明码, 卷积码 |
| Ch.10 | MIMO 系统 | mimo | MIMO 容量, 空时编码, Alamouti |
| Ch.12 | 多载波调制 | ofdm | OFDM, CP, 子载波正交性 |

### 2. Andreas F. Molisch — *Wireless Communications* (Wiley, 2nd Ed., 2011)

| 章节 | 主题 | 知识卡片 | 核心公式 |
|------|------|---------|---------|
| Ch.2 | 信息论基础 | info_theory | 熵, 互信息, 信道编码定理 |
| Ch.3 | 噪声与干扰 | noise_analysis | AWGN, 噪声系数, 匹配滤波器 |
| Ch.4 | 无线信道 | propagation | 路径损耗, Rayleigh/Rician, 多普勒 |
| Ch.5 | 调制 | modulation | BPSK/QPSK/QAM/M-FSK |
| Ch.6 | 信道编码 | coding | 分组码, 卷积码, Turbo, LDPC |
| Ch.7 | OFDM | ofdm | 子载波, CP, PAPR |
| Ch.8 | MIMO | mimo | 空间复用, 分集, 预编码 |

## 知识卡片 ↔ 章节映射

| 知识卡片 | Goldsmith | Molisch | 关键页码 |
|---------|-----------|---------|---------|
| channel_capacity | Ch.4: §4.1-4.4 | Ch.2: §2.4 | 香农容量推导 |
| modulation | Ch.6: §6.1-6.3 | Ch.5: §5.1-5.5 | BER 曲线 |
| coding | Ch.8: §8.1-8.5 | Ch.6: §6.1-6.7 | 编码增益 |
| signal_processing | Ch.5: §5.1-5.3 | Ch.2: §2.2-2.3 | 采样定理, SQNR |
| propagation | Ch.2-3 | Ch.4 | LCR/AFD |
| noise_analysis | Ch.4: §4.1-4.2 | Ch.3: §3.1-3.4 | Q 函数表 |
| mimo | Ch.10: §10.1-10.5 | Ch.8: §8.1-8.6 | MIMO 容量 |
| ofdm | Ch.12: §12.1-12.4 | Ch.7: §7.1-7.6 | OFDM 参数 |
| info_theory | Ch.4: §4.1 | Ch.2: §2.1-2.3 | 熵, 互信息 |

## 使用示例

在解题中引用教材:

> 根据 Goldsmith Ch.4 的 Shannon 定理, AWGN 信道容量由 $C = B\log_2(1+\text{SNR})$ 给出...

查看关联知识点:
```bash
python knowledge_search.py --query "shannon 信道容量"
python knowledge_search.py --show-card channel_capacity
```
