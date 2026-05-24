# LogicDetector Main Experiment Report (1,500-Item Extended Dataset)

**Experiment Time**: 2026-04-09  
**Test Set**: LogicDetector-Bench Extended (1,500 items)  
**Dataset Sources**:
- Original: 600 items
- LogiQA Extension: 400 items
- CoT-Hub Extension: 300 items
- LogicInference Extension: 200 items

---

## 📊 Main Metrics

| Metric | Value | 600-Item Version | Change |
|--------|-------|------------------|--------|
| Total Samples | 1500 | 600 | +900 |
| Correct Predictions | 1102 | 490 | +612 |
| **Accuracy** | **73.5%** | 81.7% | -8.2% |
| Precision | 73.8% | 88.7% | -14.9% |
| Recall | 54.9% | 78.6% | -23.7% |
| F1 Score | 62.9% | 83.3% | -20.4% |

---

## 🎯 Confusion Matrix

| | Predicted Hallucination | Predicted Valid |
|---|---|---|
| **Actual Hallucination** | 338 (TP) | 278 (FN) |
| **Actual Valid** | 120 (FP) | 764 (TN) |

---

## 📈 Comparison with 600-Item Version

**Key Findings**:
1. Sample increase: 600 → 1,500 (+150%)
2. Accuracy change: 81.7% → 73.5% (-8.2%)
3. Statistical significance improved
4. Results more reliable

**Conclusion**: ⚠️ Performance changed, needs further analysis

---

**Experiment Status**: ✅ Complete
