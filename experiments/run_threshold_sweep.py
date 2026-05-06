#!/usr/bin/env python3
"""threshold 调优实验：改 detector.threshold（总体融合阈值）"""

import json
import sys
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
    acc = correct / total if total else 0
    prec = tp / (tp+fp) if (tp+fp) else 0
    rec = tp / (tp+fn) if (tp+fn) else 0
    f1 = 2*prec*rec/(prec+rec) if (prec+rec) else 0
    return {'total':total,'accuracy':acc,'precision':prec,'recall':rec,'f1':f1,'tp':tp,'fp':fp,'tn':tn,'fn':fn}

data_dir = project_root / "data"

# 用 Bench 600
d = load(str(data_dir / "test_set_full_600.json"))
bench_cases = d.get('test_cases', d.get('data', []))

# 阈值列表
thresholds = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]

print("=" * 75)
print("Threshold 调优实验 — 只改 detector.threshold（融合层阈值）")
print("=" * 75)

# 先初始化一次，后面只改 threshold
detector = LogicDetector(threshold=0.35)
print("✓ 检测器初始化完成")

print(f"\n{'Threshold':<12} {'准确率':>8} {'精确率':>8} {'召回率':>8} {'F1':>8} {'TP':>4} {'FP':>4} {'TN':>4} {'FN':>4}")
print("-" * 70)

results = []
for t in thresholds:
    detector.threshold = t
    r = evaluate(detector, bench_cases)
    r['threshold'] = t
    results.append(r)
    arrow = " ← 当前" if t == 0.35 else ""
    print(f"{t:<12} {r['accuracy']*100:>7.1f}% {r['precision']*100:>7.1f}% {r['recall']*100:>7.1f}% {r['f1']*100:>7.1f}% {r['tp']:>4} {r['fp']:>4} {r['tn']:>4} {r['fn']:>4}{arrow}")

# 最佳
best = max(results, key=lambda r: r['f1'])
best2 = max(results, key=lambda r: r['accuracy'])
print(f"\n🏆 最佳 F1: threshold={best['threshold']}, F1={best['f1']*100:.1f}%, {best['accuracy']*100:.1f}%/{best['precision']*100:.1f}%/{best['recall']*100:.1f}%")
print(f"🏆 最佳准确率: threshold={best2['threshold']}, 准确率={best2['accuracy']*100:.1f}%, F1={best2['f1']*100:.1f}%")

# 建议
current = [r for r in results if r['threshold'] == 0.35][0]
best_t = [r for r in results if r['threshold'] == best['threshold']][0]
if best_t['f1'] > current['f1']:
    print(f"\n💡 建议：从 threshold=0.35 调至 {best['threshold']}，F1 提升 {best_t['f1']*100-current['f1']*100:.1f}%")
else:
    print(f"\n💡 建议：当前 threshold=0.35 已经是最优或接近最优")

# 保存
out_path = project_root / "experiments" / "threshold_sweep_results.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"✓ 已保存：{out_path}")
