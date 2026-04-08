# LogicDetector API 测试报告

**服务地址**: http://192.168.1.12:5000  
**测试时间**: 2026-04-05 22:13

---

## 🚀 服务状态

```bash
curl http://192.168.1.12:5000/health
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
curl -X POST http://192.168.1.12:5000/analyze \
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
  "explanation": "推理链不完整，缺失步骤：结论：C 是 B\n总体评分：0.90 (阈值：0.35)"
}
```

---

### 2. 批量分析

**接口**: `POST /batch`

**请求**:
```bash
curl -X POST http://192.168.1.12:5000/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["文本 1", "文本 2"]}'
```

**响应**:
```json
{
  "success": true,
  "count": 2,
  "results": [
    {"text": "文本 1", "is_hallucination": false, "confidence": 0.1},
    {"text": "文本 2", "is_hallucination": true, "confidence": 0.8}
  ]
}
```

---

## 🧪 测试结果

### 测试用例 1: 肯定后件谬误

**输入**: "如果下雨，地面会湿。地面湿了，所以下雨了。"

**预期**: 检测到幻觉 (肯定后件谬误)

**实际**:
```json
{
  "is_hallucination": false,
  "confidence": 0.1,
  "logic_fallacies": []
}
```

**状态**: ⚠️ 未检测到 (需要优化)

---

### 测试用例 2: 有效推理

**输入**: "所有哺乳动物都有脊椎。狗是哺乳动物。所以狗有脊椎。"

**预期**: 未检测到幻觉

**实际**:
```json
{
  "is_hallucination": false,
  "confidence": 0.0,
  "logic_fallacies": []
}
```

**状态**: ✅ 正确

---

## 🌐 局域网访问

**本机 IP**: 192.168.1.12

**访问地址**:
- 本地：http://localhost:5000
- 局域网：http://192.168.1.12:5000

**同一局域网内的其他设备可以访问**:
```bash
curl http://192.168.1.12:5000/health
```

---

## 🛠️ 启动/停止服务

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
| 并发支持 | 单线程 (可扩展) |

---

**报告生成时间**: 2026-04-05 22:13
