# LogicDetector Paper Summary

**Paper Title**: LogicDetector: Multi-Module Fusion for Logic Reasoning Hallucination Detection  
**Submission**: Anonymous ACL submission  
**Year**: 2026

---

## 📋 Abstract

Large Language Models (LLMs) are prone to hallucinations—statements that seem plausible but are factually incorrect or logically flawed. Existing hallucination detection methods primarily rely on semantic similarity or multi-sampling and often fail to detect logical fallacies and factual errors.

This paper proposes **LogicDetector**, a multi-module fusion approach for detecting logic reasoning hallucinations.

### Four Core Modules

1. **Logic Rule Validator** - Based on formal logic and fallacy detection
2. **Reasoning Chain Completeness Checker** - Checks whether reasoning steps are complete
3. **Self-Consistency Verifier** - Verifies consistency across multiple responses
4. **Fact Checker** - Validates claims against a common sense knowledge base

### Main Advantages

- **Lightweight**: No large semantic models required
- **Offline Deployment**: 47-85MB memory
- **Fast**: 0.5 seconds/query
- **Interpretable**: Provides clear explanations of logical fallacies

---

## 📊 Experiment Results

### Test Set

- **110 test cases** (54 manually annotated + 56 LogiQA)

### Accuracy Comparison

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

| Method | Time/Query | Memory Usage |
|--------|------------|--------------|
| **LogicDetector** | **0.5s** | **<100MB** |
| SelfCheckGPT | 8-15s | 500MB-1GB |
| NeuroLogic | 3-5s | 300-500MB |
| LLM-Check | 10-20s | 1-2GB |

**Speed Improvement**: 16-30x  
**Memory Savings**: 5-10x

### Category Accuracy

| Category | LogicDetector | Best Baseline | Improvement |
|----------|---------------|---------------|-------------|
| Valid Reasoning | **91.9%** | 88.5% | +3.4% |
| Logical Fallacies | **28.1%** | 3.1% | +25.0% |
| Factual Errors | **20.0%** | 0.0% | +20.0% |

### Ablation Study

| Configuration | Accuracy | Improvement |
|---------------|----------|-------------|
| Full Model | **55.5%** | - |
| - Module 1 (Logic) | 48.1% | +7.4% |
| - Module 2 (Chain) | 51.2% | +4.3% |
| - Module 3 (Consistency) | 52.8% | +2.7% |
| - Module 4 (Fact) | 51.8% | +3.7% |
| Single Module Best | 44.4% | +11.1% |

---

## 🔧 Technical Details

### Module 1: Logic Rule Validator

- **Foundation**: Formal logic (Z3 theorem prover) + pattern matching
- **Detection**: 6 fallacy types, 20+ detection patterns
- **Performance**: Formal fallacy detection rate 40-50%

### Module 2: Reasoning Chain Completeness Checker

- **Technique**: Lightweight sentence vectors + standard reasoning template comparison
- **Cost**: <10ms/query
- **Advantage**: Detects structural incompleteness

### Module 3: Self-Consistency Verifier

- **Optimization**: 5 samples (SelfCheckGPT requires 10-20)
- **Model**: NLI model (DistilBERT, 66M parameters)
- **Time**: 10 seconds → 2 seconds

### Module 4: Fact Checker

- **Knowledge base**: 25+ common sense facts
- **Accuracy**: 85% (within knowledge scope)
- **Memory**: <50MB

### Multi-Module Fusion

- **Architecture**: Parallel fusion framework
- **Fusion Method**: Weighted summation (late fusion)
- **Weights**: (0.4, 0.3, 0.2, 0.1)

---

## 📖 Related Work

### Hallucination Detection Methods

1. **Sampling-based methods**: SelfCheckGPT
2. **Semantic entailment methods**: FActScore
3. **Perplexity-based methods**: Perplexity
4. **Natural language inference**: NLI-based verification
5. **Knowledge graph verification**: KG-BERT
6. **Contrastive learning**: Contrastive Learning
7. **Retrieval-augmented methods**: RAG, Atlas
8. **Neuro-symbolic methods**: LINC, NeuroLogic

### LogicDetector Contributions

1. **Multi-module fusion architecture** - Novel parallel fusion framework
2. **Lightweight, offline-ready design** - No large models or external APIs needed
3. **Comprehensive logical fallacy detection** - 6 fallacy types, 20+ patterns
4. **Comprehensive experimental validation** - 110 test cases, 7 baseline methods

---

## 🚀 Application Prospects

### Suitable Scenarios

- **Privacy-sensitive environments**: Healthcare, legal, finance
- **Edge devices**: Raspberry Pi, phones
- **High-capacity applications**: 10,000+ queries/day
- **Educational applications**: Requiring interpretability

### Cost Savings

For high-capacity applications (10,000+ queries/day):
- **Annual cost savings**: $36,500-365,000
- **vs**: API-based methods ($0.01-0.10/query)

---

## 📝 Limitations and Future Work

### Limitations

1. **Limited fallacy coverage**: Only 6 fallacy types
2. **Small knowledge base**: Only 25+ facts
3. **Cannot detect consistent errors**: If all samples are wrong

### Future Work

1. **Expand fallacy types**: Cover more fallacies
2. **Expand knowledge base**: Integrate more common sense
3. **Improve fusion method**: Learn weights instead of manual settings
4. **Cross-lingual deployment**: Through pattern translation, not retraining

---

**Paper PDF**: `/home/baibai/.openclaw/media/inbound/paper_v1---862968ed-1aa4-418d-a895-51e8f6276316.pdf`
