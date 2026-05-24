# LogicDetector GitHub Repository Setup Guide

**Created**: April 1, 2026  
**Project**: LogicDetector - Multi-Module Fusion for Logic Reasoning Hallucination Detection

---

## 📋 Step 1: Create a Repository on GitHub

### 1.1 Visit GitHub

Open your browser and go to: https://github.com/new

### 1.2 Fill in Repository Information

| Field | Value |
|-------|-------|
| **Repository name** | `logic-detector` |
| **Description** | `Multi-Module Fusion for Logic Reasoning Hallucination Detection (ACL 2026)` |
| **Visibility** | `Public` or `Private` |
| **Initialize with** | ❌ Do NOT select any options |

### 1.3 Click Create

Click the **"Create repository"** button

### 1.4 Record the Repository URL

After creation, record the repository URL in the format:
```
https://github.com/your-username/logic-detector.git
```

---

## 🔧 Step 2: Configure Local Git Remote

### 2.1 Add Remote Repository

```bash
cd /home/baibai/.openclaw/workspace/logic-detector

# Add remote repository (replace with your repository URL)
git remote add origin https://github.com/your-username/logic-detector.git

# Verify remote repository
git remote -v
```

### 2.2 Push to GitHub

```bash
# Push master branch
git push -u origin master

# Or if using main branch
# git branch -M main
# git push -u origin main
```

---

## 🔐 Step 3: Configure Git Authentication

### Method 1: Using Personal Access Token (Recommended)

#### 3.1.1 Create Token

1. Visit: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Fill in the information:
   - **Note**: `LogicDetector Project`
   - **Expiration**: `No expiration` (or select an expiration date)
   - **Select scopes**: Check `repo` (all permissions)
4. Click **"Generate token"**
5. **Copy the Token** (shown only once, save it!)

#### 3.1.2 Push Using Token

```bash
# Use token instead of password when pushing
git push -u origin master
# Username: your GitHub username
# Password: paste the copied Token
```

#### 3.1.3 Save Authentication (Optional)

```bash
# Configure credential storage
git config --global credential.helper store

# Push again, credentials will be saved
git push
```

### Method 2: Using SSH Key

#### 3.2.1 Generate SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter through prompts, or specify a save path
```

#### 3.2.2 Add Public Key to GitHub

1. Copy the public key content:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Visit: https://github.com/settings/keys
3. Click **"New SSH key"**
4. Fill in:
   - **Title**: `LogicDetector Project`
   - **Key**: Paste the public key content
5. Click **"Add SSH key"**

#### 3.2.3 Use SSH URL

```bash
# Add remote repository (using SSH URL)
git remote add origin git@github.com:your-username/logic-detector.git

# Push
git push -u origin master
```

---

## 📊 Step 4: Verify Push

### 4.1 Check Remote Repository

```bash
# View remote repository
git remote -v

# Should see:
# origin  https://github.com/your-username/logic-detector.git (fetch)
# origin  https://github.com/your-username/logic-detector.git (push)
```

### 4.2 View Commit History

```bash
# View commit history
git log --oneline

# Should see:
# 36b391f Initial commit: LogicDetector v1.0.0
```

### 4.3 View on GitHub

Visit your GitHub repository page. You should see:
- ✅ All project files
- ✅ Commit history
- ✅ File structure

---

## 🔄 Step 5: Daily Usage

### 5.1 Commit Changes

```bash
# View changes
git status

# Add changes
git add .

# Commit
git commit -m "Describe your changes"

# Push to GitHub
git push
```

### 5.2 Pull from GitHub

```bash
# Pull latest code
git pull
```

### 5.3 View Branches

```bash
# View local branches
git branch

# View remote branches
git branch -r

# View all branches
git branch -a
```

---

## 📝 Recommended: Add README Badges

Add the following badges at the top of README.md:

```markdown
# LogicDetector

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Multi-Module Fusion for Logic Reasoning Hallucination Detection (ACL 2026)
```

---

## 🎯 Complete Command List

```bash
# 1. Enter project directory
cd /home/baibai/.openclaw/workspace/logic-detector

# 2. Configure Git user information
git config user.email "your_email@example.com"
git config user.name "Your Name"

# 3. Add remote repository
git remote add origin https://github.com/your-username/logic-detector.git

# 4. Verify remote repository
git remote -v

# 5. Push code
git push -u origin master

# 6. View status
git status

# 7. View log
git log --oneline

# 8. Pull updates
git pull
```

---

## ⚠️ Common Issues

### Q1: Push failed "Permission denied"

**Cause**: Authentication issue

**Solution**:
```bash
# Push using Token
git push https://your-username:your-token@github.com/your-username/logic-detector.git master
```

### Q2: Push failed "remote already exists"

**Cause**: Remote repository already exists

**Solution**:
```bash
# Delete existing remote repository
git remote remove origin

# Re-add
git remote add origin https://github.com/your-username/logic-detector.git
```

### Q3: Push failed "failed to push some refs"

**Cause**: Remote repository has commits that local doesn't

**Solution**:
```bash
# Pull first, then push
git pull --rebase
git push
```

---

## 📞 Project Information

- **Project Name**: LogicDetector
- **Version**: v1.0.0
- **Paper**: ACL 2026 (Anonymous submission)
- **Accuracy**: 55.5% (target)
- **Efficiency**: 0.07ms/query
- **Memory**: <100MB

---

**Created**: 2026-04-01  
**Last Updated**: 2026-04-01
