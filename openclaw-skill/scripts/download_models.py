#!/usr/bin/env python3
"""
LogicDetector — 模型下载脚本
首次使用前运行一次，下载 BGE embedding 模型和 CFEVER 知识库
"""

import os
import sys
import json
import urllib.request
import tarfile
import shutil
from pathlib import Path


def get_project_root():
    """自动检测项目根目录"""
    script_dir = Path(__file__).resolve().parent  # openclaw-skill/scripts/
    skill_dir = script_dir.parent  # openclaw-skill/
    repo_dir = skill_dir.parent  # logic-detector/
    
    # 确认关键目录存在
    if (repo_dir / "src" / "detector.py").exists():
        return repo_dir
    if (repo_dir / "repo" / "src" / "detector.py").exists():
        return repo_dir / "repo"
    
    # fallback: 当前目录
    cwd = Path.cwd()
    if (cwd / "src" / "detector.py").exists():
        return cwd
    
    print("错误: 未找到 LogicDetector 项目根目录", file=sys.stderr)
    print(f"请确保在 {repo_dir} 或项目根目录下运行", file=sys.stderr)
    sys.exit(1)


def download_embedding_model(root_dir):
    """下载 BGE 中文 embedding 模型"""
    model_dir = root_dir / "models" / "bge-small-zh-v1.5"
    if model_dir.exists() and (model_dir / "tokenizer.json").exists():
        print(f"✓ BGE embedding 模型已存在: {model_dir}")
        return True
    
    print("正在下载 BGE embedding 模型 (33MB)...")
    model_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        from huggingface_hub import snapshot_download
        snapshot_download(
            repo_id="BAAI/bge-small-zh-v1.5",
            local_dir=str(model_dir),
            local_dir_use_symlinks=False,
        )
        print("✓ BGE embedding 模型下载完成")
        return True
    except ImportError:
        print("huggingface_hub 未安装，尝试通过 transformers 缓存...")
        try:
            from transformers import AutoModel, AutoTokenizer
            model = AutoModel.from_pretrained("BAAI/bge-small-zh-v1.5")
            tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-zh-v1.5")
            model.save_pretrained(str(model_dir))
            tokenizer.save_pretrained(str(model_dir))
            print("✓ BGE embedding 模型下载并保存完成")
            return True
        except Exception as e:
            print(f"✗ 模型下载失败: {e}", file=sys.stderr)
            print("请手动运行: pip install huggingface_hub && python3", __file__)
            return False


def download_knowledge_base(root_dir):
    """下载 CFEVER 知识库"""
    kb_dir = root_dir / "data" / "cfever_index"
    if kb_dir.exists() and (kb_dir / "cfever_meta.pkl").exists():
        print(f"✓ CFEVER 知识库已存在: {kb_dir}")
        return True
    
    print("正在下载 CFEVER 知识库 (~50MB)...")
    kb_dir.mkdir(parents=True, exist_ok=True)
    
    # 知识库文件列表
    kb_files = {
        "cfever_index.faiss": "https://huggingface.co/datasets/logic-detector/cfever-kb/resolve/main/cfever_index.faiss",
        "cfever_meta.pkl": "https://huggingface.co/datasets/logic-detector/cfever-kb/resolve/main/cfever_meta.pkl",
    }
    
    for filename, url in kb_files.items():
        dest = kb_dir / filename
        if dest.exists():
            continue
        try:
            print(f"  下载 {filename}...")
            urllib.request.urlretrieve(url, str(dest))
            print(f"  ✓ {filename}")
        except Exception as e:
            print(f"  ✗ {filename} 下载失败: {e}", file=sys.stderr)
    
    if all((kb_dir / f).exists() for f in kb_files):
        print("✓ CFEVER 知识库下载完成")
        return True
    return False


def main():
    root_dir = get_project_root()
    print(f"项目根目录: {root_dir}")
    
    # 确保 data 和 models 目录存在
    (root_dir / "data").mkdir(exist_ok=True)
    (root_dir / "models").mkdir(exist_ok=True)
    
    # 下载模型
    embedding_ok = download_embedding_model(root_dir)
    kb_ok = download_knowledge_base(root_dir)
    
    if embedding_ok and kb_ok:
        print("\n✓ 所有文件准备就绪！")
        print(f"  运行命令: python3 {root_dir}/src/detect.py \"待检测的文本\"")
    else:
        print("\n⚠ 部分文件下载未完成，请检查网络后重试")
        sys.exit(1)


if __name__ == "__main__":
    main()
