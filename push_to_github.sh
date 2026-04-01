#!/bin/bash
# LogicDetector 推送到 GitHub 脚本

echo "======================================"
echo "LogicDetector 推送到 GitHub"
echo "======================================"
echo ""

# 配置
REPO_URL="https://github.com/bianmaxingkong/logic-detector.git"
PROJECT_DIR="/home/baibai/.openclaw/workspace/logic-detector"

cd "$PROJECT_DIR"

# 检查远程仓库
echo "检查远程仓库配置..."
git remote -v
echo ""

# 切换到 main 分支
echo "切换到 main 分支..."
git branch -M main
echo ""

# 提示输入 Token
echo "======================================"
echo "请输入 GitHub Personal Access Token"
echo "======================================"
echo ""
echo "获取 Token 步骤："
echo "1. 访问：https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 填写 Note: LogicDetector Project"
echo "4. 勾选 'repo' 权限"
echo "5. 点击 'Generate token'"
echo "6. 复制 Token (只显示一次！)"
echo ""
read -p "请输入 Token: " -s GITHUB_TOKEN
echo ""
echo ""

# 推送代码
echo "正在推送代码到 GitHub..."
echo ""

# 使用 Token 推送
git push https://bianmaxingkong:$GITHUB_TOKEN@github.com/bianmaxingkong/logic-detector.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ 推送成功!"
    echo "======================================"
    echo ""
    echo "查看仓库：https://github.com/bianmaxingkong/logic-detector"
    echo ""
else
    echo ""
    echo "======================================"
    echo "❌ 推送失败!"
    echo "======================================"
    echo ""
    echo "可能的原因："
    echo "1. Token 无效或已过期"
    echo "2. 没有仓库访问权限"
    echo "3. 网络连接问题"
    echo ""
fi
