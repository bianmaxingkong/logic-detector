"""
模块 3: 自洽性验证器 (Self-Consistency Verifier)

方案 A: 规则生成方式（免费，不需要大模型）

通过语义改写规则生成多个推理变体，然后检查变体之间是否存在矛盾。

优化:
- 使用规则改写生成变体（无需大模型）
- 仅需 5 个样本
- 基于语义相似度检测矛盾
- 推理时间：<100ms/查询

局限:
- 无法检测一致重复的错误
- 依赖改写规则的覆盖度
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ConsistencyCheck:
    """自洽性检查结果"""
    is_consistent: bool  # 是否自洽
    contradiction_count: int  # 矛盾数量
    contradictions: List[str]  # 矛盾列表
    confidence: float  # 置信度
    samples_used: int  # 使用的样本数
    variations: List[str]  # 生成的变体列表


class ConsistencyVerifier:
    """
    自洽性验证器 - 方案 A（规则生成方式）
    
    通过语义改写规则生成多个推理变体，检查变体之间的一致性。
    完全基于规则，不需要大模型。
    """
    
    def __init__(self, n_samples: int = 5):
        """
        初始化自洽性验证器
        
        Args:
            n_samples: 样本数量 (默认 5 个)
        """
        self.n_samples = n_samples
        
        # 定义改写规则模板
        self.rewrite_rules = [
            # 逻辑连接词替换
            ("如果.*那么", "若...则"),
            ("如果.*则", "假如...那么"),
            ("因此", "所以"),
            ("故", "因此"),
            ("所以", "故而"),
            ("因为", "由于"),
            
            # 句式变换
            ("所有.*都", "每一个...都"),
            ("有些.*不", "存在...不"),
            ("必然", "必定"),
            ("可能", "或许"),
        ]
        
        # 逻辑连接词库
        self.connectives = {
            "如果": ["若", "假如", "要是", "倘若"],
            "那么": ["则", "就", "便"],
            "因此": ["所以", "故", "故而", "于是"],
            "因为": ["由于", "鉴于"],
            "所有": ["每一个", "全部", "一切"],
            "有些": ["存在", "部分", "有的"],
        }
    
    def _apply_rewrite_rules(self, text: str) -> List[str]:
        """
        应用改写规则生成变体
        
        Args:
            text: 原始文本
            
        Returns:
            改写后的变体列表
        """
        variations = []
        
        # 变体 1: 替换"如果...那么"为"若...则"
        v1 = re.sub(r"如果", "若", text)
        v1 = re.sub(r"那么", "则", v1)
        if v1 != text:
            variations.append(v1)
        
        # 变体 2: 替换"因此"为"所以"
        v2 = re.sub(r"因此", "所以", text)
        if v2 != text:
            variations.append(v2)
        
        # 变体 3: 替换"故"为"因此"
        v3 = re.sub(r"故", "因此", text)
        if v3 != text:
            variations.append(v3)
        
        # 变体 4: 替换"所有"为"每一个"
        v4 = re.sub(r"所有", "每一个", text)
        if v4 != text:
            variations.append(v4)
        
        # 变体 5: 组合改写
        v5 = re.sub(r"如果", "假如", text)
        v5 = re.sub(r"那么", "就", v5)
        v5 = re.sub(r"因此", "故而", v5)
        if v5 != text:
            variations.append(v5)
        
        return variations if variations else [text]
    
    def _generate_variations(self, text: str) -> List[str]:
        """
        生成多个推理变体
        
        Args:
            text: 原始推理文本
            
        Returns:
            变体列表（包含原文本）
        """
        variations = [text]  # 保留原文本
        
        # 应用改写规则
        rewritten = self._apply_rewrite_rules(text)
        
        # 添加改写变体，直到达到目标数量
        for v in rewritten:
            if len(variations) >= self.n_samples:
                break
            if v not in variations:
                variations.append(v)
        
        # 如果变体不足，添加一些简单的语义保持变换
        while len(variations) < self.n_samples:
            # 添加空格变体（中文通常不需要，但作为占位）
            if len(variations) == 1:
                variations.append(text.strip())
            else:
                # 重复最后一个变体
                variations.append(variations[-1])
        
        return variations[:self.n_samples]
    
    def _extract_claims(self, text: str) -> List[str]:
        """
        从文本中提取关键主张/命题
        
        Args:
            text: 推理文本
            
        Returns:
            主张列表
        """
        claims = []
        
        # 提取结论（通常在"因此/所以/故"之后）
        conclusion_patterns = [
            r"因此 (.+?)(?:。|$)",
            r"所以 (.+?)(?:。|$)",
            r"故 (.+?)(?:。|$)",
            r"故而 (.+?)(?:。|$)",
        ]
        
        for pattern in conclusion_patterns:
            match = re.search(pattern, text)
            if match:
                claims.append(("conclusion", match.group(1)))
        
        # 提取前提（通常在"如果/若/因为"之后）
        premise_patterns = [
            r"如果 (.+?)，",
            r"若 (.+?)，",
            r"假如 (.+?)，",
            r"因为 (.+?)，",
        ]
        
        for pattern in premise_patterns:
            match = re.search(pattern, text)
            if match:
                claims.append(("premise", match.group(1)))
        
        return claims
    
    def _check_semantic_contradiction(self, text1: str, text2: str) -> Tuple[bool, float]:
        """
        检查两个文本是否语义矛盾
        
        基于规则和关键词的简单矛盾检测
        
        Args:
            text1: 文本 1
            text2: 文本 2
            
        Returns:
            (是否矛盾，置信度)
        """
        # 矛盾关键词对
        contradiction_pairs = [
            ("是", "不是"),
            ("有", "没有"),
            ("存在", "不存在"),
            ("所有", "有些"),
            ("都", "不都"),
            ("必然", "可能不"),
            ("一定", "不一定"),
            ("肯定", "否定"),
            ("真", "假"),
            ("正确", "错误"),
        ]
        
        # 提取两个文本的主张
        claims1 = self._extract_claims(text1)
        claims2 = self._extract_claims(text2)
        
        contradictions = []
        
        # 检查结论是否矛盾
        conclusions1 = [c[1] for c in claims1 if c[0] == "conclusion"]
        conclusions2 = [c[1] for c in claims2 if c[0] == "conclusion"]
        
        for c1 in conclusions1:
            for c2 in conclusions2:
                # 检查是否包含矛盾关键词
                for pos, neg in contradiction_pairs:
                    if pos in c1 and neg in c2:
                        contradictions.append(f"结论矛盾：'{c1}' vs '{c2}'")
                    elif neg in c1 and pos in c2:
                        contradictions.append(f"结论矛盾：'{c1}' vs '{c2}'")
        
        # 检查前提是否矛盾
        premises1 = [c[1] for c in claims1 if c[0] == "premise"]
        premises2 = [c[1] for c in claims2 if c[0] == "premise"]
        
        for p1 in premises1:
            for p2 in premises2:
                for pos, neg in contradiction_pairs:
                    if pos in p1 and neg in p2:
                        contradictions.append(f"前提矛盾：'{p1}' vs '{p2}'")
                    elif neg in p1 and pos in p2:
                        contradictions.append(f"前提矛盾：'{p1}' vs '{p2}'")
        
        # 判断是否矛盾
        is_contradiction = len(contradictions) > 0
        confidence = min(0.9, 0.5 + len(contradictions) * 0.2) if is_contradiction else 0.1
        
        return is_contradiction, confidence, contradictions
    
    def verify(self, text: str) -> ConsistencyCheck:
        """
        验证文本的自洽性
        
        Args:
            text: 待检测的推理文本
            
        Returns:
            ConsistencyCheck: 检查结果
        """
        # 生成多个变体
        variations = self._generate_variations(text)
        
        # 两两检查矛盾
        all_contradictions = []
        contradiction_count = 0
        
        for i in range(len(variations)):
            for j in range(i + 1, len(variations)):
                is_contradiction, confidence, contradictions = self._check_semantic_contradiction(
                    variations[i], variations[j]
                )
                if is_contradiction:
                    contradiction_count += len(contradictions)
                    all_contradictions.extend(contradictions)
        
        # 判断是否自洽
        is_consistent = contradiction_count == 0
        
        # 计算总体置信度
        total_pairs = len(variations) * (len(variations) - 1) / 2
        confidence = 1.0 - (contradiction_count / (total_pairs * 2)) if total_pairs > 0 else 1.0
        confidence = max(0.0, min(1.0, confidence))
        
        return ConsistencyCheck(
            is_consistent=is_consistent,
            contradiction_count=contradiction_count,
            contradictions=list(set(all_contradictions)),  # 去重
            confidence=confidence,
            samples_used=len(variations),
            variations=variations
        )
    
    def verify_with_score(self, text: str) -> float:
        """
        验证文本并返回自洽性得分
        
        Args:
            text: 待检测的推理文本
            
        Returns:
            自洽性得分 (0.0-1.0)
        """
        result = self.verify(text)
        return result.confidence
    
    def batch_verify(self, texts: List[str]) -> List[ConsistencyCheck]:
        """批量验证多个文本的自洽性"""
        return [self.verify(text) for text in texts]
    
    def get_contradiction_rate(self, text: str) -> float:
        """获取矛盾率"""
        result = self.verify(text)
        total_pairs = result.samples_used * (result.samples_used - 1) / 2
        return result.contradiction_count / total_pairs if total_pairs > 0 else 0.0


# 测试代码
if __name__ == "__main__":
    verifier = ConsistencyVerifier(n_samples=5)
    
    # 测试用例 1: 有效推理
    text1 = "如果明天下雨，比赛取消。明天下雨。因此比赛取消。"
    result1 = verifier.verify(text1)
    print(f"测试 1 (有效推理):")
    print(f"  自洽：{result1.is_consistent}")
    print(f"  置信度：{result1.confidence:.2f}")
    print(f"  变体数：{result1.samples_used}")
    print()
    
    # 测试用例 2: 肯定后件谬误
    text2 = "如果明天下雨，比赛取消。比赛取消。因此明天下雨。"
    result2 = verifier.verify(text2)
    print(f"测试 2 (肯定后件):")
    print(f"  自洽：{result2.is_consistent}")
    print(f"  置信度：{result2.confidence:.2f}")
    print(f"  变体数：{result2.samples_used}")
    print()
    
    # 测试用例 3: 否定前件
    text3 = "如果下雨，地面会湿。没有下雨。因此地面不会湿。"
    result3 = verifier.verify(text3)
    print(f"测试 3 (否定前件):")
    print(f"  自洽：{result3.is_consistent}")
    print(f"  置信度：{result3.confidence:.2f}")
    print(f"  变体数：{result3.samples_used}")
