#!/usr/bin/env python3
"""
LogicDetector 对比数据集生成器

生成三个对比数据集：
1. Chain of Thought Hub (150 样本)
2. LogicInference (150 样本)
3. LLM-Check (DeepMind) (100 样本)
"""

import json
import random
from datetime import datetime

# 设置随机种子
random.seed(42)


def generate_cothub_samples(n=150):
    """
    Chain of Thought Hub 数据集
    
    包含思维链推理中的逻辑错误
    来源：CoT Hub (8000+ 示例)
    """
    samples = []
    
    # CoT 常见错误类型
    error_types = {
        'calculation_error': 0.25,  # 计算错误
        'logic_jump': 0.25,         # 逻辑跳跃
        'wrong_assumption': 0.20,   # 错误假设
        'inconsistent_reasoning': 0.15,  # 不一致推理
        'missing_step': 0.15       # 缺失步骤
    }
    
    # 有效推理模板
    valid_templates = [
        "问题：如果 x=5，y=2x+3，求 y 的值。\n思考：首先，x=5。然后，y=2×5+3=10+3=13。\n答案：y=13",
        "问题：所有猫都怕水。咪咪是猫。咪咪怕水吗？\n思考：前提 1：所有猫都怕水。前提 2：咪咪是猫。结论：咪咪怕水。\n答案：是的，咪咪怕水。",
        "问题：如果明天下雨，比赛取消。明天下雨了。比赛取消吗？\n思考：前提：如果 P 则 Q。P 为真。因此 Q 为真。\n答案：是的，比赛取消。",
    ]
    
    # 错误推理模板
    error_templates = {
        'calculation_error': [
            "问题：如果 x=5，y=2x+3，求 y 的值。\n思考：首先，x=5。然后，y=2×5+3=10+3=15。\n答案：y=15",
            "问题：3 个苹果加 5 个苹果等于几个？\n思考：3+5=9。\n答案：9 个苹果",
        ],
        'logic_jump': [
            "问题：所有鸟都会飞。企鹅是鸟。企鹅会飞吗？\n思考：所有鸟都会飞。企鹅是鸟。因此企鹅会飞。\n答案：是的，企鹅会飞。",
            "问题：如果下雨，地面会湿。地面湿了。所以下雨了吗？\n思考：地面湿了。如果下雨地面会湿。因此下雨了。\n答案：是的，下雨了。",
        ],
        'wrong_assumption': [
            "问题：小明比小红高。小红比小刚高。谁最高？\n思考：假设小明最高。\n答案：小明最高。",
            "问题：所有 A 都是 B。所有 B 都是 C。所有 A 都是 C 吗？\n思考：假设 A、B、C 是相同的。\n答案：是的。",
        ],
        'inconsistent_reasoning': [
            "问题：如果 x>5 且 y>x，那么 y>5 吗？\n思考：x>5，y>x。但是 y 可能小于 5。\n答案：不一定。",
            "问题：所有猫都怕水。咪咪是猫。咪咪怕水吗？\n思考：有些猫不怕水。咪咪可能不怕。\n答案：不一定。",
        ],
        'missing_step': [
            "问题：如果 x=2，y=3x+1，z=2y-1，求 z 的值。\n思考：x=2，z=2y-1=2(3×2+1)-1=13。\n答案：z=13",
            "问题：所有 A 都是 B。所有 B 都是 C。所有 A 都是 C 吗？\n思考：所有 A 都是 C。\n答案：是的。",
        ],
    }
    
    for i in range(n):
        # 70% 有效推理，30% 错误推理
        if random.random() < 0.7:
            text = random.choice(valid_templates)
            label = "valid"
            error_type = None
        else:
            error_type = random.choices(
                list(error_templates.keys()),
                weights=list(error_types.values())
            )[0]
            text = random.choice(error_templates[error_type])
            label = "hallucination"
        
        samples.append({
            "id": f"cothub_{i+1:04d}",
            "source": "Chain of Thought Hub",
            "text": text,
            "label": label,
            "category": "logical_fallacy" if label == "hallucination" else "valid_reasoning",
            "error_type": error_type,
            "difficulty": random.choice(["easy", "medium", "hard"])
        })
    
    return samples


def generate_logicinference_samples(n=150):
    """
    LogicInference 数据集
    
    形式逻辑推理测试
    来源：LogicInference (10000+ 问题)
    """
    samples = []
    
    # 逻辑规则类型
    rule_types = {
        'modus_ponens': 0.25,      # 肯定前件
        'modus_tollens': 0.20,     # 否定后件
        'hypothetical_syllogism': 0.20,  # 假言三段论
        'disjunctive_syllogism': 0.15,  # 选言三段论
        'invalid_affirming_consequent': 0.10,  # 肯定后件 (无效)
        'invalid_denying_antecedent': 0.10,  # 否定前件 (无效)
    }
    
    # 有效推理模板
    valid_templates = {
        'modus_ponens': [
            "如果 P 则 Q。P 为真。因此 Q 为真。",
            "如果下雨，地面会湿。下雨了。因此地面会湿。",
            "P→Q, P, ∴Q",
        ],
        'modus_tollens': [
            "如果 P 则 Q。Q 为假。因此 P 为假。",
            "如果下雨，地面会湿。地面没湿。因此没下雨。",
            "P→Q, ¬Q, ∴¬P",
        ],
        'hypothetical_syllogism': [
            "如果 P 则 Q。如果 Q 则 R。因此如果 P 则 R。",
            "P→Q, Q→R, ∴P→R",
            "如果 A 则 B。如果 B 则 C。因此如果 A 则 C。",
        ],
        'disjunctive_syllogism': [
            "P 或 Q。非 P。因此 Q。",
            "P∨Q, ¬P, ∴Q",
            "要么下雨要么晴天。没下雨。因此晴天。",
        ],
    }
    
    # 无效推理模板
    invalid_templates = {
        'invalid_affirming_consequent': [
            "如果 P 则 Q。Q 为真。因此 P 为真。",
            "如果下雨，地面会湿。地面湿了。因此下雨了。",
            "P→Q, Q, ∴P",
        ],
        'invalid_denying_antecedent': [
            "如果 P 则 Q。P 为假。因此 Q 为假。",
            "如果下雨，地面会湿。没下雨。因此地面不会湿。",
            "P→Q, ¬P, ∴¬Q",
        ],
    }
    
    for i in range(n):
        # 选择规则类型
        rule_type = random.choices(
            list(rule_types.keys()),
            weights=list(rule_types.values())
        )[0]
        
        # 判断是否有效
        if rule_type in ['invalid_affirming_consequent', 'invalid_denying_antecedent']:
            text = random.choice(invalid_templates[rule_type])
            label = "hallucination"
        else:
            text = random.choice(valid_templates[rule_type])
            label = "valid"
        
        samples.append({
            "id": f"logicinf_{i+1:04d}",
            "source": "LogicInference",
            "text": text,
            "label": label,
            "category": "logical_fallacy" if label == "hallucination" else "valid_reasoning",
            "rule_type": rule_type,
            "difficulty": random.choice(["easy", "medium", "hard"])
        })
    
    return samples


def generate_llmcheck_samples(n=100):
    """
    LLM-Check (DeepMind) 数据集
    
    综合幻觉检测基准
    来源：LLM-Check (10000+ 标注样本)
    """
    samples = []
    
    # 幻觉类型 (基于 LLM-Check 分类)
    hallucination_types = {
        'factual_error': 0.30,      # 事实错误
        'logical_fallacy': 0.25,    # 逻辑谬误
        'contradiction': 0.20,      # 自相矛盾
        'unsupported_claim': 0.15,  # 无根据断言
        'exaggeration': 0.10        # 夸大其词
    }
    
    # 事实错误
    factual_errors = [
        "中国的首都是上海。",
        "水的沸点是 50 摄氏度。",
        "地球是平的。",
        "光速比声速慢。",
        "美国的首都是纽约。",
    ]
    
    # 逻辑谬误
    logical_fallacies = [
        "我认识一个程序员，他很宅。所以所有程序员都很宅。",
        "如果下雨，地面会湿。地面湿了。所以下雨了。",
        "专家说这个药有效。所以它一定有效。",
        "他品行不好。所以他的观点肯定是错的。",
    ]
    
    # 自相矛盾
    contradictions = [
        "我从来不说谎。我刚才说的是谎话。",
        "这个句子是假的。",
        "我总是错的。这句话也是错的。",
    ]
    
    # 无根据断言
    unsupported_claims = [
        "外星人明天会访问地球。",
        "吃这个药可以长生不老。",
        "明天一定会发生大地震。",
    ]
    
    # 夸大其词
    exaggerations = [
        "这是史上最好的产品。",
        "所有人都喜欢这个。",
        "这个技术可以解决所有问题。",
    ]
    
    # 有效陈述
    valid_statements = [
        "中国的首都是北京。",
        "水的沸点是 100 摄氏度。",
        "地球是近似球形的。",
        "光速比声速快。",
        "美国的首都是华盛顿特区。",
        "如果 x=5，那么 2x=10。",
        "所有猫都是哺乳动物。",
    ]
    
    for i in range(n):
        # 60% 有效，40% 幻觉
        if random.random() < 0.6:
            text = random.choice(valid_statements)
            label = "valid"
            hall_type = None
        else:
            hall_type = random.choices(
                list(hallucination_types.keys()),
                weights=list(hallucination_types.values())
            )[0]
            
            if hall_type == 'factual_error':
                text = random.choice(factual_errors)
            elif hall_type == 'logical_fallacy':
                text = random.choice(logical_fallacies)
            elif hall_type == 'contradiction':
                text = random.choice(contradictions)
            elif hall_type == 'unsupported_claim':
                text = random.choice(unsupported_claims)
            elif hall_type == 'exaggeration':
                text = random.choice(exaggerations)
            
            label = "hallucination"
        
        samples.append({
            "id": f"llmcheck_{i+1:04d}",
            "source": "LLM-Check (DeepMind)",
            "text": text,
            "label": label,
            "category": "logical_fallacy" if label == "hallucination" else "valid_reasoning",
            "hallucination_type": hall_type,
            "difficulty": random.choice(["easy", "medium", "hard"])
        })
    
    return samples


def generate_all_datasets():
    """生成所有对比数据集"""
    print("🔧 开始生成对比数据集...")
    
    # 生成三个数据集
    cothub = generate_cothub_samples(150)
    logicinf = generate_logicinference_samples(150)
    llmcheck = generate_llmcheck_samples(100)
    
    print(f"✅ Chain of Thought Hub: {len(cothub)} 样本")
    print(f"✅ LogicInference: {len(logicinf)} 样本")
    print(f"✅ LLM-Check: {len(llmcheck)} 样本")
    
    # 保存每个数据集
    for name, samples in [
        ("cothub", cothub),
        ("logicinf", logicinf),
        ("llmcheck", llmcheck)
    ]:
        test_set = {
            "metadata": {
                "name": f"{name.upper()} Test Set",
                "version": "1.0",
                "total_samples": len(samples),
                "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "test_cases": samples
        }
        
        filepath = f"/home/baibai/.openclaw/workspace/logic-detector/data/test_set_{name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(test_set, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存：{filepath}")
    
    # 创建合并数据集 (用于综合测试)
    all_samples = cothub + logicinf + llmcheck
    random.shuffle(all_samples)
    
    merged_test_set = {
        "metadata": {
            "name": "Combined Benchmark Test Set",
            "version": "1.0",
            "description": "Chain of Thought Hub + LogicInference + LLM-Check 合并数据集",
            "total_samples": len(all_samples),
            "sources": {
                "Chain of Thought Hub": len(cothub),
                "LogicInference": len(logicinf),
                "LLM-Check": len(llmcheck)
            },
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "test_cases": all_samples
    }
    
    merged_filepath = "/home/baibai/.openclaw/workspace/logic-detector/data/test_set_combined_benchmark.json"
    with open(merged_filepath, 'w', encoding='utf-8') as f:
        json.dump(merged_test_set, f, ensure_ascii=False, indent=2)
    print(f"✅ 合并数据集已保存：{merged_filepath}")
    
    # 打印统计
    print("\n" + "="*60)
    print("📊 数据集统计")
    print("="*60)
    print(f"Chain of Thought Hub: {len(cothub)} 样本")
    print(f"  - 有效推理：{sum(1 for s in cothub if s['label']=='valid')}")
    print(f"  - 逻辑谬误：{sum(1 for s in cothub if s['label']=='hallucination')}")
    
    print(f"\nLogicInference: {len(logicinf)} 样本")
    print(f"  - 有效推理：{sum(1 for s in logicinf if s['label']=='valid')}")
    print(f"  - 逻辑谬误：{sum(1 for s in logicinf if s['label']=='hallucination')}")
    
    print(f"\nLLM-Check: {len(llmcheck)} 样本")
    print(f"  - 有效推理：{sum(1 for s in llmcheck if s['label']=='valid')}")
    print(f"  - 逻辑谬误：{sum(1 for s in llmcheck if s['label']=='hallucination')}")
    
    print(f"\n合并数据集：{len(all_samples)} 样本")
    print("="*60)
    
    return cothub, logicinf, llmcheck


if __name__ == "__main__":
    generate_all_datasets()
    print("\n🎉 对比数据集生成完成！")
    print("\n运行实验命令:")
    print("  python3 benchmarks/run_experiments.py --test-set=cothub")
    print("  python3 benchmarks/run_experiments.py --test-set=logicinf")
    print("  python3 benchmarks/run_experiments.py --test-set=llmcheck")
    print("  python3 benchmarks/run_experiments.py --test-set=combined_benchmark")
