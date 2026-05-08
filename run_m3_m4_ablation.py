#!/usr/bin/env python3
"""
M3/M4消融实验脚本
测试移除Module 3 (ConsistencyVerifier) 和 Module 4 (FactChecker) 对LogiQA全量的影响
"""
import json
import os
import time
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.detector import LogicDetector

DATA_DIR = "/home/baibai/.openclaw/workspace/logic-detector/data"
TEST_SET = "test_set_logiqa_full_8678.json"

class AblationDetector(LogicDetector):
    """可配置禁用模块的检测器"""
    
    def __init__(self, disable_m3=False, disable_m4=False, **kwargs):
        super().__init__(**kwargs)
        self.disable_m3 = disable_m3
        self.disable_m4 = disable_m4
        
    def analyze(self, text, reasoning_type="deductive"):
        fallacies = self.logic_validator.validate(text)
        has_fallacy = len(fallacies) > 0
        logic_score = 0.0 if has_fallacy else 1.0
        
        chain_analysis = self.chain_checker.check_completeness(text, reasoning_type)
        chain_score = chain_analysis.completeness_score
        
        if not self.disable_m3:
            consistency_result = self.consistency_verifier.verify(text)
            consistency_score = consistency_result.confidence
            is_consistent = consistency_result.is_consistent
        else:
            consistency_score = 1.0
            is_consistent = True
        
        if not self.disable_m4:
            factual_errors = self.fact_checker.get_factual_errors(text)
            has_factual_error = len(factual_errors) > 0
            fact_score = 0.0 if has_factual_error else 1.0
            has_confirmed_fact = self.fact_checker.get_fact_confirmation(text)
        else:
            factual_errors = []
            has_factual_error = False
            fact_score = 1.0
            has_confirmed_fact = False

        effective_consistency = consistency_score
        if not is_consistent:
            effective_consistency = consistency_score * 0.5

        overall_score = (
            self.weights["logic"] * logic_score +
            self.weights["chain"] * chain_score +
            self.weights["consistency"] * effective_consistency +
            self.weights["fact"] * fact_score
        )

        if chain_score < 0.5 and not has_confirmed_fact:
            is_hallucination = True
            overall_score = chain_score
        elif chain_score < 0.5 and has_confirmed_fact:
            is_hallucination = (overall_score < self.threshold)
        else:
            is_hallucination = (overall_score < self.threshold)

        if has_fallacy or has_factual_error:
            is_hallucination = True
        
        return is_hallucination, overall_score

def load_dataset():
    filepath = os.path.join(DATA_DIR, TEST_SET)
    print(f"📂 加载数据集: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["test_cases"]

def test_ablation(config_name, **kwargs):
    print(f"\n{'='*60}")
    print(f"🔬 测试: {config_name}")
    print(f"{'='*60}")
    
    detector = AblationDetector(**kwargs)
    test_cases = load_dataset()
    
    tp = tn = fp = fn = 0
    start_time = time.time()
    
    for i, case in enumerate(test_cases):
        text = case["text"]
        true_hallucination = (case["label"] == "hallucination")
        is_hallucination, score = detector.analyze(text)
        
        if true_hallucination and is_hallucination:
            tp += 1
        elif not true_hallucination and not is_hallucination:
            tn += 1
        elif not true_hallucination and is_hallucination:
            fp += 1
        else:
            fn += 1
            
        if (i+1) % 2000 == 0:
            print(f"  进度: {i+1}/{len(test_cases)}...", flush=True)
    
    elapsed = time.time() - start_time
    total = tp + tn + fp + fn
    
    accuracy = (tp + tn) / total * 100 if total > 0 else 0
    precision = tp / (tp + fp) * 100 if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) * 100 if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    result = {
        "config": config_name,
        "accuracy": round(accuracy / 100, 4),
        "precision": round(precision / 100, 4),
        "recall": round(recall / 100, 4),
        "f1": round(f1 / 100, 4),
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "total_time_s": round(elapsed, 2)
    }
    
    print(f"\n📊 结果: Acc={accuracy:.2f}% P={precision:.2f}% R={recall:.2f}% F1={f1:.4f}")
    print(f"   TP={tp} TN={tn} FP={fp} FN={fn} | 耗时={elapsed:.1f}s")
    
    return result

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    results = []
    
    # 1. Full model baseline
    results.append(test_ablation("Full Model (M1+M2+M3+M4)"))
    
    # 2. Without M3 (ConsistencyVerifier)
    results.append(test_ablation("Without M3 (no ConsistencyVerifier)", disable_m3=True))
    
    # 3. Without M4 (FactChecker)
    results.append(test_ablation("Without M4 (no FactChecker)", disable_m4=True))
    
    # 4. Without M3+M4 (M1+M2 only)
    results.append(test_ablation("Without M3+M4 (M1+M2 only)", disable_m3=True, disable_m4=True))
    
    # Summary
    print(f"\n{'='*70}")
    print("📋 消融实验汇总")
    print(f"{'='*70}")
    baseline = results[0]
    print(f"{'配置':<38} {'Acc':>8} {'F1':>8} {'FP':>6} {'FN':>6} {'FPΔ':>6} {'FNΔ':>6}")
    print("-" * 70)
    for r in results:
        fp_delta = r['fp'] - baseline['fp']
        fn_delta = r['fn'] - baseline['fn']
        sign = "+" if fp_delta > 0 or fn_delta > 0 else " "
        print(f"{r['config']:<38} {r['accuracy']*100:>7.2f}% {r['f1']:>8.4f} {r['fp']:>5d} {r['fn']:>5d} {sign}{fp_delta:>+5d} {fn_delta:>+5d}")
    
    output_path = "/home/baibai/.openclaw/workspace/logic-detector/m3_m4_ablation_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"ablation_results": results, "baseline": results[0], "test_set": TEST_SET}, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {output_path}")

if __name__ == "__main__":
    main()
