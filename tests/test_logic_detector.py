"""
LogicDetector 单元测试
"""

import unittest
import sys
sys.path.insert(0, "/home/baibai/.openclaw/workspace/logic-detector/src")

from detector import LogicDetector
from modules.logic_validator import LogicValidator, FallacyType
from modules.chain_checker import ChainChecker
from modules.fact_checker import FactChecker


class TestLogicDetector(unittest.TestCase):
    """测试 LogicDetector 主类"""
    
    def setUp(self):
        """测试前准备"""
        self.detector = LogicDetector()
    
    def test_detector_initialization(self):
        """测试检测器初始化"""
        detector = LogicDetector(threshold=0.6)
        self.assertEqual(detector.threshold, 0.6)
    
    def test_detect_affirming_consequent(self):
        """测试肯定后件谬误检测"""
        text = "如果下雨，地面会湿。地面湿了，所以下雨了。"
        result = self.detector.analyze(text)
        self.assertTrue(result.is_hallucination)
        self.assertIn("肯定后件谬误", result.logic_fallacies)
    
    def test_detect_denying_antecedent(self):
        """测试否定前件谬误检测"""
        text = "如果是科学家，就很聪明。这个人不是科学家，所以他不聪明。"
        result = self.detector.analyze(text)
        self.assertTrue(result.is_hallucination)
        self.assertIn("否定前件谬误", result.logic_fallacies)
    
    def test_valid_reasoning(self):
        """测试正确推理"""
        text = "所有人都会死。苏格拉底是人。因此苏格拉底会死。"
        result = self.detector.analyze(text)
        self.assertFalse(result.is_hallucination)
        self.assertEqual(len(result.logic_fallacies), 0)
    
    def test_batch_analyze(self):
        """测试批量分析"""
        texts = [
            "如果下雨，地面会湿。地面湿了，所以下雨了。",
            "所有人都会死。苏格拉底是人。因此苏格拉底会死。",
        ]
        results = self.detector.batch_analyze(texts)
        self.assertEqual(len(results), 2)
    
    def test_module_weights(self):
        """测试模块权重"""
        weights = self.detector.get_module_weights()
        self.assertAlmostEqual(sum(weights.values()), 1.0)
        
        # 修改权重
        new_weights = {"logic": 0.5, "chain": 0.3, "consistency": 0.1, "fact": 0.1}
        self.detector.set_module_weights(new_weights)
        self.assertEqual(self.detector.get_module_weights(), new_weights)


class TestLogicValidator(unittest.TestCase):
    """测试逻辑规则验证器"""
    
    def setUp(self):
        """测试前准备"""
        self.validator = LogicValidator()
    
    def test_fallacy_types(self):
        """测试支持的谬误类型"""
        fallacy_types = self.validator.get_fallacy_types()
        self.assertEqual(len(fallacy_types), 6)
    
    def test_explain_fallacy(self):
        """测试谬误解释"""
        explanation = self.validator.explain_fallacy(FallacyType.AFFIRMING_CONSEQUENT)
        self.assertIn("肯定后件", explanation)


class TestChainChecker(unittest.TestCase):
    """测试推理链完整性检查器"""
    
    def setUp(self):
        """测试前准备"""
        self.checker = ChainChecker()
    
    def test_completeness_score(self):
        """测试完整性得分"""
        text = "前提 1: 所有 A 都是 B。前提 2: C 是 A。结论：C 是 B。"
        analysis = self.checker.check_completeness(text, "deductive")
        self.assertGreater(analysis.completeness_score, 0.5)


class TestFactChecker(unittest.TestCase):
    """测试事实检查器"""
    
    def setUp(self):
        """测试前准备"""
        self.checker = FactChecker()
    
    def test_factual_error_detection(self):
        """测试事实错误检测"""
        text = "美国的首都是纽约。"
        errors = self.checker.get_factual_errors(text)
        self.assertGreater(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
