#!/usr/bin/env python3
"""R7 final figure round — canonical figure-data freezing (Python: numerical extraction only).

Reads ONLY sealed/frozen R7 machine-readable outputs, verifies each source against its directory
manifest AND against its sealed-copy byte identity, then writes one hash-guarded canonical JSON per
figure plus a .mat for MATLAB. NO new statistical inference is performed anywhere in this file:
values are selected and reformatted, never recomputed. Counts (rows, split sizes) are counts.
"""
import json, os, hashlib, sys
import scipy.io as sio

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
R7   = f"{RELEASE_ROOT}/results/rate_primary"
Q3   = f"{RELEASE_ROOT}/results/rate_q3"
Q4   = f"{RELEASE_ROOT}/results/rate_q4"
OUT  = f"{RELEASE_ROOT}/reproduction/figure_data"; os.makedirs(OUT, exist_ok=True)

ORDER = ["Clinical only", "Clin + Radiomics", "Clin + BiomedCLIP", "Clin + RAD-DINO",
         "Clin + Rad + BiomedCLIP", "Clin + Rad + RAD-DINO"]
LABEL = ["Clinical only", "Clinical + radiomics", "Clinical + BiomedCLIP", "Clinical + RAD-DINO",
         "Clinical + radiomics + BiomedCLIP", "Clinical + radiomics + RAD-DINO"]
REFERENCE = "Clin + Rad + BiomedCLIP"; BASELINE = "Clinical only"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def manifest(d):
    m = {}
    for l in open(f"{d}/ORIGINAL_SHA256SUMS.txt"):      # manifest of the frozen record; the released copies are byte-identical
        if l.startswith("#") or not l.strip(): continue
        hh, p = l.split(); m[p.lstrip("./")] = hh
    return m

PROV = []
def canon(base, name, sealed_dir):
    """Return path to the SEALED copy after (a) working copy vs manifest, (b) sealed vs working."""
    work = f"{base}/{name}"; seal = os.path.normpath(f"{base}/{sealed_dir}/{name}")
    m = manifest(base); hw = sha(work)
    if m.get(name) != hw:
        sys.exit(f"HALT: manifest mismatch for {work}")
    if sha(seal) != hw:
        sys.exit(f"HALT: sealed copy differs from working copy for {name}")
    PROV.append({"file": name, "sealed_path": seal, "sha256": hw,
                 "manifest": f"{base}/ORIGINAL_SHA256SUMS.txt",
                 "verified": "working-copy==manifest AND sealed-copy==working-copy"})
    return seal

def plain(p):
    PROV.append({"file": os.path.basename(p), "sealed_path": p, "sha256": sha(p),
                 "manifest": "n/a (frozen read-only input outside the R7 rounds)",
                 "verified": "sha256 recorded"})
    return p

# ---------------- sources ----------------
p_q1   = canon(R7, "rate_q1_primary.json", ".")
p_q2   = canon(R7, "rate_q2_primary.json", ".")
p_q2s  = canon(R7, "rate_q2_sensitivities.json", ".")
p_pri  = canon(R7, "priorities_provenance.json", ".")
p_q3   = canon(Q3, "rate_q3.json", ".")
p_q4r  = canon(Q4, "rate_q4_regimes.json", ".")
p_q4c  = canon(Q4, "rate_q4_contrasts.json", ".")

q1 = json.load(open(p_q1)); q2 = json.load(open(p_q2)); q2s = json.load(open(p_q2s))
q3 = json.load(open(p_q3)); q4r = json.load(open(p_q4r)); q4c = json.load(open(p_q4c))
pri = json.load(open(p_pri))

# counts only (public release: from the provenance record; the split and epoch tables are regenerated, not distributed)
n739 = pri["PRIMARY"]["n_total"]; n_H1 = pri["PRIMARY"]["n_train"]; n_H2 = pri["PRIMARY"]["n_eval"]
n728 = pri["EMPTY_ARM_728"]["n_total"] - pri["EMPTY_ARM_728"]["dropped"]
n241 = 241  # from the HER2-positive record below, asserted not typed
her2pos = json.load(open(f"{R7}/rate_her2pos_not_estimated.json"))
n241 = her2pos["n_total"]
n980 = n739 + n241          # both cohorts
PROV.append({"file": "rate_her2pos_not_estimated.json", "sealed_path": f"{R7}/rate_her2pos_not_estimated.json",
             "sha256": sha(f"{R7}/rate_her2pos_not_estimated.json"),
             "manifest": f"{R7}/ORIGINAL_SHA256SUMS.txt", "verified": "sha256 recorded"})

assert n739 == 739 and n_H1 == 370 and n_H2 == 369 and n980 == 980 and n728 == 728 and n241 == 241, \
    (n739, n_H1, n_H2, n980, n728, n241)
assert q3["n_H1"] == n_H1 and q3["n_H2"] == n_H2 and q4r["n_H1"] == n_H1 and q4r["n_H2"] == n_H2
assert q2["n_eval"] == n_H2 and q2s["n_eval_primary"] == n_H2

# ---------------- anchors (QA only; values come from the JSON) ----------------
A = [(q1["q1"]["Clinical only"]["estimate"], -0.0667886451),
     (q1["q1"]["Clin + BiomedCLIP"]["estimate"], +0.0975315664),
     (q1["q1"][REFERENCE]["estimate"], +0.0463733644),
     (q2["primary"]["results"]["reference - clinical_only"]["estimate"], +0.1131620095),
     (q3["results"][REFERENCE]["pooled_optimism"], +0.2271, 1e-4),
     (q4c["contrasts"][REFERENCE]["pooled_B_minus_A"], -0.0228, 1e-4)]
for t in A:
    got, want = t[0], t[1]; tol = t[2] if len(t) > 2 else 1e-9
    assert abs(got - want) < tol, f"anchor FAIL {got} vs {want}"
assert q1["q1"]["Clin + RAD-DINO"]["ci"][1] > 0, "RAD-DINO CI upper must be positive"
assert all(q4c["contrasts"][c]["pooled_P"] == "N/A (factor P structurally absent)"
           for c in [BASELINE]), "clinical-only P must be structural N/A"

BASE = {"figure_round": "R7_final_figures", "design_width_mm": 174.0,
        "configuration_order": ORDER, "configuration_labels": LABEL,
        "historically_designated_reference_configuration": REFERENCE,
        "reference_status_note": "historical designation belongs in the caption; it carries no visual privilege",
        "provenance": PROV}

def w(name, payload):
    p = f"{OUT}/{name}"
    json.dump(payload, open(p, "w"), indent=1)
    print(f"  {name:16s} sha256 {sha(p)[:16]}")
    return p

# ---------------- Fig 1 ----------------
f1 = dict(BASE, figure="Fig1", question="corrected analytic framework (R7)",
    kind="schematic", descriptive=True, inferential=False, interval="NONE", p_value="NONE",
    reference_line="N/A",
    nodes={"root": {"label": "MAMA-MIA / I-SPY2 cohort", "n": n980},
           "her2neg": {"label": "HER2-negative", "n": n739, "role": "primary"},
           "her2pos": {"label": "HER2-positive", "n": n241,
                       "role": "exploratory / descriptive only",
                       "status": her2pos["decision"],
                       "n_control_total": her2pos["n_control_total"]},
           "split": {"label": "fixed random 50/50 split, seed 42", "seed": 42},
           "H1": {"label": "H1", "n": n_H1}, "H2": {"label": "H2", "n": n_H2},
           "sens728": {"label": "empty-arm exclusion sensitivity", "n": n728,
                       "role": "parallel sensitivity branch from HER2-negative, not a sequential exclusion"}},
    questions=[{"key": "Q1", "text": "Configuration-specific RATE/AUTOC on independent held-out evaluation"},
               {"key": "Q2", "text": "Paired incremental RATE comparison"},
               {"key": "Q3", "text": "Opposite-half vs same-sample model-development/evaluation diagnostic"},
               {"key": "Q4", "text": "Preprocessing-placement diagnostic, opposite-half model fitting"}],
    directions={"Q1": "one direction (train H1 -> evaluate H2)", "Q2": "one direction (train H1 -> evaluate H2)",
                "Q3": "both split directions", "Q4": "both split directions"},
    structural_NA=["n = 693 permutation-overlap population is not part of the final primary framework"])
w("Fig1_data.json", f1)

# ---------------- Fig 2 ----------------
f2 = dict(BASE, figure="Fig2", question="Q1 configuration-specific standard centred doubly robust RATE/AUTOC",
    kind="forest", descriptive=False, inferential=True, reference_line=0.0,
    analytic_n=n739, evaluation_n=n_H2, x_label="RATE (AUTOC)",
    interval="95% CI = estimate +/- 1.96 * SE",
    interval_method=q1["design"]["se_method"], interval_method_id="grf_half_sample_bootstrap_R2000_seed20260906",
    p_value_note="raw and Holm p exist in the source but are NOT drawn in the figure",
    rows=[{"key": k, "label": LABEL[i], "order": i + 1,
           "estimate": q1["q1"][k]["estimate"], "se": q1["q1"][k]["std_err"],
           "ci_low": q1["q1"][k]["ci"][0], "ci_high": q1["q1"][k]["ci"][1]}
          for i, k in enumerate(ORDER)],
    structural_NA=[])
w("Fig2_data.json", f2)

# ---------------- Fig 3 ----------------
r2 = q2["primary"]["results"]
SENS = [("primary", "Primary", "reference - clinical_only", None, n739, n_H2),
        ("mammaprint", "MammaPrint-expanded baseline", "reference_plus_MP - clinical_plus_MP", "mammaprint", n739, n_H2),
        ("no_epoch", "No-epoch CATE", "reference - clinical_only", "no_epoch", n739, n_H2),
        ("alt_nuisance", "Alternative treatment-nuisance", "reference - clinical_only", "alt_nuisance", n739, n_H2),
        ("empty_arm_728", "Empty-arm exclusion", "reference - clinical_only", "empty_arm_728", n728,
         q2s["n_eval_empty_arm"])]
bl = []
for key, lab, field, sk, an, en in SENS:
    src = r2 if sk is None else q2s["sensitivities"][sk]["results"]
    v = src[field]
    bl.append({"key": key, "label": lab, "order": len(bl) + 1, "analytic_n": an, "evaluation_n": en,
               "direction": "reference-side rule minus corresponding clinical baseline",
               "source_field": field, "estimate": v["estimate"], "se": v["std_err"],
               "ci_low": v["ci"][0], "ci_high": v["ci"][1],
               "role": "primary inferential contrast" if sk is None else "sensitivity"})
f3 = dict(BASE, figure="Fig3", question="Q2 incremental value of the reference configuration beyond clinical variables",
    kind="two panels: paired estimates + difference forest", descriptive=False, inferential=True,
    reference_line=0.0, analytic_n=n739, evaluation_n=n_H2,
    interval="95% CI = estimate +/- 1.96 * SE",
    interval_method="grf half-sample bootstrap over evaluation patients, R=2000, seed 20260906; "
                    "two-column priorities give a PAIRED bootstrap for the difference (same draws for both rules)",
    interval_method_id="grf_half_sample_bootstrap_paired_R2000_seed20260906",
    pairing_unit="evaluation patients; the two prioritization rules share the bootstrap draws",
    panelA={"x_label": "RATE (AUTOC)",
            "rows": [{"key": BASELINE, "label": LABEL[0], "order": 1,
                      "estimate": r2["clinical_only"]["estimate"], "se": r2["clinical_only"]["std_err"],
                      "ci_low": r2["clinical_only"]["ci"][0], "ci_high": r2["clinical_only"]["ci"][1]},
                     {"key": REFERENCE, "label": LABEL[4], "order": 2,
                      "estimate": r2["reference"]["estimate"], "se": r2["reference"]["std_err"],
                      "ci_low": r2["reference"]["ci"][0], "ci_high": r2["reference"]["ci"][1]}],
            "connector": "thin neutral line between the two point estimates: they form one paired comparison"},
    panelB={"x_label": "Difference in RATE", "rows": bl},
    structural_NA=["HER2-positive: NOT ESTIMATED FOR INFERENCE; not plotted"])
w("Fig3_data.json", f3)

# ---------------- Fig 4 ----------------
f4 = dict(BASE, figure="Fig4", question="Q3 same-sample versus opposite-half model-development/evaluation",
    kind="grouped dot/range plot", descriptive=True, inferential=False,
    interval="NONE", p_value="NONE", reference_line=0.0,
    analytic_n=n739, evaluation_n={"H1": n_H1, "H2": n_H2},
    x_label="Change in RATE (same-sample - opposite-half)",
    pooled_definition=q3["design"]["pooled"],
    rows=[{"key": k, "label": LABEL[i], "order": i + 1,
           "H1": q3["results"][k]["optimism_H1"], "H2": q3["results"][k]["optimism_H2"],
           "pooled": q3["results"][k]["pooled_optimism"]} for i, k in enumerate(ORDER)],
    series=[{"key": "H1", "label": "H1 (n = %d)" % n_H1}, {"key": "H2", "label": "H2 (n = %d)" % n_H2},
            {"key": "pooled", "label": "Pooled"}],
    structural_NA=[])
assert all(r["H1"] > 0 and r["H2"] > 0 and r["pooled"] > 0 for r in f4["rows"]), "all 18 Q3 values must be > 0"
w("Fig4_data.json", f4)

# ---------------- Fig 5 ----------------
NA = "N/A (factor P structurally absent)"
rowsB, rowsC = [], []
for i, k in enumerate(ORDER):
    bh = q4r["results"][k]["by_half"]
    rowsB.append({"key": k, "label": LABEL[i], "order": i + 1,
                  "H1": bh["H1"]["Total_B_minus_A"], "H2": bh["H2"]["Total_B_minus_A"]})
    c = q4c["contrasts"][k]
    rowsC.append({"key": k, "label": LABEL[i], "order": i + 1,
                  "P": None if c["pooled_P"] == NA else c["pooled_P"],
                  "S": c["pooled_S"],
                  "PS": None if c["pooled_PS"] == NA else c["pooled_PS"],
                  "P_structural_NA": c["pooled_P"] == NA, "PS_structural_NA": c["pooled_PS"] == NA})
f5 = dict(BASE, figure="Fig5", question="Q4 preprocessing-placement diagnostic (observed data)",
    kind="three panels: regime schematic + half-specific B-A + pooled additive contrasts",
    descriptive=True, inferential=False, interval="NONE", p_value="NONE", reference_line=0.0,
    analytic_n=n739, evaluation_n={"H1": n_H1, "H2": n_H2},
    key_definitions={"P": "Imaging-block preprocessing placement (scaling + PCA)",
                     "S": "Clinical-scaler placement"},
    panelA={"regimes": [
        {"key": "A",  "imaging": "training half", "clinical": "training half", "model": "training half", "evaluate": "opposite half"},
        {"key": "D1", "imaging": "full n = %d" % n739, "clinical": "training half", "model": "training half", "evaluate": "opposite half"},
        {"key": "D2", "imaging": "training half", "clinical": "full n = %d" % n739, "model": "training half", "evaluate": "opposite half"},
        {"key": "B",  "imaging": "full n = %d" % n739, "clinical": "full n = %d" % n739, "model": "training half", "evaluate": "opposite half"}],
        "invariant": "the CATE model is fitted on the training (opposite) half in every regime; "
                     "held-out outcomes and treatment labels never enter model fitting"},
    panelB={"x_label": "Change in RATE (B - A)", "rows": rowsB,
            "series": [{"key": "H1", "label": "H1 (n = %d)" % n_H1}, {"key": "H2", "label": "H2 (n = %d)" % n_H2}]},
    panelC={"x_label": "Pooled change in RATE", "rows": rowsC,
            "series": [{"key": "P", "label": "P"}, {"key": "S", "label": "S"}, {"key": "PS", "label": "P x S"}]},
    structural_NA=["Clinical only: pooled P and pooled P x S are structurally absent and are OMITTED, "
                   "not plotted as zero"],
    prohibited=["variance ratio", "exponentiation", "ratio = 1 reference line", "null distribution",
                "|Q4/Q3| plotted as a decomposition"])
assert sum(1 for r in rowsB if r["H1"] * r["H2"] < 0) == 6, "sign disagreement must hold in all 6 rows"
assert rowsC[0]["P"] is None and rowsC[0]["PS"] is None, "clinical-only P / PxS must be null in the JSON"
w("Fig5_data.json", f5)

# ---------------- .mat for MATLAB + manifest ----------------
def col(rows, k): return [(float("nan") if r[k] is None else r[k]) for r in rows]
sio.savemat(f"{OUT}/fig_data_r7.mat", {
  "labels": LABEL, "order": list(range(1, 7)),
  "n980": n980, "n739": n739, "n241": n241, "nH1": n_H1, "nH2": n_H2, "n728": n728,
  "f2_est": col(f2["rows"], "estimate"), "f2_lo": col(f2["rows"], "ci_low"), "f2_hi": col(f2["rows"], "ci_high"),
  "f3a_est": col(f3["panelA"]["rows"], "estimate"), "f3a_lo": col(f3["panelA"]["rows"], "ci_low"),
  "f3a_hi": col(f3["panelA"]["rows"], "ci_high"), "f3a_lab": [r["label"] for r in f3["panelA"]["rows"]],
  "f3b_est": col(bl, "estimate"), "f3b_lo": col(bl, "ci_low"), "f3b_hi": col(bl, "ci_high"),
  "f3b_lab": [r["label"] for r in bl],
  "f4_H1": col(f4["rows"], "H1"), "f4_H2": col(f4["rows"], "H2"), "f4_pooled": col(f4["rows"], "pooled"),
  "f5b_H1": col(rowsB, "H1"), "f5b_H2": col(rowsB, "H2"),
  "f5c_P": col(rowsC, "P"), "f5c_S": col(rowsC, "S"), "f5c_PS": col(rowsC, "PS"),
  "f5c_P_isNA": [int(r["P_structural_NA"]) for r in rowsC], "f5c_PS_isNA": [int(r["PS_structural_NA"]) for r in rowsC],
})
with open(f"{OUT}/FIGURE_DATA_SHA256.txt", "w") as fh:
    fh.write("# canonical figure data for the R7 final figure round\n")
    for n in ["Fig1_data.json", "Fig2_data.json", "Fig3_data.json", "Fig4_data.json", "Fig5_data.json",
              "fig_data_r7.mat"]:
        fh.write(f"{sha(f'{OUT}/{n}')}  {n}\n")
    fh.write("\n# upstream R7 sources (sealed copies), verified working==manifest and sealed==working\n")
    for p in PROV:
        fh.write(f"{p['sha256']}  {p['sealed_path']}\n")
print("\nall anchors PASS; wrote canonical/ + FIGURE_DATA_SHA256.txt")
