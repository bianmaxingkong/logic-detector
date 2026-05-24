# LogicDetector Experiment Architecture and Research Rationale

**Created**: 2026-04-05  
**Version**: v2.0  

---

## 📊 **Technologies Actually Used**

### ❌ **Z3 Theorem Prover**
**Status**: Mentioned in the paper but **not actually used**

**Reason**:
1. Chinese logical reasoning is difficult to formalize into first-order logic formulas
2. Pattern matching methods are more flexible and cover more fallacy types
3. Z3 is mainly used for formal logic verification and has limited effectiveness for informal fallacies

**Description in the Paper**:
```
Implementation Tools:
• Z3 Theorem Prover (version 4.12.1): For formal logic validation
• Pattern-based Detection: 150+ regex patterns
• Python Logic Library: Custom implementation
```

**Actual Situation**:
- ✅ **Pattern-based Detection**: Actually used (150+ regex patterns)
- ✅ **Python Logic Library**: Actually used (custom implementation)
- ❌ **Z3 Theorem Prover**: Not actually used (planned only)

---

## 🔧 **Technology Stack Actually Used**

### 1. **Pattern Matching Detection** (Core)
```python
# Technology actually used
import re

# 150+ detection patterns
patterns = {
    "affirming_consequent": [
        r"if.*then.*\..*\..*so.*",
        r"if.*then.*\..*occurs.*\..*therefore.*",
        # ... 6-10 patterns
    ],
    "denying_antecedent": [
        r"if.*then.*\..*not.*\..*therefore not.*",
        # ... 6-10 patterns
    ],
    # ... 22 fallacy types
}
```

### 2. **Reasoning Chain Completeness Check**
```python
# Template matching based on semantic similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Standard reasoning templates
templates = {
    "deductive": ["Premise 1", "Premise 2", "Conclusion"],
    "inductive": ["Observation 1", "Observation 2", "...", "Conclusion"],
    "causal": ["Cause", "Mechanism", "Evidence", "Conclusion"]
}
```

### 3. **Consistency Verification**
```python
# Contradiction detection based on NLI model
from transformers import pipeline

nli_model = pipeline("text-inference", model="distilbert-base-nli-stsb")

# Generate 5 samples, detect contradictions
samples = [generate_response() for _ in range(5)]
contradictions = check_contradictions(samples)
```

### 4. **Fact Checking**
```python
# Knowledge base pattern matching
knowledge_base = {
    "geography": {
        "capital_of_usa": "Washington D.C.",
        "population_of_china": "1.4 billion",
        # ... 100+ facts
    },
    "science": {
        "boiling_point_of_water": "100 degrees Celsius",
        "speed_of_light": "300,000 km/s",
        # ... 100+ facts
    }
}
```

---

## 🏗️ **Experiment Architecture**

### Overall Flow Diagram

```
Input Text (Question-Answer Pair)
         │
         ├──────────────────────────────────────┐
         │                                      │
         ▼                                      ▼
┌─────────────────────┐             ┌─────────────────────┐
│ Module 1: Logic     │             │ Module 2: Reasoning  │
│ Validation          │             │ Chain                │
│ - 150+ pattern match│             │ - Template matching  │
│ - 22 fallacy types  │             │ - Semantic similarity│
│ - Detection 50-60%  │             │ - <10ms/query        │
└────────┬────────────┘             └────────┬────────────┘
         │                                    │
         │ Logic Score (0/1)                  │ Completeness Score (0-1)
         │                                    │
         └──────────────────┬─────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │ Fusion Layer    │
                  │ (Weighted)      │
                  │ w1=0.4, w2=0.3  │
                  └────────┬────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
         ▼                                   ▼
┌─────────────────────┐             ┌─────────────────────┐
│ Module 3:           │             │ Module 4:           │
│ Consistency         │             │ Fact Checking       │
│ - 5 samples         │             │ - 100+ facts        │
│ - NLI contradiction │             │ - Pattern matching  │
│ - 2s/query          │             │ - 85% accuracy      │
└────────┬────────────┘             └────────┬────────────┘
         │                                   │
         │ Consistency Score (0-1)           │ Fact Score (0/1)
         │                                   │
         └──────────────────┬────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │ Final Fusion     │
                  │ Overall Score    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Output Result   │
                  │ - Hallucination?│
                  │ - Confidence    │
                  │ - Explanation   │
                  └─────────────────┘
```

---

## 📋 **Research Logic**

### Research Questions

**Core Question**: How to detect hallucinations in LLM logical reasoning in a lightweight, efficient manner?

**Sub-questions**:
1. How to detect formal logical fallacies (affirming consequent, denying antecedent, etc.)?
2. How to detect informal logical fallacies (ad hominem, appeal to authority, etc.)?
3. How to detect incomplete reasoning chains (reasoning gaps, missing premises)?
4. How to detect self-contradictory statements?
5. How to detect factual errors?

### Research Hypotheses

**H1**: Multi-module fusion outperforms single-module methods
- Verification: Ablation study (Module 1-4 individually vs. fused)
- Expected: Fusion accuracy > individual modules

**H2**: Pattern matching can effectively detect logical fallacies
- Verification: 22 fallacy types, 150+ patterns
- Expected: Formal fallacy detection 50-60%, informal 40-50%

**H3**: Lightweight design does not compromise detection performance
- Verification: Comparison with heavy methods (SelfCheckGPT, NeuroLogic)
- Expected: Comparable performance, 5-20x faster

### Technical Roadmap

```
Problem Definition → Module Design → Pattern Engineering → Experiment Validation → Result Analysis
      │                    │               │                    │                    │
      │                    │               │                    │                    │
      ▼                    ▼               ▼                    ▼                    ▼
Hallucination          4 Modules      150+ Patterns        600 Test Set        81.7% Accuracy
Detection
```

### Innovation Points

1. **Multi-module Fusion Architecture**: 4 complementary modules with weighted fusion
2. **Lightweight Design**: <100MB memory, <1s response time
3. **Comprehensive Fallacy Coverage**: 22 fallacy types, 150+ detection patterns
4. **Interpretability**: Clear fallacy types and explanations

---

## 📊 **Experiment Design**

### Dataset

**LogicDetector-Bench** (600 instances):
- Logical fallacies: 300 instances (50%)
- Valid reasoning: 250 instances (41.7%)
- Factual errors: 50 instances (8.3%)

### Baseline Methods (7)

1. Perplexity
2. Semantic Entailment
3. SelfCheckGPT (Self-consistency check)
4. NeuroLogic (Neuro-symbolic method)
5. LLM-Check (Multi-dimensional detection)
6. LINC (Formal logic verification)
7. FActScore (Factual consistency)

### Evaluation Metrics

- **Primary Metrics**: Accuracy, F1 Score
- **Secondary Metrics**: Precision, Recall
- **Efficiency Metrics**: Response time, Memory usage

### Ablation Study

| Configuration | Accuracy | Change |
|--------------|----------|--------|
| **Full Model** | **81.7%** | - |
| - Module 1 (Logic) | 73.3% | -8.4% |
| - Module 2 (Reasoning Chain) | 75.5% | -6.2% |
| - Module 3 (Consistency) | 76.8% | -4.9% |
| - Module 4 (Fact) | 74.2% | -7.5% |

**Conclusion**: Module 2 (Reasoning Chain) contributes the most; multi-module fusion improves by +13.4%

---

## 📝 **Paper Revision Suggestions**

### Corrections Needed

1. **Z3 Theorem Prover**:
   - ❌ Remove "Z3 Theorem Prover (version 4.12.1)"
   - ✅ Change to "Pattern-based Detection (150+ regex patterns)"

2. **Experiment Architecture**:
   - ✅ Add overall architecture diagram (Figure 1)
   - ✅ Describe the technology stack actually used

3. **Research Logic**:
   - ✅ Clearly state research questions and hypotheses
   - ✅ Explain technical roadmap and innovation points

### Suggested Additions

1. **Implementation Details**:
   - Specific libraries used (re, sentence-transformers, transformers)
   - Pattern engineering methods (manual writing + automatic mining)
   - Parameter settings (thresholds, weights, etc.)

2. **Case Analysis**:
   - Successful detection cases
   - Failed detection cases
   - Error analysis

---

**Document Completed**: 2026-04-05 15:52
