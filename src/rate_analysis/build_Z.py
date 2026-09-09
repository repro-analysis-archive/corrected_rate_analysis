#!/usr/bin/env python3
"""R7 step 2 — common, configuration-independent, imaging-free evaluation covariates Z.

Z is built ONLY on the evaluation half and is shared by all six prioritization rules, so that
the six comparisons differ only in the ranking. Excluded by construction: radiomics, BiomedCLIP,
RAD-DINO; `tumor_subtype` (exactly collinear with `hr` in HER2-negative: luminal_a<->hr=1 n=381,
triple_negative<->hr=0 n=358, zero off-diagonal); `her2` (constant in this population).
The two whitespace-variant `menopause` "pre" levels are merged HERE ONLY; the frozen CATE
feature pipeline is untouched.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r7_common import *

EPOCH_LEVELS = list(range(1, 23))          # fixed 22-level basis from FROZEN_EPOCH

def norm_menopause(s):
    if pd.isna(s): return "unknown"
    t = " ".join(str(s).split()).lower()
    if t.startswith("pre"):  return "pre"
    if t.startswith("peri"): return "peri"
    if t.startswith("post"): return "post"
    return "other"

def build_Z(c, idx):
    g = c.iloc[idx]
    out = {}
    age = g.age.astype(float).values
    out["age_missing"] = np.isnan(age).astype(float)
    med = np.nanmedian(age)                                   # median of THIS set only
    out["age"] = np.where(np.isnan(age), med, age)
    out["hr"] = g.hr.astype(float).values
    out["mammaprint"] = g.mammaprint.astype(float).values
    for col, pref in [("ethnicity", "eth"), ("bmi_group", "bmi")]:
        v = g[col].fillna("unknown").astype(str).str.strip().str.lower()
        for lev in sorted(v.unique()): out[f"{pref}__{lev.replace(' ','_').replace('/','_')}"] = (v == lev).astype(float).values
    mp = g.menopause.map(norm_menopause)
    for lev in sorted(mp.unique()): out[f"meno__{lev}"] = (mp == lev).astype(float).values
    ep = g.epoch.astype(int).values
    dropped = []
    for lev in EPOCH_LEVELS:
        col = (ep == lev).astype(float)
        if col.sum() == 0: dropped.append(lev); continue
        out[f"ep__{lev}"] = col
    Z = pd.DataFrame(out, index=g.index)
    return Z, {"n": int(len(g)), "n_cols": int(Z.shape[1]),
               "age_median_used": float(med), "n_age_imputed": int(out["age_missing"].sum()),
               "epoch_levels_absent_in_this_set": dropped,
               "columns": list(Z.columns),
               "excluded_by_design": ["tumor_subtype (collinear with hr)", "her2 (constant)",
                                      "radiomics", "BiomedCLIP", "RAD-DINO"],
               "menopause_pre_variants_merged": True}

if __name__ == "__main__":
    c, cols, W = r4a.load("her2neg")
    n = len(c); is_train = split_739(n)
    T = c["T"].values.astype(int); Y = c.pcr.values.astype(float)
    meta = {}
    # (a) primary evaluation half - shared by PRIMARY, MAMMAPRINT, NO_EPOCH, ALT_NUISANCE
    te = np.where(~is_train)[0]
    Z, m = build_Z(c, te); meta["primary_eval_369"] = m
    Z.assign(patient_id=c.patient_id.values[te], T=T[te], Y=Y[te]).to_csv(f"{OUT}/Z_eval_primary.csv", index=False)
    # (b) empty-arm sensitivity evaluation subset
    empty = set(pd.read_csv(EPOCH_CSV).query("epoch in [1,21]").patient_id)
    keep = ~c.patient_id.isin(empty).values
    te2 = np.where((~is_train) & keep)[0]
    Z2, m2 = build_Z(c, te2); meta["empty_arm_eval_366"] = m2
    Z2.assign(patient_id=c.patient_id.values[te2], T=T[te2], Y=Y[te2]).to_csv(f"{OUT}/Z_eval_empty_arm.csv", index=False)
    # (c) sequential cross-fold partition: NEW random 5-fold, Y-independent, seed 42
    rng = np.random.default_rng(SEED); perm = rng.permutation(n)
    fold = np.empty(n, int)
    for k, part in enumerate(np.array_split(perm, 5)): fold[part] = k + 1
    pd.DataFrame({"patient_id": c.patient_id.values, "seq_fold": fold,
                  "T": T, "Y": Y}).to_csv(f"{OUT}/seq_folds_739.csv", index=False)
    for k in range(2, 6):
        tek = np.where(fold == k)[0]
        Zk, mk = build_Z(c, tek); meta[f"seq_eval_fold{k}"] = mk
        Zk.assign(patient_id=c.patient_id.values[tek], T=T[tek], Y=Y[tek]).to_csv(f"{OUT}/Z_eval_seqfold{k}.csv", index=False)
    json.dump(meta, open(f"{OUT}/Z_provenance.json", "w"), indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "columns"} for k, v in meta.items()}, indent=1))
    print("\nseq fold sizes:", np.bincount(fold)[1:].tolist())
    print("seq fold arm counts:", [(int((T[fold==k]==1).sum()), int((T[fold==k]==0).sum())) for k in range(1,6)])
