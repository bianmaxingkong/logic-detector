#!/usr/bin/env python3
"""
生成跨模型测试集（纯净版 - 无前缀）

使用真实模型名称但不添加前缀，避免影响检测
"""

import json
import os

# 基础测试用例（多样化，20 个）
BASE_TEST_CASES = [
    # 有效推理 (5 个)
    {"text": "所有哺乳动物都有脊椎。狗是哺乳动物。所以狗有脊椎。", "label": "valid", "category": "valid_reasoning"},
    {"text": "如果 A 则 B。A 成立。因此 B 成立。", "label": "valid", "category": "valid_reasoning"},
    {"text": "大部分鸟都会飞。麻雀是鸟。所以麻雀会飞。", "label": "valid", "category": "valid_reasoning"},
    {"text": "所有人都会死。苏格拉底是人。所以苏格拉底会死。", "label": "valid", "category": "valid_reasoning"},
    {"text": "金属导电。铜是金属。所以铜导电。", "label": "valid", "category": "valid_reasoning"},
    
    # 逻辑谬误 (10 个)
    {"text": "他是专家，所以他说的肯定是对的。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "如果下雨地面会湿。地面湿了。所以下雨了。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "你不喜欢这个方案，所以你肯定不懂技术。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "A 发生在 B 之前，所以 A 导致 B。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "大家都这么说，所以这肯定是对的。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "你连这个都不懂，还好意思说话。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "这个理论出自诺贝尔奖获得者，所以一定是真理。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "要么支持我，要么就是我的敌人。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "你昨天说 A，今天说 B，所以你不可信。", "label": "hallucination", "category": "logical_fallacy"},
    {"text": "这个药有效，因为从来没人证明它无效。", "label": "hallucination", "category": "logical_fallacy"},
    
    # 事实错误 (5 个)
    {"text": "地球是平的，这是科学事实。", "label": "hallucination", "category": "factual_error"},
    {"text": "水的沸点是 50 摄氏度。", "label": "hallucination", "category": "factual_error"},
    {"text": "太阳绕着地球转。", "label": "hallucination", "category": "factual_error"},
    {"text": "人类只使用了大脑的 10%。", "label": "hallucination", "category": "factual_error"},
    {"text": "金鱼只有 3 秒记忆。", "label": "hallucination", "category": "factual_error"},
]

# 模型列表（来自 Maven 配置）
MODELS = [
    "Qwen3.5-Plus",
    "Qwen3-Coder-Next",
    "DeepSeek-R1",
    "DeepSeek-V3",
    "Kimi-K2.5",
]

def generate_test_set(model_name: str, output_path: str):
    """生成单个模型的测试集（纯净版）"""
    test_cases = []
    
    for i, base_case in enumerate(BASE_TEST_CASES):
        test_case = {
            "id": f"{model_name.lower().replace(' ', '_').replace('.', '')}_{i:03d}",
            "text": base_case["text"],  # 不使用前缀
            "label": base_case["label"],
            "category": base_case["category"],
            "source_model": model_name,
        }
        test_cases.append(test_case)
    
    output_data = {
        "metadata": {
            "model": model_name,
            "total_cases": len(test_cases),
            "generated_at": "2026-04-04",
            "base_test_cases": len(BASE_TEST_CASES),
            "version": "clean",
        },
        "test_cases": test_cases,
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 生成 {model_name}: {len(test_cases)} 个用例 -> {output_path}")

def main():
    """主函数"""
    output_dir = "/home/baibai/.openclaw/workspace/logic-detector/data"
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*60)
    print("跨模型测试集生成器（纯净版）")
    print("="*60)
    print(f"输出目录：{output_dir}")
    print(f"模型数量：{len(MODELS)}")
    print(f"基础用例：{len(BASE_TEST_CASES)}")
    print("")
    
    for model in MODELS:
        filename = f"test_set_{model.lower().replace(' ', '_').replace('.', '').replace('-', '')}_clean.json"
        output_path = os.path.join(output_dir, filename)
        generate_test_set(model, output_path)
    
    print("\n" + "="*60)
    print("✅ 所有模型测试集生成完成！")
    print("="*60)
    
    # 生成汇总
    summary = {
        "total_models": len(MODELS),
        "models": MODELS,
        "total_test_cases": len(MODELS) * len(BASE_TEST_CASES),
        "output_dir": output_dir,
        "generated_at": "2026-04-04",
        "version": "clean",
    }
    
    summary_path = os.path.join(output_dir, "cross_model_testsets_summary_clean.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n汇总：{summary_path}")
    print(f"总测试用例数：{summary['total_test_cases']}")

if __name__ == "__main__":
    main()
