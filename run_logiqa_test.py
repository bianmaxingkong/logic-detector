import sys; sys.path.insert(0, '.')
import json, time
from src.detector import LogicDetector

detector = LogicDetector(threshold=0.4, chain_checker_model='BAAI/bge-small-zh-v1.5')

with open('data/test_set_logiqa_full_8678.json') as f:
    items = json.load(f)['test_cases']

total = len(items)
print(f'LogiQA total: {total}', flush=True)

fp = tn = tp = fnc = 0
start = time.time()
for i, item in enumerate(items):
    text = item['text']
    label = 1 if item['label'] == 'hallucination' else 0
    r = detector.analyze(text)
    h = r.is_hallucination

    if h and label == 0:
        fp += 1
    elif not h and label == 0:
        tn += 1
    elif not h and label == 1:
        fnc += 1
    elif h and label == 1:
        tp += 1

    if (i + 1) % 2000 == 0:
        print(f'  [{i+1}/{total}] elapsed={time.time()-start:.0f}s tp={tp} fp={fp} tn={tn} fn={fnc}', flush=True)

elapsed = time.time() - start
acc = (tp+tn)/total
prec = tp/(tp+fp) if (tp+fp) else 0
rec = tp/(tp+fnc) if (tp+fnc) else 0
f1v = 2*prec*rec/(prec+rec) if (prec+rec) else 0

print(f'', flush=True)
print(f'=== LogiQA Results (LogicValidator rules improved) ===', flush=True)
print(f'Total: {total}, Time: {elapsed:.1f}s', flush=True)
print(f'TP={tp} TN={tn} FP={fp} FN={fnc}', flush=True)
print(f'Accuracy: {acc:.4f} ({acc*100:.2f}%)', flush=True)
print(f'Precision: {prec:.4f} ({prec*100:.2f}%)', flush=True)
print(f'Recall: {rec:.4f} ({rec*100:.2f}%)', flush=True)
print(f'F1: {f1v:.4f}', flush=True)
print(f'FP old(no_chain_fix): 653, FP prev: 0, FP new: {fp}', flush=True)
print(f'FN old(no_chain_fix): 801, FN prev: 1144, FN new: {fnc}', flush=True)
