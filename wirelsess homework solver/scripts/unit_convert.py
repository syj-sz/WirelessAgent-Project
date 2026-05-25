#!/usr/bin/env python3
"""
无线通信单位转换 — CLI 接口

用法:
  python unit_convert.py --value 30 --from dBm --to W
  python unit_convert.py --value 1e6 --from Hz --to MHz
  python unit_convert.py --value 3 --from dB --to linear
  python unit_convert.py --list
"""
import sys
import os
import json
import argparse
import math

# 内联转换逻辑
FREQ_UNITS = {"hz": 1, "khz": 1e3, "mhz": 1e6, "ghz": 1e9}
RATE_UNITS = {"bps": 1, "kbps": 1e3, "mbps": 1e6, "gbps": 1e9}
TIME_UNITS = {"s": 1, "ms": 1e-3, "us": 1e-6, "ns": 1e-9}
DIST_UNITS = {"km": 1e3, "m": 1, "cm": 1e-2, "mm": 1e-3}


def convert(value, from_unit, to_unit):
    """执行单位转换"""
    fu = from_unit.lower().strip()
    tu = to_unit.lower().strip()

    # dB <-> linear
    if fu == "db" and tu == "linear":
        return 10 ** (value / 10)
    if fu == "linear" and tu == "db":
        if value <= 0:
            return None  # log(0) / log(negative) 未定义
        return 10 * math.log10(value)

    # dBm <-> W
    if fu == "dbm" and tu == "w":
        return 10 ** ((value - 30) / 10)
    if fu == "w" and tu == "dbm":
        if value <= 0:
            return None
        return 10 * math.log10(value) + 30
    if fu == "dbm" and tu == "mw":
        return 10 ** (value / 10)
    if fu == "mw" and tu == "dbm":
        if value <= 0:
            return None
        return 10 * math.log10(value)

    # 频率
    if fu in FREQ_UNITS and tu in FREQ_UNITS:
        return value * FREQ_UNITS[fu] / FREQ_UNITS[tu]

    # 数据速率
    if fu in RATE_UNITS and tu in RATE_UNITS:
        return value * RATE_UNITS[fu] / RATE_UNITS[tu]

    # 时间
    if fu in TIME_UNITS and tu in TIME_UNITS:
        return value * TIME_UNITS[fu] / TIME_UNITS[tu]

    # 距离
    if fu in DIST_UNITS and tu in DIST_UNITS:
        return value * DIST_UNITS[fu] / DIST_UNITS[tu]

    return None


SUPPORTED = {
    "对数/线性": ["dB", "linear"],
    "功率": ["dBm", "W", "mW"],
    "频率": list(FREQ_UNITS.keys()),
    "数据速率": list(RATE_UNITS.keys()),
    "时间": list(TIME_UNITS.keys()),
    "距离": list(DIST_UNITS.keys()),
}


def main():
    parser = argparse.ArgumentParser(description="无线通信单位转换")
    parser.add_argument("--value", type=float, required=True, help="数值")
    parser.add_argument("--from", dest="from_unit", type=str, required=True, help="源单位")
    parser.add_argument("--to", dest="to_unit", type=str, required=True, help="目标单位")
    parser.add_argument("--list", action="store_true", help="列出支持的单位")
    parser.add_argument("--output", choices=["json", "text"], default="text")

    args = parser.parse_args()

    if args.list:
        print("支持的单位:\n")
        for cat, units in SUPPORTED.items():
            print(f"  [{cat}]: {', '.join(units)}")
        return

    result = convert(args.value, args.from_unit, args.to_unit)

    if args.output == "json":
        out = {"success": result is not None,
               "value": args.value, "from_unit": args.from_unit,
               "to_unit": args.to_unit, "result": result}
        if result is not None:
            out["formatted"] = f"{args.value} {args.from_unit} = {result:.6g} {args.to_unit}"
        else:
            out["error"] = f"Cannot convert from {args.from_unit} to {args.to_unit}"
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        if result is not None:
            print(f"{args.value} {args.from_unit} = {result:.6g} {args.to_unit}")
        else:
            print(f"Error: Cannot convert from '{args.from_unit}' to '{args.to_unit}'")
            print("Use --list to see supported units")


if __name__ == "__main__":
    main()
