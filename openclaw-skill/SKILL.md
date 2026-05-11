---
name: logic-detector
description: 逻辑推理幻觉检测。当用户要求分析某段论述是否存在逻辑谬误、推理链不完整、自相矛盾或事实错误时使用。也适用于用户质疑某段AI输出"看着不对劲"、"是不是有逻辑问题"、"帮我分析这段论证"。自动触发「帮我看这段有没有逻辑问题」、「这个论证有问题吗」、「检测一下这段的推理」。不适合检查纯事实性问答题（应使用搜索）。
setup:
  - type: git_clone
    repo: https://github.com/bianmaxingkong/logic-detector.git
    dest: "{{skill_dir}}/repo"
  - type: pip_install
    requirements: "{{skill_dir}}/repo/requirements.txt"
  - type: run_script
    script: "{{skill_dir}}/scripts/download_models.py"
    description: 下载 BGE embedding 模型和 CFEVER 知识库
---

# LogicDetector

基于 ACL 2026 论文实现的四模块融合架构，无需大模型，轻量级逻辑推理幻觉检测器。

**论文**: LogicDetector: Multi-Module Fusion for Logic Reasoning Hallucination Detection (ACL 2026)

## 快速开始

检测器无需任何 API key，完全本地运行。

### 下载工程（首次使用）

```bash
# 克隆仓库（如尚未克隆）
git clone https://github.com/bianmaxingkong/logic-detector.git /path/to/logic-detector
cd /path/to/logic-detector

# 安装依赖
pip install -r requirements.txt

# 下载模型文件
python3 openclaw-skill/scripts/download_models.py
```

### 基础用法

```bash
# 方式一：通过管道
echo "如果下雨地就会湿，地湿了，所以下过雨" | python3 src/detect.py

# 方式二：直接传参
python3 src/detect.py "他在这领域是专家，所以他说的一定对"

# 方式三：指定推理类型
python3 src/detect.py -r causal "因为小明每天都吃苹果，所以他不会生病"
```

## 项目结构

```
logic-detector/
├── src/
│   ├── detector.py            # 主检测引擎入口
│   ├── __init__.py            # 包定义
│   └── modules/
│       ├── logic_validator.py      # M1: 逻辑规则验证（230+ pattern，26种谬误）
│       ├── chain_checker.py        # M2: 推理链完整性检查
│       ├── self_consistency.py     # M3: 自洽性验证
│       └── fact_checker.py         # M4: 基于知识库的事实检查
├── data/
│   ├── cfever_index/               # CFEVER 知识库（FAISS index）
│   └── test_set_*.json             # 测试数据集
├── openclaw-skill/
│   ├── SKILL.md                    # 本技能文件
│   └── scripts/
│       ├── detect.py               # 检测脚本（最终使用入口）
│       └── download_models.py      # 模型下载脚本
└── requirements.txt                # Python 依赖
```

## 四模块架构

| 模块 | 名称 | 功能 | 时间 |
|------|------|------|------|
| M1 | LogicValidator | 230+ regex模式检测26种逻辑谬误 | <10ms |
| M2 | ChainChecker | 验证推理链是否完整（模板+embedding） | 35ms |
| M3 | ConsistencyVerifier | 多策略文本重构检测语义矛盾 | <150ms |
| M4 | FactChecker | CFEVER知识库（18,305条）事实核查 | <100ms |

融合权重: M1=0.4, M2=0.3, M3=0.2, M4=0.1（论文实验确定的最优配置）

M1和M4有否决权（硬投票），M2有条件否决（分数<0.5且M4未确认事实时触发）

## 输出格式

### JSON 结果字段

```json
{
  "is_hallucination": true,      // true=存在问题 false=逻辑合理
  "confidence": 0.9234,          // 置信度 (0-1)
  "logic_fallacies": [           // 检测到的谬误列表
    {
      "type": "affirming_consequent",
      "pattern": "If P then Q, Q, therefore P"
    }
  ],
  "completeness_score": 0.35,    // 推理完整度 (<0.5=不完整)
  "is_consistent": false,        // 文本是否自洽
  "factual_errors": [            // 事实错误列表
    "地球是平的，这是科学事实"
  ],
  "explanation": "..."           // 详细解释
}
```

### 命令行选项

| 参数 | 简写 | 说明 |
|------|------|------|
| `--reasoning` | `-r` | 推理类型: `deductive`(默认), `inductive`, `causal`, `analogical` |
| `--verbose` | `-v` | 输出详细解释 |
| `--quiet` | `-q` | 简略输出: 1=幻觉, 0=正常 |

## 推理类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| **deductive** | 演绎推理，一般→特殊 | 所有人都会死，苏格拉底是人→苏格拉底会死 |
| **inductive** | 归纳推理，特殊→一般 | 观察到100只天鹅都是白的→天鹅都是白的 |
| **causal** | 因果推理，因→果 | 吸烟导致肺癌 |
| **analogical** | 类比推理，A≈B→结论类推 | 地球和火星都有大气层→火星可能有生命 |

默认使用 deductive，检测器会自动推断。如果知道输入文本的推理类型，指定 `-r` 可提高准确率。

## 依赖

- Python >= 3.8
- transformers
- sentence-transformers
- faiss-cpu
- numpy
- z3-solver（逻辑规则验证）

模型文件（首次自动下载）：
- BAAI/bge-small-zh-v1.5（33MB 中文embedding模型）
- CFEVER 知识库（FAISS index + metadata，~50MB）

## 注意事项

- **首次运行**会加载模型，约1-2秒初始化
- **后续调用**约0.8秒/次
- 对中文支持良好，也支持英文输入
- 论文验证准确率：LogiQA 92.1%，LogicInference 88.6%，跨5个数据集
- 内存占用：<100MB
- **零**误报率（zero false positives on LogiQA）
