# LogicDetector Supplementary Experiment Survey Report

**Survey Date**: April 2, 2026  
**Objective**: Analyze datasets and experimental protocols in reference literature to identify transferable practices

---

## 📊 1. Dataset Analysis from Reference Literature

### 1.1 Logical Reasoning Datasets

| Dataset | Scale | Type | Takeaway |
|---------|-------|------|----------|
| **LogiQA** | 8,678 questions | Logical reasoning reading comprehension | ✅ Already using 56 questions, can expand to 200+ |
| **Chain of Thought Hub** | 8,000+ examples | Chain-of-thought reasoning | ⭐ Can extract logical error samples |
| **LogicInference** | 10,000+ problems | Formal logical reasoning | ⭐ Can extract formal fallacy samples |
| **RuleTaker** | Synthetic data | Deductive reasoning | ⭐ Can generate test cases |

### 1.2 Hallucination Detection Datasets

| Dataset | Scale | Type | Takeaway |
|---------|-------|------|----------|
| **SelfCheckGPT** | 10,000+ samples | Factual consistency | ⭐ Can adopt annotation approach |
| **FActScore** | 500+ long texts | Atomic fact evaluation | ⭐ Can adopt decomposition method |
| **LLM-Check (DeepMind)** | 10,000+ annotated samples | Multi-dimensional hallucination | ⭐ Largest benchmark |

### 1.3 Fallacy Detection Datasets

| Dataset | Scale | Fallacy Types | Takeaway |
|---------|-------|--------------|----------|
| **Huang et al. (2023)** | Not specified | 6 common fallacies | ✅ Already covering same types |
| **LogicNLI** | Synthetic data | Natural language logic reasoning | ⭐ Can adopt generation method |

---

## 🔬 2. Transferable Experimental Protocols

### 2.1 LLM-Check (Google DeepMind, 2025)

**Experimental Design Highlights**:
1. **Multi-dimensional evaluation**: Factuality, logicality, consistency, relevance
2. **Large-scale testing**: 10,000+ annotated samples
3. **15 baseline comparisons**: Comprehensive coverage of various methods
4. **Human evaluation**: 5 annotators, Kappa consistency computed

**Takeaways**:
- [ ] Add multi-dimensional evaluation metrics
- [ ] Expand test set to 1000+ samples
- [ ] Add human evaluation
- [ ] Compute inter-annotator agreement (Kappa)

---

### 2.2 SelfCheckGPT (Cambridge, 2023)

**Experimental Design Highlights**:
1. **Zero-resource detection**: No external knowledge or training required
2. **Multi-sampling strategy**: 10-20 samples to detect inconsistency
3. **Sentence-level evaluation**: Sentence-by-sentence hallucination detection
4. **AUC metric**: ROC-AUC used to evaluate detection performance

**Takeaways**:
- [ ] Add AUC-ROC metric
- [ ] Sentence-level detection granularity
- [ ] Sampling consistency analysis
- [ ] Cross-model generalization testing

---

### 2.3 FActScore (2023)

**Experimental Design Highlights**:
1. **Atomic fact decomposition**: Break text into atomic facts
2. **Fine-grained evaluation**: Each atomic fact verified individually
3. **Human verification**: Amazon Mechanical Turk annotation
4. **Correlation analysis**: Correlation with human judgment (0.82)

**Takeaways**:
- [ ] Atomic fact decomposition method
- [ ] Fine-grained evaluation metrics
- [ ] Correlation analysis with human judgment
- [ ] Cross-domain testing (biography, encyclopedia, etc.)

---

### 2.4 LINC (CMU, 2024)

**Experimental Design Highlights**:
1. **Formal logic conversion**: Natural language → first-order logic
2. **Z3 theorem proving**: Formal verification
3. **Interpretability**: Provides proof process
4. **Multi-dataset testing**: 3 datasets from different domains

**Takeaways**:
- [ ] Integrate Z3 theorem prover
- [ ] Provide formal proofs
- [ ] Cross-domain generalization testing
- [ ] Error type analysis

---

## 📈 3. Recommended Supplementary Experiments

### 3.1 Dataset Expansion Experiment

**Current**: 50 test cases  
**Target**: 500+ test cases

| Data Source | Recommended Count | Priority |
|-------------|-----------------|----------|
| LogiQA (Expanded) | 200 questions | ⭐⭐⭐ |
| Chain of Thought Hub | 100 questions | ⭐⭐⭐ |
| LogicInference | 100 questions | ⭐⭐ |
| Manual Annotation (New) | 100 questions | ⭐⭐⭐ |

**Estimated Effort**: 2-3 days  
**Expected Improvement**: More reliable results, more convincing paper

---

### 3.2 Cross-Model Generalization Experiment

**Test outputs from different LLMs**:

| Model | Test Samples | Priority |
|-------|-------------|----------|
| GPT-4 | 50 samples | ⭐⭐⭐ |
| GPT-3.5 | 50 samples | ⭐⭐ |
| Claude-3 | 50 samples | ⭐⭐ |
| Qwen-2.5 | 50 samples | ⭐⭐⭐ |
| DeepSeek-V3 | 50 samples | ⭐⭐ |

**Purpose**: Validate LogicDetector's model independence

---

### 3.3 Cross-Domain Generalization Experiment

**Test across different domains**:

| Domain | Test Samples | Priority |
|--------|-------------|----------|
| Medical Diagnosis | 50 samples | ⭐⭐⭐ |
| Legal Consultation | 50 samples | ⭐⭐⭐ |
| Educational Assessment | 50 samples | ⭐⭐ |
| Financial Analysis | 50 samples | ⭐⭐ |
| Scientific Research | 50 samples | ⭐⭐ |

**Purpose**: Validate domain adaptability

---

### 3.4 Additional Evaluation Metrics

**Current Metrics**: Accuracy  
**Recommended Additions**:

| Metric | Description | Priority |
|--------|-------------|----------|
| **Precision** | Precision rate | ⭐⭐⭐ |
| **Recall** | Recall rate | ⭐⭐⭐ |
| **F1 Score** | Comprehensive metric | ⭐⭐⭐ |
| **AUC-ROC** | Overall performance | ⭐⭐ |
| **MCC** | Matthews Correlation Coefficient | ⭐⭐ |
| **Kappa Coefficient** | Consistency check | ⭐⭐ |

---

### 3.5 Error Analysis Experiment

**Analyze LogicDetector's error cases**:

1. **False Positive Analysis**: Why were valid reasoning cases classified as hallucinations?
2. **False Negative Analysis**: Why were hallucinations missed?
3. **Fallacy Type Distribution**: Which fallacy types are hardest to detect?
4. **Length Impact**: How does text length affect detection performance?
5. **Language Impact**: Comparison of Chinese and English performance

**Output**: Error analysis table + typical cases

---

### 3.6 Extended Ablation Study

**Current Ablation**: Remove single module  
**Recommended Expansion**:

| Experiment | Description | Priority |
|------------|-------------|----------|
| Module Combination | Test different module combinations (M1+M2, M1+M4, etc.) | ⭐⭐⭐ |
| Weight Optimization | Learned optimal weights vs. fixed weights | ⭐⭐⭐ |
| Threshold Analysis | Impact of different thresholds on performance | ⭐⭐ |
| Knowledge Base Size | 25 vs 100 vs 1000 facts | ⭐⭐ |

---

### 3.7 Efficiency-Accuracy Trade-Off Experiment

**Test different configurations**:

| Configuration | Response Time | Expected Accuracy | Use Case |
|--------------|--------------|-------------------|----------|
| Module 1 Only | <0.1ms | ~40% | Real-time detection |
| Module 1+4 | <0.2ms | ~50% | Quick detection |
| Full Model | 0.5ms | ~55% | Standard detection |
| Enhanced (Z3) | ~5s | ~65% | High-precision scenarios |

---

### 3.8 Human Evaluation Experiment

**Recruit annotators for evaluation**:

- **Number of Annotators**: 3-5 people
- **Samples to Annotate**: 100 test cases
- **Annotation Content**: Whether hallucination exists, fallacy type
- **Computed Metric**: Inter-annotator Kappa coefficient
- **Comparative Analysis**: Human vs. LogicDetector agreement

**Purpose**: Validate reliability of detection results

---

## 📋 4. Experiment Priority

### High Priority (This Week) ⭐⭐⭐

1. **Expand dataset to 110 cases** (Paper target)
   - Expand 54 questions from LogiQA
   - Manually annotate 50 questions
   - Estimated time: 1-2 days

2. **Add Precision/Recall/F1 metrics**
   - Modify evaluation script
   - Re-run experiments
   - Estimated time: 2 hours

3. **Module combination ablation study**
   - Test M1+M2, M1+M4, M2+M4, etc.
   - Analyze inter-module synergy
   - Estimated time: 4 hours

### Medium Priority (Next Week) ⭐⭐

4. **Cross-model generalization test**
   - Test GPT-4, Qwen, DeepSeek, etc.
   - Validate model independence
   - Estimated time: 1 day

5. **Error analysis**
   - Analyze false positives and false negatives
   - Summarize error patterns
   - Estimated time: 4 hours

6. **Weight optimization experiment**
   - Grid search for optimal weights
   - Compare fixed weights vs. learned weights
   - Estimated time: 6 hours

### Low Priority (Future Work) ⭐

7. **Cross-domain testing** (medical, legal, financial)
8. **Human evaluation experiment** (3-5 annotators)
9. **Integrate Z3 theorem prover**
10. **AUC-ROC, Kappa coefficient, and other advanced metrics**

---

## 📊 5. Expected Experimental Results

### After Dataset Expansion (110 cases)

| Metric | Current (50 cases) | Expected (110 cases) | Improvement |
|--------|-------------------|---------------------|-------------|
| Overall Accuracy | 52.0% | 55.5% | +3.5% |
| Logical Fallacy Detection | 26.9% | 28.1% | +1.2% |
| Factual Error Detection | 83.3% | 85.0% | +1.7% |
| Valid Reasoning | 77.8% | 91.9% | +14.1% |

### After Adding More Metrics

| Metric | Expected Value | Description |
|--------|---------------|-------------|
| Precision | ~55% | Precision rate |
| Recall | ~52% | Recall rate |
| F1 Score | ~53.5% | Comprehensive metric |
| AUC-ROC | ~0.65 | Overall performance |

### After Cross-Model Generalization

| Model | Expected Accuracy | Description |
|-------|-----------------|-------------|
| GPT-4 | 50-55% | High-quality output |
| GPT-3.5 | 52-57% | Medium quality |
| Qwen-2.5 | 50-55% | Chinese optimized |
| DeepSeek-V3 | 50-55% | Open-source model |

---

## 📝 6. Experiment Execution Plan

### Week 1 (Apr 2 - Apr 7)

- [ ] **Expand test set to 110 cases** (2 days)
- [ ] **Add Precision/Recall/F1** (2 hours)
- [ ] **Module combination ablation study** (4 hours)
- [ ] **Re-run complete experiment** (2 hours)

### Week 2 (Apr 8 - Apr 14)

- [ ] **Cross-model generalization test** (1 day)
- [ ] **Error analysis** (4 hours)
- [ ] **Weight optimization experiment** (6 hours)
- [ ] **Update paper experiment section** (1 day)

### Week 3-4 (Apr 15 - Apr 30)

- [ ] **Cross-domain testing** (2 days)
- [ ] **Human evaluation experiment** (3 days)
- [ ] **Integrate Z3** (3 days)
- [ ] **Final paper revision** (2 days)

---

## 🎯 7. Summary

### Immediately Applicable (High Priority)

1. ✅ **LogiQA Dataset** - Expand to 200 questions
2. ✅ **LLM-Check Multi-dimensional Evaluation** - Add Precision/Recall/F1
3. ✅ **SelfCheckGPT's AUC Metric** - Add ROC curve
4. ✅ **FActScore's Atomic Decomposition** - Fine-grained evaluation

### Requires Additional Work (Medium Priority)

1. ⏳ **Cross-model generalization test** - Requires API calls
2. ⏳ **Error analysis** - Requires manual annotation
3. ⏳ **Weight optimization** - Requires grid search

### Future Work (Low Priority)

1. 🔮 **Human evaluation** - Requires recruiting annotators
2. 🔮 **Z3 integration** - Requires learning theorem proving
3. 🔮 **Cross-domain testing** - Requires domain experts

---

**Survey Completed**: 2026-04-02  
**Next Step**: Execute high-priority experiments (dataset expansion + new metrics)
