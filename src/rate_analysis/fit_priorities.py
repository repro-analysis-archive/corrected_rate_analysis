#!/usr/bin/env python3
"""R7 step 1 — independent held-out treatment-prioritization scores.

Fits every configuration on the TRAINING half only and predicts one priority per EVALUATION
patient. All data-adaptive preprocessing (clinical scaler, imaging scaler, PCA) is fitted on the
training half only. Evaluation outcomes and evaluation treatment labels never enter training.
The bespoke uncentred `autoc()` is NOT computed anywhere in R7.
"""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r7_common import *
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.decomposition import PCA
from econml.dml import CausalForestDML
import warnings; warnings.filterwarnings("ignore")

def priorities(c, cols, W, blocks, T, Y, tr, te, clin=None, use_W=True, discrete=True):
    CL = c[clin if clin else CLIN].values.astype(float)
    ss = StandardScaler().fit(CL[tr])
    Xtr, Xte = [ss.transform(CL[tr])], [ss.transform(CL[te])]
    prov = {"clin_scaler_fit_rows": int(len(tr)), "imaging_fit_rows": []}
    for key, k in blocks:
        V = np.nan_to_num(c[cols[key]].values.astype(float))
        s2 = StandardScaler().fit(V[tr]); p = PCA(k, random_state=SEED).fit(s2.transform(V[tr]))
        prov["imaging_fit_rows"].append({"block": key, "k": k, "fit_rows": int(len(tr))})
        Xtr.append(p.transform(s2.transform(V[tr]))); Xte.append(p.transform(s2.transform(V[te])))
    Xtr, Xte = np.hstack(Xtr), np.hstack(Xte)
    Wtr = W[tr] if use_W else None
    mt = RandomForestClassifier(**NUIS) if discrete else RandomForestRegressor(**NUIS)
    cf = CausalForestDML(model_y=RandomForestRegressor(**NUIS), model_t=mt,
                         n_estimators=500, min_samples_leaf=20, random_state=SEED, cv=5,
                         discrete_treatment=discrete)
    cf.fit(Y[tr], T[tr], X=Xtr, W=Wtr)
    prov.update({"n_train": int(len(tr)), "n_eval": int(len(te)),
                 "X_train_shape": list(Xtr.shape), "X_eval_shape": list(Xte.shape),
                 "W_used": bool(use_W), "discrete_treatment": bool(discrete)})
    return cf.effect(Xte).flatten(), prov

def run(tag, cohort, blocks_map, clin=None, use_W=True, discrete=True, drop_ids=None):
    c, cols, W = r4a.load(cohort)
    n = len(c); T = c["T"].values.astype(int); Y = c["pcr"].values.astype(float)
    is_train = split_739(n) if cohort == "her2neg" else split_739(n)
    keep = np.ones(n, bool)
    if drop_ids: keep = ~c.patient_id.isin(drop_ids).values
    tr = np.where(is_train & keep)[0]; te = np.where((~is_train) & keep)[0]
    assert len(set(tr) & set(te)) == 0
    rows, provs = [], {}
    for name, b in blocks_map.items():
        t0 = time.perf_counter()
        s, prov = priorities(c, cols, W, b, T, Y, tr, te, clin, use_W, discrete)
        prov["elapsed_s"] = round(time.perf_counter() - t0, 2); provs[name] = prov
        rows.append(pd.DataFrame({"patient_id": c.patient_id.values[te], "eval_row": np.arange(len(te)),
                                  "T": T[te], "Y": Y[te], "configuration": name, "priority": s}))
        print(f"  {tag:34s} {name:34s} n_tr={len(tr)} n_te={len(te)}  {prov['elapsed_s']:5.1f}s", flush=True)
    df = pd.concat(rows, ignore_index=True)
    meta = {"tag": tag, "cohort": cohort, "n_total": int(n), "n_train": int(len(tr)),
            "n_eval": int(len(te)), "clin": clin if clin else CLIN, "use_W": use_W,
            "discrete_treatment": discrete, "dropped": 0 if not drop_ids else int((~keep).sum()),
            "seed": SEED, "provenance": provs}
    return df, meta, c, T, Y, tr, te

if __name__ == "__main__":
    c0, _, _ = r4a.load("her2neg")
    is_train = split_739(len(c0))
    pd.DataFrame({"patient_id": c0.patient_id.values,
                  "split": np.where(is_train, "train", "eval"),
                  "T": c0["T"].values.astype(int), "Y": c0.pcr.values.astype(float),
                  "hr": c0.hr.values, "mammaprint": c0.mammaprint.values,
                  "epoch": c0.epoch.values.astype(int)}).to_csv(f"{OUT}/split_739.csv", index=False)
    print("wrote split_739.csv", flush=True)

    allmeta = {}
    df, meta, *_ = run("PRIMARY", "her2neg", CONFIGS)
    df.to_csv(f"{OUT}/priorities_primary_heldout.csv", index=False); allmeta["PRIMARY"] = meta

    MP = {"Clinical + MammaPrint": [], "Historical reference + MammaPrint": CONFIGS[REFERENCE]}
    d2, m2, *_ = run("MAMMAPRINT", "her2neg", MP, clin=CLIN + ["mammaprint"])
    d2.to_csv(f"{OUT}/priorities_sens_mammaprint.csv", index=False); allmeta["MAMMAPRINT"] = m2

    SUB = {BASELINE: CONFIGS[BASELINE], REFERENCE: CONFIGS[REFERENCE]}
    d3, m3, *_ = run("NO_EPOCH", "her2neg", SUB, use_W=False)
    d3.to_csv(f"{OUT}/priorities_sens_no_epoch.csv", index=False); allmeta["NO_EPOCH"] = m3
    d4, m4, *_ = run("ALT_NUISANCE", "her2neg", SUB, discrete=False)
    d4.to_csv(f"{OUT}/priorities_sens_alt_nuisance.csv", index=False); allmeta["ALT_NUISANCE"] = m4

    empty = set(pd.read_csv(EPOCH_CSV).query("epoch in [1,21]").patient_id)
    d5, m5, *_ = run("EMPTY_ARM_728", "her2neg", SUB, drop_ids=empty)
    d5.to_csv(f"{OUT}/priorities_sens_empty_arm.csv", index=False); allmeta["EMPTY_ARM_728"] = m5

    json.dump(allmeta, open(f"{OUT}/priorities_provenance.json", "w"), indent=1)
    print("\nwrote priorities_provenance.json", flush=True)
