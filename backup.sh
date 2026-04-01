#!/bin/bash
# LogicDetector 项目备份脚本

BACKUP_DIR="/home/baibai/backups/logic-detector"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/home/baibai/.openclaw/workspace/logic-detector"

echo "======================================"
echo "LogicDetector 项目备份"
echo "======================================"
echo "备份时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 创建备份文件
BACKUP_FILE="$BACKUP_DIR/logic-detector_$DATE.tar.gz"
echo "创建备份文件：$BACKUP_FILE"

tar -czf "$BACKUP_FILE" \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='venv' \
  --exclude='.git' \
  --exclude='benchmarks/results' \
  --exclude='*.log' \
  "$PROJECT_DIR"

# 检查备份是否成功
if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo ""
    echo "✅ 备份成功!"
    echo "备份文件：$BACKUP_FILE"
    echo "备份大小：$BACKUP_SIZE"
else
    echo ""
    echo "❌ 备份失败!"
    exit 1
fi

# 保留最近 10 个备份
echo ""
echo "清理旧备份 (保留最近 10 个)..."
cd "$BACKUP_DIR"
ls -t logic-detector_*.tar.gz | tail -n +11 | xargs -r rm
echo "✅ 清理完成"

echo ""
echo "======================================"
echo "备份完成时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "======================================"
