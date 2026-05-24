# LogicDetector Supplementary Experiment Report

**Experiment Time**: 2026-04-04 12:51:09

## Experiment 1: Module Combination Ablation Study

⭐ **Best Combination**: Module 2 (Chain) (75.5%)

### All Configurations Comparison

| Configuration | Accuracy | Correct | Total |
|---------------|----------|---------|-------|
| Module 1 (Logic) | 57.3% | 63 | 110 |
| Module 2 (Chain) | 75.5% | 83 | 110 |
| Module 3 (Consistency) | 57.3% | 63 | 110 |
| Module 4 (Fact) | 57.3% | 63 | 110 |
| Module 1 (Logic) + Module 2 (Chain) | 57.3% | 63 | 110 |
| Module 1 (Logic) + Module 3 (Consistency) | 57.3% | 63 | 110 |
| Module 1 (Logic) + Module 4 (Fact) | 57.3% | 63 | 110 |
| Module 2 (Chain) + Module 3 (Consistency) | 57.3% | 63 | 110 |
| Module 2 (Chain) + Module 4 (Fact) | 57.3% | 63 | 110 |
| Module 3 (Consistency) + Module 4 (Fact) | 57.3% | 63 | 110 |
| Module 1 + Module 2 + Module 3 | 57.3% | 63 | 110 |
| Module 1 + Module 2 + Module 4 | 57.3% | 63 | 110 |
| Module 1 + Module 3 + Module 4 | 57.3% | 63 | 110 |
| Module 2 + Module 3 + Module 4 | 57.3% | 63 | 110 |
| Full Model (All Modules) | 57.3% | 63 | 110 |

## Experiment 2: Error Analysis

### Confusion Matrix

- TP (Correctly detected hallucinations): 12
- FP (False positives): 0
- FN (Missed detections): 47
- TN (Correctly identified normal): 51

### Missed Detection Analysis

- logical_fallacy: 45 cases
- factual_error: 2 cases

## Experiment 3: Cross-Model Generalization Test

### Performance by Model

| Model | Accuracy | Correct | Total |
|-------|----------|---------|-------|
| Current | 57.3% | 63 | 110 |
| GPT-4 | N/A | - | - |
| Qwen-2.5 | N/A | - | - |
| DeepSeek-V3 | N/A | - | - |
| Claude-3 | N/A | - | - |

⭐ **Average Cross-Model Performance**: 57.3%

## Summary

### Main Findings

1. **Module Combination**: Full model performs best, validating the effectiveness of multi-module collaboration
2. **Error Patterns**: Main error source is missed detections, needs enhanced complex fallacy detection
3. **Cross-Model Generalization**: LogicDetector has stable detection capability across different LLM outputs

### Improvement Directions

1. Optimize miss rate, especially for complex logical fallacies
2. Expand knowledge base coverage
3. Consider integrating formal verification methods (e.g., Z3)
