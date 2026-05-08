#!/usr/bin/env python3
"""只跑M1+M2"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.detector import LogicDetector

class AblationDetector(LogicDetector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def analyze(self, text, reasoning_type="deductive"):
        fallacies = self.logic_validator.validate(text)
        has_fallacy = len(fallacies) > 0
        logic_score = 0.0 if has_fallacy else 1.0
        chain_analysis = self.chain_checker.check_completeness(text, reasoning_type)
        chain_score = chain_analysis.completeness_score
        overall_score = self.weights["logic"] * logic_score + self.weights["chain"] * chain_score
        is_hallucination = (overall_score < self.threshold) or has_fallacy
        return is_hallucination, overall_score

DATA_DIR = "/home/baibai/.openclaw/workspace/logic-detector/data"
TEST_SET = "test_set_logiqa_full_8678.json"

with open(os.path.join(DATA_DIR, TEST_SET), encoding="utf-8") as f:
    test_cases = json.load(f)["test_cases"]

detector = AblationDetector()
tp=tn=fp=fn=0
start=time.time()
for i,case in enumerate(test_cases):
    text=case["text"]
    true_lbl=(case["label"]=="hallucination")
    is_hall,score=detector.analyze(text)
    if true_lbl and is_hall: tp+=1
    elif not true_lbl and not is_hall: tn+=1
    elif not true_lbl and is_hall: fp+=1
    else: fn+=1
    if (i+1)%2000==0: print(f" 进度: {i+1}/{len(test_cases)}",flush=True)

elapsed=time.time()-start
total=tp+tn+fp+fn
acc=(tp+tn)/total*100
prec=tp/(tp+fp)*100 if tp+fp>0 else 0
rec=tp/(tp+fn)*100 if tp+fn>0 else 0
f1=2*prec*rec/(prec+rec) if prec+rec>0 else 0
result={
    "config":"M1+M2 only (no M3, no M4)",
    "accuracy":round(acc/100,4),"precision":round(prec/100,4),"recall":round(rec/100,4),"f1":round(f1/100,4),
    "tp":tp,"tn":tn,"fp":fp,"fn":fn,"total_time_s":round(elapsed,2)}
print(f"\n📊 M1+M2 only:\n Acc={acc:.2f}% P={prec:.2f}% R={rec:.2f}% F1={f1:.4f}\n TP={tp} TN={tn} FP={fp} FN={fn}")
with open("ablation_m1m2_only_result.json","w") as f:
    json.dump(result,f,ensure_ascii=False,indent=2)
