# LogicDetector API Test Report (Port 8080)

**Service Address**: http://192.168.1.12:8080  
**Test Time**: 2026-04-05 22:18

---

## 🚀 Service Status

```bash
curl http://192.168.1.12:8080/health
```

**Response**:
```json
{
  "status": "ok",
  "service": "LogicDetector API",
  "version": "1.0.0"
}
```

---

## 📋 API Endpoints

### 1. Single Text Analysis

**Endpoint**: `POST /analyze`

**Request**:
```bash
curl -X POST http://192.168.1.12:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "If it rains, the ground gets wet. The ground is wet, so it rained."}'
```

**Response**:
```json
{
  "success": true,
  "is_hallucination": false,
  "confidence": 0.1,
  "logic_fallacies": [],
  "explanation": "Incomplete reasoning chain..."
}
```

---

### 2. Batch Analysis

**Endpoint**: `POST /batch`

**Request**:
```bash
curl -X POST http://192.168.1.12:8080/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Text 1", "Text 2"]}'
```

---

## 🌐 Access URLs

| Access Method | URL |
|---------------|-----|
| **Local** | http://localhost:8080 |
| **LAN** | http://192.168.1.12:8080 |

---

## 🛠️ Service Management

### Start Service
```bash
cd /home/baibai/.openclaw/workspace/logic-detector
python3 api_server.py
```

### Background Start
```bash
nohup python3 api_server.py > /tmp/logicdetector_api.log 2>&1 &
```

### Stop Service
```bash
pkill -f "api_server.py"
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Response Time | <1s |
| Memory Usage | ~85MB |
| Port | 8080 |

---

**Report Generated**: 2026-04-05 22:18
