# 配置文件目录

此目录用于存放 LogicDetector 项目的配置文件。

## 📁 文件列表

### llm_config.json (不推送)

大模型配置文件，包含 API Key 等敏感信息。

**警告**: 此文件包含个人 API Key，已添加到 `.gitignore`，不会推送到 GitHub！

### 使用方法

1. 复制 `llm_config.json` 到 `config/` 目录
2. 修改 API Key 为你的密钥
3. 在代码中加载配置

```python
import json

with open('config/llm_config.json', 'r') as f:
    config = json.load(f)

# 使用配置
api_key = config['models']['providers']['sjtu']['apiKey']
```

## ⚠️ 注意事项

- **不要**将包含 API Key 的配置文件推送到 GitHub
- **不要**在代码中硬编码 API Key
- **使用**环境变量或配置文件管理敏感信息

---

**最后更新**: 2026-04-01
