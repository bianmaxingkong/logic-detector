#!/bin/bash
# LogicDetector Skill 安装脚本
# 被 OpenClaw skill 系统调用，下载工程并配置环境

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_DIR="${SKILL_DIR}/repo"

echo "=== LogicDetector Skill 安装 ==="

# 1. 克隆仓库
if [ ! -d "${REPO_DIR}" ]; then
    echo "正在克隆 LogicDetector 仓库..."
    git clone https://github.com/bianmaxingkong/logic-detector.git "${REPO_DIR}"
    echo "✓ 仓库克隆完成"
else
    echo "✓ 仓库已存在，跳过克隆"
fi

# 2. 安装 Python 依赖
if [ -f "${REPO_DIR}/requirements.txt" ]; then
    echo "正在安装 Python 依赖..."
    pip install -r "${REPO_DIR}/requirements.txt" --quiet
    echo "✓ 依赖安装完成"
fi

# 3. 下载模型文件
echo "正在下载模型文件（首次运行约需1-2分钟）..."
python3 "${SKILL_DIR}/scripts/download_models.py"

echo ""
echo "=== LogicDetector Skill 安装完成 ==="
echo "使用方式："
echo "  python3 ${REPO_DIR}/src/detect.py \"待检测的文本\""
echo "  echo \"待检测的文本\" | python3 ${REPO_DIR}/src/detect.py"
