#!/usr/bin/env python3
"""
LogicDetector CLI — 分析文本中的逻辑谬误和推理问题

Usage:
  echo "您的文本" | python3 detect.py
  python3 detect.py "您的文本"
  python3 detect.py --help

Output: JSON 格式的检测结果，包含幻觉判定、谬误类型、解释等。
"""

import sys
import json
import argparse
import os

# 抑制无关日志输出
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

DETECTOR_PATH = "/home/baibai/.openclaw/workspace/logic-detector/src"
sys.path.insert(0, DETECTOR_PATH)

import warnings
warnings.filterwarnings("ignore")

from detector import LogicDetector


def main():
    parser = argparse.ArgumentParser(description="LogicDetector — 逻辑推理幻觉检测")
    parser.add_argument("text", nargs="?", help="待检测的文本")
    parser.add_argument("--reasoning", "-r", default="deductive",
                        choices=["deductive", "inductive", "causal", "analogical"],
                        help="推理类型 (默认: deductive)")
    parser.add_argument("--verbose", "-v", action="store_true", help="输出详细解释")
    parser.add_argument("--quiet", "-q", action="store_true", help="只输出是否幻觉 (1=幻觉, 0=正常)")
    args = parser.parse_args()

    # 从参数或 stdin 读取文本
    if args.text:
        text = args.text
    else:
        text = sys.stdin.read().strip()

    if not text:
        print("错误: 请提供待检测文本", file=sys.stderr)
        sys.exit(1)

    # 初始化检测器，捕获加载过程中的日志
    try:
        detector = LogicDetector()
    except Exception as e:
        print(f"错误: 检测器初始化失败 — {e}", file=sys.stderr)
        sys.exit(1)

    # 执行检测
    result = detector.analyze(text, reasoning_type=args.reasoning)

    if args.quiet:
        print("1" if result.is_hallucination else "0")
        return

    output = {
        "is_hallucination": result.is_hallucination,
        "confidence": round(result.confidence, 4),
        "logic_fallacies": result.logic_fallacies,
        "completeness_score": round(result.completeness_score, 4),
        "is_consistent": result.is_consistent,
        "factual_errors": result.factual_errors,
        "explanation": result.explanation,
    }

    if args.verbose:
        output["module_weights"] = detector.get_module_weights()
        output["threshold"] = 0.35

    # 输出到 stdout（stderr 可能有模型加载日志）
    sys.stdout = os.fdopen(os.dup(1), "w")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
