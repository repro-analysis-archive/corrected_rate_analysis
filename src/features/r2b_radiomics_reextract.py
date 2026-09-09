#!/usr/bin/env python3
"""
R2b — corrected radiomics extraction, per ANALYSIS_PLAN.md §7.2 (commit bb70d54).

    binCount = 64 (fixed bin NUMBER)   normalize = False
    resampledPixelSpacing = [1,1,1] mm, B-spline (image); mask nearest-neighbour (pyradiomics)
    force2D = False (3D)               label = 1

H7 FIX: cohort taken EXPLICITLY from the canonical patient-ID lists, never from directory state.
Output goes to NEW filenames under JIIM_Revision/R2_features/. The archived CSVs are read-only.

Also records, per patient, the EFFECTIVE NON-EMPTY bin count — Q1/Q2 are defined on effective bins,
not on the nominal binCount, which under FBN is 64 by construction and would test nothing.
"""
import os, sys, json, time
import numpy as np
import pandas as pd
import SimpleITK as sitk
import radiomics
from radiomics import featureextractor, imageoperations
import logging
radiomics.logger.setLevel(logging.ERROR)
import warnings; warnings.filterwarnings("ignore")

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
OUT = f"{DATA}/features"; os.makedirs(OUT, exist_ok=True)
# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed

BIN_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 64
SETTINGS = {
    "binCount": BIN_COUNT,
    "normalize": False,
    "resampledPixelSpacing": [1.0, 1.0, 1.0],
    "interpolator": sitk.sitkBSpline,
    "force2D": False,
    "label": 1,
}
print(f"pyradiomics {radiomics.__version__}")
print(f"SETTINGS {SETTINGS}", flush=True)

extractor = featureextractor.RadiomicsFeatureExtractor(**SETTINGS)
extractor.enableAllFeatures()


def effective_bins(img, mask):
    """Non-empty bin count after resampling + FBN discretisation, replicating pyradiomics."""
    try:
        i2, m2 = imageoperations.resampleImage(img, mask, **SETTINGS)
        a = sitk.GetArrayFromImage(i2)[sitk.GetArrayFromImage(m2) == 1]
        if a.size == 0:
            return None, 0
        edges = imageoperations.getBinEdges(a, **SETTINGS)
        return int(len(np.unique(np.digitize(a, edges)))), int(a.size)
    except Exception:
        return None, 0


allrows, allbins, failed = {}, [], {}
for coh in ("her2neg", "her2pos"):
    ids = cohort_ids(coh, CLINICAL_XLSX)
    print(f"\n=== {coh}: {len(ids)} patients (canonical) ===", flush=True)
    rows, fails, t0 = [], [], time.time()
    for i, pid in enumerate(ids):
        ip, sp = f"{IMG}/{pid}/{pid}_0001.nii.gz", f"{SEG}/{pid}.nii.gz"
        try:
            img, mask = sitk.ReadImage(ip), sitk.ReadImage(sp)
            nb, nv = effective_bins(img, mask)
            allbins.append({"patient_id": pid, "cohort": coh,
                            "effective_bins": nb, "n_voxels_resampled": nv})
            res = extractor.execute(ip, sp)
            row = {"patient_id": pid}
            for k, v in res.items():
                if k.startswith("original_"):
                    try:
                        row[k] = float(v)
                    except Exception:
                        pass
            rows.append(row)
        except Exception as e:
            fails.append((pid, f"{type(e).__name__}: {str(e)[:70]}"))
        if (i + 1) % 50 == 0:
            el = time.time() - t0
            print(f"  [{i+1}/{len(ids)}] {el:.0f}s  eta {(len(ids)-i-1)*el/(i+1)/60:.1f}min  "
                  f"failed={len(fails)}", flush=True)
    df = pd.DataFrame(rows)
    allrows[coh], failed[coh] = df, fails
    p = f"{OUT}/radiomics_{coh}_binCount{BIN_COUNT}_20260725.csv"
    df.to_csv(p, index=False)
    print(f"  {coh}: {df.shape} in {time.time()-t0:.0f}s, failed {len(fails)} -> {p}", flush=True)

pd.DataFrame(allbins).to_csv(f"{OUT}/r2b_effective_bins_binCount{BIN_COUNT}.csv", index=False)
meta = {"date": "2026-07-25", "pyradiomics": radiomics.__version__,
        "settings": {k: (str(v) if k == "interpolator" else v) for k, v in SETTINGS.items()},
        "cohort_source": "explicit canonical ID lists (H7 fix)",
        "shapes": {k: list(v.shape) for k, v in allrows.items()},
        "failures": {k: v for k, v in failed.items()}}
with open(f"{OUT}/r2b_extraction_meta_binCount{BIN_COUNT}.json", "w") as f:
    json.dump(meta, f, indent=1)
print("\n=== R2b extraction complete ===")
print(json.dumps(meta["shapes"]))
