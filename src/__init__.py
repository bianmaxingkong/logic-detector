"""
LogicDetector: Multi-Module Fusion for Logic Reasoning Hallucination Detection

LogicDetector 是一个轻量级、多模块融合的方法，用于检测大语言模型在逻辑推理中产生的幻觉。
"""

from .detector import LogicDetector
from .modules.logic_validator import LogicValidator
from .modules.chain_checker import ChainChecker
from .modules.consistency_verifier import ConsistencyVerifier
from .modules.fact_checker import FactChecker

__version__ = "1.0.0"
__author__ = "火眼团队"
__all__ = [
    "LogicDetector",
    "LogicValidator",
    "ChainChecker",
    "ConsistencyVerifier",
    "FactChecker",
]
