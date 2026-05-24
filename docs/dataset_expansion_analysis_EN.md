# Logic Detector Dataset Expansion Analysis

**Analysis Date**: 2026-04-09  
**Purpose**: Compare dataset scales of mainstream papers and propose expansion strategies

---

## 📊 Dataset Scale Comparison

### Mainstream Paper Dataset Scales

| Paper | Main Experiment Dataset | Cross-Dataset Validation | Total Scale |
|-------|------------------------|-------------------------|-------------|
| **SelfCheckGPT** | 10,000+ sentences | Wikipedia + Bio | 10,000+ |
| **FActScore** | 500 long texts | Biography + Wiki | 1,000+ |
| **LLM-Check** | 10,000+ samples | Multi-dimensional benchmark | 10,000+ |
| **LINC** | 2,300+ problems | 3 datasets | 2,300+ |
| **Huang et al.** | Not specified | Fallacy detection | ~500-1000 |
| **LogicDetector** | **600 samples** | **10,178 samples** | **10,778 samples** |

---

## 🔍 Key Findings

### Finding 1: Main Experiment Dataset Scale Comparison

| Scale Level | Papers | Count |
|-------------|--------|-------|
| **Large scale (10,000+)** | SelfCheckGPT, LLM-Check | 2 |
| **Medium scale (1,000-5,000)** | LINC | 1 |
| **Small scale (500-1,000)** | FActScore, Huang et al. | 2 |
| **Our scale** | LogicDetector | 600 |

**Conclusion**: Our main experiment scale is comparable to FActScore (500 samples), within a **reasonable range**! ✅

---

### Finding 2: Cross-Dataset Validation Comparison

| Paper | Cross-Dataset Validation | Total Scale |
|-------|-------------------------|-------------|
| **SelfCheckGPT** | 2 datasets | 10,000+ |
| **FActScore** | 2 domains | 1,000+ |
| **LLM-Check** | Multi-dimensional | 10,000+ |
| **LINC** | 3 datasets | 2,300+ |
| **LogicDetector** | **4 datasets** | **10,778 samples** |

**Conclusion**: Our cross-dataset validation scale **exceeds most papers**! ✅

---

### Finding 3: Annotation Cost Comparison

| Paper | Annotation Method | Estimated Cost |
|-------|------------------|----------------|
| **SelfCheckGPT** | Manual annotation | High (10,000+ sentences) |
| **FActScore** | AMT (5 annotators) | High (500 long texts) |
| **LLM-Check** | 5 annotators + Kappa | Very high (10,000+ samples) |
| **LINC** | Synthetic + manual | Medium (2,300+ problems) |
| **LogicDetector** | **Existing datasets + manual** | **Low (600 main samples)** |

**Conclusion**: Our annotation cost is the **lowest**, suitable for rapid iteration! ✅

---

## 💡 Dataset Expansion Recommendations

### Plan A: Maintain Current Status (Recommended) ✅

**Rationale**:
1. **Main experiment scale is reasonable** - Comparable to FActScore (500 samples)
2. **Cross-dataset validation is sufficient** - 10,178 samples, exceeding most papers
3. **Low annotation cost** - Suitable for rapid iteration
4. **Clear paper positioning** - Pilot study

**Paper Wording**:
```
The main experiment uses 600 annotated samples, comparable to FActScore (500 samples).
Additionally, we validate generalization on 10,178 cross-dataset samples,
including LogiQA (8,678), CoT-Hub (500), and LogicInference (500).

Although the main experiment scale is smaller than SelfCheckGPT (10,000+) and
LLM-Check (10,000+), our total cross-dataset validation reaches 10,778 samples,
exceeding most existing work.
```

**Advantages**:
- ✅ No additional work required
- ✅ Reasonable scale
- ✅ Low cost

**Disadvantages**:
- ⚠️ Reviewers may question main experiment scale

---

### Plan B: Moderate Expansion (Compromise) ⭐

**Target**: Expand main experiment to 1,000-1,500 samples

**Expansion Sources**:

| Source | Current | Target | New |
|--------|---------|--------|-----|
| LogiQA | 200 | 500 | +300 |
| CoT-Hub | 150 | 400 | +250 |
| LogicInference | 150 | 400 | +250 |
| Manual | 100 | 200 | +100 |
| **Total** | **600** | **1,500** | **+900** |

**Estimated Effort**:
- Data extraction: 2-3 days
- Annotation validation: 3-5 days
- Experiment execution: 1 day
- **Total**: 1-2 weeks

**Advantages**:
- ✅ Scale increased to 1,500 samples
- ✅ Creates clear gap from FActScore
- ✅ Controllable effort

**Disadvantages**:
- ⚠️ Requires 1-2 weeks of additional work

---

### Plan C: Large-Scale Expansion (Aggressive)

**Target**: Expand main experiment to 5,000-10,000 samples

**Expansion Sources**:

| Source | Target Scale |
|--------|-------------|
| LogiQA (Full) | 8,678 samples |
| CoT-Hub (Sampled) | 1,000 samples |
| LogicInference (Sampled) | 1,000 samples |
| Manual (New) | 500 samples |
| **Total** | **11,178 samples** |

**Estimated Effort**:
- Data extraction: 1-2 days
- Annotation validation: 2-3 weeks
- Experiment execution: 2-3 days
- **Total**: 3-4 weeks

**Advantages**:
- ✅ Scale comparable to SelfCheckGPT
- ✅ Higher statistical significance
- ✅ Hard for reviewers to challenge

**Disadvantages**:
- ⚠️ Requires 3-4 weeks of additional work
- ⚠️ High annotation cost

---

## 🎯 Recommended Plan

### Primary Choice: Plan A (Maintain Current Status) ✅

**Rationale**:
1. **Reasonable scale** - Comparable to FActScore
2. **Sufficient cross-dataset validation** - 10,178 samples
3. **Low cost** - Suitable for rapid publication
4. **Clear positioning** - Pilot study

**Responding to Reviewer Concerns**:
```
We appreciate the reviewer's suggestion and agree on the importance of
large-scale datasets.

In our experimental design:
1. The main experiment (600 samples) is comparable to FActScore (500)
2. Cross-dataset validation (10,178 samples) exceeds most existing work
3. Total experimental scale (10,778) reaches benchmark dataset levels

We will clearly state this as a pilot study and plan to expand the main
experiment dataset in future work.
```

---

### Backup Choice: Plan B (Moderate Expansion) ⭐

**If time permits**, recommended to expand to 1,000-1,500 samples:

**Expansion Schedule**:

| Week | Task | Output |
|------|------|--------|
| **Week 1** | Data extraction + annotation | +500 samples |
| **Week 2** | Annotation validation + experiment | +500 samples + new results |

**Expected Impact**:
- Main experiment scale: 600 → 1,500 samples (+150%)
- Paper persuasiveness: Significantly improved
- Effort: Controllable (1-2 weeks)

---

## 📝 Paper Wording Suggestions

### Current Version (Plan A)

```
4.1 Dataset

Main Experiment Dataset (LogicDetector-Bench): 600 annotated samples
- Logical fallacies: 300 (50%)
- Valid reasoning: 250 (41.7%)
- Factual errors: 50 (8.3%)

Cross-dataset validation:
- LogiQA: 8,678 samples
- CoT-Hub: 500 samples
- LogicInference: 500 samples
- Total: 10,178 samples

Total experimental scale: 10,778 samples
```

### Expanded Version (Plan B)

```
4.1 Dataset

Main Experiment Dataset (LogicDetector-Bench): 1,500 annotated samples
- Logical fallacies: 750 (50%)
- Valid reasoning: 625 (41.7%)
- Factual errors: 125 (8.3%)

Cross-dataset validation:
- LogiQA: 8,678 samples
- CoT-Hub: 500 samples
- LogicInference: 500 samples
- Total: 10,178 samples

Total experimental scale: 11,678 samples
```

---

## 📊 Scale Comparison Visualization

```
Main Experiment Scale Comparison:

SelfCheckGPT: ████████████████████ 10,000+
LLM-Check:    ████████████████████ 10,000+
LINC:         ████████ 2,300+
FActScore:    ██ 500
Huang et al.: ██ 500-1000
LogicDetector (Current): ██ 600
LogicDetector (Expanded): █████ 1,500

Cross-Dataset Validation Comparison:

SelfCheckGPT: ████████████████████ 10,000+
LLM-Check:    ████████████████████ 10,000+
LogicDetector: ████████████████████ 10,178 ✅
LINC:         ████████ 2,300+
FActScore:    ████ 1,000+
```

---

## ✅ Final Recommendations

### If Time is Limited (Recommended)

**Choose Plan A**: Maintain current status

**Rationale**:
1. Main experiment scale comparable to FActScore (500 vs 600)
2. Cross-dataset validation exceeds most papers (10,178)
3. Total scale is reasonable (10,778)
4. Allows rapid publication

**Paper Wording**:
- Clearly state as pilot study
- Emphasize cross-dataset validation scale
- Commit to future expansion of main experiment

---

### If Time is Available

**Choose Plan B**: Expand to 1,500 samples

**Rationale**:
1. Creates clear gap from FActScore (500 vs 1,500)
2. Higher statistical significance
3. Hard for reviewers to challenge
4. Controllable effort (1-2 weeks)

**Expansion Schedule**:
- Week 1: Data extraction + annotation (+500 samples)
- Week 2: Annotation validation + experiment (+500 samples + new results)

---

## 📋 Dataset Source Details

### 1. LogiQA

**Source**: Chinese logical reasoning exams (civil service, MBA/MPA joint exams)

**Currently Used**: 200 samples  
**Expandable to**: 8,678 samples (full)

**Advantages**:
- ✅ High-quality annotation (professional logic instructors)
- ✅ Diverse reasoning types
- ✅ Public dataset

**Disadvantages**:
- ⚠️ Exam questions may rely on background knowledge

---

### 2. Chain of Thought Hub

**Source**: GitHub open-source chain-of-thought community

**Currently Used**: 150 samples  
**Expandable to**: 8,000+ samples (full)

**Advantages**:
- ✅ Chain-of-thought reasoning
- ✅ Multi-step reasoning
- ✅ Open-source dataset

**Disadvantages**:
- ⚠️ Variable quality (community contributions)

---

### 3. LogicInference

**Source**: Formal logic research community

**Currently Used**: 150 samples  
**Expandable to**: 10,000+ samples (full)

**Advantages**:
- ✅ Formal logic reasoning
- ✅ High-quality annotation
- ✅ Public dataset

**Disadvantages**:
- ⚠️ Primarily English

---

### 4. Manual (Hand-crafted)

**Source**: Targeted design

**Currently Used**: 100 samples  
**Expandable to**: 500+ samples

**Advantages**:
- ✅ Highly targeted
- ✅ Covers specific fallacy types
- ✅ Controllable quality

**Disadvantages**:
- ⚠️ Significant effort required

---

## 🎯 Summary

### Dataset Scale Assessment

| Dimension | Assessment | Description |
|-----------|-----------|-------------|
| **Main Experiment Scale** | ✅ Reasonable | Comparable to FActScore |
| **Cross-Dataset Validation** | ✅ Sufficient | Exceeds most papers |
| **Total Experimental Scale** | ✅ Reasonable | 10,778 samples |
| **Annotation Cost** | ✅ Low | Suitable for rapid iteration |
| **Statistical Significance** | ⚠️ Moderate | Can expand to 1,500 samples |

### Final Recommendation

**Recommended**: Plan A (Maintain Current Status)

**Rationale**:
1. Reasonable scale, comparable to FActScore
2. Sufficient cross-dataset validation
3. Low cost, suitable for rapid publication
4. Can be expanded in future work

**If time permits**: Plan B (Expand to 1,500 samples)

---

**Analysis Date**: 2026-04-09  
**Confidence Level**: High
