#!/usr/bin/env python3
"""
R2a — BiomedCLIP provenance verification: re-extract and compare against the archive.

H7 FIX (mandatory, R1 §11). The archived extractor defined its cohort as
`os.listdir(images)` filtered on file existence — "whatever is on disk". That glob returns 980
today but returned 739 when it ran, because the HER2+ images had not been downloaded yet. It then
wrote back to `biomedclip_embeddings_739.csv`. Here:

  * the cohort is taken EXPLICITLY from the canonical patient-ID lists, never from directory state
  * output goes to NEW filenames under JIIM_Revision/R2_features/, never over the archive
  * the archived CSVs are opened read-only

Everything else replicates extract_embeddings.py line for line (cited below), because R2a asks
whether the archive is reproducible — not whether it can be improved.
"""
import os, sys, json, time
import numpy as np
import pandas as pd
import SimpleITK as sitk
from PIL import Image
import torch
import open_clip

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))   # source data and feature matrices (not redistributed)
CLINICAL_XLSX = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from cohort_ids import cohort_ids   # cohorts derived from the workbook; no identifier list is distributed
IMG, SEG = f"{DATA}/images", f"{DATA}/segmentations"
OUT = f"{DATA}/features"
os.makedirs(OUT, exist_ok=True)

# archived embeddings of the original study: comparison targets only, not redistributed (comparison is skipped if absent)
ARCHIVE = {"her2neg": f"{DATA}/archive/biomedclip_embeddings_739.csv",
           "her2pos": f"{DATA}/archive/biomedclip_her2pos.csv"}
# cohort membership: derived from the clinical workbook by cohort_ids(); no identifier list is read or distributed

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Device: {device}", flush=True)
model, _, preprocess_val = open_clip.create_model_and_transforms(
    'hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')          # line 13-15
model = model.to(device).eval()
print("BiomedCLIP loaded", flush=True)


def embed(pid):
    """Verbatim replication of extract_embeddings.py lines 37-58."""
    img_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{IMG}/{pid}/{pid}_0001.nii.gz"))
    seg_arr = sitk.GetArrayFromImage(sitk.ReadImage(f"{SEG}/{pid}.nii.gz"))
    tumor_area = [(seg_arr[z] > 0).sum() for z in range(seg_arr.shape[0])]      # line 44
    best_z = np.argmax(tumor_area)                                             # line 45
    if max(tumor_area) == 0:                                                   # line 48-49
        best_z = seg_arr.shape[0] // 2
    slice_2d = img_arr[best_z]                                                 # line 51
    slice_norm = ((slice_2d - slice_2d.min()) /
                  (slice_2d.max() - slice_2d.min() + 1e-8) * 255).astype(np.uint8)   # line 52
    slice_rgb = np.stack([slice_norm] * 3, axis=-1)                            # line 53
    pil_img = Image.fromarray(slice_rgb)                                       # line 54
    t = preprocess_val(pil_img).unsqueeze(0).to(device)                        # line 56
    with torch.no_grad():
        return model.encode_image(t).cpu().numpy().flatten()                   # line 58


report = {"date": "2026-07-25", "device": str(device),
          "checkpoint": "hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224",
          "checkpoint_revision": "9f341de24bfb00180f1b847274256e9b65a3a32e",
          "cohort_source": "explicit canonical ID lists (H7 fix)", "cohorts": {}}

for coh in ("her2neg", "her2pos"):
    ids = cohort_ids(coh, CLINICAL_XLSX)
    have_archive = os.path.exists(ARCHIVE[coh])          # public release: comparison only if the archive is present
    arch = pd.read_csv(ARCHIVE[coh]) if have_archive else None
    cols = [c for c in arch.columns if c != "patient_id"] if have_archive else None
    print(f"\n=== {coh}: {len(ids)} patients (canonical), archive {arch.shape if have_archive else "not available"} ===", flush=True)

    rows, failed, t0 = [], [], time.time()
    for i, pid in enumerate(ids):
        try:
            e = embed(pid)
            rows.append({"patient_id": pid, **{f"emb_{j:03d}": float(v) for j, v in enumerate(e)}})
        except Exception as ex:
            failed.append((pid, f"{type(ex).__name__}: {str(ex)[:70]}"))
        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{len(ids)}] {time.time()-t0:.0f}s failed={len(failed)}", flush=True)
    new = pd.DataFrame(rows)
    dt = time.time() - t0
    print(f"  done {new.shape} in {dt:.0f}s, failed {len(failed)}", flush=True)

    newpath = f"{OUT}/biomedclip_{coh}_reextract_20260725.csv"
    new.to_csv(newpath, index=False)
    if not have_archive:
        report["cohorts"][coh] = {"n_canonical": len(ids), "n_extracted": int(len(new)), "n_failed": len(failed),
                                  "failures": failed[:10], "elapsed_s": round(dt, 1), "output": newpath,
                                  "comparison": "SKIPPED: archived embeddings of the original study not available"}
        continue

    # ---- comparison ----
    a = arch.set_index("patient_id").loc[new["patient_id"]]        # align archive to new order
    A = a[cols].values.astype(np.float64)
    B = new[[c for c in new.columns if c != "patient_id"]].values.astype(np.float64)

    id_match = list(a.index) == list(new["patient_id"])
    same_set = set(arch["patient_id"]) == set(new["patient_id"])
    same_order_as_archive = list(arch["patient_id"]) == list(new["patient_id"])

    num = (A * B).sum(1)
    den = np.linalg.norm(A, axis=1) * np.linalg.norm(B, axis=1)
    cos = num / den
    absdiff = np.abs(A - B)

    # downstream PCA agreement (30 comps, as the pipeline uses)
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from scipy.stats import spearmanr
    pa = PCA(30, random_state=42).fit_transform(StandardScaler().fit_transform(A))
    pb = PCA(30, random_state=42).fit_transform(StandardScaler().fit_transform(B))
    rhos = [abs(spearmanr(pa[:, k], pb[:, k]).statistic) for k in range(30)]

    r = {
        "n_canonical": len(ids), "n_extracted": int(len(new)), "n_failed": len(failed),
        "failures": failed[:10],
        "archive_shape": list(arch.shape), "reextract_shape": list(new.shape),
        "dim": int(B.shape[1]), "dim_matches_archive": int(B.shape[1]) == len(cols),
        "patient_id_set_identical": bool(same_set),
        "row_order_identical_to_archive": bool(same_order_as_archive),
        "aligned_for_comparison": bool(id_match),
        "cosine_median": float(np.median(cos)), "cosine_min": float(cos.min()),
        "cosine_mean": float(cos.mean()),
        "cosine_below_0.9999": int((cos < 0.9999).sum()),
        "cosine_below_0.99": int((cos < 0.99).sum()),
        "max_abs_elementwise_diff": float(absdiff.max()),
        "median_abs_elementwise_diff": float(np.median(absdiff)),
        "pca30_spearman_min": float(np.min(rhos)),
        "pca30_spearman_median": float(np.median(rhos)),
        "pca30_components_below_0.99": int(sum(1 for x in rhos if x < 0.99)),
        "elapsed_s": round(dt, 1), "output": newpath,
    }
    # thresholds from ANALYSIS_PLAN.md 8.3
    r["PASS_median_cosine_ge_0.99999"] = bool(r["cosine_median"] >= 0.99999)
    r["PASS_min_cosine_ge_0.9999"] = bool(r["cosine_min"] >= 0.9999)
    r["PASS_maxabs_le_1e-4"] = bool(r["max_abs_elementwise_diff"] <= 1e-4)
    r["PASS_pca_spearman_ge_0.99"] = bool(r["pca30_spearman_min"] >= 0.99)
    r["VERDICT"] = ("REPRODUCED" if all([r["PASS_min_cosine_ge_0.9999"], r["PASS_pca_spearman_ge_0.99"]])
                    else "GREY_ZONE" if r["cosine_min"] >= 0.99 else "NOT_REPRODUCED")
    report["cohorts"][coh] = r
    for k in ("cosine_median", "cosine_min", "max_abs_elementwise_diff",
              "pca30_spearman_min", "VERDICT"):
        print(f"    {k:28s} {r[k]}")

with open(f"{OUT}/r2a_biomedclip_verification.json", "w") as f:
    json.dump(report, f, indent=1)
print("\nwrote r2a_biomedclip_verification.json")
