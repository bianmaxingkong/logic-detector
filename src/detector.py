"""
LogicDetector 核心检测器

多模块融合架构，集成四大检测模块
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    from .modules.logic_validator import LogicValidator, FallacyType
    from .modules.chain_checker import ChainChecker
    from .modules.consistency_verifier import ConsistencyVerifier
    from .modules.fact_checker import FactChecker
except ImportError:
    from modules.logic_validator import LogicValidator, FallacyType
    from modules.chain_checker import ChainChecker
    from modules.consistency_verifier import ConsistencyVerifier
    from modules.fact_checker import FactChecker


@dataclass
class DetectionResult:
    """检测结果"""
    is_hallucination: bool  # 是否幻觉
    confidence: float  # 置信度
    logic_fallacies: List[str]  # 逻辑谬误列表
    completeness_score: float  # 推理完整性得分
    is_consistent: bool  # 是否自洽
    factual_errors: List[str]  # 事实错误列表
    explanation: str  # 解释说明


class LogicDetector:
    """
    LogicDetector: 多模块融合的逻辑推理幻觉检测器
    
    集成四大模块:
    1. 逻辑规则验证器 (权重：0.4)
    2. 推理链完整性检查器 (权重：0.3)
    3. 自洽性验证器 (权重：0.2)
    4. 事实检查器 (权重：0.1)
    """
    
    def __init__(self, threshold: float = 0.35):
        """
        初始化检测器
        
        Args:
            threshold: 幻觉判定阈值 (默认 0.35，优化后)
        """
        self.threshold = threshold
        
        # 初始化四大模块
        self.logic_validator = LogicValidator()
        self.chain_checker = ChainChecker()
        self.consistency_verifier = ConsistencyVerifier(n_samples=5)
        self.fact_checker = FactChecker()
        
        # 模块权重 (基于消融实验)
        self.weights = {
            "logic": 0.4,      # 模块 1 贡献：+7.4%
            "chain": 0.3,      # 模块 2 贡献：+4.3%
            "consistency": 0.2, # 模块 3 贡献：+2.7%
            "fact": 0.1,       # 模块 4 贡献：+3.7%
        }
    
    def analyze(self, text: str, reasoning_type: str = "deductive") -> DetectionResult:
        """
        分析文本是否存在幻觉
        
        Args:
            text: 待检测的文本
            reasoning_type: 推理类型 (deductive/inductive/causal/analogical)
            
        Returns:
            DetectionResult: 检测结果
        """
        # 模块 1: 逻辑规则验证
        fallacies = self.logic_validator.validate(text)
        has_fallacy = len(fallacies) > 0
        logic_score = 0.0 if has_fallacy else 1.0  # 有谬误直接 0 分
        
        # 模块 2: 推理链完整性检查 (主模块，基于消融实验权重最高)
        chain_analysis = self.chain_checker.check_completeness(text, reasoning_type)
        chain_score = chain_analysis.completeness_score
        
        # 模块 3: 自洽性验证 (需要语言模型)
        # TODO: 传入语言模型
        consistency_score = 1.0  # 默认自洽
        
        # 模块 4: 事实检查
        factual_errors = self.fact_checker.get_factual_errors(text)
        has_factual_error = len(factual_errors) > 0
        fact_score = 0.0 if has_factual_error else 1.0  # 有错误直接 0 分
        
        # 多模块融合 (优化策略：模块 2 主导 + 其他模块 veto 权)
        # 基于消融实验：模块 2 单独 75.5%，其他模块约 57%
        # 策略：以模块 2 为主，其他模块只负责检出明确错误
        
        # 如果模块 2 判定不完整 (得分<0.5)，直接判定为幻觉
        if chain_score < 0.5:
            is_hallucination = True
            overall_score = chain_score
        # 否则，使用加权平均，但模块 2 权重更高
        else:
            overall_score = (
                self.weights["logic"] * logic_score +
                self.weights["chain"] * chain_score +
                self.weights["consistency"] * consistency_score +
                self.weights["fact"] * fact_score
            )
            is_hallucination = (overall_score < self.threshold)
        
        # 一票否决：有明确谬误或事实错误，直接判定为幻觉
        if has_fallacy or has_factual_error:
            is_hallucination = True
        
        # 生成解释
        explanation = self._generate_explanation(
            fallacies, chain_analysis, factual_errors, overall_score
        )
        
        return DetectionResult(
            is_hallucination=is_hallucination,
            confidence=1.0 - overall_score,
            logic_fallacies=[f.fallacy_type.value for f in fallacies],
            completeness_score=chain_score,
            is_consistent=consistency_score > 0.5,
            factual_errors=[e.claim for e in factual_errors],
            explanation=explanation
        )
    
    def _generate_explanation(self, fallacies, chain_analysis, factual_errors, score: float) -> str:
        """生成检测解释"""
        explanations = []
        
        if fallacies:
            for fallacy in fallacies:
                explanations.append(
                    f"检测到逻辑谬误：{fallacy.fallacy_type.value} - {fallacy.explanation}"
                )
        
        if chain_analysis.missing_steps:
            explanations.append(
                f"推理链不完整，缺失步骤：{', '.join(chain_analysis.missing_steps)}"
            )
        
        if factual_errors:
            for error in factual_errors:
                explanations.append(f"事实错误：{error.claim}")
        
        if not explanations:
            explanations.append("未检测到明显的逻辑谬误或事实错误")
        
        explanations.append(f"总体评分：{score:.2f} (阈值：{self.threshold})")
        
        return "\n".join(explanations)
    
    def batch_analyze(self, texts: List[str]) -> List[DetectionResult]:
        """批量分析多个文本"""
        return [self.analyze(text) for text in texts]
    
    def get_module_weights(self) -> Dict[str, float]:
        """获取模块权重"""
        return self.weights.copy()
    
    def set_module_weights(self, weights: Dict[str, float]):
        """设置模块权重"""
        # 验证权重和为 1
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"权重和必须为 1.0，当前为{total}")
        self.weights = weights
    
    def explain_fallacy(self, fallacy_type: str) -> str:
        """解释特定谬误类型"""
        try:
            fallacy = FallacyType(fallacy_type)
            return self.logic_validator.explain_fallacy(fallacy)
        except ValueError:
            return f"未知的谬误类型：{fallacy_type}"
