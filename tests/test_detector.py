"""
LogicDetector 单元测试
"""

import unittest
from src.detector import LogicDetector, TruthLevel, FallacyType, Premise, Fallacy


class TestLogicDetector(unittest.TestCase):
    """测试逻辑检测器"""
    
    def setUp(self):
        """测试前准备"""
        self.detector = LogicDetector()
    
    def test_detector_initialization(self):
        """测试检测器初始化"""
        detector = LogicDetector(threshold=0.8)
        self.assertEqual(detector.threshold, 0.8)
    
    def test_premise_extraction(self):
        """测试前提提取"""
        text = "前提 1: A 是真的。前提 2: B 是真的。因此 C 是真的。"
        result = self.detector.analyze(text)
        # TODO: 实现断言
        self.assertIsInstance(result.premises, list)
    
    def test_fallacy_detection_slippery_slope(self):
        """测试滑坡谬误检测"""
        text = "如果我们允许 A，那么 B 就会发生，然后 C 就会发生，最终导致灾难。"
        result = self.detector.analyze(text)
        # TODO: 实现断言
        self.assertIsInstance(result.fallacies, list)
    
    def test_reasoning_strength_evaluation(self):
        """测试推理强度评估"""
        # 强推理示例
        strong_text = "所有人类都会死。苏格拉底是人类。因此苏格拉底会死。"
        result = self.detector.analyze(strong_text)
        self.assertGreaterEqual(result.reasoning_strength, 4)
    
    def test_reliability_classification(self):
        """测试可靠性分类"""
        self.assertEqual(self.detector._get_reliability(5), "高")
        self.assertEqual(self.detector._get_reliability(3), "中")
        self.assertEqual(self.detector._get_reliability(1), "低")


class TestPremise(unittest.TestCase):
    """测试前提类"""
    
    def test_premise_creation(self):
        """测试前提创建"""
        premise = Premise(
            text="测试前提",
            truth_level=TruthLevel.TRUE,
            source="测试来源",
            weight=0.5
        )
        self.assertEqual(premise.text, "测试前提")
        self.assertEqual(premise.truth_level, TruthLevel.TRUE)


class TestFallacy(unittest.TestCase):
    """测试谬误类"""
    
    def test_fallacy_creation(self):
        """测试谬误创建"""
        fallacy = Fallacy(
            fallacy_type=FallacyType.SLIPPERY_SLOPE,
            description="测试描述",
            risk_level="中",
            evidence="测试证据"
        )
        self.assertEqual(fallacy.fallacy_type, FallacyType.SLIPPERY_SLOPE)
        self.assertEqual(fallacy.risk_level, "中")


if __name__ == "__main__":
    unittest.main()
