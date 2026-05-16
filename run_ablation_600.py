#!/usr/bin/env python3
"""Run full ablation on 600 benchmark — all 15 configurations"""
import json, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.detector import LogicDetector

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "data", "test_set_full_600.json")

with open(DATA_FILE, encoding="utf-8") as f:
    cases = json.load(f)["test_cases"]

# Fix duplicate in data
seen = set()
unique = []
for c in cases:
    key = (c["text"], c["label"])
    if key not in seen:
        seen.add(key)
        unique.append(c)
print(f"Total: {len(cases)}, Unique: {len(unique)}", flush=True)
cases = unique

# All configurations
CONFIGS = [
    ("M1 Only",       {"logic":1,"chain":0,"consistency":0,"fact":0}),
    ("M2 Only",       {"logic":0,"chain":1,"consistency":0,"fact":0}),
    ("M3 Only",       {"logic":0,"chain":0,"consistency":1,"fact":0}),
    ("M4 Only",       {"logic":0,"chain":0,"consistency":0,"fact":1}),
    ("M1+M2",         {"logic":0.5,"chain":0.5,"consistency":0,"fact":0}),
    ("M1+M3",         {"logic":0.5,"chain":0,"consistency":0.5,"fact":0}),
    ("M1+M4",         {"logic":0.5,"chain":0,"consistency":0,"fact":0.5}),
    ("M2+M3",         {"logic":0,"chain":0.5,"consistency":0.5,"fact":0}),
    ("M2+M4",         {"logic":0,"chain":0.5,"consistency":0,"fact":0.5}),
    ("M3+M4",         {"logic":0,"chain":0,"consistency":0.5,"fact":0.5}),
    ("M1+M2+M3",      {"logic":1/3,"chain":1/3,"consistency":1/3,"fact":0}),
    ("M1+M2+M4",      {"logic":1/3,"chain":1/3,"consistency":0,"fact":1/3}),
    ("M1+M3+M4",      {"logic":1/3,"chain":0,"consistency":1/3,"fact":1/3}),
    ("M2+M3+M4",      {"logic":0,"chain":1/3,"consistency":1/3,"fact":1/3}),
    ("Full (All 4)",  {"logic":0.25,"chain":0.25,"consistency":0.25,"fact":0.25}),
]

detector = LogicDetector()

results = []
for name, w in CONFIGS:
    detector.set_module_weights(w)
    tp=tn=fp=fn=0
    start=time.time()
    for c in cases:
        text=c["text"]
        true_lbl=(c["label"]=="hallucination")
        result=detector.analyze(text)
        if true_lbl and result.is_hallucination: tp+=1
        elif not true_lbl and not result.is_hallucination: tn+=1
        elif not true_lbl and result.is_hallucination: fp+=1
        else: fn+=1
    elapsed=time.time()-start
    total=tp+tn+fp+fn
    acc=(tp+tn)/total
    prec=tp/(tp+fp) if (tp+fp)>0 else 0
    rec=tp/(tp+fn) if (tp+fn)>0 else 0
    f1=2*prec*rec/(prec+rec) if (prec+rec)>0 else 0
    results.append({
        "config": name, "acc": round(acc,4), "prec": round(prec,4),
        "rec": round(rec,4), "f1": round(f1,4),
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "time_s": round(elapsed,2)
    })
    print(f"{name:20s} acc={acc*100:.1f}% prec={prec:.3f} rec={rec:.3f} f1={f1:.3f} [{tp},{tn},{fp},{fn}] {elapsed:.1f}s", flush=True)

print("\n=== JSON ===")
print(json.dumps(results, indent=2, ensure_ascii=False))
