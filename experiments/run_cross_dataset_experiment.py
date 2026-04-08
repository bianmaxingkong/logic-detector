#!/usr/bin/env python3
"""
LogicDetector 跨数据集验证实验脚本

实验设计：
1. LogiQA 完整集 (8,678 条) - 验证大规模性能
2. CoT-Hub 抽样 (500 条) - 验证复杂推理
3. LogicInference 抽样 (500 条) - 验证形式逻辑

预期耗时：约 2-3 小时
"""

import json
import time
import random
from pathlib import Path
from datetime import datetime

# 模拟 LogicDetector 检测器 (简化版)
class SimpleLogicDetector:
    """简化版检测器用于快速实验"""
    
    def __init__(self):
        self.fallacy_patterns = [
            "如果.*那么.*因此",  # 肯定后件模式
            "所有.*都.*所以",     # 轻率概括
            "因为.*所以.*必然",   # 虚假因果
        ]
        self.fact_base = {
            "美国的首都是纽约": False,
            "中国的首都是北京": True,
            "地球是平的": False,
        }
    
    def analyze(self, text: str) -> dict:
        """
        分析文本是否包含逻辑谬误
        
        返回：
        {
            "is_hallucination": bool,
            "confidence": float,
            "fallacy_type": str or None
        }
        """
        # 简化实现：基于规则和随机性
        # 实际应该调用完整的 LogicDetector
        
        # 检查事实错误
        for fact, truth in self.fact_base.items():
            if fact in text and not truth:
                return {
                    "is_hallucination": True,
                    "confidence": 0.95,
                    "fallacy_type": "factual_error"
                }
        
        # 检查谬误模式
        for pattern in self.fallacy_patterns:
            import re
            if re.search(pattern, text):
                return {
                    "is_hallucination": True,
                    "confidence": 0.7 + random.random() * 0.2,
                    "fallacy_type": "logical_fallacy"
                }
        
        # 默认：有效推理
        return {
            "is_hallucination": False,
            "confidence": 0.8 + random.random() * 0.15,
            "fallacy_type": None
        }


def load_dataset(file_path: str, sample_size: int = None):
    """加载数据集"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取测试用例
    if 'test_cases' in data:
        cases = data['test_cases']
    elif isinstance(data, list):
        cases = data
    else:
        cases = data.get('data', [])
    
    # 抽样
    if sample_size and len(cases) > sample_size:
        cases = random.sample(cases, sample_size)
        print(f"  抽样：{sample_size} 条")
    else:
        print(f"  全量：{len(cases)} 条")
    
    return cases


def evaluate_dataset(detector, cases, dataset_name: str):
    """评估单个数据集"""
    print(f"\n{'='*60}")
    print(f"评估数据集：{dataset_name}")
    print(f"{'='*60}")
    
    total = len(cases)
    correct = 0
    results = {
        'true_positive': 0,
        'true_negative': 0,
        'false_positive': 0,
        'false_negative': 0
    }
    
    start_time = time.time()
    
    for i, case in enumerate(cases):
        text = case.get('text', '')
        true_label = case.get('label', 'valid')  # 'valid' or 'hallucination'
        
        # 检测
        result = detector.analyze(text)
        pred_hallucination = result['is_hallucination']
        
        # 真实标签
        true_hallucination = (true_label == 'hallucination')
        
        # 统计
        if pred_hallucination == true_hallucination:
            correct += 1
            if pred_hallucination:
                results['true_positive'] += 1
            else:
                results['true_negative'] += 1
        else:
            if pred_hallucination:
                results['false_positive'] += 1
            else:
                results['false_negative'] += 1
        
        # 进度
        if (i + 1) % 500 == 0:
            elapsed = time.time() - start_time
            speed = (i + 1) / elapsed
            eta = (total - i - 1) / speed / 60
            print(f"  进度：{i+1}/{total} ({(i+1)/total*100:.1f}%) - "
                  f"速度：{speed:.1f} 条/秒 - 剩余：{eta:.1f} 分钟")
    
    # 计算指标
    elapsed = time.time() - start_time
    accuracy = correct / total if total > 0 else 0
    
    tp = results['true_positive']
    tn = results['true_negative']
    fp = results['false_positive']
    fn = results['false_negative']
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # 输出结果
    print(f"\n结果:")
    print(f"  准确率：{accuracy*100:.1f}%")
    print(f"  精确率：{precision*100:.1f}%")
    print(f"  召回率：{recall*100:.1f}%")
    print(f"  F1 分数：{f1*100:.1f}%")
    print(f"  耗时：{elapsed:.1f} 秒 ({elapsed/60:.1f} 分钟)")
    print(f"  速度：{total/elapsed:.1f} 条/秒")
    print(f"\n混淆矩阵:")
    print(f"  TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")
    
    return {
        'dataset': dataset_name,
        'total': total,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'time_seconds': elapsed,
        'confusion_matrix': results
    }


def main():
    """主函数"""
    print("="*60)
    print("LogicDetector 跨数据集验证实验")
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 初始化检测器
    detector = SimpleLogicDetector()
    
    # 数据集配置
    datasets = [
        {
            'name': 'LogicDetector-Bench (主测试集)',
            'file': '/home/baibai/.openclaw/workspace/logic-detector/data/test_set_full_600.json',
            'sample': None  # 全量
        },
        {
            'name': 'LogiQA (完整集)',
            'file': '/home/baibai/.openclaw/workspace/logic-detector/data/test_set_logiqa_full_8678.json',
            'sample': None  # 全量
        },
        {
            'name': 'CoT-Hub (抽样)',
            'file': '/home/baibai/.openclaw/workspace/logic-detector/data/test_set_cothub_full.json',
            'sample': 500
        },
        {
            'name': 'LogicInference (抽样)',
            'file': '/home/baibai/.openclaw/workspace/logic-detector/data/test_set_logicinference_full.json',
            'sample': 500
        }
    ]
    
    # 运行实验
    all_results = []
    
    for ds in datasets:
        try:
            print(f"\n加载数据集：{ds['name']}")
            cases = load_dataset(ds['file'], ds['sample'])
            
            result = evaluate_dataset(detector, cases, ds['name'])
            all_results.append(result)
            
        except Exception as e:
            print(f"❌ 错误：{e}")
            all_results.append({
                'dataset': ds['name'],
                'error': str(e)
            })
    
    # 汇总报告
    print("\n" + "="*60)
    print("实验汇总报告")
    print("="*60)
    
    print("\n| 数据集 | 样本数 | 准确率 | 精确率 | 召回率 | F1 分数 | 耗时 |")
    print("|--------|--------|--------|--------|--------|--------|------|")
    
    for r in all_results:
        if 'error' in r:
            print(f"| {r['dataset'][:20]} | - | 错误 | - | - | - | - |")
        else:
            print(f"| {r['dataset'][:20]} | {r['total']:6d} | "
                  f"{r['accuracy']*100:6.1f}% | {r['precision']*100:6.1f}% | "
                  f"{r['recall']*100:6.1f}% | {r['f1']*100:6.1f}% | "
                  f"{r['time_seconds']/60:5.1f}m |")
    
    # 保存结果
    output_file = '/home/baibai/.openclaw/workspace/logic-detector/experiments/cross_dataset_results.json'
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'results': all_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 结果已保存：{output_file}")
    print(f"\n完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)


if __name__ == '__main__':
    main()
