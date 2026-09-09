#!/usr/bin/env python3
"""
Recompute the effective-bins / voxel-count diagnostic. FIX ONLY — no binning parameter changes.

Bug: the segmentation masks are stored as 32-bit float. SimpleITK's LabelShapeStatisticsImageFilter
rejects float in 3D, so `imageoperations.resampleImage` raised inside the helper's bare `except`,
which returned (None, 0). That made n_voxels_resampled zero for most patients and Q9 read 96% FAIL
on a metric that was measuring nothing.

Pyradiomics' own extractor casts the mask internally, which is why `extractor.execute` succeeded for
all 980 and the extracted features are unaffected. Only this auxiliary diagnostic was wrong.

Fix: cast the mask to UInt8 before resampling, exactly as pyradiomics does, and let exceptions
surface instead of being swallowed.
"""
import os, sys
import numpy as np
import pandas as pd
import SimpleITK as sitk
import radiomics, logging
from radiomics import imageoperations
radiomics.logger.setLevel(logging.ERROR)
import warnings; warnings.filterwarnings("ignore")

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
OUT = f"{DATA}/features"; os.makedirs(OUT, exist_ok=True)
BC = int(sys.argv[1]) if len(sys.argv) > 1 else 64
SETTINGS = {"binCount": BC, "normalize": False, "resampledPixelSpacing": [1.0, 1.0, 1.0],
            "interpolator": sitk.sitkBSpline, "force2D": False, "label": 1}
# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed

rows, errs = [], []
for coh in ("her2neg", "her2pos"):
    ids = cohort_ids(coh, CLINICAL_XLSX)
    print(f"{coh}: {len(ids)}", flush=True)
    for i, pid in enumerate(ids):
        try:
            img = sitk.ReadImage(f"{IMG}/{pid}/{pid}_0001.nii.gz")
            mask = sitk.ReadImage(f"{SEG}/{pid}.nii.gz")
            mask = sitk.Cast(mask, sitk.sitkUInt8)            # <-- the fix
            i2, m2 = imageoperations.resampleImage(img, mask, **SETTINGS)
            a = sitk.GetArrayFromImage(i2)[sitk.GetArrayFromImage(m2) == 1]
            if a.size == 0:
                errs.append((pid, "empty ROI after resample")); continue
            edges = imageoperations.getBinEdges(a, **SETTINGS)
            nb = int(len(np.unique(np.digitize(a, edges))))
            rows.append({"patient_id": pid, "cohort": coh, "effective_bins": nb,
                         "n_voxels_resampled": int(a.size),
                         "voxels_per_bin": float(a.size) / BC})
        except Exception as e:
            errs.append((pid, f"{type(e).__name__}: {str(e)[:70]}"))
        if (i + 1) % 200 == 0:
            print(f"  {i+1}", flush=True)

df = pd.DataFrame(rows)
df.to_csv(f"{OUT}/r2b_effective_bins_binCount{BC}.csv", index=False)
print(f"\ncomputed {len(df)} / 980, errors {len(errs)}")
for e in errs[:5]:
    print("  ", e)
if len(df):
    print(f"effective_bins     median {df.effective_bins.median():.0f}  "
          f"IQR [{df.effective_bins.quantile(.25):.0f}, {df.effective_bins.quantile(.75):.0f}]  "
          f"min {df.effective_bins.min():.0f}  max {df.effective_bins.max():.0f}")
    print(f"n_voxels_resampled median {df.n_voxels_resampled.median():.0f}  "
          f"min {df.n_voxels_resampled.min():.0f}")
    print(f"voxels_per_bin     median {df.voxels_per_bin.median():.1f}  "
          f"prop < 10: {(df.voxels_per_bin < 10).mean():.4f}")
