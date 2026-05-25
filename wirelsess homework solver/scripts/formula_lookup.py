#!/usr/bin/env python3
"""
无线通信公式查询与计算 — CLI 接口

用法:
  python formula_lookup.py --search "bandwidth"
  python formula_lookup.py --formula raised_cosine_bandwidth --Rs 2000 --alpha 0.5
  python formula_lookup.py --formula shannon_capacity --B 1e6 --SNR_dB 30
  python formula_lookup.py --list
"""
import sys
import os
import json
import argparse
import math

# 内联公式库
FORMULAS = {
    # ==== 带宽公式 ====
    "raised_cosine_bandwidth": {
        "formula": "B = Rs * (1 + alpha) / 2",
        "description": "升余弦滤波器第一零点带宽",
        "params": ["Rs", "alpha"],
        "note": "Rs = 符号速率 (baud), alpha = 滚降因子 (0~1)。M进制时: Rs = Rb/log2(M)",
        "category": "带宽",
        "calculator": None
    },
    "spectral_efficiency": {
        "formula": "eta_b = 2 / (1 + alpha)",
        "description": "升余弦脉冲成形频谱效率",
        "params": ["alpha"],
        "note": "alpha = 滚降因子。结果单位 bit/s/Hz",
        "category": "带宽",
        "calculator": None
    },
    "symbol_rate": {
        "formula": "Rs = Rb / log2(M)",
        "description": "M进制调制的符号速率",
        "params": ["Rb", "M"],
        "note": "Rb = 比特速率, M = 调制阶数 (2,4,8,16,...)",
        "category": "带宽",
        "calculator": None
    },
    "nrz_bandwidth": {
        "formula": "B = Rb",
        "description": "NRZ 第一零点带宽",
        "params": ["Rb"],
        "note": "Rb = 比特速率",
        "category": "带宽",
        "calculator": None
    },
    "nyquist_min_bandwidth": {
        "formula": "B_min = Rs / 2",
        "description": "Nyquist 理论最小带宽",
        "params": ["Rs"],
        "note": "Rs = 符号速率",
        "category": "带宽",
        "calculator": None
    },

    # ==== BER 公式 ====
    "bpsk_ber": {
        "formula": "BER = 0.5 * erfc(sqrt(Eb_N0))",
        "description": "相干 BPSK 误码率",
        "params": ["Eb_N0"],
        "note": "Eb_N0 使用线性值。QPSK 与 BPSK 公式相同",
        "category": "BER",
        "calculator": "ber_bpsk_coherent"
    },
    "bfsk_ber": {
        "formula": "BER = 0.5 * erfc(sqrt(Eb_N0 / 2))",
        "description": "相干正交 BFSK 误码率",
        "params": ["Eb_N0"],
        "note": "注意分母有 2！比 BPSK 有 3dB 惩罚",
        "category": "BER",
        "calculator": "ber_bfsk_coherent"
    },
    "ask_ber": {
        "formula": "BER = 0.5 * erfc(sqrt(Eb_N0 / 2))",
        "description": "相干 ASK/OOK 误码率",
        "params": ["Eb_N0"],
        "note": "与相干 BFSK 相同",
        "category": "BER",
        "calculator": "ber_bfsk_coherent"
    },
    "dpsk_ber": {
        "formula": "BER = 0.5 * exp(-Eb_N0)",
        "description": "DPSK 误码率",
        "params": ["Eb_N0"],
        "note": "Eb_N0 使用线性值",
        "category": "BER",
        "calculator": "ber_dpsk"
    },
    "nc_bfsk_ber": {
        "formula": "BER = 0.5 * exp(-Eb_N0 / 2)",
        "description": "非相干 BFSK 误码率",
        "params": ["Eb_N0"],
        "note": "Eb_N0 使用线性值",
        "category": "BER",
        "calculator": "ber_bfsk_noncoherent"
    },
    "nakagami_dpsk_ber": {
        "formula": "BER = 0.5 * (1 + gamma_b/m)^(-m)",
        "description": "Nakagami-m 衰落下的 DPSK 误码率",
        "params": ["gamma_b", "m"],
        "note": "gamma_b = 平均每比特 SNR (线性), m = Nakagami 参数",
        "category": "BER",
        "calculator": None
    },

    # ==== FM/AM 调制 ====
    "carson_bandwidth": {
        "formula": "BW = 2 * (delta_f + fm)",
        "description": "Carson 规则 FM 带宽",
        "params": ["delta_f", "fm"],
        "note": "delta_f = 频率偏移, fm = 调制频率",
        "category": "调制",
        "calculator": "fm_carson_bandwidth"
    },
    "fm_snr_improvement": {
        "formula": "G_FM = 3 * beta^2 * (beta + 1)",
        "description": "FM SNR 改善因子（鉴频器检测）",
        "params": ["beta"],
        "note": "beta = 调制指数 = delta_f/fm",
        "category": "调制",
        "calculator": None
    },
    "am_snr_improvement": {
        "formula": "G_AM = 2 * m^2 / (2 + m^2)",
        "description": "AM SNR 改善因子（包络检测）",
        "params": ["m"],
        "note": "m = 调制指数 (标准 AM 中 0~1)",
        "category": "调制",
        "calculator": None
    },
    "fm_modulation_index": {
        "formula": "beta = delta_f / fm",
        "description": "FM 调制指数",
        "params": ["delta_f", "fm"],
        "note": "delta_f = 频率偏移, fm = 调制频率",
        "category": "调制",
        "calculator": None
    },

    # ==== Delta 调制 ====
    "dm_snr": {
        "formula": "SNR_dB = -13.60 + 30 * log10(fs / fm)",
        "description": "Delta 调制 SNR (WCHW 版本)",
        "params": ["fs", "fm"],
        "note": "fs = 采样频率, fm = 最大信号频率。常量 -13.60 来自 WCHW 数据集",
        "category": "信号处理",
        "calculator": None
    },

    # ==== PCM/量化 ====
    "pcm_sqnr": {
        "formula": "SQNR_dB = 6.02 * n + 1.76",
        "description": "PCM 信号-量化噪声比",
        "params": ["n"],
        "note": "n = 每样本比特数",
        "category": "信号处理",
        "calculator": None
    },
    "quantization_levels": {
        "formula": "L = 2^n",
        "description": "量化级别数",
        "params": ["n"],
        "note": "n = 每样本比特数",
        "category": "信号处理",
        "calculator": None
    },
    "pcm_bitrate": {
        "formula": "Rb = fs * n",
        "description": "PCM 比特速率",
        "params": ["fs", "n"],
        "note": "fs = 采样频率, n = 每样本比特数",
        "category": "信号处理",
        "calculator": None
    },

    # ==== Rayleigh 衰落 ====
    "rayleigh_lcr": {
        "formula": "N_R = sqrt(2*pi) * fD * rho * exp(-rho^2)",
        "description": "Rayleigh 衰落电平穿越率",
        "params": ["fD", "rho"],
        "note": "fD = 最大多普勒频率, rho = 阈值/RMS (归一化阈值)",
        "category": "传播",
        "calculator": "rayleigh_level_crossing_rate"
    },
    "rayleigh_afd": {
        "formula": "T_fade = (exp(rho^2) - 1) / (rho * fD * sqrt(2*pi))",
        "description": "Rayleigh 信道平均衰落时长",
        "params": ["fD", "rho"],
        "note": "fD = 多普勒频率, rho = 归一化阈值",
        "category": "传播",
        "calculator": "rayleigh_average_fade_duration"
    },
    "markov_correlation": {
        "formula": "rho = J0(2*pi*fD*Ts)",
        "description": "Markov 模型相关系数",
        "params": ["fD", "Ts"],
        "note": "fD = 多普勒频率, Ts = 符号周期, J0 = Bessel 函数",
        "category": "传播",
        "calculator": None
    },

    # ==== 信道容量 ====
    "shannon_capacity": {
        "formula": "C = B * log2(1 + SNR_linear)",
        "description": "Shannon 信道容量定理",
        "params": ["B", "SNR_dB"],
        "note": "SNR_dB 需转换为线性: SNR_linear = 10^(SNR_dB/10)",
        "category": "信道容量",
        "calculator": "shannon_capacity"
    },

    # ==== 差错控制编码 ====
    "error_detection": {
        "formula": "e_detect = d_min - 1",
        "description": "最大可检测错误数",
        "params": ["d_min"],
        "note": "d_min = 最小码距",
        "category": "编码",
        "calculator": None
    },
    "error_correction": {
        "formula": "e_correct = floor((d_min - 1) / 2)",
        "description": "最大可纠正错误数",
        "params": ["d_min"],
        "note": "d_min = 最小码距",
        "category": "编码",
        "calculator": None
    },

    # ==== 工具 ====
    "db_to_linear": {
        "formula": "linear = 10^(dB/10)",
        "description": "dB 转线性比例",
        "params": ["dB"],
        "note": "用于功率比",
        "category": "工具",
        "calculator": None
    },
    "linear_to_db": {
        "formula": "dB = 10 * log10(linear)",
        "description": "线性比例转 dB",
        "params": ["linear"],
        "note": "用于功率比",
        "category": "工具",
        "calculator": None
    },
    "q_function_inverse": {
        "formula": "Q^(-1)(BER)",
        "description": "常见 BER 目标的逆 Q 函数值",
        "params": ["ber"],
        "note": "Q^(-1)(10^-4)≈3.719, Q^(-1)(10^-5)≈4.265, Q^(-1)(10^-6)≈4.753",
        "category": "工具",
        "calculator": "Q_inverse"
    },
}


def compute_formula(formula_type, params):
    """根据公式类型和参数计算结果"""
    try:
        ftype = formula_type.lower().strip()
        if ftype not in FORMULAS:
            return None

        if ftype == "raised_cosine_bandwidth":
            Rs, alpha = params.get("Rs"), params.get("alpha")
            if Rs is not None and alpha is not None:
                return Rs * (1 + alpha) / 2
        elif ftype == "spectral_efficiency":
            alpha = params.get("alpha")
            if alpha is not None:
                return 2 / (1 + alpha)
        elif ftype == "symbol_rate":
            Rb, M = params.get("Rb"), params.get("M")
            if Rb is not None and M is not None:
                return Rb / math.log2(M)
        elif ftype == "nrz_bandwidth":
            Rb = params.get("Rb")
            if Rb is not None:
                return Rb
        elif ftype == "nyquist_min_bandwidth":
            Rs = params.get("Rs")
            if Rs is not None:
                return Rs / 2
        elif ftype == "bpsk_ber" or ftype == "bfsk_ber" or ftype == "ask_ber":
            Eb_N0 = params.get("Eb_N0")
            if Eb_N0 is not None:
                divisor = 2 if ftype != "bpsk_ber" else 1
                return 0.5 * math.erfc(math.sqrt(Eb_N0 / divisor))
        elif ftype == "dpsk_ber":
            Eb_N0 = params.get("Eb_N0")
            if Eb_N0 is not None:
                return 0.5 * math.exp(-Eb_N0)
        elif ftype == "nc_bfsk_ber":
            Eb_N0 = params.get("Eb_N0")
            if Eb_N0 is not None:
                return 0.5 * math.exp(-Eb_N0 / 2)
        elif ftype == "nakagami_dpsk_ber":
            gamma_b, m = params.get("gamma_b"), params.get("m")
            if gamma_b is not None and m is not None:
                return 0.5 * ((1 + gamma_b / m) ** (-m))
        elif ftype == "carson_bandwidth":
            delta_f, fm = params.get("delta_f"), params.get("fm")
            if delta_f is not None and fm is not None:
                return 2 * (delta_f + fm)
        elif ftype == "fm_snr_improvement":
            beta = params.get("beta")
            if beta is not None:
                return 3 * (beta ** 2) * (beta + 1)
        elif ftype == "am_snr_improvement":
            m = params.get("m")
            if m is not None:
                return 2 * (m ** 2) / (2 + m ** 2)
        elif ftype == "fm_modulation_index":
            delta_f, fm = params.get("delta_f"), params.get("fm")
            if delta_f is not None and fm is not None:
                return delta_f / fm
        elif ftype == "dm_snr":
            fs, fm = params.get("fs"), params.get("fm")
            if fs is not None and fm is not None:
                return -13.60 + 30 * math.log10(fs / fm)
        elif ftype == "pcm_sqnr":
            n = params.get("n")
            if n is not None:
                return 6.02 * n + 1.76
        elif ftype == "quantization_levels":
            n = params.get("n")
            if n is not None:
                return 2 ** n
        elif ftype == "pcm_bitrate":
            fs, n = params.get("fs"), params.get("n")
            if fs is not None and n is not None:
                return fs * n
        elif ftype == "rayleigh_lcr":
            fD, rho = params.get("fD"), params.get("rho")
            if fD is not None and rho is not None:
                return math.sqrt(2 * math.pi) * fD * rho * math.exp(-rho**2)
        elif ftype == "rayleigh_afd":
            fD, rho = params.get("fD"), params.get("rho")
            if fD is not None and rho is not None:
                return (math.exp(rho**2) - 1) / (rho * fD * math.sqrt(2 * math.pi))
        elif ftype == "shannon_capacity":
            B, SNR_dB = params.get("B"), params.get("SNR_dB")
            if B is not None and SNR_dB is not None:
                return B * math.log2(1 + 10 ** (SNR_dB / 10))
        elif ftype == "error_detection":
            d_min = params.get("d_min")
            if d_min is not None:
                return d_min - 1
        elif ftype == "error_correction":
            d_min = params.get("d_min")
            if d_min is not None:
                return math.floor((d_min - 1) / 2)
        elif ftype == "db_to_linear":
            dB = params.get("dB")
            if dB is not None:
                return 10 ** (dB / 10)
        elif ftype == "linear_to_db":
            linear = params.get("linear")
            if linear is not None and linear > 0:
                return 10 * math.log10(linear)
        return None
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="无线通信公式查询与计算")
    parser.add_argument("--formula", type=str, help="公式名称")
    parser.add_argument("--list", action="store_true", help="列出所有公式")
    parser.add_argument("--search", type=str, help="搜索公式 (关键词匹配)")
    parser.add_argument("--category", type=str, help="按分类筛选")
    # 参数
    parser.add_argument("--B", type=float, help="带宽"); parser.add_argument("--SNR_dB", type=float, help="SNR")
    parser.add_argument("--Rs", type=float, help="符号速率"); parser.add_argument("--alpha", type=float, help="滚降因子")
    parser.add_argument("--Rb", type=float, help="比特速率"); parser.add_argument("--M", type=float, help="调制阶数")
    parser.add_argument("--Eb_N0", type=float, help="Eb/N0 线性值"); parser.add_argument("--n", type=int, help="比特数")
    parser.add_argument("--fD", type=float, help="多普勒频率"); parser.add_argument("--rho", type=float, help="归一化阈值")
    parser.add_argument("--delta_f", type=float, help="频率偏移"); parser.add_argument("--fm", type=float, help="调制频率")
    parser.add_argument("--fs", type=float, help="采样频率"); parser.add_argument("--d_min", type=int, help="最小码距")
    parser.add_argument("--beta", type=float, help="调制指数"); parser.add_argument("--m", type=float, help="调制指数(AM)")
    parser.add_argument("--dB", type=float, help="dB 值"); parser.add_argument("--linear", type=float, help="线性值")
    parser.add_argument("--gamma_b", type=float, help="每比特平均SNR")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    if args.list:
        categories = {}
        for fname, info in FORMULAS.items():
            cat = info.get("category", "其他")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(fname)

        print(f"共 {len(FORMULAS)} 个公式:\n")
        for cat in sorted(categories.keys()):
            print(f"[{cat}]")
            for fname in categories[cat]:
                info = FORMULAS[fname]
                print(f"  {fname:<35s} {info['formula']}")
            print()
        return

    if args.search:
        keyword = args.search.lower()
        matched = [(fname, info) for fname, info in FORMULAS.items()
                   if keyword in fname.lower() or keyword in info["description"].lower()
                   or keyword in info.get("category", "").lower()]
        if args.category:
            matched = [(f, i) for f, i in matched if i.get("category") == args.category]
        if matched:
            print(f"搜索 '{args.search}' 匹配 {len(matched)} 个公式:\n")
            for fname, info in matched:
                print(f"  [{info['category']}] {fname}")
                print(f"    公式: {info['formula']}")
                print(f"    描述: {info['description']}")
                print(f"    参数: {', '.join(info['params'])}")
                print(f"    备注: {info['note']}")
                if info.get("calculator"):
                    print(f"    精确计算: telecom_calc.py {info['calculator']}")
                print()
        else:
            print(f"未找到匹配 '{args.search}' 的公式")
        return

    if args.category:
        matched = [(f, i) for f, i in FORMULAS.items() if i.get("category") == args.category]
        print(f"分类 [{args.category}] 共 {len(matched)} 个公式:\n")
        for fname, info in matched:
            print(f"  {fname}: {info['formula']} — {info['description']}")
        return

    if args.formula:
        fname = args.formula.lower()
        info = FORMULAS.get(fname)
        if not info:
            # 模糊匹配
            matches = [f for f in FORMULAS if args.formula.lower() in f.lower()]
            if matches:
                print(f"未找到 '{args.formula}'，你可能想找: {', '.join(matches)}")
            else:
                print(f"未知公式: {args.formula}")
            return

        # 收集参数
        param_aliases = {
            "B": "B", "SNR_dB": "SNR_dB", "Rs": "Rs", "alpha": "alpha",
            "Rb": "Rb", "M": "M", "Eb_N0": "Eb_N0", "n": "n",
            "fD": "fD", "rho": "rho", "delta_f": "delta_f", "fm": "fm",
            "fs": "fs", "d_min": "d_min", "beta": "beta", "m": "m",
            "dB": "dB", "linear": "linear", "gamma_b": "gamma_b"
        }
        params = {}
        for cli_name, internal_name in param_aliases.items():
            value = getattr(args, cli_name, None)
            if value is not None:
                params[internal_name] = value

        result = compute_formula(fname, params) if params else None

        if args.output == "json":
            output = {"name": fname, "formula": info["formula"],
                      "description": info["description"],
                      "params": info["params"], "note": info["note"],
                      "category": info.get("category", ""),
                      "calculator": info.get("calculator"),
                      "computed_result": result}
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print(f"Name:        {fname}")
            print(f"Category:    {info.get('category', 'N/A')}")
            print(f"Formula:     {info['formula']}")
            print(f"Description: {info['description']}")
            print(f"Parameters:  {', '.join(info['params'])}")
            print(f"Note:        {info['note']}")
            if info.get("calculator"):
                print(f"Calculator:  telecom_calc.py {info['calculator']}")
            if result is not None:
                print(f"Result:      {result:.6g}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
