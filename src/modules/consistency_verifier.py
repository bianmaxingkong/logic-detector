"""
模块 3: 自洽性验证器 (Self-Consistency Verifier)

通过多策略改写生成语义多样的推理变体，再使用句向量嵌入
检测变体之间的语义分歧。如果不同表达方式之间存在矛盾
或较大的语义距离，则表明推理可能存在自洽性问题。

设计:
- 多样性改写策略: 语序变换，结构重组，连接词替换
- 语义比较: 使用 bge-small-zh-v1.5 嵌入并计算配对余弦相似度
- 矛盾检测: 相似度矩阵 + 原子主张否定对检测
- 推理时间: <150ms/查询
- 内存: 复用已有句向量模型（不额外加载）
"""

import re
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer


@dataclass
class ConsistencyCheck:
    """自洽性检查结果"""
    is_consistent: bool          # 是否自洽
    contradiction_count: int     # 矛盾数量
    contradictions: List[str]    # 矛盾描述列表
    confidence: float            # 自洽置信度 (0-1)
    variation_diversity: float   # 变体多样性得分 (0-1)
    samples_used: int            # 变体数量
    variations: List[str]        # 所有变体


class ConsistencyVerifier:
    """
    自洽性验证器 - 方案 B（句向量 + 多策略改写）
    
    通过多种改写策略生成推理变体，使用句向量嵌入
    检测变体间的语义分歧，判断推理是否自洽。
    """

    def __init__(self, n_samples: int = 5, model_name: str = "BAAI/bge-small-zh-v1.5", threshold: float = 0.35):
        """
        初始化自洽性验证器

        Args:
            n_samples: 变体数量 (默认 5)
            model_name: 句向量模型名 (默认 bge-small-zh-v1.5)
            threshold: 自洽判定阈值 (默认 0.35)
        """
        self.n_samples = n_samples
        self.threshold = threshold

        # 加载句向量模型（复用 M2 同样的轻量模型）
        self.embedder = SentenceTransformer(model_name)

        # 矛盾关键词对（扩展版）
        self.contradiction_pairs: List[Tuple[str, str]] = [
            ("是", "不是"), ("是", "并非"),
            ("有", "没有"), ("存在", "不存在"),
            ("所有", "有些"), ("全部", "部分"),
            ("都", "不都"), ("都会", "都不会"),
            ("必然", "不可能"), ("一定", "不一定"),
            ("肯定", "否定"), ("正确", "错误"),
            ("真", "假"), ("真实", "虚假"),
            ("必须", "不必"), ("需要", "不需要"),
            ("同意", "反对"), ("支持", "反对"),
            ("增加", "减少"), ("上升", "下降"),
            ("包含", "不包含"), ("属于", "不属于"),
            ("可以", "不可以"), ("能", "不能"),
            ("会", "不会"), ("可能", "不可能"),
            ("要", "不要"), ("应该", "不应该"),
        ]

        # 模态强度等级（从强到弱）
        self.modal_strength = {
            "必然": 1.0, "必定": 1.0, "一定": 0.9, "肯定": 0.9,
            "很可能": 0.7, "大概": 0.6, "可能": 0.5, "也许": 0.4,
            "未必": 0.3, "不一定": 0.2, "不可能": 0.0,
        }

    # ─── 多样性变体生成 ─────────────────────────────────

    def _rewrite_reorder(self, text: str) -> List[str]:
        """策略 1: 语序变换"""
        variants = []

        # 如果A，那么B。A。所以B。 → 交换结论和前提
        m = re.search(r"如果(.+?)[，,].+?[。，].+?所以(.+?)[。，]", text)
        if m:
            cause, effect = m.group(1), m.group(2)
            variants.append(f"由于{cause}，所以{effect}。")
            variants.append(f"因为{cause}，所以{effect}。")

        # A。因此B。 → B。因为A。
        m = re.search(r"(.+?)。因此(.+?)。", text)
        if m:
            premise, conclusion = m.group(1), m.group(2)
            variants.append(f"{conclusion}。因为{premise}。")
            variants.append(f"{conclusion}，这是由于{premise}。")

        # 因为A，所以B → B是因为A
        m = re.search(r"因为(.+?)，所以(.+?)。", text)
        if m:
            cause, effect = m.group(1), m.group(2)
            variants.append(f"{effect}，是因为{cause}。")
            variants.append(f"{cause}导致了{effect}。")

        return variants

    def _rewrite_restructure(self, text: str) -> List[str]:
        """策略 2: 结构重组（拆句/合句/换连接）"""
        variants = []

        # 如果A，那么B。A。所以B。 → 去掉"如果...那么"，直接三段式
        syllogism = re.search(
            r"如果(.+?)，(那么|则|就)(.+?)[。，](.+?)[。，](所以|因此|故)(.+?)。",
            text
        )
        if syllogism:
            cond, _, conseq, premise, _, concl = (
                syllogism.group(1), syllogism.group(2),
                syllogism.group(3), syllogism.group(4),
                syllogism.group(5), syllogism.group(6),
            )
            variants.append(f"假设{cond}，则{conseq}。事实是{premise}。故{concl}。")
            variants.append(f"已知{cond}→{conseq}，且{premise}，因此{concl}。")

        # 多句推理 → 合并为一段
        sentences = re.split(r"[。！？；\n]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if len(sentences) >= 3:
            # 合并：A；B；因此C
            merged = "；".join(sentences[:-1]) + f"。{sentences[-1]}。"
            if merged != text:
                variants.append(merged)
            # 连词版：先A，然后B，所以C
            chain = "，然后".join(sentences[:-1]) + f"，所以{sentences[-1]}。"
            variants.append(chain)

        return variants

    def _rewrite_modal(self, text: str) -> List[str]:
        """策略 3: 模态词微调"""
        variants = []

        # 换同级别模态词：必然↔必定、可能↔也许
        swaps = [
            ("必然", "必定"), ("可能", "也许"), ("大概", "或许"),
            ("因此", "所以"), ("故", "因此"), ("因为", "由于"),
        ]
        for old, new in swaps:
            if old in text:
                variants.append(text.replace(old, new, 1))

        # 如果文本用了强模态（必然/一定/肯定），生成弱模态版本
        for strong in ["必然", "一定", "肯定"]:
            if strong in text:
                weak_v = text.replace(strong, "可能", 1)
                if weak_v != text:
                    variants.append(weak_v)
                break

        return variants

    def _rewrite_negate(self, text: str) -> List[str]:
        """策略 4: 选择性子句否定（生成对立观点变体）"""
        variants = []

        # 提取结论句（所以/因此/故后的句子）
        conclusion_m = re.search(r"(所以|因此|故|故而|于是)(.+?)。", text)
        if conclusion_m:
            prefix = conclusion_m.group(0)
            conclusion = conclusion_m.group(2).strip()

            # 对结论做否定变换
            negated = self._negate_clause(conclusion)
            if negated and negated != conclusion:
                neg_v = text.replace(prefix, f"因此{negated}。")
                variants.append(neg_v)

            # 加条件限定："所以B" → "所以B可能不成立"
            variants.append(
                text.replace(prefix, f"因此{conclusion}，但这一结论可能不成立。")
            )

            # "所以B" → "所以是否B成立仍需验证"
            variants.append(
                text.replace(prefix, f"因此{conclusion}，但这需要进一步验证。")
            )

        return variants

    @staticmethod
    def _negate_clause(clause: str) -> Optional[str]:
        """对单个子句做语义否定"""
        # 是/不是互转
        if re.search(r"^(.*?)是(.+?)$", clause):
            if "不是" in clause:
                return clause.replace("不是", "是", 1)
            else:
                return clause.replace("是", "不是", 1)
        # 有/没有
        if re.search(r"^(.*?)有(.+?)$", clause):
            if "没有" in clause or "没" in clause:
                return clause  # 复杂情况不做
            else:
                return f"不{clause}" if not clause.startswith("不") else clause[1:]
        # 都不会/都会
        if "都不会" in clause:
            return clause.replace("都不会", "都会")
        if "都" in clause:
            return clause.replace("都", "不都")
        # 默认加"不"
        if not clause.startswith("不") and not clause.startswith("没有"):
            return "不" + clause
        return None

    def _generate_variations(self, text: str) -> List[str]:
        """综合所有改写策略，生成最多 n_samples 个变体"""
        all_variants = [text]  # 保留原文

        # 依次应用各种策略
        for strategy in [
            self._rewrite_reorder,
            self._rewrite_restructure,
            self._rewrite_modal,
            self._rewrite_negate,
        ]:
            new_variants = strategy(text)
            for v in new_variants:
                if v not in all_variants and len(all_variants) < self.n_samples:
                    all_variants.append(v)

        # 如果还不够 n_samples，截断或垫原文
        while len(all_variants) < self.n_samples:
            all_variants.append(all_variants[-1])

        return all_variants[:self.n_samples]

    # ─── 原子主张提取 ───────────────────────────────────

    def _extract_claims(self, text: str) -> List[str]:
        """从文本中提取原子主张"""
        claims = []
        seen = set()

        def add(c: str):
            c = c.strip().rstrip("。；,!！")
            if c and c not in seen and len(c) >= 2:
                seen.add(c)
                claims.append(c)

        # 1) 结论句：所以/因此/故/由此
        for m in re.finditer(r"(所以|因此|故|故而|于是|由此)(.+?)(?:。|；|$)", text):
            add(m.group(2))

        # 2) 前提句：如果/由于/因为/假设
        for m in re.finditer(r"(如果|若|假设|假如|要是)(.+?)(?:，|,)", text):
            add(m.group(2))
        for m in re.finditer(r"(由于|因为|鉴于)(.+?)(?:，|,|。)", text):
            add(m.group(2))

        # 注意：条件句（如果A，那么B）中的B不做独立主张提取
        # 避免"如果下雨地面会湿"中的"地面会湿"被当成事实断言

        # 3) 所有陈述句（取在矛盾关键词对的候选句）
        # 注意跳过以条件连词起句的句子
        cond_starters = ["如果", "若", "假设", "假如", "要是", "只要", "除非"]
        for sent in re.split(r"[。！？；]+", text):
            sent = sent.strip()
            if len(sent) < 3:
                continue
            # 跳过条件句，避免误判
            if any(sent.startswith(cs) for cs in cond_starters):
                continue
            # 看这句是否包含矛盾关键词对的任一端
            for pos, neg in self.contradiction_pairs:
                if pos in sent or neg in sent:
                    add(sent)
                    break

        # 4) 任意陈述句（长度>5且有谓语标记的句子）
        # 注意：以条件连接词起句的句子不做孤立主张提取
        # 否则"如果下雨地面会湿"中的"地面会湿"会被当成事实主张
        conditional_starters = ["如果", "若", "假设", "假如", "要是", "只要", "除非"]
        for sent in re.split(r"[。！？；]+", text):
            sent = sent.strip()
            if not sent or len(sent) < 6:
                continue
            # 跳过条件句
            if any(sent.startswith(cs) for cs in conditional_starters):
                continue
            if any(kw in sent for kw in ["是", "有", "会", "能", "要", "属于", "包含", "所有"]):
                add(sent)

        return claims

    # ─── 语义矛盾检测 ───────────────────────────────────

    def _find_claim_contradictions(self, text: str) -> List[str]:
        """在同一文本内部寻找自相矛盾的主张对"""
        contradictions = []
        claims = self._extract_claims(text)

        # 过滤：如果两个主张有子串关系（一个是另一个的严格子串），
        # 或者包含条件从句标记，则不是真正的矛盾
        def is_different_claims(a: str, b: str) -> bool:
            """判断两个主张是否真正不同（排除子串关系）"""
            if a in b or b in a:
                return False
            # 排除条件标记
            cond_markers = ["如果", "若", "假设", "假如", "只要"]
            for m in cond_markers:
                if m in a and m in b:
                    return False
            return True

        # 两两检查矛盾关键词对
        for i, c1 in enumerate(claims):
            for j, c2 in enumerate(claims):
                if i >= j or not is_different_claims(c1, c2):
                    continue
                for pos, neg in self.contradiction_pairs:
                    if pos in c1 and neg in c2:
                        contradictions.append(
                            f"主张相互矛盾：'{c1}' vs '{c2}'（{pos}/{neg}）"
                        )
                    elif neg in c1 and pos in c2:
                        contradictions.append(
                            f"主张相互矛盾：'{c1}' vs '{c2}'（{pos}/{neg}）"
                        )

        return contradictions

    def _check_embedding_consistency(self, variations: List[str]) -> Tuple[float, List[str]]:
        """
        使用句向量检查变体间的语义一致性。
        
        Returns:
            (consistency_score, warnings)
        """
        if len(variations) < 2:
            return 1.0, []

        # 计算所有变体的嵌入
        embeddings = self.embedder.encode(variations, normalize_embeddings=True)
        sim_matrix = embeddings @ embeddings.T  # 余弦相似度矩阵

        # 排除自相似 (对角线)
        n = len(variations)

        # 配对相似度的均值 = 一致性得分
        triu_sum = 0.0
        triu_count = 0
        min_sim = 1.0
        min_pair = (0, 0)
        for i in range(n):
            for j in range(i + 1, n):
                sim = float(sim_matrix[i][j])
                triu_sum += sim
                triu_count += 1
                if sim < min_sim:
                    min_sim = sim
                    min_pair = (i, j)

        avg_sim = triu_sum / triu_count if triu_count > 0 else 1.0

        # 变体多样性 = 1 - 平均相似度
        diversity = 1.0 - avg_sim

        # 一致性得分：高平均相似度 = 一致
        consistency = avg_sim

        # 产生警告
        warnings = []
        if min_sim < 0.6:
            warnings.append(
                f"变体间语义分歧：'{variations[min_pair[0]][:40]}...' vs "
                f"'{variations[min_pair[1]][:40]}...' "
                f"(相似度={min_sim:.2f})"
            )

        return consistency, warnings, diversity

    def verify(self, text: str) -> ConsistencyCheck:
        """
        验证文本的自洽性

        Args:
            text: 待检测的推理文本

        Returns:
            ConsistencyCheck: 检查结果
        """
        # 1. 生成多样性变体
        variations = self._generate_variations(text)

        # 2. 文本内主张矛盾检查
        claim_contradictions = self._find_claim_contradictions(text)

        # 3. 变体间语义一致性检查
        embed_consistency, embed_warnings, diversity = \
            self._check_embedding_consistency(variations)

        # 4. 综合矛盾列表
        all_contradictions = claim_contradictions + embed_warnings
        contradiction_count = len(all_contradictions)

        # 5. 计算最终置信度
        # 主张矛盾直接扣分（如果有明确的矛盾词对，扣更多）
        claim_penalty = 0.0
        if claim_contradictions:
            claim_penalty = min(0.5, len(claim_contradictions) * 0.25)

        # 嵌入一致性加权
        embed_score = embed_consistency

        # 最终得分
        confidence = max(0.0, min(1.0, embed_score - claim_penalty))

        # 判断是否自洽
        is_consistent = contradiction_count == 0 and confidence >= self.threshold

        return ConsistencyCheck(
            is_consistent=is_consistent,
            contradiction_count=contradiction_count,
            contradictions=all_contradictions,
            confidence=confidence,
            variation_diversity=diversity,
            samples_used=len(variations),
            variations=variations,
        )

    def verify_with_score(self, text: str) -> float:
        """返回自洽性得分 (0.0-1.0)"""
        return self.verify(text).confidence

    def batch_verify(self, texts: List[str]) -> List[ConsistencyCheck]:
        """批量验证"""
        return [self.verify(text) for text in texts]

    def get_contradiction_rate(self, text: str) -> float:
        """获取矛盾率"""
        result = self.verify(text)
        total_pairs = result.samples_used * (result.samples_used - 1) / 2
        rate = result.contradiction_count / max(total_pairs, 1)
        return min(rate, 1.0)


# 测试
if __name__ == "__main__":
    import time

    print("=" * 60)
    print("M3 自洽性验证器测试")
    print("=" * 60)

    verifier = ConsistencyVerifier(n_samples=5)

    # 测试 1: 有效三段论
    t1 = "如果明天下雨，比赛取消。明天下雨。因此比赛取消。"
    start = time.time()
    r1 = verifier.verify(t1)
    elapsed = (time.time() - start) * 1000
    print(f"\n[测试1] 有效三段论 ({elapsed:.0f}ms)")
    print(f"  自洽: {r1.is_consistent}, 置信度: {r1.confidence:.3f}")
    print(f"  矛盾数: {r1.contradiction_count}")
    print(f"  变体多样性: {r1.variation_diversity:.3f}")

    # 测试 2: 自相矛盾的文本
    t2 = "所有鸟类都会飞。企鹅是鸟类。因此企鹅会飞。但企鹅其实不会飞。"
    start = time.time()
    r2 = verifier.verify(t2)
    elapsed = (time.time() - start) * 1000
    print(f"\n[测试2] 自相矛盾 ({elapsed:.0f}ms)")
    print(f"  自洽: {r2.is_consistent}, 置信度: {r2.confidence:.3f}")
    print(f"  矛盾数: {r2.contradiction_count}")
    if r2.contradictions:
        for c in r2.contradictions[:3]:
            print(f"  ⚠  {c}")
    print(f"  变体多样性: {r2.variation_diversity:.3f}")

    # 测试 3: 内矛盾文本
    t3 = "这个方案是正确的。这个方案是错误的。"
    start = time.time()
    r3 = verifier.verify(t3)
    elapsed = (time.time() - start) * 1000
    print(f"\n[测试3] 直接矛盾 ({elapsed:.0f}ms)")
    print(f"  自洽: {r3.is_consistent}, 置信度: {r3.confidence:.3f}")
    print(f"  矛盾数: {r3.contradiction_count}")
    if r3.contradictions:
        for c in r3.contradictions[:3]:
            print(f"  ⚠  {c}")

    # 测试 4: 否定前件（推理错误但可能自洽 = 低分但不是矛盾）
    t4 = "如果下雨，地面会湿。没有下雨。因此地面不会湿。"
    r4 = verifier.verify(t4)
    print(f"\n[测试4] 否定前件（推理错误）")
    print(f"  自洽: {r4.is_consistent}, 置信度: {r4.confidence:.3f}")
    print(f"  矛盾数: {r4.contradiction_count}")
    if r4.contradictions:
        for c in r4.contradictions[:3]:
            print(f"  ⚠  {c}")

    # 测试 5: 简单事实陈述
    t5 = "太阳从东边升起。一天有24个小时。水在零度结冰。"
    r5 = verifier.verify(t5)
    print(f"\n[测试5] 事实陈述（非推理）")
    print(f"  自洽: {r5.is_consistent}, 置信度: {r5.confidence:.3f}")
    print(f"  矛盾数: {r5.contradiction_count}")
    if r5.contradictions:
        for c in r5.contradictions[:3]:
            print(f"  ⚠  {c}")

    # 测试 6: 展示变体
    print(f"\n[测试1 变体展示]")
    for i, v in enumerate(r1.variations):
        print(f"  [{i}] {v}")
