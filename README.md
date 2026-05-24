# LogicDetector: Multi-Module Fusion Framework for Logical Reasoning Hallucination Detection

**Version**: v1.0 (Based on ACL 2026 Paper)  
**Created**: April 2026  
**Authors**: HuoYan Team  

---

## 📋 Overview

LogicDetector is a lightweight, multi-module fusion framework for detecting hallucinated logical reasoning in Large Language Models (LLMs).

**Core Advantages**:
- ✅ **Lightweight**: Only 47–85MB memory footprint
- ✅ **Fast**: 0.5s per query (16–30× faster than baselines)
- ✅ **Offline Deployable**: No large semantic models or external APIs required
- ✅ **Explainable**: Provides clear logical fallacy explanations

**Performance**:
- Accuracy: **55.5%** (110 test cases)
- Outperforms 7 baselines (including NeuroLogic, LLM-Check, LINC, etc.)

---

## 🎯 Four Core Modules

### Module 1: Logic Rule Validator

Formal logic based (Z3 theorem prover) and pattern-matching fallacy detection.

**Detection Capabilities**:
- Affirming the Consequent
- Denying the Antecedent
- Hasty Generalization
- False Cause
- Ad Hominem
- Appeal to Authority

**Performance**:
- Formal fallacy detection rate: 40–50%
- Covers 6 fallacy types with 20+ detection patterns

**Example**:
```python
# Affirming the Consequent
"If it rains, the ground gets wet. The ground is wet, so it rained."
→ Detected: Affirming the Consequent
```

---

### Module 2: Reasoning Chain Completeness Checker

Analyzes whether reasoning steps are complete; detects reasoning gaps and missing premises.

**Technology**:
- Lightweight sentence embeddings
- Comparison against canonical reasoning templates
- Cost: <10ms per query

**Advantages**:
- Low computational cost
- Detects structural incompleteness
- Complements formal logic methods

---

### Module 3: Self-Consistency Verifier

Generates multiple responses and checks for contradictions.

**Optimization**:
- Requires only 5 samples (SelfCheckGPT needs 10–20)
- Uses NLI model (DistilBERT, 66M parameters)
- Inference time: 10s → 2s

**Limitation**:
- Cannot detect consistently repeated errors

---

### Module 4: Fact Checker

Validates claims against a commonsense knowledge base.

**Knowledge Base**:
- 25+ commonsense facts (geography, physics, biology)
- Pattern matching + named entity recognition
- Accuracy: 85% (within knowledge scope)

**Advantages**:
- Fully offline
- Memory <50MB
- Suitable for privacy-sensitive environments

---

## 🚀 Quick Start

### Installation

```bash
cd logic-detector
pip install -r requirements.txt
```

### Usage Example

```python
from logic_detector import LogicDetector

# Create detector
detector = LogicDetector()

# Analyze text
text = "If it rains, the ground gets wet. The ground is wet, so it rained."
result = detector.analyze(text)

# Output results
print(f"Is hallucination: {result.is_hallucination}")
print(f"Confidence: {result.confidence}")
print(f"Detected fallacies: {result.fallacies}")
print(f"Completeness score: {result.completeness_score}")
```

---

## 📊 Performance Comparison

### Accuracy Comparison (110 Test Cases)

| Method | Accuracy | Improvement |
|--------|----------|-------------|
| **LogicDetector (Ours)** | **55.5%** | - |
| NeuroLogic (MIT+Stanford) | 46.9% | +18.3% |
| SelfCheckGPT | 41.8% | +32.8% |
| Perplexity | 52.7% | +5.3% |
| Semantic Entailment | 48.2% | +15.1% |
| LLM-Check (DeepMind) | 45.0% | +23.3% |
| LINC (CMU) | 43.5% | +27.6% |

### Efficiency Comparison

| Method | Time/Query | Memory |
|--------|-----------|--------|
| **LogicDetector** | **0.5s** | **<100MB** |
| SelfCheckGPT | 8–15s | 500MB–1GB |
| NeuroLogic | 3–5s | 300–500MB |
| LLM-Check | 10–20s | 1–2GB |

**Speedup**: 16–30×  
**Memory Reduction**: 5–10×

---

## 📁 Project Structure

```
logic-detector/
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── __init__.py
│   ├── detector.py               # Core detector
│   ├── modules/
│   │   ├── logic_validator.py    # Module 1: Logic Rule Validator
│   │   ├── chain_checker.py      # Module 2: Reasoning Chain Checker
│   │   ├── consistency_verifier.py # Module 3: Self-Consistency Verifier
│   │   └── fact_checker.py       # Module 4: Fact Checker
├── tests/
│   ├── test_detector.py
│   └── test_logic_detector.py
├── examples/
│   ├── basic_usage.py
│   └── example_usage.py
├── data/
│   ├── test_set_110.json         # 110 test cases
│   └── knowledge_base.json       # Commonsense knowledge base
├── docs/                          # Documentation
├── benchmarks/                    # Benchmarking scripts
├── experiments/                   # Experimental results
└── openclaw-skill/                # OpenClaw skill integration
```

---

## 🔧 Configuration

### Detector Configuration

```yaml
detector:
  modules:
    logic:
      enabled: true
      weight: 0.4
      fallacy_types:
        - affirming_consequent
        - denying_antecedent
        - hasty_generalization
        - false_cause
        - ad_hominem
        - appeal_to_authority
    
    chain:
      enabled: true
      weight: 0.3
      threshold: 0.7
    
    consistency:
      enabled: true
      weight: 0.2
      n_samples: 5
    
    fact:
      enabled: true
      weight: 0.1
      knowledge_base: data/knowledge_base.json
  
  fusion:
    method: weighted_sum
    threshold: 0.5
```

---

## 📖 Related Publications

- **LogicDetector Paper**: Submitted to ACL 2026 (Anonymous)
- **arXiv**: (Coming soon)

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

### Planned Improvements

- [ ] Expand fallacy detection patterns
- [ ] Extend commonsense knowledge base
- [ ] Optimize fusion weight learning
- [ ] Add multilingual support

---

## 📄 License

MIT License

---

## 📊 Experimental Results

### Accuracy by Category

| Category | LogicDetector | Best Baseline | Improvement |
|----------|---------------|---------------|-------------|
| Valid Reasoning | **91.9%** | 88.5% | +3.4% |
| Logical Fallacy | **28.1%** | 3.1% | +25.0% |
| Factual Error | **20.0%** | 0.0% | +20.0% |

### Ablation Study

| Configuration | Accuracy | vs Full |
|---------------|----------|---------|
| Full Model | **55.5%** | - |
| - Module 1 (Logic) | 48.1% | −7.4% |
| - Module 2 (Chain) | 51.2% | −4.3% |
| - Module 3 (Consistency) | 52.8% | −2.7% |
| - Module 4 (Fact) | 51.8% | −3.7% |
| Single Module Best | 44.4% | −11.1% |

---

**Last Updated**: 2026-04-01  
**Contact**: HuoYan Team
