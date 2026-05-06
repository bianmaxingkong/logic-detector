#!/usr/bin/env python3
"""全量跑 CoT-Hub (8,000)、LogicInference (10,000)、Manual (100)"""

import json
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))
from detector import LogicDetector

def load(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate(detector, test_cases):
    total = len(test_cases)
    correct = tp = fp = tn = fn = 0
    for i, case in enumerate(test_cases):
        text = case['text']
        true_label = case['label']
        result = detector.analyze(text, reasoning_type=case.get('reasoning_type', 'deductive'))
        pred = 'hallucination' if result.is_hallucination else 'valid'
        if pred == true_label:
            correct += 1
        if true_label == 'hallucination' and pred == 'hallucination':
            tp += 1
        elif true_label == 'valid' and pred == 'hallucination':
            fp += 1
        elif true_label == 'valid' and pred == 'valid':
            tn += 1
        elif true_label == 'hallucination' and pred == 'valid':
            fn += 1
        if (i+1) % 1000 == 0:
            print(f"  ... 已处理 {i+1}/{total}", flush=True)
    acc = correct / total if total else 0
    prec = tp / (tp+fp) if (tp+fp) else 0
    rec = tp / (tp+fn) if (tp+fn) else 0
    f1 = 2*prec*rec/(prec+rec) if (prec+rec) else 0
    return {'total':total,'correct':correct,'accuracy':acc,'precision':prec,'recall':rec,'f1':f1,'tp':tp,'fp':fp,'tn':tn,'fn':fn}

def print_r(results, name):
    print(f"\n{name}:")
    print(f"  样本数：{results['total']}")
    print(f"  准确率：{results['accuracy']*100:.1f}%")
    print(f"  精确率：{results['precision']*100:.1f}%")
    print(f"  召回率：{results['recall']*100:.1f}%")
    print(f"  F1 分数：{results['f1']*100:.1f}%")
    print(f"  TP={results['tp']} FP={results['fp']} TN={results['tn']} FN={results['fn']}")

detector = LogicDetector(threshold=0.35)
print("✓ 检测器初始化完成")

data_dir = project_root / "data"
all_results = {}

# 1. CoT-Hub 全量 (8,000)
print("\n加载 CoT-Hub 全量...")
d = load(str(data_dir / "test_set_cothub_full.json"))
cases = d.get('test_cases', d.get('data', []))
print(f"  ✓ {len(cases)} 条")
print("  运行检测...")
r = evaluate(detector, cases)
all_results['CoT-Hub (全量 8,000)'] = r
print_r(r, 'CoT-Hub (全量 8,000)')

# 2. LogicInference 全量 (10,000)
print("\n加载 LogicInference 全量...")
d = load(str(data_dir / "test_set_logicinference_full.json"))
cases = d.get('test_cases', d.get('data', []))
print(f"  ✓ {len(cases)} 条")
print("  运行检测...")
r = evaluate(detector, cases)
all_results['LogicInference (全量 10,000)'] = r
print_r(r, 'LogicInference (全量 10,000)')

# 3. Manual (100 条 — 从 Bench 600 中提取)
print("\n加载 Manual (从 Bench 600 提取)...")
d = load(str(data_dir / "test_set_full_600.json"))
all_bench = d.get('test_cases', d.get('data', []))
manual = [c for c in all_bench if c.get('source','') == 'Manual']
print(f"  ✓ {len(manual)} 条")
print("  运行检测...")
r = evaluate(detector, manual)
all_results['Manual (100 条)'] = r
print_r(r, 'Manual (100 条)')

# 汇总
print("\n" + "="*60)
print("全量数据集验证结果汇总")
print("="*60)
print(f"\n{'数据集':<28} {'样本数':>8} {'准确率':>10} {'精确率':>10} {'召回率':>10} {'F1':>8}")
print("-"*75)
for name, r in all_results.items():
    print(f"{name:<28} {r['total']:>8} {r['accuracy']*100:>9.1f}% {r['precision']*100:>9.1f}% {r['recall']*100:>9.1f}% {r['f1']*100:>7.1f}%")

# 保存
out = project_root / "experiments" / "full_datasets_results.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump({'datasets': all_results}, f, ensure_ascii=False, indent=2)
print(f"\n✓ 结果已保存：{out}")
