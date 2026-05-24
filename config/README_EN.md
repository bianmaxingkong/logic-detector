# Configuration Directory

This directory stores configuration files for the LogicDetector project.

## 📁 File List

### llm_config.json (Not Pushed)

Large model configuration file, containing sensitive information such as API Keys.

**Warning**: This file contains personal API Keys and has been added to `.gitignore`. It will NOT be pushed to GitHub!

### Usage

1. Copy `llm_config.json` to the `config/` directory
2. Modify the API Key to your own key
3. Load configuration in code

```python
import json

with open('config/llm_config.json', 'r') as f:
    config = json.load(f)

# Use configuration
api_key = config['models']['providers']['sjtu']['apiKey']
```

## ⚠️ Important Notes

- **DO NOT** push configuration files containing API Keys to GitHub
- **DO NOT** hardcode API Keys in code
- **Use** environment variables or configuration files to manage sensitive information

---

**Last Updated**: 2026-04-01
