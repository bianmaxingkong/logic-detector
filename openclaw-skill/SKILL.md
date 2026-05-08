---
name: logic-detector
description: 逻辑推理幻觉检测。当用户要求分析某段论述是否存在逻辑谬误、推理链不完整、自相矛盾或事实错误时使用。也适用于用户质疑某段AI输出"看着不对劲"、"是不是有逻辑问题"、"帮我分析这段论证"。自动触发「帮我看这段有没有逻辑问题」、「这个论证有问题吗」、「检测一下这段的推理」。不适合检查纯事实性问答题（应使用搜索）。
---

# LogicDetector

现成的逻辑推理幻觉检测器。基于 ACL 2026 论文实现的四模块融合架构，可在本地快速运行。

## 触发方式

当用户要求分析某段文本的逻辑性时，运行：

```bash
python3 /home/baibai/.openclaw/skills/logic-detector/scripts/detect.py "待检测的文本"
```

或通过 stdin 传入：

```bash
echo "待检测的文本" | python3 /home/baibai/.openclaw/skills/logic-detector/scripts/detect.py
```

## 输出解读

脚本返回 JSON，包含：

| 字段 | 含义 |
|------|------|
| `is_hallucination` | true=存在问题，false=逻辑合理 |
| `logic_fallacies` | 检测到的逻辑谬误类型列表（如空=无） |
| `completeness_score` | 推理链完整度 (0-1)，<0.5 表示推理不完整 |
| `is_consistent` | 文本内部是否自洽 |
| `factual_errors` | 事实错误列表（如空=无） |
| `confidence` | 系统对自身判断的置信度 |

## 推理类型

- `deductive` (默认) — 演绎推理，从一般到特殊
- `inductive` — 归纳推理，从特殊到一般
- `causal` — 因果推理
- `analogical` — 类比推理

Example:
```bash
python3 /home/baibai/.openclaw/skills/logic-detector/scripts/detect.py -r causal "因为小明每天都吃苹果，所以他不会生病"
```

## 注意事项

- **首次运行会加载模型**（BGE embedding + CFEVER KB），约1-2秒初始化
- 后续调用较快（~0.8s/次）
- 检测器对中文支持良好，也支持英文
- 简要结果可用 `-q` 参数快速判断
- 当用户只给了文本没指定推理类型时，默认为演绎推理 (deductive)
