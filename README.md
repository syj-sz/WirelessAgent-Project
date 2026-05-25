# 🦞 WirelessAgent — 小龙虾·无线智能体

<p align="center">
  <strong>面向无线通信领域的专业 AI 智能体平台</strong><br>
  习题解答 · 标准检索 · 论文速递 · 网络规划 · 报告生成
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Python-3.10+-yellow" alt="Python">
  <img src="https://img.shields.io/badge/framework-LangGraph-orange" alt="LangGraph">
  <img src="https://img.shields.io/badge/LLM-Claude%20%7C%20GPT%20%7C%20Gemini-purple" alt="LLM">
</p>

---

## 📖 项目简介

**WirelessAgent（小龙虾）** 是一个面向无线通信领域的专业 AI 智能体平台，依托大语言模型（LLM）智能体能力，结合无线通信领域的课程知识、3GPP/ITU 标准文档、前沿论文和工程案例，为无线通信方向的学生、网络工程师、科研人员和从业者提供高效、准确、可追溯的 AI 辅助服务。

本项目基于以下前期研究：
- **WirelessAgent** (China Communications, 2025) — 基于 LLM 的无线网络智能体框架，采用 LangGraph 工作流与 Human-in-the-loop 机制
- **WirelessAgent++** (arXiv, 2026) — 引入领域自适应 MCTS 算法，实现工作流与工具的联合自动优化
- **WirelessBench** — 面向无线网络的容忍度感知、工具集成的评测基准（WCHW / WCNS / WCMSA）
- **AgentX Competition** (UC Berkeley, 2026) — 国际智能体竞赛验证框架竞争力

---

## ✨ 核心功能

| 模块 | 说明 | 状态 |
|------|------|------|
| 🧮 **习题解答** (Homework Solver) | 覆盖信号与系统、通信原理、MIMO、OFDM、信道编码等课程，支持 LaTeX 输入、分步推导、知识点关联 | MVP |
| 📡 **标准检索** (Standard Search) | 3GPP/ITU/IEEE 标准文档语义检索，自然语言查询，参数速查 | Phase 2 |
| 📄 **论文速递** (Paper Digest) | arXiv/JSAC/TWC 等每日论文抓取，中文摘要生成，研究方向定制推送 | Phase 2 |
| 📶 **网络规划** (Network Planning) | 基站部署方案生成、网络切片配置、链路预算与覆盖评估 | Phase 3 |
| 📊 **报告生成** (Report Generator) | 实验报告/技术调研/方案设计自动生成，多格式模板导出 | Phase 2 |
| 🏆 **WirelessBench 评测** | WCHW 习题评测基准，四维评分体系（公式/数值/单位/步骤），持续评估 Agent 性能 | Phase 1 |

---

## 🏗️ 技术架构
---
┌─────────────────────────────────────────────────────┐
│                 前端 (React / Next.js)                │
│         对话界面  ·  报告预览  ·  用户中心              │
├─────────────────────────────────────────────────────┤
│                  API 网关 (FastAPI)                   │
│         用户认证  ·  请求路由  ·  限流  ·  日志         │
├─────────────────────────────────────────────────────┤
│              智能体核心 (Agent Core)                   │
│  ┌─────────────────┬─────────────────────────┐      │
│  │ 工序设计 (MCTS)   │ 工序执行 (LangGraph)      │      │
│  │ · 任务分解        │ · ReAct 工具调用           │      │
│  │ · 工具选择        │ · 状态管理                │      │
│  │ · 工作流自动优化   │ · Human-in-the-loop      │      │
│  └─────────────────┴─────────────────────────┘      │
├─────────────────────────────────────────────────────┤
│          工具层 (数学求解器 · 仿真接口 · 检索 · 计算)    │
├─────────────────────────────────────────────────────┤
│    数据与知识层 (向量数据库 · 知识图谱 · 文档存储)       │
├─────────────────────────────────────────────────────┤
│      基础设施 (Claude/GPT/Gemini · GPU · O-RAN)      │
└─────────────────────────────────────────────────────┘
```

### 技术选型

| 层次 | 技术 |
|------|------|
| **LLM 后端** | Claude Opus / GPT / Gemini（多模型路由） |
| **Agent 框架** | LangGraph + 自研 MCTS 引擎 |
| **RAG 检索** | 向量数据库 (Milvus/Pinecone) + 混合检索 |
| **前端** | React + Next.js + Tailwind CSS |
| **后端** | Python (FastAPI) + Node.js |
| **数据库** | PostgreSQL + Redis |
| **评测体系** | WirelessBench (WCHW + WCNS + WCMSA) |

---


## 📊 WCHW 评测基准

WirelessBench-WCHW 覆盖无线通信 6 大核心主题、449 道习题，采用四维评分体系：

| 评分维度 | 权重 | 说明 |
|----------|------|------|
| 公式准确性 | 35% | 推导过程和最终公式的正确性 |
| 数值精度 | 25% | 计算结果数值的精确度 |
| 单位正确性 | 20% | 物理单位的正确使用与转换 |
| 步骤逻辑 | 20% | 解题步骤的逻辑完整性与清晰度 |

### 基准结果

| 方法 | 准确率 | 提升 |
|------|--------|------|
| Original (Qwen-Turbo) | 58.34% | — |
| CoT | 60.32% | +1.98% |
| MedPrompt | 61.22% | +2.88% |
| AFlow | 69.92% | +11.58% |
| **WirelessAgent (Ours)** | **77.94%** | **+19.60%** |

---

## 🗺️ 路线图

- [x] **Phase 1** — 前后端框架、习题解答模块、WirelessBench-WCHW 上线
- [ ] **Phase 2** — MCTS 自动化工序设计、标准检索、论文速递、报告生成
- [ ] **Phase 3** — 网络规划辅助、O-RAN 数据生成、多模型路由
- [ ] **Phase 4** — 规模化运营 (5,000 MAU)、商业化探索、英文版上线

---

## 📄 参考文献

1. Tong J, Guo W, Shao J, et al. **WirelessAgent: Large Language Model Agents for Intelligent Wireless Networks**. *China Communications*, Nov., 2025.
2. Tong J, Li Z, Liu F, et al. **WirelessAgent++: Automated Agentic Workflow Design and Benchmarking for Wireless Networks**. *arXiv:2603.00501*, 2026.

---
<p align="center">
  <sub>Made with ❤️ by WirelessAgent Working Group</sub>
</p>
