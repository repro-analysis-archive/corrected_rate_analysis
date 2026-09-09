#!/usr/bin/env python3
"""
G1 — radiomics QC gate, per ANALYSIS_PLAN.md §7.3 plus the R1 post-R2a §2 reporting requirements.

Outcome-blinded throughout: reads feature matrices only. Y, T, CATE and AUTOC are never touched.

Produces (a) Q1-Q9 individually with threshold / measured / pass-fail, (b) old-vs-new side by side
on the collapse metrics, (c) a per-family breakdown of how many features changed materially, and
(d) feature-wise Spearman between the two extractions summarised per family.
"""
import os, json, sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
ROOT = f"{DATA}/archive"      # original-study radiomics (comparison baseline; not redistributed)
FEAT = f"{DATA}/features"
OUT = f"{RELEASE_ROOT}/reproduction/features"; os.makedirs(OUT, exist_ok=True)
BC = int(sys.argv[1]) if len(sys.argv) > 1 else 64

OLD = {"her2neg": f"{ROOT}/radiomics_all739.csv", "her2pos": f"{ROOT}/radiomics_her2pos.csv"}
NEW = {c: f"{FEAT}/radiomics_{c}_binCount{BC}_20260725.csv" for c in OLD}
BINS = pd.read_csv(f"{FEAT}/r2b_effective_bins_binCount{BC}.csv")

FAMS = ["shape", "firstorder", "glcm", "glrlm", "glszm", "ngtdm", "gldm"]
fam_of = lambda c: next((f for f in FAMS if c.startswith(f"original_{f}_")), "other")
TEXTURE = ["glcm", "glrlm", "glszm", "ngtdm", "gldm"]

R = {"date": "2026-07-25", "binCount": BC, "cohorts": {}, "Q": {}, "outcome_blinded": True}


def collapse_metrics(df):
    """The four degeneracy indicators, computed identically on either extraction."""
    m = {}
    e = df.get("original_firstorder_Entropy")
    m["prop_abs_entropy_lt_1e-12"] = float((e.abs() < 1e-12).mean()) if e is not None else None
    m["prop_entropy_exactly_0"] = float((e == 0.0).mean()) if e is not None else None
    j = df.get("original_glcm_JointEnergy")
    m["prop_jointenergy_eq_1"] = float((j == 1.0).mean()) if j is not None else None
    u = df.get("original_firstorder_Uniformity")
    m["prop_uniformity_eq_1"] = float((u == 1.0).mean()) if u is not None else None
    m["prop_uniformity_gt_0.99"] = float((u > 0.99).mean()) if u is not None else None
    tex = [c for c in df.columns if fam_of(c) in TEXTURE]
    sd = df[tex].std(ddof=1)
    nzv = 0
    for c in tex:
        v = df[c].dropna()
        if len(v) == 0:
            continue
        vc = v.value_counts()
        fr = vc.iloc[0] / vc.iloc[1] if len(vc) > 1 else np.inf
        if fr > 19 and (v.nunique() / len(v) * 100) < 10:
            nzv += 1
    m["n_texture"] = len(tex)
    m["prop_texture_zero_variance"] = float((sd == 0).sum() / len(tex))
    m["prop_texture_near_zero_variance"] = float(nzv / len(tex))
    return m


# ---------------- load ----------------
old_all, new_all = [], []
for coh in OLD:
    o = pd.read_csv(OLD[coh]); n = pd.read_csv(NEW[coh])
    o = o.set_index("patient_id"); n = n.set_index("patient_id").loc[o.index]
    R["cohorts"][coh] = {"n_old": len(o), "n_new": len(n),
                         "features_old": o.shape[1], "features_new": n.shape[1],
                         "ids_aligned": bool(list(o.index) == list(n.index)),
                         "collapse_OLD": collapse_metrics(o.reset_index()),
                         "collapse_NEW": collapse_metrics(n.reset_index())}
    old_all.append(o); new_all.append(n)
o_all = pd.concat(old_all); n_all = pd.concat(new_all)
common = [c for c in o_all.columns if c in n_all.columns]
R["n_features_common"] = len(common)
R["features_only_old"] = [c for c in o_all.columns if c not in n_all.columns][:20]
R["features_only_new"] = [c for c in n_all.columns if c not in o_all.columns][:20]

col_OLD = collapse_metrics(o_all.reset_index())
col_NEW = collapse_metrics(n_all.reset_index())
R["collapse_pooled"] = {"OLD": col_OLD, "NEW": col_NEW}

# ---------------- Q1-Q9 ----------------
eb = BINS["effective_bins"].dropna().astype(float)
q = {}
q["Q1"] = dict(metric="median effective (non-empty) bins per tumour in [30,130]",
               measured=float(np.median(eb)), threshold="30 <= median <= 130",
               **{"pass": bool(30 <= np.median(eb) <= 130)})
p16_256 = float(((eb >= 16) & (eb <= 256)).mean())
q["Q2"] = dict(metric="proportion with effective bins in [16,256]", measured=p16_256,
               threshold=">= 0.90", **{"pass": bool(p16_256 >= 0.90)})
q["Q3"] = dict(metric="proportion |first-order Entropy| < 1e-12", measured=col_NEW["prop_abs_entropy_lt_1e-12"],
               threshold="<= 0.01", **{"pass": bool(col_NEW["prop_abs_entropy_lt_1e-12"] <= 0.01)})
q["Q4"] = dict(metric="proportion GLCM JointEnergy == 1.0", measured=col_NEW["prop_jointenergy_eq_1"],
               threshold="<= 0.01", **{"pass": bool(col_NEW["prop_jointenergy_eq_1"] <= 0.01)})
q["Q5"] = dict(metric="proportion first-order Uniformity > 0.99", measured=col_NEW["prop_uniformity_gt_0.99"],
               threshold="<= 0.05", **{"pass": bool(col_NEW["prop_uniformity_gt_0.99"] <= 0.05)})
nzv_tot = col_NEW["prop_texture_zero_variance"] + col_NEW["prop_texture_near_zero_variance"]
q["Q6"] = dict(metric="zero/near-zero-variance texture features (share of 75)", measured=float(nzv_tot),
               threshold="<= 0.05", **{"pass": bool(nzv_tot <= 0.05)})
meta = json.load(open(f"{FEAT}/r2b_extraction_meta_binCount{BC}.json"))
nfail = sum(len(v) for v in meta["failures"].values())
nan_inf = int(np.isnan(n_all[common].values).sum() + np.isinf(n_all[common].values).sum())
q["Q7"] = dict(metric="extraction failures + NaN + Inf", measured=int(nfail + nan_inf),
               threshold="== 0", **{"pass": bool(nfail + nan_inf == 0)})
vol = "original_shape_MeshVolume"
if vol in n_all.columns:
    rho_vol = {c: abs(spearmanr(n_all[c], n_all[vol], nan_policy="omit").statistic)
               for c in common if c != vol}
    hi = {c: round(float(v), 4) for c, v in rho_vol.items() if v > 0.9}
else:
    hi = {}
q["Q8"] = dict(metric="features with |rho| > 0.9 vs MeshVolume (disclosure only)",
               measured=len(hi), threshold="disclosure only", **{"pass": True}, detail=hi)
lt10 = float((BINS["n_voxels_resampled"].astype(float) / BC < 10).mean())
q["Q9"] = dict(metric="proportion of tumours with < 10 voxels per bin", measured=lt10,
               threshold="<= 0.05", **{"pass": bool(lt10 <= 0.05)})
R["Q"] = q
required = [k for k in q if k != "Q8"]
R["G1_VERDICT"] = "PASS" if all(q[k]["pass"] for k in required) else "FAIL"
R["G1_failures"] = [k for k in required if not q[k]["pass"]]

# ---------------- old vs new, feature-wise ----------------
rows = []
for c in common:
    a, b = o_all[c].values.astype(float), n_all[c].values.astype(float)
    ok = np.isfinite(a) & np.isfinite(b)
    rho = spearmanr(a[ok], b[ok]).statistic if ok.sum() > 10 and np.std(a[ok]) > 0 and np.std(b[ok]) > 0 else np.nan
    rows.append({"feature": c, "family": fam_of(c), "spearman": rho,
                 "old_median": float(np.nanmedian(a)), "new_median": float(np.nanmedian(b)),
                 "old_sd": float(np.nanstd(a)), "new_sd": float(np.nanstd(b))})
fw = pd.DataFrame(rows)
fw.to_csv(f"{OUT}/g1_feature_correlations_binCount{BC}.csv", index=False)

fam = {}
for f in FAMS:
    s = fw[fw.family == f]
    if not len(s):
        continue
    r = s["spearman"].dropna()
    fam[f] = {"n_features": int(len(s)), "n_rho_computable": int(len(r)),
              "rho_median": float(r.median()) if len(r) else None,
              "rho_min": float(r.min()) if len(r) else None,
              "n_rho_below_0.5": int((r.abs() < 0.5).sum()),
              "n_rho_below_0.9": int((r.abs() < 0.9).sum()),
              "n_materially_changed_rho_lt_0.9": int((r.abs() < 0.9).sum()),
              "n_rho_nan_degenerate_old": int(s["spearman"].isna().sum())}
R["per_family"] = fam
r_all = fw["spearman"].dropna()
R["overall_correlation"] = {"n": int(len(r_all)), "median": float(r_all.median()),
                            "min": float(r_all.min()), "n_below_0.5": int((r_all.abs() < 0.5).sum()),
                            "n_below_0.9": int((r_all.abs() < 0.9).sum()),
                            "n_nan": int(fw["spearman"].isna().sum())}

with open(f"{OUT}/g1_qc_report_binCount{BC}.json", "w") as f:
    json.dump(R, f, indent=1)

# ---------------- print ----------------
print("=" * 78); print(f"G1 QC GATE — binCount={BC}"); print("=" * 78)
print(f"\nfeatures: old {o_all.shape[1]}, new {n_all.shape[1]}, common {len(common)}")
print(f"\n{'ID':4s} {'metric':52s} {'measured':>12s} {'thresh':>14s}  P/F")
for k in sorted(q):
    v = q[k]
    m = v["measured"]
    ms = f"{m:.4f}" if isinstance(m, float) else str(m)
    print(f"{k:4s} {v['metric'][:52]:52s} {ms:>12s} {v['threshold']:>14s}  {'PASS' if v['pass'] else 'FAIL'}")
print(f"\nG1 VERDICT: {R['G1_VERDICT']}" + (f"  failures={R['G1_failures']}" if R["G1_failures"] else ""))

print("\n--- collapse metrics, OLD vs NEW (pooled n=980) ---")
print(f"{'metric':44s} {'OLD':>10s} {'NEW':>10s}")
for k in ("prop_abs_entropy_lt_1e-12", "prop_entropy_exactly_0", "prop_jointenergy_eq_1",
          "prop_uniformity_eq_1", "prop_uniformity_gt_0.99",
          "prop_texture_zero_variance", "prop_texture_near_zero_variance"):
    print(f"{k:44s} {col_OLD[k]:>10.4f} {col_NEW[k]:>10.4f}")

print("\n--- per-family old-vs-new Spearman ---")
print(f"{'family':12s} {'n':>4s} {'rho med':>9s} {'rho min':>9s} {'<0.5':>6s} {'<0.9':>6s} {'nan':>5s}")
for f, v in fam.items():
    print(f"{f:12s} {v['n_features']:>4d} "
          f"{(v['rho_median'] if v['rho_median'] is not None else float('nan')):>9.3f} "
          f"{(v['rho_min'] if v['rho_min'] is not None else float('nan')):>9.3f} "
          f"{v['n_rho_below_0.5']:>6d} {v['n_rho_below_0.9']:>6d} {v['n_rho_nan_degenerate_old']:>5d}")
o = R["overall_correlation"]
print(f"\noverall: n={o['n']} median rho={o['median']:.3f} min={o['min']:.3f} "
      f"<0.5: {o['n_below_0.5']} <0.9: {o['n_below_0.9']} nan(degenerate): {o['n_nan']}")
print(f"\nwrote g1_qc_report_binCount{BC}.json and g1_feature_correlations_binCount{BC}.csv")
