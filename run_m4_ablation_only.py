#!/usr/bin/env python3
"""
快速运行：只测 Without M4 消融配置
"""
import json
import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.detector import LogicDetector

DATA_DIR = "/home/baibai/.openclaw/workspace/logic-detector/data"
TEST_SET = "test_set_logiqa_full_8678.json"

class AblationDetector(LogicDetector):
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
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["test_cases"]

def test_single():
    config_name = "Without M4 (no FactChecker)"
    print(f"\n{'='*60}", flush=True)
    print(f"🔬 测试: {config_name}", flush=True)
    print(f"{'='*60}", flush=True)
    
    detector = AblationDetector(disable_m4=True)
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
    
    print(f"\n📊 {config_name} 结果:", flush=True)
    print(f"  准确率: {accuracy:.2f}%", flush=True)
    print(f"  精确率: {precision:.2f}%", flush=True)
    print(f"  召回率: {recall:.2f}%", flush=True)
    print(f"  F1: {f1:.4f}", flush=True)
    print(f"  TP={tp} TN={tn} FP={fp} FN={fn} | 耗时={elapsed:.1f}s", flush=True)
    
    return result

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    result = test_single()
    
    output_path = "/home/baibai/.openclaw/workspace/logic-detector/ablation_without_m4_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存: {output_path}")
