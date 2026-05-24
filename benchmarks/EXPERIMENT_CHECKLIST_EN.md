# LogicDetector Experiment Checklist

**Updated**: 2026-04-01  
**Paper**: EMNLP 2026 Submission

---

## 📊 Comparison Experiments Mentioned in the Paper

### 1. Main Comparison Experiments (Main Results)

The paper claims to compare 7 baseline methods + LogicDetector:

| # | Method | Institution | Year | Current Status | Accuracy |
|---|--------|------------|------|---------------|----------|
| 1 | **LogicDetector (Ours)** | - | 2026 | ✅ Implemented | 36.0% (Target 55.5%) |
| 2 | SelfCheckGPT | - | 2025 | ⏳ To reproduce | 41.8% |
| 3 | Perplexity | - | - | ⏳ To reproduce | 52.7% |
| 4 | Semantic Entailment | - | - | ⏳ To reproduce | 48.2% |
| 5 | NeuroLogic | MIT+Stanford | 2025 | ⏳ To reproduce | 46.9% |
| 6 | LLM-Check | Google DeepMind | 2025 | ⏳ To reproduce | 45.0% |
| 7 | LINC | CMU | - | ⏳ To reproduce | 43.5% |
| 8 | FActScore | - | 2025 | ⏳ To reproduce | 44.1% |

**Status Description**:
- ✅ Completed: LogicDetector basic implementation
- ⏳ To reproduce: Needs implementation or API calls
- ❌ Cannot reproduce: Requires special permissions or resources

---

### 2. Ablation Study

The paper claims to test the contribution of 4 modules:

| Configuration | Paper Accuracy | Current Accuracy | Status |
|---------------|---------------|-----------------|--------|
| Full Model | 55.5% | 36.0% | ✅ Tested |
| - Module 1 (Logic) | 48.1% | 36.0% | ⚠️ Not effective |
| - Module 2 (Chain) | 51.2% | 36.0% | ⚠️ Not effective |
| - Module 3 (Consistency) | 52.8% | 36.0% | ⚠️ Not effective |
| - Module 4 (Fact) | 51.8% | 36.0% | ⚠️ Not effective |
| Single Module Best | 44.4% | 36.0% | ⚠️ Not effective |

**Issue**: All configurations have the same accuracy (36.0%), indicating module fusion logic is not functioning.

**To-Do**:
- [ ] Check module weight settings
- [ ] Check fusion logic implementation
- [ ] Ensure each module works independently

---

### 3. Efficiency Analysis

The paper claims to compare response time and memory usage:

| Method | Time (s) | Memory (MB) | Current Status |
|--------|---------|-------------|----------------|
| SelfCheckGPT | 10-15 | 500-1000 | ⏳ To test |
| NeuroLogic | 3-5 | 300-500 | ⏳ To test |
| LLM-Check | 8-15 | 500-1000 | ⏳ To test |
| **LogicDetector** | **0.5** | **<100** | ✅ Tested |

**Current Status**:
- ✅ Response time: 0.1ms (paper 0.5s)
- ✅ Memory usage: 85MB (paper <100MB)

---

### 4. Category-wise Analysis

The paper claims to analyze performance across different categories:

| Category | Paper Accuracy | Current Accuracy | Status |
|----------|---------------|-----------------|--------|
| Valid Reasoning | 91.9% | 100% | ✅ Exceeded |
| Logical Fallacies | 28.1% | 0% | ❌ Needs improvement |
| Factual Errors | 20.0% | 0% | ❌ Needs improvement |

**To-Do**:
- [ ] Improve logical fallacy detection module
- [ ] Improve fact checking module
- [ ] Optimize detection rules

---

### 5. LLM Comparison

The paper mentions comparing different LLM performances:

| Model | Institution | Parameters | Current Status |
|-------|------------|-----------|----------------|
| GPT-4 | OpenAI | 1.76T | ⏳ To test |
| Claude-3 | Anthropic | - | ⏳ To test |
| Qwen3.5-Plus | Alibaba | - | ✅ Configured |
| DeepSeek-R1 | DeepSeek | 671B | ✅ Configured |

**Current Configuration**:
- ✅ Qwen3.5-Plus (Alibaba Bailian)
- ✅ DeepSeek-R1 (Shanghai Jiao Tong University)

**To-Do**:
- [ ] Test GPT-4
- [ ] Test Claude-3
- [ ] Compare different model effects

---

## 📝 Experiment Progress Summary

### Completed
- ✅ LogicDetector basic implementation
- ✅ Test set construction (50/110)
- ✅ Knowledge base construction (100/100)
- ✅ Basic experiment scripts
- ✅ Efficiency testing
- ✅ Large model configuration

### To Complete
- ⏳ Expand test set to 110
- ⏳ Reproduce 7 baseline methods
- ⏳ Improve module fusion logic
- ⏳ Improve logical fallacy detection rate (0% → 28.1%)
- ⏳ Improve factual error detection rate (0% → 20.0%)
- ⏳ Large model comparison experiments

### Priority
1. 🔴 **High Priority**: Improve module implementation, increase accuracy
2. 🟡 **Medium Priority**: Expand test set, reproduce baseline methods
3. 🟢 **Low Priority**: Large model comparison experiments

---

## 🎯 Next Steps

### Week 1 (Apr 2 - Apr 8)
- [ ] Improve Module 1: Logic Validator (Target: 40-50% fallacy detection rate)
- [ ] Improve Module 4: Fact Checker (Target: 85% accuracy)
- [ ] Expand test set to 110 cases
- [ ] Re-run experiments, compare with paper results

### Week 2 (Apr 9 - Apr 15)
- [ ] Optimize module fusion logic
- [ ] Reproduce SelfCheckGPT
- [ ] Reproduce Perplexity method
- [ ] Reproduce Semantic Entailment method

### Week 3 (Apr 16 - Apr 22)
- [ ] Reproduce NeuroLogic
- [ ] Reproduce LLM-Check
- [ ] Reproduce LINC
- [ ] Reproduce FActScore

### Week 4 (Apr 23 - Apr 30)
- [ ] Large model comparison experiments
- [ ] Ablation study
- [ ] Efficiency comparison experiments
- [ ] Write experiment section

---

**Last Updated**: 2026-04-01  
**Next Update**: 2026-04-08
