---
name: Wireless Homework Solver
description: "无线通信课程作业辅导：通信原理、信息论、MIMO、OFDM、调制编码等专业内容"
user-invocable: true
---

# Wireless Homework Solver — 无线通信课程作业辅导

覆盖 9 大领域：信道容量、调制、编码、信号处理、传播、噪声分析、MIMO、OFDM、信息论。

## 环境

```bash
pip install -r <skill_dir>/requirements.txt
```

依赖：numpy, scipy。纯本地，不耗 API token。

## 工作原理

**模型擅长的事**（推导、解释、分类、生成步骤）→ 由当前 agent 的底层模型直接完成。
**模型不擅长的事**（精确数值计算、单位换算、确定性公式检索）→ 调用下方脚本。

---

## 脚本工具

### 精确电信计算

```bash
py <skill_dir>/scripts/telecom_calc.py Q_function --x 4.0
py <skill_dir>/scripts/telecom_calc.py ber_bpsk_coherent --Eb_N0_dB 10
py <skill_dir>/scripts/telecom_calc.py shannon_capacity --bandwidth_Hz 1e6 --snr_dB 30
py <skill_dir>/scripts/telecom_calc.py --list
```

支持：Q-function、各类 BER（BPSK/QPSK/M-PSK/M-QAM/FSK）、信道容量、Rayleigh/Rician 衰落、MRC 分集增益、线性分组码纠错等。

### 公式查询

```bash
py <skill_dir>/scripts/formula_lookup.py --search "bandwidth"
py <skill_dir>/scripts/formula_lookup.py --formula raised_cosine_bandwidth --Rs 2000 --alpha 0.5
py <skill_dir>/scripts/formula_lookup.py --list
```

包含 30+ 条 WCHW 数据集验证过的公式。

### 单位转换

```bash
py <skill_dir>/scripts/unit_convert.py --value 30 --from dBm --to W
py <skill_dir>/scripts/unit_convert.py --value 1e6 --from Hz --to MHz
py <skill_dir>/scripts/unit_convert.py --value 3 --from dB --to linear
```

支持 dB/dBm/dBW、Hz-kHz-MHz-GHz、W-mW-uW 等。

---

## 解题流程（当前 agent 执行）

### Step 1: 理解题目
- 文字/LaTeX 直接接受，图片用视觉识别
- 确定知识领域（信道容量/调制/编码/传播/噪声/MIMO/OFDM/信息论）

### Step 2: 分析与推导 + 给出答案
1. 列出已知条件和待求量
2. 选择正确公式（引用 `references/formulas.md` 或知识卡片中对应章节）
3. 分步推导，每步标注物理意义
4. 调用 `telecom_calc.py` 做精确计算（不要自己手算数值）
5. 调用 `unit_convert.py` 验证单位一致性
6. 给出最终答案（**加粗**突出数值结果）

### Step 3: 知识点关联（本题精确关联，放在答案之后）

在解答完成后，**根据本题实际推导过程**，逐条列出本题用到的具体知识点和公式。
不要只说领域名称，要精确到每一步用了什么定理、什么公式、什么方法。

必须包含以下三类内容：

**（a）本步骤用到的公式/定理**
- 列出本题推导中实际调用的每个公式或定理
- 每个公式写清楚：公式本身 + 用于哪一步 + 对应 `references/formulas.md` 中的条目

**（b）本步骤用到的概念/方法**
- 列出本题涉及的通信概念和计算方法
- 例如：初等行变换化系统码、最小码距的列向量判定法、伴随式与错误图样的关系

**（c）参考来源**
- 引用对应知识卡片：`references/knowledge_cards/<领域>.md`
- 引用教材章节：`references/textbooks_index.md`

格式示例：

```
━━━ 本题知识点关联 ━━━

[公式]
1. 系统码生成矩阵：G = [I_k | P]
   → 用于 (1) 初等行变换，将 G 化为行最简形
   → references/formulas.md → linear_block_code

2. 校验矩阵：H = [P^T | I_(n-k)]
   → 用于 (2) 由系统码形式直接写出 H
   → references/formulas.md → linear_block_code

3. 最小码距判定：d_min = min{ w(c) | c 属于 C, c != 0 }
   等价于 H 中线性相关的最小列数
   → 用于 (2) 判定 d_min = 4

4. 伴随式定义：s = e · H^T
   → 用于 (3) 由 s 反推错误图样 e

[概念]
5. 初等行变换（行交换、行消去）
   → 用于 (1) 将 G 化为系统码形式，不改变码空间

6. 码重与错误图样
   → 用于 (3) 限定码重为 2 的 e，筛选出 4 个解

[参考]
  知识卡片：references/knowledge_cards/coding.md
  教材：Goldsmith Ch.8、Molish Ch.6
━━━━━━━━━━━━━━━━
```
注意：这个示例写在代码块里只是为了在 SKILL.md 中展示。
实际输出知识点关联时，代码块标记本身不要输出，只用纯文本行。

### Step 4: 输出评分卡

对用户答案（如果有）做四维评分：

| 维度 | 权重 | 评分标准 |
|------|------|----------|
| 公式准确性 | 35% | 公式选择是否正确 |
| 数值精度 | 25% | <1%→满分, <5%→0.9, <10%→0.7, <20%→0.5 |
| 单位正确性 | 20% | 单位匹配/等价 |
| 步骤逻辑 | 20% | 推导链完整、有条理 |

输出格式：
```
TOTAL: 0.85 [B]
公式准确性 0.90 [B]  ████████████░░░░░░
数值精度   0.95 [B]  ██████████████░░░░
单位正确性 0.80 [B]  ██████████░░░░░░░░
步骤逻辑   0.75 [C]  █████████░░░░░░░░░
```

---

## 知识卡片

参见 `references/knowledge_cards/`：
- 信道容量 — Shannon 定理、Nyquist 准则、频谱效率
- 调制技术 — BPSK/QPSK/QAM/ASK/FSK、星座图、BER
- 信道编码 — 线性分组码、卷积码、汉明码
- 信号处理 — 采样、滤波、FFT、基带等效
- 无线传播 — 路径损耗、Rayleigh/Rician 衰落、多普勒
- 噪声分析 — erfc、Q-function、噪声系数
- MIMO — 空间复用、分集、波束赋形
- OFDM — 子载波、循环前缀、ICI/ISI
- 信息论 — 熵、互信息、信道编码定理

---

> <rule name="output_format" severity="error">
> **禁用 LaTeX。** 面向用户的所有输出必须用纯文本 + Unicode 符号，绝不能输出 `$`、`\(`、`\[`、`\log`、`\frac`、`\sqrt`、`\cdot` 等任何 LaTeX 命令或定界符。
>
> **纯文本公式书写规则：**
>
> 1. **Unicode 上下标：** 下标用 ₂ ₃ ₀ ₁ ₄ ₅ ₆ ₇ ₈ ₉，上标用 ² ³ ⁰ ¹ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁺ ⁻ ⁻¹
> 2. **特殊字符：** √ 代替 \sqrt，× 或 · 代替 \times/\cdot，÷ 代替 \div，→ 代替 \rightarrow，∞ 代替 \infty，≈ 代替 \approx
> 3. **函数名直接写：** log₂、erfc(x)、Q(x)、sin(θ)、cos(ωt) 等
> 4. **分数用 /：** a/b，复杂分数加括号如 (a + b) / (c - d)
> 5. **指数用 ^ + 括号：** e^(jωt)、10⁻⁶、2¹⁰
> 6. **希腊字母直接用 Unicode：** α β γ δ ε θ λ μ π ρ σ τ φ ψ ω Ω Δ Σ
>
> **矩阵/行列式展示规则（必须完整展开，禁止用 LaTeX 或省略表示）：**
>
> 矩阵必须完整展开为行 x 列的形式，每个元素写在对应位置上。初等行变换的
> **每一步**都要展示完整矩阵，不能只在文字里描述变换操作而不展示矩阵。
>
> 示例：
> ```
> 2x2 矩阵：
> [a  b]
> [c  d]
>
> 4x8 增广矩阵：
> [1  0  0  0  |  1  1  1  0]
> [0  1  0  0  |  1  1  0  1]
> [0  0  1  0  |  1  0  1  1]
> [0  0  0  1  |  0  1  1  1]
>
> 列向量：
> [1]
> [2]
> [3]
> ```
>
> **初等行变换流程的展示要求（以 (8,4) 码为例）：**
>
> 正确写法（每一步展示完整矩阵）：
> ```
> Step 1: r3 ← r3 + r1
>
> [1  1  1  0  1  0  0  0]
> [0  0  1  1  1  1  0  0]
> [0  0  1  0  1  0  1  1]
> [0  1  1  1  0  0  0  1]
>
> Step 2: r2 ↔ r4
>
> [1  1  1  0  1  0  0  0]
> [0  1  1  1  0  0  0  1]
> [0  0  1  1  1  1  0  0]
> [0  0  1  0  1  0  1  1]
>
> （继续直到得到系统码形式...）
> ```
>
> 错误写法（只有文字描述，没有完整矩阵）：
> ```
> Step 1: r3 ← r3 + r1
> Step 2: r2 ↔ r4
> （然后直接跳到结果矩阵）
> ```
>
> **最后检查：** 输出中绝不能包含 `\` 或 `$` 字符。
> </rule>
