#!/usr/bin/env python3
"""
R2c mechanism test — CLS pooling with `use_fast=True`.

The single mechanism hypothesised IN ADVANCE (R1 post-R2a, before the result was known):

  archive run 2026-02-07 logged: "The image processor of type `BitImageProcessor` is now loaded as
                                  a FAST processor by default"
  reconstruction on transformers 4.57.6 logged: "Using a SLOW image processor as `use_fast` is unset"

The transformers default flipped between versions. The archive therefore used the fast processor;
the first reconstruction used the slow one. Fast and slow BitImageProcessor differ in resize/rescale
implementation, which is a real preprocessing difference of the observed magnitude.

Verdict table, fixed by R1 BEFORE this ran:
  max abs diff <= 1e-12                      -> REPRODUCED (mechanism identified and corrected)
  1e-12 < max abs diff <= 1e-4, others pass  -> REPRODUCED WITH MECHANISM ACCOUNTED FOR
  max abs diff > 1e-4                        -> NOT REPRODUCED; RAD-DINO withdrawn, HER2+ reduced
                                                (and NO further search over preprocessing variants)

Pooling is CLS only. mean_patch and pooler were run as diagnostics and may not be adopted on the
basis of better agreement.
"""
import os, json, time
import numpy as np
import pandas as pd
import SimpleITK as sitk
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModel

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
OUT = f"{DATA}/features"; os.makedirs(OUT, exist_ok=True)
REPO, REV = "microsoft/rad-dino", "2ec9ca0e7a73c23aded999b844acd2f07c7e46b9"
# archived embeddings of the original study: comparison targets only, not redistributed (comparison is skipped if absent)
ARCHIVE = {"her2neg": f"{DATA}/archive/raddino_embeddings_739.csv", "her2pos": f"{DATA}/archive/raddino_her2pos.csv"}
# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
proc_fast = AutoImageProcessor.from_pretrained(REPO, revision=REV, use_fast=True)
model = AutoModel.from_pretrained(REPO, revision=REV).to(device).eval()
print(f"device {device} | processor {type(proc_fast).__name__} (use_fast=True)", flush=True)


def embed(pid, processor):
    img_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{IMG}/{pid}/{pid}_0001.nii.gz"))
    seg_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{SEG}/{pid}.nii.gz"))
    ta = [(seg_arr[z] > 0).sum() for z in range(seg_arr.shape[0])]
    bz = np.argmax(ta) if max(ta) > 0 else seg_arr.shape[0] // 2
    sl = img_arr[bz]
    sn = ((sl - sl.min()) / (sl.max() - sl.min() + 1e-8) * 255).astype(np.uint8)
    pil = Image.fromarray(np.stack([sn] * 3, axis=-1))
    inp = processor(images=pil, return_tensors="pt").to(device)
    with torch.no_grad():
        return model(**inp).last_hidden_state[:, 0, :].cpu().numpy().flatten()   # CLS


def compare(A, B):
    cos = (A * B).sum(1) / (np.linalg.norm(A, axis=1) * np.linalg.norm(B, axis=1))
    ad = np.abs(A - B)
    relL2 = np.linalg.norm(A - B, axis=1) / np.linalg.norm(A, axis=1)
    return {"cosine_median": float(np.median(cos)), "cosine_min": float(cos.min()),
            "cos_lt_0.9999": int((cos < 0.9999).sum()), "cos_lt_0.99": int((cos < 0.99).sum()),
            "max_abs_diff": float(ad.max()), "median_abs_diff": float(np.median(ad)),
            "rel_L2_max": float(relL2.max()), "rel_L2_median": float(np.median(relL2))}


def verdict(m):
    if m["cosine_min"] < 0.99:
        return "DROP", "cosine below 0.99"
    if m["cosine_min"] < 0.9999:
        return "NOT_REPRODUCED", "cosine in [0.99, 0.9999) — 8.3a reclassification"
    d = m["max_abs_diff"]
    if d <= 1e-12:
        return "REPRODUCED", "max abs diff <= 1e-12; mechanism identified and corrected"
    if d <= 1e-4:
        return "REPRODUCED_MECHANISM_ACCOUNTED", (
            f"residual {d:.3e} within 1e-4; attributable to the transformers fast/slow "
            "BitImageProcessor default flip between the archive run and the rebuild")
    return "NOT_REPRODUCED", f"max abs diff {d:.3e} exceeds 1e-4 even with the mechanism corrected"


rep = {"date": "2026-07-25", "device": str(device), "pooling": "cls",
       "mechanism_tested": "use_fast=True (transformers default flipped between versions)",
       "hypothesis_fixed_in_advance": True, "cohorts": {}}

for coh in ("her2neg", "her2pos"):
    ids = cohort_ids(coh, CLINICAL_XLSX)
    have_archive = os.path.exists(ARCHIVE[coh])          # public release: comparison only if the archive is present
    t0 = time.time()
    B = np.vstack([embed(p, proc_fast) for p in ids]).astype(np.float64)
    if not have_archive:
        cols = [f"raddino_{j:03d}" for j in range(B.shape[1])]
        pd.DataFrame(B, columns=cols).assign(patient_id=ids)[["patient_id"] + cols].to_csv(
            f"{OUT}/raddino_{coh}_reextract_cls_usefast_20260725.csv", index=False)
        rep["cohorts"][coh] = {"n": len(ids), "elapsed_s": round(time.time() - t0, 1),
                               "comparison": "SKIPPED: archived embeddings of the original study not available"}
        print(f"{coh}: extracted {B.shape}; archive comparison skipped", flush=True)
        continue
    arch = pd.read_csv(ARCHIVE[coh]).set_index("patient_id").loc[ids]
    A = arch.values.astype(np.float64)
    m = compare(A, B); v, why = verdict(m)
    m.update({"verdict": v, "reason": why, "n": len(ids), "elapsed_s": round(time.time() - t0, 1)})
    rep["cohorts"][coh] = m
    print(f"\n{coh}: cos_med {m['cosine_median']:.15f}  cos_min {m['cosine_min']:.15f}")
    print(f"  max_abs_diff {m['max_abs_diff']:.3e}   rel_L2 max {m['rel_L2_max']:.3e}")
    print(f"  -> {v}: {why}", flush=True)
    if v.startswith("REPRODUCED"):
        pd.DataFrame(B, columns=list(arch.columns)).assign(patient_id=ids)[
            ["patient_id"] + list(arch.columns)].to_csv(
            f"{OUT}/raddino_{coh}_reextract_cls_usefast_20260725.csv", index=False)
        # re-run consistency within the same environment
        B2 = np.vstack([embed(p, proc_fast) for p in ids]).astype(np.float64)
        rep["cohorts"][coh]["rerun_identical"] = bool(np.array_equal(B, B2))
        rep["cohorts"][coh]["rerun_max_abs_diff"] = float(np.abs(B - B2).max())
        print(f"  rerun consistency: identical={np.array_equal(B, B2)} "
              f"maxdiff={np.abs(B-B2).max():.3e}", flush=True)

vs = [c.get("verdict", "SKIPPED") for c in rep["cohorts"].values()]
rep["OVERALL"] = ("EXTRACTED_NO_COMPARISON" if any(v == "SKIPPED" for v in vs)
                  else "REPRODUCED" if all(v == "REPRODUCED" for v in vs)
                  else "REPRODUCED_MECHANISM_ACCOUNTED" if all(v.startswith("REPRODUCED") for v in vs)
                  else "NOT_REPRODUCED")
with open(f"{OUT}/r2c_usefast_result.json", "w") as f:
    json.dump(rep, f, indent=1)
print(f"\nOVERALL: {rep['OVERALL']}")
