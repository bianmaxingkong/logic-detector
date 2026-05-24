# LogicDetector User Guide

## 📖 Introduction

LogicDetector is a framework for detecting logical fallacies in large language model outputs.

## 🚀 Quick Start

### 1. Installation

```bash
cd logic-detector
pip install -r requirements.txt
```

### 2. Basic Usage

```python
from src.detector import LogicDetector

# Create detector
detector = LogicDetector()

# Analyze text
text = "Your text content"
result = detector.analyze(text)

# View results
print(result.summary)
```

## 📊 Feature Description

### Logic Chain Analysis

LogicDetector extracts premises and conclusions from text to construct logic chains:

```
Premise 1 → Premise 2 → Premise 3 → Conclusion
```

### Logical Fallacy Detection

Supports detection of the following fallacy types:

| Fallacy Type | Description | Example |
|--------------|-------------|---------|
| Slippery Slope | Unreasonable inference of a chain of negative consequences | "If A is allowed, it will lead to Z" |
| Confirmation Bias | Only focusing on information that supports one's view | Selective use of evidence |
| Appeal to Authority | Accepting a claim solely because of the authority's identity | "Experts say so, so it's correct" |
| Ad Hominem | Attacking the person rather than the argument | "He has bad character, so his view is wrong" |
| False Dilemma | Incorrectly limiting the number of options | "Either A or B" (ignoring C) |

### Scoring System

| Dimension | Description |
|-----------|-------------|
| Premise Authenticity | ✅ True / ⚠️ Possible / ❌ False |
| Reasoning Strength | ⭐⭐⭐⭐⭐ (1-5 stars) |
| Conclusion Reliability | High / Medium / Low |

## 🔧 Advanced Usage

### Custom Threshold

```python
detector = LogicDetector(threshold=0.8)
```

### Batch Analysis

```python
texts = ["Text 1", "Text 2", "Text 3"]
results = [detector.analyze(text) for text in texts]
```

## 📝 Examples

See the complete example code in the `examples/` directory.

## ❓ Frequently Asked Questions

### Q: How accurate is the detection?
A: Depends on text type and complexity. Manual review of important analyses is recommended.

### Q: What languages are supported?
A: Currently supports Chinese and English.

### Q: How can I contribute new fallacy types?
A: Pull Requests are welcome!

## 📖 Related Resources

- [API Documentation](api.md)
- [GitHub Repository](#)
- [Related Paper](../../maven-mvp/output/LogicDetector_论文.pdf)
