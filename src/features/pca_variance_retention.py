#!/usr/bin/env python3
"""
R1 post-R2c §6b — variance retained by the corrected radiomics at 20 PCs, per fold, both cohorts,
compared against the FM blocks at 30 PCs.

Outcome-blinded in the sense that matters: no outcome-dependent RESULT is computed or examined —
no CATE, no AUTOC, no treatment effect. T and Y are read ONLY to construct the prespecified
stratified folds (StratifiedKFold on 2*T+Y), exactly as the pipeline does. Stated explicitly
rather than glossed.
"""
import os, json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import StratifiedKFold

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
ROOT = f"{DATA}/archive"      # original-study feature matrices (not redistributed)
R2 = f"{DATA}/features"
OUTDIR = f"{RELEASE_ROOT}/reproduction/features"; os.makedirs(OUTDIR, exist_ok=True)
FZ = f"{R2}/FROZEN_R2B"
SEED, N_OUTER = 42, 5
CLIN = f"{DATA}/clinical_and_imaging_info.xlsx"


def prep(her2, ctrl):
    df = pd.read_excel(CLIN)
    c = df[df["dataset"] == "ISPY2"].copy()
    c = c[c["her2"] == her2].dropna(subset=["pcr"]).copy()
    c["T"] = (c["nac_agent"] != ctrl).astype(int)
    return c[["patient_id", "T", "pcr"]]


BLOCKS = {
    "radiomics_CORRECTED": (f"{FZ}/radiomics_{{c}}_binCount64_20260725.csv", 20),
    "radiomics_ORIGINAL":  ({"her2neg": f"{ROOT}/radiomics_all739.csv",
                             "her2pos": f"{ROOT}/radiomics_her2pos.csv"}, 20),
    "BiomedCLIP":          ({"her2neg": f"{ROOT}/biomedclip_embeddings_739.csv",
                             "her2pos": f"{ROOT}/biomedclip_her2pos.csv"}, 30),
    "RAD-DINO":            ({"her2neg": f"{ROOT}/raddino_embeddings_739.csv",
                             "her2pos": f"{ROOT}/raddino_her2pos.csv"}, 30),
}
COH = {"her2neg": ("Paclitaxel", 0.0), "her2pos": ("Paclitaxel + Trastuzumab", 1.0)}

out = {"date": "2026-07-25", "seed": SEED, "n_outer_folds": N_OUTER,
       "note": ("T and Y used ONLY to construct the prespecified stratified folds; "
                "no outcome-dependent result computed or examined"),
       "results": {}}

for coh, (ctrl, hv) in COH.items():
    cl = prep(hv, ctrl)
    out["results"][coh] = {}
    for name, (src, k) in BLOCKS.items():
        path = src.format(c=coh) if isinstance(src, str) else src[coh]
        df = pd.read_csv(path)
        m = cl.merge(df, on="patient_id")
        feats = [c for c in df.columns if c != "patient_id"]
        X = np.nan_to_num(m[feats].values.astype(float), nan=0, posinf=0, neginf=0)
        T = m["T"].values.astype(int); Y = m["pcr"].values.astype(int)
        skf = StratifiedKFold(n_splits=N_OUTER, shuffle=True, random_state=SEED)
        per_fold = []
        for tr, te in skf.split(m, 2 * T + Y):
            ss = StandardScaler().fit(X[tr])
            keff = min(k, X.shape[1], len(tr))
            p = PCA(n_components=keff, random_state=SEED).fit(ss.transform(X[tr]))
            per_fold.append(float(np.sum(p.explained_variance_ratio_)))
        # full-data reference
        ssf = StandardScaler().fit(X)
        pf = PCA(n_components=min(k, X.shape[1]), random_state=SEED).fit(ssf.transform(X))
        out["results"][coh][name] = {
            "n": int(len(m)), "p_raw": len(feats), "n_components": k,
            "per_fold_variance_retained": [round(v, 6) for v in per_fold],
            "median": round(float(np.median(per_fold)), 6),
            "min": round(float(np.min(per_fold)), 6), "max": round(float(np.max(per_fold)), 6),
            "full_data_reference": round(float(np.sum(pf.explained_variance_ratio_)), 6),
        }

with open(f"{OUTDIR}/pca_variance_retention.json", "w") as f:
    json.dump(out, f, indent=1)

print("=" * 86)
print("VARIANCE RETAINED — per-fold PCA (fit on training folds), median [min-max]")
print("=" * 86)
print(f"{'cohort':9s} {'block':22s} {'p_raw':>6s} {'k':>4s} {'median':>9s} {'min':>9s} {'max':>9s}")
for coh in out["results"]:
    for name, r in out["results"][coh].items():
        print(f"{coh:9s} {name:22s} {r['p_raw']:>6d} {r['n_components']:>4d} "
              f"{r['median']*100:>8.2f}% {r['min']*100:>8.2f}% {r['max']*100:>8.2f}%")

print("\n--- the fairness comparison the ruling asks about ---")
for coh in out["results"]:
    rc = out["results"][coh]["radiomics_CORRECTED"]["median"]
    ro = out["results"][coh]["radiomics_ORIGINAL"]["median"]
    bc = out["results"][coh]["BiomedCLIP"]["median"]
    rd = out["results"][coh]["RAD-DINO"]["median"]
    print(f"  {coh}: corrected radiomics @20 = {rc*100:.2f}%   (original @20 = {ro*100:.2f}%)")
    print(f"           BiomedCLIP @30 = {bc*100:.2f}%   RAD-DINO @30 = {rd*100:.2f}%")
    print(f"           gap vs BiomedCLIP: {(bc-rc)*100:+.2f} pp")
print(f"\nwrote {R2}/pca_variance_retention.json")
