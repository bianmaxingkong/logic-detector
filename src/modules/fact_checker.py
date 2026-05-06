"""
模块 4: 事实检查器 (Fact Checker) — 基于 CFEVER 知识库 + FAISS 检索

对输入文本中的事实性声明，通过 CFEVER 知识库进行验证。
使用 bge-small-zh-v1.5 嵌入 + FAISS 搜索，找最相似的知识条目。

支持的标签：
- supports  → 输入中的声明与事实一致（正确）
- refutes   → 输入中的声明与事实矛盾（错误 = 幻觉）

核心逻辑：
1. 提取输入文本中的事实性声明
2. 对每个声明：嵌入 → FAISS 搜索 top-k
3. 如果最佳 refutes 匹配 > 阈值 且 > 最佳 supports 匹配 → 事实错误
4. 如果最佳 supports 匹配 > 阈值 → 事实正确（跳过）
5. 否则 → 无法判断

优势：
- 完全离线运行
- 内存占用 <200MB (含嵌入模型)
- 单条延迟 ~10ms

知识库来源: CFEVER (Chinese Fact Extraction and VERification) — AAAI-24
"""

import re, pickle
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


@dataclass
class FactError:
    """事实错误记录"""
    claim: str            # 输入中的原声名
    matched_claim: str    # KB 中匹配的 refutes 条目
    similarity: float     # 余弦相似度
    label: str = 'refutes'  # 固定为 refutes


class FactChecker:
    """
    基于 CFEVER + FAISS 的事实检查器
    """

    def __init__(self, threshold: float = 0.70, top_k: int = 5):
        """
        Args:
            threshold: 相似度阈值（默认 0.70，经验值）
            top_k: 搜索候选项数
        """
        self.threshold = threshold
        self.top_k = top_k

        # 定位索引文件
        index_dir = Path(__file__).parent.parent.parent / "data" / "cfever_index"
        faiss_path = index_dir / "cfever_index.faiss"
        meta_path = index_dir / "cfever_meta.pkl"

        if not faiss_path.exists() or not meta_path.exists():
            raise FileNotFoundError(
                f"CFEVER 索引未找到！请先运行 scripts/build_cfever_index.py\n"
                f"  期望位置: {faiss_path}"
            )

        # 加载元数据
        with open(meta_path, 'rb') as f:
            self.meta = pickle.load(f)
        self.claims = self.meta['claims']
        self.labels = self.meta['labels']
        print(f"  [FactChecker] 加载 CFEVER 知识库: {len(self.claims)} 条 "
              f"({self.meta['num_supports']} supports + {self.meta['num_refutes']} refutes)")

        # 加载 FAISS 索引
        self.index = faiss.read_index(str(faiss_path))
        print(f"  [FactChecker] FAISS 索引已加载 ({self.index.ntotal} 条)")

        # 加载嵌入模型
        self.embedder = SentenceTransformer("BAAI/bge-small-zh-v1.5")
        print(f"  [FactChecker] 嵌入模型已加载 (dim={self.meta['embed_dim']})")

    # ------------------------------------------------------------------
    # 公共接口
    # ------------------------------------------------------------------

    def get_factual_errors(self, text: str) -> List[FactError]:
        """
        检查文本中的事实性错误

        Args:
            text: 待检测文本

        Returns:
            FactError 列表（空 = 无检测到的错误）
        """
        claims = self._extract_claims(text)
        if not claims:
            return []

        errors = []
        for claim in claims:
            error = self._verify_claim(claim)
            if error is not None:
                errors.append(error)

        return errors

    def get_fact_confirmation(self, text: str, threshold: Optional[float] = None) -> bool:
        """
        检查文本中是否有被知识库确认为正确的声明

        反向信号：即使 chain 评分低，如果事实被确认正确，也应放行

        Args:
            text: 待检测文本
            threshold: 相似度阈值（默认使用 self.threshold）

        Returns:
            True 如果有至少一个声明的 supports 匹配 > 阈值（事实被确认）
        """
        thresh = threshold if threshold is not None else 0.85
        claims = self._extract_claims(text)
        if not claims:
            return False

        for claim in claims:
            emb = self.embedder.encode([claim], normalize_embeddings=True).astype(np.float32)
            scores, idxs = self.index.search(emb, self.top_k)

            best_supports = 0.0
            best_refutes = 0.0
            for j in range(len(scores[0])):
                idx = idxs[0][j]
                sim = float(scores[0][j])
                label = self.labels[idx]
                if label == 'supports' and sim > best_supports:
                    best_supports = sim
                elif label == 'refutes' and sim > best_refutes:
                    best_refutes = sim

            # 事实被确认：supports 匹配超过阈值且强于 refutes
            if best_supports >= thresh and best_supports > best_refutes:
                return True

        return False

    # ------------------------------------------------------------------
    # 声明提取
    # ------------------------------------------------------------------

    def _extract_claims(self, text: str) -> List[str]:
        """从推理文本中提取事实性声明"""
        sentences = re.split(r'[。！？\n]', text)
        claims = []

        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 5:
                continue
            if '?' in sent or '？' in sent:
                continue
            if re.match(r'^(如果|假设|若|要是|假如)', sent):
                continue
            skip_pats = [r'^(这|那|它|他|她)', r'如何|怎样|为什么|多少', r'请|帮我|回答']
            if any(re.match(p, sent) for p in skip_pats):
                continue
            claims.append(sent)

        return claims

    # ------------------------------------------------------------------
    # 声明验证：核心逻辑
    # ------------------------------------------------------------------

    def _verify_claim(self, claim: str) -> Optional[FactError]:
        """
        验证单个声明

        逻辑：
          FAISS 搜索 top-k 个最近邻
          找到最佳 supports 匹配分数 S 和最佳 refutes 匹配分数 R
          
          规则：
          - R ≥ threshold 且 R > S → 事实错误（返回 FactError）
          - S ≥ threshold 且 S ≥ R → 事实正确（返回 None）
          - 其他 → 无法判断（返回 None）

        Returns:
            FactError 若检测到错误，否则 None
        """
        emb = self.embedder.encode([claim], normalize_embeddings=True).astype(np.float32)
        scores, idxs = self.index.search(emb, self.top_k)

        best_supports = 0.0
        best_refutes = 0.0
        best_refutes_idx = -1

        for j in range(len(scores[0])):
            idx = idxs[0][j]
            sim = float(scores[0][j])
            label = self.labels[idx]

            if label == 'supports' and sim > best_supports:
                best_supports = sim
            elif label == 'refutes' and sim > best_refutes:
                best_refutes = sim
                best_refutes_idx = idx

        # 判断逻辑：refutes 匹配强于 supports → 事实错误
        if best_refutes >= self.threshold and best_refutes > best_supports:
            return FactError(
                claim=claim,
                matched_claim=self.claims[best_refutes_idx],
                similarity=best_refutes,
            )

        return None
