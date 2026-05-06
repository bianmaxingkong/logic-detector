#!/usr/bin/env python3
"""
构建 CFEVER 知识库 + 补充常识知识库 → FAISS 索引

流程：
1. 从 HuggingFace 加载 CFEVER 数据集
2. 加载补充常识知识库（覆盖常识盲区）
3. 提取 supports (11K) + refutes (7K) 的 claims + 常识 claims
4. 用 bge-small-zh-v1.5 全部嵌入
5. 构建 FAISS 索引（余弦相似度）
6. 保存到 data/cfever_index/
"""

import json, sys, pickle, os, time
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

DATA_DIR = project_root / "data" / "cfever_index"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Step 1: 加载 CFEVER 训练数据
# ============================================================
print("=" * 60)
print("Step 1/4: 加载知识库数据...")
print("=" * 60)

from datasets import load_dataset

ds = load_dataset("IKMLab-team/cfever", split="train")
print(f"  CFEVER 训练集: {len(ds)} 条")

supports_claims = []
refutes_claims = []
supports_domains = []
refutes_domains = []

for item in ds:
    label = item['label']
    claim = item['claim'].strip()
    domain = item.get('domain', 'unknown')
    if label == 'supports':
        supports_claims.append(claim)
        supports_domains.append(domain)
    elif label == 'refutes':
        refutes_claims.append(claim)
        refutes_domains.append(domain)

print(f"  CFEVER supports: {len(supports_claims)} | refutes: {len(refutes_claims)}")

# ============================================================
# Step 2: 加载补充常识知识库
# ============================================================
supp_path = project_root / "scripts" / "supplement_kb.py"
if supp_path.exists():
    sys.path.insert(0, str(project_root / "scripts"))
    from supplement_kb import COMMON_SENSE_FACTS
    for claim, label in COMMON_SENSE_FACTS:
        if label == 'supports':
            supports_claims.append(claim)
            supports_domains.append('常识')
        elif label == 'refutes':
            refutes_claims.append(claim)
            refutes_domains.append('常识')
    print(f"  补充常识: +{len(COMMON_SENSE_FACTS)} 条 ({sum(1 for _,l in COMMON_SENSE_FACTS if l=='supports')} supports + {sum(1 for _,l in COMMON_SENSE_FACTS if l=='refutes')} refutes)")

# 合并
all_claims = supports_claims + refutes_claims
all_labels = ['supports'] * len(supports_claims) + ['refutes'] * len(refutes_claims)
all_domains = supports_domains + refutes_domains

print(f"\n  总知识库: {len(all_claims)} 条 ({len(supports_claims)} supports + {len(refutes_claims)} refutes)")

# ============================================================
# Step 3: 嵌入
# ============================================================
print("\n" + "=" * 60)
print("Step 3/4: 用 bge-small-zh-v1.5 嵌入...")
print("=" * 60)

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
model_name = "bge-small-zh-v1.5"
embed_dim = model.get_sentence_embedding_dimension()
print(f"  模型维度: {embed_dim}")

batch_size = 256
embeddings = []

t0 = time.time()
for i in range(0, len(all_claims), batch_size):
    batch = all_claims[i:i+batch_size]
    batch_emb = model.encode(batch, normalize_embeddings=True, show_progress_bar=False)
    embeddings.append(batch_emb)
    elapsed = time.time() - t0
    rate = (i + len(batch)) / elapsed if elapsed > 0 else 0
    print(f"  [{i+len(batch)}/{len(all_claims)}] {rate:.0f} it/s", end='\r')

embeddings = np.vstack(embeddings).astype(np.float32)
print(f"\n  嵌入完成: {embeddings.shape}, 耗时 {time.time()-t0:.1f}s")

# ============================================================
# Step 4: 构建 FAISS 索引
# ============================================================
print("\n" + "=" * 60)
print("Step 4/4: 构建 FAISS 索引...")
print("=" * 60)

import faiss

index = faiss.IndexFlatIP(embed_dim)
index.add(embeddings)
print(f"  索引大小: {index.ntotal} 条")

# ============================================================
# Step 5: 保存
# ============================================================
print("\n" + "=" * 60)
print(" 保存到磁盘...")
print("=" * 60)

faiss_path = DATA_DIR / "cfever_index.faiss"
faiss.write_index(index, str(faiss_path))
print(f"  FAISS 索引: {faiss_path} ({os.path.getsize(faiss_path)/1024/1024:.1f} MB)")

meta_path = DATA_DIR / "cfever_meta.pkl"
meta = {
    'claims': all_claims,
    'labels': all_labels,
    'domains': all_domains,
    'num_supports': len(supports_claims),
    'num_refutes': len(refutes_claims),
    'embed_dim': embed_dim,
    'model_name': model_name,
}
with open(meta_path, 'wb') as f:
    pickle.dump(meta, f)
print(f"  元数据: {meta_path} ({os.path.getsize(meta_path)/1024:.1f} KB)")

# ============================================================
# 验证
# ============================================================
print("\n" + "=" * 60)
print("验证搜索...")
print("=" * 60)

test_queries = [
    "樂山大佛興建於宋朝。",
    "美國的首都是紐約。",
    "地球是平的。",
    "太陽從西邊升起。",
    "水在攝氏100度沸騰。",
]

for q in test_queries:
    q_emb = model.encode([q], normalize_embeddings=True).astype(np.float32)
    scores, idxs = index.search(q_emb, 3)
    print(f"\n  查询: {q}")
    for j, (score, idx) in enumerate(zip(scores[0], idxs[0])):
        label = all_labels[idx]
        print(f"    #{j+1} [{label:10s}] (sim={score:.3f}) {all_claims[idx][:60]}")

print(f"\n✅ 构建完成！{len(all_claims)} 条知识，保存到 {DATA_DIR}/")
