#!/usr/bin/env python3
"""Run ablation on large-scale datasets — all 15 configurations per dataset.
Results are batch-saved incrementally to avoid losing partial progress."""
import json, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.detector import LogicDetector

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "data", "ablation_large_results.json")

# Datasets: focused selection for fast turnaround
DATASETS = [
    ("LogiQA-1k",     os.path.join(BASE, "data", "test_set_logiqa_1000.json")),
    ("LogicInference", os.path.join(BASE, "data", "test_set_logicinference_full.json")),
]

# All 15 configurations
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

def load_cases(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["test_cases"]

def evaluate(detector, cases):
    tp=tn=fp=fn=0
    start=time.time()
    for c in cases:
        true_lbl=(c["label"]=="hallucination")
        result=detector.analyze(c["text"])
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
    return {"acc":round(acc,4),"prec":round(prec,4),"rec":round(rec,4),"f1":round(f1,4),
            "tp":tp,"tn":tn,"fp":fp,"fn":fn,"time_s":round(elapsed,2)}

detector = LogicDetector()
all_results = {}

for ds_name, ds_path in DATASETS:
    print(f"\n{'='*60}")
    print(f"Dataset: {ds_name}")
    cases = load_cases(ds_path)
    print(f"  Samples: {len(cases)}")
    ds_results = []
    for name, w in CONFIGS:
        detector.set_module_weights(w)
        r = evaluate(detector, cases)
        r["config"] = name
        ds_results.append(r)
        print(f"  {name:20s} acc={r['acc']*100:.1f}% prec={r['prec']:.3f} rec={r['rec']:.3f} f1={r['f1']:.3f} [{r['tp']:5d},{r['tn']:5d},{r['fp']:3d},{r['fn']:5d}] {r['time_s']:.0f}s")
    all_results[ds_name] = ds_results
    # Save incrementally
    partial = {"datasets": list(all_results.keys()), "results": all_results, "partial": True}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(partial, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved to {OUT}")

final = {"datasets": list(all_results.keys()), "results": all_results, "partial": False}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(final, f, indent=2, ensure_ascii=False)
print(f"\n{'='*60}")
print(f"All done! Saved to {OUT}")
