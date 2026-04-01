# LogicDetector 使用指南

## 📖 简介

LogicDetector 是一个用于检测大语言模型输出中逻辑谬误的框架。

## 🚀 快速开始

### 1. 安装

```bash
cd logic-detector
pip install -r requirements.txt
```

### 2. 基本使用

```python
from src.detector import LogicDetector

# 创建检测器
detector = LogicDetector()

# 分析文本
text = "你的文本内容"
result = detector.analyze(text)

# 查看结果
print(result.summary)
```

## 📊 功能说明

### 逻辑链条分析

LogicDetector 会提取文本中的前提和结论，构建逻辑链条：

```
前提 1 → 前提 2 → 前提 3 → 结论
```

### 逻辑谬误检测

支持检测以下谬误类型：

| 谬误类型 | 说明 | 示例 |
|----------|------|------|
| 滑坡谬误 | 不合理地推断一系列负面后果 | "如果允许 A，就会导致 Z" |
| 确认偏误 | 只关注支持自己观点的信息 | 选择性使用证据 |
| 诉诸权威 | 仅因权威身份而接受观点 | "专家说的，所以是对的" |
| 人身攻击 | 攻击人而非论点 | "他人品不好，所以观点错误" |
| 虚假两难 | 错误地限制选项数量 | "要么 A，要么 B"（忽略 C） |

### 评分系统

| 维度 | 说明 |
|------|------|
| 前提真实性 | ✅ 真实 / ⚠️ 可能 / ❌ 虚假 |
| 推理强度 | ⭐⭐⭐⭐⭐ (1-5 星) |
| 结论可靠性 | 高 / 中 / 低 |

## 🔧 高级用法

### 自定义阈值

```python
detector = LogicDetector(threshold=0.8)
```

### 批量分析

```python
texts = ["文本 1", "文本 2", "文本 3"]
results = [detector.analyze(text) for text in texts]
```

## 📝 示例

查看 `examples/` 目录中的完整示例代码。

## ❓ 常见问题

### Q: 检测准确率如何？
A: 取决于文本类型和复杂度，建议人工复核重要分析。

### Q: 支持哪些语言？
A: 目前主要支持中文和英文。

### Q: 如何贡献新的谬误类型？
A: 欢迎提交 Pull Request！

## 📖 相关资源

- [API 文档](api.md)
- [GitHub 仓库](#)
- [相关论文](../../maven-mvp/output/LogicDetector_论文.pdf)
