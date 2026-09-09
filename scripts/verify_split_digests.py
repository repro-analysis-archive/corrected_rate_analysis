#!/usr/bin/env python3
"""Verify a regenerated split, sequential partition, epoch table and cohort definition against splits/SPLIT_DIGESTS.json.

Digest method (SPLIT_DIGESTS.json, field "method"): SHA-256 of the UTF-8 text obtained by sorting the patient
identifiers of a set lexicographically and joining them with a newline character, without a trailing newline.
The digests reveal no identifier; a user who has downloaded the MAMA-MIA clinical workbook regenerates the sets with
the released code and compares them here.

    python scripts/verify_split_digests.py            # after `bash scripts/run_pipeline.sh analysis` (or stage 1)

Inputs (all regenerated, none distributed): reproduction/rate_primary/split_739.csv, reproduction/rate_primary/
seq_folds_739.csv, reproduction/splits/epoch_assignment.csv, and the clinical workbook under JIIM_DATA_ROOT.
"""
import os, sys, json, hashlib
import pandas as pd

RELEASE_ROOT = os.environ.get("JIIM_RELEASE_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
DATA = os.environ.get("JIIM_DATA_ROOT", os.path.join(RELEASE_ROOT, "external_data"))
REF = json.load(open(os.path.join(RELEASE_ROOT, "splits", "SPLIT_DIGESTS.json")))

def digest(ids): return hashlib.sha256("\n".join(sorted(map(str, ids))).encode("utf-8")).hexdigest()
def sha_file(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

n_ok = n_fail = 0
def chk(name, got, want):
    global n_ok, n_fail
    ok = got == want; n_ok += ok; n_fail += (not ok)
    print(f"  {'OK  ' if ok else 'FAIL'} {name}")

sp = pd.read_csv(os.path.join(RELEASE_ROOT, "reproduction", "rate_primary", "split_739.csv"))
chk("H1 (train) identifier set", digest(sp.patient_id[sp.split == "train"]), REF["H1_train"]["sha256"])
chk("H2 (evaluation) identifier set", digest(sp.patient_id[sp.split == "eval"]), REF["H2_evaluation"]["sha256"])
chk("HER2-negative cohort identifier set", digest(sp.patient_id), REF["her2neg_cohort"]["sha256"])
sq = pd.read_csv(os.path.join(RELEASE_ROOT, "reproduction", "rate_primary", "seq_folds_739.csv"))
for k in range(1, 6):
    chk(f"sequential fold {k} identifier set", digest(sq.patient_id[sq.seq_fold == k]), REF["sequential_folds"][str(k)]["sha256"])
ep_path = os.path.join(RELEASE_ROOT, "reproduction", "splits", "epoch_assignment.csv")
chk("epoch assignment table (file sha256)", sha_file(ep_path), REF["epoch_assignment_table"]["sha256_of_file"])
ep = pd.read_csv(ep_path)
chk("empty-arm epoch (1, 21) patient set", digest(ep.patient_id[ep.epoch.isin([1, 21])]), REF["empty_arm_epoch_patients"]["sha256"])
xlsx = os.path.join(DATA, "clinical_and_imaging_info.xlsx")
if os.path.exists(xlsx):
    chk("clinical workbook sha256 (the digests are conditional on this version)", sha_file(xlsx), REF["conditional_on"]["clinical_and_imaging_info.xlsx_sha256"])
    df = pd.read_excel(xlsx); c = df[df.dataset == "ISPY2"]
    chk("HER2-positive cohort identifier set", digest(c[c.her2 == 1.0].dropna(subset=["pcr"]).patient_id), REF["her2pos_cohort"]["sha256"])
else:
    print("  skip HER2-positive cohort and workbook checks: clinical workbook not found under JIIM_DATA_ROOT")
print(f"\n{n_ok} digests verified, {n_fail} mismatches -> {'PASS' if n_fail == 0 else 'FAIL'}")
sys.exit(0 if n_fail == 0 else 1)
