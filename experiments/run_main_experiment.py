#!/usr/bin/env python3
"""
LogicDetector 主实验脚本 - 600 条测试集

运行完整的 600 样本测试，验证 81.7% 准确率

使用方法:
    python run_main_experiment.py
"""

import json
import sys
import os
from pathlib import Path

# 添加 src 目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from detector import LogicDetector, DetectionResult


def load_test_set(filepath: str) -> dict:
    """加载测试集"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate(detector: LogicDetector, test_cases: list) -> dict:
    """
    在测试集上评估检测器
    
    Returns:
        评估结果字典
    """
    total = len(test_cases)
    correct = 0
    tp = fp = tn = fn = 0
    
    detailed_results = []
    
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
        
        # 记录详细结果
        detailed_results.append({
            'id': case.get('id', f'case_{i}'),
            'text': text[:100],  # 截断以便存储
            'true_label': true_label,
            'pred_label': pred_label,
            'is_correct': is_correct,
            'confidence': result.confidence,
            'fallacies': result.logic_fallacies,
        })
    
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
        'detailed_results': detailed_results,
    }


def print_results(results: dict, dataset_name: str):
    """打印评估结果"""
    print(f"\n{'='*60}")
    print(f"数据集：{dataset_name}")
    print(f"{'='*60}")
    print(f"总样本数：{results['total']}")
    print(f"正确判断：{results['correct']}")
    print(f"准确率：{results['accuracy']*100:.1f}%")
    print(f"精确率：{results['precision']*100:.1f}%")
    print(f"召回率：{results['recall']*100:.1f}%")
    print(f"F1 分数：{results['f1']*100:.1f}%")
    print(f"\n混淆矩阵:")
    print(f"  TP (真阳性): {results['tp']}")
    print(f"  FP (假阳性): {results['fp']}")
    print(f"  TN (真阴性): {results['tn']}")
    print(f"  FN (假阴性): {results['fn']}")
    print(f"{'='*60}\n")


def main():
    """主函数"""
    print("LogicDetector 主实验 - 600 条测试集")
    print("="*60)
    
    # 初始化检测器
    detector = LogicDetector(threshold=0.35)
    print("✓ 检测器初始化完成")
    
    # 加载测试集
    test_set_path = project_root / "data" / "test_set_full_600.json"
    
    if not test_set_path.exists():
        print(f"❌ 测试集文件不存在：{test_set_path}")
        print("请先生成测试集：python data/generate_full_test_set.py")
        sys.exit(1)
    
    print(f"加载测试集：{test_set_path}")
    data = load_test_set(str(test_set_path))
    test_cases = data['test_cases']
    print(f"✓ 加载 {len(test_cases)} 个测试用例")
    
    # 运行评估
    print("\n运行检测...")
    results = evaluate(detector, test_cases)
    
    # 打印结果
    print_results(results, "LogicDetector-Bench (600 条)")
    
    # 保存结果
    output_path = Path(__file__).parent / "experiments" / "main_experiment_600_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 结果已保存到：{output_path}")
    
    # 生成 Markdown 报告
    report_path = Path(__file__).parent / "experiments" / "main_experiment_600_report.md"
    
    report_content = f"""# LogicDetector 主实验报告 (600 条测试集)

**实验时间**: {Path(output_path).stat().st_mtime}
**测试集**: LogicDetector-Bench (600 条)

---

## 📊 主要指标

| 指标 | 数值 |
|------|------|
| 总样本数 | {results['total']} |
| 正确判断 | {results['correct']} |
| **准确率** | **{results['accuracy']*100:.1f}%** |
| 精确率 | {results['precision']*100:.1f}% |
| 召回率 | {results['recall']*100:.1f}% |
| F1 分数 | {results['f1']*100:.1f}% |

---

## 🎯 混淆矩阵

| | 预测幻觉 | 预测有效 |
|---|---|---|
| **真实幻觉** | {results['tp']} (TP) | {results['fn']} (FN) |
| **真实有效** | {results['fp']} (FP) | {results['tn']} (TN) |

---

## 📈 与目标对比

| 指标 | 目标值 | 实际值 | 达成率 |
|------|--------|--------|--------|
| 准确率 | 81.7% | {results['accuracy']*100:.1f}% | {results['accuracy']/0.817*100:.1f}% |

---

## ✅ 实验状态

{"🎉 实验成功！准确率达到或超过 81.7% 目标" if results['accuracy'] >= 0.817 else "⚠️ 准确率略低于目标，需要进一步优化"}

---

**备注**: 详细结果见 `{output_path.name}`
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✓ 实验报告已保存到：{report_path}")
    
    # 返回退出码
    if results['accuracy'] >= 0.80:
        print("\n✅ 实验成功！")
        sys.exit(0)
    else:
        print("\n⚠️  准确率低于预期，请检查")
        sys.exit(1)


if __name__ == "__main__":
    main()
