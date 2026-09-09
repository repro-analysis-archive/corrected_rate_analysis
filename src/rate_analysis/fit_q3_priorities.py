#!/usr/bin/env python3
"""R7-Q3 step 1 - honest and apparent prioritization scores in BOTH directions.
A_H2 is reused verbatim from the frozen R7 output. C_H2, A_H1, C_H1 are new fits.
The retired bespoke autoc() is never computed."""
import os, sys, json, time, hashlib
RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
R7 = os.path.join(RELEASE_ROOT, "reproduction", "rate_primary")     # primary-stage outputs (the frozen R7 set in the original run)
OUT3 = os.path.join(RELEASE_ROOT, "reproduction", "rate_q3"); os.makedirs(OUT3, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r7_common import *                                   # frozen R7 loader + constants
from build_Z import build_Z                               # frozen R7 Z spec, unmodified
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.decomposition import PCA
from econml.dml import CausalForestDML
import warnings; warnings.filterwarnings("ignore")
FZ = R7

def make_cf():
    return CausalForestDML(model_y=RandomForestRegressor(**NUIS),
                           model_t=RandomForestClassifier(**NUIS),
                           n_estimators=500, min_samples_leaf=20, random_state=SEED, cv=5,
                           discrete_treatment=True)

def honest(c, cols, W, blocks, T, Y, fit_idx, eval_idx):
    """preprocessing AND model fitted on fit_idx; priorities predicted on eval_idx (disjoint)."""
    assert len(set(fit_idx) & set(eval_idx)) == 0
    CL = c[CLIN].values.astype(float)
    ss = StandardScaler().fit(CL[fit_idx])
    Xf, Xe = [ss.transform(CL[fit_idx])], [ss.transform(CL[eval_idx])]
    rows = {"clin_scaler_fit_rows": int(len(fit_idx)), "imaging_fit_rows": []}
    for key, k in blocks:
        V = np.nan_to_num(c[cols[key]].values.astype(float))
        s2 = StandardScaler().fit(V[fit_idx]); p = PCA(k, random_state=SEED).fit(s2.transform(V[fit_idx]))
        rows["imaging_fit_rows"].append(int(len(fit_idx)))
        Xf.append(p.transform(s2.transform(V[fit_idx]))); Xe.append(p.transform(s2.transform(V[eval_idx])))
    cf = make_cf(); cf.fit(Y[fit_idx], T[fit_idx], X=np.hstack(Xf), W=W[fit_idx])
    return cf.effect(np.hstack(Xe)).flatten(), rows

def apparent(c, cols, W, blocks, T, Y, idx):
    """preprocessing AND model fitted on idx; priorities predicted on the SAME idx."""
    CL = c[CLIN].values.astype(float)
    parts = [StandardScaler().fit_transform(CL[idx])]
    rows = {"clin_scaler_fit_rows": int(len(idx)), "imaging_fit_rows": []}
    for key, k in blocks:
        V = np.nan_to_num(c[cols[key]].values.astype(float))[idx]
        parts.append(PCA(k, random_state=SEED).fit_transform(StandardScaler().fit_transform(V)))
        rows["imaging_fit_rows"].append(int(len(idx)))
    X = np.hstack(parts); cf = make_cf(); cf.fit(Y[idx], T[idx], X=X, W=W[idx])
    return cf.effect(X).flatten(), rows

if __name__ == "__main__":
    c, cols, W = r4a.load("her2neg")
    n = len(c); T = c["T"].values.astype(int); Y = c.pcr.values.astype(float)
    sp = pd.read_csv(f"{FZ}/split_739.csv")
    assert (sp.patient_id.values == c.patient_id.values).all(), "frozen split does not align"
    assert (sp["T"].values == T).all() and np.allclose(sp.Y.values, Y)
    H1 = np.where(sp.split.values == "train")[0]      # R7 training half, n=370
    H2 = np.where(sp.split.values == "eval")[0]       # R7 evaluation half, n=369
    print(f"H1 n={len(H1)}  H2 n={len(H2)}  disjoint={len(set(H1)&set(H2))==0}", flush=True)

    frozen_A_H2 = pd.read_csv(f"{FZ}/priorities_primary_heldout.csv")
    prov, out = {}, {"H1": [], "H2": []}
    for name, b in CONFIGS.items():
        # --- direction 1: evaluate on H2 ---
        a2 = frozen_A_H2[frozen_A_H2.configuration == name]
        assert (a2.patient_id.values == c.patient_id.values[H2]).all()
        t0 = time.perf_counter(); c2, r2 = apparent(c, cols, W, b, T, Y, H2)
        prov[f"C_H2|{name}"] = dict(r2, regime="apparent", half="H2", n=int(len(H2)),
                                    elapsed_s=round(time.perf_counter()-t0, 2))
        out["H2"].append(pd.DataFrame({"patient_id": c.patient_id.values[H2], "T": T[H2], "Y": Y[H2],
                                       "configuration": name, "priority_A": a2.priority.values,
                                       "priority_C": c2}))
        # --- direction 2: evaluate on H1 ---
        t0 = time.perf_counter(); a1, r1a = honest(c, cols, W, b, T, Y, H2, H1)
        prov[f"A_H1|{name}"] = dict(r1a, regime="honest", half="H1", fit_half="H2",
                                    n=int(len(H1)), elapsed_s=round(time.perf_counter()-t0, 2))
        t0 = time.perf_counter(); c1, r1c = apparent(c, cols, W, b, T, Y, H1)
        prov[f"C_H1|{name}"] = dict(r1c, regime="apparent", half="H1", n=int(len(H1)),
                                    elapsed_s=round(time.perf_counter()-t0, 2))
        out["H1"].append(pd.DataFrame({"patient_id": c.patient_id.values[H1], "T": T[H1], "Y": Y[H1],
                                       "configuration": name, "priority_A": a1, "priority_C": c1}))
        print(f"  {name:26s} C_H2 sd={c2.std():.5f}  A_H1 sd={a1.std():.5f}  C_H1 sd={c1.std():.5f}", flush=True)
    pd.concat(out["H1"], ignore_index=True).to_csv(f"{OUT3}/priorities_q3_H1.csv", index=False)
    pd.concat(out["H2"], ignore_index=True).to_csv(f"{OUT3}/priorities_q3_H2.csv", index=False)

    # common imaging-free DR covariates for H1, same locked spec
    Z1, m1 = build_Z(c, H1)
    Z1.assign(patient_id=c.patient_id.values[H1], T=T[H1], Y=Y[H1]).to_csv(f"{OUT3}/Z_H1.csv", index=False)
    json.dump({"Z_H1": m1, "priorities": prov,
               "A_H2_source": "REUSED VERBATIM from FROZEN_R7/priorities_primary_heldout.csv",
               "H2_DR_source": "REUSED VERBATIM from FROZEN_R7/dr_scores_primary_heldout.csv"},
              open(f"{OUT3}/q3_provenance.json", "w"), indent=1)
    print("\nwrote priorities_q3_H1.csv, priorities_q3_H2.csv, Z_H1.csv, q3_provenance.json")
