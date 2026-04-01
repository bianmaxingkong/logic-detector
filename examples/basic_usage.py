"""
LogicDetector 基础使用示例

演示如何使用 LogicDetector 检测逻辑推理中的幻觉
"""

import sys
sys.path.insert(0, "/home/baibai/.openclaw/workspace/logic-detector/src")

from detector import LogicDetector


def main():
    # 创建检测器
    detector = LogicDetector(threshold=0.5)
    
    print("=" * 60)
    print("LogicDetector 基础使用示例")
    print("=" * 60)
    print()
    
    # 示例 1: 肯定后件谬误
    text1 = "如果下雨，地面会湿。现在地面湿了，所以下雨了。"
    print(f"示例 1: {text1}")
    result1 = detector.analyze(text1)
    print(f"是否幻觉：{result1.is_hallucination}")
    print(f"置信度：{result1.confidence:.2f}")
    print(f"逻辑谬误：{result1.logic_fallacies}")
    print(f"解释：{result1.explanation}")
    print()
    
    # 示例 2: 否定前件谬误
    text2 = "如果是科学家，就很聪明。这个人不是科学家，所以他不聪明。"
    print(f"示例 2: {text2}")
    result2 = detector.analyze(text2)
    print(f"是否幻觉：{result2.is_hallucination}")
    print(f"置信度：{result2.confidence:.2f}")
    print(f"逻辑谬误：{result2.logic_fallacies}")
    print(f"解释：{result2.explanation}")
    print()
    
    # 示例 3: 轻率概括
    text3 = "我认识一个程序员，他很宅。所以所有程序员都很宅。"
    print(f"示例 3: {text3}")
    result3 = detector.analyze(text3)
    print(f"是否幻觉：{result3.is_hallucination}")
    print(f"置信度：{result3.confidence:.2f}")
    print(f"逻辑谬误：{result3.logic_fallacies}")
    print(f"解释：{result3.explanation}")
    print()
    
    # 示例 4: 正确的推理
    text4 = "所有人都会死。苏格拉底是人。因此苏格拉底会死。"
    print(f"示例 4: {text4}")
    result4 = detector.analyze(text4)
    print(f"是否幻觉：{result4.is_hallucination}")
    print(f"置信度：{result4.confidence:.2f}")
    print(f"逻辑谬误：{result4.logic_fallacies}")
    print(f"解释：{result4.explanation}")
    print()
    
    # 示例 5: 事实错误
    text5 = "美国的首都是纽约。地球是平的。"
    print(f"示例 5: {text5}")
    result5 = detector.analyze(text5)
    print(f"是否幻觉：{result5.is_hallucination}")
    print(f"置信度：{result5.confidence:.2f}")
    print(f"事实错误：{result5.factual_errors}")
    print(f"解释：{result5.explanation}")
    print()
    
    print("=" * 60)
    print("示例运行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
