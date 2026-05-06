#!/usr/bin/env python3
"""
Embedding Model Comparison for M2 ChainChecker

Compares multiple sentence embedding models on Bench 110.
Outputs comparison table for paper inclusion.
"""

import sys, json, time, importlib
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))

from detector import LogicDetector
from modules.chain_checker import ChainChecker

MODELS = [
    ("BAAI/bge-small-zh-v1.5", "bge-small-zh", "33MB", "BAAI, 中文优化"),
    ("BAAI/bge-base-zh-v1.5",  "bge-base-zh",  "136MB", "BAAI, 更高质量"),
    ("moka-ai/m3e-base",       "m3e-base",     "100MB", "Moka, 通用中文"),
    ("shibing624/text2vec-base-chinese", "text2vec", "100MB", "Shibing624, 中文句向量"),
]

def load_bench(path="data/test_set_110.json"):
    with open(project_root / path, 'r') as f:
        data = json.load(f)
    return data['test_cases']

def evaluate_model(model_hf_name: str, model_label: str, test_cases: list) -> dict:
    """Run full evaluation with specified embedding model for ChainChecker"""
    
    # Create detector
    detector = LogicDetector()
    
    # Patch the chain checker with new model
    print(f"\n  Loading embedding model: {model_hf_name}...", end=" ", flush=True)
    t0 = time.time()
    new_cc = ChainChecker(model_name=model_hf_name)
    detector.chain_checker = new_cc
    t_load = time.time() - t0
    print(f"done ({t_load:.1f}s)")
    
    correct = 0
    total = 0
    tp = fp = tn = fn = 0
    latencies = []
    
    for i, s in enumerate(test_cases):
        text = s.get('text', '')
        label = s.get('label', s.get('expected', 'false'))
        expected = label == 'hallucination'
        
        t0 = time.time()
        result = detector.analyze(text)
        lat = time.time() - t0
        latencies.append(lat)
        
        pred = result.is_hallucination
        
        if pred and expected:
            tp += 1
        elif pred and not expected:
            fp += 1
        elif not pred and not expected:
            tn += 1
        else:
            fn += 1
        
        if pred == expected:
            correct += 1
        total += 1
        
        if (i+1) % 25 == 0:
            print(f"    ... {i+1}/{len(test_cases)}")
    
    acc = correct / total
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    avg_lat = sum(latencies) / len(latencies)
    
    return {
        "model": model_label,
        "model_hf": model_hf_name,
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "tn": tn,
        "total": total,
        "avg_latency_ms": round(avg_lat * 1000, 1),
        "load_time_s": round(t_load, 1),
    }


def print_table(results: list):
    """Print comparison table for paper"""
    print("\n" + "="*90)
    print("Embedding Model Comparison — Bench 110")
    print("="*90)
    print(f"{'Model':<22} {'Acc':>6} {'Prec':>6} {'Recall':>6} {'F1':>6} {'FP':>4} {'FN':>4} {'Lat(ms)':>8} {'Load(s)':>8}")
    print("-"*90)
    for r in results:
        print(f"{r['model']:<22} {r['accuracy']*100:>5.1f}% {r['precision']*100:>5.1f}% {r['recall']*100:>5.1f}% {r['f1']*100:>5.1f}% {r['fp']:>4} {r['fn']:>4} {r['avg_latency_ms']:>8.1f} {r['load_time_s']:>8.1f}")
    print("="*90)
    
    # Find best
    best = max(results, key=lambda r: r['accuracy'])
    best_f1 = max(results, key=lambda r: r['f1'])
    print(f"\n🏆 Best Accuracy: {best['model']} ({best['accuracy']*100:.1f}%)")
    print(f"🏆 Best F1: {best_f1['model']} ({best_f1['f1']*100:.1f}%)")


def save_results(results: list):
    """Save to JSON for paper reference"""
    path = project_root / "experiments" / "embedding_comparison_results.json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({
            "experiment": "M2 ChainChecker Embedding Model Comparison",
            "dataset": "Bench 110 (test_set_110.json)",
            "date": "2026-05-05",
            "threshold": 0.35,
            "models": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to: {path}")
    return path


if __name__ == "__main__":
    print("=" * 90)
    print("LogicDetector — M2 Embedding Model Comparison")
    print("Dataset: Bench 110 (test_set_110.json)")
    print("=" * 90)
    
    test_cases = load_bench()
    print(f"Loaded {len(test_cases)} test cases")
    
    all_results = []
    
    for hf_name, label, size, desc in MODELS:
        print(f"\n{'─'*60}")
        print(f"[{label}] {desc} ({size})")
        print(f"{'─'*60}")
        try:
            result = evaluate_model(hf_name, label, test_cases)
            all_results.append(result)
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            all_results.append({
                "model": label,
                "model_hf": hf_name,
                "error": str(e),
                "accuracy": 0, "precision": 0, "recall": 0, "f1": 0,
                "fp": 0, "fn": 0, "tp": 0, "tn": 0, "total": 0,
            })
    
    print_table(all_results)
    save_path = save_results(all_results)
    
    # Generate LaTeX table
    print("\n\n📄 LaTeX Table for Paper:\n")
    print("\\begin{table}[t]")
    print("\\centering")
    print("\\caption{M2 ChainChecker: Sentence embedding model comparison}")
    print("\\label{tab:embedding-comparison}")
    print("\\begin{tabular}{lrrrrrr}")
    print("\\toprule")
    print("Model & Accuracy & Precision & Recall & F1 & FP & FN \\\\")
    print("\\midrule")
    for r in all_results:
        if r.get('error'):
            print(f"{r['model']} & -- & -- & -- & -- & -- & -- \\\\")
        else:
            print(f"{r['model']} & {r['accuracy']*100:.1f}\\% & {r['precision']*100:.1f}\\% & {r['recall']*100:.1f}\\% & {r['f1']*100:.1f}\\% & {r['fp']} & {r['fn']} \\\\")
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\end{table}")
