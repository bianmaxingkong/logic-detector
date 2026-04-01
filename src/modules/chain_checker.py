"""
模块 2: 推理链完整性检查器 (Reasoning Chain Completeness Checker)

分析推理步骤是否完整，检测推理跳跃和缺失前提

技术:
- 轻量级句向量 (sentence embeddings)
- 与标准推理模板对比
- 计算成本：<10ms/查询

优势:
- 低计算成本
- 检测结构性不完整
- 补充形式逻辑方法
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ChainAnalysis:
    """推理链分析结果"""
    completeness_score: float  # 完整性得分 (0-1)
    missing_steps: List[str]  # 缺失的推理步骤
    reasoning_jumps: List[str]  # 推理跳跃点
    standard_template: str  # 标准推理模板
    matched_steps: List[str]  # 匹配的步骤


class ChainChecker:
    """推理链完整性检查器"""
    
    def __init__(self):
        # 加载标准推理模板
        self.templates = self._load_reasoning_templates()
        # 加载轻量级句向量模型 (使用预训练模型)
        self.embedding_model = self._load_embedding_model()
    
    def _load_reasoning_templates(self) -> Dict[str, List[str]]:
        """加载标准推理模板"""
        return {
            "deductive": [
                "前提 1: 所有 A 都是 B",
                "前提 2: C 是 A",
                "结论：C 是 B",
            ],
            "inductive": [
                "观察 1: A1 具有性质 P",
                "观察 2: A2 具有性质 P",
                "...",
                "观察 N: AN 具有性质 P",
                "结论：所有 A 都具有性质 P",
            ],
            "causal": [
                "原因：A 发生",
                "机制：A 导致 B 的机制",
                "证据：A 和 B 的相关性/实验证据",
                "结论：A 导致 B",
            ],
            "analogical": [
                "A 具有性质 P1, P2, P3...",
                "B 具有性质 P1, P2, P3...",
                "A 具有性质 Q",
                "结论：B 也具有性质 Q",
            ],
        }
    
    def _load_embedding_model(self):
        """加载轻量级句向量模型"""
        # TODO: 加载 DistilBERT 或其他轻量级模型
        # 目前使用占位实现
        return None
    
    def _compute_embedding(self, text: str) -> np.ndarray:
        """计算文本向量"""
        # TODO: 实现真正的句向量计算
        # 目前使用随机向量作为占位
        return np.random.rand(768)
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)
    
    def check_completeness(self, reasoning_chain: str, reasoning_type: str = "deductive") -> ChainAnalysis:
        """
        检查推理链的完整性
        
        Args:
            reasoning_chain: 推理链文本
            reasoning_type: 推理类型 (deductive/inductive/causal/analogical)
            
        Returns:
            ChainAnalysis: 分析结果
        """
        # 获取标准模板
        template = self.templates.get(reasoning_type, self.templates["deductive"])
        
        # 分割推理步骤
        steps = self._split_reasoning_steps(reasoning_chain)
        
        # 匹配步骤
        matched_steps = []
        missing_steps = []
        
        for i, template_step in enumerate(template):
            if i < len(steps):
                # 计算相似度
                step_vec = self._compute_embedding(steps[i])
                template_vec = self._compute_embedding(template_step)
                similarity = self._cosine_similarity(step_vec, template_vec)
                
                if similarity > 0.6:  # 相似度阈值
                    matched_steps.append(steps[i])
                else:
                    missing_steps.append(template_step)
            else:
                missing_steps.append(template_step)
        
        # 检测推理跳跃
        reasoning_jumps = self._detect_jumps(steps)
        
        # 计算完整性得分
        completeness_score = len(matched_steps) / len(template) if template else 0.0
        
        return ChainAnalysis(
            completeness_score=completeness_score,
            missing_steps=missing_steps,
            reasoning_jumps=reasoning_jumps,
            standard_template="\n".join(template),
            matched_steps=matched_steps
        )
    
    def _split_reasoning_steps(self, text: str) -> List[str]:
        """分割推理步骤"""
        # 按句号、分号等分割
        steps = re.split(r'[。；.；]', text)
        return [step.strip() for step in steps if step.strip()]
    
    def _detect_jumps(self, steps: List[str]) -> List[str]:
        """检测推理跳跃"""
        jumps = []
        
        # TODO: 实现推理跳跃检测逻辑
        # 检查步骤之间的逻辑连贯性
        
        return jumps
    
    def has_missing_steps(self, reasoning_chain: str) -> bool:
        """检查是否有缺失的推理步骤"""
        analysis = self.check_completeness(reasoning_chain)
        return len(analysis.missing_steps) > 0
    
    def get_completeness_score(self, reasoning_chain: str) -> float:
        """获取推理链完整性得分"""
        analysis = self.check_completeness(reasoning_chain)
        return analysis.completeness_score


# 导入 re 模块
import re
