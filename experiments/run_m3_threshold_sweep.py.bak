#!/usr/bin/env python3
"""M3 内部 threshold 调优实验 - 改的是 consistency_verifier 里 is_consistent 的判定阈值"""

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
    not_consistent_count = 0
    for i, case in enumerate(test_cases):
        text = case['text']
        true_label = case['label']
        result = detector.analyze(text, reasoning_type=case.get('reasoning_type', 'deductive'))
        pred = 'hallucination' if result.is_hallucination else 'valid'
        if not result.is_consistent:
            not_consistent_count += 1
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
    return {'total':total,'accuracy':acc,'precision':prec,'recall':rec,'f1':f1,
            'tp':tp,'fp':fp,'tn':tn,'fn':fn,'not_consistent':not_consistent_count}

data_dir = project_root / "data"

# 用 Bench 600
d = load(str(data_dir / "test_set_full_600.json"))
bench_cases = d.get('test_cases', d.get('data', []))

# 要测试的 M3 阈值
m3_thresholds = [0, 0.1, 0.2, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]

print("=" * 80)
print("M3 内部 threshold 调优实验")
print("=" * 80)
print()
print(f"{'M3阈值':<10} {'准确率':>8} {'精确率':>8} {'召回率':>8} {'F1':>8} {'TP':>4} {'FP':>4} {'TN':>4} {'FN':>4} {'M3标记不一致':>12}")
print("-" * 85)

results = []
for i, t in enumerate(m3_thresholds):
    # 首次初始化加载模型，后续复用（consistency_verifier 每次重建但模型已缓存）
    detector = LogicDetector(threshold=0.35, m3_threshold=t)
    r = evaluate(detector, bench_cases)
    r['m3_threshold'] = t
    results.append(r)
    marker = " ← 当前" if t == 0.35 else ""
    print(f"{t:<10} {r['accuracy']*100:>7.1f}% {r['precision']*100:>7.1f}% {r['recall']*100:>7.1f}% {r['f1']*100:>7.1f}% {r['tp']:>4} {r['fp']:>4} {r['tn']:>4} {r['fn']:>4} {r['not_consistent']:>8}{marker}")

# 最佳 F1
best = max(results, key=lambda r: r['f1'])
print(f"\n🏆 最佳 F1: threshold={best['m3_threshold']}, F1={best['f1']*100:.1f}% (准确率={best['accuracy']*100:.1f}%, 精确率={best['precision']*100:.1f}%, 召回率={best['recall']*100:.1f}%)")

# 如果在 0.35 附近，找最优 + 解释
center = [r for r in results if r['m3_threshold'] == 0.35][0]
print(f"\n📊 当前(0.35): F1={center['f1']*100:.1f}%, 一致数={center['not_consistent']} 条不一致")

# 与最佳对比
if best['m3_threshold'] != 0.35:
    delta_f1 = best['f1'] - center['f1']
    print(f"\n💡 建议: threshold 从 0.35 调至 {best['m3_threshold']}, F1 变化 {delta_f1*100:+.1f}%")
else:
    print(f"\n💡 当前 0.35 已是最佳值")

# 保存
out_path = project_root / "experiments" / "m3_threshold_sweep_results.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"✓ 已保存：{out_path}")
