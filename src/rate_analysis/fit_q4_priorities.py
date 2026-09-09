#!/usr/bin/env python3
"""R7-Q4 - preprocessing-placement regimes A / D1 / D2 / B, both split directions.
The causal forest is ALWAYS fitted on the training (opposite) half. Only unsupervised
preprocessing placement varies. Held-out Y and T never enter any fit. autoc() is never called."""
import os, sys, json, time
RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
R7  = os.path.join(RELEASE_ROOT, "reproduction", "rate_primary")     # primary-stage outputs (the frozen R7 set in the original run)
OUT4 = os.path.join(RELEASE_ROOT, "reproduction", "rate_q4"); os.makedirs(OUT4, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r7_common import *
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.decomposition import PCA
from econml.dml import CausalForestDML
import warnings; warnings.filterwarnings("ignore")
FZ = R7
REGIMES = {"A": (False, False), "D1": (True, False), "D2": (False, True), "B": (True, True)}  # (img_full, clin_full)

def regime(c, cols, W, blocks, T, Y, tr, te, img_full, clin_full):
    n = len(T); CL = c[CLIN].values.astype(float)
    prov = {"clin_fit_rows": None, "img_fit_rows": [], "cf_fit_rows": int(len(tr)),
            "cf_fit_rows_in_heldout": len(set(tr) & set(te))}
    if clin_full:
        ss = StandardScaler().fit(CL); prov["clin_fit_rows"] = int(n)
    else:
        ss = StandardScaler().fit(CL[tr]); prov["clin_fit_rows"] = int(len(tr))
    Xtr, Xte = [ss.transform(CL[tr])], [ss.transform(CL[te])]
    for key, k in blocks:
        V = np.nan_to_num(c[cols[key]].values.astype(float))
        if img_full:
            s2 = StandardScaler().fit(V); p = PCA(k, random_state=SEED).fit(s2.transform(V))
            prov["img_fit_rows"].append(int(n))
        else:
            s2 = StandardScaler().fit(V[tr]); p = PCA(k, random_state=SEED).fit(s2.transform(V[tr]))
            prov["img_fit_rows"].append(int(len(tr)))
        Xtr.append(p.transform(s2.transform(V[tr]))); Xte.append(p.transform(s2.transform(V[te])))
    cf = CausalForestDML(model_y=RandomForestRegressor(**NUIS), model_t=RandomForestClassifier(**NUIS),
                         n_estimators=500, min_samples_leaf=20, random_state=SEED, cv=5,
                         discrete_treatment=True)
    cf.fit(Y[tr], T[tr], X=np.hstack(Xtr), W=W[tr])      # opposite-half outcomes/treatments ONLY
    return cf.effect(np.hstack(Xte)).flatten(), prov

if __name__ == "__main__":
    c, cols, W = r4a.load("her2neg")
    n = len(c); T = c["T"].values.astype(int); Y = c.pcr.values.astype(float)
    sp = pd.read_csv(f"{FZ}/split_739.csv")
    assert (sp.patient_id.values == c.patient_id.values).all()
    H1 = np.where(sp.split.values == "train")[0]; H2 = np.where(sp.split.values == "eval")[0]
    assert len(set(H1) & set(H2)) == 0 and len(H1) == 370 and len(H2) == 369
    out, prov = {"H1": [], "H2": []}, {}
    for half, tr, te in [("H2", H1, H2), ("H1", H2, H1)]:
        for name, b in CONFIGS.items():
            cols_out = {"patient_id": c.patient_id.values[te], "T": T[te], "Y": Y[te]}
            for rg, (imf, clf) in REGIMES.items():
                t0 = time.perf_counter()
                s, p = regime(c, cols, W, b, T, Y, tr, te, imf, clf)
                p.update(regime=rg, half=half, config=name, has_imaging=len(b) > 0,
                         elapsed_s=round(time.perf_counter() - t0, 2))
                prov[f"{half}|{name}|{rg}"] = p
                cols_out[f"priority_{rg}"] = s
            d = pd.DataFrame(cols_out); d.insert(3, "configuration", name)
            out[half].append(d)
            id_D1A = float(np.max(np.abs(d.priority_D1 - d.priority_A)))
            id_BD2 = float(np.max(np.abs(d.priority_B - d.priority_D2)))
            prov[f"{half}|{name}|identity"] = {"max_abs_D1_minus_A": id_D1A, "max_abs_B_minus_D2": id_BD2}
            print(f"  {half}  {name:26s} maxabs(D1-A)={id_D1A:.3e}  maxabs(B-D2)={id_BD2:.3e}", flush=True)
    for h in ("H1", "H2"):
        pd.concat(out[h], ignore_index=True).to_csv(f"{OUT4}/priorities_q4_{h}.csv", index=False)
    leak = sum(v.get("cf_fit_rows_in_heldout", 0) for v in prov.values() if "cf_fit_rows_in_heldout" in v)
    json.dump({"regimes": "A=(img train, clin train) D1=(img FULL739, clin train) "
                          "D2=(img train, clin FULL739) B=(img FULL739, clin FULL739); "
                          "causal forest fitted on the training half in ALL regimes",
               "total_cf_fit_rows_falling_in_the_held_out_half": leak,
               "per_run": prov}, open(f"{OUT4}/q4_provenance.json", "w"), indent=1)
    print(f"\ntotal causal-forest fit rows falling in a held-out half: {leak}")
    print("wrote priorities_q4_H1.csv, priorities_q4_H2.csv, q4_provenance.json")
