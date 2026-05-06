#!/usr/bin/env python3
"""
全数据集批量测试脚本
自动测试所有全量数据集，输出详细指标和汇总报告
"""
import json
import os
import time
from tqdm import tqdm
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.detector import LogicDetector

# 全量数据集列表
FULL_DATASETS = [
    ("LogiQA全量 (8678条)", "test_set_logiqa_full_8678.json"),
    ("LogicInference全量", "test_set_logicinference_full.json"),
    ("COTHUB全量", "test_set_cothub_full.json"),
    ("混合全量 (10000条)", "test_set_full_10000.json"),
    ("扩展全量 (1500条)", "test_set_full_1500_extended.json"),
    ("Bench110全量", "test_set_110_full.json"),
]

DATA_DIR = "/home/baibai/.openclaw/workspace/logic-detector/data"

def load_dataset(filename):
    """加载数据集"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["test_cases"]

def test_dataset(detector, dataset_name, test_cases):
    """测试单个数据集"""
    print(f"\n{'='*80}")
    print(f"📊 开始测试：{dataset_name}，样本量：{len(test_cases)}条")
    print(f"{'='*80}")
    
    tp = tn = fp = fn = 0
    start_time = time.time()
    
    for case in tqdm(test_cases, desc="测试进度"):
        text = case["text"]
        true_hallucination = (case["label"] == "hallucination")
        
        result = detector.analyze(text)
        pred_hallucination = result.is_hallucination
        
        if true_hallucination and pred_hallucination:
            tp += 1
        elif not true_hallucination and not pred_hallucination:
            tn += 1
        elif not true_hallucination and pred_hallucination:
            fp += 1
        elif true_hallucination and not pred_hallucination:
            fn += 1
    
    total_time = time.time() - start_time
    avg_time_per_sample = total_time / len(test_cases) * 1000
    
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # 输出结果
    print(f"\n✅ {dataset_name} 测试完成")
    print(f"总耗时：{total_time:.2f}秒，平均单样本耗时：{avg_time_per_sample:.2f}ms")
    print(f"总样本量：{total}")
    print(f"TP={tp}, TN={tn}, FP={fp}, FN={fn}")
    print(f"准确率：{accuracy:.4f} ({(tp+tn)}/{total})")
    print(f"精确率：{precision:.4f}")
    print(f"召回率：{recall:.4f}")
    print(f"F1分数：{f1:.4f}")
    
    return {
        "dataset_name": dataset_name,
        "total_samples": total,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "total_time": total_time,
        "avg_time_per_sample": avg_time_per_sample
    }

def main():
    print("🚀 全数据集批量测试启动")
    print(f"测试模型：BAAI/bge-small-zh-v1.5，阈值：0.4")
    print(f"待测试数据集：{len(FULL_DATASETS)}个")
    
    # 初始化检测器
    detector = LogicDetector(threshold=0.4)
    print("检测器初始化完成\n")
    
    results = []
    all_start_time = time.time()
    
    for name, filename in FULL_DATASETS:
        try:
            test_cases = load_dataset(filename)
            res = test_dataset(detector, name, test_cases)
            results.append(res)
        except Exception as e:
            print(f"❌ 测试数据集 {name} 失败：{str(e)}")
    
    total_all_time = time.time() - all_start_time
    
    # 输出汇总报告
    print(f"\n\n{'='*80}")
    print("🏆 全数据集测试汇总报告")
    print(f"{'='*80}")
    print(f"总测试数据集：{len(results)}个")
    print(f"总耗时：{total_all_time:.2f}秒 ({total_all_time/60:.1f}分钟)")
    print()
    print(f"{'数据集名称':<20} {'样本量':<8} {'准确率':<8} {'F1':<8} {'精确率':<8} {'召回率':<8} {'单样本耗时':<10}")
    print(f"{'-'*80}")
    for res in results:
        print(f"{res['dataset_name']:<20} {res['total_samples']:<8} {res['accuracy']:.4f}  {res['f1']:.4f}  {res['precision']:.4f}  {res['recall']:.4f}  {res['avg_time_per_sample']:.2f}ms")
    
    # 保存完整结果
    result_file = "/home/baibai/.openclaw/workspace/logic-detector/full_dataset_test_results.json"
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "total_datasets": len(results),
                "total_time": total_all_time,
                "model": "BAAI/bge-small-zh-v1.5",
                "threshold": 0.4
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)
    print(f"\n📝 完整测试结果已保存到：{result_file}")
    print("✅ 全数据集测试全部完成！")

if __name__ == "__main__":
    main()
