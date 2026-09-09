#!/usr/bin/env python3
"""R7 step 4 - sequential cross-fold priorities (Q1 sensitivity only).
New Y-independent random 5-fold partition, seed 42. For k=2..5 the CATE rule is fitted on
folds 1..k-1 and evaluated on fold k, so fold k is never used to train the rule that ranks it.
Never used for the primary Q2 paired-difference p-value."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r7_common import *
from fit_priorities import priorities
import warnings; warnings.filterwarnings("ignore")

c, cols, W = r4a.load("her2neg")
n = len(c); T = c["T"].values.astype(int); Y = c.pcr.values.astype(float)
fold = pd.read_csv(f"{OUT}/seq_folds_739.csv").seq_fold.values
assert (pd.read_csv(f"{OUT}/seq_folds_739.csv").patient_id.values == c.patient_id.values).all()

rows, prov = [], {}
for k in range(2, 6):
    tr = np.where(fold <= k - 1)[0]; te = np.where(fold == k)[0]
    assert len(set(tr) & set(te)) == 0
    for name, b in CONFIGS.items():
        t0 = time.perf_counter()
        s, p = priorities(c, cols, W, b, T, Y, tr, te)
        p["elapsed_s"] = round(time.perf_counter() - t0, 2); prov[f"fold{k}|{name}"] = p
        rows.append(pd.DataFrame({"seq_fold": k, "patient_id": c.patient_id.values[te],
                                  "T": T[te], "Y": Y[te], "configuration": name, "priority": s}))
    print(f"  fold {k}: trained on folds 1..{k-1} (n={len(tr)}), evaluated on n={len(te)}", flush=True)
pd.concat(rows, ignore_index=True).to_csv(f"{OUT}/priorities_sequential.csv", index=False)
json.dump(prov, open(f"{OUT}/priorities_sequential_provenance.json", "w"), indent=1)
print("wrote priorities_sequential.csv")
