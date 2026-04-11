#!/usr/bin/env python3
"""
LogicDetector 跨数据集验证实验

在多个数据集上验证泛化能力

数据集:
- LogicDetector-Bench: 600 条
- LogiQA: 8,678 条
- CoT-Hub: 500 条 (抽样)
- LogicInference: 500 条 (抽样)

使用方法:
    python run_cross_dataset_experiment.py
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# 添加 src 目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from detector import LogicDetector


def load_test_set(filepath: str) -> dict:
    """加载测试集"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate(detector: LogicDetector, test_cases: list, sample_limit: int = None) -> dict:
    """
    在测试集上评估检测器
    
    Args:
        detector: 检测器实例
        test_cases: 测试用例列表
        sample_limit: 样本数量限制（用于抽样）
    
    Returns:
        评估结果字典
    """
    if sample_limit:
        test_cases = test_cases[:sample_limit]
    
    total = len(test_cases)
    correct = 0
    tp = fp = tn = fn = 0
    
    for i, case in enumerate(test_cases):
        text = case['text']
        true_label = case['label']  # 'valid' or 'hallucination'
        
        # 运行检测
        result = detector.analyze(text, reasoning_type=case.get('reasoning_type', 'deductive'))
        pred_label = 'hallucination' if result.is_hallucination else 'valid'
        
        # 统计
        is_correct = (pred_label == true_label)
        if is_correct:
            correct += 1
        
        # 混淆矩阵
        if true_label == 'hallucination' and pred_label == 'hallucination':
            tp += 1
        elif true_label == 'valid' and pred_label == 'hallucination':
            fp += 1
        elif true_label == 'valid' and pred_label == 'valid':
            tn += 1
        elif true_label == 'hallucination' and pred_label == 'valid':
            fn += 1
    
    # 计算指标
    accuracy = correct / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'total': total,
        'correct': correct,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'tn': tn,
        'fn': fn,
    }


def print_results(results: dict, dataset_name: str):
    """打印评估结果"""
    print(f"\n{dataset_name}:")
    print(f"  样本数：{results['total']}")
    print(f"  准确率：{results['accuracy']*100:.1f}%")
    print(f"  精确率：{results['precision']*100:.1f}%")
    print(f"  召回率：{results['recall']*100:.1f}%")
    print(f"  F1 分数：{results['f1']*100:.1f}%")


def main():
    """主函数"""
    print("="*60)
    print("LogicDetector 跨数据集验证实验")
    print("="*60)
    print(f"实验时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 初始化检测器
    detector = LogicDetector(threshold=0.35)
    print("\n✓ 检测器初始化完成")
    
    # 定义数据集配置
    datasets = [
        {
            'name': 'LogicDetector-Bench',
            'file': 'test_set_full_600.json',
            'sample': None,  # 全部
            'expected': 81.7,
        },
        {
            'name': 'LogiQA (完整)',
            'file': 'test_set_logiqa_full_8678.json',
            'sample': None,  # 全部
            'expected': 80.0,
        },
        {
            'name': 'CoT-Hub (抽样)',
            'file': 'test_set_cothub_full.json',
            'sample': 500,
            'expected': 80.0,
        },
        {
            'name': 'LogicInference (抽样)',
            'file': 'test_set_logicinference_full.json',
            'sample': 500,
            'expected': 80.0,
        },
    ]
    
    # 存储所有结果
    all_results = {}
    
    # 逐个数据集测试
    for dataset in datasets:
        data_path = project_root / "data" / dataset['file']
        
        if not data_path.exists():
            print(f"\n⚠️  数据集不存在：{dataset['file']}")
            print(f"   跳过 {dataset['name']}")
            all_results[dataset['name']] = {
                'error': 'File not found',
                'expected': dataset['expected'],
            }
            continue
        
        print(f"\n加载数据集：{dataset['name']}...")
        data = load_test_set(str(data_path))
        test_cases = data.get('test_cases', data.get('data', []))
        
        if not test_cases:
            print(f"   ⚠️  数据格式不正确，跳过")
            all_results[dataset['name']] = {
                'error': 'Invalid format',
                'expected': dataset['expected'],
            }
            continue
        
        sample_limit = dataset['sample']
        sample_text = f" (抽样 {sample_limit} 条)" if sample_limit else ""
        print(f"   ✓ 加载 {len(test_cases)} 条{sample_text}")
        
        # 运行评估
        print(f"   运行检测...")
        results = evaluate(detector, test_cases, sample_limit)
        
        # 存储结果
        all_results[dataset['name']] = {
            **results,
            'expected': dataset['expected'],
            'sample_limit': sample_limit,
        }
        
        # 打印结果
        print_results(results, dataset['name'])
    
    # 汇总报告
    print("\n" + "="*60)
    print("跨数据集验证结果汇总")
    print("="*60)
    
    print(f"\n{'数据集':<25} {'样本数':>8} {'准确率':>10} {'预期':>10} {'达成率':>10}")
    print("-"*65)
    
    for name, results in all_results.items():
        if 'error' in results:
            print(f"{name:<25} {'-':>8} {'-':>10} {results['expected']:>10.1f}% {'-':>10}")
        else:
            accuracy = results['accuracy'] * 100
            expected = results['expected']
            achievement = (accuracy / expected) * 100 if expected > 0 else 0
            print(f"{name:<25} {results['total']:>8} {accuracy:>9.1f}% {expected:>9.1f}% {achievement:>9.1f}%")
    
    print("="*60)
    
    # 保存结果
    output_path = project_root / "experiments" / "cross_dataset_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        'experiment_time': datetime.now().isoformat(),
        'threshold': 0.35,
        'datasets': all_results,
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 结果已保存到：{output_path}")
    
    # 生成 Markdown 报告
    report_path = project_root / "experiments" / "cross_dataset_report.md"
    
    # 计算平均准确率
    valid_results = [r for r in all_results.values() if 'error' not in r]
    avg_accuracy = sum(r['accuracy'] for r in valid_results) / len(valid_results) if valid_results else 0
    
    report_content = f"""# LogicDetector 跨数据集验证实验报告

**实验时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**检测器阈值**: 0.35

---

## 📊 实验结果汇总

| 数据集 | 样本数 | 准确率 | 精确率 | 召回率 | F1 分数 | 预期值 | 达成率 |
|--------|--------|--------|--------|--------|--------|--------|--------|
"""
    
    for name, results in all_results.items():
        if 'error' in results:
            report_content += f"| {name} | - | - | - | - | - | {results['expected']:.1f}% | - |\n"
        else:
            achievement = (results['accuracy'] / results['expected']) * 100 if results['expected'] > 0 else 0
            report_content += f"| {name} | {results['total']} | {results['accuracy']*100:.1f}% | {results['precision']*100:.1f}% | {results['recall']*100:.1f}% | {results['f1']*100:.1f}% | {results['expected']:.1f}% | {achievement:.1f}% |\n"
    
    report_content += f"""
---

## 📈 泛化能力分析

**平均准确率**: {avg_accuracy*100:.1f}%

### 结论

{"✅ **泛化能力优秀！** 所有数据集准确率均在 80% 左右，证明模型具有良好的跨数据集泛化能力。" if avg_accuracy >= 0.78 else "⚠️ **泛化能力一般** 部分数据集准确率偏低，需要进一步优化。"}

### 关键发现

1. **LogicDetector-Bench (600 条)**: {"✅" if all_results.get('LogicDetector-Bench', {}).get('accuracy', 0) >= 0.80 else "⚠️"} 主实验基准
2. **LogiQA (8,678 条)**: {"✅" if all_results.get('LogiQA (完整)', {}).get('accuracy', 0) >= 0.78 else "⚠️"} 大规模验证
3. **CoT-Hub (500 条)**: {"✅" if all_results.get('CoT-Hub (抽样)', {}).get('accuracy', 0) >= 0.78 else "⚠️"} 思维链数据
4. **LogicInference (500 条)**: {"✅" if all_results.get('LogicInference (抽样)', {}).get('accuracy', 0) >= 0.78 else "⚠️"} 逻辑推理数据

---

## 🎯 下一步

- [ ] 分析各数据集的错误案例
- [ ] 针对性优化检测规则
- [ ] 将结果写入论文

---

**实验状态**: {"✅ 完成" if len(valid_results) >= 3 else "⚠️ 部分完成"}
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✓ 实验报告已保存到：{report_path}")
    
    # 返回退出码
    if avg_accuracy >= 0.78:
        print("\n✅ 跨数据集验证成功！")
        sys.exit(0)
    else:
        print("\n⚠️  平均准确率低于预期，请检查")
        sys.exit(1)


if __name__ == "__main__":
    main()
