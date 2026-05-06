#!/usr/bin/env python3
"""
多嵌入模型对比脚本
对比不同中文句向量模型在ChainChecker中的效果
"""

import json
import time
from typing import Dict, List
from src.modules.chain_checker import ChainChecker
from src.detector import LogicDetector

# 待测试模型列表
TEST_MODELS = [
    ("BAAI/bge-small-zh-v1.5", "33MB，中文优化小模型"),
    ("BAAI/bge-base-zh-v1.5", "136MB，中文优化基础模型"),
    ("moka-ai/m3e-base", "~100MB，M3E中文嵌入模型"),
    ("shibing624/text2vec-base-chinese", "~100MB，text2vec中文模型"),
]

# 测试阈值范围
TEST_THRESHOLDS = [0.35, 0.4, 0.45, 0.5]

def load_benchmark() -> List[Dict]:
    """加载Bench 110测试集"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "data/test_set_110.json")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["test_cases"]

def evaluate_model(model_name: str, threshold: float = 0.35) -> Dict:
    """评估单个模型在指定阈值下的表现"""
    print(f"\n[INFO] 评估模型: {model_name}，阈值: {threshold}")
    
    # 初始化检测器
    detector = LogicDetector(
        threshold=threshold,
        chain_checker_model=model_name
    )
    
    # 加载测试集
    test_cases = load_benchmark()
    
    # 统计指标
    tp = 0  # True Positive
    tn = 0  # True Negative
    fp = 0  # False Positive
    fn = 0  # False Negative
    total_time = 0.0
    
    for idx, case in enumerate(test_cases):
        is_hallucination = (case["label"] == "hallucination")
        
        # 预测
        start_time = time.time()
        text = case["text"]
        result = detector.analyze(text)
        pred_is_hallucination = result.is_hallucination
        end_time = time.time()
        
        total_time += (end_time - start_time)
        
        # 统计
        if is_hallucination == True and pred_is_hallucination == True:
            tp += 1
        elif is_hallucination == False and pred_is_hallucination == False:
            tn += 1
        elif is_hallucination == False and pred_is_hallucination == True:
            fp += 1
        elif is_hallucination == True and pred_is_hallucination == False:
            fn += 1
    
    # 计算指标
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    avg_time_per_sample = total_time / total if total > 0 else 0.0
    
    return {
        "model_name": model_name,
        "threshold": threshold,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "avg_time_per_sample": avg_time_per_sample,
        "total_time": total_time
    }

def run_comparison():
    """运行所有模型对比"""
    results = []
    
    print("=== 嵌入模型对比测试 ===")
    print(f"测试模型数量: {len(TEST_MODELS)}")
    print(f"测试阈值: {TEST_THRESHOLDS}")
    print(f"测试集大小: {len(load_benchmark())} 样本")
    
    for model_name, model_desc in TEST_MODELS:
        print(f"\n[INFO] 测试模型: {model_name} ({model_desc})")
        for threshold in TEST_THRESHOLDS:
            result = evaluate_model(model_name, threshold)
            results.append(result)
            print(f"阈值 {threshold}: 准确率={result['accuracy']:.4f}, F1={result['f1']:.4f}, 精确率={result['precision']:.4f}, 召回率={result['recall']:.4f}")
    
    return results

def print_summary(results: List[Dict]):
    """打印汇总结果"""
    print("\n\n=== 对比结果汇总 ===")
    
    # 按F1排序
    sorted_results = sorted(results, key=lambda x: x["f1"], reverse=True)
    
    print(f"{'模型名':<40} {'阈值':<6} {'准确率':<8} {'F1':<8} {'精确率':<8} {'召回率':<8} {'平均耗时':<10}")
    print("-" * 120)
    
    for res in sorted_results:
        print(f"{res['model_name']:<40} {res['threshold']:<6} {res['accuracy']:.4f}  {res['f1']:.4f}  {res['precision']:.4f}  {res['recall']:.4f}  {res['avg_time_per_sample']*1000:.2f}ms")
    
    # 最佳模型
    best = sorted_results[0]
    print("\n🎉 最佳配置:")
    print(f"模型: {best['model_name']}")
    print(f"阈值: {best['threshold']}")
    print(f"准确率: {best['accuracy']:.4f} ({best['tp']+best['tn']}/{best['tp']+best['tn']+best['fp']+best['fn']})")
    print(f"F1: {best['f1']:.4f}")
    print(f"精确率: {best['precision']:.4f}")
    print(f"召回率: {best['recall']:.4f}")
    print(f"平均耗时: {best['avg_time_per_sample']*1000:.2f}ms/样本")
    
    # 保存结果
    with open("embedding_models_comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 embedding_models_comparison_results.json")

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    results = run_comparison()
    print_summary(results)
