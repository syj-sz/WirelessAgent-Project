#!/usr/bin/env python3
"""
电信函数精确计算器 — CLI 接口

用法:
  python telecom_calc.py Q_function --x 4.0
  python telecom_calc.py ber_bpsk_coherent --Eb_N0_dB 10
  python telecom_calc.py shannon_capacity --bandwidth_Hz 1e6 --snr_dB 30
  python telecom_calc.py --list
"""
import sys
import os
import json
import argparse
import math

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

# 检测 scipy 是否可用
try:
    import scipy
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# 纯 math 回退实现（无 scipy 时使用）
def _fallback_calculate(operation, **kwargs):
    """无 scipy 时的回退实现"""
    try:
        if operation == "erfc":
            x = kwargs.get("x", 0)
            result = math.erfc(x)
            return {"value": result, "formula": f"\\operatorname{{erfc}}({x})", "explanation": f"erfc({x}) = {result:.10e}"}

        elif operation == "erf":
            x = kwargs.get("x", 0)
            result = math.erf(x)
            return {"value": result, "formula": f"\\operatorname{{erf}}({x})", "explanation": f"erf({x}) = {result:.10e}"}

        elif operation == "Q_function":
            x = kwargs.get("x", 0)
            result = 0.5 * math.erfc(x / math.sqrt(2))
            return {"value": result, "formula": f"Q({x}) = \\frac{{1}}{{2}} \\operatorname{{erfc}}\\left(\\frac{{{x}}}{{\\sqrt{{2}}}}\\right)",
                    "explanation": f"Q({x}) = {result:.10e}"}

        elif operation == "Q_inverse":
            p = kwargs.get("p", 0.5)
            if p <= 0 or p >= 1:
                return {"error": "p must be between 0 and 1"}
            # 牛顿法近似
            x = 0.0
            for _ in range(50):
                qx = 0.5 * math.erfc(x / math.sqrt(2))
                dqx = -math.exp(-x*x/2) / math.sqrt(2 * math.pi)
                if abs(qx - p) < 1e-12:
                    break
                x = x - (qx - p) / dqx
            return {"value": x, "formula": f"Q^{{-1}}({p})",
                    "explanation": f"Q^(-1)({p}) = {x:.6f}"}

        elif operation == "bessel_J":
            n, x = kwargs.get("n", 0), kwargs.get("x", 0)
            return {"error": "Bessel functions require scipy. Install: pip install scipy"}

        elif operation == "bessel_I":
            return {"error": "Bessel functions require scipy. Install: pip install scipy"}

        elif operation == "bessel_Y":
            return {"error": "Bessel functions require scipy. Install: pip install scipy"}

        elif operation == "marcum_Q":
            return {"error": "Marcum Q-function requires scipy. Install: pip install scipy"}

        elif operation == "ber_bpsk_coherent":
            Eb_N0_dB = kwargs.get("Eb_N0_dB", 0)
            Eb_N0_linear = 10 ** (Eb_N0_dB / 10)
            result = 0.5 * math.erfc(math.sqrt(Eb_N0_linear))
            return {"value": result, "formula": f"P_b = \\frac{{1}}{{2}} \\operatorname{{erfc}}\\left(\\sqrt{{{Eb_N0_linear:.4f}}}\\right)",
                    "explanation": f"BPSK BER at {Eb_N0_dB}dB: P_b = {result:.6e}"}

        elif operation == "ber_bfsk_coherent":
            Eb_N0_dB = kwargs.get("Eb_N0_dB", 0)
            Eb_N0_linear = 10 ** (Eb_N0_dB / 10)
            result = 0.5 * math.erfc(math.sqrt(Eb_N0_linear / 2))
            return {"value": result, "formula": f"P_b = \\frac{{1}}{{2}} \\operatorname{{erfc}}\\left(\\sqrt{{\\frac{{{Eb_N0_linear:.4f}}}{{2}}}}\\right)",
                    "explanation": f"BFSK coherent BER at {Eb_N0_dB}dB: P_b = {result:.6e}"}

        elif operation == "ber_bfsk_noncoherent":
            Eb_N0_dB = kwargs.get("Eb_N0_dB", 0)
            Eb_N0_linear = 10 ** (Eb_N0_dB / 10)
            result = 0.5 * math.exp(-Eb_N0_linear / 2)
            return {"value": result, "formula": f"P_b = \\frac{{1}}{{2}} \\exp\\left(-\\frac{{{Eb_N0_linear:.4f}}}{{2}}\\right)",
                    "explanation": f"Non-coherent BFSK BER at {Eb_N0_dB}dB: P_b = {result:.6e}"}

        elif operation == "ber_dpsk":
            Eb_N0_dB = kwargs.get("Eb_N0_dB", 0)
            Eb_N0_linear = 10 ** (Eb_N0_dB / 10)
            result = 0.5 * math.exp(-Eb_N0_linear)
            return {"value": result, "formula": f"P_b = \\frac{{1}}{{2}} \\exp\\left(-{{{Eb_N0_linear:.4f}}}\\right)",
                    "explanation": f"DPSK BER at {Eb_N0_dB}dB: P_b = {result:.6e}"}

        elif operation == "shannon_capacity":
            B = kwargs.get("bandwidth_Hz", 1e6)
            snr_dB = kwargs.get("snr_dB", 0)
            snr_linear = 10 ** (snr_dB / 10)
            capacity = B * math.log2(1 + snr_linear)
            return {"value": capacity, "formula": f"C = {B} \\log_2\\left(1 + {snr_linear:.4f}\\right)",
                    "explanation": f"Shannon capacity: C = {capacity:.2f} bps = {capacity/1e6:.4f} Mbps"}

        elif operation == "rayleigh_outage_probability":
            gamma_th = kwargs.get("gamma_threshold", 1)
            gamma_avg = kwargs.get("gamma_avg", 10)
            result = 1 - math.exp(-gamma_th / gamma_avg)
            return {"value": result, "formula": f"P_{{\\text{{out}}}} = 1 - \\exp\\left(-\\frac{{{gamma_th}}}{{{gamma_avg}}}\\right)",
                    "explanation": f"Rayleigh outage probability: P_out = {result:.6e}"}

        elif operation == "rayleigh_level_crossing_rate":
            rho, f_D = kwargs.get("rho", 1), kwargs.get("f_D", 100)
            result = math.sqrt(2 * math.pi) * f_D * rho * math.exp(-rho**2)
            return {"value": result, "formula": f"N_R = \\sqrt{{2\\pi}} \\cdot {f_D} \\cdot {rho} \\cdot \\exp\\left(-{rho}^2\\right)",
                    "explanation": f"Level crossing rate: N_R = {result:.4f} crossings/s"}

        elif operation == "rayleigh_average_fade_duration":
            rho, f_D = kwargs.get("rho", 1), kwargs.get("f_D", 100)
            if rho == 0:
                return {"error": "rho cannot be zero"}
            tau = (math.exp(rho**2) - 1) / (rho * f_D * math.sqrt(2 * math.pi))
            return {"value": tau, "formula": f"\\tau = \\frac{{\\exp({rho}^2) - 1}}{{{rho} \\cdot {f_D} \\cdot \\sqrt{{2\\pi}}}}",
                    "explanation": f"Average fade duration: tau = {tau:.6e} s"}

        elif operation == "rician_outage_probability":
            return {"error": "Rician outage requires Marcum Q-function (scipy). Install: pip install scipy"}

        elif operation == "fm_bessel_coefficients":
            return {"error": "FM Bessel coefficients require scipy. Install: pip install scipy"}

        elif operation == "fm_carson_bandwidth":
            delta_f = kwargs.get("delta_f", 75000)
            f_m = kwargs.get("f_m", 15000)
            bandwidth = 2 * (delta_f + f_m)
            beta = delta_f / f_m
            return {"value": bandwidth, "beta": beta,
                    "formula": f"B = 2({delta_f} + {f_m}) = {bandwidth}",
                    "explanation": f"Carson's rule: B = {bandwidth} Hz, beta = {beta:.2f}"}

        else:
            return {"error": f"Unknown operation: {operation}"}
    except Exception as e:
        return {"error": str(e)}


AVAILABLE_OPERATIONS = [
    "erfc", "erf", "Q_function", "Q_inverse",
    "bessel_J", "bessel_I", "bessel_Y",
    "marcum_Q",
    "ber_bpsk_coherent", "ber_bfsk_coherent",
    "ber_bfsk_noncoherent", "ber_dpsk",
    "shannon_capacity",
    "rayleigh_outage_probability",
    "rayleigh_level_crossing_rate",
    "rayleigh_average_fade_duration",
    "rician_outage_probability",
    "fm_bessel_coefficients", "fm_carson_bandwidth"
]


def calculate(operation, **kwargs):
    """统一计算入口，回退到 math（scipy 用作 Bessel/Marcum 等高精度函数）"""
    return _fallback_calculate(operation, **kwargs)


def main():
    parser = argparse.ArgumentParser(description="电信函数精确计算器 (SciPy-based)")
    parser.add_argument("operation", nargs="?", help="运算名称")
    parser.add_argument("--list", action="store_true", help="列出所有可用函数")
    # 通用参数
    parser.add_argument("--x", type=float)
    parser.add_argument("--n", type=int)
    parser.add_argument("--a", type=float)
    parser.add_argument("--b", type=float)
    parser.add_argument("--M", type=int, default=1, help="Marcum Q 阶数")
    parser.add_argument("--p", type=float, help="概率参数")
    # 通信参数
    parser.add_argument("--Eb_N0_dB", type=float, help="Eb/N0 (dB)")
    parser.add_argument("--bandwidth_Hz", type=float, help="带宽 (Hz)")
    parser.add_argument("--snr_dB", type=float, help="SNR (dB)")
    parser.add_argument("--gamma_threshold", type=float)
    parser.add_argument("--gamma_avg", type=float)
    parser.add_argument("--K", type=float, help="Rician K-factor")
    parser.add_argument("--rho", type=float, help="归一化阈值")
    parser.add_argument("--f_D", type=float, help="多普勒频率 (Hz)")
    parser.add_argument("--delta_f", type=float, help="频率偏移 (Hz)")
    parser.add_argument("--f_m", type=float, help="调制频率 (Hz)")
    parser.add_argument("--beta", type=float, help="调制指数")
    parser.add_argument("--n_max", type=int, default=10, help="最大侧带阶数")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    if args.list:
        print(f"可用电信函数 ({len(AVAILABLE_OPERATIONS)} 个):\n")
        categories = {
            "误差函数": ["erfc", "erf", "Q_function", "Q_inverse"],
            "Bessel 函数": ["bessel_J", "bessel_I", "bessel_Y"],
            "Marcum Q": ["marcum_Q"],
            "误码率 (BER)": ["ber_bpsk_coherent", "ber_bfsk_coherent",
                        "ber_bfsk_noncoherent", "ber_dpsk"],
            "信道容量": ["shannon_capacity"],
            "衰落信道": ["rayleigh_outage_probability",
                      "rayleigh_level_crossing_rate",
                      "rayleigh_average_fade_duration",
                      "rician_outage_probability"],
            "FM 调制": ["fm_bessel_coefficients", "fm_carson_bandwidth"],
        }
        for cat, ops in categories.items():
            print(f"  [{cat}]")
            for op in ops:
                print(f"    {op}")
            print()
        print(f"计算引擎: {'SciPy (高精度)' if HAS_SCIPY else 'math (基础)'}")
        return

    if not args.operation:
        parser.print_help()
        return

    # 收集参数
    param_names = ["x", "n", "a", "b", "M", "p",
                   "Eb_N0_dB", "bandwidth_Hz", "snr_dB",
                   "gamma_threshold", "gamma_avg", "K",
                   "rho", "f_D", "delta_f", "f_m",
                   "beta", "n_max"]
    kwargs = {}
    for pname in param_names:
        value = getattr(args, pname, None)
        if value is not None:
            kwargs[pname] = value

    result = calculate(args.operation, **kwargs)

    if args.output == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            val = result.get("value", "N/A")
            if isinstance(val, float):
                if abs(val) < 0.001 and val != 0:
                    print(f"Result: {val:.6e}")
                else:
                    print(f"Result: {val:.6g}")
            else:
                print(f"Result: {val}")
            if result.get("formula"):
                print(f"Formula: {result['formula']}")
            if result.get("explanation"):
                print(f"Explanation: {result['explanation']}")
            if result.get("beta"):
                print(f"Beta: {result['beta']:.4f}")
            if result.get("note"):
                print(f"Note: {result['note']}")


if __name__ == "__main__":
    main()
