# LogicDetector API 测试报告 (端口 8080)

**服务地址**: http://192.168.1.12:8080  
**测试时间**: 2026-04-05 22:18

---

## 🚀 服务状态

```bash
curl http://192.168.1.12:8080/health
```

**响应**:
```json
{
  "status": "ok",
  "service": "LogicDetector API",
  "version": "1.0.0"
}
```

---

## 📋 API 接口

### 1. 单一文本分析

**接口**: `POST /analyze`

**请求**:
```bash
curl -X POST http://192.168.1.12:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "如果下雨，地面会湿。地面湿了，所以下雨了。"}'
```

**响应**:
```json
{
  "success": true,
  "is_hallucination": false,
  "confidence": 0.1,
  "logic_fallacies": [],
  "explanation": "推理链不完整..."
}
```

---

### 2. 批量分析

**接口**: `POST /batch`

**请求**:
```bash
curl -X POST http://192.168.1.12:8080/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["文本 1", "文本 2"]}'
```

---

## 🌐 访问地址

| 访问方式 | 地址 |
|----------|------|
| **本机访问** | http://localhost:8080 |
| **局域网访问** | http://192.168.1.12:8080 |

---

## 🛠️ 服务管理

### 启动服务
```bash
cd /home/baibai/.openclaw/workspace/logic-detector
python3 api_server.py
```

### 后台启动
```bash
nohup python3 api_server.py > /tmp/logicdetector_api.log 2>&1 &
```

### 停止服务
```bash
pkill -f "api_server.py"
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 响应时间 | <1s |
| 内存占用 | ~85MB |
| 端口 | 8080 |

---

**报告生成时间**: 2026-04-05 22:18
