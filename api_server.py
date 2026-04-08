#!/usr/bin/env python3
"""
LogicDetector API Server
支持局域网访问的 RESTful API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from detector import LogicDetector

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 初始化检测器
detector = LogicDetector()

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "service": "LogicDetector API",
        "version": "1.0.0"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """分析文本"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "缺少 text 参数"}), 400
        
        result = detector.analyze(text)
        
        return jsonify({
            "success": True,
            "is_hallucination": result.is_hallucination,
            "confidence": round(result.confidence, 3),
            "logic_fallacies": result.logic_fallacies,
            "explanation": result.explanation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch', methods=['POST'])
def batch_analyze():
    """批量分析"""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({"error": "缺少 texts 参数"}), 400
        
        results = []
        for text in texts:
            result = detector.analyze(text)
            results.append({
                "text": text[:100],
                "is_hallucination": result.is_hallucination,
                "confidence": round(result.confidence, 3)
            })
        
        return jsonify({
            "success": True,
            "count": len(results),
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import socket
    
    # 获取本机 IP
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"\n🚀 LogicDetector API Server 启动中...")
    print(f"📍 本地访问：http://localhost:8080")
    print(f"🌐 局域网访问：http://{local_ip}:8080")
    print(f"📋 API 文档：http://{local_ip}:8080/docs")
    print(f"\n按 Ctrl+C 停止服务\n")
    
    # 启动服务 (0.0.0.0 允许局域网访问)
    app.run(host='0.0.0.0', port=8080, debug=False)
