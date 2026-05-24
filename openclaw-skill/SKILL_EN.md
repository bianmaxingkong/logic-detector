---
name: logic-detector
description: Logic reasoning hallucination detection. Use when the user asks to analyze whether a piece of text contains logical fallacies, incomplete reasoning chains, self-contradiction, or factual errors. Also applicable when the user questions an AI output as "seems off," "does this have logic issues," or "help me analyze this argument." Auto-triggers on "check this for logic issues," "is this argument problematic," "detect the reasoning here." Not suitable for checking purely factual question-answering (should use search).
setup:
  - type: git_clone
    repo: https://github.com/bianmaxingkong/logic-detector.git
    dest: "{{skill_dir}}/repo"
  - type: pip_install
    requirements: "{{skill_dir}}/repo/requirements.txt"
  - type: run_script
    script: "{{skill_dir}}/scripts/download_models.py"
    description: Download BGE embedding model and CFEVER knowledge base
---

# LogicDetector

A four-module fusion architecture based on the ACL 2026 paper, requiring no large models—a lightweight logic reasoning hallucination detector.

**Paper**: LogicDetector: Multi-Module Fusion for Logic Reasoning Hallucination Detection (ACL 2026)

## Quick Start

The detector requires no API key and runs entirely locally.

### Download the Project (First-time Use)

```bash
# Clone the repository (if not yet cloned)
git clone https://github.com/bianmaxingkong/logic-detector.git /path/to/logic-detector
cd /path/to/logic-detector

# Install dependencies
pip install -r requirements.txt

# Download model files
python3 openclaw-skill/scripts/download_models.py
```

### Basic Usage

```bash
# Method 1: Via pipe
echo "If it rains the ground gets wet, the ground is wet, so it must have rained" | python3 src/detect.py

# Method 2: Direct argument
python3 src/detect.py "He is an expert in this field, so what he says must be correct"

# Method 3: Specify reasoning type
python3 src/detect.py -r causal "Because Xiaoming eats apples every day, he won't get sick"
```

## Project Structure

```
logic-detector/
├── src/
│   ├── detector.py            # Main detection engine entry point
│   ├── __init__.py            # Package definition
│   └── modules/
│       ├── logic_validator.py      # M1: Logic rule validation (230+ patterns, 26 fallacies)
│       ├── chain_checker.py        # M2: Reasoning chain completeness check
│       ├── self_consistency.py     # M3: Self-consistency verification
│       └── fact_checker.py         # M4: Knowledge-base fact checking
├── data/
│   ├── cfever_index/               # CFEVER knowledge base (FAISS index)
│   └── test_set_*.json             # Test datasets
├── openclaw-skill/
│   ├── SKILL.md                    # This skill file
│   └── scripts/
│       ├── detect.py               # Detection script (final usage entry point)
│       └── download_models.py      # Model download script
└── requirements.txt                # Python dependencies
```

## Four-Module Architecture

| Module | Name | Function | Time |
|--------|------|----------|------|
| M1 | LogicValidator | 230+ regex patterns detecting 26 logical fallacies | <10ms |
| M2 | ChainChecker | Verify reasoning chain completeness (templates + embedding) | 35ms |
| M3 | ConsistencyVerifier | Multi-strategy text restructuring to detect semantic contradictions | <150ms |
| M4 | FactChecker | CFEVER knowledge base (18,305 items) fact verification | <100ms |

Fusion weights: M1=0.4, M2=0.3, M3=0.2, M4=0.1 (optimal configuration determined by paper experiments)

M1 and M4 have veto power (hard voting), M2 has conditional veto (triggered when score <0.5 and M4 hasn't confirmed facts)

## Output Format

### JSON Result Fields

```json
{
  "is_hallucination": true,      // true=problem exists false=logically sound
  "confidence": 0.9234,          // Confidence (0-1)
  "logic_fallacies": [           // List of detected fallacies
    {
      "type": "affirming_consequent",
      "pattern": "If P then Q, Q, therefore P"
    }
  ],
  "completeness_score": 0.35,    // Reasoning completeness (<0.5=incomplete)
  "is_consistent": false,        // Whether text is self-consistent
  "factual_errors": [            // List of factual errors
    "The Earth is flat, that's a scientific fact"
  ],
  "explanation": "..."           // Detailed explanation
}
```

### Command Line Options

| Parameter | Short | Description |
|-----------|-------|-------------|
| `--reasoning` | `-r` | Reasoning type: `deductive` (default), `inductive`, `causal`, `analogical` |
| `--verbose` | `-v` | Output detailed explanation |
| `--quiet` | `-q` | Brief output: 1=hallucination, 0=normal |

## Reasoning Types

| Type | Description | Example |
|------|-------------|---------|
| **deductive** | Deductive reasoning, general→specific | All humans are mortal, Socrates is human→Socrates is mortal |
| **inductive** | Inductive reasoning, specific→general | Observed 100 swans are all white→All swans are white |
| **causal** | Causal reasoning, cause→effect | Smoking causes lung cancer |
| **analogical** | Analogical reasoning, A≈B→conclusion extended | Earth and Mars both have atmospheres→Mars might have life |

Default is deductive; the detector will infer automatically. If you know the reasoning type of the input text, specifying `-r` can improve accuracy.

## Dependencies

- Python >= 3.8
- transformers
- sentence-transformers
- faiss-cpu
- numpy
- z3-solver (logic rule validation)

Model files (auto-download on first use):
- BAAI/bge-small-zh-v1.5 (33MB Chinese embedding model)
- CFEVER knowledge base (FAISS index + metadata, ~50MB)

## Important Notes

- **First run** loads models, ~1-2 seconds initialization
- **Subsequent calls** ~0.8 seconds/query
- Good Chinese support, also accepts English input
- Paper-verified accuracy: LogiQA 92.1%, LogicInference 88.6%, across 5 datasets
- Memory usage: <100MB
- **Zero** false positive rate (on LogiQA)
