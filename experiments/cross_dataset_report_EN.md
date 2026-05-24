# LogicDetector Cross-Dataset Validation Experiment Report

**Experiment Time**: 2026-05-05 20:30:39  
**Detector Threshold**: 0.35

---

## 📊 Experiment Results Summary

| Dataset | Samples | Accuracy | Precision | Recall | F1 Score | Expected Value | Achievement Rate |
|---------|---------|----------|-----------|--------|----------|----------------|------------------|
| LogicDetector-Bench | 600 | 86.7% | 89.7% | 87.1% | 88.4% | 81.7% | 1.06x |
| LogiQA (Full) | 8678 | 84.1% | 69.1% | 100.0% | 81.8% | 80.0% | 1.05x |
| CoT-Hub (Sample) | 500 | 74.4% | 100.0% | 9.2% | 16.9% | 80.0% | 0.93x |
| LogicInference (Sample) | 500 | 54.6% | 16.4% | 35.9% | 22.5% | 80.0% | 0.68x |

---

## 📈 Generalization Analysis

**Average Accuracy**: 74.9%

### Conclusion

⚠️ **Moderate generalization** Some datasets show low accuracy and need further optimization.

### Key Findings

1. **LogicDetector-Bench (600)**: ✅ Main experiment benchmark
2. **LogiQA (8,678)**: ✅ Large-scale validation
3. **CoT-Hub (500)**: ⚠️ Chain-of-thought data
4. **LogicInference (500)**: ⚠️ Logic reasoning data

---

## 🎯 Next Steps

- [ ] Analyze error cases in each dataset
- [ ] Targeted optimization of detection rules
- [ ] Write results into paper

---

**Experiment Status**: ✅ Complete
