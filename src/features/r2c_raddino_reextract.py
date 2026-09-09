#!/usr/bin/env python3
"""
R2c — RAD-DINO reconstruction and verification, under ANALYSIS_PLAN.md amendment 8.3a (6a969e6d).

The extraction procedure survives verbatim in a terminal transcript
(R0_freeze_audit/recovered/terminal_output_20260207_ver2:6114-6187). Only the two-line
`from_pretrained` preamble was lost to terminal line-wrap. Everything below the preamble is
replicated exactly from that transcript, with the line numbers cited.

Pooling is CLS — `outputs.last_hidden_state[:, 0, :]`, annotated `# CLS token` in the source.
Per R1, the CLS form is tried FIRST; a row-spread heuristic that pointed at mean-pooling is a
weaker signal than the annotated source and must not reorder the trials.

RULING under 8.3a (applied mechanically at the end):
  max abs diff <= 1e-12                 -> REPRODUCED, no explanation needed
  1e-12 < max abs diff <= 1e-4          -> passes numerically, but reproduction is confirmed ONLY
                                           if the residual is mechanistically accounted for
  cosine in [0.99, 0.9999)              -> NOT REPRODUCED (a similar-but-different pipeline)
  cosine < 0.99                         -> DROP

H7: cohort from the canonical patient-ID lists; output to new filenames; archive read-only.
"""
import os, sys, json, time, itertools
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
# archived embeddings of the original study (comparison targets, not redistributed): this verification script requires them
ARCHIVE = {"her2neg": f"{DATA}/archive/raddino_embeddings_739.csv", "her2pos": f"{DATA}/archive/raddino_her2pos.csv"}
# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")   # transcript: mps
print(f"Device: {device}", flush=True)

# ---- the reconstructed preamble (the only lost lines) ----
processor = AutoImageProcessor.from_pretrained(REPO, revision=REV, use_fast=True)  # PINNED [R1 pre-R3 A]:
# the transformers fast/slow default flipped between the archive run and the rebuild and was the
# single point of failure. Never rely on the default. Scope: RAD-DINO only - BiomedCLIP goes
# through open_clip, not AutoImageProcessor, and already reproduces bit-for-bit.
model = AutoModel.from_pretrained(REPO, revision=REV).to(device).eval()
print(f"RAD-DINO loaded: {type(model).__name__}, hidden {model.config.hidden_size}", flush=True)


def embed(pid, pooling="cls"):
    """Verbatim from terminal_output_20260207_ver2:6121-6136."""
    img_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{IMG}/{pid}/{pid}_0001.nii.gz"))
    seg_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{SEG}/{pid}.nii.gz"))
    ta = [(seg_arr[z] > 0).sum() for z in range(seg_arr.shape[0])]          # :6121
    bz = np.argmax(ta) if max(ta) > 0 else seg_arr.shape[0] // 2            # :6122
    sl = img_arr[bz]                                                        # :6123
    sn = ((sl - sl.min()) / (sl.max() - sl.min() + 1e-8) * 255).astype(np.uint8)   # :6124
    pil_img = Image.fromarray(np.stack([sn] * 3, axis=-1))                  # :6125
    inputs = processor(images=pil_img, return_tensors="pt").to(device)      # :6127
    with torch.no_grad():
        o = model(**inputs)                                                 # :6129
        if pooling == "cls":
            return o.last_hidden_state[:, 0, :].cpu().numpy().flatten()     # :6136  <- CLS
        if pooling == "mean_patch":
            return o.last_hidden_state[:, 1:, :].mean(1).cpu().numpy().flatten()
        if pooling == "pooler":
            return o.pooler_output.cpu().numpy().flatten()
    raise ValueError(pooling)


def compare(A, B):
    num = (A * B).sum(1); den = np.linalg.norm(A, axis=1) * np.linalg.norm(B, axis=1)
    cos = num / den
    return {"cosine_median": float(np.median(cos)), "cosine_min": float(cos.min()),
            "cos_lt_0.9999": int((cos < 0.9999).sum()), "cos_lt_0.99": int((cos < 0.99).sum()),
            "max_abs_diff": float(np.abs(A - B).max()),
            "median_abs_diff": float(np.median(np.abs(A - B)))}


def rule_8_3a(m):
    d, cmin = m["max_abs_diff"], m["cosine_min"]
    if cmin < 0.99:
        return "DROP", "cosine below 0.99"
    if cmin < 0.9999:
        return "NOT_REPRODUCED", ("cosine in [0.99, 0.9999): a similar-but-different pipeline "
                                  "(8.3a reclassification)")
    if d <= 1e-12:
        return "REPRODUCED", "max abs diff <= 1e-12; no explanation required"
    if d <= 1e-4:
        return "REPRODUCED_PENDING_MECHANISM", ("numeric thresholds pass but residual is "
                                                f"{d:.3e}; 8.3a requires the residual be "
                                                "mechanistically accounted for")
    return "NOT_REPRODUCED", f"max abs diff {d:.3e} exceeds 1e-4"


report = {"date": "2026-07-25", "device": str(device), "repo": REPO, "revision": REV,
          "amendment": "8.3a (commit 6a969e6d3e3cdd6b8574e1082301077c3b9d2ef2)",
          "pooling_trial_order": ["cls", "mean_patch", "pooler"], "cohorts": {}}

for coh in ("her2neg", "her2pos"):
    ids = cohort_ids(coh, CLINICAL_XLSX)
    arch = pd.read_csv(ARCHIVE[coh]).set_index("patient_id").loc[ids]
    cols = list(arch.columns)
    A = arch.values.astype(np.float64)
    print(f"\n=== {coh}: {len(ids)} patients, archive {arch.shape} ===", flush=True)

    res_coh = {"n": len(ids), "archive_shape": [len(arch), len(cols)], "trials": {}}
    for pooling in ("cls", "mean_patch", "pooler"):
        try:
            t0 = time.time(); rows, fails = [], []
            for i, pid in enumerate(ids):
                try:
                    rows.append(embed(pid, pooling))
                except Exception as e:
                    fails.append((pid, f"{type(e).__name__}: {str(e)[:60]}")); rows.append(None)
                if (i + 1) % 200 == 0:
                    print(f"  [{pooling}] {i+1}/{len(ids)} {time.time()-t0:.0f}s", flush=True)
            if any(r is None for r in rows):
                res_coh["trials"][pooling] = {"error": f"{len(fails)} failures", "fails": fails[:5]}
                continue
            B = np.vstack(rows).astype(np.float64)
            if B.shape[1] != A.shape[1]:
                res_coh["trials"][pooling] = {"dim": int(B.shape[1]), "archive_dim": int(A.shape[1]),
                                              "verdict": "DIM_MISMATCH"}
                print(f"  {pooling}: dim {B.shape[1]} vs archive {A.shape[1]} — skip", flush=True)
                continue
            m = compare(A, B); v, why = rule_8_3a(m)
            m.update({"verdict": v, "reason": why, "elapsed_s": round(time.time() - t0, 1),
                      "n_failed": len(fails)})
            res_coh["trials"][pooling] = m
            print(f"  {pooling}: cos_med {m['cosine_median']:.15f} cos_min {m['cosine_min']:.15f} "
                  f"maxdiff {m['max_abs_diff']:.3e} -> {v}", flush=True)
            if v.startswith("REPRODUCED"):
                pd.DataFrame(B, columns=cols).assign(patient_id=ids)[["patient_id"] + cols].to_csv(
                    f"{OUT}/raddino_{coh}_reextract_{pooling}_20260725.csv", index=False)
                res_coh["accepted_pooling"] = pooling
                break        # CLS first; stop at the first form that reproduces
        except Exception as e:
            res_coh["trials"][pooling] = {"error": f"{type(e).__name__}: {str(e)[:120]}"}
            print(f"  {pooling}: ERROR {e}", flush=True)
    report["cohorts"][coh] = res_coh

acc = {c: r.get("accepted_pooling") for c, r in report["cohorts"].items()}
report["accepted_pooling_by_cohort"] = acc
report["OVERALL"] = ("REPRODUCED" if all(acc.values()) and len(set(v for v in acc.values() if v)) == 1
                     else "SEE_TRIALS")
with open(f"{OUT}/r2c_raddino_verification.json", "w") as f:
    json.dump(report, f, indent=1)
print(f"\naccepted pooling: {acc}\nOVERALL: {report['OVERALL']}")
print("wrote r2c_raddino_verification.json")
