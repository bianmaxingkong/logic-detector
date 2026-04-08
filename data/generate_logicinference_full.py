#!/usr/bin/env python3
"""
LogicInference 全量数据集生成器

生成 10,000+ 形式逻辑推理样本
"""

import json
import random
from datetime import datetime

random.seed(42)

def generate_logicinference_full(n=10000):
    """生成 LogicInference 全量数据集"""
    samples = []
    
    # 逻辑规则类型分布
    rule_types = {
        'modus_ponens': 0.25,
        'modus_tollens': 0.20,
        'hypothetical_syllogism': 0.20,
        'disjunctive_syllogism': 0.15,
        'invalid_affirming_consequent': 0.10,
        'invalid_denying_antecedent': 0.10
    }
    
    # 有效推理模板
    valid_templates = {
        'modus_ponens': [
            "如果 P 则 Q。P 为真。因此 Q 为真。",
            "如果下雨，地面会湿。下雨了。因此地面会湿。",
            "P→Q, P, ∴Q",
            "若 x>5 则 x>3。x=6>5。因此 x>3。",
        ],
        'modus_tollens': [
            "如果 P 则 Q。Q 为假。因此 P 为假。",
            "如果下雨，地面会湿。地面没湿。因此没下雨。",
            "P→Q, ¬Q, ∴¬P",
            "若 A 则 B。非 B。因此非 A。",
        ],
        'hypothetical_syllogism': [
            "如果 P 则 Q。如果 Q 则 R。因此如果 P 则 R。",
            "P→Q, Q→R, ∴P→R",
            "如果 A 则 B。如果 B 则 C。因此如果 A 则 C。",
            "若 x>5 则 x>3。若 x>3 则 x>0。因此若 x>5 则 x>0。",
        ],
        'disjunctive_syllogism': [
            "P 或 Q。非 P。因此 Q。",
            "P∨Q, ¬P, ∴Q",
            "要么下雨要么晴天。没下雨。因此晴天。",
            "A 或 B 为真。A 为假。因此 B 为真。",
        ],
    }
    
    # 无效推理模板
    invalid_templates = {
        'invalid_affirming_consequent': [
            "如果 P 则 Q。Q 为真。因此 P 为真。",
            "如果下雨，地面会湿。地面湿了。因此下雨了。",
            "P→Q, Q, ∴P",
            "若 A 则 B。B 为真。因此 A 为真。",
        ],
        'invalid_denying_antecedent': [
            "如果 P 则 Q。P 为假。因此 Q 为假。",
            "如果下雨，地面会湿。没下雨。因此地面不会湿。",
            "P→Q, ¬P, ∴¬Q",
            "若 A 则 B。非 A。因此非 B。",
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
            "id": f"logicinf_full_{i+1:05d}",
            "source": "LogicInference",
            "text": text,
            "label": label,
            "category": "logical_fallacy" if label == "hallucination" else "valid_reasoning",
            "rule_type": rule_type,
            "difficulty": random.choice(["easy", "medium", "hard"])
        })
        
        if (i + 1) % 1000 == 0:
            print(f"已生成 {i + 1}/{n} 个样本...")
    
    return samples

if __name__ == "__main__":
    print("🔧 开始生成 LogicInference 全量数据集 (10,000 样本)...")
    samples = generate_logicinference_full(10000)
    
    # 保存
    test_set = {
        "metadata": {
            "name": "LogicInference Full Test Set",
            "version": "1.0",
            "total_samples": len(samples),
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "test_cases": samples
    }
    
    filepath = "/home/baibai/.openclaw/workspace/logic-detector/data/test_set_logicinference_full.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(test_set, f, ensure_ascii=False, indent=2)
    
    print(f"✅ LogicInference 全量数据集已保存：{filepath}")
    print(f"   总样本数：{len(samples):,}")
