#!/usr/bin/env python3
"""
R1 §3 step 1 — ROI voxel-count distribution after resampling to 1 mm isotropic.

Pure geometry. Touches no outcome, treatment, CATE or AUTOC, and is therefore permitted before
ANALYSIS_PLAN.md commits. Masks are resampled with NEAREST NEIGHBOUR (B-spline is for the image;
interpolating a label map would invent fractional labels).

The decision rule is fixed in advance by the R1 sign-off and is applied mechanically below:

    Choose the largest binCount in {32, 64} for which at least 95% of tumours have at least
    10 voxels per bin. If 64 qualifies, primary = 64, sensitivity = 32. If only 32 qualifies,
    primary = 32, sensitivity = 64. If neither qualifies, stop and report.

10 voxels/bin  ->  binCount 64 requires >= 640 voxels ; binCount 32 requires >= 320 voxels.
"""
import os, json
import numpy as np
import pandas as pd
import SimpleITK as sitk

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
SEG = f"{DATA}/segmentations"
OUT = f"{RELEASE_ROOT}/reproduction/features/roi_voxel_distribution.json"; os.makedirs(os.path.dirname(OUT), exist_ok=True)
LABEL = 1  # radiomics_all.py settings: {'label': 1}

ids_neg = cohort_ids("her2neg", CLINICAL_XLSX)
ids_pos = cohort_ids("her2pos", CLINICAL_XLSX)
print(f"HER2- {len(ids_neg)}   HER2+ {len(ids_pos)}   union {len(set(ids_neg) | set(ids_pos))}")


def resample_to_1mm(img):
    osp = np.array(img.GetSpacing(), dtype=float)
    osz = np.array(img.GetSize(), dtype=int)
    nsp = np.array([1.0, 1.0, 1.0])
    nsz = np.maximum(np.round(osz * osp / nsp).astype(int), 1)
    f = sitk.ResampleImageFilter()
    f.SetOutputSpacing(nsp.tolist())
    f.SetSize([int(v) for v in nsz])
    f.SetOutputOrigin(img.GetOrigin())
    f.SetOutputDirection(img.GetDirection())
    f.SetInterpolator(sitk.sitkNearestNeighbor)   # label map
    f.SetDefaultPixelValue(0)
    return f.Execute(img)


rows = []
for i, pid in enumerate(sorted(set(ids_neg) | set(ids_pos))):
    p = f"{SEG}/{pid}.nii.gz"
    if not os.path.exists(p):
        rows.append({"patient_id": pid, "error": "missing_segmentation"})
        continue
    try:
        m = sitk.ReadImage(p)
        sp = np.array(m.GetSpacing(), dtype=float)
        a0 = sitk.GetArrayFromImage(m)
        n_native = int((a0 == LABEL).sum())
        vol_mm3 = float(n_native * sp.prod())
        a1 = sitk.GetArrayFromImage(resample_to_1mm(m))
        rows.append({
            "patient_id": pid,
            "n_voxels_1mm": int((a1 == LABEL).sum()),
            "n_voxels_native": n_native,
            "volume_mm3_from_native": vol_mm3,
            "spacing": [round(float(s), 4) for s in sp],
        })
    except Exception as e:
        rows.append({"patient_id": pid, "error": f"{type(e).__name__}: {str(e)[:60]}"})
    if (i + 1) % 200 == 0:
        print(f"  {i+1} processed", flush=True)

df = pd.DataFrame(rows)
errs = df[df.get("error").notna()] if "error" in df else df.iloc[0:0]
ok = df[df["n_voxels_1mm"].notna()] if "n_voxels_1mm" in df else df.iloc[0:0]
print(f"\nprocessed {len(df)}   ok {len(ok)}   errors {len(errs)}")

THRESH = [320, 640, 1280, 2560]


def describe(sub, name):
    v = sub["n_voxels_1mm"].astype(float).values
    d = {
        "cohort": name, "n": int(len(v)),
        "median": float(np.median(v)),
        "q1": float(np.percentile(v, 25)), "q3": float(np.percentile(v, 75)),
        "iqr": float(np.percentile(v, 75) - np.percentile(v, 25)),
        "min": float(v.min()), "max": float(v.max()),
        "prop_below": {str(t): float((v < t).mean()) for t in THRESH},
        "prop_at_or_above": {str(t): float((v >= t).mean()) for t in THRESH},
    }
    print(f"\n--- {name} (n={d['n']}) ---")
    print(f"  median {d['median']:.0f}   IQR [{d['q1']:.0f}, {d['q3']:.0f}]   "
          f"min {d['min']:.0f}   max {d['max']:.0f}")
    for t in THRESH:
        print(f"  < {t:5d} voxels : {d['prop_below'][str(t)]*100:6.2f} %      "
              f">= {t:5d} : {d['prop_at_or_above'][str(t)]*100:6.2f} %")
    return d


sets = {
    "HER2neg": ok[ok["patient_id"].isin(ids_neg)],
    "HER2pos": ok[ok["patient_id"].isin(ids_pos)],
    "union": ok,
}
dist = {k: describe(v, k) for k, v in sets.items()}

# ---------------- the pre-fixed rule ----------------
print("\n" + "=" * 74)
print("APPLYING THE PRE-FIXED RULE (>=95% of tumours with >=10 voxels per bin)")
print("=" * 74)
REQ = {64: 640, 32: 320}
decision = {}
for name in ("union", "HER2neg", "HER2pos"):
    v = sets[name]["n_voxels_1mm"].astype(float).values
    quals = {}
    for bc in (64, 32):
        frac = float((v >= REQ[bc]).mean())
        quals[bc] = {"frac_meeting": frac, "qualifies": bool(frac >= 0.95),
                     "required_voxels": REQ[bc]}
        print(f"  {name:8s} binCount {bc:3d} -> {frac*100:6.2f}% have >= {REQ[bc]} voxels"
              f"   {'QUALIFIES' if frac >= 0.95 else 'does not qualify'}")
    if quals[64]["qualifies"]:
        prim, sens, status = 64, 32, "OK"
    elif quals[32]["qualifies"]:
        prim, sens, status = 32, 64, "OK"
    else:
        prim, sens, status = None, None, "STOP_AND_REPORT"
    decision[name] = {"qualification": quals, "primary_binCount": prim,
                      "sensitivity_binCount": sens, "status": status}
    print(f"  {name:8s} => primary {prim}, sensitivity {sens}  [{status}]\n")

out = {
    "date": "2026-07-25", "label_counted": LABEL,
    "resample": "1 mm isotropic, sitkNearestNeighbor (label map)",
    "rule": ("largest binCount in {32,64} with >=95% of tumours having >=10 voxels/bin; "
             "64 needs >=640 voxels, 32 needs >=320"),
    "rule_fixed_before_seeing_distribution": True,
    "n_processed": int(len(df)), "n_ok": int(len(ok)), "n_errors": int(len(errs)),
    "errors": errs.to_dict("records") if len(errs) else [],
    "distribution": dist, "decision": decision,
    "DECISION_governing": decision["union"],
}
with open(OUT, "w") as f:
    json.dump(out, f, indent=1)
ok[["patient_id", "n_voxels_1mm", "n_voxels_native", "volume_mm3_from_native"]].to_csv(
    OUT.replace(".json", "_per_patient.csv"), index=False)
print(f"wrote {OUT}")
