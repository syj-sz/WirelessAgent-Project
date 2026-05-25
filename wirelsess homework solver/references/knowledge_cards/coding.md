# 信道编码 (Channel Coding)

> 教材参考: Goldsmith Ch.8, Molish Ch.6

## 核心公式

### 检错能力

$$e_{\text{detect}} = d_{\min} - 1$$

### 纠错能力

$$e_{\text{correct}} = \left\lfloor\frac{d_{\min} - 1}{2}\right\rfloor$$

### 编码率

$$R = \frac{k}{n}$$

其中 $k$ 为信息位数, $n$ 为编码后总位数。

### 编码增益

$$G_{\text{coding}} = \left(\frac{E_b}{N_0}\right)_{\text{uncoded}} - \left(\frac{E_b}{N_0}\right)_{\text{coded}} \quad \text{(dB, 相同 BER 下)}$$

### 汉明界

$$2^{n-k} \geq \sum_{i=0}^{t} \binom{n}{i}$$

其中 $t = \lfloor(d_{\min}-1)/2\rfloor$。

## 关键概念

- **线性分组码**: 生成矩阵 $G$ 与校验矩阵 $H$, $GH^T = 0$
- **汉明码**: 可纠单错的完备码 $(n=2^m-1, k=2^m-1-m, d_{\min}=3)$
- **最小距离 $d_{\min}$**: 任意两个不同码字间的最小 Hamming 距离
- **硬判决 vs 软判决**: 二值 vs 多电平量化
- **Turbo 码**: 并行级联卷积码 + 迭代译码
- **LDPC 码**: 稀疏校验矩阵 + 置信传播译码

## 典型考题

1. 给定生成矩阵, 求所有码字和 $d_{\min}$
2. 编码率 $R=1/2$, 比较编码/未编码 BER 性能
3. $(7,4)$ 汉明码纠错验证

## 计算工具

```bash
# 使用 formula_lookup 查看编码相关公式
python formula_lookup.py --category 编码
```
