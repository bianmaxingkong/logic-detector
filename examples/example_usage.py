"""
LogicDetector 使用示例

演示如何使用 LogicDetector 框架分析文本的逻辑结构和检测逻辑谬误
"""

from src.detector import LogicDetector, FallacyType, TruthLevel


def main():
    # 创建检测器
    detector = LogicDetector()
    
    # 示例文本：达利欧关于霍尔木兹海峡的评论
    text = """
    霍尔木兹海峡是全球 30% 石油运输通道。
    美伊冲突可能升级。
    伊朗可能封锁霍尔木兹海峡。
    因此，这将改变世界。
    """
    
    print("=" * 60)
    print("LogicDetector 逻辑分析示例")
    print("=" * 60)
    print(f"\n分析文本:\n{text}\n")
    
    # 分析文本
    result = detector.analyze(text)
    
    # 输出结果
    print("逻辑链条:")
    for i, premise in enumerate(result.premises, 1):
        print(f"  前提{i}: {premise.text}")
        print(f"    真实性：{premise.truth_level.value}")
        print(f"    来源：{premise.source}")
        print(f"    权重：{premise.weight}")
        print()
    
    print("检测到的逻辑谬误:")
    if result.fallacies:
        for fallacy in result.fallacies:
            print(f"  - {fallacy.fallacy_type.value}")
            print(f"    描述：{fallacy.description}")
            print(f"    风险等级：{fallacy.risk_level}")
            print()
    else:
        print("  未检测到明显逻辑谬误")
        print()
    
    print(f"推理强度：{'⭐' * result.reasoning_strength} ({result.reasoning_strength}/5)")
    print(f"结论可靠性：{result.conclusion_reliability}")
    print(f"\n摘要：{result.summary}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
