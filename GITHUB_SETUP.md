# LogicDetector GitHub 仓库设置指南

**创建时间**: 2026 年 4 月 1 日  
**项目**: LogicDetector - 多模块融合的逻辑推理幻觉检测框架

---

## 📋 第一步：在 GitHub 上创建仓库

### 1.1 访问 GitHub

打开浏览器访问：https://github.com/new

### 1.2 填写仓库信息

| 字段 | 值 |
|------|-----|
| **Repository name** | `logic-detector` |
| **Description** | `Multi-Module Fusion for Logic Reasoning Hallucination Detection (ACL 2026)` |
| **Visibility** | `Public` (公开) 或 `Private` (私有) |
| **Initialize with** | ❌ 不要勾选任何选项 |

### 1.3 点击创建

点击 **"Create repository"** 按钮

### 1.4 记录仓库地址

创建成功后，记录仓库地址，格式：
```
https://github.com/你的用户名/logic-detector.git
```

---

## 🔧 第二步：配置本地 Git 远程仓库

### 2.1 添加远程仓库

```bash
cd /home/baibai/.openclaw/workspace/logic-detector

# 添加远程仓库 (替换为你的仓库地址)
git remote add origin https://github.com/你的用户名/logic-detector.git

# 验证远程仓库
git remote -v
```

### 2.2 推送到 GitHub

```bash
# 推送主分支
git push -u origin master

# 或者如果使用 main 分支
# git branch -M main
# git push -u origin main
```

---

## 🔐 第三步：配置 Git 认证

### 方式 1: 使用 Personal Access Token (推荐)

#### 3.1.1 创建 Token

1. 访问：https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 填写信息：
   - **Note**: `LogicDetector Project`
   - **Expiration**: `No expiration` (或选择过期时间)
   - **Select scopes**: 勾选 `repo` (全部权限)
4. 点击 **"Generate token"**
5. **复制 Token** (只显示一次，务必保存！)

#### 3.1.2 使用 Token 推送

```bash
# 推送时使用 Token 代替密码
git push -u origin master
# 用户名：你的 GitHub 用户名
# 密码：粘贴刚才复制的 Token
```

#### 3.1.3 保存认证信息 (可选)

```bash
# 配置凭证存储
git config --global credential.helper store

# 再次推送，会保存凭证
git push
```

### 方式 2: 使用 SSH 密钥

#### 3.2.1 生成 SSH 密钥

```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 一路回车，或指定保存路径
```

#### 3.2.2 添加公钥到 GitHub

1. 复制公钥内容：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. 访问：https://github.com/settings/keys
3. 点击 **"New SSH key"**
4. 填写：
   - **Title**: `LogicDetector Project`
   - **Key**: 粘贴公钥内容
5. 点击 **"Add SSH key"**

#### 3.2.3 使用 SSH 地址

```bash
# 添加远程仓库 (使用 SSH 地址)
git remote add origin git@github.com:你的用户名/logic-detector.git

# 推送
git push -u origin master
```

---

## 📊 第四步：验证推送

### 4.1 检查远程仓库

```bash
# 查看远程仓库
git remote -v

# 应该看到：
# origin  https://github.com/你的用户名/logic-detector.git (fetch)
# origin  https://github.com/你的用户名/logic-detector.git (push)
```

### 4.2 查看提交历史

```bash
# 查看提交历史
git log --oneline

# 应该看到：
# 36b391f Initial commit: LogicDetector v1.0.0
```

### 4.3 在 GitHub 上查看

访问你的 GitHub 仓库页面，应该能看到：
- ✅ 所有项目文件
- ✅ 提交历史
- ✅ 文件结构

---

## 🔄 第五步：日常使用

### 5.1 提交更改

```bash
# 查看更改
git status

# 添加更改
git add .

# 提交
git commit -m "描述你的更改"

# 推送到 GitHub
git push
```

### 5.2 从 GitHub 拉取

```bash
# 拉取最新代码
git pull
```

### 5.3 查看分支

```bash
# 查看本地分支
git branch

# 查看远程分支
git branch -r

# 查看所有分支
git branch -a
```

---

## 📝 推荐：添加 README 徽章

在 README.md 顶部添加以下徽章：

```markdown
# LogicDetector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

多模块融合的逻辑推理幻觉检测框架 (ACL 2026)
```

---

## 🎯 完整命令清单

```bash
# 1. 进入项目目录
cd /home/baibai/.openclaw/workspace/logic-detector

# 2. 配置 Git 用户信息
git config user.email "your_email@example.com"
git config user.name "Your Name"

# 3. 添加远程仓库
git remote add origin https://github.com/你的用户名/logic-detector.git

# 4. 验证远程仓库
git remote -v

# 5. 推送代码
git push -u origin master

# 6. 查看状态
git status

# 7. 查看日志
git log --oneline

# 8. 拉取更新
git pull
```

---

## ⚠️ 常见问题

### Q1: 推送失败 "Permission denied"

**原因**: 认证问题

**解决**:
```bash
# 使用 Token 推送
git push https://你的用户名:你的 Token@github.com/你的用户名/logic-detector.git master
```

### Q2: 推送失败 "remote already exists"

**原因**: 远程仓库已存在

**解决**:
```bash
# 删除现有远程仓库
git remote remove origin

# 重新添加
git remote add origin https://github.com/你的用户名/logic-detector.git
```

### Q3: 推送失败 "failed to push some refs"

**原因**: 远程仓库有本地没有的提交

**解决**:
```bash
# 先拉取再推送
git pull --rebase
git push
```

---

## 📞 项目信息

- **项目名称**: LogicDetector
- **版本**: v1.0.0
- **论文**: ACL 2026 (Anonymous submission)
- **准确率**: 55.5% (目标)
- **效率**: 0.07ms/查询
- **内存**: <100MB

---

**创建日期**: 2026-04-01  
**最后更新**: 2026-04-01
