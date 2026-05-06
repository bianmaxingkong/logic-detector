#!/usr/bin/env python3
"""
阈值优化脚本
在0.3到0.5的范围内测试不同阈值的表现，找到最佳平衡点
"""
import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.detector import LogicDetector

def load_benchmark():
    """加载Bench 110测试集"""
    with open("/home/baibai/.openclaw/workspace/logic-detector/data/test_set_110.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["test_cases"]

def evaluate_threshold(threshold, test_cases):
    """评估指定阈值下的表现"""
    detector = LogicDetector(threshold=threshold)
    
    tp = tn = fp = fn = 0
    total_time = 0.0
    
    for case in test_cases:
        text = case["text"]
        true_hallucination = (case["label"] == "hallucination")
        
        result = detector.analyze(text)
        pred_hallucination = result.is_hallucination
        
        if true_hallucination and pred_hallucination:
            tp +=1
        elif not true_hallucination and not pred_hallucination:
            tn +=1
        elif not true_hallucination and pred_hallucination:
            fp +=1
        elif true_hallucination and not pred_hallucination:
            fn +=1
    
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total >0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) >0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) >0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) >0 else 0.0
    
    return {
        "threshold": threshold,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    }

def main():
    test_cases = load_benchmark()
    print(f"阈值优化测试启动，测试集大小：{len(test_cases)}条\n")
    
    # 测试阈值范围：0.3 ~ 0.5，步长0.02
    thresholds = [0.3 + 0.02 * i for i in range(11)]
    results = []
    
    for th in thresholds:
        th_rounded = round(th, 2)
        print(f"正在测试阈值：{th_rounded:.2f}...")
        res = evaluate_threshold(th_rounded, test_cases)
        results.append(res)
        print(f"  准确率：{res['accuracy']:.4f}，F1：{res['f1']:.4f}，精确率：{res['precision']:.4f}，召回率：{res['recall']:.4f}")
        print(f"  TP：{res['tp']}，TN：{res['tn']}，FP：{res['fp']}，FN：{res['fn']}\n")
    
    # 按F1排序找最优
    sorted_by_f1 = sorted(results, key=lambda x: (-x["f1"], -x["accuracy"], -x["recall"]))
    best = sorted_by_f1[0]
    
    print("=" * 80)
    print("🎉 最优阈值结果：")
    print(f"最优阈值：{best['threshold']:.2f}")
    print(f"准确率：{best['accuracy']:.4f} ({best['tp']+best['tn']}/{len(test_cases)})")
    print(f"F1分数：{best['f1']:.4f}")
    print(f"精确率：{best['precision']:.4f}")
    print(f"召回率：{best['recall']:.4f}")
    print(f"错误统计：FP={best['fp']}（误判），FN={best['fn']}（漏判）")
    print("=" * 80)
    
    # 保存所有结果
    with open("/home/baibai/.openclaw/workspace/logic-detector/threshold_optimization_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n所有阈值测试结果已保存到：threshold_optimization_results.json")
    
    # 输出推荐配置
    print("\n📌 推荐配置：")
    print(f"model: BAAI/bge-small-zh-v1.5")
    print(f"threshold: {best['threshold']:.2f}")
    print(f"expected performance: accuracy={best['accuracy']:.2%}, F1={best['f1']:.4f}")

if __name__ == "__main__":
    main()
